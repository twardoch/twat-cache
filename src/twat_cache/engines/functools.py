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

from functools import lru_cache
from typing import Any, cast

from loguru import logger

from twat_cache.types import CacheConfig, CacheKey, P, R
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

        # Initialize the cache storage
        maxsize = getattr(config, "maxsize", None)
        self._maxsize = maxsize if maxsize is not None else 128
        self._cache = lru_cache(maxsize=self._maxsize)
        logger.debug(f"Initialized functools cache with maxsize: {self._maxsize}")

    def _get_cached_value(self, key: CacheKey) -> R | None:
        """
        Retrieve a value from the cache.

        Args:
            key: The cache key to look up

        Returns:
            The cached value if found, None otherwise
        """
        try:
            return cast(R, self._cache.cache_info().hits)  # type: ignore
        except AttributeError:
            return None

    def _set_cached_value(self, key: CacheKey, value: R) -> None:
        """
        Store a value in the cache.

        Args:
            key: The cache key to store under
            value: The value to cache
        """
        # functools.lru_cache handles storage internally
        pass

    def clear(self) -> None:
        """Clear all cached values."""
        if hasattr(self._cache, "cache_clear"):
            self._cache.cache_clear()  # type: ignore
        self._hits = 0
        self._misses = 0
        logger.debug("Cleared functools cache")

    @property
    def stats(self) -> dict[str, Any]:
        """Get cache statistics."""
        stats = super().stats
        if hasattr(self._cache, "cache_info"):
            info = self._cache.cache_info()  # type: ignore
            stats.update(
                {
                    "type": "functools",
                    "maxsize": self._maxsize,
                    "current_size": info.currsize,
                    "hits": info.hits,
                    "misses": info.misses,
                }
            )
        return stats

    def validate_config(self) -> None:
        """
        Validate the engine configuration.

        Raises:
            ValueError: If the configuration is invalid
        """
        super().validate_config()

        # Additional functools-specific validation
        maxsize = getattr(self._config, "maxsize", None)
        if maxsize is not None and not isinstance(maxsize, int):
            msg = "maxsize must be an integer or None"
            raise ValueError(msg)

    def _get_backend_key_components(self) -> list[str]:
        """Get functools-specific components for key generation."""
        return ["functools"]  # Add backend type to key to avoid conflicts

    def cache(self, func: F) -> F:
        """Apply functools caching to the function.

        Args:
            func: Function to be cached

        Returns:
            Cached function wrapper
        """
        return cast(F, self._cache(func))
