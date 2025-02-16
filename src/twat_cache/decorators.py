#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "loguru",
#   "functools",
#   "diskcache",
#   "cachebox",
#   "types-diskcache",
# ]
# ///
# this_file: src/twat_cache/decorators.py

"""
Core caching decorators.

This module provides four main decorators:
- mcache: Memory-based caching using functools.lru_cache
- bcache: Basic disk caching using diskcache
- fcache: Fast in-memory caching using cachebox
- ucache: Universal caching with automatic fallback
"""

import functools
import json
import uuid
from pathlib import Path
from typing import Any, TypeVar, cast, ParamSpec
from collections.abc import Callable
from loguru import logger
from functools import wraps, lru_cache

from .cache import register_cache, update_stats, CacheStats
from .config import CacheConfig, create_cache_config
from .engines.base import BaseCacheEngine
from .engines.functools import FunctoolsCacheEngine  # Always available
from .engines.diskcache import DiskCacheEngine
from .engines.cachebox import CacheBoxEngine

# Type variables for generic function types
P = ParamSpec("P")
R = TypeVar("R")
F = Callable[P, R]

# Cache types
CacheDict = dict[str, Any]
CacheKey = str
CacheValue = Any

# Try to import optional backends
try:
    from diskcache import Cache as DiskCache

    HAS_DISKCACHE = True
except ImportError:
    HAS_DISKCACHE = False
    logger.debug("diskcache not available")

try:
    from cachebox import Cache as BoxCache

    HAS_CACHEBOX = True
except ImportError:
    HAS_CACHEBOX = False
    logger.debug("cachebox not available")

_BACKEND_PRIORITY = [
    "cachebox",
    "diskcache",
    "joblib",
    "memory",  # functools
]


def _get_backend(config: CacheConfig) -> BaseCacheEngine:
    """Select and instantiate the appropriate cache backend."""
    if config.preferred_engine:
        if config.preferred_engine == "memory":
            return FunctoolsCacheEngine(config)
        elif config.preferred_engine == "diskcache" and DiskCacheEngine.is_available():
            return DiskCacheEngine(config)
        elif config.preferred_engine == "cachebox" and CacheBoxEngine.is_available():
            return CacheBoxEngine(config)
        # ... other preferred engines ...
        logger.warning(
            f"Preferred engine '{config.preferred_engine}' not available. Falling back..."
        )

    for backend_name in _BACKEND_PRIORITY:
        if backend_name == "memory":
            return FunctoolsCacheEngine(config)
        elif backend_name == "diskcache" and DiskCacheEngine.is_available():
            return DiskCacheEngine(config)
        elif backend_name == "cachebox" and CacheBoxEngine.is_available():
            return CacheBoxEngine(config)
        # ... other backends ...

    # Should never reach here, as functools is always available
    return FunctoolsCacheEngine(config)


