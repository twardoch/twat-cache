"""Cache engine implementations."""

from typing import Sequence

try:
    from twat_cache.engines.aiocache import AioCacheEngine

    HAS_AIOCACHE = True
except ImportError:
    HAS_AIOCACHE = False

try:
    from twat_cache.engines.cachebox import CacheBoxEngine

    HAS_CACHEBOX = True
except ImportError:
    HAS_CACHEBOX = False

try:
    from twat_cache.engines.cachetools import CacheToolsEngine

    HAS_CACHETOOLS = True
except ImportError:
    HAS_CACHETOOLS = False

try:
    from twat_cache.engines.diskcache import DiskCacheEngine

    HAS_DISKCACHE = True
except ImportError:
    HAS_DISKCACHE = False

try:
    from twat_cache.engines.joblib import JoblibEngine

    HAS_JOBLIB = True
except ImportError:
    HAS_JOBLIB = False

try:
    from twat_cache.engines.klepto import KleptoEngine

    HAS_KLEPTO = True
except ImportError:
    HAS_KLEPTO = False

from twat_cache.engines.functools import FunctoolsCacheEngine

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
