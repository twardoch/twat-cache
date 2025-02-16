#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "loguru",
# ]
# ///
# this_file: src/twat_cache/cache.py

"""
Main cache interface.

This module provides a simple interface for managing caches and retrieving
cache statistics. For the main caching decorators, see the decorators module.
"""

from typing import Any

from loguru import logger

from .config import CacheConfig
from .engines.manager import get_engine_manager


def clear_cache(
    folder_name: str | None = None,
    preferred_engine: str | None = None,
) -> None:
    """
    Clear the cache for the given configuration.

    Args:
        folder_name: Optional name of the cache folder to clear
        preferred_engine: Optional name of the cache engine to clear

    Example:
        ```python
        # Clear specific cache
        clear_cache(folder_name="my_cache")

        # Clear all caches
        clear_cache()
        ```
    """
    # Create configuration
    config = CacheConfig(
        folder_name=folder_name,
        preferred_engine=preferred_engine,
    )

    # Get engine manager
    manager = get_engine_manager()

    # Get appropriate engine
    engine = manager.get_engine(config)
    logger.debug(f"Clearing cache for engine: {engine.__class__.__name__}")

    # Clear cache
    engine.clear()


def get_stats(
    folder_name: str | None = None,
    preferred_engine: str | None = None,
) -> dict[str, Any]:
    """
    Get cache statistics for the given configuration.

    Args:
        folder_name: Optional name of the cache folder
        preferred_engine: Optional name of the cache engine

    Returns:
        Dictionary containing cache statistics

    Example:
        ```python
        # Get stats for specific cache
        stats = get_stats(folder_name="my_cache")
        print(f"Cache hits: {stats['hits']}")
        ```
    """
    # Create configuration
    config = CacheConfig(
        folder_name=folder_name,
        preferred_engine=preferred_engine,
    )

    # Get engine manager
    manager = get_engine_manager()

    # Get appropriate engine
    engine = manager.get_engine(config)
    logger.debug(f"Getting stats for engine: {engine.__class__.__name__}")

    # Get stats
    return engine.stats
