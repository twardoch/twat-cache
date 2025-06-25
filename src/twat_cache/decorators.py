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
import importlib.util
import json
from pathlib import Path
from typing import (
    Any,
    Protocol,
    cast,
)
from collections.abc import Awaitable, Callable

# Import the logger from our logging module
from .logging import logger

from .config import CacheConfig, create_cache_config, EvictionPolicy
# BaseCacheEngine might not be directly needed here anymore if ucache delegates fully
# from .engines.base import BaseCacheEngine
from .engines.manager import get_engine_manager
from .exceptions import EngineNotAvailableError # For acache
from .type_defs import P, R, AsyncR


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


# HAS_AIOCACHE constant is no longer needed. Engine availability is handled by CacheEngineManager.

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


# mcache, bcache, fcache are deprecated.
# Their functionality will be covered by ucache with specific configurations.

def acache(
    maxsize: int | None = None,
    ttl: float | None = None,
    policy: EvictionPolicy = "lru",
    # Add serializer to be consistent, though AioCacheEngine might handle it differently
    serializer: Callable[[Any], str] | None = None,
) -> AsyncCacheDecorator[P, AsyncR]:
    """
    Async-capable caching decorator.

    Uses AioCacheEngine to cache results of asynchronous functions.
    If AioCacheEngine is not available or cannot be instantiated, this decorator
    will raise an EngineNotAvailableError.

    Args:
        maxsize: Maximum size of the cache. None means unlimited.
        ttl: Time-to-live in seconds. None means no TTL.
        policy: Cache eviction policy (e.g., "lru", "fifo").
        serializer: Optional custom serializer for cache keys.

    Returns:
        A decorator for async functions.

    Raises:
        EngineNotAvailableError: If AioCacheEngine cannot be initialized.
    """
    logger.debug(f"acache invoked with: maxsize={maxsize}, ttl={ttl}, policy='{policy}'")

    # Configuration specifically for aiocache
    # folder_name is typically not used by memory-based async caches like aiocache's defaults
    config = create_cache_config(
        preferred_engine="aiocache", # Explicitly request aiocache
        maxsize=maxsize,
        ttl=ttl,
        policy=policy,
        serializer=serializer,
        # folder_name=None, # Explicitly None for memory-based
        # cache_type="memory", # Implicit with aiocache often, or engine handles
    )

    engine_manager = get_engine_manager()
    # Attempt to create an aiocache engine instance
    # The type of cache_engine_instance will be BaseCacheEngine.
    # We expect it to be an AioCacheEngine or a compatible async engine.
    cache_engine_instance = engine_manager.create_engine_instance(config)

    if cache_engine_instance is None or not cache_engine_instance.name.startswith("AioCache"):
        # Check if it's None OR if it's not an AioCacheEngine (or a sub-class like AioCacheEngine)
        # This check on name is a bit heuristic; ideally, we'd check isinstance(cache_engine_instance, AioCacheEngine),
        # but that would require importing AioCacheEngine here, creating a circular dep or just more imports.
        # The CacheEngineManager should have logged if it couldn't create 'aiocache'.
        logger.error(
            "Failed to obtain an AioCacheEngine instance. "
            "acache requires the 'aiocache' backend."
        )
        raise EngineNotAvailableError(
            engine_name="aiocache",
            message="AioCacheEngine is not available or could not be instantiated. "
                    "Please ensure 'aiocache' is installed and configured correctly."
        )

    # We have a cache_engine_instance, presumably an AioCacheEngine.
    # Its .cache() method should be suitable for async functions.
    def decorator(
        func: Callable[P, AsyncR] | Callable[P, Awaitable[AsyncR]],
    ) -> Callable[P, Awaitable[AsyncR]]:

        # The engine's .cache() method is responsible for returning an async wrapper.
        # BaseCacheEngine.cache is typed for sync, so we might need a cast
        # or ensure AioCacheEngine's .cache method has the correct async signature.
        # For now, let's assume the engine's .cache method is correctly implemented for async.

        # Directly call the engine's cache method.
        # If cache_engine_instance is indeed an AioCacheEngine, its `cache` method
        # should correctly handle async functions and return an async wrapper.
        cached_func = cache_engine_instance.cache(func) # type: ignore

        # The cached_func returned by AioCacheEngine.cache should already be an async def wrapper.
        # So, we can return it directly.
        # No need for an additional async def wrapper here if the engine does it right.
        return cached_func

    return decorator


