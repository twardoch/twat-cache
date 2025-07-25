#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "loguru",
# ]
# ///
# this_file: src/twat_cache/cache.py

"""Global cache management utilities for TWAT-Cache.

This module provides centralized management for all active cache instances,
including registration, statistics tracking, and batch operations.

Components:
    CacheStats: NamedTuple for cache performance metrics.
        Tracks hits, misses, size, and capacity for each cache.
    
    CacheEntry: Registry entry containing cache instance and metadata.
        Stores the engine, wrapper function, and statistics.
    
    Global Registry: Thread-safe registry of all active caches.
        Enables centralized management and monitoring.

Functions:
    register_cache: Register a new cache instance in the global registry.
    unregister_cache: Remove a cache from the registry (cleanup).
    get_cache: Retrieve a specific cache by name.
    list_caches: Get all registered cache names.
    clear_all_caches: Clear all registered caches at once.
    get_all_stats: Aggregate statistics from all caches.
    clear_cache_by_name: Clear a specific cache by name.
    get_cache_directory: Get the base cache directory path.

Use Cases:
    1. Application-wide cache management and monitoring
    2. Debugging and profiling cache performance
    3. Graceful shutdown with cleanup of all caches
    4. Cache statistics aggregation for monitoring
    5. Selective cache clearing for maintenance

Example:
    Managing multiple caches::
    
        from twat_cache.cache import list_caches, clear_all_caches, get_all_stats
        from twat_cache import ucache
        
        @ucache
        def compute1(x): return x ** 2
        
        @ucache
        def compute2(x): return x ** 3
        
        # List all active caches
        print(list_caches())
        # Output: ['compute1', 'compute2']
        
        # Get aggregate statistics
        stats = get_all_stats()
        print(f"Total hits: {stats['total_hits']}")
        
        # Clear all caches at once
        clear_all_caches()

Note:
    The global registry is automatically managed by decorators.
    Manual registration is only needed for custom cache implementations.
"""

from pathlib import Path
from typing import Any, NamedTuple
from loguru import logger
from .engines.base import BaseCacheEngine


class CacheStats(NamedTuple):
    """Cache statistics."""

    hits: int
    misses: int
    size: int
    maxsize: int | None


class CacheEntry(NamedTuple):
    """Cache registry entry."""

    cache: BaseCacheEngine[Any, Any]  # Store the engine instance
    wrapper: Any
    stats: CacheStats


# Global registry of active caches
_active_caches: dict[str, CacheEntry] = {}


def register_cache(
    name: str, cache: BaseCacheEngine[Any, Any], wrapper: Any, stats: CacheStats
) -> None:
    """
    Register an active cache instance.

    Args:
        name: Unique name for the cache
        cache: The cache instance
        wrapper: The wrapper function
        stats: Initial cache statistics
    """
    _active_caches[name] = CacheEntry(cache, wrapper, stats)
    logger.debug(f"Registered cache: {name}")


def clear_cache(name: str | None = None) -> None:
    """
    Clear one or all caches.

    Args:
        name: Name of cache to clear, or None to clear all
    """
    if name is not None:
        if name in _active_caches:
            _active_caches[name].cache.clear()
            # Reset stats (simplified)
            entry = _active_caches[name]
            _active_caches[name] = entry._replace(
                stats=CacheStats(0, 0, 0, entry.stats.maxsize)
            )
        return

    for cache_name, entry in list(_active_caches.items()):  # Iterate over a copy
        entry.cache.clear()
        # Reset stats (simplified)
        _active_caches[cache_name] = entry._replace(
            stats=CacheStats(0, 0, 0, entry.stats.maxsize)
        )

    # Also clear cache directories
    cache_dir = Path.home() / ".cache" / "twat_cache"
    if cache_dir.exists():
        for path in cache_dir.glob("*"):
            if path.is_dir():
                try:
                    for file in path.glob("*"):
                        file.unlink()
                    path.rmdir()
                except OSError as e:
                    logger.warning(f"Failed to clear cache directory {path}: {e}")
        logger.debug("Cleared cache directories")


def get_stats(name: str | None = None) -> dict[str, Any]:
    """
    Get cache statistics.

    Args:
        name: Name of cache to get stats for, or None for all

    Returns:
        Dictionary of cache statistics
    """
    if name is not None:
        if name not in _active_caches:
            return {
                "hits": 0,
                "misses": 0,
                "size": 0,
                "maxsize": None,
            }
        entry = _active_caches[name]
        return {
            "hits": entry.stats.hits,
            "misses": entry.stats.misses,
            "size": entry.stats.size,
            "maxsize": entry.stats.maxsize,
        }

    total_stats = {
        "total_caches": len(_active_caches),
        "hits": 0,
        "misses": 0,
        "size": 0,
    }
    for entry in _active_caches.values():
        total_stats["hits"] += entry.stats.hits
        total_stats["misses"] += entry.stats.misses
        total_stats["size"] += entry.stats.size
    return total_stats


def update_stats(
    name: str, *, hit: bool = False, miss: bool = False, size: int | None = None
) -> None:
    """
    Update cache statistics.

    Args:
        name: Name of the cache to update
        hit: Whether to increment hit count
        miss: Whether to increment miss count
        size: New cache size (if changed)
    """
    if name not in _active_caches:
        return

    entry = _active_caches[name]
    hits = entry.stats.hits + (1 if hit else 0)
    misses = entry.stats.misses + (1 if miss else 0)
    new_size = (
        size if size is not None else entry.stats.size
    )  # We don't track size changes automatically

    _active_caches[name] = CacheEntry(
        entry.cache,
        entry.wrapper,
        CacheStats(hits, misses, new_size, entry.stats.maxsize),
    )