def twat_cache(
    folder_name: str | None = None,
    maxsize: int | None = None,
    preferred_engine: str | None = None,
    serializer: Callable[[Any], str] | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        config = CacheConfig(
            maxsize=maxsize,
            folder_name=folder_name,
            preferred_engine=preferred_engine,
            serializer=serializer,
        )
        backend = _get_backend(config)
        cache_id = f"{backend.name}_{func.__name__}"  # Simplified ID

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            key = make_key(*args, **kwargs, serializer=config.serializer)
            cached_result = backend.get(key)
            if cached_result is not None:
                update_stats(cache_id, hit=True)
                return cached_result

            update_stats(cache_id, miss=True)
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                backend.set(key, e)
                raise
            backend.set(key, result)
            return result

        register_cache(
            cache_id,
            backend,  # Store the backend instance itself
            wrapper,
            CacheStats(hits=0, misses=0, size=0, maxsize=config.maxsize),
        )
        return wrapper

    return decorator


def make_key(*args: Any, **kwargs: Any) -> CacheKey:
    """
    Create a cache key from function arguments.

    Handles unhashable types by converting them to JSON strings.
    """

    # Convert args to a stable form
    def convert(obj: Any) -> str | int | float | bool | None:
        if isinstance(obj, list | dict | set):
            return json.dumps(obj, sort_keys=True)
        if isinstance(obj, int | float | str | bool | type(None)):
            return obj
        return str(obj)

    # Convert args and kwargs to stable forms
    converted_args = tuple(convert(arg) for arg in args)
    converted_kwargs = {k: convert(v) for k, v in sorted(kwargs.items())}

    # Create a stable string representation
    return json.dumps((converted_args, converted_kwargs), sort_keys=True)


def mcache(maxsize: int | None = None) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Memory-based caching using functools.lru_cache.

    Args:
        maxsize: Maximum cache size (None for unlimited)

    Returns:
        A decorator that caches function results in memory
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        cache: CacheDict = {}
        cache_id = f"mcache_{func.__name__}_{uuid.uuid4().hex[:8]}"

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            key = make_key(*args, **kwargs)

            if key in cache:
                update_stats(cache_id, hit=True)
                return cast(R, cache[key])

            update_stats(cache_id, miss=True)
            try:
                result = func(*args, **kwargs)
                cache[key] = result
            except Exception as e:
                # Cache the exception
                cache[key] = e
                raise

            # Enforce maxsize
            if maxsize is not None and len(cache) > maxsize:
                # Simple LRU: remove oldest item
                cache.pop(next(iter(cache)))

            update_stats(cache_id, size=len(cache))
            return result

        # Register cache with initial stats
        register_cache(
            cache_id,
            cache,
            wrapper,
            CacheStats(hits=0, misses=0, size=0, maxsize=maxsize),
        )

        return wrapper

    return decorator


def bcache(
    folder_name: str | None = None, maxsize: int | None = None
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Basic disk caching using diskcache.

    Args:
        folder_name: Cache directory name
        maxsize: Maximum cache size (None for unlimited)

    Returns:
        A decorator that caches function results to disk
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        if not HAS_DISKCACHE:
            logger.warning("diskcache not available, falling back to memory cache")
            return mcache(maxsize=maxsize)(func)

        cache_dir = (
            Path.home() / ".cache" / "twat_cache" / (folder_name or func.__name__)
        )
        cache_dir.mkdir(parents=True, exist_ok=True)
        cache = DiskCache(str(cache_dir), size_limit=maxsize or int(1e9))
        cache_id = f"bcache_{func.__name__}_{uuid.uuid4().hex[:8]}"

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            key = make_key(*args, **kwargs)

            result = cache.get(key)
            if result is not None:
                update_stats(cache_id, hit=True)
                if isinstance(result, Exception):
                    raise result
                return cast(R, result)

            update_stats(cache_id, miss=True)
            try:
                result = func(*args, **kwargs)
                cache.set(key, result)
            except Exception as e:
                # Cache the exception
                cache.set(key, e)
                raise

            update_stats(cache_id, size=len(cache))
            return result

        # Register cache with initial stats
        register_cache(
            cache_id,
            cache,
            wrapper,
            CacheStats(hits=0, misses=0, size=0, maxsize=maxsize),
        )

        return wrapper

    return decorator


def fcache(maxsize: int | None = None) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Fast in-memory caching using cachebox.

    Args:
        maxsize: Maximum cache size (None for unlimited)

    Returns:
        A decorator that caches function results using cachebox
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        if not HAS_CACHEBOX:
            logger.warning("cachebox not available, falling back to memory cache")
            return mcache(maxsize=maxsize)(func)

        cache = BoxCache(maxsize=maxsize or 0)  # 0 means unlimited in cachebox
        cache_id = f"fcache_{func.__name__}_{uuid.uuid4().hex[:8]}"

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            key = make_key(*args, **kwargs)

            result = cache.get(key)
            if result is not None:
                update_stats(cache_id, hit=True)
                if isinstance(result, Exception):
                    raise result
                return cast(R, result)

            update_stats(cache_id, miss=True)
            try:
                result = func(*args, **kwargs)
                cache[key] = result
            except Exception as e:
                # Cache the exception
                cache[key] = e
                raise

            update_stats(cache_id, size=len(cache))
            return result

        # Register cache with initial stats
        register_cache(
            cache_id,
            cache,
            wrapper,
            CacheStats(hits=0, misses=0, size=0, maxsize=maxsize),
        )

        return wrapper

    return decorator


def ucache(
    preferred_engine: str | None = None,
    folder_name: str | None = None,
    maxsize: int | None = None,
    config: CacheConfig | None = None,  # For backward compatibility
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Universal caching with automatic fallback.

    Args:
        preferred_engine: Preferred caching backend ('memory', 'disk', or 'fast')
        folder_name: Cache directory name (for disk cache)
        maxsize: Maximum cache size (None for unlimited)
        config: Optional configuration object (for backward compatibility)

    Returns:
        A decorator that caches function results using the best available backend
    """
    # Handle legacy config
    if config is not None:
        maxsize = config.maxsize or maxsize
        folder_name = config.folder_name or folder_name
        preferred_engine = config.preferred_engine or preferred_engine
    else:
        # Create and validate config
        config = create_cache_config(
            maxsize=maxsize,
            folder_name=folder_name,
            preferred_engine=preferred_engine,
        )

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        # Try preferred engine first
        if preferred_engine == "fast" and HAS_CACHEBOX:
            logger.debug("Using fast cache (cachebox)")
            return fcache(maxsize=maxsize)(func)
        elif preferred_engine == "disk" and HAS_DISKCACHE:
            logger.debug("Using disk cache (diskcache)")
            return bcache(folder_name=folder_name, maxsize=maxsize)(func)
        elif preferred_engine == "memory":
            logger.debug("Using memory cache (functools)")
            return mcache(maxsize=maxsize)(func)

        # Auto-select best available
        if HAS_CACHEBOX:
            logger.debug("Using fast cache (cachebox)")
            return fcache(maxsize=maxsize)(func)
        elif HAS_DISKCACHE:
            logger.debug("Using disk cache (diskcache)")
            return bcache(folder_name=folder_name, maxsize=maxsize)(func)
        else:
            logger.debug("Using memory cache (functools)")
            return mcache(maxsize=maxsize)(func)

    return decorator
