"""Joblib-based cache engine implementation."""

from typing import Optional, cast

from ..paths import get_cache_path
from .base import CacheEngine, F


class DummyMemory:
    """Dummy implementation of joblib.Memory for when joblib is not available."""

    def cache(self, func: F) -> F:
        return func

    def clear(self) -> None:
        pass


try:
    from joblib.memory import Memory as JoblibMemory

    HAS_JOBLIB = True
except ImportError:
    JoblibMemory = DummyMemory
    HAS_JOBLIB = False


class JoblibEngine(CacheEngine):
    """Cache engine using joblib for disk caching of numpy arrays and large objects."""

    def __init__(self, folder_name: Optional[str] = None):
        """Initialize joblib cache engine.

        Args:
            folder_name: Optional name for the cache folder
        """
        self._folder_name = folder_name or "joblib"
        self._memory = (
            JoblibMemory(str(get_cache_path(self._folder_name)), verbose=0)
            if HAS_JOBLIB
            else DummyMemory()
        )

    def cache(self, func: F) -> F:
        """Apply joblib caching to the function.

        Args:
            func: Function to be cached

        Returns:
            Cached function wrapper
        """
        return cast(F, self._memory.cache(func))

    def clear(self) -> None:
        """Clear all cached values."""
        self._memory.clear()

    @property
    def is_available(self) -> bool:
        """Check if joblib is available."""
        return HAS_JOBLIB

    @property
    def name(self) -> str:
        """Get engine name."""
        return "joblib"
