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
from typing import Any, Awaitable, TypeVar, cast, Optional, Union, overload
from collections.abc import Callable

from loguru import logger

from .config import create_cache_config, CacheConfig, CacheType, EvictionPolicy
from .engines.base import BaseCacheEngine
from .type_defs import P, R, AsyncR

# Try to import optional backends
try:
    import aiocache

    HAS_AIOCACHE = True
except ImportError:
    HAS_AIOCACHE = False
    logger.warning("aiocache not available, will fall back to async wrapper")

try:
    import cachebox

    HAS_CACHEBOX = True
except ImportError:
    HAS_CACHEBOX = False
    logger.warning("cachebox not available, will fall back to cachetools")

try:
    import cachetools

    HAS_CACHETOOLS = True
except ImportError:
    HAS_CACHETOOLS = False
    logger.warning("cachetools not available, will fall back to functools")

try:
    import diskcache

    HAS_DISKCACHE = True
except ImportError:
    HAS_DISKCACHE = False
    logger.warning("diskcache not available, will fall back to memory cache")

try:
    import joblib

    HAS_JOBLIB = True
except ImportError:
    HAS_JOBLIB = False
    logger.warning("joblib not available, will fall back to memory cache")

try:
    import klepto

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
    policy: EvictionPolicy = "lru",
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Memory-based caching using fastest available backend.

    Args:
        maxsize: Maximum cache size (None for unlimited)
        ttl: Time-to-live in seconds (None for no expiry)
        policy: Cache eviction policy

    Returns:
        A caching decorator using the best available memory backend
    """
    config = create_cache_config(
        maxsize=maxsize,
        ttl=ttl,
        policy=policy,
        cache_type="memory",
    )

    if HAS_CACHEBOX:
        from .engines.cachebox import CacheBoxEngine

        engine = CacheBoxEngine(config)
        return engine.cache
    elif HAS_CACHETOOLS:
        from .engines.cachetools import CacheToolsEngine

        engine = CacheToolsEngine(config)
        return engine.cache
    else:
        from .engines.functools import FunctoolsEngine

        engine = FunctoolsEngine(config)
        return engine.cache


def bcache(
    folder_name: Optional[str] = None,
    maxsize: Optional[int] = None,
    ttl: Optional[float] = None,
    policy: EvictionPolicy = "lru",
    use_sql: bool = True,
    secure: bool = True,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
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

        engine = DiskCacheEngine(config)
        return engine.cache
    elif HAS_KLEPTO and use_sql:
        from .engines.klepto import KleptoEngine

        engine = KleptoEngine(config)
        return engine.cache
    else:
        return mcache(maxsize=maxsize, ttl=ttl, policy=policy)


def fcache(
    folder_name: Optional[str] = None,
    maxsize: Optional[int] = None,
    ttl: Optional[float] = None,
    compress: bool = False,
    secure: bool = True,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
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

        engine = JoblibEngine(config)
        return engine.cache
    elif HAS_KLEPTO:
        from .engines.klepto import KleptoEngine

        engine = KleptoEngine(config)
        return engine.cache
    else:
        return mcache(maxsize=maxsize, ttl=ttl)


@overload
def acache(
    maxsize: Optional[int] = None,
    ttl: Optional[float] = None,
    policy: EvictionPolicy = "lru",
) -> Callable[[Callable[P, Awaitable[AsyncR]]], Callable[P, Awaitable[AsyncR]]]: ...


@overload
def acache(
    maxsize: Optional[int] = None,
    ttl: Optional[float] = None,
    policy: EvictionPolicy = "lru",
) -> Callable[[Callable[P, AsyncR]], Callable[P, Awaitable[AsyncR]]]: ...


def acache(
    maxsize: Optional[int] = None,
    ttl: Optional[float] = None,
    policy: EvictionPolicy = "lru",
) -> Union[
    Callable[[Callable[P, Awaitable[AsyncR]]], Callable[P, Awaitable[AsyncR]]],
    Callable[[Callable[P, AsyncR]], Callable[P, Awaitable[AsyncR]]],
]:
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

        engine = AioCacheEngine(config)
        return engine.cache
    else:
        # Fall back to async wrapper around memory cache
        def decorator(
            func: Union[Callable[P, AsyncR], Callable[P, Awaitable[AsyncR]]],
        ) -> Callable[P, Awaitable[AsyncR]]:
            mem_cache = mcache(maxsize=maxsize, ttl=ttl, policy=policy)
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


def ucache(
    folder_name: Optional[str] = None,
    maxsize: Optional[int] = None,
    ttl: Optional[float] = None,
    policy: EvictionPolicy = "lru",
    preferred_engine: Optional[str] = None,
    use_sql: bool = False,
    compress: bool = False,
    secure: bool = True,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
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

    # Try preferred engine first if specified
    if preferred_engine:
        if preferred_engine == "cachebox" and HAS_CACHEBOX:
            from .engines.cachebox import CacheBoxEngine

            return CacheBoxEngine(config).cache
        elif preferred_engine == "klepto" and HAS_KLEPTO:
            from .engines.klepto import KleptoEngine

            return KleptoEngine(config).cache
        elif preferred_engine == "diskcache" and HAS_DISKCACHE:
            from .engines.diskcache import DiskCacheEngine

            return DiskCacheEngine(config).cache
        elif preferred_engine == "joblib" and HAS_JOBLIB:
            from .engines.joblib import JoblibEngine

            return JoblibEngine(config).cache
        elif preferred_engine == "cachetools" and HAS_CACHETOOLS:
            from .engines.cachetools import CacheToolsEngine

            return CacheToolsEngine(config).cache
        elif preferred_engine == "functools":
            from .engines.functools import FunctoolsEngine

            return FunctoolsEngine(config).cache
        elif preferred_engine == "aiocache" and HAS_AIOCACHE:
            from .engines.aiocache import AioCacheEngine

            return AioCacheEngine(config).cache  # type: ignore

    # Auto-select best available backend
    if folder_name:
        if use_sql and HAS_DISKCACHE:
            return bcache(
                folder_name=folder_name,
                maxsize=maxsize,
                ttl=ttl,
                policy=policy,
                use_sql=True,
                secure=secure,
            )
        elif compress and HAS_JOBLIB:
            return fcache(
                folder_name=folder_name,
                maxsize=maxsize,
                ttl=ttl,
                compress=True,
                secure=secure,
            )
        else:
            return bcache(
                folder_name=folder_name,
                maxsize=maxsize,
                ttl=ttl,
                policy=policy,
                use_sql=False,
                secure=secure,
            )
    else:
        return mcache(maxsize=maxsize, ttl=ttl, policy=policy)
