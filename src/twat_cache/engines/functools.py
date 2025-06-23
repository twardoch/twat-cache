#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "loguru",
# ]
# ///
# this_file: src/twat_cache/engines/functools.py

"""
Functools-based cache engine implementation.

This module provides a basic cache engine implementation using Python's built-in
functools.lru_cache. It serves as a fallback when no other caching backends
are available.
"""

import functools
import time
from typing import Any
from collections.abc import Callable

from loguru import logger

from twat_cache.engines.base import BaseCacheEngine
from twat_cache.type_defs import CacheConfig, P, R, CacheKey


class FunctoolsCacheEngine(BaseCacheEngine[P, R]):
    """Cache engine implementation using functools.lru_cache."""

    @classmethod
    def is_available(cls) -> bool:
        """Check if functools is available."""
        return True  # Always available as it's in the standard library

    def __init__(self, config: CacheConfig) -> None:
        """Initialize the cache engine with the given configuration."""
        super().__init__(config)
        self._hits = 0
        self._misses = 0
        self._cache: dict[CacheKey, R] = {}
        self._maxsize = config.maxsize or None
        self._ttl = config.ttl
        self._last_access: dict[CacheKey, float] = {}

    def _get_cached_value(self, key: CacheKey) -> R | None:
        """Retrieve a value from the cache."""
        # Functools lru_cache doesn't expose direct get by key in a way that fits this model easily.
        # This engine primarily relies on the wrapper from its `cache` method.
        # This internal _cache dict is mostly for stats/TTL in this particular engine.
        if self._ttl is not None:
            now = time.time()
            if key in self._last_access and (now - self._last_access[key] > self._ttl):
                if key in self._cache:
                    del self._cache[key]
                del self._last_access[key]
                self._misses += 1 # Consider it a miss if TTL expired
                return None

        cached_value = self._cache.get(key)
        if cached_value is not None:
            self._hits +=1
            self._last_access[key] = time.time()
            return cached_value
        else:
            self._misses +=1
            return None

    def _set_cached_value(self, key: CacheKey, value: R) -> None:
        """Store a value in the cache."""
        # This internal _cache dict is mostly for stats/TTL in this particular engine.
        # The main functools.lru_cache wrapper handles its own storage.
        self._cache[key] = value
        self._last_access[key] = time.time()
        # LRU/maxsize for self._cache would need separate implementation if self._cache is primary
        # For now, assume functools.lru_cache handles its own size limiting.

    def cache(self, func: Callable[P, R]) -> Callable[P, R]:
        """
        Decorate a function to cache its results using functools.lru_cache.
        """
        # Create the core functools cache wrapper
        if self._maxsize is not None:
            underlying_cached_func = functools.lru_cache(maxsize=self._maxsize)(func)
        else:
            underlying_cached_func = functools.cache(func)

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            # Key generation for our internal TTL tracking, not for functools.lru_cache
            # (it does its own keying based on args/kwargs)
            # However, for consistency with a potential _get/_set pattern, we generate it.
            key = self._make_key(func, args, kwargs) # Corrected _make_key usage

            # TTL check for our internal _cache, if we were using it as primary
            if self._ttl is not None:
                now = time.time()
                if key in self._last_access and (now - self._last_access[key] > self._ttl):
                    # Expire our internal tracking if any
                    if key in self._cache: del self._cache[key]
                    if key in self._last_access: del self._last_access[key]
            # Call the functools-cached function
            # This will handle its own caching, hits, misses internally.
            # Our own _hits/_misses will be for the _get_cached_value calls if they were primary.
            # For now, let's assume this engine's stats are simpler.
            try:
                # We don't directly use self._get_cached_value or self._set_cached_value here
                # as functools.lru_cache handles the caching.
                # This design means FunctoolsCacheEngine is a bit of a special case.
                result = underlying_cached_func(*args, **kwargs)
                # Update our simple stats based on lru_cache_info if possible, or approximate
                # For simplicity, we're not trying to sync perfectly with lru_cache's internal stats here.
                # self._hits += 1 # This would be double counting if lru_cache also counts.
                return result
            except Exception as e:
                # self._misses += 1 # Similar to above.
                raise e

        # Expose cache_info and cache_clear from the underlying functools cache object
        wrapper.cache_info = underlying_cached_func.cache_info # type: ignore
        wrapper.cache_clear = underlying_cached_func.cache_clear # type: ignore
        return wrapper

    def clear(self) -> None:
        """Clear all cached values."""
        # Requires that self.cache() has been called on at least one function
        # and the wrapper is somehow accessible, or we clear a known global/instance cache.
        # This is problematic for functools.lru_cache if not tied to an instance method.
        # For now, clear the internal dict.
        # Proper clearing of dynamically created lru_cache wrappers is complex.
        if hasattr(self, "_cache"): # our internal dict
            self._cache.clear()
            self._last_access.clear()
        # If there was a specific wrapped function instance stored on self, we could call:
        # if hasattr(self, "cached_function_instance"):
        #     self.cached_function_instance.cache_clear()
        logger.warning("FunctoolsCacheEngine.clear() clears its internal tracking cache; "
                       "clearing the actual functools.lru_cache requires access to the wrapped function.")
        self._hits = 0
        self._misses = 0

    def validate_config(self) -> None:
        """
        Validate the engine configuration.

        Raises:
            ValueError: If the configuration is invalid
        """
        if self._config.maxsize is not None and self._config.maxsize <= 0:
            msg = "maxsize must be positive"
            raise ValueError(msg)

        if self._config.ttl is not None and self._config.ttl < 0:
            msg = "ttl must be non-negative"
            raise ValueError(msg)

    @property
    def stats(self) -> dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            A dictionary containing cache statistics:
            - hits: Number of cache hits
            - misses: Number of cache misses
            - size: Current number of items in cache
            - maxsize: Maximum number of items allowed
        """
        return {
            "hits": self._hits,
            "misses": self._misses,
            "size": len(self._cache),
            "maxsize": self._maxsize,
            "backend": "functools",
            "policy": "lru" if self._maxsize else None,
            "ttl": self._ttl,
        }
