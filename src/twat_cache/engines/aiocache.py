"""Async-capable cache engine using aiocache package."""

from __future__ import annotations

# this_file: src/twat_cache/engines/aiocache.py

from typing import Any, cast
from collections.abc import Callable

from twat_cache.engines.base import BaseCacheEngine
from twat_cache.type_defs import F, P, R, CacheKey


try:
    from aiocache import Cache, caches
    from aiocache.decorators import cached

    HAS_AIOCACHE = True
except ImportError:
    HAS_AIOCACHE = False
    Cache = type("Cache", (), {})
    caches = None

    def cached(*args: Any, **kwargs: Any) -> Callable[[F], F]:
        return lambda f: f


class AioCacheEngine(BaseCacheEngine[P, R]):
    """Cache engine using aiocache for async-capable caching."""

    def __init__(self, config):
        """Initialize aiocache engine.

        Args:
            config: Cache configuration.
        """
        super().__init__(config)  # Call superclass constructor
        if HAS_AIOCACHE:
            caches.set_config(
                {
                    "default": {
                        "cache": "aiocache.SimpleMemoryCache",
                        "serializer": {
                            "class": "aiocache.serializers.PickleSerializer"
                        },
                        "plugins": [],
                        "ttl": 0,  # No expiration
                        "maxsize": self._config.maxsize or 0,  # 0 means unlimited
                    }
                }
            )
            self._cache = Cache()
        else:
            self._cache = None

    def _get_cached_value(self, key: CacheKey) -> R | None:
        """Retrieve a value from the cache."""
        if not self.is_available:
            return None

        async def get_value():
            return await self._cache.get(key)  # type: ignore

        import asyncio

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        return loop.run_until_complete(get_value())

    def _set_cached_value(self, key: CacheKey, value: R) -> None:
        """Store a value in the cache."""
        if not self.is_available:
            return

        async def set_value():
            await self._cache.set(key, value)  # type: ignore

        import asyncio

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        loop.run_until_complete(set_value())

    def clear(self) -> None:
        """Clear all cached values."""
        if self._cache is not None:
            import asyncio

            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            loop.run_until_complete(self._cache.clear())

    @property
    def is_available(self) -> bool:
        """Check if aiocache is available."""
        return HAS_AIOCACHE and self._cache is not None

    @property
    def name(self) -> str:
        """Get engine name."""
        return "aiocache"

    def cache(self, func: Callable[P, R]) -> Callable[P, R]:
        """Apply aiocache caching to the function.

        Args:
            func: Function to be cached

        Returns:
            Cached function wrapper
        """
        if not self.is_available:
            return func

        # Handle both async and sync functions
        if not hasattr(func, "__await__"):
            # For sync functions, wrap in async and sync wrappers
            @cached(
                cache=self._cache,
                key_builder=lambda *args, **kwargs: str(args) + str(kwargs),
            )
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                return func(*args, **kwargs)

            def sync_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                import asyncio

                try:
                    loop = asyncio.get_event_loop()
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                return loop.run_until_complete(async_wrapper(*args, **kwargs))

            return cast(Callable[P, R], sync_wrapper)
        else:
            # For async functions, use aiocache directly
            return cast(Callable[P, R], cached(cache=self._cache)(func))
