#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "loguru",
#   "cachetools",
#   "types-cachetools",
# ]
# ///
# this_file: src/twat_cache/engines/cachetools.py

"""Flexible in-memory cache engine using cachetools package."""

from __future__ import annotations

from typing import Any, cast
from collections.abc import Callable

from twat_cache.config import CacheConfig
from twat_cache.engines.base import BaseCacheEngine, is_package_available
from twat_cache.type_defs import CacheKey, P, R


class CacheToolsEngine(BaseCacheEngine[P, R]):
    """Cache engine using cachetools."""

    @classmethod
    def is_available(cls) -> bool:
        """Check if cachetools is available."""
        return is_package_available("cachetools")

    def __init__(self, config: CacheConfig) -> None:
        """Initialize the cachetools engine.

        Args:
            config: Cache configuration settings.
        """
        super().__init__(config)
        self._config = config
        self._cache = None

        if not CacheToolsEngine.is_available():
            msg = "cachetools is not available"
            raise ImportError(msg)

        # Import here to avoid loading if not used
        from cachetools import (
            Cache,
            LRUCache,
            LFUCache,
            TTLCache,
            RRCache,
            TLRUCache,
        )

        # Select cache type based on policy and TTL
        if config.ttl:
            if config.policy == "lru":
                cache_type = TLRUCache
            else:
                cache_type = TTLCache
        else:
            cache_types = {
                "lru": LRUCache,
                "lfu": LFUCache,
                "rr": RRCache,
            }
            cache_type = cache_types.get(config.policy, LRUCache)

        cache_args: dict[str, Any] = {"maxsize": config.maxsize or 100}
        if config.ttl and (cache_type is TTLCache or cache_type is TLRUCache):
            # Only pass ttl if it's configured AND the cache type supports it.
            # TTLCache and TLRUCache from cachetools accept a 'ttl' parameter.
            cache_args["ttl"] = config.ttl

        self._cache: Cache = cache_type(**cache_args) # type: ignore[call-arg]

    def cache(self, func: Callable[P, R]) -> Callable[P, R]:
        """Decorate a function with caching.

        Args:
            func: Function to cache.

        Returns:
            Callable: Decorated function with caching.
        """
        if not self._cache:
            msg = "Cache not initialized"
            raise RuntimeError(msg)

        # Import here to avoid loading if not used
        from cachetools import cached

        return cast(
            Callable[P, R],
            cached(
                cache=self._cache,
            )(func),
        )

    def _get_cached_value(self, key: CacheKey) -> R | None:
        """Get a value from the cache.

        Args:
            key: Cache key.

        Returns:
            Optional[R]: Cached value if found, None otherwise.
        """
        if not self._cache:
            # This case should ideally not be hit if used by BaseCacheEngine.cache decorator,
            # which calls _get_cached_value. But good for direct use.
            self._misses += 1 # Assuming direct call if _cache is None
            return None

        # cachetools .get() returns the value or the default (None here)
        value = self._cache.get(str(key))
        if value is not None: # Or however cachetools signifies a hit from a miss with default=None
            self._hits +=1 # Approximate, actual hits are internal to cachetools object for @cached
        else:
            self._misses +=1 # Approximate
        return cast(R | None, value)

    def _set_cached_value(self, key: CacheKey, value: R) -> None:
        """Set a value in the cache.

        Args:
            key: Cache key.
            value: Value to cache.
        """
        if not self._cache:
            msg = "Cache not initialized" # Should not happen if __init__ ran
            raise RuntimeError(msg)

        self._cache[str(key)] = value
        self._size = len(self._cache) # Approximate size tracking

    def clear(self) -> None:
        """Clear all cached values."""
        if not self._cache:
            msg = "Cache not initialized"
            raise RuntimeError(msg)

        self._cache.clear()

    @property
    def stats(self) -> dict[str, Any]:
        """Get cache statistics.

        Returns:
            dict[str, Any]: Dictionary of cache statistics.
        """
        if not self._cache:
            msg = "Cache not initialized"
            raise RuntimeError(msg)

        return {
            "hits": getattr(self._cache, "hits", 0),
            "misses": getattr(self._cache, "misses", 0),
            "size": len(self._cache),
            "maxsize": self._cache.maxsize,
            "policy": self._config.policy,
            "ttl": getattr(self._cache, "ttl", None),
        }
