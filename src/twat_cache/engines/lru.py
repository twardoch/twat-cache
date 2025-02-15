"""LRU cache engine implementation."""
from __future__ import annotations

from functools import lru_cache
from typing import cast

from twat_cache.engines.base import CacheEngine, F


class LRUEngine(CacheEngine):
    """LRU cache engine using Python's built-in functools.lru_cache."""

    def __init__(self, maxsize: int | None = None):
        """Initialize LRU cache engine.

        Args:
            maxsize: Maximum size for LRU cache (None means unlimited)
        """
        self._maxsize = maxsize

    def cache(self, func: F) -> F:
        """Apply LRU caching to the function.

        Args:
            func: Function to be cached

        Returns:
            Cached function wrapper
        """
        return cast(F, lru_cache(maxsize=self._maxsize)(func))

    def clear(self) -> None:
        """Clear is not supported for LRU cache."""

    @property
    def is_available(self) -> bool:
        """LRU cache is always available as it's built into Python."""
        return True

    @property
    def name(self) -> str:
        """Get engine name."""
        return "lru"
