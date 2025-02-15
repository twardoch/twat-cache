"""
twat_cache - Flexible caching utilities for Python functions.

This package provides a unified interface for caching function results using various
backends (memory, disk, SQL). It automatically handles cache directory management
and offers a simple decorator interface.
"""

from collections.abc import Callable
from importlib import metadata
from pathlib import Path
from typing import Optional, TypeVar

__version__ = metadata.version(__name__)

T = TypeVar("T")

from twat_cache.cache import get_cache_path, ucache

__all__ = ["__version__", "get_cache_path", "ucache"]
