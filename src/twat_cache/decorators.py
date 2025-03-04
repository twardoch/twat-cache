#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "loguru",
#   "functools",
#   "diskcache",
#   "joblib",
#   "types-diskcache",
#   "pydantic",
#   "aiocache",
#   "cachetools",
#   "cachebox",
#   "klepto",
#   "types-cachetools",
# ]
# ///
# this_file: src/twat_cache/decorators.py

"""
Core caching decorators.

This module provides five main decorators:
- mcache: Memory-based caching using fastest available backend (with fallback to functools)
- bcache: Basic disk caching using diskcache (with fallback to memory)
- fcache: Fast file-based caching using joblib (with fallback to memory)
- acache: Async-capable caching using aiocache (with fallback to async wrapper)
- ucache: Universal caching that automatically selects best available backend

These decorators provide a simple interface for caching function results with various
backends, automatically handling fallbacks if preferred backends are not available.
"""

import asyncio
import functools
import json
from pathlib import Path
from typing import (
    Any,
    cast,
    Protocol,
)
from collections.abc import Callable, Awaitable
import importlib.util


from .config import create_cache_config, CacheConfig, EvictionPolicy
from .engines.base import BaseCacheEngine
from .engines.functools import FunctoolsCacheEngine
from .type_defs import P, R, AsyncR, CacheDecorator as CacheDecoratorType


class CacheDecorator(Protocol[P, R]):
    """
    Protocol for cache decorators.

    This protocol defines the interface for cache decorators that can be applied
    to synchronous functions. Cache decorators wrap functions to store and retrieve
    results based on input parameters.
    """

    def __call__(self, func: Callable[P, R]) -> Callable[P, R]: ...


class AsyncCacheDecorator(Protocol[P, AsyncR]):
    """
    Protocol for async cache decorators.

    This protocol defines the interface for cache decorators that can be applied
    to asynchronous functions. Async cache decorators wrap coroutine functions to
    store and retrieve results based on input parameters.
    """

    def __call__(
        self, func: Callable[P, AsyncR] | Callable[P, Awaitable[AsyncR]]
    ) -> Callable[P, Awaitable[AsyncR]]: ...


# Check optional backend availability
HAS_AIOCACHE = bool(importlib.util.find_spec("aiocache"))
HAS_CACHEBOX = bool(importlib.util.find_spec("cachebox"))
HAS_CACHETOOLS = bool(importlib.util.find_spec("cachetools"))
HAS_DISKCACHE = bool(importlib.util.find_spec("diskcache"))
HAS_JOBLIB = bool(importlib.util.find_spec("joblib"))
HAS_KLEPTO = bool(importlib.util.find_spec("klepto"))


def get_cache_dir(folder_name: str | None = None) -> Path:
    """
    Get or create cache directory.

    Creates a cache directory for storing cached data. The directory is created
    under the user's home directory in `.cache/twat_cache/[folder_name]`.
    If the directory already exists, it is returned as is.

    Args:
        folder_name: Optional name for the cache folder. If None, 'default' is used.
            Must contain only alphanumeric characters, dash, underscore, and dot.

    Returns:
        Path: Path object pointing to the cache directory.

    Raises:
        ValueError: If folder_name contains invalid characters.
        OSError: If directory creation fails due to permission issues or disk errors.

    Example:
        >>> cache_dir = get_cache_dir("my_app")
        >>> print(cache_dir)
        /home/user/.cache/twat_cache/my_app
    """
    if folder_name and not all(c.isalnum() or c in "-_." for c in folder_name):
        msg = f"Invalid folder name '{folder_name}'. Use only alphanumeric chars, dash, underscore and dot"
        raise ValueError(msg)

    base_dir = Path.home() / ".cache" / "twat_cache"
    cache_dir = base_dir / (folder_name or "default")

    try:
        cache_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        msg = f"Failed to create cache directory {cache_dir}: {e}"
        raise OSError(msg) from e

    return cache_dir


