#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "loguru",
# ]
# ///
# this_file: src/twat_cache/engines/functools.py

"""
Functools-based cache engine implementation.

This module provides a memory-based cache implementation using Python's
built-in functools.lru_cache. This is the always-available fallback cache
backend that requires no external dependencies.
"""

from typing import Any, cast
from collections.abc import Callable
from functools import wraps, lru_cache
import json

from twat_cache.type_defs import CacheConfig, P, R, CacheKey
from .base import BaseCacheEngine


class FunctoolsCacheEngine(BaseCacheEngine[P, R]):
    """
    Memory-based cache engine implementation using functools.lru_cache.

    This engine uses Python's built-in functools.lru_cache for caching,
    providing an efficient in-memory caching solution that's always available.

    Args:
        config: Cache configuration object implementing CacheConfig protocol
    """

    def __init__(self, config: CacheConfig) -> None:
        """Initialize the functools cache engine."""
        super().__init__(config)
        self._cache = lru_cache(maxsize=config.maxsize)

    def get(self, key: str) -> R | None:
        """
        Get a value from the cache.

        Args:
            key: The key to look up

        Returns:
            The cached value if found, None otherwise
        """
        try:
            return self._cache.cache_getitem(lambda k: k, key)  # type: ignore
        except KeyError:
            return None

    def set(self, key: str, value: R) -> None:
        """
        Store a value in the cache.

        Args:
            key: The key to store under
            value: The value to cache
        """
        self._cache(lambda k: k)(key)  # type: ignore
        self._cache.cache_setitem(lambda k: k, key, value)  # type: ignore

    def clear(self) -> None:
        """Clear all cached values and reset statistics."""
        self._cache.cache_clear()

    @property
    def name(self) -> str:
        """
        Get the name of the cache engine.

        Returns:
            str: The name of the cache engine
        """
        return "memory"

    @property
    def stats(self) -> dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            dict: A dictionary containing cache statistics
        """
        return {
            "type": "functools",
            "maxsize": self._config.maxsize,
            "current_size": len(self._cache),
            "hits": self._hits,
            "misses": self._misses,
            "size": len(self._cache),
            "backend": self.__class__.__name__,
            "path": None,
        }

    def validate_config(self) -> None:
        """
        Validate the engine configuration.

        Raises:
            ValueError: If the configuration is invalid
        """
        super().validate_config()

        # Additional functools-specific validation
        maxsize = self._config.maxsize
        if maxsize is not None and not isinstance(maxsize, int):
            msg = "maxsize must be an integer or None"
            raise ValueError(msg)

    def _get_backend_key_components(self) -> list[str]:
        """Get functools-specific components for key generation."""
        return ["functools"]  # Add backend type to key to avoid conflicts

    def cache(
        self, func: Callable[P, R] | None = None
    ) -> Callable[P, R] | Callable[[Callable[P, R]], Callable[P, R]]:
        """
        Decorate a function with caching behavior.

        This method can be used both as a decorator and as a decorator factory:

        @engine.cache
        def func(): ...

        @engine.cache()
        def func(): ...

        Args:
            func: The function to cache, or None if used as a decorator factory

        Returns:
            A wrapped function with caching behavior, or a decorator
        """

        def decorator(f: Callable[P, R]) -> Callable[P, R]:
            @wraps(f)
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                key = json.dumps(tuple(args) + tuple(kwargs.items()), sort_keys=True)
                result = self._get_cached_value(key)
                if result is None:
                    try:
                        result = f(*args, **kwargs)
                        self._set_cached_value(key, result)
                    except Exception as e:
                        # Cache the exception to avoid recomputing
                        # We know the exception is safe to cache in this context
                        self._set_cached_value(key, cast(R, e))
                        raise
                elif isinstance(result, Exception):
                    raise result
                return result

            return wrapper

        if func is None:
            return decorator
        return decorator(func)

    def _get_cached_value(self, key: CacheKey) -> R | None:
        """
        Retrieve a value from the cache.

        Args:
            key: The cache key to look up

        Returns:
            The cached value if found, None otherwise
        """
        try:
            return self._cache.cache_getitem(lambda k: k, str(key))  # type: ignore
        except KeyError:
            return None

    def _set_cached_value(self, key: CacheKey, value: R) -> None:
        """
        Store a value in the cache.

        Args:
            key: The cache key to store under
            value: The value to cache
        """
        self._cache(lambda k: k)(str(key))  # type: ignore
        self._cache.cache_setitem(lambda k: k, str(key), value)  # type: ignore
