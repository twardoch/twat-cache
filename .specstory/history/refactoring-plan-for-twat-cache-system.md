## SpecStory

## Refactoring Plan for Twat Cache System (16/02/2025, 14:34:36)

_**User**_

F@TODO.md @README.md @VARIA.md @twat_cache O.md read Core goals and then execute TASK speced there. 

---

_**Assistant**_

Okay, I've reviewed the `README.md`, `VARIA.md`, and the current codebase. I've also considered the core goals and implementation tasks outlined in `TODO.md`. Here's a detailed plan, including code structures and pseudocode, to move forward with `twat_cache`.

Wait, but... before diving into the plan, let's critically assess the current state. The existing code has a *lot* of separate engine files, many of which duplicate a significant amount of logic. The `EngineManager` tries to handle the complexity, but it's become a bit unwieldy. The decorators in `decorators.py` also have redundant code. The core idea of fallback is good, but the implementation is overly complex. We need to drastically simplify.

Here's the revised plan, focusing on simplification and leveraging existing libraries more effectively:

**DETAILED PLAN**

1.  **Consolidate Decorators:** Instead of four separate decorators (`mcache`, `bcache`, `fcache`, `ucache`), we'll have *one* primary decorator: `twat_cache`. This decorator will handle backend selection and fallback logic internally. This significantly reduces code duplication.

2.  **Simplify Engine Management:** Instead of the complex `EngineManager`, we'll use a simple prioritized list of backend types and a factory function to instantiate them. We'll keep the ability to specify a `preferred_engine`, but the fallback logic will be much simpler.

3.  **Leverage `functools.lru_cache` as the Base:** We'll *always* use `functools.lru_cache` as the innermost wrapper. This provides a consistent interface and basic caching functionality even if no optional backends are installed. Other backends will *wrap* the `lru_cache` instance, adding their specific features (disk persistence, serialization, etc.).

4.  **Simplified Configuration:** We'll use a single `CacheConfig` dataclass (which already exists, but we'll refine it) to hold configuration options. We'll remove the complex config system and rely on simple keyword arguments to the decorator.

5.  **Key Generation:** We'll improve the `make_key` function to handle a wider variety of input types more robustly, including dataclasses and Pydantic models. We'll use `json.dumps` with `sort_keys=True` and a custom encoder to handle unhashable types.

6.  **Cache Statistics:** We'll maintain a simple mechanism for tracking cache hits, misses, and size, but we'll simplify the `_active_caches` registry.

7. **Serialization:** We will use `json` for serialization, and allow users to specify a custom serializer if needed.

**CODE STRUCTURES (and Pseudocode)**

*   **`twat_cache/__init__.py`:**  No major changes, just export the main `twat_cache` decorator and `get_cache_path`.

*   **`twat_cache/cache.py`:**
    *   `clear_cache`: Simplified to clear all caches or a specific one by name.
    *   `get_stats`: Simplified to return basic stats.
    *   `_active_caches`:  We'll keep this, but it will store less information (mainly just the wrapper function and basic stats).

*   **`twat_cache/config.py`:**
    *   `CacheConfig`: Keep this, but remove `cache_type`. Add `serializer` (optional, defaults to `json`).

*   **`twat_cache/decorators.py`:**
    *   `twat_cache`: The *only* decorator.  It will take `folder_name`, `maxsize`, `preferred_engine`, and `serializer` as keyword arguments.
        *   Internally, it will create a `CacheConfig`.
        *   It will use a helper function (`_get_backend`) to select and instantiate the appropriate backend.
        *   It will *always* create a `functools.lru_cache` instance.
        *   If a backend is available, it will wrap the `lru_cache` instance with the backend's caching logic.
        *   It will register the cache (wrapper function and stats) in `_active_caches`.

