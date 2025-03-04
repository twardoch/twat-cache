"""Flexible caching utilities for Python functions with multiple high-performance backends."""

# this_file: src/twat_cache/__init__.py

from twat_cache.cache import clear_cache, get_stats
from twat_cache.decorators import bcache, fcache, mcache, ucache
from twat_cache.utils import get_cache_path
from twat_cache.context import engine_context, CacheContext, get_or_create_engine
from twat_cache.exceptions import (
    TwatCacheError,
    ConfigurationError,
    EngineError,
    EngineNotAvailableError,
    CacheOperationError,
    CacheKeyError,
    CacheValueError,
    SerializationError,
    ResourceError,
    ConcurrencyError,
    PathError,
)

try:
    from twat_cache.__version__ import __version__
except ImportError:
    __version__ = "0.0.0"

__all__ = [
    "__version__",
    "bcache",
    "clear_cache",
    "fcache",
    "get_cache_path",
    "get_stats",
    "mcache",
    "ucache",
    # Context management
    "engine_context",
    "CacheContext",
    "get_or_create_engine",
    # Exceptions
    "TwatCacheError",
    "ConfigurationError",
    "EngineError",
    "EngineNotAvailableError",
    "CacheOperationError",
    "CacheKeyError",
    "CacheValueError",
    "SerializationError",
    "ResourceError",
    "ConcurrencyError",
    "PathError",
]