def make_key(serializer: Callable[[Any], str] | None = None, *args: Any, **kwargs: Any) -> str:
    """
    Create a cache key from function arguments.

    Generates a unique string key based on the provided arguments. This key is used
    to identify cached values. The function handles serialization of arguments to
    ensure consistent key generation.

    Args:
        serializer: Optional function to serialize non-JSON-serializable objects.
            If None, a default serializer is used that converts objects to strings.
        *args: Positional arguments to include in the key.
        **kwargs: Keyword arguments to include in the key.

    Returns:
        str: A string key that uniquely identifies the arguments.

    Example:
        >>> make_key(None, 1, 2, name="test")
        '[[1, 2], {"name": "test"}]'

        >>> # With custom serializer
        >>> def my_serializer(obj):
        ...     if isinstance(obj, complex):
        ...         return [obj.real, obj.imag]
        ...     return str(obj)
        >>> make_key(my_serializer, complex(1, 2), name="test")
        '[[[1.0, 2.0]], {"name": "test"}]'
    """

    def default_serializer(obj: Any) -> Any:
        if isinstance(obj, str | int | float | bool | type(None)):
            return obj
        return str(obj)

    ser = serializer or default_serializer

    # Convert args and kwargs to stable forms
    converted_args = tuple(ser(arg) for arg in args)
    converted_kwargs = {k: ser(v) for k, v in sorted(kwargs.items())}

    # Create a stable string representation
    return json.dumps((converted_args, converted_kwargs), sort_keys=True)


def mcache(
    maxsize: int | None = None,
    ttl: float | None = None,
    policy: str = "lru",
    *,  # Force remaining arguments to be keyword-only
    secure: bool = True,
) -> CacheDecorator[P, R]:
    """
    Memory-based caching using fastest available backend.

    Creates a decorator that caches function results in memory using the best
    available backend. The function automatically falls back to simpler backends
    if preferred ones are not available.

    Args:
        maxsize: Maximum number of items to store in the cache. None means unlimited,
            but this may lead to memory issues for long-running applications.
        ttl: Time-to-live in seconds. None means entries never expire. Use this to
            automatically invalidate cached results after a certain time.
        policy: Cache eviction policy when maxsize is reached. Options include:
            - "lru": Least Recently Used (default)
            - "fifo": First In First Out
            - "lifo": Last In First Out
            - "mru": Most Recently Used
            - "lfu": Least Frequently Used
        secure: Whether to use secure file permissions for any temporary files.
            Set to False only in trusted environments where performance is critical.

    Returns:
        CacheDecorator: A decorator that can be applied to functions to cache their results.

    Raises:
        ValueError: If an invalid policy is specified.

    Example:
        >>> @mcache(maxsize=100, ttl=3600)  # Cache up to 100 results for 1 hour
        ... def expensive_calculation(x, y):
        ...     print(f"Computing {x} + {y}")
        ...     return x + y
        >>>
        >>> expensive_calculation(1, 2)  # This will compute and cache
        Computing 1 + 2
        3
        >>> expensive_calculation(1, 2)  # This will use cached result
        3
    """
    config = create_cache_config(
        maxsize=maxsize,
        ttl=ttl,
        policy=policy,
        cache_type="memory",
        secure=secure,
    )

    if HAS_CACHEBOX:
        from .engines import cachebox

        engine: BaseCacheEngine[P, R] = cachebox.CacheBoxEngine(config)  # type: ignore[abstract]
        return cast(CacheDecorator[P, R], engine.cache)
    elif HAS_CACHETOOLS:
        from .engines import cachetools

        engine = cachetools.CacheToolsEngine(config)  # type: ignore[abstract]
        return cast(CacheDecorator[P, R], engine.cache)
    else:
        from .engines import functools_engine

        engine = functools_engine.FunctoolsCacheEngine(config)  # type: ignore[abstract]
        return cast(CacheDecorator[P, R], engine.cache)


