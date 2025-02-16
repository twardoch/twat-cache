#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "loguru",
#   "klepto",
# ]
# ///
# this_file: src/twat_cache/engines/klepto.py

"""Flexible cache engine using klepto."""

import time
from typing import Any, cast
import importlib.util
from collections.abc import Callable

from klepto import lru_cache, lfu_cache, rr_cache
from klepto.archives import (
    dir_archive,
    sqltable_archive,
    file_archive,
    sql_archive,
)
from loguru import logger

from twat_cache.config import CacheConfig
from twat_cache.type_defs import CacheKey, P, R
from .base import BaseCacheEngine, is_package_available


class KleptoEngine(BaseCacheEngine[P, R]):
    """
    Flexible cache engine using klepto.

    This engine provides advanced caching with support for:
    - Multiple eviction policies (LRU, LFU, RR)
    - Multiple backends (memory, file, directory, SQL)
    - TTL-based expiration (via our wrapper)
    - Maxsize limitation
    """

    def __init__(self, config: CacheConfig) -> None:
        """Initialize the klepto cache engine."""
        super().__init__(config)

        if not self.is_available:
            msg = "klepto is not available"
            raise ImportError(msg)

        # Import here to avoid loading if not used
        from klepto import keyed_cache

        # Create cache based on policy
        maxsize = config.maxsize or float("inf")
        if config.policy == "lru":
            self._cache = lru_cache(maxsize=maxsize)
        elif config.policy == "lfu":
            self._cache = lfu_cache(maxsize=maxsize)
        elif config.policy == "rr":
            self._cache = rr_cache(maxsize=maxsize)
        else:
            # Default to LRU
            self._cache = lru_cache(maxsize=maxsize)

        # Create archive if folder specified
        if self._cache_path:
            if config.use_sql:
                # Use SQL archive
                self._archive = sql_archive(
                    str(self._cache_path / "cache.db"),
                    maxsize=maxsize,
                    timeout=config.ttl,
                )
            else:
                # Use directory archive
                self._archive = dir_archive(
                    dirname=str(self._cache_path),
                    maxsize=maxsize,
                    timeout=config.ttl,
                )

            # Set secure permissions if requested
            if config.secure:
                self._cache_path.chmod(0o700)
                for path in self._cache_path.glob("**/*"):
                    if path.is_file():
                        path.chmod(0o600)

            # Load existing cache
            self._archive.load()
            self._cache.update(self._archive)

        else:
            self._archive = None

        # Initialize TTL tracking
        self._expiry: dict[CacheKey, float] = {}

        logger.debug(
            f"Initialized {self.__class__.__name__} with "
            f"maxsize={maxsize}, policy={config.policy}"
        )

    def _get_cached_value(self, key: CacheKey) -> R | None:
        """
        Retrieve a value from the cache.

        Args:
            key: The cache key to look up

        Returns:
            The cached value if found and not expired, None otherwise
        """
        try:
            # Check TTL if configured
            if key in self._expiry:
                if time.time() >= self._expiry[key]:
                    del self._cache[key]
                    if self._archive:
                        del self._archive[key]
                        self._archive.sync()
                    del self._expiry[key]
                    return None

            # Try to get from cache
            if key not in self._cache:
                return None

            return cast(R, self._cache[key])

        except Exception as e:
            logger.warning(f"Error retrieving from klepto cache: {e}")
            return None

    def _set_cached_value(self, key: CacheKey, value: R) -> None:
        """
        Store a value in the cache.

        Args:
            key: The cache key to store under
            value: The value to cache
        """
        try:
            # Store in cache
            self._cache[key] = value
            if self._archive:
                self._archive[key] = value
                self._archive.sync()

            # Set TTL if configured
            if self._config.ttl is not None:
                self._expiry[key] = time.time() + self._config.ttl

            # Update size tracking
            self._size = len(self._cache)

        except Exception as e:
            logger.warning(f"Error storing to klepto cache: {e}")

    def clear(self) -> None:
        """Clear all cached values."""
        try:
            self._cache.clear()
            if self._archive:
                self._archive.clear()
                self._archive.sync()
            self._expiry.clear()
            self._hits = 0
            self._misses = 0
            self._size = 0
        except Exception as e:
            logger.warning(f"Error clearing klepto cache: {e}")

    @property
    def stats(self) -> dict[str, Any]:
        """Get cache statistics."""
        base_stats = super().stats
        try:
            base_stats.update(
                {
                    "currsize": len(self._cache),
                    "maxsize": self._cache.maxsize,  # type: ignore
                    "policy": self._config.policy,
                    "archive_type": (
                        type(self._archive).__name__ if self._archive else None
                    ),
                }
            )
        except Exception as e:
            logger.warning(f"Error getting klepto cache stats: {e}")
        return base_stats

    def __del__(self) -> None:
        """Clean up resources."""
        try:
            if self._archive:
                self._archive.sync()
                self._archive.close()
        except Exception as e:
            logger.warning(f"Error closing klepto cache: {e}")

    @property
    def is_available(self) -> bool:
        """Check if this cache engine is available for use."""
        return is_package_available("klepto")

    def cache(self, func: Callable[P, R]) -> Callable[P, R]:
        """Decorate a function with caching.

        Args:
            func: Function to cache.

        Returns:
            Callable: Decorated function with caching.
        """
        if not self._cache:
            msg = "Cache not initialized"
            raise RuntimeError(msg)

        return cast(
            Callable[P, R],
            keyed_cache(
                cache=self._cache,
                typed=True,
            )(func),
        )

    def get(self, key: CacheKey) -> R | None:
        """Get a value from the cache.

        Args:
            key: Cache key.

        Returns:
            Optional[R]: Cached value if found, None otherwise.
        """
        if not self._cache:
            msg = "Cache not initialized"
            raise RuntimeError(msg)

        return cast(R | None, self._cache.get(str(key)))

    def set(self, key: CacheKey, value: R) -> None:
        """Set a value in the cache.

        Args:
            key: Cache key.
            value: Value to cache.
        """
        if not self._cache:
            msg = "Cache not initialized"
            raise RuntimeError(msg)

        self._cache[str(key)] = value
        self._cache.dump()

    def clear(self) -> None:
        """Clear all cached values."""
        if not self._cache:
            msg = "Cache not initialized"
            raise RuntimeError(msg)

        self._cache.clear()
        self._cache.dump()

    @property
    def stats(self) -> dict[str, Any]:
        """Get cache statistics.

        Returns:
            dict[str, Any]: Dictionary of cache statistics.
        """
        if not self._cache:
            msg = "Cache not initialized"
            raise RuntimeError(msg)

        return {
            "hits": getattr(self._cache, "hits", 0),
            "misses": getattr(self._cache, "misses", 0),
            "size": len(self._cache),
            "maxsize": self._config.maxsize,
            "policy": self._config.policy,
            "ttl": self._config.ttl,
        }
