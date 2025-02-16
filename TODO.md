---
this_file: TODO.md
---

# twat_cache TODO List

## Core Goals

1. Provide simple, easy-to-use caching decorators with seamless fallback:
   - `mcache`: Memory-based caching using fastest available backend
     - Primary: cachebox (Rust-based, highest performance)
     - Secondary: cachetools (flexible in-memory)
     - Fallback: functools.lru_cache
   - `bcache`: Basic disk caching using database backends
     - Primary: diskcache (SQLite + filesystem hybrid)
     - Secondary: klepto with SQL backend
     - Fallback: mcache
   - `fcache`: Fast file-based caching for direct object access
     - Primary: joblib (optimized for NumPy arrays)
     - Secondary: klepto with file/directory backend
     - Fallback: mcache
   - `acache`: Async-capable caching (separate from sync decorators)
     - Primary: aiocache
     - Secondary: async wrapper around mcache
   - `ucache`: Universal caching that automatically selects best available backend
     - Ordered preference: cachebox > klepto > diskcache > joblib > cachetools > functools
     - Async support via aiocache when explicitly requested

2. Minimize code complexity:
   - Let 3rd party packages do the heavy lifting
   - Don't reinvent caching mechanisms
   - Provide simple passthrough to underlying functionality
   - Focus on ease of use over feature completeness

3. Implement seamless fallback:
   - If preferred backend isn't available, fall back gracefully
   - Use simple warning logs to inform about fallbacks
   - Always have functools.lru_cache as final fallback
   - Provide clear indication of which backend is being used

4. Keep it simple:
   - Remove complex abstraction layers
   - Minimize our own code
   - Provide direct access to underlying cache objects
   - Use simple kwargs for configuration

5. Advanced Features:
   - TTL support for bcache and fcache
   - Multiple eviction policies for mcache
   - Proper file permissions and security for disk caches
   - Cache inspection and maintenance utilities
   - Race condition handling in multi-process scenarios

## Detailed Implementation Plan

### 1. Core API Structure

#### src/twat_cache/__init__.py
```python
"""Flexible caching utilities for Python functions with multiple high-performance backends."""

from twat_cache.cache import clear_cache, get_stats
from twat_cache.decorators import mcache, bcache, fcache, acache, ucache
from twat_cache.utils import get_cache_path

__version__ = "1.8.0"
__all__ = ["__version__", "mcache", "bcache", "fcache", "acache", "ucache", 
           "clear_cache", "get_stats", "get_cache_path"]
```

#### src/twat_cache/decorators.py
```python
"""Core caching decorators."""
from typing import Any, Callable, TypeVar, ParamSpec, Awaitable, Optional
from collections.abc import Callable

P = ParamSpec("P")
R = TypeVar("R")
AsyncR = TypeVar("AsyncR")

def mcache(
    maxsize: Optional[int] = None,
    ttl: Optional[float] = None,
    policy: str = "lru"
) -> Callable[[Callable[P, R]], Callable[P, R]]: ...

def bcache(
    folder_name: Optional[str] = None,
    maxsize: Optional[int] = None,
    ttl: Optional[float] = None,
    sql_backend: bool = True
) -> Callable[[Callable[P, R]], Callable[P, R]]: ...

def fcache(
    folder_name: Optional[str] = None,
    maxsize: Optional[int] = None,
    ttl: Optional[float] = None,
    compress: bool = False
) -> Callable[[Callable[P, R]], Callable[P, R]]: ...

def acache(
    maxsize: Optional[int] = None,
    ttl: Optional[float] = None,
    backend: str = "aiocache"
) -> Callable[[Callable[P, Awaitable[AsyncR]]], Callable[P, Awaitable[AsyncR]]]: ...

def ucache(
    folder_name: Optional[str] = None,
    maxsize: Optional[int] = None,
    ttl: Optional[float] = None,
    preferred_engine: Optional[str] = None,
    use_async: bool = False
) -> Callable[[Callable[P, R]], Callable[P, R]]: ...
```

#### src/twat_cache/config.py
```python
"""Cache configuration system."""
from typing import Optional
from pydantic import BaseModel, Field

class CacheConfig(BaseModel):
    """Cache configuration settings."""
    maxsize: Optional[int] = Field(default=None, ge=1)
    folder_name: Optional[str] = None
    ttl: Optional[float] = Field(default=None, ge=0)
    use_sql: bool = False
    compress: bool = False
    secure: bool = True
    policy: str = "lru"
    backend: Optional[str] = None
    
    class Config:
        validate_assignment = True
        extra = "forbid"

def create_cache_config(**kwargs) -> CacheConfig: ...
```

#### src/twat_cache/engines/base.py
```python
"""Base cache engine implementation."""
from abc import ABC, abstractmethod
from typing import Generic, Optional, Any
from ..type_defs import P, R, CacheKey

class BaseCacheEngine(ABC, Generic[P, R]):
    """Abstract base class for cache engines."""
    
    @abstractmethod
    def __init__(self, config: CacheConfig) -> None: ...
    
    @abstractmethod
    def cache(self, func: Callable[P, R]) -> Callable[P, R]: ...
    
    @abstractmethod
    def get(self, key: CacheKey) -> Optional[R]: ...
    
    @abstractmethod
    def set(self, key: CacheKey, value: R) -> None: ...
    
    @abstractmethod
    def clear(self) -> None: ...
    
    @property
    @abstractmethod
    def stats(self) -> dict[str, Any]: ...
    
    @property
    @abstractmethod
    def is_available(self) -> bool: ...
```

