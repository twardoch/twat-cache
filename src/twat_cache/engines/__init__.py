#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "loguru",
# ]
# ///
# this_file: src/twat_cache/engines/__init__.py

"""
Cache engine implementations.

This package provides various cache engine implementations for different
backends and use cases.
"""

from typing import Dict, List, Type, Any, cast

from .base import BaseCacheEngine, is_package_available
from .manager import get_engine_manager

# Optional imports are handled by CacheEngineManager during its registration phase.
# Individual engine classes are not typically directly imported from this __init__.
# The manager will attempt to import them.

# Export key components
__all__ = [
    "BaseCacheEngine", # Abstract base class for engines
    "get_engine_manager", # Access to the singleton engine manager
    "is_package_available", # Utility function
    # Individual engine classes like FunctoolsCacheEngine, DiskCacheEngine, etc.,
    # are not exported here by default. They are registered with the manager.
]
