"""Flexible caching utilities for Python functions with multiple high-performance backends."""

# this_file: src/twat_cache/__init__.py

from twat_cache.cache import ucache
from twat_cache.decorators import bcache, fcache, scache
from twat_cache.utils import get_cache_path

try:
    from twat_cache.__version__ import __version__
except ImportError:
    __version__ = "0.0.0"

__all__ = ["__version__", "bcache", "fcache", "get_cache_path", "scache", "ucache"]
