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
"""

import asyncio
import functools
import json
from pathlib import Path
from typing import (
    Any,
    cast,
    overload,
    Protocol,
    Optional,
    ParamSpec,
    TypeVar,
    Dict,
    Callable,
    Awaitable,
)
from collections.abc import Awaitable

from loguru import logger

from .config import create_cache_config, CacheConfig, EvictionPolicy
from .engines.base import BaseCacheEngine
from .engines.functools import FunctoolsCacheEngine
from .paths import get_cache_path
from .type_defs import P, R, AsyncR, CacheDecorator, CacheKey, CacheValue


class CacheDecorator(Protocol[P, R]):
    """Protocol for cache decorators."""

    def __call__(self, func: Callable[P, R]) -> Callable[P, R]: ...


class AsyncCacheDecorator(Protocol[P, AsyncR]):
    """Protocol for async cache decorators."""

    def __call__(
        self, func: Callable[P, AsyncR] | Callable[P, Awaitable[AsyncR]]
    ) -> Callable[P, Awaitable[AsyncR]]: ...


# Try to import optional backends
try:
    import aiocache  # type: ignore

    HAS_AIOCACHE = True
except ImportError:
    HAS_AIOCACHE = False
    logger.warning("aiocache not available, will fall back to async wrapper")

try:
    import cachebox  # type: ignore

    HAS_CACHEBOX = True
except ImportError:
    HAS_CACHEBOX = False
    logger.warning("cachebox not available, will fall back to cachetools")

try:
    import cachetools  # type: ignore

    HAS_CACHETOOLS = True
except ImportError:
    HAS_CACHETOOLS = False
    logger.warning("cachetools not available, will fall back to functools")

try:
    import diskcache  # type: ignore

    HAS_DISKCACHE = True
except ImportError:
    HAS_DISKCACHE = False
    logger.warning("diskcache not available, will fall back to memory cache")

try:
    import joblib  # type: ignore

    HAS_JOBLIB = True
except ImportError:
    HAS_JOBLIB = False
    logger.warning("joblib not available, will fall back to memory cache")

try:
    import klepto  # type: ignore

    HAS_KLEPTO = True
except ImportError:
    HAS_KLEPTO = False
    logger.warning("klepto not available, will fall back to memory cache")


def get_cache_dir(folder_name: str | None = None) -> Path:
    """
    Get or create cache directory.

    Args:
        folder_name: Optional name for the cache folder

    Returns:
        Path to the cache directory

    Raises:
        ValueError: If folder_name contains invalid characters
        OSError: If directory creation fails
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


def make_key(
    serializer: Callable[[Any], str] | None = None, *args: Any, **kwargs: Any
) -> str:
    """
    Create a cache key from function arguments.

    Args:
        serializer: Optional function to serialize non-JSON-serializable objects
        *args: Positional arguments to include in key
        **kwargs: Keyword arguments to include in key

    Returns:
        A string key that uniquely identifies the arguments
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
    maxsize: Optional[int] = None,
    ttl: Optional[float] = None,
    policy: str = "lru",
    *,  # Force remaining arguments to be keyword-only
    secure: bool = True,
) -> CacheDecorator[P, R]:
    """
    Memory-based caching using fastest available backend.

    Args:
        maxsize: Maximum cache size (None for unlimited)
        ttl: Time-to-live in seconds (None for no expiry)
        policy: Cache eviction policy
        secure: Whether to use secure file permissions

    Returns:
        A caching decorator using the best available memory backend
    """
    config = create_cache_config(
        maxsize=maxsize,
        ttl=ttl,
        policy=policy,
        cache_type="memory",
        secure=secure,
    )

    if HAS_CACHEBOX:
        from .engines.cachebox import CacheBoxEngine

        engine: BaseCacheEngine[P, R] = CacheBoxEngine(config)
        return cast(CacheDecorator[P, R], engine.cache)
    elif HAS_CACHETOOLS:
        from .engines.cachetools import CacheToolsEngine

        engine = CacheToolsEngine(config)
        return cast(CacheDecorator[P, R], engine.cache)
    else:
        from .engines.functools import FunctoolsCacheEngine

        engine = FunctoolsCacheEngine(config)
        return cast(CacheDecorator[P, R], engine.cache)


def bcache(
    folder_name: Optional[str] = None,
    maxsize: Optional[int] = None,
    ttl: Optional[float] = None,
    policy: str = "lru",
    *,  # Force remaining arguments to be keyword-only
    use_sql: bool = True,
    secure: bool = True,
) -> CacheDecorator[P, R]:
    """
    Basic disk caching using database backends.

    Args:
        folder_name: Cache directory name
        maxsize: Maximum cache size (None for unlimited)
        ttl: Time-to-live in seconds (None for no expiry)
        policy: Cache eviction policy
        use_sql: Whether to use SQL-based disk cache
        secure: Whether to use secure file permissions

    Returns:
        A caching decorator using the best available disk backend
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
        from .engines.diskcache import DiskCacheEngine

        engine: BaseCacheEngine[P, R] = DiskCacheEngine(config)
        return cast(CacheDecorator[P, R], engine.cache)
    elif HAS_KLEPTO and use_sql:
        from .engines.klepto import KleptoEngine

        engine = KleptoEngine(config)
        return cast(CacheDecorator[P, R], engine.cache)
    else:
        return mcache(maxsize=maxsize, ttl=ttl, policy=policy)