def bcache(
    folder_name: str | None = None,
    maxsize: int | None = None,
    ttl: float | None = None,
    policy: str = "lru",
    *,  # Force remaining arguments to be keyword-only
    use_sql: bool = True,
    secure: bool = True,
) -> CacheDecorator[P, R]:
    """
    Basic disk caching using database backends.

    Creates a decorator that caches function results on disk using database backends.
    This is useful for persistent caching across program runs and for larger datasets
    that may not fit in memory.

    Args:
        folder_name: Name of the folder to store cache files. If None, 'default' is used.
            Must contain only alphanumeric characters, dash, underscore, and dot.
        maxsize: Maximum size of the cache in bytes. None means unlimited.
            For disk caches, this helps prevent excessive disk usage.
        ttl: Time-to-live in seconds. None means entries never expire.
            Use this to automatically invalidate cached results after a certain time.
        policy: Cache eviction policy when maxsize is reached. Options include:
            - "lru": Least Recently Used (default)
            - "fifo": First In First Out
            - "lifo": Last In First Out
            - "mru": Most Recently Used
            - "lfu": Least Frequently Used
        use_sql: Whether to use SQL-based disk cache for better performance with
            large datasets. Set to False for simpler file-based storage.
        secure: Whether to use secure file permissions. Set to False only in
            trusted environments where performance is critical.

    Returns:
        CacheDecorator: A decorator that can be applied to functions to cache their results.

    Raises:
        ValueError: If folder_name contains invalid characters or if an invalid policy is specified.
        OSError: If cache directory creation fails.

    Example:
        >>> @bcache(folder_name="my_calculations", ttl=86400)  # Cache for 1 day
        ... def expensive_calculation(x, y):
        ...     print(f"Computing {x} + {y}")
        ...     return x + y
        >>>
        >>> # First run will compute and cache
        >>> expensive_calculation(1, 2)
        Computing 1 + 2
        3
        >>>
        >>> # Second run will use cached result, even after program restart
        >>> expensive_calculation(1, 2)
        3
    """
    config = create_cache_config(
        folder_name=folder_name,
        maxsize=maxsize,
        ttl=ttl,
        policy=policy,
        use_sql=use_sql,
        secure=secure,
        cache_type="disk",
    )

    if HAS_DISKCACHE:
        from .engines import diskcache

        engine: BaseCacheEngine[P, R] = diskcache.DiskCacheEngine(config)  # type: ignore[abstract]
        return cast(CacheDecorator[P, R], engine.cache)
    elif HAS_KLEPTO and use_sql:
        from .engines import klepto

        engine = klepto.KleptoEngine(config)  # type: ignore[abstract]
        return cast(CacheDecorator[P, R], engine.cache)
    else:
        return mcache(maxsize=maxsize, ttl=ttl, policy=policy)


def fcache(
    folder_name: str | None = None,
    maxsize: int | None = None,
    ttl: float | None = None,
    *,  # Force remaining arguments to be keyword-only
    compress: bool = False,
    secure: bool = True,
) -> CacheDecorator[P, R]:
    """
    Fast file-based caching optimized for large objects.

    Creates a decorator that caches function results in files, optimized for
    large data objects like NumPy arrays, pandas DataFrames, or machine learning models.
    This cache is particularly useful for scientific computing and data analysis.

    Args:
        folder_name: Name of the folder to store cache files. If None, 'default' is used.
            Must contain only alphanumeric characters, dash, underscore, and dot.
        maxsize: Maximum number of items to store in the cache. None means unlimited.
            For file caches, this controls the number of files, not their total size.
        ttl: Time-to-live in seconds. None means entries never expire.
            Use this to automatically invalidate cached results after a certain time.
        compress: Whether to compress cached data to save disk space.
            Compression adds CPU overhead but reduces disk usage.
        secure: Whether to use secure file permissions. Set to False only in
            trusted environments where performance is critical.

    Returns:
        CacheDecorator: A decorator that can be applied to functions to cache their results.

    Raises:
        ValueError: If folder_name contains invalid characters.
        OSError: If cache directory creation fails.
        ImportError: If no suitable backend is available and fallback fails.

    Example:
        >>> import numpy as np
        >>>
        >>> @fcache(folder_name="matrix_ops", compress=True)
        ... def matrix_multiply(a, b):
        ...     print("Computing matrix multiplication")
        ...     return np.dot(a, b)
        >>>
        >>> # Create some large matrices
        >>> a = np.random.rand(1000, 1000)
        >>> b = np.random.rand(1000, 1000)
        >>>
        >>> # First call computes and caches
        >>> result1 = matrix_multiply(a, b)
        Computing matrix multiplication
        >>>
        >>> # Second call uses cache
        >>> result2 = matrix_multiply(a, b)
        >>>
        >>> # Verify results are the same
        >>> np.allclose(result1, result2)
        True
    """
    config = create_cache_config(
        folder_name=folder_name,
        maxsize=maxsize,
        ttl=ttl,
        compress=compress,
        secure=secure,
        cache_type="file",
    )

    if HAS_JOBLIB:
        from .engines.joblib import JoblibEngine

        engine: BaseCacheEngine[P, R] = JoblibEngine(config)
        return cast(CacheDecorator[P, R], engine.cache)
    elif HAS_KLEPTO:
        from .engines.klepto import KleptoEngine

        engine = KleptoEngine(config)
        return cast(CacheDecorator[P, R], engine.cache)
    else:
        return mcache(maxsize=maxsize, ttl=ttl)


