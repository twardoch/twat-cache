"""Scientific computing cache engine using klepto package."""

from __future__ import annotations

from typing import Any, cast

from twat_cache.engines.base import BaseCacheEngine
from twat_cache.types import F, CacheKey, P, R
from twat_cache.paths import get_cache_path

try:
    from klepto.archives import dir_archive
    from klepto.keymaps import keymap
    from klepto.keymaps import picklemap

    HAS_KLEPTO = True
except ImportError:
    HAS_KLEPTO = False
    dir_archive = type("dir_archive", (), {})  # type: ignore
    keymap = picklemap = lambda *args, **kwargs: lambda f: f  # type: ignore


class KleptoEngine(BaseCacheEngine[P, R]):
    """Cache engine using klepto for scientific computing caching."""

    def __init__(self, config):
        """Initialize klepto engine.

        Args:
            config: Cache configuration.
        """
        super().__init__(config)
        folder_name = getattr(self._config, "folder_name", None)
        self._folder_name = folder_name or "klepto"
        if HAS_KLEPTO:
            cache_dir = get_cache_path(self._folder_name)
            self._cache = dir_archive(
                str(cache_dir),
                cached=True,  # Cache in memory and persist to disk
                serialized=True,  # Use serialization for objects
                keymap=keymap(typed=False, flat=True),  # Simple key mapping
                protocol=5,  # Use latest pickle protocol
            )
            # Initialize the archive
            self._cache.load()
        else:
            self._cache = None

    def _get_cached_value(self, key: CacheKey) -> R | None:
        """Retrieve a value from the cache."""
        if not self.is_available:
            return None

        try:
            return self._cache[key]
        except KeyError:
            return None

    def _set_cached_value(self, key: CacheKey, value: R) -> None:
        """Store a value in the cache."""
        if not self.is_available:
            return

        self._cache[key] = value
        self._cache.dump()  # Persist to disk

    def clear(self) -> None:
        """Clear all cached values."""
        if self._cache is not None:
            self._cache.clear()
            self._cache.dump()

    @property
    def is_available(self) -> bool:
        """Check if klepto is available."""
        return HAS_KLEPTO and self._cache is not None

    @property
    def name(self) -> str:
        """Get engine name."""
        return "klepto"

    def cache(self, func: F) -> F:
        """Apply klepto caching to the function.

        Args:
            func: Function to be cached

        Returns:
            Cached function wrapper
        """
        if not self.is_available:
            return func

        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = (args, tuple(sorted(kwargs.items())))
            if key in self._cache:
                return self._cache[key]
            result = func(*args, **kwargs)
            self._cache[key] = result
            self._cache.dump()  # Persist to disk
            return result

        return cast(F, wrapper)
