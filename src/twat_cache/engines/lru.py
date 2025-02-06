"""LRU cache engine implementation."""

from functools import lru_cache, wraps
from typing import Any, Callable, Optional, TypeVar, cast

from .base import CacheEngine, F


class LRUEngine(CacheEngine):
    """LRU cache engine using Python's built-in functools.lru_cache."""

    def __init__(self, maxsize: Optional[int] = None):
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
        pass

    @property
    def is_available(self) -> bool:
        """LRU cache is always available as it's built into Python."""
        return True

    @property
    def name(self) -> str:
        """Get engine name."""
        return "lru"
