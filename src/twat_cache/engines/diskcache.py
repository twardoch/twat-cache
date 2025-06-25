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
from functools import wraps
from typing import Any, cast
from collections.abc import Callable

# Skipping analyzing "diskcache": module is installed, but missing library stubs or py.typed marker
from diskcache import Cache  # type: ignore
from loguru import logger

from twat_cache.config import CacheConfig
from twat_cache.exceptions import (
    EngineNotAvailableError,
    CacheOperationError,
    ResourceError,
)
from twat_cache.type_defs import P, R
from .base import BaseCacheEngine
from .common import ensure_dir_exists


class DiskCacheEngine(BaseCacheEngine[P, R]):
    """
    Disk-based cache engine using diskcache.

    This engine provides persistent caching using SQLite and the filesystem,
    with support for TTL, compression, and secure file permissions.
    """

    @classmethod
    def is_available(cls) -> bool:
        """Check if diskcache is available."""
        try:
            import diskcache

            return True
        except ImportError:
            return False

    def __init__(self, config: CacheConfig) -> None:
        """Initialize the disk cache engine."""
        super().__init__(config)

        if not self._cache_path:
            logger.error("Cache path is required for disk cache")
            msg = "diskcache"
            raise EngineNotAvailableError(
                msg, "Cache path is required but not provided"
            )

        if not self.is_available():
            logger.error("diskcache is not available")
            msg = "diskcache"
            raise EngineNotAvailableError(
                msg,
                "Package is not installed. Install with 'pip install diskcache'",
            )

        try:
            # Ensure cache directory exists with proper permissions
            ensure_dir_exists(
                self._cache_path, mode=0o700 if self._config.secure else 0o755
            )

            # Initialize DiskCache with the configuration
            self._disk_cache = Cache(
                directory=str(self._cache_path),
                size_limit=self._config.maxsize,
                disk_min_file_size=0,  # Cache everything to disk
                statistics=True,
                tag_index=True,
                disk_pickle_protocol=4,
            )

            logger.debug(f"Initialized DiskCache at {self._cache_path}")
        except Exception as e:
            logger.error(f"Failed to initialize DiskCache: {e}")
            msg = f"Failed to initialize DiskCache: {e!s}"
            raise ResourceError(msg) from e

    def cleanup(self) -> None:
        """Clean up resources used by the cache engine."""
        try:
            if hasattr(self, "_disk_cache") and self._disk_cache is not None:
                self._disk_cache.close()
                logger.debug(f"Closed DiskCache at {self._cache_path}")
        except Exception as e:
            logger.error(f"Error closing DiskCache: {e}")
        finally:
            super().cleanup()

    def _get_cached_value(self, key: CacheKey) -> R | None:
        """
        Retrieve a value from the cache.
        Relies on diskcache's internal TTL handling.
        """
        try:
            # Default behavior of diskcache.get: returns None if key not found or expired.
            cached_value = self._disk_cache.get(key, default=None)

            if cached_value is not None:
                self._hits += 1
                logger.trace(f"Cache hit for key {key}")
                return cast(R, cached_value) # Value is directly the stored object
            else:
                self._misses += 1
                logger.trace(f"Cache miss for key {key} (not found or expired by diskcache)")
                return None
        except Exception as e:
            logger.error(f"Error getting from DiskCache for key {key}: {e}", exc_info=True)
            self._misses += 1 # Count as miss on error
            return None

    def _set_cached_value(self, key: CacheKey, value: R) -> None:
        """
        Store a value in the cache.
        Uses diskcache's 'expire' parameter for TTL.
        """
        try:
            self._disk_cache.set(
                key=key,
                value=value,  # Store the raw value
                expire=self._config.ttl,  # Let DiskCache handle expiry in seconds
                tag=key.split(":")[0] if ":" in key else "general",  # Basic tagging
                retry=True,
            )
            # Update cache size stat (safely)
            try:
                self._size = self._disk_cache.volume()
            except Exception:
                # Fallback if volume() not available or other issue
                # This is not ideal as it won't reflect true size.
                pass # Avoid incrementing self._size without better logic
            logger.trace(f"Stored value for key {key}")
        except Exception as e:
            logger.error(f"Error setting to DiskCache for key {key}: {e}")
            raise CacheOperationError(f"Failed to set value for key {key} in DiskCache") from e

    def cache(self, func: Callable[P, R]) -> Callable[P, R]:
        """
        Decorate a function to cache its results using DiskCache.
        """
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            key = self._make_key(func, args, kwargs)
            cached_value = self._get_cached_value(key)

            if cached_value is not None:
                return cached_value

            # Cache miss, compute value
            # self._misses has already been incremented by _get_cached_value if it returned None
            result = func(*args, **kwargs)
            self._set_cached_value(key, result)
            return result
        return wrapper

    def clear(self) -> None:
        """Clear all entries from the cache."""
        try:
            if hasattr(self, "_disk_cache") and self._disk_cache is not None:
                self._disk_cache.clear()
                self._hits = 0
                self._misses = 0
                self._size = 0
                logger.debug(f"Cleared DiskCache at {self._cache_path}")
        except Exception as e:
            logger.error(f"Error clearing DiskCache: {e}")
            msg = f"Failed to clear DiskCache: {e!s}"
            raise CacheOperationError(msg) from e

    @property
    def stats(self) -> dict[str, Any]:
        """Get cache statistics."""
        base_stats = super().stats

        try:
            if hasattr(self, "_disk_cache") and self._disk_cache is not None:
                # Get statistics dictionary safely
                disk_stats_dict = self._disk_cache.stats(enable=True)

                # Safely update stats dictionary
                if isinstance(disk_stats_dict, dict):
                    base_stats["disk_hits"] = disk_stats_dict.get("hits", 0)
                    base_stats["disk_misses"] = disk_stats_dict.get("misses", 0)

                # Get size and volume safely
                try:
                    base_stats["disk_size"] = self._disk_cache.volume()
                except Exception:
                    base_stats["disk_size"] = 0

        except Exception as e:
            logger.error(f"Error getting DiskCache stats: {e}")

        return base_stats