# Helper functions _get_available_backends, _select_best_backend, _create_engine
# are now removed as ucache will use CacheEngineManager.

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
    # Add serializer argument consistent with make_key, though engines might handle it
    serializer: Callable[[Any], str] | None = None,
) -> CacheDecorator[P, R]:
    """
    Universal caching decorator.

    Configures and applies a cache engine based on the provided parameters.
    It uses CacheEngineManager to obtain an engine instance.

    Args:
        folder_name: Name of the folder for disk-based caches.
        maxsize: Maximum size of the cache. None means unlimited.
        ttl: Time-to-live in seconds. None means no TTL.
        policy: Cache eviction policy (e.g., "lru", "fifo").
        preferred_engine: Name of the preferred cache engine (e.g., "diskcache", "functools").
        use_sql: Hint for engines like Klepto (if used) whether to use SQL. (Consider if needed for MVP)
        compress: Whether to compress data for disk-based caches.
        secure: Secure file permissions for disk caches; or secure key generation hint.
        serializer: Optional custom serializer for cache keys. (Currently make_key handles this globally)

    Returns:
        A decorator function that caches results of the decorated function.
    """
    logger.debug(
        f"ucache invoked with: preferred_engine={preferred_engine}, maxsize={maxsize}, ttl={ttl}, policy='{policy}'"
    )

    # Create a configuration object from the decorator arguments
    # 'cache_type' is removed as 'preferred_engine' dictates the engine.
    # 'use_sql' is a hint that specific engines might use, keep for now.
    config = create_cache_config(
        folder_name=folder_name,
        maxsize=maxsize,
        ttl=ttl,
        policy=policy,
        preferred_engine=preferred_engine,
        use_sql=use_sql, # Retained as it's a CacheConfig param, though its impact is engine-specific
        compress=compress,
        secure=secure,
        serializer=serializer, # Pass serializer to config
        # cache_type="auto", # No longer needed, preferred_engine is key
    )

    engine_manager = get_engine_manager()
    # The func argument is not available at this stage for create_engine_instance,
    # which is fine as our new CacheEngineManager doesn't need it.
    cache_engine_instance = engine_manager.create_engine_instance(config)

    if cache_engine_instance is None:
        # This case should be rare if 'functools' is always a fallback.
        logger.error(
            "Failed to obtain a cache engine instance. "
            "The ucache decorator will run the function without caching."
        )

        # Return a decorator that does nothing but run the original function
        def no_cache_decorator(func: Callable[P, R]) -> Callable[P, R]:
            @functools.wraps(func)
            def no_cache_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                return func(*args, **kwargs)
            return no_cache_wrapper
        return no_cache_decorator

    # If an engine was successfully obtained, create the actual caching decorator
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        # Use the .cache() method from the instantiated engine
        # This engine.cache(func) returns the actual wrapped function.
        cached_func = cache_engine_instance.cache(func)

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            # The cached_func already handles try-except for cache errors internally
            # if the engine's .cache() method is robust.
            # However, adding a top-level try-except here for ucache provides a safety net
            # in case the engine's .cache() method itself raises an unexpected error
            # or if cache_engine_instance.cache(func) failed.
            try:
                return cached_func(*args, **kwargs)
            except Exception as e:
                # This log is specific to ucache's own handling
                logger.warning(
                    f"Error during cached function execution via ucache for '{func.__name__}': {e}. "
                    "Executing original function without cache."
                )
                return func(*args, **kwargs)
        return wrapper
    return decorator
