"""
CacheBox-based cache engine implementation.

This module provides a cache engine implementation using the CacheBox library,
which offers high-performance in-memory caching with advanced features.
"""

from __future__ import annotations

from typing import Any, cast
from collections.abc import Callable

from twat_cache.config import CacheConfig
from twat_cache.engines.base import BaseCacheEngine, is_package_available
from twat_cache.type_defs import CacheKey, P, R


class CacheBoxEngine(BaseCacheEngine[P, R]):
    """Cache engine using cachebox."""

    @classmethod
    def is_available(cls) -> bool:
        """Check if cachebox is available."""
        return is_package_available("cachebox")

    def __init__(self, config: CacheConfig) -> None:
        """Initialize the cachebox engine.

        Args:
            config: Cache configuration settings.
        """
        super().__init__(config)
        self._config = config

        if not CacheBoxEngine.is_available():
            msg = "cachebox is not available"
            raise ImportError(msg)

        # Import here to avoid loading if not used
        from cachebox import Cache, LRUCache, LFUCache, FIFOCache, RRCache

        # Select cache type based on policy
        cache_types = {
            "lru": LRUCache,
            "lfu": LFUCache,
            "fifo": FIFOCache,
            "rr": RRCache,
        }

        cache_type = cache_types.get(config.policy, LRUCache)
        # CacheBox doesn't support TTL in constructor
        self._cache: Cache = cache_type(
            maxsize=config.maxsize or 100,
        )

    def cache(self, func: Callable[P, R]) -> Callable[P, R]:
        """Decorate a function with caching.

        Args:
            func: Function to cache.

        Returns:
            Callable: Decorated function with caching.
        """
        if self._cache is None:
            msg = "Cache not initialized"
            raise RuntimeError(msg)

        # Import here to avoid loading if not used
        from cachebox import cached

        return cast(
            Callable[P, R],
            cached(
                cache=self._cache,
                key_maker=None,  # Use default key generation
            )(func),
        )

    def _get_cached_value(self, key: CacheKey) -> R | None:
        """Get a value from the cache.

        Args:
            key: Cache key.

        Returns:
            Optional[R]: Cached value if found, None otherwise.
        """
        if self._cache is None:
            msg = "Cache not initialized"
            raise RuntimeError(msg)

        return cast(R | None, self._cache.get(str(key)))

    def _set_cached_value(self, key: CacheKey, value: R) -> None:
        """Set a value in the cache.

        Args:
            key: Cache key.
            value: Value to cache.
        """
        if self._cache is None:
            msg = "Cache not initialized"
            raise RuntimeError(msg)

        self._cache[str(key)] = value

    def get(self, key: CacheKey) -> R | None:
        """Get a value from the cache.

        Args:
            key: Cache key.

        Returns:
            Optional[R]: Cached value if found, None otherwise.
        """
        return self._get_cached_value(key)

    def set(self, key: CacheKey, value: R) -> None:
        """Set a value in the cache.

        Args:
            key: Cache key.
            value: Value to cache.
        """
        self._set_cached_value(key, value)

    def clear(self) -> None:
        """Clear all cached values."""
        if self._cache is None:
            msg = "Cache not initialized"
            raise RuntimeError(msg)

        self._cache.clear()

    @property
    def stats(self) -> dict[str, Any]:
        """Get cache statistics.

        Returns:
            dict[str, Any]: Dictionary of cache statistics.
        """
        if self._cache is None:
            msg = "Cache not initialized"
            raise RuntimeError(msg)

        return {
            "hits": self._cache.hits,
            "misses": self._cache.misses,
            "size": len(self._cache),
            "maxsize": self._cache.maxsize,
            "policy": self._config.policy,
        }

