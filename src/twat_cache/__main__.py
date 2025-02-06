#!/usr/bin/env python3
"""
Flexible caching utilities for Python functions.

This module provides a unified interface for caching function results using various
backends (memory, disk, SQL). It automatically handles cache directory management
and offers a simple decorator interface.

Example:
    from twat_cache import ucache

    @ucache()
    def expensive_computation(x):
        return x * x

    # Results will be cached automatically
    result = expensive_computation(42)
"""

import inspect
import uuid
from functools import lru_cache, cache
from pathlib import Path
from typing import Any, TypeVar, cast
from collections.abc import Callable

T = TypeVar("T")


@cache
def get_cache_path(folder_name: str | None = None) -> Path:
    """
    Get or create a cache directory path.

    Args:
        folder_name: Optional name for the cache folder. If None, generates a UUID
            based on the caller's file path.

    Returns:
        Path: The resolved cache directory path.
    """

    def generate_uuid() -> str:
        """Generate a UUID based on the file of the caller."""
        caller_frame = inspect.stack()[2]
        caller_file = caller_frame.filename
        caller_path = Path(caller_file).resolve()
        return str(uuid.uuid5(uuid.NAMESPACE_URL, str(caller_path)))

    try:
        import platformdirs

        root_cache_dir = Path(platformdirs.user_cache_dir())
    except ImportError:
        root_cache_dir = Path.home() / ".cache"

    if not folder_name:
        folder_name = generate_uuid()

    cache_path = root_cache_dir / folder_name
    cache_path.mkdir(parents=True, exist_ok=True)

    return cache_path


# Initialize optional caching backends
try:
    from diskcache import Cache

    DISK_CACHE: Any | None = Cache(get_cache_path("twat_cache"))
except ImportError:
    DISK_CACHE = None

try:
    from joblib import Memory

    JOBLIB_MEMORY: Any | None = Memory(get_cache_path("twat_cache"), verbose=0)
except ImportError:
    JOBLIB_MEMORY = None


def ucache(
    folder_name: str | None = None,
    use_sql: bool = False,
    maxsize: int | None = None,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    A decorator for caching function results with various backends.

    This decorator provides a unified interface for caching function results using
    different backends based on availability and requirements:
    - SQL-based caching using diskcache (if use_sql=True and available)
    - Joblib caching for numpy arrays and large objects (if available)
    - LRU caching in memory as fallback

    Args:
        folder_name: Optional name for the cache folder
        use_sql: Whether to use SQL-based caching (requires diskcache)
        maxsize: Maximum size for LRU cache (None means unlimited)

    Returns:
        A decorator function that wraps the target function with caching

    Example:
        @ucache(folder_name="my_cache")
        def expensive_function(x):
            return x * x
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        if use_sql and DISK_CACHE is not None:
            return cast(Callable[..., T], DISK_CACHE.memoize()(func))

        elif JOBLIB_MEMORY is not None:
            memory: Any = (
                JOBLIB_MEMORY
                if folder_name is None
                else Memory(get_cache_path(folder_name), verbose=0)  # type: ignore
            )
            return cast(Callable[..., T], memory.cache(func))

        else:
            return cast(Callable[..., T], lru_cache(maxsize=maxsize)(func))

    return decorator
