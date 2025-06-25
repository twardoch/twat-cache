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

import asyncio # Moved to top
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

        if not self.is_available:
            msg = "aiocache is not available"
            raise ImportError(msg)

        # Import base and default
        from aiocache import Cache, SimpleMemoryCache

        # Conditionally import and try to use RedisCache
        if is_package_available("redis"):
            try:
                from aiocache import RedisCache
                self._cache: Cache = RedisCache(
                    endpoint=config.redis_host or "localhost",
                    port=config.redis_port or 6379,
                    namespace=config.folder_name,
                    ttl=config.ttl,
                )
                return # Successfully initialized RedisCache
            except ImportError: # Should not happen if is_package_available is True, but defensive
                pass
            except Exception: # Catch connection errors etc.
                # Log this error, then fallback
                # from loguru import logger # Avoid top-level import for conditional use
                # logger.warning("Failed to initialize aiocache.RedisCache, falling back.")
                pass


        # Conditionally import and try to use MemcachedCache
        if is_package_available("pymemcache"):
            try:
                from aiocache import MemcachedCache
                self._cache = MemcachedCache(
                    endpoint=config.memcached_host or "localhost", # type: ignore
                    port=config.memcached_port or 11211, # type: ignore
                    namespace=config.folder_name,
                    ttl=config.ttl,
                )
                return # Successfully initialized MemcachedCache
            except ImportError:
                pass
            except Exception:
                # from loguru import logger
                # logger.warning("Failed to initialize aiocache.MemcachedCache, falling back.")
                pass

        # Default fallback to SimpleMemoryCache only if self._cache hasn't been set
        if self._cache is None:
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
        if not self._cache:
            msg = "Cache not initialized"
            raise RuntimeError(msg)

        # Import here to avoid loading if not used
        from aiocache import cached

        return cast(
            Callable[P, R],
            cached(
                ttl=self._config.ttl,
                cache=self._cache, # This is the aiocache instance
                namespace=self._config.folder_name, # aiocache uses namespace
            )(func),
        )

    def _get_cached_value(self, key: CacheKey) -> R | None:
        """Get a value from the cache (synchronous wrapper for aiocache)."""
        if not self._cache:
            self._misses += 1
            return None
        try:
            # Aiocache methods are async, so we need to run them in an event loop
            # This is a blocking call, which is not ideal for an async engine's direct sync methods
            # but necessary to fulfill the BaseCacheEngine synchronous abstract method.
            loop = asyncio.get_event_loop()
            value = loop.run_until_complete(self._cache.get(str(key)))
            if value is not None:
                self._hits += 1
            else:
                self._misses += 1
            return cast(R | None, value)
        except Exception: # pragma: no cover
            self._misses += 1
            return None

    def _set_cached_value(self, key: CacheKey, value: R) -> None:
        """Set a value in the cache (synchronous wrapper for aiocache)."""
        if not self._cache:
            raise RuntimeError("Cache not initialized") # Should not happen

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._cache.set(str(key), value, ttl=self._config.ttl))
        # self._size might not be easily trackable here without another async call

    def clear(self) -> None:
        """Clear all cached values (synchronous wrapper for aiocache)."""
        if not self._cache:
            raise RuntimeError("Cache not initialized") # Should not happen

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._cache.clear(namespace=self._config.folder_name))
        self._hits = 0
        self._misses = 0
        # self._size = 0 # Size tracking might be complex

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
            "hits": self._cache.hits,
            "misses": self._cache.misses,
            "size": len(self._cache),
            "backend": self._cache.__class__.__name__,
        }

    # Removed duplicated is_available property
    # The @classmethod is_available is correctly defined in the class.
