"""
CacheBox-based cache engine implementation.

This module provides a cache engine implementation using the CacheBox library,
which offers high-performance in-memory caching with advanced features.
"""

from typing import Any, Dict, Optional, cast

from loguru import logger

from twat_cache.type_defs import (
    F,
    CacheKey,
    P,
    R,
    CacheConfig,
)
from .base import BaseCacheEngine


class CacheBoxEngine(BaseCacheEngine[P, R]):
    """Cache engine implementation using CacheBox."""

    def __init__(self, config: CacheConfig) -> None:
        """Initialize the cache engine with the given configuration."""
        super().__init__(config)
        self._hits = 0
        self._misses = 0
        self._cache: Dict[CacheKey, R] = {}
        self._maxsize = config.maxsize or None
        self._ttl = config.ttl

        try:
            import cachebox

            self._backend = cachebox.Cache(maxsize=self._maxsize)
        except ImportError as e:
            msg = "CacheBox not available"
            raise ImportError(msg) from e

    def cache(self, func: F) -> F:
        """
        Decorate a function to cache its results.

        Args:
            func: The function to cache

        Returns:
            A wrapped function that caches its results
        """
        return cast(F, self._backend.memoize(maxsize=self._maxsize)(func))

    def clear(self) -> None:
        """Clear all cached values."""
        if hasattr(self, "_backend"):
            self._backend.clear()
            self._hits = 0
            self._misses = 0

    def validate_config(self) -> None:
        """
        Validate the engine configuration.

        Raises:
            ValueError: If the configuration is invalid
        """
        if self._config.maxsize is not None and self._config.maxsize <= 0:
            msg = "maxsize must be positive"
            raise ValueError(msg)

        if self._config.ttl is not None and self._config.ttl < 0:
            msg = "ttl must be non-negative"
            raise ValueError(msg)

    @property
    def stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            A dictionary containing cache statistics:
            - hits: Number of cache hits
            - misses: Number of cache misses
            - size: Current number of items in cache
            - maxsize: Maximum number of items allowed
        """
        return {
            "hits": self._hits,
            "misses": self._misses,
            "size": len(self._cache),
            "maxsize": self._maxsize,
            "backend": "cachebox",
            "policy": "lru" if self._maxsize else None,
            "ttl": self._ttl,
        }

    @classmethod
    def is_available(cls) -> bool:
        """Check if this cache engine is available for use."""
        try:
            import cachebox

            return True
        except ImportError:
            return False
