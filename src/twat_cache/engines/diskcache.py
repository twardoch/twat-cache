#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "loguru",
#   "diskcache",
#   "types-diskcache",
# ]
# ///
# this_file: src/twat_cache/engines/diskcache.py

"""Disk-based cache engine using diskcache."""

from __future__ import annotations

import time
from typing import Any, cast
from collections.abc import Callable

from diskcache import Cache
from loguru import logger

from twat_cache.config import CacheConfig
from twat_cache.type_defs import CacheKey, P, R
from .base import BaseCacheEngine, is_package_available


class DiskCacheEngine(BaseCacheEngine[P, R]):
    """
    Disk-based cache engine using diskcache.

    This engine provides persistent caching using SQLite and the filesystem,
    with support for TTL, compression, and secure file permissions.
    """

    @classmethod
    def is_available(cls) -> bool:
        """Check if diskcache is available."""
        return is_package_available("diskcache")

    def __init__(self, config: CacheConfig) -> None:
        """Initialize the disk cache engine."""
        super().__init__(config)

        if not self._cache_path:
            msg = "Cache path is required for disk cache"
            raise ValueError(msg)

        if not self.is_available:
            msg = "diskcache is not available"
            raise ImportError(msg)

        # Initialize diskcache with our settings
        self._disk_cache = Cache(
            directory=str(self._cache_path),
            size_limit=self._config.maxsize or int(1e9),
            disk_min_file_size=0,  # Small values in SQLite
            disk_pickle_protocol=5,  # Latest protocol
            statistics=True,  # Enable hit/miss tracking
            tag_index=True,  # Enable tag-based operations
            eviction_policy="least-recently-used",  # Match our LRU default
            sqlite_cache_size=2048,  # 2MB page cache
            sqlite_mmap_size=1024 * 1024 * 32,  # 32MB mmap
            disk_compression_level=6 if self._config.compress else 0,
        )

        # Set secure permissions if requested
        if self._config.secure:
            self._cache_path.chmod(0o700)
            for path in self._cache_path.glob("**/*"):
                if path.is_file():
                    path.chmod(0o600)

        logger.debug(
            f"Initialized {self.__class__.__name__} at {self._cache_path}"
            f" with maxsize={self._config.maxsize}, ttl={self._config.ttl}"
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
            # Get value and expiry time
            result = self._disk_cache.get(str(key), default=None, retry=True)
            if result is None:
                return None

            value, expiry = result

            # Check TTL if configured
            if expiry is not None:
                if time.time() >= expiry:
                    self._disk_cache.delete(str(key))
                    return None

            return cast(R, value)

        except Exception as e:
            logger.warning(f"Error retrieving from disk cache: {e}")
            return None

    def _set_cached_value(self, key: CacheKey, value: R) -> None:
        """
        Store a value in the cache.

        Args:
            key: The cache key to store under
            value: The value to cache
        """
        try:
            # Calculate expiry time if TTL configured
            expiry = (
                time.time() + self._config.ttl if self._config.ttl is not None else None
            )

            # Store value with expiry
            self._disk_cache.set(
                str(key),
                (value, expiry),
                expire=self._config.ttl,
                retry=True,
                tag=None,
            )

        except Exception as e:
            logger.warning(f"Error storing to disk cache: {e}")

    def clear(self) -> None:
        """Clear all cached values."""
        try:
            self._disk_cache.clear()
            self._hits = 0
            self._misses = 0
            self._size = 0
        except Exception as e:
            logger.warning(f"Error clearing disk cache: {e}")

    @property
    def stats(self) -> dict[str, Any]:
        """Get cache statistics."""
        base_stats = super().stats
        try:
            disk_stats = self._disk_cache.stats(enable=True)
            base_stats.update(
                {
                    "hits": disk_stats.hits,
                    "misses": disk_stats.misses,
                    "size": disk_stats.size,
                    "max_size": disk_stats.max_size,
                }
            )
        except Exception as e:
            logger.warning(f"Error getting disk cache stats: {e}")
        return base_stats

    def __del__(self) -> None:
        """Clean up resources."""
        try:
            self._disk_cache.close()
        except Exception as e:
            logger.warning(f"Error closing disk cache: {e}")

    def cache(self, func: Callable[P, R]) -> Callable[P, R]:
        """Decorate a function with caching.

        Args:
            func: Function to cache.

        Returns:
            Callable: Decorated function with caching.
        """
        if not self._disk_cache:
            msg = "Cache not initialized"
            raise RuntimeError(msg)

        # Import here to avoid loading if not used
        from diskcache import memoize

        return cast(
            Callable[P, R],
            memoize(
                cache=self._disk_cache,
                typed=True,
            )(func),
        )

    def get(self, key: CacheKey) -> R | None:
        """Get a value from the cache.

        Args:
            key: Cache key.

        Returns:
            Optional[R]: Cached value if found, None otherwise.
        """
        if not self._disk_cache:
            msg = "Cache not initialized"
            raise RuntimeError(msg)

        return cast(R | None, self._disk_cache.get(str(key)))

    def set(self, key: CacheKey, value: R) -> None:
        """Set a value in the cache.

        Args:
            key: Cache key.
            value: Value to cache.
        """
        if not self._disk_cache:
            msg = "Cache not initialized"
            raise RuntimeError(msg)

        self._disk_cache.set(str(key), value)
