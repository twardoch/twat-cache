#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "loguru",
#   "aiocache",
# ]
# ///
# this_file: src/twat_cache/engines/aiocache.py

"""Async-capable cache engine using aiocache."""

import asyncio
from typing import Any, cast

from aiocache import Cache, SimpleMemoryCache, RedisCache, MemcachedCache
from loguru import logger

from twat_cache.config import CacheConfig
from twat_cache.type_defs import CacheKey, P, AsyncR
from .base import BaseCacheEngine


class AioCacheEngine(BaseCacheEngine[P, AsyncR]):
    """
    Async-capable cache engine using aiocache.

    This engine provides asynchronous caching with support for:
    - Multiple backends (memory, Redis, Memcached)
    - TTL-based expiration
    - Maxsize limitation (via our wrapper)
    """

    def __init__(self, config: CacheConfig) -> None:
        """Initialize the aiocache engine."""
        super().__init__(config)

        # Select backend based on availability
        try:
            import redis

            self._cache: Cache = RedisCache(
                ttl=self._config.ttl or 0,
                namespace=self._config.folder_name,
            )
            logger.debug("Using Redis backend for aiocache")
        except ImportError:
            try:
                import pymemcache

                self._cache = MemcachedCache(
                    ttl=self._config.ttl or 0,
                    namespace=self._config.folder_name,
                )
                logger.debug("Using Memcached backend for aiocache")
            except ImportError:
                self._cache = SimpleMemoryCache(
                    ttl=self._config.ttl or 0,
                    namespace=self._config.folder_name,
                )
                logger.debug("Using memory backend for aiocache")

        logger.debug(
            f"Initialized {self.__class__.__name__} with ttl={self._config.ttl}"
        )

    async def _get_cached_value_async(self, key: CacheKey) -> AsyncR | None:
        """
        Retrieve a value from the cache asynchronously.

        Args:
            key: The cache key to look up

        Returns:
            The cached value if found and not expired, None otherwise
        """
        try:
            result = await self._cache.get(str(key))
            if result is None:
                return None
            return cast(AsyncR, result)
        except Exception as e:
            logger.warning(f"Error retrieving from aiocache: {e}")
            return None

    def _get_cached_value(self, key: CacheKey) -> AsyncR | None:
        """
        Retrieve a value from the cache.

        This is a synchronous wrapper around the async get method.

        Args:
            key: The cache key to look up

        Returns:
            The cached value if found and not expired, None otherwise
        """
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self._get_cached_value_async(key))

    async def _set_cached_value_async(self, key: CacheKey, value: AsyncR) -> None:
        """
        Store a value in the cache asynchronously.

        Args:
            key: The cache key to store under
            value: The value to cache
        """
        try:
            await self._cache.set(
                str(key),
                value,
                ttl=self._config.ttl or None,
            )
            self._size = await self._cache.raw("dbsize")  # type: ignore
        except Exception as e:
            logger.warning(f"Error storing to aiocache: {e}")

    def _set_cached_value(self, key: CacheKey, value: AsyncR) -> None:
        """
        Store a value in the cache.

        This is a synchronous wrapper around the async set method.

        Args:
            key: The cache key to store under
            value: The value to cache
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._set_cached_value_async(key, value))

    async def clear_async(self) -> None:
        """Clear all cached values asynchronously."""
        try:
            await self._cache.clear()
            self._hits = 0
            self._misses = 0
            self._size = 0
        except Exception as e:
            logger.warning(f"Error clearing aiocache: {e}")

    def clear(self) -> None:
        """Clear all cached values."""
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.clear_async())

    @property
    def stats(self) -> dict[str, Any]:
        """Get cache statistics."""
        base_stats = super().stats
        try:
            loop = asyncio.get_event_loop()
            info = loop.run_until_complete(self._cache.raw("info"))  # type: ignore
            base_stats.update(info)
        except Exception as e:
            logger.warning(f"Error getting aiocache stats: {e}")
        return base_stats

    def __del__(self) -> None:
        """Clean up resources."""
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self._cache.close())  # type: ignore
        except Exception as e:
            logger.warning(f"Error closing aiocache: {e}")

    @classmethod
    def is_available(cls) -> bool:
        """Check if this cache engine is available for use."""
        try:
            import aiocache

            return True
        except ImportError:
            return False
