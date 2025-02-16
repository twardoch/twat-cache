#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "loguru",
#   "pydantic",
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
import json
from pathlib import Path
from typing import Any, Generic, cast, Optional
from collections.abc import Callable
from importlib import util

from loguru import logger

from twat_cache.config import CacheConfig
from twat_cache.type_defs import CacheKey, P, R
from twat_cache.paths import get_cache_path, validate_cache_path


def is_package_available(package_name: str) -> bool:
    """Check if a Python package is available.

    Args:
        package_name: Name of the package to check.

    Returns:
        bool: True if the package is available, False otherwise.
    """
    return bool(util.find_spec(package_name))


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
        self._cache: dict[CacheKey, tuple[R, float | None]] = {}

        # Validate configuration
        self.validate_config()

        # Initialize cache path if needed
        if self._config.folder_name is not None:
            self._cache_path = get_cache_path(self._config.folder_name)
            if self._config.secure:
                self._cache_path.chmod(0o700)

        logger.debug(f"Initialized {self.__class__.__name__} with config: {config}")

    @property
    def stats(self) -> dict[str, Any]:
        """Get cache statistics."""
        return {
            "hits": self._hits,
            "misses": self._misses,
            "size": self._size,
            "maxsize": self._config.maxsize,
            "backend": self.__class__.__name__,
            "path": str(self._cache_path) if self._cache_path else None,
            "policy": self._config.policy,
            "ttl": self._config.ttl,
        }

    def validate_config(self) -> None:
        """
        Validate the engine configuration.

        Raises:
            ValueError: If the configuration is invalid
        """
        # Config is already validated by Pydantic
        # Just validate cache folder if provided
        if self._config.folder_name is not None:
            try:
                validate_cache_path(self._config.folder_name)
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
        try:
            # Try JSON serialization first for stable representation
            args_str = json.dumps(args, sort_keys=True) if args else ""
            kwargs_str = (
                json.dumps(dict(sorted(kwargs.items())), sort_keys=True)
                if kwargs
                else ""
            )
        except (TypeError, ValueError):
            # Fall back to str() for non-JSON-serializable objects
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
        components = []
        if self._config.ttl is not None:
            components.append(f"ttl={self._config.ttl}")
        if self._config.policy != "lru":
            components.append(f"policy={self._config.policy}")
        return components

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
                if isinstance(cached_value, Exception):
                    raise cached_value
                return cast(R, cached_value)

            # Cache miss - compute and store
            self._misses += 1
            try:
                value = func(*args, **kwargs)
                self._set_cached_value(key, value)
            except Exception as e:
                # Cache the exception
                self._set_cached_value(key, cast(R, e))
                raise
            self._size += 1
            logger.trace(f"Cache miss for {func.__name__} with key {key}")

            return value

        return wrapper

    def get(self, key: str) -> R | None:
        """Get a value from the cache."""
        return self._get_cached_value(key)

    def set(self, key: str, value: R) -> None:
        """Set a value in the cache."""
        self._set_cached_value(key, value)

    @property
    def name(self) -> str:
        """Get the name of the cache engine."""
        return self.__class__.__name__

    @classmethod
    def is_available(cls) -> bool:
        """Check if this cache engine is available for use."""
        return True  # Override in subclasses if availability depends on imports


class CacheEngine(BaseCacheEngine[P, R]):
    """
    Concrete implementation of the cache engine protocol.

    This class provides a default implementation using a simple in-memory
    dictionary cache with the configured eviction policy.
    """

    def _get_cached_value(self, key: CacheKey) -> R | None:
        """
        Retrieve a value from the cache.

        Args:
            key: The cache key to look up

        Returns:
            The cached value if found and not expired, None otherwise
        """
        if key not in self._cache:
            return None

        value, expiry = self._cache[key]
        if expiry is not None and expiry <= 0:
            del self._cache[key]
            self._size -= 1
            return None

        return value

    def _set_cached_value(self, key: CacheKey, value: R) -> None:
        """
        Store a value in the cache.

        Args:
            key: The cache key to store under
            value: The value to cache
        """
        # Check maxsize
        if self._config.maxsize is not None and self._size >= self._config.maxsize:
            # Remove oldest item based on policy
            if self._config.policy == "lru":
                # Remove least recently used
                oldest_key = next(iter(self._cache))
                del self._cache[oldest_key]
                self._size -= 1
            elif self._config.policy == "fifo":
                # Remove first item added
                oldest_key = next(iter(self._cache))
                del self._cache[oldest_key]
                self._size -= 1
            # Other policies would be implemented here

        # Store with TTL if configured
        expiry = self._config.ttl
        self._cache[key] = (value, expiry)
        self._size += 1

    def clear(self) -> None:
        """Clear all cached values."""
        self._cache.clear()
        self._size = 0
        self._hits = 0
        self._misses = 0
