#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "loguru",
#   "cachetools",
#   "types-cachetools",
# ]
# ///
# this_file: src/twat_cache/engines/cachetools.py

"""Memory-based cache engine using cachetools."""

from typing import Any, cast

from cachetools import Cache, LRUCache, TTLCache, LFUCache, FIFOCache, RRCache
from loguru import logger

from twat_cache.config import CacheConfig
from twat_cache.type_defs import CacheKey, P, R
from .base import BaseCacheEngine


class CacheToolsEngine(BaseCacheEngine[P, R]):
    """
    Memory-based cache engine using cachetools.

    This engine provides flexible in-memory caching with support for:
    - Multiple eviction policies (LRU, LFU, FIFO, RR)
    - TTL-based expiration
    - Maxsize limitation
    """

    def __init__(self, config: CacheConfig) -> None:
        """Initialize the cachetools cache engine."""
        super().__init__(config)
        maxsize = config.maxsize or float("inf")

        # Create cache based on policy
        if config.ttl is not None:
            self._cache: Cache = TTLCache(
                maxsize=maxsize,
                ttl=config.ttl,
            )
        elif config.policy == "lru":
            self._cache = LRUCache(maxsize=maxsize)
        elif config.policy == "lfu":
            self._cache = LFUCache(maxsize=maxsize)
        elif config.policy == "fifo":
            self._cache = FIFOCache(maxsize=maxsize)
        elif config.policy == "rr":
            self._cache = RRCache(maxsize=maxsize)
        else:
            # Default to LRU
            self._cache = LRUCache(maxsize=maxsize)

        logger.debug(
            f"Initialized {self.__class__.__name__} with "
            f"maxsize={maxsize}, policy={config.policy}"
        )

    def _get_cached_value(self, key: CacheKey) -> R | None:
        """
        Retrieve a value from the cache.

        Args:
            key: The cache key to look up

        Returns:
            The cached value if found and not expired, None otherwise
        """
        try:
            return cast(R, self._cache.get(key))
        except Exception as e:
            logger.warning(f"Error retrieving from cachetools cache: {e}")
            return None

    def _set_cached_value(self, key: CacheKey, value: R) -> None:
        """
        Store a value in the cache.

        Args:
            key: The cache key to store under
            value: The value to cache
        """
        try:
            self._cache[key] = value
            self._size = len(self._cache)
        except Exception as e:
            logger.warning(f"Error storing to cachetools cache: {e}")

    def clear(self) -> None:
        """Clear all cached values."""
        try:
            self._cache.clear()
            self._hits = 0
            self._misses = 0
            self._size = 0
        except Exception as e:
            logger.warning(f"Error clearing cachetools cache: {e}")

    @property
    def stats(self) -> dict[str, Any]:
        """Get cache statistics."""
        base_stats = super().stats
        try:
            base_stats.update(
                {
                    "currsize": len(self._cache),
                    "maxsize": self._cache.maxsize,
                    "policy": self._config.policy,
                }
            )
        except Exception as e:
            logger.warning(f"Error getting cachetools stats: {e}")
        return base_stats

    @classmethod
    def is_available(cls) -> bool:
        """Check if this cache engine is available for use."""
        try:
            import cachetools

            return True
        except ImportError:
            return False
