"""Disk-based cache engine using diskcache package."""

from __future__ import annotations

from typing import cast

from twat_cache.engines.base import BaseCacheEngine
from twat_cache.types import F, CacheKey, P, R
from twat_cache.paths import get_cache_path

try:
    from diskcache import Cache

    HAS_DISKCACHE = True
except ImportError:
    HAS_DISKCACHE = False
    Cache = None


class DiskCacheEngine(BaseCacheEngine[P, R]):
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

    def _get_cached_value(self, key: CacheKey) -> R | None:
        """Retrieve a value from the cache."""
        if not self.is_available:
            return None
        try:
            return self._cache.get(key)  # type: ignore
        except KeyError:
            return None

    def _set_cached_value(self, key: CacheKey, value: R) -> None:
        """Store a value in the cache."""
        if not self.is_available:
            return
        self._cache.set(key, value)  # type: ignore

    def clear(self) -> None:
        """Clear all cached values."""
        if self._cache is not None:
            self._cache.clear()

    @property
    def is_available(self) -> bool:
        """Check if diskcache is available."""
        return HAS_DISKCACHE and self._cache is not None

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
