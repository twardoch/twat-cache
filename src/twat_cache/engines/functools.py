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
from functools import wraps
import json

from loguru import logger

from twat_cache.types import CacheConfig, P, R
from .base import CacheEngine


class FunctoolsCacheEngine(CacheEngine[P, R]):
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

        # Initialize the cache storage
        maxsize = config.get_maxsize()
        self._maxsize = maxsize if maxsize is not None else 128
        self._hits = 0
        self._misses = 0
        self._cache: dict[str, R] = {}  # Use str keys for hashability
        self._cache_order: list[str] = []  # Track LRU order
        logger.debug(f"Initialized functools cache with maxsize: {self._maxsize}")

    def get(self, key: Any) -> R | None:
        """
        Get a value from the cache.

        Args:
            key: The key to look up

        Returns:
            The cached value if found, None otherwise
        """
        return self._get_cached_value(key)

    def set(self, key: Any, value: R) -> None:
        """
        Set a value in the cache.

        Args:
            key: The key to store under
            value: The value to cache
        """
        self._set_cached_value(key, value)

    def _make_key(self, *args: Any, **kwargs: Any) -> str:
        """
        Create a hashable key from function arguments.

        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            A string key that uniquely identifies the arguments
        """
        try:
            # Try to create a JSON-serializable representation
            key_dict = {
                "args": [
                    str(arg)
                    if not isinstance(arg, (int, float, str, bool, type(None)))
                    else arg
                    for arg in args
                ],
                "kwargs": {
                    k: str(v)
                    if not isinstance(v, (int, float, str, bool, type(None)))
                    else v
                    for k, v in sorted(kwargs.items())
                },
            }
            return json.dumps(key_dict, sort_keys=True, default=str)
        except (TypeError, ValueError):
            # Fallback to string representation if JSON serialization fails
            args_str = ",".join(repr(arg) for arg in args)
            kwargs_str = ",".join(f"{k}={repr(v)}" for k, v in sorted(kwargs.items()))
            return f"args[{args_str}]kwargs[{kwargs_str}]"

    def _get_cached_value(self, key: Any) -> R | None:
        """
        Retrieve a value from the cache.

        Args:
            key: The cache key to look up

        Returns:
            The cached value if found, None otherwise
        """
        try:
            str_key = self._make_key(key) if not isinstance(key, str) else key
            value = self._cache.get(str_key)
            if value is not None:
                self._hits += 1
                # Move to end (most recently used)
                if str_key in self._cache_order:
                    self._cache_order.remove(str_key)
                    self._cache_order.append(str_key)
                return value
            self._misses += 1
            return None
        except (TypeError, ValueError):
            self._misses += 1
            return None

    def _set_cached_value(self, key: Any, value: R) -> None:
        """
        Store a value in the cache.

        Args:
            key: The cache key to store under
            value: The value to cache
        """
        try:
            str_key = self._make_key(key) if not isinstance(key, str) else key

            # If key exists, update it and move to end
            if str_key in self._cache:
                self._cache[str_key] = value
                if str_key in self._cache_order:
                    self._cache_order.remove(str_key)
                    self._cache_order.append(str_key)
                return

            # If cache is full, remove oldest items until we have space
            while len(self._cache) >= self._maxsize and self._cache_order:
                oldest_key = self._cache_order.pop(0)
                self._cache.pop(oldest_key, None)

            # Add new item
            self._cache[str_key] = value
            self._cache_order.append(str_key)
        except (TypeError, ValueError):
            pass

    def clear(self) -> None:
        """Clear all cached values and reset statistics."""
        self._cache.clear()
        self._cache_order.clear()
        self._hits = 0
        self._misses = 0
        logger.debug("Cleared functools cache")

    @property
    def stats(self) -> dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            dict: A dictionary containing cache statistics
        """
        return {
            "type": "functools",
            "maxsize": self._maxsize,
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
        maxsize = self._config.get_maxsize()
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
                key = self._make_key(*args, **kwargs)
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
