#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "loguru",
# ]
# ///
# this_file: src/twat_cache/engines/base.py

"""
Base cache engine implementation.

This module provides the foundation for all cache backend implementations,
implementing common functionality and enforcing the CacheEngine protocol.
"""

from abc import ABC, abstractmethod
from functools import wraps
import inspect
from pathlib import Path
from typing import Any, Generic, cast
from collections.abc import Callable

from loguru import logger

from twat_cache.types import CacheConfig, CacheKey, P, R
from twat_cache.paths import get_cache_path, validate_cache_path


class BaseCacheEngine(ABC, Generic[P, R]):
    """
    Abstract base class for cache engine implementations.

    This class provides common functionality and enforces the CacheEngine protocol
    for all cache backend implementations.

    Args:
        config: Cache configuration object implementing CacheConfig protocol
    """

    def __init__(self, config: CacheConfig) -> None:
        """Initialize the cache engine with the given configuration."""
        self._config = config
        self._hits = 0
        self._misses = 0
        self._size = 0
        self._cache_path: Path | None = None

        # Validate configuration
        self.validate_config()

        # Initialize cache path if needed
        if hasattr(self._config, "folder_name"):
            self._cache_path = get_cache_path(self._config.folder_name)

        logger.debug(f"Initialized {self.__class__.__name__} with config: {config}")

    @property
    def stats(self) -> dict[str, Any]:
        """Get cache statistics."""
        return {
            "hits": self._hits,
            "misses": self._misses,
            "size": self._size,
            "maxsize": getattr(self._config, "maxsize", None),
            "backend": self.__class__.__name__,
            "path": str(self._cache_path) if self._cache_path else None,
        }

    def validate_config(self) -> None:
        """
        Validate the engine configuration.

        Raises:
            ValueError: If the configuration is invalid
        """
        # Validate maxsize if present
        if hasattr(self._config, "maxsize"):
            maxsize = self._config.maxsize
            if maxsize is not None and maxsize <= 0:
                msg = "maxsize must be positive or None"
                raise ValueError(msg)

        # Validate cache folder if provided
        if hasattr(self._config, "cache_dir"):
            try:
                validate_cache_path(self._config.cache_dir)
            except ValueError as e:
                msg = f"Invalid cache folder: {e}"
                raise ValueError(msg) from e

    def _make_key(self, func: Callable[P, R], args: tuple, kwargs: dict) -> CacheKey:
        """
        Generate a cache key for the given function and arguments.

        This method creates a unique key based on:
        1. The function's module and name
        2. The function's arguments
        3. Any relevant configuration parameters

        Args:
            func: The function being cached
            args: Positional arguments to the function
            kwargs: Keyword arguments to the function

        Returns:
            A cache key suitable for the backend
        """
        # Get function info
        module = inspect.getmodule(func)
        module_name = module.__name__ if module else "unknown_module"
        func_name = func.__name__

        # Convert args and kwargs to a stable string representation
        args_str = str(args) if args else ""
        kwargs_str = str(sorted(kwargs.items())) if kwargs else ""

        # Combine components into a key
        key_components = [
            module_name,
            func_name,
            args_str,
            kwargs_str,
        ]

        # Add any backend-specific components
        backend_key = self._get_backend_key_components()
        if backend_key:
            key_components.extend(backend_key)

        return tuple(key_components)

    def _get_backend_key_components(self) -> list[str]:
        """
        Get backend-specific components for key generation.

        Override this in backend implementations if needed.
        """
        return []

    @abstractmethod
    def _get_cached_value(self, key: CacheKey) -> R | None:
        """
        Retrieve a value from the cache.

        Args:
            key: The cache key to look up

        Returns:
            The cached value if found, None otherwise
        """
        ...

    @abstractmethod
    def _set_cached_value(self, key: CacheKey, value: R) -> None:
        """
        Store a value in the cache.

        Args:
            key: The cache key to store under
            value: The value to cache
        """
        ...

    @abstractmethod
    def clear(self) -> None:
        """Clear all cached values."""
        ...

    def cache(self, func: Callable[P, R]) -> Callable[P, R]:
        """
        Decorate a function with caching capability.

        Args:
            func: The function to cache

        Returns:
            A wrapped function that will use the cache
        """

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            # Generate cache key
            key = self._make_key(func, args, kwargs)

            # Try to get from cache
            cached_value = self._get_cached_value(key)
            if cached_value is not None:
                self._hits += 1
                logger.trace(f"Cache hit for {func.__name__} with key {key}")
                return cached_value

            # Cache miss - compute and store
            self._misses += 1
            value = func(*args, **kwargs)
            self._set_cached_value(key, value)
            self._size += 1
            logger.trace(f"Cache miss for {func.__name__} with key {key}")

            return value

        return cast(Callable[P, R], wrapper)


class CacheEngine(BaseCacheEngine[P, R]):
    """
    Concrete implementation of the cache engine protocol.

    This class provides a default implementation of the abstract methods
    defined in BaseCacheEngine. It can be used directly or subclassed
    for more specific caching needs.
    """

    def _get_cached_value(self, key: CacheKey) -> R | None:
        """
        Retrieve a value from the cache.

        This default implementation always returns None, indicating a cache miss.
        Subclasses should override this with actual caching logic.

        Args:
            key: The cache key to look up

        Returns:
            None, indicating a cache miss
        """
        return None

    def _set_cached_value(self, key: CacheKey, value: R) -> None:
        """
        Store a value in the cache.

        This default implementation does nothing.
        Subclasses should override this with actual caching logic.

        Args:
            key: The cache key to store under
            value: The value to cache
        """
        pass

    def clear(self) -> None:
        """
        Clear all cached values.

        This default implementation does nothing.
        Subclasses should override this with actual cache clearing logic.
        """
        pass

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

    def cache(
        self, func: Callable[P, R] | None = None
    ) -> Callable[P, R] | Callable[[Callable[P, R]], Callable[P, R]]:
        """
        Decorate a function to cache its results.

        This method can be used both as a decorator and as a decorator factory:

        @engine.cache
        def func(): ...

        @engine.cache()
        def func(): ...

        Args:
            func: The function to cache, or None if used as a decorator factory

        Returns:
            A wrapped function that caches its results, or a decorator
        """

        def decorator(f: Callable[P, R]) -> Callable[P, R]:
            @wraps(f)
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                key = self._make_key(f, args, kwargs)
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
