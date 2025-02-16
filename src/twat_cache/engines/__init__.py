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

# Import base engine
from twat_cache.engines.base import BaseCacheEngine
from twat_cache.engines.functools import FunctoolsCacheEngine

# Import optional engines if available
if HAS_AIOCACHE:
    from twat_cache.engines.aiocache import AioCacheEngine
if HAS_CACHEBOX:
    from twat_cache.engines.cachebox import CacheBoxEngine
if HAS_CACHETOOLS:
    from twat_cache.engines.cachetools import CacheToolsEngine
if HAS_DISKCACHE:
    from twat_cache.engines.diskcache import DiskCacheEngine
if HAS_JOBLIB:
    from twat_cache.engines.joblib import JoblibEngine
if HAS_KLEPTO:
    from twat_cache.engines.klepto import KleptoEngine

_all_engines = [
    "FunctoolsCacheEngine",
    "AioCacheEngine" if HAS_AIOCACHE else None,
    "CacheBoxEngine" if HAS_CACHEBOX else None,
    "CacheToolsEngine" if HAS_CACHETOOLS else None,
    "DiskCacheEngine" if HAS_DISKCACHE else None,
    "JoblibEngine" if HAS_JOBLIB else None,
    "KleptoEngine" if HAS_KLEPTO else None,
]

__all__: Sequence[str] = [x for x in _all_engines if x is not None]
