"""Disk-based cache engine using diskcache package."""

from __future__ import annotations

from typing import Any, cast
import json

from twat_cache.engines.base import CacheEngine
from twat_cache.types import F, CacheKey, P, R
from twat_cache.paths import get_cache_path

try:
    from diskcache import Cache

    HAS_DISKCACHE = True
except ImportError:
    HAS_DISKCACHE = False
    Cache = None


class DiskCacheEngine(CacheEngine[P, R]):
    """Cache engine using diskcache package for SQL-based disk caching."""

    def __init__(self, config):
        """Initialize disk cache engine.

        Args:
            config: Cache configuration.
        """
        super().__init__(config)
        folder_name = getattr(self._config, "folder_name", None)
        self._folder_name = folder_name or "diskcache"
        self._cache = (
            Cache(str(get_cache_path(self._folder_name))) if HAS_DISKCACHE else None
        )
        self._hits = 0
        self._misses = 0

    def _get_cached_value(self, key: CacheKey) -> R | None:
        """Retrieve a value from the cache."""
        if not self.is_available:
            return None
        try:
            str_key = json.dumps(key, sort_keys=True, default=str)
            value = self._cache.get(str_key)  # type: ignore
            if value is not None:
                self._hits += 1
                return value
            self._misses += 1
            return None
        except (KeyError, TypeError, ValueError):
            self._misses += 1
            return None

    def _set_cached_value(self, key: CacheKey, value: R) -> None:
        """Store a value in the cache."""
        if not self.is_available:
            return
        try:
            str_key = json.dumps(key, sort_keys=True, default=str)
            self._cache.set(str_key, value)  # type: ignore
        except (TypeError, ValueError):
            pass

    def clear(self) -> None:
        """Clear all cached values."""
        if self._cache is not None:
            self._cache.clear()
            self._hits = 0
            self._misses = 0

    @property
    def is_available(self) -> bool:
        """Check if diskcache is available."""
        return HAS_DISKCACHE and self._cache is not None

    @property
    def stats(self) -> dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            dict: A dictionary containing cache statistics
        """
        return {
            "type": "diskcache",
            "maxsize": getattr(self._config, "maxsize", None),
            "current_size": len(self._cache) if self._cache else 0,  # type: ignore
            "hits": self._hits,
            "misses": self._misses,
            "size": len(self._cache) if self._cache else 0,  # type: ignore
            "backend": self.__class__.__name__,
            "path": str(get_cache_path(self._folder_name)),
        }

    @property
    def name(self) -> str:
        """Get engine name."""
        return "diskcache"

    def cache(self, func: F) -> F:
        """Apply disk caching to the function.

        Args:
            func: Function to be cached

        Returns:
            Cached function wrapper
        """
        if not self.is_available:
            return func
        return cast(F, self._cache.memoize()(func))