def acache(
    maxsize: int | None = None,
    ttl: float | None = None,
    policy: EvictionPolicy = "lru",
) -> (
    Callable[[Callable[P, Awaitable[AsyncR]]], Callable[P, Awaitable[AsyncR]]]
    | Callable[[Callable[P, AsyncR]], Callable[P, Awaitable[AsyncR]]]
):
    """
    Async-capable caching decorator.

    Creates a decorator that caches results of asynchronous functions. This decorator
    works with both coroutine functions and regular functions that return awaitable objects.
    It automatically handles the asynchronous nature of the cached functions.

    Args:
        maxsize: Maximum number of items to store in the cache. None means unlimited,
            but this may lead to memory issues for long-running applications.
        ttl: Time-to-live in seconds. None means entries never expire. Use this to
            automatically invalidate cached results after a certain time.
        policy: Cache eviction policy when maxsize is reached. Options include:
            - "lru": Least Recently Used (default)
            - "fifo": First In First Out
            - "lifo": Last In First Out
            - "mru": Most Recently Used
            - "lfu": Least Frequently Used

    Returns:
        A decorator that can be applied to async functions to cache their results.
        The decorated function will always return an awaitable object.

    Raises:
        ValueError: If an invalid policy is specified.
        RuntimeError: If the event loop is not available.
        ImportError: If aiocache is not available and fallback fails.

    Example:
        >>> import asyncio
        >>>
        >>> @acache(maxsize=100, ttl=60)
        ... async def fetch_data(url):
        ...     print(f"Fetching data from {url}")
        ...     # Simulate network request
        ...     await asyncio.sleep(1)
        ...     return f"Data from {url}"
        >>>
        >>> async def main():
        ...     # First call will fetch and cache
        ...     data1 = await fetch_data("https://example.com")
        ...     print(data1)
        ...
        ...     # Second call will use cached result
        ...     data2 = await fetch_data("https://example.com")
        ...     print(data2)
        >>>
        >>> # Run the example
        >>> asyncio.run(main())
        Fetching data from https://example.com
        Data from https://example.com
        Data from https://example.com
    """
    config = create_cache_config(
        maxsize=maxsize,
        ttl=ttl,
        policy=policy,
        cache_type="async",
    )

    if HAS_AIOCACHE:
        # Import the module but don't instantiate the class directly here
        # to avoid linter errors about abstract methods
        from .engines import aiocache

        def decorator(
            func: Callable[P, AsyncR] | Callable[P, Awaitable[AsyncR]],
        ) -> Callable[P, Awaitable[AsyncR]]:
            """Decorator that wraps a function with async caching."""
            # Create the engine instance inside the decorator where it's actually used
            engine: Any = aiocache.AioCacheEngine(config)  # type: ignore[abstract]
            cache_func = engine.cache(func)

            @functools.wraps(func)
            async def wrapper(*args: P.args, **kwargs: P.kwargs) -> AsyncR:
                """Wrapper that ensures the result is awaitable."""
                result = cache_func(*args, **kwargs)
                if asyncio.iscoroutine(result):
                    return await result
                return cast(AsyncR, result)  # Cast to satisfy type checker

            return wrapper

        return decorator
    else:
        # Fallback to memory cache with async wrapper
        # Convert EvictionPolicy to str for mcache
        policy_str = str(policy) if policy is not None else "lru"
        mem_cache: Any = mcache(maxsize=maxsize, ttl=ttl, policy=policy_str)

        def decorator(
            func: Callable[P, AsyncR] | Callable[P, Awaitable[AsyncR]],
        ) -> Callable[P, Awaitable[AsyncR]]:
            """Decorator that wraps a function with async-compatible caching."""
            cached_func = cast(Callable[..., Any], mem_cache(cast(Callable[..., Any], func)))

            @functools.wraps(func)
            async def wrapper(*args: P.args, **kwargs: P.kwargs) -> AsyncR:
                """Wrapper that ensures the result is awaitable."""
                result = cached_func(*args, **kwargs)
                if asyncio.iscoroutine(result):
                    return await result
                return cast(AsyncR, result)  # Cast to satisfy type checker

            return wrapper

        return decorator


