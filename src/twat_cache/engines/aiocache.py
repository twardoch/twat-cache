#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "loguru",
#   "aiocache",
# ]
# ///
# this_file: src/twat_cache/engines/aiocache.py

"""Async-capable cache engine using aiocache package."""

from __future__ import annotations

from typing import Any, cast
from collections.abc import Callable

from twat_cache.config import CacheConfig
from twat_cache.engines.base import BaseCacheEngine, is_package_available
from twat_cache.type_defs import CacheKey, P, R


class AioCacheEngine(BaseCacheEngine[P, R]):
    """Cache engine using aiocache."""

    @classmethod
    def is_available(cls) -> bool:
        """Check if aiocache is available."""
        return is_package_available("aiocache")

    def __init__(self, config: CacheConfig) -> None:
        """Initialize the aiocache engine.

        Args:
            config: Cache configuration settings.
        """
        super().__init__(config)
        self._config = config
        self._cache = None

        if not AioCacheEngine.is_available():
            msg = "aiocache is not available"
            raise ImportError(msg)

        # Import here to avoid loading if not used
        from aiocache import Cache, RedisCache, SimpleMemoryCache

        # Select backend based on availability
        if is_package_available("redis"):
            self._cache: Cache = RedisCache(
                endpoint=config.redis_host or "localhost",
                port=config.redis_port or 6379,
                namespace=config.folder_name,
                ttl=config.ttl,
            )
        else:
            self._cache = SimpleMemoryCache(
                namespace=config.folder_name,
                ttl=config.ttl,
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
        from aiocache import cached

        # Use the cache class type instead of instance
        cache_type = type(self._cache)
        
        return cast(
            Callable[P, R],
            cached(
                ttl=self._config.ttl,
                cache=cache_type,
                namespace=self._config.folder_name,
                endpoint=getattr(self._cache, 'endpoint', None),
                port=getattr(self._cache, 'port', None),
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

        self._cache.set(str(key), value, ttl=self._config.ttl)

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
            "backend": self._cache.__class__.__name__,
        }

