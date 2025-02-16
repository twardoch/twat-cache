---
this_file: TODO.md
---

# twat_cache TODO List

## Overview

`twat_cache` is a Python library providing multiple high-performance caching backends with a unified interface. The project aims to support various caching strategies from simple in-memory caching to distributed solutions.

## Implemented Features

* ✅ Memory-based cache using functools.lru_cache (always available)
* ✅ SQL-based disk cache with SQLite backend (`diskcache`)
* ✅ Async-capable caching (`aiocache`)
* ✅ Rust-based high-performance cache (`cachebox`)
* ✅ Flexible in-memory caching (`cachetools`)
* ✅ Scientific computing caching (`klepto`)
* ✅ Efficient array caching (`joblib`)
* ✅ Path management system
* ✅ Type system with abstract base classes
* ✅ Configuration management
* ✅ Basic test suite

As you develop, run 

```
uv venv; source .venv/bin/activate; uv pip install -e .[all,dev,test]; hatch run lint:fix; hatch test
```

to ensure that the code is linted and tested. This will inform your next steps. 

## Phase 1: Immediate Fixes (Completed)

* ✅ **1.1. Fix `aiocache.py` Linter Errors:**
  + ✅ **1.1.1. Correct Imports:**
  + ✅ **1.1.2. Add Type Hints:**
  + ✅ **1.1.3 Add this\_file magic record:**
* ✅ **1.2. Review and Consolidate `CacheEngine` and `BaseCacheEngine`:**
  + ✅ **1.2.1.**
  + ✅ **1.2.2.** Update all imports.
* ✅ **1.3. Update `DEPENDENCIES.txt`:**
  + ✅ **1.3.1.** Remove the incorrect file listing.
  + ✅ **1.3.2.** Add missing dependencies.

## Phase 2: Deeper Dependency Integration and Code Enhancement

* **2.1. Implement Core Cache Engine Functionality:**
  + ✅ **2.1.1.** Implement the abstract methods in engine classes.
  + ✅ **2.1.2.** Add comprehensive docstrings to these methods.
  + ✅ **2.1.3.** Rename `lru.py` to `functools.py` and update implementation.
  + ✅ **2.1.4.** Remove custom SQL and Redis implementations.
  + **2.1.5.** Fix failing tests and complete test coverage:
    - ❌ Fix Pydantic field validator issues in CacheConfig
    - ❌ Fix linting issues (27 remaining)
    - ❌ Fix cache stats tracking
    - ❌ Fix list/unhashable type handling
    - ❌ Fix cache clearing behavior
  + **2.1.6.** Add missing engine-specific tests:
    - ❌ Test cache eviction policies
    - ❌ Test concurrent access
    - ❌ Test error handling
    - ❌ Test serialization/deserialization
    - ❌ Test memory limits
    - ❌ Test cache invalidation strategies

* **2.2. Enhance `EngineManager`:**
  + **2.2.1. Prioritized Engine Selection:**
    - ✅ Fix engine priority list implementation
    - ✅ Add proper engine type hints
    - ❌ Add tests for fallback behavior
  + **2.2.2. Lazy Loading:**
    - ❌ Implement lazy engine registration
    - ❌ Add lazy import mechanism
    - ❌ Add tests for lazy loading
  + **2.2.3. Global Cache:**
    - ✅ Add proper caching to `get_engine`
    - ✅ Add cache invalidation
    - ❌ Add tests for caching behavior

* **2.3. Improve Type System:**
  + **2.3.1. Pydantic Integration:**
    - ❌ Fix field validator implementation
    - ❌ Add proper model validation
    - ❌ Add custom error messages
  + **2.3.2. Type Hints:**
    - ✅ Use `typing_extensions`
    - ✅ Update type imports
    - ❌ Add proper generic constraints
  + **2.3.3. Type Stubs:**
    - ❌ Create stub directory
    - ❌ Add stubs for optional backends
    - ❌ Add type tests

* **2.4. Configuration System:**
  + **2.4.1. Validation:**
    - ❌ Fix Pydantic model validation
    - ❌ Add config schema validation
    - ❌ Add runtime checks
  + **2.4.2. Environment Variables:**
    - ❌ Add env var support
    - ❌ Document in README.md
    - ❌ Add validation
  + **2.4.3. Default Values:**
    - ✅ Review and update
    - ✅ Add documentation
    - ❌ Add validation tests

* **2.5. `ucache` Decorator Refinement:**
  + **2.5.1. Simplified Interface:**
    - ✅ Update documentation
    - ✅ Add examples
  + **2.5.2. Key Building:**
    - ✅ Add custom key builders
    - ✅ Add tests
  + **2.5.3. Serialization:**
    - ❌ Add serializer protocol
    - ❌ Implement basic serializers
    - ❌ Add tests

* **2.6. Asynchronous Support:**
  + **2.6.1. `aiocache` Integration:**
    - ✅ Complete async methods
    - ✅ Fix event loop handling
  + **2.6.2. Async Tests:**
    - ❌ Add pytest-asyncio tests
    - ❌ Test error cases

* **2.7. Error Handling:**
  + **2.7.1. Consistent Exceptions:**
    - ❌ Create exceptions.py
    - ❌ Add custom exceptions
  + **2.7.2. Graceful Degradation:**
    - ✅ Add fallback mechanisms
    - ❌ Add tests

* **2.8. Documentation:**
  + **2.8.1. API Reference:**
    - ❌ Set up Sphinx
    - ❌ Add docstrings
  + **2.8.2. Examples:**
    - ✅ Update README.md
    - ✅ Add code examples
  + **2.8.3. Configuration Guide:**
    - ❌ Create guide
    - ❌ Add examples

* **2.9. Testing:**
  + **2.9.1 Comprehensive Unit Tests:**
    - ✅ Fix failing tests
    - ❌ Add missing tests
  + **2.9.2 Integration Tests:**
    - ✅ Add engine interaction tests
    - ✅ Add configuration tests
  + **2.9.3 Benchmark Tests:**
    - ❌ Set up pytest-benchmark
    - ❌ Add performance tests
    - ❌ Add comparison tests