#### src/twat_cache/engines/cachebox.py
```python
"""Rust-based high-performance cache engine."""
from typing import Optional
from ..type_defs import P, R, CacheKey
from .base import BaseCacheEngine

class CacheBoxEngine(BaseCacheEngine[P, R]):
    """Cachebox-based caching engine."""
    
    def __init__(self, config: CacheConfig) -> None: ...
    def cache(self, func: Callable[P, R]) -> Callable[P, R]: ...
    def get(self, key: CacheKey) -> Optional[R]: ...
    def set(self, key: CacheKey, value: R) -> None: ...
    def clear(self) -> None: ...
```

[Similar signatures for other engine implementations...]

#### src/twat_cache/type_defs.py
```python
"""Type definitions for the caching system."""
from typing import TypeVar, ParamSpec, Union, Any

P = ParamSpec("P")
R = TypeVar("R")
AsyncR = TypeVar("AsyncR")
CacheKey = Union[str, tuple[Any, ...]]
```

### 2. Implementation Priorities

1. Core Decorator Implementation:
   - [ ] Implement `mcache` with backend priority system
   - [ ] Implement `bcache` with SQL/disk backend selection
   - [ ] Implement `fcache` with compression support
   - [ ] Implement `acache` with async capabilities
   - [ ] Enhance `ucache` with TTL and security features

2. Engine Implementation:
   - [ ] Complete CacheBoxEngine implementation
   - [ ] Complete DiskCacheEngine with TTL
   - [ ] Complete JobLibEngine with compression
   - [ ] Complete AioCacheEngine for async
   - [ ] Add security features to all disk-based engines

3. Configuration System:
   - [ ] Implement CacheConfig with all features
   - [ ] Add validation for all config options
   - [ ] Add secure defaults for disk caches
   - [ ] Add TTL support across all engines

4. Security Features:
   - [ ] Implement secure file permissions
   - [ ] Add key sanitization
   - [ ] Add optional encryption
   - [ ] Add secure cleanup

5. Performance Features:
   - [ ] Implement compression for large objects
   - [ ] Add race condition protection
   - [ ] Optimize key generation
   - [ ] Add performance monitoring

### 3. Testing Plan

1. Unit Tests:
   ```python
   # test_decorators.py
   def test_mcache_backends(): ...
   def test_bcache_backends(): ...
   def test_fcache_backends(): ...
   async def test_acache_backends(): ...
   def test_ucache_features(): ...
   
   # test_security.py
   def test_file_permissions(): ...
   def test_key_sanitization(): ...
   def test_encryption(): ...
   
   # test_performance.py
   def test_race_conditions(): ...
   def test_compression(): ...
   def test_key_generation(): ...
   ```

2. Integration Tests:
   ```python
   # test_integration.py
   def test_backend_fallback(): ...
   def test_ttl_behavior(): ...
   def test_security_features(): ...
   async def test_async_integration(): ...
   ```

3. Benchmark Tests:
   ```python
   # test_benchmarks.py
   def test_memory_performance(): ...
   def test_disk_performance(): ...
   def test_async_performance(): ...
   ```

### 4. Documentation Plan

1. API Documentation:
   - [ ] Core decorator usage
   - [ ] Backend selection guide
   - [ ] Configuration options
   - [ ] Security best practices

2. Tutorials:
   - [ ] Basic caching guide
   - [ ] Advanced features guide
   - [ ] Security guide
   - [ ] Performance optimization guide

3. Examples:
   - [ ] Basic usage examples
   - [ ] Backend selection examples
   - [ ] Security configuration examples
   - [ ] Performance optimization examples

### 5. Release Plan

1. Version 1.8.0:
   - [ ] Complete core features
   - [ ] Fix all critical issues
   - [ ] Complete documentation
   - [ ] Pass all tests

2. Version 1.9.0:
   - [ ] Add advanced features
   - [ ] Enhance security
   - [ ] Add benchmarks
   - [ ] Add migration guide

3. Version 2.0.0:
   - [ ] Complete async support
   - [ ] Add all planned features
   - [ ] Comprehensive documentation
   - [ ] Production ready

## Development Notes

Remember to run:
```bash
uv venv; source .venv/bin/activate; uv pip install -e .[all,dev,test]; hatch run lint:fix; hatch test;
```

## Implementation Guidelines

1. Keep It Simple:
   - Use direct backend calls
   - Minimize abstraction layers
   - Focus on ease of use

2. Focus on User Experience:
   - Make decorators intuitive
   - Provide sensible defaults
   - Keep configuration minimal
   - Clear indication of active backend

3. Efficient Fallbacks:
   - Try preferred backend first
   - Fall back gracefully with warning
   - Always have functools.lru_cache as backup
   - Log backend selection clearly

4. Backend Selection:
   - Allow explicit backend choice in `ucache`
   - Provide optimized defaults per use case
   - Support async when needed
   - Implement proper security measures

5. Performance Considerations:
   - Use fastest available backend
   - Minimize serialization overhead
   - Provide direct cache access
   - Handle race conditions properly

6. Security Best Practices:
   - Secure file permissions
   - Safe key generation
   - Optional encryption
   - Proper cleanup