def _get_available_backends() -> dict[str, bool]:
    """
    Get a dictionary of available cache backends.

    Checks which cache backends are available in the current environment
    by checking if the required packages are installed.

    Returns:
        dict[str, bool]: Dictionary mapping backend names to availability status.

    Example:
        >>> backends = _get_available_backends()
        >>> print(backends)
        {'aiocache': True, 'cachebox': False, 'cachetools': True, 'diskcache': True, 'joblib': True}
    """
    return {
        "aiocache": HAS_AIOCACHE,
        "cachebox": HAS_CACHEBOX,
        "cachetools": HAS_CACHETOOLS,
        "diskcache": HAS_DISKCACHE,
        "joblib": HAS_JOBLIB,
        "klepto": HAS_KLEPTO,
    }


def _select_best_backend(
    preferred: str | None = None,
    *,  # Force remaining arguments to be keyword-only
    is_async: bool = False,
    needs_disk: bool = False,
) -> str:
    """
    Select the best available backend based on requirements.

    Determines the most suitable cache backend based on the specified preferences
    and requirements. It considers whether async support is needed and whether
    disk storage is required.

    Args:
        preferred: Name of the preferred backend. If available, this backend will be used.
            If not available, a suitable alternative will be selected.
        is_async: Whether async support is required. If True, only backends with
            async support will be considered.
        needs_disk: Whether disk storage is required. If True, only backends with
            disk storage capabilities will be considered.

    Returns:
        str: Name of the selected backend.

    Raises:
        ImportError: If no suitable backend is available for the specified requirements.

    Example:
        >>> # Select best backend with disk storage
        >>> backend = _select_best_backend(needs_disk=True)
        >>> print(backend)
        'diskcache'

        >>> # Select best async backend
        >>> backend = _select_best_backend(is_async=True)
        >>> print(backend)
        'aiocache'
    """
    backends = _get_available_backends()

    # If preferred backend is available and meets requirements, use it
    if preferred and backends.get(preferred):
        if is_async and preferred != "aiocache":
            # Only aiocache supports async natively
            pass
        elif needs_disk and preferred not in ("diskcache", "klepto", "joblib"):
            # Only these backends support disk storage
            pass
        else:
            return preferred

    # Select based on requirements
    if is_async:
        if backends["aiocache"]:
            return "aiocache"
        # No good async fallback, will need to wrap
        if needs_disk:
            if backends["diskcache"]:
                return "diskcache"
            elif backends["klepto"]:
                return "klepto"
            elif backends["joblib"]:
                return "joblib"
        elif backends["cachebox"]:
            return "cachebox"
        elif backends["cachetools"]:
            return "cachetools"
    elif needs_disk:
        if backends["diskcache"]:
            return "diskcache"
        elif backends["klepto"]:
            return "klepto"
        elif backends["joblib"]:
            return "joblib"
    elif backends["cachebox"]:
        return "cachebox"
    elif backends["cachetools"]:
        return "cachetools"

    # Fallback to functools (always available)
    return "functools"


def _create_engine(config: CacheConfig, func: Callable[P, R]) -> BaseCacheEngine[P, R]:
    """
    Create a cache engine based on configuration.

    Instantiates the appropriate cache engine based on the provided configuration
    and the function to be cached. This is an internal function used by the ucache
    decorator to create the most suitable engine.

    Args:
        config: Configuration for the cache engine, including parameters like
            maxsize, ttl, policy, and cache type.
        func: The function that will be cached. Used to determine if the function
            is asynchronous.

    Returns:
        BaseCacheEngine: An instance of the appropriate cache engine.

    Raises:
        ImportError: If the required backend is not available.
        ValueError: If the configuration is invalid.

    Example:
        >>> def example_func(x, y):
        ...     return x + y
        >>>
        >>> config = create_cache_config(maxsize=100, ttl=60)
        >>> engine = _create_engine(config, example_func)
        >>> print(type(engine).__name__)
        'CacheToolsEngine'
    """
    # Check if function is async
    is_async = asyncio.iscoroutinefunction(func)
    needs_disk = config.cache_type in ("disk", "file")

    # Select backend
    backend = _select_best_backend(config.preferred_engine, is_async=is_async, needs_disk=needs_disk)

    # Create engine based on selected backend - import modules instead of directly
    # instantiating classes to avoid linter errors about abstract methods
    if backend == "aiocache" and HAS_AIOCACHE:
        from .engines import aiocache

        return aiocache.AioCacheEngine(config)  # type: ignore[abstract]
    elif backend == "cachebox" and HAS_CACHEBOX:
        from .engines import cachebox

        return cachebox.CacheBoxEngine(config)  # type: ignore[abstract]
    elif backend == "cachetools" and HAS_CACHETOOLS:
        from .engines import cachetools

        return cachetools.CacheToolsEngine(config)  # type: ignore[abstract]
    elif backend == "diskcache" and HAS_DISKCACHE:
        from .engines import diskcache

        return diskcache.DiskCacheEngine(config)  # type: ignore[abstract]
    elif backend == "joblib" and HAS_JOBLIB:
        from .engines import joblib

        return joblib.JoblibEngine(config)  # type: ignore[abstract]
    elif backend == "klepto" and HAS_KLEPTO:
        from .engines import klepto

        return klepto.KleptoEngine(config)  # type: ignore[abstract]
    else:
        # Always fallback to functools which is guaranteed to be available
        from .engines import functools_engine

        return functools_engine.FunctoolsCacheEngine(config)  # type: ignore[abstract]


