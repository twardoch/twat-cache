"""Disk-based cache engine using diskcache package."""

from __future__ import annotations

from typing import Any, cast
import json

from twat_cache.engines.base import BaseCacheEngine
from twat_cache.types import F, CacheKey, P, R, CacheConfig
from twat_cache.paths import get_cache_path
from loguru import logger

try:
    from diskcache import Cache

    HAS_DISKCACHE = True
except ImportError:
    HAS_DISKCACHE = False
    logger.debug("diskcache not available")
    Cache = None


class DiskCacheEngine(BaseCacheEngine[P, R]):
    """Cache engine using diskcache package for SQL-based disk caching."""

    def __init__(self, config: CacheConfig):
        """Initialize disk cache engine.

        Args:
            config: Cache configuration.
        """
        super().__init__(config)
        self._folder_name = config.folder_name or "diskcache"
        self._cache_dir = get_cache_path(self._folder_name)
        self._cache = Cache(str(self._cache_dir)) if HAS_DISKCACHE else None
        self._hits = 0
        self._misses = 0

    def get(self, key: str) -> R | None:
        if not self._cache: return None
        return self._cache.get(key)

    def set(self, key: str, value: R) -> None:
        if not self._cache: return
        self._cache.set(key, value)

    def clear(self) -> None:
        if not self._cache: return
        self._cache.clear()
        self._hits = 0
        self._misses = 0

    @classmethod
    def is_available(cls) -> bool:
        """Check if diskcache is available."""
        return HAS_DISKCACHE

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
            "path": str(self._cache_dir),
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
