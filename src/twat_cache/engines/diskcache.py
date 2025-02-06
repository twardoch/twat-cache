"""Disk-based cache engine using diskcache package."""

from typing import cast

from twat_cache.paths import get_cache_path
from .base import CacheEngine, F

try:
    from diskcache import Cache

    HAS_DISKCACHE = True
except ImportError:
    HAS_DISKCACHE = False
    Cache = None


class DiskCacheEngine(CacheEngine):
    """Cache engine using diskcache package for SQL-based disk caching."""

    def __init__(self, folder_name: str | None = None):
        """Initialize disk cache engine.

        Args:
            folder_name: Optional name for the cache folder
        """
        self._folder_name = folder_name or "diskcache"
        self._cache = (
            Cache(get_cache_path(self._folder_name)) if HAS_DISKCACHE else None
        )

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