*   **`twat_cache/engines/`:**  We'll keep this directory, but drastically simplify the files.
    *   `base.py`:  Keep the `BaseCacheEngine`, but simplify it.  It will no longer need to handle key generation or argument processing. It will primarily define the interface for `get`, `set`, and `clear`.
    *   `functools.py`:  This will now simply contain a wrapper around `functools.lru_cache` to conform to the `BaseCacheEngine` interface.
    *   `diskcache.py`, `cachebox.py`, `joblib.py`, etc.:  These will be significantly simplified. They will *only* implement the `get`, `set`, and `clear` methods, leveraging their respective libraries. They will *not* handle argument processing or key generation. They will wrap the `functools.lru_cache` instance.
    *   `manager.py`:  This will be *removed*. Its functionality will be replaced by a simple helper function in `decorators.py`.

*   **`twat_cache/paths.py`:** No major changes.

*   **`twat_cache/types.py`:** No major changes.

*   **`twat_cache/utils.py`:** Add `make_key` function here.

**SNIPPETS and PSEUDOCODE**

```python:src/twat_cache/decorators.py
# this_file: src/twat_cache/decorators.py
from functools import wraps, lru_cache
from typing import Callable, TypeVar, ParamSpec, Any
from .config import CacheConfig
from .engines.base import BaseCacheEngine
from .engines.functools import FunctoolsCacheEngine  # Always available
from .engines.diskcache import DiskCacheEngine
from .engines.cachebox import CacheBoxEngine
# ... other engine imports ...
from .cache import register_cache, update_stats, CacheStats
from .utils import make_key
from loguru import logger

P = ParamSpec("P")
R = TypeVar("R")

_BACKEND_PRIORITY = [
    "cachebox",
    "diskcache",
    "joblib",
    "memory",  # functools
]

def _get_backend(config: CacheConfig) -> BaseCacheEngine:
    """Select and instantiate the appropriate cache backend."""
    if config.preferred_engine:
        if config.preferred_engine == "memory":
            return FunctoolsCacheEngine(config)
        elif config.preferred_engine == "diskcache" and DiskCacheEngine.is_available():
            return DiskCacheEngine(config)
        elif config.preferred_engine == "cachebox" and CacheBoxEngine.is_available():
            return CacheBoxEngine(config)
        # ... other preferred engines ...
        logger.warning(f"Preferred engine '{config.preferred_engine}' not available. Falling back...")

    for backend_name in _BACKEND_PRIORITY:
        if backend_name == "memory":
            return FunctoolsCacheEngine(config)
        elif backend_name == "diskcache" and DiskCacheEngine.is_available():
            return DiskCacheEngine(config)
        elif backend_name == "cachebox" and CacheBoxEngine.is_available():
            return CacheBoxEngine(config)
        # ... other backends ...

    # Should never reach here, as functools is always available
    return FunctoolsCacheEngine(config)


def twat_cache(
    folder_name: str | None = None,
    maxsize: int | None = None,
    preferred_engine: str | None = None,
    serializer: Callable[[Any], str] | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        config = CacheConfig(
            maxsize=maxsize,
            folder_name=folder_name,
            preferred_engine=preferred_engine,
            serializer=serializer
        )
        backend = _get_backend(config)
        cache_id = f"{backend.name}_{func.__name__}" # Simplified ID

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            key = make_key(*args, **kwargs, serializer=config.serializer)
            cached_result = backend.get(key)
            if cached_result is not None:
                update_stats(cache_id, hit=True)
                return cached_result

            update_stats(cache_id, miss=True)
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                backend.set(key, e)
                raise
            backend.set(key, result)
            return result

        register_cache(
            cache_id,
            backend,  # Store the backend instance itself
            wrapper,
            CacheStats(hits=0, misses=0, size=0, maxsize=config.maxsize),
        )
        return wrapper

    return decorator

```

```python:src/twat_cache/engines/base.py
# this_file: src/twat_cache/engines/base.py
from abc import ABC, abstractmethod
from typing import Any, Generic
from ..types import P, R, CacheConfig

class BaseCacheEngine(ABC, Generic[P, R]):
    def __init__(self, config: CacheConfig):
        self._config = config
        self._hits = 0
        self._misses = 0
        self._size = 0

    @abstractmethod
    def get(self, key: str) -> R | None:
        ...

    @abstractmethod
    def set(self, key: str, value: R) -> None:
        ...

    @abstractmethod
    def clear(self) -> None:
        ...

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @classmethod
    def is_available(cls) -> bool:
        return True # Override in subclasses if availability depends on imports
```

