#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "loguru",
#   "cachetools",
#   "types-cachetools",
# ]
# ///
# this_file: src/twat_cache/engines/cachetools.py

"""Flexible in-memory cache engine using cachetools package."""

from __future__ import annotations

from typing import Any, cast
from collections.abc import Callable

from twat_cache.config import CacheConfig
from twat_cache.engines.base import BaseCacheEngine, is_package_available
from twat_cache.type_defs import CacheKey, P, R


class CacheToolsEngine(BaseCacheEngine[P, R]):
    """In-memory cache engine backed by the ``cachetools`` library.

    Supports LRU, LFU, and round-robin eviction policies, plus optional
    TTL expiry via ``cachetools.TTLCache``.  Falls back to ``LRUCache``
    for any unrecognised policy.
    """

    @classmethod
    def is_available(cls) -> bool:
        """Return ``True`` if cachetools is installed."""
        return is_package_available("cachetools")

    def __init__(self, config: CacheConfig) -> None:
        """Initialise the cachetools engine.

        Args:
            config: Cache configuration settings.
        """
        super().__init__(config)
        self._config = config
        self._cache: Any = None

        if not CacheToolsEngine.is_available():
            msg = "cachetools is not available"
            raise ImportError(msg)

        # Lazy-import so the module can be loaded without cachetools
        from cachetools import LRUCache, LFUCache, TTLCache, RRCache  # noqa: PLC0415

        cache_args: dict[str, Any] = {"maxsize": config.maxsize or 100}

        if config.ttl:
            # TTLCache accepts (maxsize, ttl) — covers both LRU and non-LRU TTL cases
            cache_args["ttl"] = config.ttl
            self._cache = TTLCache(**cache_args)
        else:
            cache_types = {
                "lru": LRUCache,
                "lfu": LFUCache,
                "rr": RRCache,
            }
            cache_type = cache_types.get(config.policy or "lru", LRUCache)
            self._cache = cache_type(**cache_args)

    def cache(self, func: Callable[P, R]) -> Callable[P, R]:
        """Wrap *func* with a cachetools-backed LRU decorator.

        Args:
            func: Function to cache.

        Returns:
            Callable: Decorated function with caching.
        """
        if self._cache is None:
            msg = "Cache not initialized"
            raise RuntimeError(msg)

        from cachetools import cached  # noqa: PLC0415

        return cast(Callable[P, R], cached(cache=self._cache)(func))

    def _get_cached_value(self, key: CacheKey) -> R | None:
        """Return the cached value for *key*, or ``None`` on a miss.

        Args:
            key: Cache key.
        """
        if self._cache is None:
            self._misses += 1
            return None

        value = self._cache.get(str(key))
        if value is not None:
            self._hits += 1
        else:
            self._misses += 1
        return cast(R | None, value)

    def _set_cached_value(self, key: CacheKey, value: R) -> None:
        """Store *value* under *key*.

        Args:
            key: Cache key.
            value: Value to cache.
        """
        if self._cache is None:
            msg = "Cache not initialized"
            raise RuntimeError(msg)

        self._cache[str(key)] = value
        self._size = len(self._cache)

    def clear(self) -> None:
        """Evict all cached entries."""
        if self._cache is None:
            msg = "Cache not initialized"
            raise RuntimeError(msg)

        self._cache.clear()

    @property
    def stats(self) -> dict[str, Any]:
        """Return a snapshot of cache statistics.

        Returns:
            dict[str, Any]: Dictionary of cache statistics.
        """
        if self._cache is None:
            msg = "Cache not initialized"
            raise RuntimeError(msg)

        return {
            "hits": getattr(self._cache, "hits", 0),
            "misses": getattr(self._cache, "misses", 0),
            "size": len(self._cache),
            "maxsize": self._cache.maxsize,
            "policy": self._config.policy,
            "ttl": getattr(self._cache, "ttl", None),
        }
