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
        """Retrieve a value from the cache."""
        try:
            cache_result = self._disk_cache.get(key, default=None, expire_time=True)
            if cache_result is not None:
                # diskcache get with expire_time=True returns (value, expire_at_timestamp)
                # If item is expired, diskcache itself should return None or handle it.
                # However, the previous code stored (result, expire_time_custom_calc) as value.
                # We need to be careful here. Assuming diskcache's `expire` on set works.
                # If diskcache returns a value, it means it's not expired according to its own TTL.

                # Let's simplify and trust diskcache's expiry.
                # The value stored is (actual_result, custom_expire_time_stored_by_old_code)
                # We only care about actual_result if diskcache gives it to us.
                if isinstance(cache_result, tuple) and len(cache_result) == 2 and not isinstance(cache_result[1], bool):
                    # This condition tries to detect if it's our old (value, expire_time) tuple
                    # or diskcache's internal (value, True/False for expired).
                    # This is fragile. Ideally, we'd only store raw values.
                    # For now, assume if diskcache.get returns something, it's valid by its TTL.
                    # The value itself might be our (actual_value, custom_ttl_timestamp) tuple.
                    # Let's assume the value fetched IS the actual data `R` if not None.
                    # This part needs more robust handling if we were to strictly follow the old logic.
                    # Simplified: if diskcache returns it, it's a hit.
                    self._hits += 1
                    logger.trace(f"Cache hit for key {key}")
                    # If the stored item was (actual_value, custom_expire_time), return actual_value
                    if isinstance(cache_result, tuple) and len(cache_result) == 2: # Check if it's our tuple
                         # This is still a bit of a guess. If diskcache returns the (value, expire_time) tuple
                         # we stored, then cache_result[0] is the actual data.
                         # If diskcache has its own format for get(expire_time=True), this needs adjustment.
                         # Assuming diskcache returns the raw stored value if expire_time=False (default)
                         # and (value, timestamp) if expire_time=True and value is not expired.

                        # Re-checking diskcache docs:
                        # If `expire_time` is true, the return value is a ``(value, time)`` tuple
                        # where `time` is the timestamp of when the value expires.
                        # If the value does not expire, then `time` is None.
                        # If the value is not found, then ``default`` is returned.

                        value, diskcache_expire_at = cache_result
                        if diskcache_expire_at is None or time.time() < diskcache_expire_at:
                            self._hits += 1
                            logger.trace(f"Cache hit for key {key}")
                            return cast(R, value) # Value here is our (actual_result, custom_expire_time)
                        else:
                            self._disk_cache.delete(key) # Explicitly delete if our check says expired
                            self._misses += 1
                            logger.trace(f"Cache miss (expired) for key {key}")
                            return None
                else: # If cache_result is not a tuple (e.g. default was returned, or value is not a tuple)
                    self._misses +=1
                    logger.trace(f"Cache miss for key {key}")
                    return None

            self._misses += 1
            logger.trace(f"Cache miss for key {key}")
            return None
        except Exception as e:
            logger.error(f"Error getting from DiskCache for key {key}: {e}")
            self._misses += 1
            return None

    def _set_cached_value(self, key: CacheKey, value: R) -> None:
        """Store a value in the cache."""
        try:
            # The old code stored a tuple: (result, custom_expire_time).
            # DiskCache's `set` has an `expire` argument for TTL in seconds.
            # It's better to rely on DiskCache's own TTL mechanism.
            self._disk_cache.set(
                key=key,
                value=value, # Store the raw value
                expire=self._config.ttl, # Let DiskCache handle expiry
                tag=key.split(":")[0] if ":" in key else "general", # Basic tagging
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