```python:src/twat_cache/engines/functools.py
# this_file: src/twat_cache/engines/functools.py
from functools import lru_cache
from typing import Any
from .base import BaseCacheEngine
from ..types import P, R, CacheConfig

class FunctoolsCacheEngine(BaseCacheEngine[P, R]):
    def __init__(self, config: CacheConfig):
        super().__init__(config)
        self._cache = lru_cache(maxsize=config.maxsize)

    def get(self, key: str) -> R | None:
        try:
            return self._cache.cache_getitem(lambda k: k, key) # type: ignore
        except KeyError:
            return None

    def set(self, key: str, value: R) -> None:
        self._cache(lambda k: k)(key)  # type: ignore
        self._cache.cache_setitem(lambda k:k, key, value) # type: ignore


    def clear(self) -> None:
        self._cache.cache_clear()

    @property
    def name(self) -> str:
        return "memory"
```

```python:src/twat_cache/engines/diskcache.py
# this_file: src/twat_cache/engines/diskcache.py
from typing import Any
from .base import BaseCacheEngine
from ..types import P, R, CacheConfig
from ..paths import get_cache_path
from loguru import logger

try:
    from diskcache import Cache
    HAS_DISKCACHE = True
except ImportError:
    HAS_DISKCACHE = False
    logger.debug("diskcache not available")

class DiskCacheEngine(BaseCacheEngine[P, R]):
    def __init__(self, config: CacheConfig):
        super().__init__(config)
        self._folder_name = config.folder_name or "diskcache"
        self._cache_dir = get_cache_path(self._folder_name)
        self._cache = Cache(str(self._cache_dir)) if HAS_DISKCACHE else None

    def get(self, key: str) -> R | None:
        if not self._cache: return None
        return self._cache.get(key)

    def set(self, key: str, value: R) -> None:
        if not self._cache: return
        self._cache.set(key, value)

    def clear(self) -> None:
        if not self._cache: return
        self._cache.clear()

    @classmethod
    def is_available(cls) -> bool:
        return HAS_DISKCACHE
```

```python:src/twat_cache/utils.py
# this_file: src/twat_cache/utils.py
import json
from typing import Any, Callable
from pathlib import Path

try:
    import platformdirs

    HAS_PLATFORMDIRS = True
except ImportError:
    HAS_PLATFORMDIRS = False


def get_cache_path(folder_name: str | None = None) -> Path:
    """Get the path for cache storage."""
    if HAS_PLATFORMDIRS:
        base_path = Path(platformdirs.user_cache_dir("twat_cache"))
    else:
        base_path = Path.home() / ".cache" / "twat_cache"

    if folder_name:
        base_path = base_path / folder_name

    base_path.mkdir(parents=True, exist_ok=True)
    return base_path

class DataclassJSONEncoder(json.JSONEncoder):
    """JSON encoder that handles dataclasses."""
    def default(self, o):
        if hasattr(o, '__dataclass_fields__'):  # Check for dataclass
            return o.__dict__
        try:
            return super().default(o)
        except TypeError:
            return str(o)  # Fallback to string representation


def make_key(*args: Any, **kwargs: Any, serializer: Callable[[Any], str] | None = None) -> str:
    """
    Create a cache key from function arguments.

    Handles unhashable types by converting them to JSON strings.  Uses a
    custom serializer if provided.
    """
    if serializer:
        return serializer((args, kwargs))

    # Use the custom encoder to handle dataclasses
    return json.dumps((args, kwargs), sort_keys=True, cls=DataclassJSONEncoder)

```

