---
this_file: TODO.md
---

# Test Adjustment Plan

## Issues with Current Tests

1. Dependency Management:
   - Tests assume all optional backends are available
   - No proper fallback testing
   - Hard dependencies on aiocache causing test failures

2. Test Structure:
   - Magic numbers in comparisons
   - Brittle backend-specific tests
   - Insufficient async testing
   - Missing integration tests

3. Test Philosophy:
   - Tests don't follow "test behavior, not implementation"
   - Too much focus on specific backends
   - Not enough focus on fallback behavior
   - Missing performance benchmarks

## Required Test Changes

### 1. Dependency Tests
```python
def test_backend_availability():
    """Test proper backend detection and fallback."""
    # Test each backend's availability
    assert mcache.get_available_backends() == ["functools"]  # Minimum
    
    # Test fallback behavior
    @mcache()
    def func(x): return x
    
    # Should work even with no optional backends
    assert func(1) == 1
```

### 2. Decorator Tests
```python
def test_decorator_behavior():
    """Test decorator behavior regardless of backend."""
    call_count = 0
    
    @ucache()
    def func(x):
        nonlocal call_count
        call_count += 1
        return x
        
    # Test caching behavior
    assert func(1) == 1
    assert call_count == 1
    assert func(1) == 1
    assert call_count == 1  # Still 1, used cache
```

### 3. Configuration Tests
```python
def test_config_validation():
    """Test configuration validation without backend specifics."""
    # Test invalid configs
    with pytest.raises(ValidationError):
        create_cache_config(maxsize=-1)
        
    # Test valid configs
    config = create_cache_config(maxsize=None)
    assert config.maxsize is None
```

### 4. Integration Tests
```python
def test_cache_integration():
    """Test cache integration with real-world scenarios."""
    # Test with large objects
    data = [1] * 1000000
    
    @fcache(compress=True)
    def process_large_data(x):
        return sum(x)
        
    # Should handle large data efficiently
    assert process_large_data(data) == 1000000
```

### 5. Performance Tests
```python
def test_cache_performance(benchmark):
    """Test cache performance metrics."""
    @mcache()
    def func(x): return x
    
    # Measure cache hit performance
    result = benchmark(lambda: func(1))
    assert result < 0.001  # Sub-millisecond
```

## Implementation Plan

1. First Phase (Critical):
   - [ ] Remove hard dependencies in test imports
   - [ ] Add proper backend detection tests
   - [ ] Implement basic behavior tests
   - [ ] Fix configuration tests

2. Second Phase (Important):
   - [ ] Add integration tests
   - [ ] Implement performance benchmarks
   - [ ] Add stress tests
   - [ ] Add async tests

3. Third Phase (Enhancement):
   - [ ] Add security tests
   - [ ] Add race condition tests
   - [ ] Add memory leak tests
   - [ ] Add documentation tests

## Test Constants

Replace magic numbers with meaningful constants:

```python
# test_constants.py
CACHE_SIZE = 100
SMALL_CACHE = 10
LARGE_CACHE = 1000

TEST_VALUE = 42
SQUARE_INPUT = 5
SQUARE_RESULT = 25

FILE_PERMISSIONS = 0o700
CACHE_TTL = 0.5
```

## Test Categories

1. Unit Tests:
   - Core functionality without backends
   - Configuration validation
   - Key generation
   - TTL handling

2. Integration Tests:
   - Backend fallback behavior
   - File system interaction
   - Concurrent access
   - Memory management

3. Performance Tests:
   - Cache hit/miss timing
   - Memory usage
   - Disk usage
   - Network usage (for Redis)

4. Security Tests:
   - File permissions
   - Key sanitization
   - Race conditions
   - Resource cleanup

# TODO List for twat-cache

## Critical Issues (Priority 1)

### Missing Dependencies
- [ ] Fix missing `aiocache` dependency causing test failures
- [ ] Add proper dependency management in pyproject.toml
- [ ] Add fallback behavior when optional dependencies are missing

### Linter Errors
- [ ] Fix boolean argument type issues in function definitions
- [ ] Address magic number warnings in tests
- [ ] Fix unused imports in engine availability checks
- [ ] Reduce complexity in `ucache` function
- [ ] Fix module naming conflict with `functools.py`

### Type System
- [ ] Add missing type stubs for external dependencies:
  - [ ] aiocache
  - [ ] diskcache
  - [ ] joblib
  - [ ] klepto
  - [ ] redis
  - [ ] pymemcache
- [ ] Fix unbound type variables in async code
- [ ] Update Union types to use | operator (Python 3.10+)

## Important Improvements (Priority 2)

### Code Quality
- [ ] Refactor `ucache` to reduce complexity
- [ ] Improve error handling in engine imports
- [ ] Add proper cleanup in async code
- [ ] Implement proper context managers for cache resources

### Testing
- [ ] Fix failing test suite
- [ ] Add proper async test coverage
- [ ] Add stress tests for race conditions
- [ ] Add integration tests for all backends
- [ ] Add performance benchmarks

### Documentation
- [ ] Add migration guide
- [ ] Add performance comparison guide
- [ ] Add troubleshooting section
- [ ] Update type hints documentation

## Future Enhancements (Priority 3)

### Features
- [ ] Add cache warming capability
- [ ] Implement cache prefetching
- [ ] Add compression options
- [ ] Add encryption support

### Security
- [ ] Add access control
- [ ] Implement audit logging
- [ ] Add cache poisoning protection
- [ ] Improve file permission handling

### Performance
- [ ] Add caching statistics
- [ ] Optimize key generation
- [ ] Improve memory usage
- [ ] Add cache size estimation

## Development Process

1. First address critical dependency issues:
   ```bash
   uv pip install aiocache redis pymemcache
   ```

2. Then fix linter errors:
   ```bash
   hatch run lint:fix
   ```

3. Run tests to verify fixes:
   ```bash
   hatch test
   ```

4. Update documentation to reflect changes:
   ```bash
   hatch run docs:build
   ```

## Notes

- Keep both sync and async interfaces consistent
- Maintain backward compatibility
- Follow PEP 8 and type hinting best practices
- Document all changes in LOG.md

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