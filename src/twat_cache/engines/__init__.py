"""Cache engine implementations."""

from __future__ import annotations

import importlib.util
from collections.abc import Sequence

# Check optional backend availability
HAS_AIOCACHE = bool(importlib.util.find_spec("aiocache"))
HAS_CACHEBOX = bool(importlib.util.find_spec("cachebox"))
HAS_CACHETOOLS = bool(importlib.util.find_spec("cachetools"))
HAS_DISKCACHE = bool(importlib.util.find_spec("diskcache"))
HAS_JOBLIB = bool(importlib.util.find_spec("joblib"))
HAS_KLEPTO = bool(importlib.util.find_spec("klepto"))

# Import base engine and always available engines
from twat_cache.engines.base import BaseCacheEngine
from twat_cache.engines.functools import FunctoolsCacheEngine

# Define base exports
__all__ = [
    "BaseCacheEngine",
    "FunctoolsCacheEngine",
    "HAS_AIOCACHE",
    "HAS_CACHEBOX",
    "HAS_CACHETOOLS",
    "HAS_DISKCACHE",
    "HAS_JOBLIB",
    "HAS_KLEPTO",
]

# Import and export optional engines if available
if HAS_AIOCACHE:
    from twat_cache.engines.aiocache import AioCacheEngine

    __all__.append("AioCacheEngine")

if HAS_CACHEBOX:
    from twat_cache.engines.cachebox import CacheBoxEngine

    __all__.append("CacheBoxEngine")

if HAS_CACHETOOLS:
    from twat_cache.engines.cachetools import CacheToolsEngine

    __all__.append("CacheToolsEngine")

if HAS_DISKCACHE:
    from twat_cache.engines.diskcache import DiskCacheEngine

    __all__.append("DiskCacheEngine")

if HAS_JOBLIB:
    from twat_cache.engines.joblib import JoblibEngine

    __all__.append("JoblibEngine")

if HAS_KLEPTO:
    from twat_cache.engines.klepto import KleptoEngine

    __all__.append("KleptoEngine")
