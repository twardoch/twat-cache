---
this_file: TODO.md
---

# twat_cache TODO List

## Overview

`twat_cache` is a Python library providing multiple high-performance caching backends with a unified interface. The project aims to support various caching strategies from simple in-memory caching to distributed solutions.

## Implemented Features

* ✅ Memory-based LRU cache (always available)
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

* **2.1. Implement `_get`,   `_set`,  `_clear` in `BaseCacheEngine`:**
  + ✅ **2.1.1.** Implement the abstract methods in engine classes.
  + ✅ **2.1.2.** Add comprehensive docstrings to these methods.

+ [] 2.1.2. %%%% INTERCUT TODO!

1. In @decorators.py Rename the `scache` decorator to `mcache`, and put the universal cache decorator `ucache` there, which should let us optionally specify the engine but by default use the fastest memory implementation

2. Change the name of the fallback module from `lru` to `functools` and verify that it actually DOES use it.

3. Verify every engine to see if it conforms to a common API, and if it's needed/sensible. 

4. Verify that all the glue code makes sense. Are there any redundant, unnecessary files? 

5. Then get back to TESTS.
%%%% CONTINUE BELOW


  + **2.1.3.** Add unit tests for each of these methods in `tests/test_twat_cache.py`.  **<-- NEXT**
    - Create `tests/test_twat_cache.py`.
    - Add basic test structure (setup, teardown).
    - Add tests for `LRUCacheEngine`:
      * Test `_get_cached_value` (hit and miss).
      * Test `_set_cached_value`.
      * Test `clear`.
      * Test `maxsize` enforcement.
    - Add tests for `CacheBoxEngine` (similar to LRU).
    - Add tests for `CacheToolsEngine` (similar to LRU).
    - Add tests for `DiskCacheEngine`:
      * Test interaction with the filesystem.
      * Test persistence across sessions.
    - Add tests for `JoblibEngine`:
      * Test caching of NumPy arrays.
    - Add tests for `KleptoEngine`:
      * Test persistence to disk.
    - Add tests for `AioCacheEngine`:
      * Test basic async operations.

* **2.2. Enhance `EngineManager`:**
  + **2.2.1. Prioritized Engine Selection:** Refine `get_engine` in `src/twat_cache/engines/manager.py`.
    - Implement the full priority list: `cachebox`, `cachetools`, `aiocache`, `klepto`, `diskcache`, `joblib`, `memory`.
    - Incorporate `cache_type` hints from decorators.
    - Add unit tests for priority selection.
  + **2.2.2. Lazy Loading:** Implement lazy loading of engines.
    - Modify `_register_available_engines` to only register names and availability flags.
    - Defer actual import and class instantiation until `get_engine` is called.
    - Add tests to verify lazy loading.
  + **2.2.3. Global Cache:** Add `@functools.cache` to `get_engine`.
    - Add tests to verify that the cache is working.

* **2.3. Improve Type Hinting:**
  + **2.3.1. Use `typing_extensions`:** Import and use `typing_extensions`.
    - Add `typing_extensions` to `dependencies` in `pyproject.toml`.
    - Replace `ParamSpec` import with `from typing_extensions import ParamSpec`.
  + **2.3.2. Generic Types:** Ensure consistent use of `P`,  `R`,  `CacheKey`,  `CacheValue`.
  + **2.3.3. Type Stubs:** Create `.pyi` files for optional dependencies.
    - Create `src/twat_cache/engines/stubs/`.
    - Add stub files for `cachebox`, `aiocache`, `cachetools`, `diskcache`, `joblib`, `klepto`.

* **2.4. Configuration and Defaults:**
  + **2.4.1. Centralized Configuration:** Use `GlobalConfig` and `CacheConfig` consistently.
    - Modify `ucache` to accept and pass a `CacheConfig` object.
    - Modify engine constructors to accept a `CacheConfig` object.
    - Remove individual parameter passing.
  + **2.4.2. Environment Variables:** Document environment variables in `README.md`.
  + **2.4.3. Default Values:** Review and document all default values.

* **2.5. `ucache` Decorator Refinement:**
  + **2.5.1. Simplified Interface:** Document `ucache` as the primary API.
  + **2.5.2. Key Building:** Implement a more robust key-building mechanism.
    - Allow users to provide a custom key-building function.
    - Consider using `functools.partial` for more complex keys.
    - Add tests for custom key builders.
  + **2.5.3. Serialization:** Add support for custom serializers.
    - Define a `Serializer` protocol in `types.py`.
    - Add a `serializer` parameter to `ucache`.
    - Implement `PickleSerializer`, `JSONSerializer`, `MsgpackSerializer`.
    - Add tests for different serializers.

* **2.6. Asynchronous Support:**
  + **2.6.1. `aiocache` Integration:** Complete `AioCacheEngine` implementation.
    - Ensure all methods are `async`.
    - Handle event loop management correctly.
  + **2.6.2. Async Tests:** Add async tests using `pytest-asyncio`.

* **2.7. Error Handling:**
  + **2.7.1. Consistent Exceptions:** Define custom exception classes.
    - Create `src/twat_cache/exceptions.py`.
    - Define `CacheNotFound`, `CacheError`, `ConfigurationError`.
    - Use these exceptions throughout the codebase.
  + **2.7.2. Graceful Degradation:** Implement graceful degradation.
    - Ensure `ucache` always works, falling back to `LRUCacheEngine`.

* **2.8. Documentation:**
  + **2.8.1. API Reference:** Generate API documentation.
    - Set up Sphinx.
    - Configure `sphinx-autodoc-typehints`.
    - Add docstrings to all public classes and functions.
  + **2.8.2. Examples:** Add examples to `README.md` and docstrings.
  + **2.8.3. Configuration Guide:** Create a detailed configuration guide.

* **2.9. Testing:**
  + **2.9.1 Comprehensive Unit Tests:** Complete unit test coverage.
  + **2.9.2 Integration Tests:** Develop integration tests.
    - Test interactions between different engines.
    - Test `ucache` with various configurations.
  + **2.9.3 Benchmark Tests:** Implement benchmark tests.
    - Use `pytest-benchmark`.
    - Compare performance of different backends.
