"""Rust-based cache engine using cachebox package."""

from __future__ import annotations

from typing import cast

from twat_cache.engines.base import BaseCacheEngine
from twat_cache.types import F, CacheKey, P, R

try:
    from cachebox import Cache

    HAS_CACHEBOX = True
except ImportError:
    HAS_CACHEBOX = False
    Cache = None


class CacheBoxEngine(BaseCacheEngine[P, R]):
    """Cache engine using cachebox for high-performance Rust-based caching."""

    def __init__(self, config):
        """Initialize cachebox engine.

        Args:
            config: Cache configuration.
        """
        super().__init__(config)
        maxsize = getattr(self._config, "maxsize", None)
        self._maxsize = maxsize or 0  # 0 means unlimited in cachebox
        self._cache = Cache(maxsize=self._maxsize) if HAS_CACHEBOX else None

    def _get_cached_value(self, key: CacheKey) -> R | None:
        """Retrieve a value from the cache."""
        if not self.is_available:
            return None
        return cast(R, self._cache.get(key))

    def _set_cached_value(self, key: CacheKey, value: R) -> None:
        """Store a value in the cache."""
        if not self.is_available:
            return
        # cachebox handles maxsize internally, so no need for extra logic here
        self._cache[key] = value

    def clear(self) -> None:
        """Clear all cached values."""
        if self._cache is not None:
            self._cache.clear()

    @property
    def is_available(self) -> bool:
        """Check if cachebox is available."""
        return HAS_CACHEBOX and self._cache is not None

    @property
    def name(self) -> str:
        """Get engine name."""
        return "cachebox"

    def cache(self, func: F) -> F:
        """Apply cachebox caching to the function.

        Args:
            func: Function to be cached

        Returns:
            Cached function wrapper
        """
        if not self.is_available:
            return func
        return cast(F, self._cache.memoize(func))