def fcache(
    folder_name: Optional[str] = None,
    maxsize: Optional[int] = None,
    ttl: Optional[float] = None,
    *,  # Force remaining arguments to be keyword-only
    compress: bool = False,
    secure: bool = True,
) -> CacheDecorator[P, R]:
    """
    Fast file-based caching optimized for large objects.

    Args:
        folder_name: Cache directory name
        maxsize: Maximum cache size (None for unlimited)
        ttl: Time-to-live in seconds (None for no expiry)
        compress: Whether to compress cached data
        secure: Whether to use secure file permissions

    Returns:
        A caching decorator using the best available file backend
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


@overload
def acache(
    maxsize: int | None = None,
    ttl: float | None = None,
    policy: EvictionPolicy = "lru",
) -> Callable[[Callable[P, Awaitable[AsyncR]]], Callable[P, Awaitable[AsyncR]]]: ...


@overload
def acache(
    maxsize: int | None = None,
    ttl: float | None = None,
    policy: EvictionPolicy = "lru",
) -> Callable[[Callable[P, AsyncR]], Callable[P, Awaitable[AsyncR]]]: ...


def acache(
    maxsize: int | None = None,
    ttl: float | None = None,
    policy: EvictionPolicy = "lru",
) -> (
    Callable[[Callable[P, Awaitable[AsyncR]]], Callable[P, Awaitable[AsyncR]]]
    | Callable[[Callable[P, AsyncR]], Callable[P, Awaitable[AsyncR]]]
):
    """
    Async-capable caching using aiocache.

    Args:
        maxsize: Maximum cache size (None for unlimited)
        ttl: Time-to-live in seconds (None for no expiry)
        policy: Cache eviction policy

    Returns:
        An async caching decorator
    """
    config = create_cache_config(
        maxsize=maxsize,
        ttl=ttl,
        policy=policy,
        cache_type="async",
    )

    if HAS_AIOCACHE:
        from .engines.aiocache import AioCacheEngine

        engine: BaseCacheEngine[P, AsyncR] = AioCacheEngine(config)
        return cast(AsyncCacheDecorator[P, AsyncR], engine.cache)
    else:
        # Fall back to async wrapper around memory cache
        def decorator(
            func: Callable[P, AsyncR] | Callable[P, Awaitable[AsyncR]],
        ) -> Callable[P, Awaitable[AsyncR]]:
            mem_cache: CacheDecorator[P, AsyncR] = cast(
                CacheDecorator[P, AsyncR],
                mcache(maxsize=maxsize, ttl=ttl, policy=policy),
            )
            cached_func = mem_cache(func)  # type: ignore

            @functools.wraps(func)
            async def wrapper(*args: P.args, **kwargs: P.kwargs) -> AsyncR:
                loop = asyncio.get_event_loop()
                if asyncio.iscoroutinefunction(func):
                    coro = cached_func(*args, **kwargs)  # type: ignore
                    return await coro
                else:
                    return await loop.run_in_executor(
                        None,
                        cached_func,
                        *args,
                        **kwargs,  # type: ignore
                    )

            return wrapper

        return decorator


def _get_available_backends() -> Dict[str, bool]:
    """Get a mapping of available backends."""
    return {
        "aiocache": HAS_AIOCACHE,
        "cachebox": HAS_CACHEBOX,
        "cachetools": HAS_CACHETOOLS,
        "diskcache": HAS_DISKCACHE,
        "joblib": HAS_JOBLIB,
        "klepto": HAS_KLEPTO,
        "functools": True,  # Always available
    }


def _select_best_backend(
    preferred: Optional[str] = None,
    *,  # Force remaining arguments to be keyword-only
    is_async: bool = False,
    needs_disk: bool = False,
) -> str:
    """Select the best available backend based on requirements.

    Args:
        preferred: Preferred backend name.
        is_async: Whether async support is needed.
        needs_disk: Whether disk storage is needed.

    Returns:
        str: Name of the selected backend.
    """
    available = _get_available_backends()

    # If preferred backend is available, use it
    if preferred and available.get(preferred):
        return preferred

    # For async functions, try aiocache first
    if is_async and available["aiocache"]:
        return "aiocache"

    # For disk storage, try backends in order
    if needs_disk:
        disk_backends = ["diskcache", "joblib", "klepto"]
        for backend in disk_backends:
            if available[backend]:
                return backend

    # For memory storage, try backends in order
    memory_backends = ["cachebox", "cachetools"]
    for backend in memory_backends:
        if available[backend]:
            return backend

    # Fallback to functools
    return "functools"


def _create_engine(config: CacheConfig, func: Callable[P, R]) -> BaseCacheEngine[P, R]:
    """Create a cache engine based on configuration and function.

    Args:
        config: Cache configuration.
        func: Function to cache.

    Returns:
        CacheEngine: Selected cache engine instance.
    """
    # Determine requirements
    is_async = asyncio.iscoroutinefunction(func)
    needs_disk = bool(config.folder_name)

    # Select backend
    backend = _select_best_backend(
        preferred=config.preferred_engine,
        is_async=is_async,
        needs_disk=needs_disk,
    )

    # Create engine based on selection
    if backend == "functools":
        return FunctoolsCacheEngine(config)
    elif backend == "aiocache":
        from .engines.aiocache import AioCacheEngine

        return AioCacheEngine(config)
    elif backend == "cachebox":
        from .engines.cachebox import CacheBoxEngine

        return CacheBoxEngine(config)
    elif backend == "cachetools":
        from .engines.cachetools import CacheToolsEngine

        return CacheToolsEngine(config)
    elif backend == "diskcache":
        from .engines.diskcache import DiskCacheEngine

        return DiskCacheEngine(config)
    elif backend == "joblib":
        from .engines.joblib import JoblibEngine

        return JoblibEngine(config)
    elif backend == "klepto":
        from .engines.klepto import KleptoEngine

        return KleptoEngine(config)
    else:
        return FunctoolsCacheEngine(config)


def ucache(
    folder_name: Optional[str] = None,
    maxsize: Optional[int] = None,
    ttl: Optional[float] = None,
    policy: str = "lru",
    preferred_engine: Optional[str] = None,
    *,  # Force remaining arguments to be keyword-only
    use_sql: bool = False,
    compress: bool = False,
    secure: bool = True,
) -> CacheDecorator[P, R]:
    """
    Universal caching that automatically selects best available backend.

    Args:
        folder_name: Cache directory name
        maxsize: Maximum cache size (None for unlimited)
        ttl: Time-to-live in seconds (None for no expiry)
        policy: Cache eviction policy
        preferred_engine: Preferred caching backend
        use_sql: Whether to use SQL-based disk cache
        compress: Whether to compress cached data
        secure: Whether to use secure file permissions

    Returns:
        A caching decorator using the best available backend
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
    )

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        engine = _create_engine(config, func)
        return engine.cache(func)

    return decorator
