"""Flexible caching utilities for Python functions with multiple high-performance backends."""

# this_file: src/twat_cache/__init__.py

from twat_cache.cache import clear_cache, get_stats
from twat_cache.decorators import ucache, acache # Keep ucache and acache
from twat_cache.utils import get_cache_path
from twat_cache.context import engine_context, CacheContext, get_or_create_engine # get_or_create_engine might be internal later
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

# Version management - will be handled by build system eventually
try:
    from twat_cache.__version__ import __version__
except ImportError:
    # Fallback version if not installed or __version__.py not generated
    __version__ = "0.1.0.dev0"


__all__ = [
    # Main Decorators
    "ucache",
    "acache",
    # Cache Management
    "clear_cache",
    "get_stats",
    # Contextual Tools
    "CacheContext",
    "engine_context",
    "get_cache_path", # Utility
    "get_or_create_engine", # May become internal
    # Exceptions (alphabetical)
    "CacheKeyError",
    "CacheOperationError",
    "CacheValueError",
    "ConcurrencyError",
    "ConfigurationError",
    "EngineError",
    "EngineNotAvailableError",
    "PathError",
    "ResourceError",
    "SerializationError",
    "TwatCacheError", # Base exception
    # Version
    "__version__",
]
