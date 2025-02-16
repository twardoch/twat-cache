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

## Implementation Status

### Completed ✅
- Basic decorator interface
- Type system with protocols
- Configuration system
- Basic test structure
- Core cache engines integration

### In Progress 🚧
1. Fixing Linter Issues:
   - [ ] Remove magic numbers from tests
   - [ ] Fix boolean parameter warnings
   - [ ] Address unused imports
   - [ ] Fix function complexity issues

2. Improving Test Coverage:
   - [ ] Add proper fallback tests
   - [ ] Add async tests
   - [ ] Add integration tests
   - [ ] Add performance benchmarks

3. Documentation Updates:
   - [ ] Add migration guide
   - [ ] Add performance comparison
   - [ ] Add troubleshooting section
   - [ ] Update type hints documentation

### Next Steps 📋

1. Core Functionality (Priority 1):
   - [ ] Complete fallback mechanism implementation
   - [ ] Add proper logging for fallback cases
   - [ ] Implement cache stats collection
   - [ ] Add cache inspection utilities

2. Testing (Priority 2):
   - [ ] Add test constants for magic numbers
   - [ ] Implement proper async testing
   - [ ] Add stress tests for race conditions
   - [ ] Add backend-specific tests

3. Documentation (Priority 3):
   - [ ] Update README with new examples
   - [ ] Add detailed configuration guide
   - [ ] Document fallback behavior
   - [ ] Add performance tips

## Implementation Notes

1. Keep focus on simplicity:
   - Don't try to replicate all features of underlying cache libraries
   - Provide simple passthrough to advanced features when needed
   - Keep our code minimal and maintainable

2. Prioritize user experience:
   - Make fallback behavior transparent
   - Provide clear error messages
   - Document common use cases
   - Make configuration intuitive

3. Testing strategy:
   - Focus on behavior, not implementation
   - Test fallback scenarios thoroughly
   - Ensure proper async behavior
   - Verify cache consistency

4. Documentation approach:
   - Focus on common use cases
   - Provide clear examples
   - Document fallback behavior
   - Include troubleshooting tips