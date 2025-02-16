"""Flexible cache engine using cachetools package."""

from __future__ import annotations

from typing import Any, cast
from collections.abc import MutableMapping

from twat_cache.engines.base import BaseCacheEngine
from twat_cache.types import F, CacheKey, P, R

try:
    from cachetools import LRUCache, cached

    HAS_CACHETOOLS = True
except ImportError:
    HAS_CACHETOOLS = False
    LRUCache = type("LRUCache", (), {})  # type: ignore

    def cached(*args, **kwargs):  # type: ignore
        return lambda f: f


class CacheToolsEngine(BaseCacheEngine[P, R]):
    """Cache engine using cachetools for flexible in-memory caching."""

    def __init__(self, config):
        """Initialize cachetools engine.

        Args:
            config: Cache configuration.
        """
        super().__init__(config)
        maxsize = getattr(self._config, "maxsize", None)
        self._maxsize = maxsize or float("inf")  # inf means unlimited in cachetools
        self._cache: MutableMapping[Any, Any] | None = (
            LRUCache(maxsize=self._maxsize) if HAS_CACHETOOLS else None
        )

    def _get_cached_value(self, key: CacheKey) -> R | None:
        """Retrieve a value from the cache."""
        if not self.is_available:
            return None
        try:
            return self._cache[key]  # type: ignore
        except KeyError:
            return None

    def _set_cached_value(self, key: CacheKey, value: R) -> None:
        """Store a value in the cache."""
        if not self.is_available:
            return
        # cachetools handles maxsize internally
        self._cache[key] = value  # type: ignore

    def clear(self) -> None:
        """Clear all cached values."""
        if self._cache is not None:
            self._cache.clear()

    @property
    def is_available(self) -> bool:
        """Check if cachetools is available."""
        return HAS_CACHETOOLS and self._cache is not None

    @property
    def name(self) -> str:
        """Get engine name."""
        return "cachetools"

    def cache(self, func: F) -> F:
        """Apply cachetools caching to the function.

        Args:
            func: Function to be cached

        Returns:
            Cached function wrapper
        """
        if not self.is_available:
            return func
        return cast(F, cached(cache=self._cache)(func))