```python:src/twat_cache/cache.py
# this_file: src/twat_cache/cache.py
from typing import Any, NamedTuple
from loguru import logger
from .engines.base import BaseCacheEngine

class CacheStats(NamedTuple):
    """Cache statistics."""
    hits: int
    misses: int
    size: int
    maxsize: int | None

class CacheEntry(NamedTuple):
    """Cache registry entry."""
    cache: BaseCacheEngine[Any, Any]  # Store the engine instance
    wrapper: Any
    stats: CacheStats

_active_caches: dict[str, CacheEntry] = {}

def register_cache(name: str, cache: BaseCacheEngine[Any, Any], wrapper: Any, stats: CacheStats) -> None:
    _active_caches[name] = CacheEntry(cache, wrapper, stats)
    logger.debug(f"Registered cache: {name}")

def clear_cache(name: str | None = None) -> None:
    if name is not None:
        if name in _active_caches:
            _active_caches[name].cache.clear()
            # Reset stats (simplified)
            entry = _active_caches[name]
            _active_caches[name] = entry._replace(stats=CacheStats(0, 0, 0, entry.stats.maxsize))
        return

    for cache_name, entry in list(_active_caches.items()):  # Iterate over a copy
        entry.cache.clear()
        # Reset stats (simplified)
        _active_caches[cache_name] = entry._replace(stats=CacheStats(0, 0, 0, entry.stats.maxsize))

def get_stats(name: str | None = None) -> dict[str, Any]:
    if name is not None:
        if name not in _active_caches:
            return {
                "hits": 0,
                "misses": 0,
                "size": 0,
                "maxsize": None,
            }
        entry = _active_caches[name]
        return {
            "hits": entry.stats.hits,
            "misses": entry.stats.misses,
            "size": entry.stats.size,
            "maxsize": entry.stats.maxsize,
        }

    total_stats = {
        "total_caches": len(_active_caches),
        "hits": 0,
        "misses": 0,
        "size": 0,
    }
    for entry in _active_caches.values():
        total_stats["hits"] += entry.stats.hits
        total_stats["misses"] += entry.stats.misses
        total_stats["size"] += entry.stats.size
    return total_stats

def update_stats(name: str, *, hit: bool = False, miss: bool = False, size: int | None = None) -> None:
    if name not in _active_caches:
        return

    entry = _active_caches[name]
    hits = entry.stats.hits + (1 if hit else 0)
    misses = entry.stats.misses + (1 if miss else 0)
    new_size = size if size is not None else entry.stats.size # We don't track size changes automatically

    _active_caches[name] = CacheEntry(
        entry.cache,
        entry.wrapper,
        CacheStats(hits, misses, new_size, entry.stats.maxsize),
    )
```

```python:src/twat_cache/config.py
# this_file: src/twat_cache/config.py
from dataclasses import dataclass, field
from typing import Any, Callable

@dataclass
class CacheConfig:
    """Cache configuration."""
    maxsize: int | None = None
    folder_name: str | None = None
    preferred_engine: str | None = None
    serializer: Callable[[Any], str] | None = None  # Add serializer
    use_sql: bool = field(default=False, init=False) # Removed from __init__

    def validate(self) -> None:
        """Validate configuration."""
        if self.maxsize is not None and self.maxsize <= 0:
            msg = "maxsize must be positive if specified"
            raise ValueError(msg)
```

This detailed plan and the accompanying code snippets provide a solid foundation for refactoring `twat_cache`. The key improvements are:

*   **Reduced Code Duplication:** The single `twat_cache` decorator and simplified engine structure significantly reduce redundancy.
*   **Simplified Logic:** The fallback mechanism is much easier to understand and maintain.
*   **Improved Key Generation:** The `make_key` function is more robust.
*   **Leveraging `functools.lru_cache`:** This provides a consistent base and simplifies the engine implementations.
*   **Clearer Configuration:** The `CacheConfig` dataclass is streamlined.

The next step is to implement these changes in the codebase. I will start by editing `src/twat_cache/decorators.py`, `src/twat_cache/utils.py`, `src/twat_cache/engines/base.py`, `src/twat_cache/engines/functools.py`, `src/twat_cache/cache.py`, and `src/twat_cache/config.py` as outlined above. Then I will simplify the other engine files, and finally remove `src/twat_cache/engines/manager.py`.


---

_**User**_

continue

---

_**Assistant**_



---



---

