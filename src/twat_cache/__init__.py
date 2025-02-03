"""
twat_cache - Flexible caching utilities for Python functions.

This package provides a unified interface for caching function results using various
backends (memory, disk, SQL). It automatically handles cache directory management
and offers a simple decorator interface.
"""

from importlib import metadata

from .__main__ import get_cache_path, ucache

__version__ = metadata.version(__name__)
__all__ = ["__version__", "get_cache_path", "ucache"]
