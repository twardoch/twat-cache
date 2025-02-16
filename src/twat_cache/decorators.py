#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "loguru",
#   "functools",
#   "diskcache",
#   "joblib",
#   "types-diskcache",
# ]
# ///
# this_file: src/twat_cache/decorators.py

"""
Core caching decorators.

This module provides four main decorators:
- mcache: Memory-based caching using fastest available backend (with fallback to functools)
- bcache: Basic disk caching using diskcache (with fallback to memory)
- fcache: Fast file-based caching using joblib (with fallback to memory)
- ucache: Universal caching that automatically selects best available backend
"""

import functools
import json
from pathlib import Path
from typing import Any, cast
from collections.abc import Callable
from loguru import logger

from .config import create_cache_config
from .engines.cachebox import HAS_CACHEBOX
from .engines.klepto import HAS_KLEPTO
from .type_defs import P, R

# Try to import optional backends
try:
    from diskcache import Cache as DiskCache

    HAS_DISKCACHE = True
except ImportError:
    HAS_DISKCACHE = False
    logger.warning("diskcache not available, will fall back to memory cache")

try:
    from joblib import Memory

    HAS_JOBLIB = True
except ImportError:
    HAS_JOBLIB = False
    logger.warning("joblib not available, will fall back to memory cache")


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


def mcache(maxsize: int | None = None) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Memory-based caching using fastest available backend (with fallback to functools).

    Args:
        maxsize: Maximum cache size (None for unlimited)
    """
    # Try cachetools first as it's more flexible
    try:
        from cachetools import LRUCache, cached

        cache = LRUCache(maxsize=maxsize or float("inf"))
        return lambda func: cast(Callable[P, R], cached(cache=cache)(func))
    except ImportError:
        logger.debug("cachetools not available, using functools.lru_cache")
        return lambda func: cast(
            Callable[P, R], functools.lru_cache(maxsize=maxsize)(func)
        )


def bcache(
    folder_name: str | None = None, maxsize: int | None = None
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Basic disk caching using diskcache (with fallback to memory).

    Args:
        folder_name: Cache directory name
        maxsize: Maximum cache size (None for unlimited)
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        if HAS_DISKCACHE:
            cache_dir = get_cache_dir(folder_name)
            cache = DiskCache(str(cache_dir), size_limit=maxsize or int(1e9))

            @functools.wraps(func)
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                key = make_key(None, *args, **kwargs)
                result = cache.get(key)
                if result is not None:
                    return cast(R, result)
                result = func(*args, **kwargs)
                cache.set(key, result)
                return result

            return wrapper
        else:
            logger.warning(f"Falling back to memory cache for {func.__name__}")
            return mcache(maxsize=maxsize)(func)

    return decorator


def fcache(
    folder_name: str | None = None, maxsize: int | None = None
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Fast file-based caching using joblib (with fallback to memory).

    Args:
        folder_name: Cache directory name
        maxsize: Maximum cache size (None for unlimited)
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        if HAS_JOBLIB:
            cache_dir = get_cache_dir(folder_name)
            memory = Memory(str(cache_dir), verbose=0)
            return cast(Callable[P, R], memory.cache(func))
        else:
            logger.warning(f"Falling back to memory cache for {func.__name__}")
            return mcache(maxsize=maxsize)(func)

    return decorator


def ucache(
    folder_name: str | None = None,
    maxsize: int | None = None,
    preferred_engine: str | None = None,
    use_async: bool = False,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Universal caching that automatically selects best available backend.

    Args:
        folder_name: Cache directory name
        maxsize: Maximum cache size (None for unlimited)
        preferred_engine: Preferred caching backend:
            - 'cachebox': High-performance Rust-based caching
            - 'klepto': Scientific computing with flexible key mapping
            - 'diskcache': SQL-based disk caching
            - 'joblib': File-based caching for large arrays
            - 'cachetools': Flexible in-memory caching
            - 'memory': Simple functools.lru_cache
            - 'async': Async-capable caching (requires use_async=True)
        use_async: Whether to use async-capable caching

    Returns:
        A caching decorator using the best available or specified backend
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        # Handle async caching explicitly
        if use_async:
            try:
                from aiocache import Cache, cached

                return cached(cache=Cache())(func)  # type: ignore
            except ImportError:
                logger.warning(
                    f"aiocache not available for {func.__name__}, falling back"
                )

        # Try preferred engine first if specified
        if preferred_engine:
            if preferred_engine == "cachebox" and HAS_CACHEBOX:
                from .engines.cachebox import CacheBoxEngine

                engine = CacheBoxEngine(
                    create_cache_config(
                        maxsize=maxsize,
                        folder_name=folder_name,
                    )
                )
                return engine.cache(func)
            elif preferred_engine == "klepto" and HAS_KLEPTO:
                from .engines.klepto import KleptoEngine

                engine = KleptoEngine(
                    create_cache_config(
                        maxsize=maxsize,
                        folder_name=folder_name,
                    )
                )
                return engine.cache(func)
            elif preferred_engine == "diskcache" and HAS_DISKCACHE:
                return bcache(folder_name=folder_name, maxsize=maxsize)(func)
            elif preferred_engine == "joblib" and HAS_JOBLIB:
                return fcache(folder_name=folder_name, maxsize=maxsize)(func)
            elif preferred_engine == "cachetools":
                try:
                    from cachetools import LRUCache, cached

                    cache = LRUCache(maxsize=maxsize or float("inf"))
                    return cached(cache=cache)(func)  # type: ignore
                except ImportError:
                    logger.warning(
                        f"cachetools not available for {func.__name__}, falling back"
                    )
            elif preferred_engine == "memory":
                return mcache(maxsize=maxsize)(func)

            logger.warning(
                f"Preferred engine {preferred_engine} not available for {func.__name__}, trying alternatives"
            )

        # Auto-select best available backend
        try:
            from .engines.cachebox import CacheBoxEngine

            engine = CacheBoxEngine(
                create_cache_config(
                    maxsize=maxsize,
                    folder_name=folder_name,
                )
            )
            if engine.is_available:
                return engine.cache(func)
        except ImportError:
            pass

        try:
            from .engines.klepto import KleptoEngine

            engine = KleptoEngine(
                create_cache_config(
                    maxsize=maxsize,
                    folder_name=folder_name,
                )
            )
            if engine.is_available:
                return engine.cache(func)
        except ImportError:
            pass

        if HAS_JOBLIB:
            return fcache(folder_name=folder_name, maxsize=maxsize)(func)
        elif HAS_DISKCACHE:
            return bcache(folder_name=folder_name, maxsize=maxsize)(func)
        else:
            logger.warning(
                f"No disk caching available, using memory cache for {func.__name__}"
            )
            return mcache(maxsize=maxsize)(func)

    return decorator