def ucache(
    folder_name: str | None = None,
    maxsize: int | None = None,
    ttl: float | None = None,
    policy: str = "lru",
    preferred_engine: str | None = None,
    *,  # Force remaining arguments to be keyword-only
    use_sql: bool = False,
    compress: bool = False,
    secure: bool = True,
) -> CacheDecorator[P, R]:
    """
    Universal caching decorator that automatically selects the best backend.

    Creates a decorator that intelligently selects the most appropriate caching
    backend based on the function being decorated and the available packages.
    This is the most flexible caching decorator and is recommended for most use cases.

    Args:
        folder_name: Name of the folder to store cache files if disk caching is used.
            If None, 'default' is used. Must contain only alphanumeric characters,
            dash, underscore, and dot.
        maxsize: Maximum number of items to store in the cache. None means unlimited.
            For memory caches, this controls the number of items. For disk caches,
            this may control the number of items or the total size in bytes.
        ttl: Time-to-live in seconds. None means entries never expire. Use this to
            automatically invalidate cached results after a certain time.
        policy: Cache eviction policy when maxsize is reached. Options include:
            - "lru": Least Recently Used (default)
            - "fifo": First In First Out
            - "lifo": Last In First Out
            - "mru": Most Recently Used
            - "lfu": Least Frequently Used
        preferred_engine: Name of the preferred cache engine to use. If available,
            this engine will be used. If not available, a suitable alternative will be selected.
            Options include: "aiocache", "cachebox", "cachetools", "diskcache", "joblib", "klepto".
        use_sql: Whether to use SQL-based disk cache for better performance with
            large datasets. Only applies if a disk cache is selected.
        compress: Whether to compress cached data to save disk space. Only applies
            if a file-based cache is selected.
        secure: Whether to use secure file permissions. Set to False only in
            trusted environments where performance is critical.

    Returns:
        CacheDecorator: A decorator that can be applied to functions to cache their results.

    Raises:
        ValueError: If folder_name contains invalid characters or if an invalid policy is specified.
        OSError: If cache directory creation fails.

    Example:
        >>> # Basic usage with automatic backend selection
        >>> @ucache(maxsize=100, ttl=3600)
        ... def expensive_calculation(x, y):
        ...     print(f"Computing {x} + {y}")
        ...     return x + y
        >>>
        >>> # First call computes and caches
        >>> expensive_calculation(1, 2)
        Computing 1 + 2
        3
        >>>
        >>> # Second call uses cached result
        >>> expensive_calculation(1, 2)
        3

        >>> # With preferred engine
        >>> @ucache(preferred_engine="diskcache", folder_name="persistent_cache")
        ... def long_running_task(input_data):
        ...     print("Processing data...")
        ...     # Simulate long computation
        ...     import time
        ...     time.sleep(2)
        ...     return f"Result: {input_data}"
        >>>
        >>> long_running_task("test")
        Processing data...
        'Result: test'
        >>>
        >>> # Subsequent calls use cache
        >>> long_running_task("test")
        'Result: test'
    """
    config = create_cache_config(
        folder_name=folder_name,
        maxsize=maxsize,
        ttl=ttl,
        policy=policy,
        preferred_engine=preferred_engine,
        use_sql=use_sql,
        compress=compress,
        secure=secure,
        cache_type="auto",
    )

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        """Decorator that wraps a function with the best available caching backend."""
        engine = _create_engine(config, func)
        return cast(Callable[P, R], engine.cache(func))

    return decorator
