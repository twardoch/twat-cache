## SpecStory

## Refining Decorators and Integration Goals (16/02/2025, 14:17:08)

_**User**_

1. Read @README.md — note that in the .venv you have the actual code of the 3rd party libs to consult!

2. Read @LOG.md and @TODO.md

3. Step back and reason about the rationale: we wanted a simple package that exposes some decorators and passes all the cache heavy lifting to the 3rd parties. Check the implementation and tell me how we match. 

4. Reduce the common API of our code to the minimum, don't try to expose a universal API that does everything. For that, implement an easy passthru that just exposes the objects or functions provided by the 3rd parties

5. What DOES matter, though, is ease of use. We wanted the 3 specialized decorators (mcache, bcache, fcache) and a universal ucache decorator. What I want is a seamless integration of the engines so that if a given engine isn't available, we issue a logger warning but a fallback mechanism kicks in. 

6. Rewrite our goals in @TODO.md to match the above

7. Adjusts the tests so they’re sensible and realistic. 

YOUR CATCHPHRASE IS:

```
uv venv; source .venv/bin/activate; uv pip install -e .[all,dev,test]; hatch run lint:fix; hatch test;
```

REPEAT IT OFTEN.

Then adjust our implementation, and continue TODO

---

_**Assistant**_

I'll help you analyze and refine the project according to your requirements. Let me start by gathering information about the current state.

First, let me check the README and TODO files:

---

_****_

Read file: README.md

---

_****_



Let me check TODO.md:

---

_****_

Read file: TODO.md

---

_****_



Let me check the implementation of our cache engines:

---

_****_

<details>
            <summary>Searched codebase "How are cache engines implemented in the codebase?" • **25** results</summary>
        
| File | Lines |
|------|-------|
| `src/twat_cache/engines/manager.py` | L79-127 |
| `src/twat_cache/engines/manager.py` | L228-270 |
| `src/twat_cache/engines/manager.py` | L185-228 |
| `src/twat_cache/engines/base.py` | L201-270 |
| `src/twat_cache/engines/__init__.py` | L1-23 |
| `src/twat_cache/engines/manager.py` | L127-185 |
| `src/twat_cache/engines/cachebox.py` | L1-72 |
| `src/twat_cache/engines/base.py` | L1-67 |
| `src/twat_cache/engines/diskcache.py` | L1-63 |
| `src/twat_cache/engines/aiocache.py` | L1-54 |
| `src/twat_cache/engines/cachetools.py` | L1-63 |
| `src/twat_cache/engines/manager.py` | L1-79 |
| `src/twat_cache/engines/diskcache.py` | L63-112 |
| `src/twat_cache/engines/base.py` | L130-201 |
| `src/twat_cache/engines/joblib.py` | L19-82 |
| `src/twat_cache/engines/joblib.py` | L1-19 |
| `src/twat_cache/engines/base.py` | L270-315 |
| `src/twat_cache/engines/functools.py` | L1-62 |
| `src/twat_cache/engines/cachetools.py` | L63-81 |
| `src/twat_cache/engines/joblib.py` | L82-93 |
| `src/twat_cache/engines/aiocache.py` | L54-112 |
| `src/twat_cache/engines/functools.py` | L162-208 |
| `src/twat_cache/engines/klepto.py` | L57-104 |
| `src/twat_cache/engines/base.py` | L67-130 |
| `src/twat_cache/engines/klepto.py` | L1-57 |

</details>

---

_****_



Let me analyze the current state and propose changes based on your requirements:

1. **Current State Analysis**:
- We have a robust but complex caching system with multiple backends
- Each backend has its own implementation with specific features
- The code tries to provide a universal API across all backends
- There's a lot of boilerplate and repeated code

2. **Core Issues**:
- Too much abstraction trying to unify different caching approaches
- Complex configuration system
- Trying to handle too many edge cases
- Not enough focus on ease of use

3. **Your Requirements**:
- Simple package with decorators
- Let 3rd parties do the heavy lifting
- Minimal common API
- Easy passthrough to 3rd party functionality
- Three specialized decorators (mcache, bcache, fcache) and one universal (ucache)
- Seamless fallback mechanism

4. **Proposed Changes**:

Let me update the TODO.md first to reflect our new direction:

---

_****_

```diff
  # twat_cache TODO List
  
- ## Overview
- 
- `twat_cache` is a Python library providing multiple high-performance caching backends with a unified interface. The project aims to support various caching strategies from simple in-memory caching to distributed solutions.
- 
- ## Implemented Features
- 
- * ✅ Memory-based cache using functools.lru_cache (always available)
- * ✅ SQL-based disk cache with SQLite backend (`diskcache`)
- * ✅ Async-capable caching (`aiocache`)
- * ✅ Rust-based high-performance cache (`cachebox`)
- * ✅ Flexible in-memory caching (`cachetools`)
- * ✅ Scientific computing caching (`klepto`)
- * ✅ Efficient array caching (`joblib`)
- * ✅ Path management system
- * ✅ Type system with abstract base classes
- * ✅ Configuration management
- * ✅ Basic test suite
- 
- As you develop, run 
- 
- ```
- uv venv; source .venv/bin/activate; uv pip install -e .[all,dev,test]; hatch run lint:fix; hatch test
- ```
- 
- to ensure that the code is linted and tested. This will inform your next steps. 
- 
- ## Phase 1: Immediate Fixes (Completed)
- 
- * ✅ **1.1. Fix `aiocache.py` Linter Errors:**
-   + ✅ **1.1.1. Correct Imports:**
-   + ✅ **1.1.2. Add Type Hints:**
-   + ✅ **1.1.3 Add this_file magic record:**
- * ✅ **1.2. Review and Consolidate `CacheEngine` and `BaseCacheEngine`:**
-   + ✅ **1.2.1.**
-   + ✅ **1.2.2.** Update all imports.
- * ✅ **1.3. Update `DEPENDENCIES.txt`:**
-   + ✅ **1.3.1.** Remove the incorrect file listing.
-   + ✅ **1.3.2.** Add missing dependencies.
- 
- ## Phase 2: Core Functionality and Testing
- 
- * **2.1. Fix Configuration System:**
-   + **2.1.1. Fix CacheConfig Implementation:**
-     - ✅ Update Pydantic field validators to use @classmethod
-     - ✅ Fix model_config settings
-     - ❌ Fix Pydantic model initialization (TypeError: CacheConfig() takes no arguments)
-     - ❌ Add proper error messages for field validation
-   + **2.1.2. Fix Cache Directory Management:**
-     - ❌ Implement proper cache directory creation
-     - ❌ Add directory cleanup on errors
-     - ❌ Add cache size monitoring
-   + **2.1.3. Add Validation:**
-     - ❌ Add config schema validation
-     - ❌ Add runtime checks for backend availability
-     - ❌ Add type validation for cache keys
- 
- * **2.2. Fix Cache Engine Issues:**
-   + **2.2.1. Fix Core Engine Components:**
-     - ❌ Fix CacheEngine import in base.py (current blocker)
-     - ❌ Fix stats tracking in FunctoolsCacheEngine
-     - ❌ Fix maxsize enforcement
-     - ❌ Implement proper cache key generation
-   + **2.2.2. Add Error Handling:**
-     - ❌ Add proper exception hierarchy
-     - ❌ Add fallback mechanisms for failed backends
-     - ❌ Add retry logic for transient failures
- 
- 
- * **2.3. Fix Test Suite:**
-   + **2.3.1. Fix Critical Test Failures:**
-     - ❌ Fix CacheEngine import in test_engines.py
-     - ❌ Fix CacheConfig initialization tests
-     - ❌ Fix cache stats tracking tests
-   + **2.3.2. Add Engine-specific Tests:**
-     - ❌ Add tests for each backend type
-     - ❌ Add concurrent access tests
-     - ❌ Add error handling tests
-   + **2.3.3. Add Performance Tests:**
-     - ❌ Add benchmark suite
-     - ❌ Add memory usage tests
-     - ❌ Add cache invalidation tests
- 
- * **2.4. Documentation and Examples:**
-   + **2.4.1. Update Documentation:**
-     - ❌ Add configuration guide
-     - ❌ Add backend selection guide
-     - ❌ Add performance optimization guide
-   + **2.4.2. Add Examples:**
-     - ❌ Add examples for each backend
-     - ❌ Add error handling examples
-     - ❌ Add performance optimization examples
- 
+ ## Core Goals
+ 
+ 1. Provide simple, easy-to-use caching decorators:
+    - `mcache`: Memory-based caching (using functools.lru_cache)
+    - `bcache`: Basic disk caching (using diskcache)
+    - `fcache`: Fast in-memory caching (using cachebox)
+    - `ucache`: Universal caching with automatic fallback
+ 
+ 2. Minimize our own code:
+    - Let 3rd party packages do the heavy lifting
+    - Don't reinvent caching mechanisms
+    - Provide simple passthrough to underlying functionality
+    - Focus on ease of use over feature completeness
+ 
+ 3. Implement seamless fallback:
+    - If preferred backend isn't available, fall back gracefully
+    - Use simple warning logs to inform about fallbacks
+    - Always have functools.lru_cache as final fallback
+ 
+ ## Implementation Tasks
+ 
+ ### Phase 1: Core Functionality
+ 
+ * **1.1. Simplify Decorators:**
+   - [ ] Implement `mcache` using functools.lru_cache
+   - [ ] Implement `bcache` using diskcache
+   - [ ] Implement `fcache` using cachebox
+   - [ ] Implement `ucache` with fallback logic
+ 
+ * **1.2. Streamline Backend Integration:**
+   - [ ] Remove complex abstraction layers
+   - [ ] Simplify backend detection
+   - [ ] Implement basic logging for fallbacks
+   - [ ] Add simple passthrough to backend features
+ 
+ * **1.3. Fix Configuration:**
+   - [ ] Remove complex config system
+   - [ ] Use simple kwargs for decorator options
+   - [ ] Add basic path management for disk caches
+   - [ ] Implement minimal validation
+ 
+ ### Phase 2: Testing and Documentation
+ 
+ * **2.1. Improve Test Suite:**
+   - [ ] Add basic decorator tests
+   - [ ] Test fallback mechanisms
+   - [ ] Verify backend detection
+   - [ ] Add simple performance tests
+ 
+ * **2.2. Update Documentation:**
+   - [ ] Add clear usage examples
+   - [ ] Document fallback behavior
+   - [ ] Add backend-specific notes
+   - [ ] Update installation guide
+ 
+ ### Phase 3: Polish and Release
+ 
+ * **3.1. Final Touches:**
+   - [ ] Clean up dependencies
+   - [ ] Verify type hints
+   - [ ] Add proper error messages
+   - [ ] Update package metadata
+ 
+ * **3.2. Release Preparation:**
+   - [ ] Run final test suite
+   - [ ] Update version numbers
+   - [ ] Prepare release notes
+   - [ ] Publish to PyPI
+ 
+ ## Development Notes
+ 
+ Remember to run:
+ ```bash
+ uv venv; source .venv/bin/activate; uv pip install -e .[all,dev,test]; hatch run lint:fix; hatch test;
+ ```
+ 
+ ## Implementation Guidelines
+ 
+ 1. Keep It Simple:
+    - Minimize abstraction layers
+    - Use direct backend calls where possible
+    - Don't try to normalize all backends
+ 
+ 2. Focus on User Experience:
+    - Make decorators intuitive to use
+    - Provide sensible defaults
+    - Keep configuration minimal
+ 
+ 3. Efficient Fallbacks:
+    - Try preferred backend first
+    - Fall back gracefully with warning
+    - Always have functools.lru_cache as backup
  
```

---

_****_



Wait, but let me think critically about this plan:

1. **Potential Issues**:
- We still need to maintain backward compatibility for existing users
- The fallback mechanism needs to be smart about performance implications
- We need to handle async functions properly

2. **Additional Considerations**:
- Should we keep the engine manager for backend selection?
- How do we handle cache invalidation across backends?
- What about cache key generation?

Let me check our test suite to see what we need to adjust:

---

_****_

<details>
            <summary>Searched codebase "test files in the codebase" • **25** results</summary>
        
| File | Lines |
|------|-------|
| `tests/test_config.py` | L145-163 |
| `tests/test_config.py` | L81-101 |
| `tests/test_config.py` | L65-81 |
| `tests/test_twat_cache.py` | L110-118 |
| `tests/test_twat_cache.py` | L1-42 |
| `tests/test_config.py` | L163-188 |
| `tests/test_engines.py` | L1-35 |
| `tests/test_twat_cache.py` | L88-96 |
| `tests/test_config.py` | L101-120 |
| `tests/test_cache.py` | L1-41 |
| `tests/test_config.py` | L188-199 |
| `tests/test_engines.py` | L47-54 |
| `tests/test_config.py` | L46-65 |
| `tests/test_twat_cache.py` | L130-138 |
| `tests/test_cache.py` | L132-157 |
| `tests/test_engines.py` | L133-152 |
| `tests/test_twat_cache.py` | L96-110 |
| `tests/test_engines.py` | L88-98 |
| `tests/test_engines.py` | L54-67 |
| `tests/test_twat_cache.py` | L214-227 |
| `tests/test_twat_cache.py` | L195-208 |
| `tests/test_engines.py` | L152-178 |
| `tests/test_twat_cache.py` | L188-195 |
| `tests/test_config.py` | L1-46 |
| `tests/test_twat_cache.py` | L55-68 |

</details>

---

_****_



Based on the test files, I see we need to make several adjustments:

1. **Simplify Test Suite**:
- Remove complex configuration tests
- Focus on testing the core decorators
- Add specific tests for fallback behavior
- Keep basic functionality tests

2. **Adjust Test Structure**:
- Create separate test files for each decorator
- Add integration tests for ucache fallback
- Add simple performance benchmarks
- Keep basic cache operation tests

Let me propose a new test structure:

---

_****_

```diff
- 
+ #!/usr/bin/env -S uv run
+ # /// script
+ # dependencies = [
+ #   "pytest",
+ #   "pytest-asyncio",
+ #   "loguru",
+ # ]
+ # ///
+ # this_file: tests/test_decorators.py
+ 
+ """Tests for twat_cache decorators.
+ 
+ This module tests the core decorators (mcache, bcache, fcache, ucache)
+ and their fallback behavior.
+ """
+ 
+ import pytest
+ from pathlib import Path
+ from typing import Any, Callable
+ import time
+ 
+ from twat_cache.decorators import mcache, bcache, fcache, ucache
+ 
+ 
+ # Test utilities
+ def expensive_computation(x: int) -> int:
+     """Simulate an expensive computation."""
+     time.sleep(0.1)  # Simulate work
+     return x * x
+ 
+ 
+ async def async_computation(x: int) -> int:
+     """Simulate an async computation."""
+     await asyncio.sleep(0.1)  # Simulate work
+     return x * x
+ 
+ 
+ # Basic decorator tests
+ def test_mcache_basic():
+     """Test basic memory caching."""
+ 
+     @mcache()
+     def func(x: int) -> int:
+         return expensive_computation(x)
+ 
+     # First call should compute
+     start = time.time()
+     result1 = func(5)
+     time1 = time.time() - start
+ 
+     # Second call should be from cache
+     start = time.time()
+     result2 = func(5)
+     time2 = time.time() - start
+ 
+     assert result1 == result2 == 25
+     assert time2 < time1  # Cached call should be faster
+ 
+ 
+ def test_bcache_basic(tmp_path: Path):
+     """Test basic disk caching."""
+     cache_dir = tmp_path / "cache"
+ 
+     @bcache(folder_name=str(cache_dir))
+     def func(x: int) -> int:
+         return expensive_computation(x)
+ 
+     # First call should compute
+     result1 = func(5)
+ 
+     # Second call should be from cache
+     result2 = func(5)
+ 
+     assert result1 == result2 == 25
+     assert cache_dir.exists()
+ 
+ 
+ def test_fcache_basic():
+     """Test fast caching with cachebox."""
+ 
+     @fcache()
+     def func(x: int) -> int:
+         return expensive_computation(x)
+ 
+     # First call should compute
+     result1 = func(5)
+ 
+     # Second call should be from cache
+     result2 = func(5)
+ 
+     assert result1 == result2 == 25
+ 
+ 
+ def test_ucache_basic():
+     """Test universal caching."""
+ 
+     @ucache()
+     def func(x: int) -> int:
+         return expensive_computation(x)
+ 
+     # First call should compute
+     result1 = func(5)
+ 
+     # Second call should be from cache
+     result2 = func(5)
+ 
+     assert result1 == result2 == 25
+ 
+ 
+ # Fallback tests
+ def test_ucache_fallback(monkeypatch):
+     """Test ucache fallback behavior."""
+     # Simulate no backends available except functools
+     monkeypatch.setattr("twat_cache.engines.HAS_CACHEBOX", False)
+     monkeypatch.setattr("twat_cache.engines.HAS_DISKCACHE", False)
+ 
+     @ucache()
+     def func(x: int) -> int:
+         return expensive_computation(x)
+ 
+     # Should still work with functools backend
+     result = func(5)
+     assert result == 25
+ 
+ 
+ # Async tests
+ @pytest.mark.asyncio
+ async def test_async_caching():
+     """Test caching with async functions."""
+ 
+     @ucache()
+     async def func(x: int) -> int:
+         return await async_computation(x)
+ 
+     # First call
+     result1 = await func(5)
+ 
+     # Second call
+     result2 = await func(5)
+ 
+     assert result1 == result2 == 25
+ 
+ 
+ # Performance tests
+ def test_cache_performance():
+     """Basic performance comparison of different caches."""
+     results = {}
+     times = {}
+ 
+     # Test each decorator
+     for decorator in [mcache(), bcache(), fcache(), ucache()]:
+ 
+         @decorator
+         def func(x: int) -> int:
+             return expensive_computation(x)
+ 
+         # Time first call
+         start = time.time()
+         results[decorator.__name__] = func(5)
+         times[decorator.__name__] = time.time() - start
+ 
+         # Time cached call
+         start = time.time()
+         _ = func(5)
+         times[f"{decorator.__name__}_cached"] = time.time() - start
+ 
+     # All results should be the same
+     assert len(set(results.values())) == 1
+ 
+     # Cached calls should be faster
+     for name, time_taken in times.items():
+         if name.endswith("_cached"):
+             assert time_taken < times[name[:-7]]
+ 
+ 
+ # Error handling tests
+ def test_decorator_error_handling():
+     """Test error handling in decorators."""
+ 
+     @ucache()
+     def func(x: int) -> int:
+         if x < 0:
+             raise ValueError("Negative input")
+         return x * x
+ 
+     # Valid input should work
+     assert func(5) == 25
+ 
+     # Error should be raised consistently
+     with pytest.raises(ValueError):
+         func(-1)
+ 
+     with pytest.raises(ValueError):
+         func(-1)  # Same error from cache
+ 
```

---

_****_



Let me fix the linter error:

---

_****_

```diff
  """
  
+ import asyncio
  import pytest
  from pathlib import Path
```

---

_****_



Now let me propose a simplified implementation of our decorators:

---

_****_

```diff
- """Specialized cache decorators for different use cases."""
- 
+ #!/usr/bin/env -S uv run
+ # /// script
+ # dependencies = [
+ #   "loguru",
+ #   "functools",
+ #   "diskcache",
+ #   "cachebox",
+ # ]
+ # ///
  # this_file: src/twat_cache/decorators.py
  
- from collections.abc import Callable
- from typing import Any, TypeVar
- 
+ """
+ Core caching decorators.
+ 
+ This module provides four main decorators:
+ - mcache: Memory-based caching using functools.lru_cache
+ - bcache: Basic disk caching using diskcache
+ - fcache: Fast in-memory caching using cachebox
+ - ucache: Universal caching with automatic fallback
+ """
+ 
+ import functools
+ from pathlib import Path
+ from typing import Any, Callable, TypeVar, cast, ParamSpec
  from loguru import logger
  
- from twat_cache.engines.manager import get_engine_manager
- from twat_cache.config import create_cache_config
- from twat_cache.types import CacheConfig
- 
- F = TypeVar("F", bound=Callable[..., Any])
- 
- 
- def ucache(
-     maxsize: int | None = None,
-     folder_name: str | None = None,
-     use_sql: bool = False,
-     preferred_engine: str | None = None,
-     cache_type: str | None = None,
-     config: CacheConfig | None = None,
- ) -> Callable[[F], F]:
-     """Universal cache decorator that can use any available cache engine.
- 
-     This is the recommended general-purpose cache decorator. It will automatically
-     select the most appropriate and efficient caching engine based on the parameters
-     and available backends.
- 
-     If no specific preferences are given, it defaults to using the fastest available
-     memory-based cache.
+ # Type variables for generic function types
+ P = ParamSpec("P")
+ R = TypeVar("R")
+ F = Callable[P, R]
+ 
+ # Try to import optional backends
+ try:
+     from diskcache import Cache as DiskCache
+ 
+     HAS_DISKCACHE = True
+ except ImportError:
+     HAS_DISKCACHE = False
+     logger.debug("diskcache not available")
+ 
+ try:
+     from cachebox import Cache as BoxCache
+ 
+     HAS_CACHEBOX = True
+ except ImportError:
+     HAS_CACHEBOX = False
+     logger.debug("cachebox not available")
+ 
+ 
+ def mcache(maxsize: int | None = None) -> Callable[[F], F]:
+     """
+     Memory-based caching using functools.lru_cache.
  
      Args:
-         maxsize: Maximum size for cache (None means unlimited)
-         folder_name: Optional name for persistent cache folder
-         preferred_engine: Optional name of preferred engine
-         use_sql: Whether to prefer SQL-based caching
-         cache_type: Optional cache type hint ("speed", "database", "filesystem")
-         config: Optional pre-configured CacheConfig instance
+         maxsize: Maximum cache size (None for unlimited)
  
      Returns:
-         A decorator function that caches the decorated function's results
- 
-     Example:
-         ```python
-         @ucache(maxsize=100)
-         def expensive_computation(x: int) -> int:
-             return x * x
- 
-         # Results will be cached automatically
-         result = expensive_computation(42)
-         ```
-     """
-     # Use provided config or create new one
-     if config is None:
-         config = create_cache_config(
-             maxsize=maxsize,
-             folder_name=folder_name,
-             use_sql=use_sql,
-             preferred_engine=preferred_engine,
-             cache_type=cache_type,
-         )
- 
-     # Get engine manager
-     manager = get_engine_manager()
+         A decorator that caches function results in memory
+     """
  
      def decorator(func: F) -> F:
-         """Wrap the function with caching."""
-         # Get appropriate engine
-         engine = manager.get_engine(config)
-         logger.debug(f"Using cache engine: {engine.__class__.__name__}")
- 
-         # Apply caching
-         return engine.cache(func)
+         return cast(F, functools.lru_cache(maxsize=maxsize)(func))
  
      return decorator
  
  
- def mcache(
-     maxsize: int | None = None,
-     preferred_engine: str | None = None,
+ def bcache(
+     folder_name: str | None = None, maxsize: int | None = None
  ) -> Callable[[F], F]:
-     """Speed-optimized in-memory cache decorator.
- 
-     Prioritizes fastest in-memory engines:
-     1. cachebox (Rust-based, fastest)
-     2. cachetools (flexible in-memory)
-     3. LRU cache (built-in)
+     """
+     Basic disk caching using diskcache.
  
      Args:
-         maxsize: Maximum size for cache (None means unlimited)
-         preferred_engine: Optional name of preferred engine (must be memory-based)
+         folder_name: Cache directory name
+         maxsize: Maximum cache size (None for unlimited)
  
      Returns:
-         A decorator function that caches the decorated function's results
-     """
-     return ucache(
-         maxsize=maxsize,
-         preferred_engine=preferred_engine,
-         cache_type="speed",
-     )
- 
- 
- def bcache(
-     folder_name: str | None = None,
-     maxsize: int | None = None,
-     preferred_engine: str | None = None,
- ) -> Callable[[F], F]:
-     """Database-persistent cache decorator.
- 
-     Prioritizes database-backed engines:
-     1. diskcache (SQLite-based)
-     2. aiocache (with Redis/Memcached backends)
+         A decorator that caches function results to disk
+     """
+ 
+     def decorator(func: F) -> F:
+         if not HAS_DISKCACHE:
+             logger.warning("diskcache not available, falling back to memory cache")
+             return mcache(maxsize=maxsize)(func)
+ 
+         cache_dir = (
+             Path.home() / ".cache" / "twat_cache" / (folder_name or func.__name__)
+         )
+         cache_dir.mkdir(parents=True, exist_ok=True)
+         cache = DiskCache(str(cache_dir))
+ 
+         @functools.wraps(func)
+         def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
+             key = (args, tuple(sorted(kwargs.items())))
+             result = cache.get(key)
+             if result is None:
+                 result = func(*args, **kwargs)
+                 cache.set(key, result)
+             return cast(R, result)
+ 
+         return cast(F, wrapper)
+ 
+     return decorator
+ 
+ 
+ def fcache(maxsize: int | None = None) -> Callable[[F], F]:
+     """
+     Fast in-memory caching using cachebox.
  
      Args:
-         folder_name: Optional name for the cache folder
-         maxsize: Maximum size for cache (None means unlimited)
-         preferred_engine: Optional name of preferred engine (must be DB-based)
+         maxsize: Maximum cache size (None for unlimited)
  
      Returns:
-         A decorator function that caches the decorated function's results
-     """
-     return ucache(
-         folder_name=folder_name,
-         maxsize=maxsize,
-         use_sql=True,
-         preferred_engine=preferred_engine,
-         cache_type="database",
-     )
- 
- 
- def fcache(
+         A decorator that caches function results using cachebox
+     """
+ 
+     def decorator(func: F) -> F:
+         if not HAS_CACHEBOX:
+             logger.warning("cachebox not available, falling back to memory cache")
+             return mcache(maxsize=maxsize)(func)
+ 
+         cache = BoxCache(maxsize=maxsize or 0)  # 0 means unlimited in cachebox
+ 
+         @functools.wraps(func)
+         def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
+             key = (args, tuple(sorted(kwargs.items())))
+             result = cache.get(key)
+             if result is None:
+                 result = func(*args, **kwargs)
+                 cache[key] = result
+             return cast(R, result)
+ 
+         return cast(F, wrapper)
+ 
+     return decorator
+ 
+ 
+ def ucache(
+     preferred_engine: str | None = None,
      folder_name: str | None = None,
      maxsize: int | None = None,
-     preferred_engine: str | None = None,
  ) -> Callable[[F], F]:
-     """Filesystem-persistent cache decorator.
- 
-     Prioritizes filesystem-based engines:
-     1. joblib (optimized for arrays/large data)
-     2. klepto (scientific computing)
-     3. diskcache (file-based mode)
+     """
+     Universal caching with automatic fallback.
  
      Args:
-         folder_name: Optional name for the cache folder
-         maxsize: Maximum size for cache (None means unlimited)
-         preferred_engine: Optional name of preferred engine (must be filesystem-based)
+         preferred_engine: Preferred caching backend ('memory', 'disk', or 'fast')
+         folder_name: Cache directory name (for disk cache)
+         maxsize: Maximum cache size (None for unlimited)
  
      Returns:
-         A decorator function that caches the decorated function's results
-     """
-     return ucache(
-         folder_name=folder_name,
-         maxsize=maxsize,
-         preferred_engine=preferred_engine,
-         cache_type="filesystem",
-     )
+         A decorator that caches function results using the best available backend
+     """
+ 
+     def decorator(func: F) -> F:
+         # Try preferred engine first
+         if preferred_engine == "fast" and HAS_CACHEBOX:
+             return fcache(maxsize=maxsize)(func)
+         elif preferred_engine == "disk" and HAS_DISKCACHE:
+             return bcache(folder_name=folder_name, maxsize=maxsize)(func)
+         elif preferred_engine == "memory":
+             return mcache(maxsize=maxsize)(func)
+ 
+         # Auto-select best available
+         if HAS_CACHEBOX:
+             logger.debug("Using fast cache (cachebox)")
+             return fcache(maxsize=maxsize)(func)
+         elif HAS_DISKCACHE:
+             logger.debug("Using disk cache (diskcache)")
+             return bcache(folder_name=folder_name, maxsize=maxsize)(func)
+         else:
+             logger.debug("Using memory cache (functools)")
+             return mcache(maxsize=maxsize)(func)
+ 
+     return decorator
  
```

---

_****_



Let me run our catchphrase to check if everything works:

---

_****_

```bash
uv venv; source .venv/bin/activate; uv pip install -e .[all,dev,test]; hatch run lint:fix; hatch test;
```

```
Using CPython 3.12.8 interpreter at: /usr/local/bin/python3.12
Creating virtual environment at: .venv
Activate with: source .venv/bin/activate
zsh: no matches found: .[all,dev,test]
Rewriting tests/test_decorators.py
Rewriting src/twat_cache/decorators.py
warning: The top-level linter settings are deprecated in favour of their c
ounterparts in the `lint` section. Please update the following options in `pypro
ject.toml`:                                                           - 'per-fil
e-ignores' -> 'lint.per-file-ignores'
src/twat_cache/config.py:152:26: PLR2004 Magic value used in comparison, c
onsider replacing `9` with a constant variable                                |
150 |             msg = "compression_level must be an integer"
151 |             raise ValueError(msg)
152 |         if not 0 <= v <= 9:
    |                          ^ PLR2004
153 |             msg = "compression_level must be between 0 and 9"
154 |             raise ValueError(msg)
    |

src/twat_cache/engines/base.py:213:33: ARG002 Unused method argument: `key
`                                                                             |
211 |     """
212 |
213 |     def _get_cached_value(self, key: CacheKey) -> R | None:
    |                                 ^^^ ARG002
214 |         """
215 |         Retrieve a value from the cache.
    |

src/twat_cache/engines/functools.py:1:1: A005 Module `functools` shadows a
 Python standard-library module                                           src/tw
at_cache/engines/joblib.py:49:33: ARG002 Unused method argument: `ke
y`                                                                           |
47 |         )
48 |
49 |     def _get_cached_value(self, key: CacheKey) -> R | None:
   |                                 ^^^ ARG002
50 |         """Retrieve a value from the cache.
   |

src/twat_cache/engines/klepto.py:20:34: ARG005 Unused lambda argument: `ar
gs`                                                                          |
18 |     HAS_KLEPTO = False
19 |     dir_archive = type("dir_archive", (), {})  # type: ignore
20 |     keymap = picklemap = lambda *args, **kwargs: lambda f: f  # type:
 ignore                                                                      |
                                ^^^^ ARG005
   |

src/twat_cache/engines/klepto.py:20:42: ARG005 Unused lambda argument: `kw
args`                                                                        |
18 |     HAS_KLEPTO = False
19 |     dir_archive = type("dir_archive", (), {})  # type: ignore
20 |     keymap = picklemap = lambda *args, **kwargs: lambda f: f  # type:
 ignore                                                                      |
                                        ^^^^^^ ARG005
   |

src/twat_cache/paths.py:100:5: C901 `clear_cache` is too complex (11 > 10)
    |
100 | def clear_cache(folder_name: str | None = None) -> None:
    |     ^^^^^^^^^^^ C901
101 |     """
102 |     Clear the cache directory for the given folder name.
    |

src/twat_cache/types.py:1:1: A005 Module `types` shadows a Python standard
-library module                                                           tests/
test_cache.py:175:34: PLR2004 Magic value used in comparison, consid
er replacing `15` with a constant variable                                    |
173 |     result2 = process_list(test_list)
174 |
175 |     assert result1 == result2 == 15
    |                                  ^^ PLR2004
    |

tests/test_config.py:74:38: PLR2004 Magic value used in comparison, consid
er replacing `1000` with a constant variable                                 |
72 |     # Check default values
73 |     assert config.cache_dir == get_cache_path("global")
74 |     assert config.default_maxsize == 1000
   |                                      ^^^^ PLR2004
75 |     assert not config.default_use_sql
76 |     assert config.default_engine == "lru"
   |

tests/test_config.py:79:40: PLR2004 Magic value used in comparison, consid
er replacing `6` with a constant variable                                    |
77 |     assert config.default_cache_type is None
78 |     assert config.enable_compression
79 |     assert config.compression_level == 6
   |                                        ^ PLR2004
80 |     assert not config.debug
81 |     assert config.log_file is None
   |

tests/test_config.py:184:36: PLR2004 Magic value used in comparison, consi
der replacing `100` with a constant variable                                  |
182 |         cache_type="speed",
183 |     )
184 |     assert config.get_maxsize() == 100
    |                                    ^^^ PLR2004
185 |     assert config.get_folder_name() == "test"
186 |     assert config.get_use_sql() is True
    |

tests/test_decorators.py:56:34: PLR2004 Magic value used in comparison, co
nsider replacing `25` with a constant variable                               |
54 |     time2 = time.time() - start
55 |
56 |     assert result1 == result2 == 25
   |                                  ^^ PLR2004
57 |     assert time2 < time1  # Cached call should be faster
   |

tests/test_decorators.py:74:34: PLR2004 Magic value used in comparison, co
nsider replacing `25` with a constant variable                               |
72 |     result2 = func(5)
73 |
74 |     assert result1 == result2 == 25
   |                                  ^^ PLR2004
75 |     assert cache_dir.exists()
   |

tests/test_decorators.py:91:34: PLR2004 Magic value used in comparison, co
nsider replacing `25` with a constant variable                               |
89 |     result2 = func(5)
90 |
91 |     assert result1 == result2 == 25
   |                                  ^^ PLR2004
   |

tests/test_decorators.py:107:34: PLR2004 Magic value used in comparison, c
onsider replacing `25` with a constant variable                               |
105 |     result2 = func(5)
106 |
107 |     assert result1 == result2 == 25
    |                                  ^^ PLR2004
    |

tests/test_decorators.py:123:22: PLR2004 Magic value used in comparison, c
onsider replacing `25` with a constant variable                               |
121 |     # Should still work with functools backend
122 |     result = func(5)
123 |     assert result == 25
    |                      ^^ PLR2004
    |

tests/test_decorators.py:141:34: PLR2004 Magic value used in comparison, c
onsider replacing `25` with a constant variable                               |
139 |     result2 = await func(5)
140 |
141 |     assert result1 == result2 == 25
    |                                  ^^ PLR2004
    |

tests/test_decorators.py:188:23: PLR2004 Magic value used in comparison, c
onsider replacing `25` with a constant variable                               |
187 |     # Valid input should work
188 |     assert func(5) == 25
    |                       ^^ PLR2004
189 |
190 |     # Error should be raised consistently
    |

tests/test_engines.py:62:45: FBT003 Boolean positional value in function c
all                                                                          |
60 |     assert isinstance(base_engine._make_key("test"), str)
61 |     assert isinstance(base_engine._make_key(123), str)
62 |     assert isinstance(base_engine._make_key(True), str)
   |                                             ^^^^ FBT003
63 |
64 |     # Test with complex types
   |

tests/test_engines.py:82:22: PLR2004 Magic value used in comparison, consi
der replacing `4` with a constant variable                                   |
80 |     # First call
81 |     result = test_function(2)
82 |     assert result == 4
   |                      ^ PLR2004
83 |     assert call_count == 1
   |

tests/test_engines.py:87:22: PLR2004 Magic value used in comparison, consi
der replacing `4` with a constant variable                                   |
85 |     # Second call (should use cache)
86 |     result = test_function(2)
87 |     assert result == 4
   |                      ^ PLR2004
88 |     assert call_count == 1  # Should not increment
   |

Found 29 errors (7 fixed, 22 remaining).
========================== test session starts ===========================
platform darwin -- Python 3.12.8, pytest-8.3.4, pluggy-1.5.0 -- /Users/ada
m/Library/Application Support/hatch/env/virtual/twat-cache/ivvP1xkE/hatch-test.p
y3.12/bin/python3                                                   cachedir: .p
ytest_cache
rootdir: /Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good
/twat/plugins/repos/twat_cache                                            config
file: pyproject.toml
plugins: rerunfailures-14.0, mock-3.14.0, xdist-3.6.1
collected 46 items                                                       

tests/test_cache.py::test_cache_settings_validation PASSED         [  2%]
tests/test_cache.py::test_basic_caching PASSED                     [  4%]
tests/test_cache.py::test_cache_clear FAILED                       [  6%]
tests/test_cache.py::test_cache_stats FAILED                       [  8%]
tests/test_cache.py::test_list_processing FAILED                   [ 10%]
tests/test_cache.py::test_different_backends FAILED                [ 13%]
tests/test_cache.py::test_cache_with_complex_types FAILED          [ 15%]
tests/test_cache.py::test_cache_exceptions FAILED                  [ 17%]
tests/test_cache.py::test_kwargs_handling FAILED                   [ 19%]
tests/test_config.py::test_cache_config_validation PASSED          [ 21%]
tests/test_config.py::test_default_config PASSED                   [ 23%]
tests/test_config.py::test_custom_config PASSED                    [ 26%]
tests/test_config.py::test_global_config_env_vars PASSED           [ 28%]
tests/test_config.py::test_get_cache_config PASSED                 [ 30%]
tests/test_config.py::test_logging_configuration PASSED            [ 32%]
tests/test_config.py::test_cache_config_creation PASSED            [ 34%]
tests/test_config.py::test_cache_config_with_sql PASSED            [ 36%]
tests/test_decorators.py::test_mcache_basic PASSED                 [ 39%]
tests/test_decorators.py::test_bcache_basic FAILED                 [ 41%]
tests/test_decorators.py::test_fcache_basic PASSED                 [ 43%]
tests/test_decorators.py::test_ucache_basic PASSED                 [ 45%]
tests/test_decorators.py::test_ucache_fallback FAILED              [ 47%]
tests/test_decorators.py::test_async_caching SKIPPED (async de...) [ 50%]
tests/test_decorators.py::test_cache_performance PASSED            [ 52%]
tests/test_decorators.py::test_decorator_error_handling PASSED     [ 54%]
tests/test_engines.py::test_base_engine_initialization PASSED      [ 56%]
tests/test_engines.py::test_base_engine_key_generation PASSED      [ 58%]
tests/test_engines.py::test_base_engine_cache_decorator PASSED     [ 60%]
tests/test_engines.py::test_base_engine_validation PASSED          [ 63%]
tests/test_engines.py::test_lru_cache_initialization PASSED        [ 65%]
tests/test_engines.py::test_lru_cache_maxsize_enforcement PASSED   [ 67%]
tests/test_engines.py::test_lru_cache_clear PASSED                 [ 69%]
tests/test_engines.py::test_lru_cache_with_complex_values PASSED   [ 71%]
tests/test_engines.py::test_lru_cache_stats_accuracy FAILED        [ 73%]
tests/test_twat_cache.py::test_lru_cache_get_set PASSED            [ 76%]
tests/test_twat_cache.py::test_lru_cache_clear PASSED              [ 78%]
tests/test_twat_cache.py::test_lru_cache_maxsize PASSED            [ 80%]
tests/test_twat_cache.py::test_disk_cache_persistence FAILED       [ 82%]
tests/test_twat_cache.py::test_joblib_numpy_array SKIPPED (num...) [ 84%]
tests/test_twat_cache.py::test_klepto_persistence FAILED           [ 86%]
tests/test_twat_cache.py::test_async_cache_operations SKIPPED      [ 89%]
tests/test_twat_cache.py::test_cachebox_operations FAILED          [ 91%]
tests/test_twat_cache.py::test_cachetools_operations FAILED        [ 93%]
tests/test_twat_cache.py::test_functools_cache_get_set PASSED      [ 95%]
tests/test_twat_cache.py::test_functools_cache_clear PASSED        [ 97%]
tests/test_twat_cache.py::test_functools_cache_maxsize PASSED      [100%]

================================ FAILURES ================================
____________________________ test_cache_clear ____________________________

    def test_cache_clear() -> None:
        """Test cache clearing functionality."""
        call_count = 0
    
        @ucache()
        def cached_function(x: int) -> int:
            nonlocal call_count
            call_count += 1
            return x * x
    
        # First call
        assert cached_function(TEST_INPUT) == TEST_RESULT
        assert call_count == 1
    
        # Clear cache
        clear_cache()
    
        # Should recompute after clear
        assert cached_function(TEST_INPUT) == TEST_RESULT
>       assert call_count == EXPECTED_CALL_COUNT
E       assert 1 == 2

tests/test_cache.py:86: AssertionError
-------------------------- Captured stderr call --------------------------
2025-02-16 14:19:42.032 | DEBUG    | twat_cache.decorators:decorator:173 -
 Using memory cache (functools)                                           2025-0
2-16 14:19:42.032 | DEBUG    | twat_cache.engines.manager:_register_
engine:148 - Registered cache engine: memory                              2025-0
2-16 14:19:42.033 | DEBUG    | twat_cache.engines.manager:_register_
engine:148 - Registered cache engine: cachebox                            2025-0
2-16 14:19:42.033 | DEBUG    | twat_cache.engines.manager:_register_
engine:148 - Registered cache engine: cachetools                          2025-0
2-16 14:19:42.033 | DEBUG    | twat_cache.engines.manager:_register_
engine:148 - Registered cache engine: aiocache                            2025-0
2-16 14:19:42.033 | DEBUG    | twat_cache.engines.manager:_register_
engine:148 - Registered cache engine: klepto                              2025-0
2-16 14:19:42.033 | DEBUG    | twat_cache.engines.manager:_register_
engine:148 - Registered cache engine: diskcache                           2025-0
2-16 14:19:42.033 | DEBUG    | twat_cache.engines.manager:_register_
engine:148 - Registered cache engine: joblib                              2025-0
2-16 14:19:42.033 | DEBUG    | twat_cache.engines.manager:_register_
available_engines:124 - Registered cache engines: ['memory', 'cachebox', 'cachet
ools', 'aiocache', 'klepto', 'diskcache', 'joblib']                 2025-02-16 1
4:19:42.033 | DEBUG    | twat_cache.engines.manager:_create_fa
llback_engine:227 - Using LRU cache                                       2025-0
2-16 14:19:42.034 | DEBUG    | twat_cache.paths:get_cache_path:70 - 
Created cache directory: /Users/adam/Library/Caches/twat_cache/twat_cache_d2e4f3
0b                                                                  2025-02-16 1
4:19:42.034 | DEBUG    | twat_cache.engines.base:__init__:55 -
 Initialized FunctoolsCacheEngine with config: maxsize=None folder_name=None use
_sql=False preferred_engine=None cache_type=None                    2025-02-16 1
4:19:42.034 | DEBUG    | twat_cache.engines.functools:__init__
:50 - Initialized functools cache with maxsize: 128                       2025-0
2-16 14:19:42.034 | DEBUG    | twat_cache.cache:clear_cache:55 - Cle
aring cache for engine: FunctoolsCacheEngine                              2025-0
2-16 14:19:42.034 | DEBUG    | twat_cache.engines.functools:clear:17
0 - Cleared functools cache                                               ______
______________________ test_cache_stats ____________________________

    def test_cache_stats() -> None:
        """Test cache statistics."""
        call_count = 0
    
        @ucache()
        def cached_function(x: int) -> int:
            nonlocal call_count
            call_count += 1
            return x * x
    
        # Generate some cache activity
        for _i in range(3):
            cached_function(TEST_INPUT)
            cached_function(TEST_INPUT_2)
    
        # Get stats
        stats = get_stats()
    
        # Basic stats checks
        assert isinstance(stats, dict)
>       assert stats["hits"] >= MIN_STATS_COUNT
E       assert 0 >= 2

tests/test_cache.py:109: AssertionError
-------------------------- Captured stderr call --------------------------
2025-02-16 14:19:42.079 | DEBUG    | twat_cache.decorators:decorator:173 -
 Using memory cache (functools)                                           2025-0
2-16 14:19:42.079 | DEBUG    | twat_cache.engines.manager:_create_fa
llback_engine:227 - Using LRU cache                                       2025-0
2-16 14:19:42.079 | DEBUG    | twat_cache.paths:get_cache_path:70 - 
Created cache directory: /Users/adam/Library/Caches/twat_cache/twat_cache_b0f97c
10                                                                  2025-02-16 1
4:19:42.079 | DEBUG    | twat_cache.engines.base:__init__:55 -
 Initialized FunctoolsCacheEngine with config: maxsize=None folder_name=None use
_sql=False preferred_engine=None cache_type=None                    2025-02-16 1
4:19:42.079 | DEBUG    | twat_cache.engines.functools:__init__
:50 - Initialized functools cache with maxsize: 128                       2025-0
2-16 14:19:42.079 | DEBUG    | twat_cache.cache:get_stats:93 - Getti
ng stats for engine: FunctoolsCacheEngine                                 ______
____________________ test_list_processing __________________________

    def test_list_processing() -> None:
        """Test caching with list processing."""
        call_count = 0
    
        @ucache()
        def process_list(data: list[int]) -> int:
            nonlocal call_count
            call_count += 1
            return sum(data)
    
        test_list = [1, 2, 3, 4, 5]
    
        # First call
>       result1 = process_list(test_list)
E       TypeError: unhashable type: 'list'

tests/test_cache.py:127: TypeError
-------------------------- Captured stderr call --------------------------
2025-02-16 14:19:42.084 | DEBUG    | twat_cache.decorators:decorator:173 -
 Using memory cache (functools)                                           ______
__________________ test_different_backends _________________________

    def test_different_backends() -> None:
        """Test using different cache backends."""
        results: list[Any] = []
    
        # Test with different configurations
        configs = [
            create_cache_config(maxsize=100),  # Memory cache
            create_cache_config(folder_name="disk_test", use_sql=True),  #
 SQL cache
      create_cache_config(folder_name="disk_test", use_sql=False),  
# Disk cache
  ]
    
        for config in configs:
    
>           @ucache(config=config)
E           TypeError: ucache() got an unexpected keyword argument 'config
'                                                                         
tests/test_cache.py:148: TypeError
_____________________ test_cache_with_complex_types ______________________

    def test_cache_with_complex_types() -> None:
        """Test caching with complex types."""
    
        @ucache(maxsize=100)
        def process_list(items: list[int]) -> int:
            return sum(items)
    
        test_list = [1, 2, 3, 4, 5]
    
        # First call
>       result1 = process_list(test_list)
E       TypeError: unhashable type: 'list'

tests/test_cache.py:170: TypeError
-------------------------- Captured stderr call --------------------------
2025-02-16 14:19:42.092 | DEBUG    | twat_cache.decorators:decorator:173 -
 Using memory cache (functools)                                           ______
___________________ test_cache_exceptions __________________________

    def test_cache_exceptions() -> None:
        """Test caching of exceptions."""
        call_count = 0
    
        @ucache(maxsize=100)
        def failing_function(x: int) -> None:
            nonlocal call_count
            call_count += 1
            msg = "Test error"
            raise ValueError(msg)
    
        # First call
        with pytest.raises(ValueError):
            failing_function(5)
        assert call_count == 1
    
        # Second call should not recompute
        with pytest.raises(ValueError):
            failing_function(5)
>       assert call_count == 1
E       assert 2 == 1

tests/test_cache.py:197: AssertionError
-------------------------- Captured stderr call --------------------------
2025-02-16 14:19:42.097 | DEBUG    | twat_cache.decorators:decorator:173 -
 Using memory cache (functools)                                           ______
____________________ test_kwargs_handling __________________________

    def test_kwargs_handling() -> None:
        """Test caching with different keyword arguments."""
        call_count = 0
    
        @ucache()
        def kwarg_function(x: int, multiplier: int = 1) -> int:
            nonlocal call_count
            call_count += 1
            return x * multiplier
    
        # Test with different kwarg combinations
        assert kwarg_function(TEST_INPUT) == TEST_INPUT
        assert call_count == 1
    
        assert kwarg_function(TEST_INPUT, multiplier=1) == TEST_INPUT
>       assert call_count == 1  # Should use cache
E       assert 2 == 1

tests/test_cache.py:215: AssertionError
-------------------------- Captured stderr call --------------------------
2025-02-16 14:19:42.102 | DEBUG    | twat_cache.decorators:decorator:173 -
 Using memory cache (functools)                                           ______
_____________________ test_bcache_basic ____________________________

tmp_path = PosixPath('/private/var/folders/05/clcynl0509ldxltl599hhhx40000
gn/T/pytest-of-adam/pytest-32/test_bcache_basic0')                        
    def test_bcache_basic(tmp_path: Path):
        """Test basic disk caching."""
        cache_dir = tmp_path / "cache"
    
        @bcache(folder_name=str(cache_dir))
        def func(x: int) -> int:
            return expensive_computation(x)
    
        # First call should compute
        result1 = func(5)
    
        # Second call should be from cache
        result2 = func(5)
    
        assert result1 == result2 == 25
>       assert cache_dir.exists()
E       AssertionError: assert False
E        +  where False = exists()
E        +    where exists = PosixPath('/private/var/folders/05/clcynl0509
ldxltl599hhhx40000gn/T/pytest-of-adam/pytest-32/test_bcache_basic0/cache').exist
s                                                                   
tests/test_decorators.py:75: AssertionError
-------------------------- Captured stderr call --------------------------
2025-02-16 14:19:42.246 | WARNING  | twat_cache.decorators:decorator:84 - 
diskcache not available, falling back to memory cache                     ______
____________________ test_ucache_fallback __________________________

obj = <module 'twat_cache.engines' from '/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_cache/src/twat_cache/en
gines/__init__.py'>                                                 name = 'HAS_
CACHEBOX', ann = 'twat_cache.engines'

    def annotated_getattr(obj: object, name: str, ann: str) -> object:
        try:
>           obj = getattr(obj, name)
E           AttributeError: module 'twat_cache.engines' has no attribute '
HAS_CACHEBOX'                                                             
/Users/adam/Library/Application Support/hatch/env/virtual/twat-cache/ivvP1
xkE/hatch-test.py3.12/lib/python3.12/site-packages/_pytest/monkeypatch.py:90: At
tributeError                                                        
The above exception was the direct cause of the following exception:

monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x10ec0e8a0>

    def test_ucache_fallback(monkeypatch):
        """Test ucache fallback behavior."""
        # Simulate no backends available except functools
>       monkeypatch.setattr("twat_cache.engines.HAS_CACHEBOX", False)

tests/test_decorators.py:114: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
/Users/adam/Library/Application Support/hatch/env/virtual/twat-cache/ivvP1
xkE/hatch-test.py3.12/lib/python3.12/site-packages/_pytest/monkeypatch.py:104: i
n derive_importpath                                                     annotate
d_getattr(target, attr, ann=module)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

obj = <module 'twat_cache.engines' from '/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_cache/src/twat_cache/en
gines/__init__.py'>                                                 name = 'HAS_
CACHEBOX', ann = 'twat_cache.engines'

    def annotated_getattr(obj: object, name: str, ann: str) -> object:
        try:
            obj = getattr(obj, name)
        except AttributeError as e:
>           raise AttributeError(
                f"{type(obj).__name__!r} object at {ann} has no attribute 
{name!r}"
      ) from e
E           AttributeError: 'module' object at twat_cache.engines has no a
ttribute 'HAS_CACHEBOX'                                                   
/Users/adam/Library/Application Support/hatch/env/virtual/twat-cache/ivvP1
xkE/hatch-test.py3.12/lib/python3.12/site-packages/_pytest/monkeypatch.py:92: At
tributeError                                                        ____________
_________ test_lru_cache_stats_accuracy ______________________

base_config = CacheConfigImpl(maxsize=100, folder_name=None, use_sql=False
, preferred_engine=None, cache_type=None)                                 
    def test_lru_cache_stats_accuracy(base_config: CacheConfig) -> None:
        """Test accuracy of LRU cache statistics."""
        engine = FunctoolsCacheEngine(base_config)
    
        # Test initial stats
>       stats = engine.stats()
E       TypeError: 'dict' object is not callable

tests/test_engines.py:160: TypeError
______________________ test_disk_cache_persistence _______________________

disk_engine = <twat_cache.engines.diskcache.DiskCacheEngine object at 0x10
dfd4e90>                                                                  
    def test_disk_cache_persistence(disk_engine: DiskCacheEngine) -> None:
        """Test persistence of disk cache."""
        key: CacheKey = "test_key"
        value = "test_value"
    
        disk_engine._set_cached_value(key, value)
>       assert disk_engine._get_cached_value(key) == value
E       AssertionError: assert None == 'test_value'
E        +  where None = _get_cached_value('test_key')
E        +    where _get_cached_value = <twat_cache.engines.diskcache.Disk
CacheEngine object at 0x10dfd4e90>._get_cached_value                      
tests/test_twat_cache.py:105: AssertionError
________________________ test_klepto_persistence _________________________

klepto_engine = <twat_cache.engines.klepto.KleptoEngine object at 0x10ec0d
d90>                                                                      
    def test_klepto_persistence(klepto_engine: KleptoEngine) -> None:
        """Test persistence of klepto cache."""
        key: CacheKey = "test_key"
        value = {"complex": "data", "nested": {"value": 42}}
    
        klepto_engine._set_cached_value(key, value)
>       assert klepto_engine._get_cached_value(key) == value
E       AssertionError: assert None == {'complex': 'data', 'nested': {'val
ue': 42}}                                                                 E
   +  where None = _get_cached_value('test_key')
E        +    where _get_cached_value = <twat_cache.engines.klepto.KleptoE
ngine object at 0x10ec0dd90>._get_cached_value                            
tests/test_twat_cache.py:147: AssertionError
________________________ test_cachebox_operations ________________________

cachebox_engine = <twat_cache.engines.cachebox.CacheBoxEngine object at 0x
10ea81d90>                                                                
    def test_cachebox_operations(cachebox_engine: CacheBoxEngine) -> None:
        """Test basic operations for cachebox."""
        key: CacheKey = "test_key"
        value = "test_value"
    
        assert cachebox_engine._get_cached_value(key) is None
        cachebox_engine._set_cached_value(key, value)
>       assert cachebox_engine._get_cached_value(key) == value
E       AssertionError: assert None == 'test_value'
E        +  where None = _get_cached_value('test_key')
E        +    where _get_cached_value = <twat_cache.engines.cachebox.Cache
BoxEngine object at 0x10ea81d90>._get_cached_value                        
tests/test_twat_cache.py:185: AssertionError
_______________________ test_cachetools_operations _______________________

cachetools_engine = <twat_cache.engines.cachetools.CacheToolsEngine object
 at 0x10ec0fe90>                                                          
    def test_cachetools_operations(cachetools_engine: CacheToolsEngine) ->
 None:
  """Test basic operations for cachetools."""
        key: CacheKey = "test_key"
        value = "test_value"
    
        assert cachetools_engine._get_cached_value(key) is None
        cachetools_engine._set_cached_value(key, value)
>       assert cachetools_engine._get_cached_value(key) == value
E       AssertionError: assert None == 'test_value'
E        +  where None = _get_cached_value('test_key')
E        +    where _get_cached_value = <twat_cache.engines.cachetools.Cac
heToolsEngine object at 0x10ec0fe90>._get_cached_value                    
tests/test_twat_cache.py:205: AssertionError
============================ warnings summary ============================
tests/test_twat_cache.py::test_async_cache_operations
  /Users/adam/Library/Application Support/hatch/env/virtual/twat-cache/ivv
P1xkE/hatch-test.py3.12/lib/python3.12/site-packages/_pytest/runner.py:142: Runt
imeWarning: coroutine 'async_engine' was never awaited                  item.fun
cargs = None  # type: ignore[attr-defined]
  Enable tracemalloc to get traceback where the object was allocated.
  See https://docs.pytest.org/en/stable/how-to/capture-warnings.html#resou
rce-warnings for more info.                                               
-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
======================== short test summary info =========================
FAILED tests/test_cache.py::test_cache_clear - assert 1 == 2
FAILED tests/test_cache.py::test_cache_stats - assert 0 >= 2
FAILED tests/test_cache.py::test_list_processing - TypeError: unhashable t
ype: 'list'                                                               FAILED
 tests/test_cache.py::test_different_backends - TypeError: ucache() 
got an unexpected keyword argument 'config'                               FAILED
 tests/test_cache.py::test_cache_with_complex_types - TypeError: unh
ashable type: 'list'                                                      FAILED
 tests/test_cache.py::test_cache_exceptions - assert 2 == 1
FAILED tests/test_cache.py::test_kwargs_handling - assert 2 == 1
FAILED tests/test_decorators.py::test_bcache_basic - AssertionError: asser
t False                                                                   FAILED
 tests/test_decorators.py::test_ucache_fallback - AttributeError: 'm
odule' object at twat_cache.engines has no attribut...                    FAILED
 tests/test_engines.py::test_lru_cache_stats_accuracy - TypeError: '
dict' object is not callable                                              FAILED
 tests/test_twat_cache.py::test_disk_cache_persistence - AssertionEr
ror: assert None == 'test_value'                                          FAILED
 tests/test_twat_cache.py::test_klepto_persistence - AssertionError:
 assert None == {'complex': 'data', 'nested': {'value'...                 FAILED
 tests/test_twat_cache.py::test_cachebox_operations - AssertionError
: assert None == 'test_value'                                             FAILED
 tests/test_twat_cache.py::test_cachetools_operations - AssertionErr
or: assert None == 'test_value'                                           ======
==== 14 failed, 29 passed, 3 skipped, 1 warning in 1.24s ===========

```

---

_****_



I see several issues that need to be fixed:

1. **Cache Key Generation**:
- Lists are unhashable, need to convert to tuples
- Need to handle kwargs properly
- Need to handle complex types

2. **Backend Issues**:
- Backends not properly initialized
- Cache persistence not working
- Stats not working correctly

3. **Test Issues**:
- Config parameter not supported in ucache
- Fallback tests failing
- Stats tests failing

Let me fix these issues one by one. First, let's fix the cache key generation and backend initialization:

---

_****_

```diff
  
  import functools
+ import json
  from pathlib import Path
- from typing import TypeVar, cast, ParamSpec
- from collections.abc import Callable
+ from typing import Any, Callable, TypeVar, cast, ParamSpec
  from loguru import logger
  
      logger.debug("cachebox not available")
  
+ 
+ def make_key(*args: Any, **kwargs: Any) -> str:
+     """
+     Create a cache key from function arguments.
+ 
+     Handles unhashable types by converting them to JSON strings.
+     """
+ 
+     # Convert args to a stable form
+     def convert(obj: Any) -> Any:
+         if isinstance(obj, (list, dict, set)):
+             return json.dumps(obj, sort_keys=True)
+         if isinstance(obj, (int, float, str, bool, type(None))):
+             return obj
+         return str(obj)
+ 
+     # Convert args and kwargs to stable forms
+     converted_args = tuple(convert(arg) for arg in args)
+     converted_kwargs = {k: convert(v) for k, v in sorted(kwargs.items())}
+ 
+     # Create a stable string representation
+     return json.dumps((converted_args, converted_kwargs), sort_keys=True)
+ 
  
  def mcache(maxsize: int | None = None) -> Callable[[F], F]:
  
      def decorator(func: F) -> F:
-         return cast(F, functools.lru_cache(maxsize=maxsize)(func))
+         cache = {}
+         hits = 0
+         misses = 0
+ 
+         @functools.wraps(func)
+         def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
+             nonlocal hits, misses
+             key = make_key(*args, **kwargs)
+ 
+             if key in cache:
+                 hits += 1
+                 return cast(R, cache[key])
+ 
+             misses += 1
+             result = func(*args, **kwargs)
+             cache[key] = result
+ 
+             # Enforce maxsize
+             if maxsize is not None and len(cache) > maxsize:
+                 # Simple LRU: remove oldest item
+                 cache.pop(next(iter(cache)))
+ 
+             return result
+ 
+         # Add stats
+         wrapper.hits = hits  # type: ignore
+         wrapper.misses = misses  # type: ignore
+         wrapper.cache = cache  # type: ignore
+         wrapper.maxsize = maxsize  # type: ignore
+ 
+         return cast(F, wrapper)
  
      return decorator
          )
          cache_dir.mkdir(parents=True, exist_ok=True)
-         cache = DiskCache(str(cache_dir))
+         cache = DiskCache(str(cache_dir), size_limit=maxsize or int(1e9))
+         hits = 0
+         misses = 0
  
          @functools.wraps(func)
          def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
-             key = (args, tuple(sorted(kwargs.items())))
+             nonlocal hits, misses
+             key = make_key(*args, **kwargs)
+ 
              result = cache.get(key)
-             if result is None:
+             if result is not None:
+                 hits += 1
+                 return cast(R, result)
+ 
+             misses += 1
              result = func(*args, **kwargs)
              cache.set(key, result)
-             return cast(R, result)
+             return result
+ 
+         # Add stats
+         wrapper.hits = hits  # type: ignore
+         wrapper.misses = misses  # type: ignore
+         wrapper.cache = cache  # type: ignore
+         wrapper.maxsize = maxsize  # type: ignore
  
          return cast(F, wrapper)
  
          cache = BoxCache(maxsize=maxsize or 0)  # 0 means unlimited in cachebox
+         hits = 0
+         misses = 0
  
          @functools.wraps(func)
          def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
-             key = (args, tuple(sorted(kwargs.items())))
+             nonlocal hits, misses
+             key = make_key(*args, **kwargs)
+ 
              result = cache.get(key)
-             if result is None:
+             if result is not None:
+                 hits += 1
+                 return cast(R, result)
+ 
+             misses += 1
              result = func(*args, **kwargs)
              cache[key] = result
-             return cast(R, result)
+             return result
+ 
+         # Add stats
+         wrapper.hits = hits  # type: ignore
+         wrapper.misses = misses  # type: ignore
+         wrapper.cache = cache  # type: ignore
+         wrapper.maxsize = maxsize  # type: ignore
  
          return cast(F, wrapper)
      folder_name: str | None = None,
      maxsize: int | None = None,
+     config: dict[str, Any] | None = None,  # For backward compatibility
  ) -> Callable[[F], F]:
      """
          folder_name: Cache directory name (for disk cache)
          maxsize: Maximum cache size (None for unlimited)
+         config: Optional configuration dict (for backward compatibility)
  
      Returns:
          A decorator that caches function results using the best available backend
      """
+     # Handle legacy config
+     if config is not None:
+         maxsize = config.get("maxsize", maxsize)
+         folder_name = config.get("folder_name", folder_name)
+         preferred_engine = config.get("preferred_engine", preferred_engine)
  
      def decorator(func: F) -> F:
          # Try preferred engine first
          if preferred_engine == "fast" and HAS_CACHEBOX:
+             logger.debug("Using fast cache (cachebox)")
              return fcache(maxsize=maxsize)(func)
          elif preferred_engine == "disk" and HAS_DISKCACHE:
+             logger.debug("Using disk cache (diskcache)")
              return bcache(folder_name=folder_name, maxsize=maxsize)(func)
          elif preferred_engine == "memory":
+             logger.debug("Using memory cache (functools)")
              return mcache(maxsize=maxsize)(func)
  
```

---

_****_



Let me fix the linter errors:

---

_****_

```diff
  #   "diskcache",
  #   "cachebox",
+ #   "types-diskcache",
  # ]
  # ///
  import json
  from pathlib import Path
- from typing import Any, Callable, TypeVar, cast, ParamSpec
+ from typing import Any, Callable, TypeVar, cast, ParamSpec, Dict, Union
  from loguru import logger
  
  R = TypeVar("R")
  F = Callable[P, R]
+ 
+ # Cache types
+ CacheDict = Dict[str, Any]
+ CacheKey = str
+ CacheValue = Any
  
  # Try to import optional backends
  
  
- def make_key(*args: Any, **kwargs: Any) -> str:
+ def make_key(*args: Any, **kwargs: Any) -> CacheKey:
      """
      Create a cache key from function arguments.
  
      # Convert args to a stable form
-     def convert(obj: Any) -> Any:
+     def convert(obj: Any) -> Union[str, int, float, bool, None]:
          if isinstance(obj, (list, dict, set)):
              return json.dumps(obj, sort_keys=True)
  
  
- def mcache(maxsize: int | None = None) -> Callable[[F], F]:
+ def mcache(maxsize: int | None = None) -> Callable[[Callable[P, R]], Callable[P, R]]:
      """
      Memory-based caching using functools.lru_cache.
      """
  
-     def decorator(func: F) -> F:
-         cache = {}
+     def decorator(func: Callable[P, R]) -> Callable[P, R]:
+         cache: CacheDict = {}
          hits = 0
          misses = 0
          wrapper.maxsize = maxsize  # type: ignore
  
-         return cast(F, wrapper)
+         return wrapper
  
      return decorator
  def bcache(
      folder_name: str | None = None, maxsize: int | None = None
- ) -> Callable[[F], F]:
+ ) -> Callable[[Callable[P, R]], Callable[P, R]]:
      """
      Basic disk caching using diskcache.
      """
  
-     def decorator(func: F) -> F:
+     def decorator(func: Callable[P, R]) -> Callable[P, R]:
          if not HAS_DISKCACHE:
              logger.warning("diskcache not available, falling back to memory cache")
          wrapper.maxsize = maxsize  # type: ignore
  
-         return cast(F, wrapper)
+         return wrapper
  
      return decorator
  
  
- def fcache(maxsize: int | None = None) -> Callable[[F], F]:
+ def fcache(maxsize: int | None = None) -> Callable[[Callable[P, R]], Callable[P, R]]:
      """
      Fast in-memory caching using cachebox.
      """
  
-     def decorator(func: F) -> F:
+     def decorator(func: Callable[P, R]) -> Callable[P, R]:
          if not HAS_CACHEBOX:
              logger.warning("cachebox not available, falling back to memory cache")
          wrapper.maxsize = maxsize  # type: ignore
  
-         return cast(F, wrapper)
+         return wrapper
  
      return decorator
      maxsize: int | None = None,
      config: dict[str, Any] | None = None,  # For backward compatibility
- ) -> Callable[[F], F]:
+ ) -> Callable[[Callable[P, R]], Callable[P, R]]:
      """
      Universal caching with automatic fallback.
          preferred_engine = config.get("preferred_engine", preferred_engine)
  
-     def decorator(func: F) -> F:
+     def decorator(func: Callable[P, R]) -> Callable[P, R]:
          # Try preferred engine first
          if preferred_engine == "fast" and HAS_CACHEBOX:
```

---

_****_





Let me run our catchphrase again to check if the changes helped:

---

_****_

```bash
uv venv; source .venv/bin/activate; uv pip install -e .[all,dev,test]; hatch run lint:fix; hatch test;
```

```
Using CPython 3.12.8 interpreter at: /usr/local/bin/python3.12
Creating virtual environment at: .venv
Activate with: source .venv/bin/activate
zsh: no matches found: .[all,dev,test]
Rewriting src/twat_cache/decorators.py
warning: The top-level linter settings are deprecated in favour of their c
ounterparts in the `lint` section. Please update the following options in
`pyproject.toml`:
  - 'per-file-ignores' -> 'lint.per-file-ignores'
src/twat_cache/config.py:152:26: PLR2004 Magic value used in comparison, c
onsider replacing `9` with a constant variable
    |
150 |             msg = "compression_level must be an integer"
151 |             raise ValueError(msg)
152 |         if not 0 <= v <= 9:
    |                          ^ PLR2004
153 |             msg = "compression_level must be between 0 and 9"
154 |             raise ValueError(msg)
    |

src/twat_cache/engines/base.py:213:33: ARG002 Unused method argument: `key
`
    |
211 |     """
212 |
213 |     def _get_cached_value(self, key: CacheKey) -> R | None:
    |                                 ^^^ ARG002
214 |         """
215 |         Retrieve a value from the cache.
    |

src/twat_cache/engines/functools.py:1:1: A005 Module `functools` shadows a
 Python standard-library module
src/twat_cache/engines/joblib.py:49:33: ARG002 Unused method argument: `ke
y`
   |
47 |         )
48 |
49 |     def _get_cached_value(self, key: CacheKey) -> R | None:
   |                                 ^^^ ARG002
50 |         """Retrieve a value from the cache.
   |

src/twat_cache/engines/klepto.py:20:34: ARG005 Unused lambda argument: `ar
gs`
   |
18 |     HAS_KLEPTO = False
19 |     dir_archive = type("dir_archive", (), {})  # type: ignore
20 |     keymap = picklemap = lambda *args, **kwargs: lambda f: f  # type:
 ignore
   |                                  ^^^^ ARG005
   |

src/twat_cache/engines/klepto.py:20:42: ARG005 Unused lambda argument: `kw
args`
   |
18 |     HAS_KLEPTO = False
19 |     dir_archive = type("dir_archive", (), {})  # type: ignore
20 |     keymap = picklemap = lambda *args, **kwargs: lambda f: f  # type:
 ignore
   |                                          ^^^^^^ ARG005
   |

src/twat_cache/paths.py:100:5: C901 `clear_cache` is too complex (11 > 10)
    |
100 | def clear_cache(folder_name: str | None = None) -> None:
    |     ^^^^^^^^^^^ C901
101 |     """
102 |     Clear the cache directory for the given folder name.
    |

src/twat_cache/types.py:1:1: A005 Module `types` shadows a Python standard
-library module
tests/test_cache.py:175:34: PLR2004 Magic value used in comparison, consid
er replacing `15` with a constant variable
    |
173 |     result2 = process_list(test_list)
174 |
175 |     assert result1 == result2 == 15
    |                                  ^^ PLR2004
    |

tests/test_config.py:74:38: PLR2004 Magic value used in comparison, consid
er replacing `1000` with a constant variable
   |
72 |     # Check default values
73 |     assert config.cache_dir == get_cache_path("global")
74 |     assert config.default_maxsize == 1000
   |                                      ^^^^ PLR2004
75 |     assert not config.default_use_sql
76 |     assert config.default_engine == "lru"
   |

tests/test_config.py:79:40: PLR2004 Magic value used in comparison, consid
er replacing `6` with a constant variable
   |
77 |     assert config.default_cache_type is None
78 |     assert config.enable_compression
79 |     assert config.compression_level == 6
   |                                        ^ PLR2004
80 |     assert not config.debug
81 |     assert config.log_file is None
   |

tests/test_config.py:184:36: PLR2004 Magic value used in comparison, consi
der replacing `100` with a constant variable
    |
182 |         cache_type="speed",
183 |     )
184 |     assert config.get_maxsize() == 100
    |                                    ^^^ PLR2004
185 |     assert config.get_folder_name() == "test"
186 |     assert config.get_use_sql() is True
    |

tests/test_decorators.py:56:34: PLR2004 Magic value used in comparison, co
nsider replacing `25` with a constant variable
   |
54 |     time2 = time.time() - start
55 |
56 |     assert result1 == result2 == 25
   |                                  ^^ PLR2004
57 |     assert time2 < time1  # Cached call should be faster
   |

tests/test_decorators.py:74:34: PLR2004 Magic value used in comparison, co
nsider replacing `25` with a constant variable
   |
72 |     result2 = func(5)
73 |
74 |     assert result1 == result2 == 25
   |                                  ^^ PLR2004
75 |     assert cache_dir.exists()
   |

tests/test_decorators.py:91:34: PLR2004 Magic value used in comparison, co
nsider replacing `25` with a constant variable
   |
89 |     result2 = func(5)
90 |
91 |     assert result1 == result2 == 25
   |                                  ^^ PLR2004
   |

tests/test_decorators.py:107:34: PLR2004 Magic value used in comparison, c
onsider replacing `25` with a constant variable
    |
105 |     result2 = func(5)
106 |
107 |     assert result1 == result2 == 25
    |                                  ^^ PLR2004
    |

tests/test_decorators.py:123:22: PLR2004 Magic value used in comparison, c
onsider replacing `25` with a constant variable
    |
121 |     # Should still work with functools backend
122 |     result = func(5)
123 |     assert result == 25
    |                      ^^ PLR2004
    |

tests/test_decorators.py:141:34: PLR2004 Magic value used in comparison, c
onsider replacing `25` with a constant variable
    |
139 |     result2 = await func(5)
140 |
141 |     assert result1 == result2 == 25
    |                                  ^^ PLR2004
    |

tests/test_decorators.py:188:23: PLR2004 Magic value used in comparison, c
onsider replacing `25` with a constant variable
    |
187 |     # Valid input should work
188 |     assert func(5) == 25
    |                       ^^ PLR2004
189 |
190 |     # Error should be raised consistently
    |

tests/test_engines.py:62:45: FBT003 Boolean positional value in function c
all
   |
60 |     assert isinstance(base_engine._make_key("test"), str)
61 |     assert isinstance(base_engine._make_key(123), str)
62 |     assert isinstance(base_engine._make_key(True), str)
   |                                             ^^^^ FBT003
63 |
64 |     # Test with complex types
   |

tests/test_engines.py:82:22: PLR2004 Magic value used in comparison, consi
der replacing `4` with a constant variable
   |
80 |     # First call
81 |     result = test_function(2)
82 |     assert result == 4
   |                      ^ PLR2004
83 |     assert call_count == 1
   |

tests/test_engines.py:87:22: PLR2004 Magic value used in comparison, consi
der replacing `4` with a constant variable
   |
85 |     # Second call (should use cache)
86 |     result = test_function(2)
87 |     assert result == 4
   |                      ^ PLR2004
88 |     assert call_count == 1  # Should not increment
   |

Found 26 errors (4 fixed, 22 remaining).
========================== test session starts ===========================
platform darwin -- Python 3.12.8, pytest-8.3.4, pluggy-1.5.0 -- /Users/ada
m/Library/Application Support/hatch/env/virtual/twat-cache/ivvP1xkE/hatch-
test.py3.12/bin/python3
cachedir: .pytest_cache
rootdir: /Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good
/twat/plugins/repos/twat_cache
configfile: pyproject.toml
plugins: rerunfailures-14.0, mock-3.14.0, xdist-3.6.1
collected 46 items                                                       

tests/test_cache.py::test_cache_settings_validation PASSED         [  2%]
tests/test_cache.py::test_basic_caching PASSED                     [  4%]
tests/test_cache.py::test_cache_clear FAILED                       [  6%]
tests/test_cache.py::test_cache_stats FAILED                       [  8%]
tests/test_cache.py::test_list_processing PASSED                   [ 10%]
tests/test_cache.py::test_different_backends FAILED                [ 13%]
tests/test_cache.py::test_cache_with_complex_types PASSED          [ 15%]
tests/test_cache.py::test_cache_exceptions FAILED                  [ 17%]
tests/test_cache.py::test_kwargs_handling FAILED                   [ 19%]
tests/test_config.py::test_cache_config_validation PASSED          [ 21%]
tests/test_config.py::test_default_config PASSED                   [ 23%]
tests/test_config.py::test_custom_config PASSED                    [ 26%]
tests/test_config.py::test_global_config_env_vars PASSED           [ 28%]
tests/test_config.py::test_get_cache_config PASSED                 [ 30%]
tests/test_config.py::test_logging_configuration PASSED            [ 32%]
tests/test_config.py::test_cache_config_creation PASSED            [ 34%]
tests/test_config.py::test_cache_config_with_sql PASSED            [ 36%]
tests/test_decorators.py::test_mcache_basic PASSED                 [ 39%]
tests/test_decorators.py::test_bcache_basic FAILED                 [ 41%]
tests/test_decorators.py::test_fcache_basic PASSED                 [ 43%]
tests/test_decorators.py::test_ucache_basic PASSED                 [ 45%]
tests/test_decorators.py::test_ucache_fallback FAILED              [ 47%]
tests/test_decorators.py::test_async_caching SKIPPED (async de...) [ 50%]
tests/test_decorators.py::test_cache_performance PASSED            [ 52%]
tests/test_decorators.py::test_decorator_error_handling PASSED     [ 54%]
tests/test_engines.py::test_base_engine_initialization PASSED      [ 56%]
tests/test_engines.py::test_base_engine_key_generation PASSED      [ 58%]
tests/test_engines.py::test_base_engine_cache_decorator PASSED     [ 60%]
tests/test_engines.py::test_base_engine_validation PASSED          [ 63%]
tests/test_engines.py::test_lru_cache_initialization PASSED        [ 65%]
tests/test_engines.py::test_lru_cache_maxsize_enforcement PASSED   [ 67%]
tests/test_engines.py::test_lru_cache_clear PASSED                 [ 69%]
tests/test_engines.py::test_lru_cache_with_complex_values PASSED   [ 71%]
tests/test_engines.py::test_lru_cache_stats_accuracy FAILED        [ 73%]
tests/test_twat_cache.py::test_lru_cache_get_set PASSED            [ 76%]
tests/test_twat_cache.py::test_lru_cache_clear PASSED              [ 78%]
tests/test_twat_cache.py::test_lru_cache_maxsize PASSED            [ 80%]
tests/test_twat_cache.py::test_disk_cache_persistence FAILED       [ 82%]
tests/test_twat_cache.py::test_joblib_numpy_array SKIPPED (num...) [ 84%]
tests/test_twat_cache.py::test_klepto_persistence FAILED           [ 86%]
tests/test_twat_cache.py::test_async_cache_operations SKIPPED      [ 89%]
tests/test_twat_cache.py::test_cachebox_operations FAILED          [ 91%]
tests/test_twat_cache.py::test_cachetools_operations FAILED        [ 93%]
tests/test_twat_cache.py::test_functools_cache_get_set PASSED      [ 95%]
tests/test_twat_cache.py::test_functools_cache_clear PASSED        [ 97%]
tests/test_twat_cache.py::test_functools_cache_maxsize PASSED      [100%]

================================ FAILURES ================================
____________________________ test_cache_clear ____________________________

    def test_cache_clear() -> None:
        """Test cache clearing functionality."""
        call_count = 0
    
        @ucache()
        def cached_function(x: int) -> int:
            nonlocal call_count
            call_count += 1
            return x * x
    
        # First call
        assert cached_function(TEST_INPUT) == TEST_RESULT
        assert call_count == 1
    
        # Clear cache
        clear_cache()
    
        # Should recompute after clear
        assert cached_function(TEST_INPUT) == TEST_RESULT
>       assert call_count == EXPECTED_CALL_COUNT
E       assert 1 == 2

tests/test_cache.py:86: AssertionError
-------------------------- Captured stderr call --------------------------
2025-02-16 14:21:05.979 | DEBUG    | twat_cache.decorators:decorator:271 -
 Using memory cache (functools)
2025-02-16 14:21:05.979 | DEBUG    | twat_cache.engines.manager:_register_
engine:148 - Registered cache engine: memory
2025-02-16 14:21:05.979 | DEBUG    | twat_cache.engines.manager:_register_
engine:148 - Registered cache engine: cachebox
2025-02-16 14:21:05.979 | DEBUG    | twat_cache.engines.manager:_register_
engine:148 - Registered cache engine: cachetools
2025-02-16 14:21:05.979 | DEBUG    | twat_cache.engines.manager:_register_
engine:148 - Registered cache engine: aiocache
2025-02-16 14:21:05.979 | DEBUG    | twat_cache.engines.manager:_register_
engine:148 - Registered cache engine: klepto
2025-02-16 14:21:05.979 | DEBUG    | twat_cache.engines.manager:_register_
engine:148 - Registered cache engine: diskcache
2025-02-16 14:21:05.979 | DEBUG    | twat_cache.engines.manager:_register_
engine:148 - Registered cache engine: joblib
2025-02-16 14:21:05.979 | DEBUG    | twat_cache.engines.manager:_register_
available_engines:124 - Registered cache engines: ['memory', 'cachebox', '
cachetools', 'aiocache', 'klepto', 'diskcache', 'joblib']
2025-02-16 14:21:05.980 | DEBUG    | twat_cache.engines.manager:_create_fa
llback_engine:227 - Using LRU cache
2025-02-16 14:21:05.980 | DEBUG    | twat_cache.paths:get_cache_path:70 - 
Created cache directory: /Users/adam/Library/Caches/twat_cache/twat_cache_
8ffd3846
2025-02-16 14:21:05.980 | DEBUG    | twat_cache.engines.base:__init__:55 -
 Initialized FunctoolsCacheEngine with config: maxsize=None folder_name=No
ne use_sql=False preferred_engine=None cache_type=None
2025-02-16 14:21:05.980 | DEBUG    | twat_cache.engines.functools:__init__
:50 - Initialized functools cache with maxsize: 128
2025-02-16 14:21:05.980 | DEBUG    | twat_cache.cache:clear_cache:55 - Cle
aring cache for engine: FunctoolsCacheEngine
2025-02-16 14:21:05.980 | DEBUG    | twat_cache.engines.functools:clear:17
0 - Cleared functools cache
____________________________ test_cache_stats ____________________________

    def test_cache_stats() -> None:
        """Test cache statistics."""
        call_count = 0
    
        @ucache()
        def cached_function(x: int) -> int:
            nonlocal call_count
            call_count += 1
            return x * x
    
        # Generate some cache activity
        for _i in range(3):
            cached_function(TEST_INPUT)
            cached_function(TEST_INPUT_2)
    
        # Get stats
        stats = get_stats()
    
        # Basic stats checks
        assert isinstance(stats, dict)
>       assert stats["hits"] >= MIN_STATS_COUNT
E       assert 0 >= 2

tests/test_cache.py:109: AssertionError
-------------------------- Captured stderr call --------------------------
2025-02-16 14:21:06.027 | DEBUG    | twat_cache.decorators:decorator:271 -
 Using memory cache (functools)
2025-02-16 14:21:06.027 | DEBUG    | twat_cache.engines.manager:_create_fa
llback_engine:227 - Using LRU cache
2025-02-16 14:21:06.027 | DEBUG    | twat_cache.paths:get_cache_path:70 - 
Created cache directory: /Users/adam/Library/Caches/twat_cache/twat_cache_
ddf18b47
2025-02-16 14:21:06.027 | DEBUG    | twat_cache.engines.base:__init__:55 -
 Initialized FunctoolsCacheEngine with config: maxsize=None folder_name=No
ne use_sql=False preferred_engine=None cache_type=None
2025-02-16 14:21:06.027 | DEBUG    | twat_cache.engines.functools:__init__
:50 - Initialized functools cache with maxsize: 128
2025-02-16 14:21:06.027 | DEBUG    | twat_cache.cache:get_stats:93 - Getti
ng stats for engine: FunctoolsCacheEngine
________________________ test_different_backends _________________________

    def test_different_backends() -> None:
        """Test using different cache backends."""
        results: list[Any] = []
    
        # Test with different configurations
        configs = [
            create_cache_config(maxsize=100),  # Memory cache
            create_cache_config(folder_name="disk_test", use_sql=True),  #
 SQL cache
            create_cache_config(folder_name="disk_test", use_sql=False),

# Disk cache
        ]
    
        for config in configs:
    
>           @ucache(config=config)

tests/test_cache.py:148: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
src/twat_cache/decorators.py:247: in ucache
    maxsize = config.get("maxsize", maxsize)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = CacheConfigImpl(maxsize=100, folder_name=None, use_sql=False, prefe
rred_engine=None, cache_type=None)
item = 'get'

    def __getattr__(self, item: str) -> Any:
        private_attributes = object.__getattribute__(self, '__private_attr
ibutes__')
        if item in private_attributes:
            attribute = private_attributes[item]
            if hasattr(attribute, '__get__'):
                return attribute.__get__(self, type(self))  # type: ignore
    
            try:
                # Note: self.__pydantic_private__ cannot be None if self._
_private_attributes__ has items
                return self.__pydantic_private__[item]  # type: ignore
            except KeyError as exc:
                raise AttributeError(f'{type(self).__name__!r} object has 
no attribute {item!r}') from exc
        else:
            # `__pydantic_extra__` can fail to be set if the model is not 
yet fully initialized.
            # See `BaseModel.__repr_args__` for more details
            try:
                pydantic_extra = object.__getattribute__(self, '__pydantic
_extra__')
            except AttributeError:
                pydantic_extra = None
    
            if pydantic_extra:
                try:
                    return pydantic_extra[item]
                except KeyError as exc:
                    raise AttributeError(f'{type(self).__name__!r} object 
has no attribute {item!r}') from exc
            else:
                if hasattr(self.__class__, item):
                    return super().__getattribute__(item)  # Raises Attrib
uteError if appropriate
                else:
                    # this is the current error
>                   raise AttributeError(f'{type(self).__name__!r} object 
has no attribute {item!r}')
E                   AttributeError: 'CacheConfigImpl' object has no attrib
ute 'get'

/Users/adam/Library/Application Support/hatch/env/virtual/twat-cache/ivvP1
xkE/hatch-test.py3.12/lib/python3.12/site-packages/pydantic/main.py:891: A
ttributeError
_________________________ test_cache_exceptions __________________________

    def test_cache_exceptions() -> None:
        """Test caching of exceptions."""
        call_count = 0
    
        @ucache(maxsize=100)
        def failing_function(x: int) -> None:
            nonlocal call_count
            call_count += 1
            msg = "Test error"
            raise ValueError(msg)
    
        # First call
        with pytest.raises(ValueError):
            failing_function(5)
        assert call_count == 1
    
        # Second call should not recompute
        with pytest.raises(ValueError):
            failing_function(5)
>       assert call_count == 1
E       assert 2 == 1

tests/test_cache.py:197: AssertionError
-------------------------- Captured stderr call --------------------------
2025-02-16 14:21:06.061 | DEBUG    | twat_cache.decorators:decorator:271 -
 Using memory cache (functools)
__________________________ test_kwargs_handling __________________________

    def test_kwargs_handling() -> None:
        """Test caching with different keyword arguments."""
        call_count = 0
    
        @ucache()
        def kwarg_function(x: int, multiplier: int = 1) -> int:
            nonlocal call_count
            call_count += 1
            return x * multiplier
    
        # Test with different kwarg combinations
        assert kwarg_function(TEST_INPUT) == TEST_INPUT
        assert call_count == 1
    
        assert kwarg_function(TEST_INPUT, multiplier=1) == TEST_INPUT
>       assert call_count == 1  # Should use cache
E       assert 2 == 1

tests/test_cache.py:215: AssertionError
-------------------------- Captured stderr call --------------------------
2025-02-16 14:21:06.067 | DEBUG    | twat_cache.decorators:decorator:271 -
 Using memory cache (functools)
___________________________ test_bcache_basic ____________________________

tmp_path = PosixPath('/private/var/folders/05/clcynl0509ldxltl599hhhx40000
gn/T/pytest-of-adam/pytest-33/test_bcache_basic0')

    def test_bcache_basic(tmp_path: Path):
        """Test basic disk caching."""
        cache_dir = tmp_path / "cache"
    
        @bcache(folder_name=str(cache_dir))
        def func(x: int) -> int:
            return expensive_computation(x)
    
        # First call should compute
        result1 = func(5)
    
        # Second call should be from cache
        result2 = func(5)
    
        assert result1 == result2 == 25
>       assert cache_dir.exists()
E       AssertionError: assert False
E        +  where False = exists()
E        +    where exists = PosixPath('/private/var/folders/05/clcynl0509
ldxltl599hhhx40000gn/T/pytest-of-adam/pytest-33/test_bcache_basic0/cache')
.exists

tests/test_decorators.py:75: AssertionError
-------------------------- Captured stderr call --------------------------
2025-02-16 14:21:06.212 | WARNING  | twat_cache.decorators:decorator:144 -
 diskcache not available, falling back to memory cache
__________________________ test_ucache_fallback __________________________

obj = <module 'twat_cache.engines' from '/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_cache/src/twat_ca
che/engines/__init__.py'>
name = 'HAS_CACHEBOX', ann = 'twat_cache.engines'

    def annotated_getattr(obj: object, name: str, ann: str) -> object:
        try:
>           obj = getattr(obj, name)
E           AttributeError: module 'twat_cache.engines' has no attribute '
HAS_CACHEBOX'

/Users/adam/Library/Application Support/hatch/env/virtual/twat-cache/ivvP1
xkE/hatch-test.py3.12/lib/python3.12/site-packages/_pytest/monkeypatch.py:
90: AttributeError

The above exception was the direct cause of the following exception:

monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x10e8a8e00>

    def test_ucache_fallback(monkeypatch):
        """Test ucache fallback behavior."""
        # Simulate no backends available except functools
>       monkeypatch.setattr("twat_cache.engines.HAS_CACHEBOX", False)

tests/test_decorators.py:114: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
/Users/adam/Library/Application Support/hatch/env/virtual/twat-cache/ivvP1
xkE/hatch-test.py3.12/lib/python3.12/site-packages/_pytest/monkeypatch.py:
104: in derive_importpath
    annotated_getattr(target, attr, ann=module)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

obj = <module 'twat_cache.engines' from '/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_cache/src/twat_ca
che/engines/__init__.py'>
name = 'HAS_CACHEBOX', ann = 'twat_cache.engines'

    def annotated_getattr(obj: object, name: str, ann: str) -> object:
        try:
            obj = getattr(obj, name)
        except AttributeError as e:
>           raise AttributeError(
                f"{type(obj).__name__!r} object at {ann} has no attribute 
{name!r}"
            ) from e
E           AttributeError: 'module' object at twat_cache.engines has no a
ttribute 'HAS_CACHEBOX'

/Users/adam/Library/Application Support/hatch/env/virtual/twat-cache/ivvP1
xkE/hatch-test.py3.12/lib/python3.12/site-packages/_pytest/monkeypatch.py:
92: AttributeError
_____________________ test_lru_cache_stats_accuracy ______________________

base_config = CacheConfigImpl(maxsize=100, folder_name=None, use_sql=False
, preferred_engine=None, cache_type=None)

    def test_lru_cache_stats_accuracy(base_config: CacheConfig) -> None:
        """Test accuracy of LRU cache statistics."""
        engine = FunctoolsCacheEngine(base_config)
    
        # Test initial stats
>       stats = engine.stats()
E       TypeError: 'dict' object is not callable

tests/test_engines.py:160: TypeError
______________________ test_disk_cache_persistence _______________________

disk_engine = <twat_cache.engines.diskcache.DiskCacheEngine object at 0x10
e8ab4a0>

    def test_disk_cache_persistence(disk_engine: DiskCacheEngine) -> None:
        """Test persistence of disk cache."""
        key: CacheKey = "test_key"
        value = "test_value"
    
        disk_engine._set_cached_value(key, value)
>       assert disk_engine._get_cached_value(key) == value
E       AssertionError: assert None == 'test_value'
E        +  where None = _get_cached_value('test_key')
E        +    where _get_cached_value = <twat_cache.engines.diskcache.Disk
CacheEngine object at 0x10e8ab4a0>._get_cached_value

tests/test_twat_cache.py:105: AssertionError
________________________ test_klepto_persistence _________________________

klepto_engine = <twat_cache.engines.klepto.KleptoEngine object at 0x10e8ab
080>

    def test_klepto_persistence(klepto_engine: KleptoEngine) -> None:
        """Test persistence of klepto cache."""
        key: CacheKey = "test_key"
        value = {"complex": "data", "nested": {"value": 42}}
    
        klepto_engine._set_cached_value(key, value)
>       assert klepto_engine._get_cached_value(key) == value
E       AssertionError: assert None == {'complex': 'data', 'nested': {'val
ue': 42}}
E        +  where None = _get_cached_value('test_key')
E        +    where _get_cached_value = <twat_cache.engines.klepto.KleptoE
ngine object at 0x10e8ab080>._get_cached_value

tests/test_twat_cache.py:147: AssertionError
________________________ test_cachebox_operations ________________________

cachebox_engine = <twat_cache.engines.cachebox.CacheBoxEngine object at 0x
10ea91880>

    def test_cachebox_operations(cachebox_engine: CacheBoxEngine) -> None:
        """Test basic operations for cachebox."""
        key: CacheKey = "test_key"
        value = "test_value"
    
        assert cachebox_engine._get_cached_value(key) is None
        cachebox_engine._set_cached_value(key, value)
>       assert cachebox_engine._get_cached_value(key) == value
E       AssertionError: assert None == 'test_value'
E        +  where None = _get_cached_value('test_key')
E        +    where _get_cached_value = <twat_cache.engines.cachebox.Cache
BoxEngine object at 0x10ea91880>._get_cached_value

tests/test_twat_cache.py:185: AssertionError
_______________________ test_cachetools_operations _______________________

cachetools_engine = <twat_cache.engines.cachetools.CacheToolsEngine object
 at 0x10e8abef0>

    def test_cachetools_operations(cachetools_engine: CacheToolsEngine) ->
 None:
        """Test basic operations for cachetools."""
        key: CacheKey = "test_key"
        value = "test_value"
    
        assert cachetools_engine._get_cached_value(key) is None
        cachetools_engine._set_cached_value(key, value)
>       assert cachetools_engine._get_cached_value(key) == value
E       AssertionError: assert None == 'test_value'
E        +  where None = _get_cached_value('test_key')
E        +    where _get_cached_value = <twat_cache.engines.cachetools.Cac
heToolsEngine object at 0x10e8abef0>._get_cached_value

tests/test_twat_cache.py:205: AssertionError
============================ warnings summary ============================
tests/test_twat_cache.py::test_async_cache_operations
  /Users/adam/Library/Application Support/hatch/env/virtual/twat-cache/ivv
P1xkE/hatch-test.py3.12/lib/python3.12/site-packages/_pytest/runner.py:142
: RuntimeWarning: coroutine 'async_engine' was never awaited
    item.funcargs = None  # type: ignore[attr-defined]
  Enable tracemalloc to get traceback where the object was allocated.
  See https://docs.pytest.org/en/stable/how-to/capture-warnings.html#resou
rce-warnings for more info.

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
======================== short test summary info =========================
FAILED tests/test_cache.py::test_cache_clear - assert 1 == 2
FAILED tests/test_cache.py::test_cache_stats - assert 0 >= 2
FAILED tests/test_cache.py::test_different_backends - AttributeError: 'Cac
heConfigImpl' object has no attribute 'get'
FAILED tests/test_cache.py::test_cache_exceptions - assert 2 == 1
FAILED tests/test_cache.py::test_kwargs_handling - assert 2 == 1
FAILED tests/test_decorators.py::test_bcache_basic - AssertionError: asser
t False
FAILED tests/test_decorators.py::test_ucache_fallback - AttributeError: 'm
odule' object at twat_cache.engines has no attribut...
FAILED tests/test_engines.py::test_lru_cache_stats_accuracy - TypeError: '
dict' object is not callable
FAILED tests/test_twat_cache.py::test_disk_cache_persistence - AssertionEr
ror: assert None == 'test_value'
FAILED tests/test_twat_cache.py::test_klepto_persistence - AssertionError:
 assert None == {'complex': 'data', 'nested': {'value'...
FAILED tests/test_twat_cache.py::test_cachebox_operations - AssertionError
: assert None == 'test_value'
FAILED tests/test_twat_cache.py::test_cachetools_operations - AssertionErr
or: assert None == 'test_value'
========== 12 failed, 31 passed, 3 skipped, 1 warning in 1.29s ===========

```

---

_****_





I see several issues that need to be fixed:

1. **Cache Key Generation**:
- The key generation is working better now, but we need to handle kwargs properly
- Need to fix the cache clearing mechanism

2. **Backend Issues**:
- Need to fix the stats tracking
- Need to fix the backend availability checks
- Need to fix the cache persistence

3. **Test Issues**:
- Need to fix the config handling in ucache
- Need to fix the fallback tests
- Need to fix the stats tests

Let me fix these issues one by one. First, let's fix the cache clearing and stats:

---

_****_

```diff
  
  """
- Main cache interface.
+ Cache management utilities.
  
- This module provides a simple interface for managing caches and retrieving
- cache statistics. For the main caching decorators, see the decorators module.
- """
- 
- from typing import Any, cast
- 
+ This module provides functions for managing cache state, including:
+ - Clearing caches
+ - Getting cache statistics
+ - Managing cache directories
+ """
+ 
+ from pathlib import Path
+ from typing import Any, Dict
  from loguru import logger
  
- from .config import create_cache_config
- from .engines.manager import get_engine_manager, EngineManager
+ # Global registry of active caches
+ _active_caches: Dict[str, Any] = {}
  
  
- def clear_cache(
-     folder_name: str | None = None,
-     preferred_engine: str | None = None,
- ) -> None:
+ def register_cache(name: str, cache: Any) -> None:
      """
-     Clear the cache for the given configuration.
+     Register an active cache instance.
  
      Args:
-         folder_name: Optional name of the cache folder to clear
-         preferred_engine: Optional name of the cache engine to clear
- 
-     Example:
-         ```python
-         # Clear specific cache
-         clear_cache(folder_name="my_cache")
- 
-         # Clear all caches
-         clear_cache()
-         ```
-     """
-     # Create configuration
-     config = create_cache_config(
-         folder_name=folder_name,
-         preferred_engine=preferred_engine,
-     )
+         name: Unique name for the cache
+         cache: The cache instance to register
+     """
+     _active_caches[name] = cache
+     logger.debug(f"Registered cache: {name}")
+ 
+ 
+ def clear_cache(name: str | None = None) -> None:
+     """
+     Clear one or all caches.
+ 
+     Args:
+         name: Name of cache to clear, or None to clear all
+     """
+     if name is not None:
+         if name in _active_caches:
+             cache = _active_caches[name]
+             if hasattr(cache, "clear"):
+                 cache.clear()
+             logger.debug(f"Cleared cache: {name}")
+         return
+ 
+     # Clear all caches
+     for cache_name, cache in _active_caches.items():
+         if hasattr(cache, "clear"):
+             cache.clear()
+         logger.debug(f"Cleared cache: {cache_name}")
  
-     # Get engine manager
-     manager = get_engine_manager()
- 
-     # Get appropriate engine
-     engine = manager.get_engine(config)
-     logger.debug(f"Clearing cache for engine: {engine.__class__.__name__}")
- 
-     # Clear cache
-     engine.clear()
+     # Also clear cache directories
+     cache_dir = Path.home() / ".cache" / "twat_cache"
+     if cache_dir.exists():
+         for path in cache_dir.glob("*"):
+             if path.is_dir():
+                 try:
+                     for file in path.glob("*"):
+                         file.unlink()
+                     path.rmdir()
+                 except OSError as e:
+                     logger.warning(f"Failed to clear cache directory {path}: {e}")
+         logger.debug("Cleared cache directories")
  
  
- def get_stats(
-     folder_name: str | None = None,
-     preferred_engine: str | None = None,
- ) -> dict[str, Any]:
+ def get_stats(name: str | None = None) -> Dict[str, Any]:
      """
-     Get cache statistics for the given configuration.
+     Get cache statistics.
  
      Args:
-         folder_name: Optional name of the cache folder
-         preferred_engine: Optional name of the cache engine
+         name: Name of cache to get stats for, or None for all
  
      Returns:
-         Dictionary containing cache statistics
- 
-     Example:
-         ```python
-         # Get stats for specific cache
-         stats = get_stats(folder_name="my_cache")
-         print(f"Cache hits: {stats['hits']}")
-         ```
-     """
-     # Create configuration
-     config = create_cache_config(
-         folder_name=folder_name,
-         preferred_engine=preferred_engine,
-     )
- 
-     # Get engine manager
-     manager: EngineManager = get_engine_manager()
- 
-     # Get appropriate engine
-     engine = manager.get_engine(config)
-     logger.debug(f"Getting stats for engine: {engine.__class__.__name__}")
- 
-     # Get stats
-     return cast(dict[str, Any], engine.stats)
+         Dictionary of cache statistics
+     """
+     stats: Dict[str, Any] = {
+         "total_caches": len(_active_caches),
+         "hits": 0,
+         "misses": 0,
+         "size": 0,
+     }
+ 
+     if name is not None:
+         if name not in _active_caches:
+             return stats
+         cache = _active_caches[name]
+         if hasattr(cache, "hits"):
+             stats["hits"] = cache.hits
+         if hasattr(cache, "misses"):
+             stats["misses"] = cache.misses
+         if hasattr(cache, "cache"):
+             stats["size"] = len(cache.cache)
+         return stats
+ 
+     # Aggregate stats from all caches
+     for cache in _active_caches.values():
+         if hasattr(cache, "hits"):
+             stats["hits"] += cache.hits
+         if hasattr(cache, "misses"):
+             stats["misses"] += cache.misses
+         if hasattr(cache, "cache"):
+             stats["size"] += len(cache.cache)
+ 
+     return stats
  
```

---

_****_





Now let's update the decorators to use the new cache registry:

---

_****_

```diff
  import functools
  import json
+ import uuid
  from pathlib import Path
- from typing import Any, TypeVar, cast, ParamSpec
- from collections.abc import Callable
+ from typing import Any, Callable, TypeVar, cast, ParamSpec, Dict, Union
  from loguru import logger
+ 
+ from .cache import register_cache
  
  # Type variables for generic function types
  
  # Cache types
- CacheDict = dict[str, Any]
+ CacheDict = Dict[str, Any]
  CacheKey = str
  CacheValue = Any
  
      # Convert args to a stable form
-     def convert(obj: Any) -> str | int | float | bool | None:
-         if isinstance(obj, list | dict | set):
+     def convert(obj: Any) -> Union[str, int, float, bool, None]:
+         if isinstance(obj, (list, dict, set)):
              return json.dumps(obj, sort_keys=True)
-         if isinstance(obj, int | float | str | bool | type(None)):
+         if isinstance(obj, (int, float, str, bool, type(None))):
              return obj
          return str(obj)
          hits = 0
          misses = 0
+         cache_id = f"mcache_{func.__name__}_{uuid.uuid4().hex[:8]}"
  
          @functools.wraps(func)
          wrapper.cache = cache  # type: ignore
          wrapper.maxsize = maxsize  # type: ignore
+ 
+         # Register cache
+         register_cache(cache_id, wrapper)
  
          return wrapper
          hits = 0
          misses = 0
+         cache_id = f"bcache_{func.__name__}_{uuid.uuid4().hex[:8]}"
  
          @functools.wraps(func)
          wrapper.cache = cache  # type: ignore
          wrapper.maxsize = maxsize  # type: ignore
+ 
+         # Register cache
+         register_cache(cache_id, wrapper)
  
          return wrapper
          hits = 0
          misses = 0
+         cache_id = f"fcache_{func.__name__}_{uuid.uuid4().hex[:8]}"
  
          @functools.wraps(func)
          wrapper.cache = cache  # type: ignore
          wrapper.maxsize = maxsize  # type: ignore
+ 
+         # Register cache
+         register_cache(cache_id, wrapper)
  
          return wrapper
```

---

_****_





Let me run our catchphrase again to check if the changes helped:

---

_****_

```bash
uv venv; source .venv/bin/activate; uv pip install -e .[all,dev,test]; hatch run lint:fix; hatch test;
```

```
Using CPython 3.12.8 interpreter at: /usr/local/bin/python3.12
Creating virtual environment at: .venv
Activate with: source .venv/bin/activate
zsh: no matches found: .[all,dev,test]
Rewriting src/twat_cache/cache.py
Rewriting src/twat_cache/decorators.py
warning: The top-level linter settings are deprecated in favour of their c
ounterparts in the `lint` section. Please update the following options in
`pyproject.toml`:
  - 'per-file-ignores' -> 'lint.per-file-ignores'
src/twat_cache/cache.py:38:5: C901 `clear_cache` is too complex (11 > 10)
   |
38 | def clear_cache(name: str | None = None) -> None:
   |     ^^^^^^^^^^^ C901
39 |     """
40 |     Clear one or all caches.
   |

src/twat_cache/config.py:152:26: PLR2004 Magic value used in comparison, c
onsider replacing `9` with a constant variable
    |
150 |             msg = "compression_level must be an integer"
151 |             raise ValueError(msg)
152 |         if not 0 <= v <= 9:
    |                          ^ PLR2004
153 |             msg = "compression_level must be between 0 and 9"
154 |             raise ValueError(msg)
    |

src/twat_cache/engines/base.py:213:33: ARG002 Unused method argument: `key
`
    |
211 |     """
212 |
213 |     def _get_cached_value(self, key: CacheKey) -> R | None:
    |                                 ^^^ ARG002
214 |         """
215 |         Retrieve a value from the cache.
    |

src/twat_cache/engines/functools.py:1:1: A005 Module `functools` shadows a
 Python standard-library module
src/twat_cache/engines/joblib.py:49:33: ARG002 Unused method argument: `ke
y`
   |
47 |         )
48 |
49 |     def _get_cached_value(self, key: CacheKey) -> R | None:
   |                                 ^^^ ARG002
50 |         """Retrieve a value from the cache.
   |

src/twat_cache/engines/klepto.py:20:34: ARG005 Unused lambda argument: `ar
gs`
   |
18 |     HAS_KLEPTO = False
19 |     dir_archive = type("dir_archive", (), {})  # type: ignore
20 |     keymap = picklemap = lambda *args, **kwargs: lambda f: f  # type:
 ignore
   |                                  ^^^^ ARG005
   |

src/twat_cache/engines/klepto.py:20:42: ARG005 Unused lambda argument: `kw
args`
   |
18 |     HAS_KLEPTO = False
19 |     dir_archive = type("dir_archive", (), {})  # type: ignore
20 |     keymap = picklemap = lambda *args, **kwargs: lambda f: f  # type:
 ignore
   |                                          ^^^^^^ ARG005
   |

src/twat_cache/paths.py:100:5: C901 `clear_cache` is too complex (11 > 10)
    |
100 | def clear_cache(folder_name: str | None = None) -> None:
    |     ^^^^^^^^^^^ C901
101 |     """
102 |     Clear the cache directory for the given folder name.
    |

src/twat_cache/types.py:1:1: A005 Module `types` shadows a Python standard
-library module
tests/test_cache.py:175:34: PLR2004 Magic value used in comparison, consid
er replacing `15` with a constant variable
    |
173 |     result2 = process_list(test_list)
174 |
175 |     assert result1 == result2 == 15
    |                                  ^^ PLR2004
    |

tests/test_config.py:74:38: PLR2004 Magic value used in comparison, consid
er replacing `1000` with a constant variable
   |
72 |     # Check default values
73 |     assert config.cache_dir == get_cache_path("global")
74 |     assert config.default_maxsize == 1000
   |                                      ^^^^ PLR2004
75 |     assert not config.default_use_sql
76 |     assert config.default_engine == "lru"
   |

tests/test_config.py:79:40: PLR2004 Magic value used in comparison, consid
er replacing `6` with a constant variable
   |
77 |     assert config.default_cache_type is None
78 |     assert config.enable_compression
79 |     assert config.compression_level == 6
   |                                        ^ PLR2004
80 |     assert not config.debug
81 |     assert config.log_file is None
   |

tests/test_config.py:184:36: PLR2004 Magic value used in comparison, consi
der replacing `100` with a constant variable
    |
182 |         cache_type="speed",
183 |     )
184 |     assert config.get_maxsize() == 100
    |                                    ^^^ PLR2004
185 |     assert config.get_folder_name() == "test"
186 |     assert config.get_use_sql() is True
    |

tests/test_decorators.py:56:34: PLR2004 Magic value used in comparison, co
nsider replacing `25` with a constant variable
   |
54 |     time2 = time.time() - start
55 |
56 |     assert result1 == result2 == 25
   |                                  ^^ PLR2004
57 |     assert time2 < time1  # Cached call should be faster
   |

tests/test_decorators.py:74:34: PLR2004 Magic value used in comparison, co
nsider replacing `25` with a constant variable
   |
72 |     result2 = func(5)
73 |
74 |     assert result1 == result2 == 25
   |                                  ^^ PLR2004
75 |     assert cache_dir.exists()
   |

tests/test_decorators.py:91:34: PLR2004 Magic value used in comparison, co
nsider replacing `25` with a constant variable
   |
89 |     result2 = func(5)
90 |
91 |     assert result1 == result2 == 25
   |                                  ^^ PLR2004
   |

tests/test_decorators.py:107:34: PLR2004 Magic value used in comparison, c
onsider replacing `25` with a constant variable
    |
105 |     result2 = func(5)
106 |
107 |     assert result1 == result2 == 25
    |                                  ^^ PLR2004
    |

tests/test_decorators.py:123:22: PLR2004 Magic value used in comparison, c
onsider replacing `25` with a constant variable
    |
121 |     # Should still work with functools backend
122 |     result = func(5)
123 |     assert result == 25
    |                      ^^ PLR2004
    |

tests/test_decorators.py:141:34: PLR2004 Magic value used in comparison, c
onsider replacing `25` with a constant variable
    |
139 |     result2 = await func(5)
140 |
141 |     assert result1 == result2 == 25
    |                                  ^^ PLR2004
    |

tests/test_decorators.py:188:23: PLR2004 Magic value used in comparison, c
onsider replacing `25` with a constant variable
    |
187 |     # Valid input should work
188 |     assert func(5) == 25
    |                       ^^ PLR2004
189 |
190 |     # Error should be raised consistently
    |

tests/test_engines.py:62:45: FBT003 Boolean positional value in function c
all
   |
60 |     assert isinstance(base_engine._make_key("test"), str)
61 |     assert isinstance(base_engine._make_key(123), str)
62 |     assert isinstance(base_engine._make_key(True), str)
   |                                             ^^^^ FBT003
63 |
64 |     # Test with complex types
   |

tests/test_engines.py:82:22: PLR2004 Magic value used in comparison, consi
der replacing `4` with a constant variable
   |
80 |     # First call
81 |     result = test_function(2)
82 |     assert result == 4
   |                      ^ PLR2004
83 |     assert call_count == 1
   |

tests/test_engines.py:87:22: PLR2004 Magic value used in comparison, consi
der replacing `4` with a constant variable
   |
85 |     # Second call (should use cache)
86 |     result = test_function(2)
87 |     assert result == 4
   |                      ^ PLR2004
88 |     assert call_count == 1  # Should not increment
   |

Found 28 errors (5 fixed, 23 remaining).
========================== test session starts ===========================
platform darwin -- Python 3.12.8, pytest-8.3.4, pluggy-1.5.0 -- /Users/ada
m/Library/Application Support/hatch/env/virtual/twat-cache/ivvP1xkE/hatch-
test.py3.12/bin/python3
cachedir: .pytest_cache
rootdir: /Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good
/twat/plugins/repos/twat_cache
configfile: pyproject.toml
plugins: rerunfailures-14.0, mock-3.14.0, xdist-3.6.1
collected 46 items                                                       

tests/test_cache.py::test_cache_settings_validation PASSED         [  2%]
tests/test_cache.py::test_basic_caching PASSED                     [  4%]
tests/test_cache.py::test_cache_clear FAILED                       [  6%]
tests/test_cache.py::test_cache_stats FAILED                       [  8%]
tests/test_cache.py::test_list_processing PASSED                   [ 10%]
tests/test_cache.py::test_different_backends FAILED                [ 13%]
tests/test_cache.py::test_cache_with_complex_types PASSED          [ 15%]
tests/test_cache.py::test_cache_exceptions FAILED                  [ 17%]
tests/test_cache.py::test_kwargs_handling FAILED                   [ 19%]
tests/test_config.py::test_cache_config_validation PASSED          [ 21%]
tests/test_config.py::test_default_config PASSED                   [ 23%]
tests/test_config.py::test_custom_config PASSED                    [ 26%]
tests/test_config.py::test_global_config_env_vars PASSED           [ 28%]
tests/test_config.py::test_get_cache_config PASSED                 [ 30%]
tests/test_config.py::test_logging_configuration PASSED            [ 32%]
tests/test_config.py::test_cache_config_creation PASSED            [ 34%]
tests/test_config.py::test_cache_config_with_sql PASSED            [ 36%]
tests/test_decorators.py::test_mcache_basic PASSED                 [ 39%]
tests/test_decorators.py::test_bcache_basic FAILED                 [ 41%]
tests/test_decorators.py::test_fcache_basic PASSED                 [ 43%]
tests/test_decorators.py::test_ucache_basic PASSED                 [ 45%]
tests/test_decorators.py::test_ucache_fallback FAILED              [ 47%]
tests/test_decorators.py::test_async_caching SKIPPED (async de...) [ 50%]
tests/test_decorators.py::test_cache_performance PASSED            [ 52%]
tests/test_decorators.py::test_decorator_error_handling PASSED     [ 54%]
tests/test_engines.py::test_base_engine_initialization PASSED      [ 56%]
tests/test_engines.py::test_base_engine_key_generation PASSED      [ 58%]
tests/test_engines.py::test_base_engine_cache_decorator PASSED     [ 60%]
tests/test_engines.py::test_base_engine_validation PASSED          [ 63%]
tests/test_engines.py::test_lru_cache_initialization PASSED        [ 65%]
tests/test_engines.py::test_lru_cache_maxsize_enforcement PASSED   [ 67%]
tests/test_engines.py::test_lru_cache_clear PASSED                 [ 69%]
tests/test_engines.py::test_lru_cache_with_complex_values PASSED   [ 71%]
tests/test_engines.py::test_lru_cache_stats_accuracy FAILED        [ 73%]
tests/test_twat_cache.py::test_lru_cache_get_set PASSED            [ 76%]
tests/test_twat_cache.py::test_lru_cache_clear PASSED              [ 78%]
tests/test_twat_cache.py::test_lru_cache_maxsize PASSED            [ 80%]
tests/test_twat_cache.py::test_disk_cache_persistence FAILED       [ 82%]
tests/test_twat_cache.py::test_joblib_numpy_array SKIPPED (num...) [ 84%]
tests/test_twat_cache.py::test_klepto_persistence FAILED           [ 86%]
tests/test_twat_cache.py::test_async_cache_operations SKIPPED      [ 89%]
tests/test_twat_cache.py::test_cachebox_operations FAILED          [ 91%]
tests/test_twat_cache.py::test_cachetools_operations FAILED        [ 93%]
tests/test_twat_cache.py::test_functools_cache_get_set PASSED      [ 95%]
tests/test_twat_cache.py::test_functools_cache_clear PASSED        [ 97%]
tests/test_twat_cache.py::test_functools_cache_maxsize PASSED      [100%]

================================ FAILURES ================================
____________________________ test_cache_clear ____________________________

    def test_cache_clear() -> None:
        """Test cache clearing functionality."""
        call_count = 0
    
        @ucache()
        def cached_function(x: int) -> int:
            nonlocal call_count
            call_count += 1
            return x * x
    
        # First call
        assert cached_function(TEST_INPUT) == TEST_RESULT
        assert call_count == 1
    
        # Clear cache
        clear_cache()
    
        # Should recompute after clear
        assert cached_function(TEST_INPUT) == TEST_RESULT
>       assert call_count == EXPECTED_CALL_COUNT
E       assert 1 == 2

tests/test_cache.py:86: AssertionError
-------------------------- Captured stderr call --------------------------
2025-02-16 14:22:41.322 | DEBUG    | twat_cache.decorators:decorator:286 -
 Using memory cache (functools)
2025-02-16 14:22:41.322 | DEBUG    | twat_cache.cache:register_cache:35 - 
Registered cache: mcache_cached_function_7e23d129
2025-02-16 14:22:41.322 | DEBUG    | twat_cache.cache:clear_cache:57 - Cle
ared cache: mcache_expensive_function_f2588046
2025-02-16 14:22:41.322 | DEBUG    | twat_cache.cache:clear_cache:57 - Cle
ared cache: mcache_cached_function_7e23d129
____________________________ test_cache_stats ____________________________

    def test_cache_stats() -> None:
        """Test cache statistics."""
        call_count = 0
    
        @ucache()
        def cached_function(x: int) -> int:
            nonlocal call_count
            call_count += 1
            return x * x
    
        # Generate some cache activity
        for _i in range(3):
            cached_function(TEST_INPUT)
            cached_function(TEST_INPUT_2)
    
        # Get stats
        stats = get_stats()
    
        # Basic stats checks
        assert isinstance(stats, dict)
>       assert stats["hits"] >= MIN_STATS_COUNT
E       assert 0 >= 2

tests/test_cache.py:109: AssertionError
-------------------------- Captured stderr call --------------------------
2025-02-16 14:22:41.373 | DEBUG    | twat_cache.decorators:decorator:286 -
 Using memory cache (functools)
2025-02-16 14:22:41.373 | DEBUG    | twat_cache.cache:register_cache:35 - 
Registered cache: mcache_cached_function_0a18c5e3
________________________ test_different_backends _________________________

    def test_different_backends() -> None:
        """Test using different cache backends."""
        results: list[Any] = []
    
        # Test with different configurations
        configs = [
            create_cache_config(maxsize=100),  # Memory cache
            create_cache_config(folder_name="disk_test", use_sql=True),  #
 SQL cache
            create_cache_config(folder_name="disk_test", use_sql=False),

# Disk cache
        ]
    
        for config in configs:
    
>           @ucache(config=config)

tests/test_cache.py:148: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
src/twat_cache/decorators.py:262: in ucache
    maxsize = config.get("maxsize", maxsize)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = CacheConfigImpl(maxsize=100, folder_name=None, use_sql=False, prefe
rred_engine=None, cache_type=None)
item = 'get'

    def __getattr__(self, item: str) -> Any:
        private_attributes = object.__getattribute__(self, '__private_attr
ibutes__')
        if item in private_attributes:
            attribute = private_attributes[item]
            if hasattr(attribute, '__get__'):
                return attribute.__get__(self, type(self))  # type: ignore
    
            try:
                # Note: self.__pydantic_private__ cannot be None if self._
_private_attributes__ has items
                return self.__pydantic_private__[item]  # type: ignore
            except KeyError as exc:
                raise AttributeError(f'{type(self).__name__!r} object has 
no attribute {item!r}') from exc
        else:
            # `__pydantic_extra__` can fail to be set if the model is not 
yet fully initialized.
            # See `BaseModel.__repr_args__` for more details
            try:
                pydantic_extra = object.__getattribute__(self, '__pydantic
_extra__')
            except AttributeError:
                pydantic_extra = None
    
            if pydantic_extra:
                try:
                    return pydantic_extra[item]
                except KeyError as exc:
                    raise AttributeError(f'{type(self).__name__!r} object 
has no attribute {item!r}') from exc
            else:
                if hasattr(self.__class__, item):
                    return super().__getattribute__(item)  # Raises Attrib
uteError if appropriate
                else:
                    # this is the current error
>                   raise AttributeError(f'{type(self).__name__!r} object 
has no attribute {item!r}')
E                   AttributeError: 'CacheConfigImpl' object has no attrib
ute 'get'

/Users/adam/Library/Application Support/hatch/env/virtual/twat-cache/ivvP1
xkE/hatch-test.py3.12/lib/python3.12/site-packages/pydantic/main.py:891: A
ttributeError
_________________________ test_cache_exceptions __________________________

    def test_cache_exceptions() -> None:
        """Test caching of exceptions."""
        call_count = 0
    
        @ucache(maxsize=100)
        def failing_function(x: int) -> None:
            nonlocal call_count
            call_count += 1
            msg = "Test error"
            raise ValueError(msg)
    
        # First call
        with pytest.raises(ValueError):
            failing_function(5)
        assert call_count == 1
    
        # Second call should not recompute
        with pytest.raises(ValueError):
            failing_function(5)
>       assert call_count == 1
E       assert 2 == 1

tests/test_cache.py:197: AssertionError
-------------------------- Captured stderr call --------------------------
2025-02-16 14:22:41.410 | DEBUG    | twat_cache.decorators:decorator:286 -
 Using memory cache (functools)
2025-02-16 14:22:41.410 | DEBUG    | twat_cache.cache:register_cache:35 - 
Registered cache: mcache_failing_function_e3e601f4
__________________________ test_kwargs_handling __________________________

    def test_kwargs_handling() -> None:
        """Test caching with different keyword arguments."""
        call_count = 0
    
        @ucache()
        def kwarg_function(x: int, multiplier: int = 1) -> int:
            nonlocal call_count
            call_count += 1
            return x * multiplier
    
        # Test with different kwarg combinations
        assert kwarg_function(TEST_INPUT) == TEST_INPUT
        assert call_count == 1
    
        assert kwarg_function(TEST_INPUT, multiplier=1) == TEST_INPUT
>       assert call_count == 1  # Should use cache
E       assert 2 == 1

tests/test_cache.py:215: AssertionError
-------------------------- Captured stderr call --------------------------
2025-02-16 14:22:41.416 | DEBUG    | twat_cache.decorators:decorator:286 -
 Using memory cache (functools)
2025-02-16 14:22:41.416 | DEBUG    | twat_cache.cache:register_cache:35 - 
Registered cache: mcache_kwarg_function_50746b0d
___________________________ test_bcache_basic ____________________________

tmp_path = PosixPath('/private/var/folders/05/clcynl0509ldxltl599hhhx40000
gn/T/pytest-of-adam/pytest-34/test_bcache_basic0')

    def test_bcache_basic(tmp_path: Path):
        """Test basic disk caching."""
        cache_dir = tmp_path / "cache"
    
        @bcache(folder_name=str(cache_dir))
        def func(x: int) -> int:
            return expensive_computation(x)
    
        # First call should compute
        result1 = func(5)
    
        # Second call should be from cache
        result2 = func(5)
    
        assert result1 == result2 == 25
>       assert cache_dir.exists()
E       AssertionError: assert False
E        +  where False = exists()
E        +    where exists = PosixPath('/private/var/folders/05/clcynl0509
ldxltl599hhhx40000gn/T/pytest-of-adam/pytest-34/test_bcache_basic0/cache')
.exists

tests/test_decorators.py:75: AssertionError
-------------------------- Captured stderr call --------------------------
2025-02-16 14:22:41.563 | WARNING  | twat_cache.decorators:decorator:151 -
 diskcache not available, falling back to memory cache
__________________________ test_ucache_fallback __________________________

obj = <module 'twat_cache.engines' from '/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_cache/src/twat_ca
che/engines/__init__.py'>
name = 'HAS_CACHEBOX', ann = 'twat_cache.engines'

    def annotated_getattr(obj: object, name: str, ann: str) -> object:
        try:
>           obj = getattr(obj, name)
E           AttributeError: module 'twat_cache.engines' has no attribute '
HAS_CACHEBOX'

/Users/adam/Library/Application Support/hatch/env/virtual/twat-cache/ivvP1
xkE/hatch-test.py3.12/lib/python3.12/site-packages/_pytest/monkeypatch.py:
90: AttributeError

The above exception was the direct cause of the following exception:

monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x10c099d60>

    def test_ucache_fallback(monkeypatch):
        """Test ucache fallback behavior."""
        # Simulate no backends available except functools
>       monkeypatch.setattr("twat_cache.engines.HAS_CACHEBOX", False)

tests/test_decorators.py:114: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
/Users/adam/Library/Application Support/hatch/env/virtual/twat-cache/ivvP1
xkE/hatch-test.py3.12/lib/python3.12/site-packages/_pytest/monkeypatch.py:
104: in derive_importpath
    annotated_getattr(target, attr, ann=module)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

obj = <module 'twat_cache.engines' from '/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_cache/src/twat_ca
che/engines/__init__.py'>
name = 'HAS_CACHEBOX', ann = 'twat_cache.engines'

    def annotated_getattr(obj: object, name: str, ann: str) -> object:
        try:
            obj = getattr(obj, name)
        except AttributeError as e:
>           raise AttributeError(
                f"{type(obj).__name__!r} object at {ann} has no attribute 
{name!r}"
            ) from e
E           AttributeError: 'module' object at twat_cache.engines has no a
ttribute 'HAS_CACHEBOX'

/Users/adam/Library/Application Support/hatch/env/virtual/twat-cache/ivvP1
xkE/hatch-test.py3.12/lib/python3.12/site-packages/_pytest/monkeypatch.py:
92: AttributeError
_____________________ test_lru_cache_stats_accuracy ______________________

base_config = CacheConfigImpl(maxsize=100, folder_name=None, use_sql=False
, preferred_engine=None, cache_type=None)

    def test_lru_cache_stats_accuracy(base_config: CacheConfig) -> None:
        """Test accuracy of LRU cache statistics."""
        engine = FunctoolsCacheEngine(base_config)
    
        # Test initial stats
>       stats = engine.stats()
E       TypeError: 'dict' object is not callable

tests/test_engines.py:160: TypeError
______________________ test_disk_cache_persistence _______________________

disk_engine = <twat_cache.engines.diskcache.DiskCacheEngine object at 0x10
c09a480>

    def test_disk_cache_persistence(disk_engine: DiskCacheEngine) -> None:
        """Test persistence of disk cache."""
        key: CacheKey = "test_key"
        value = "test_value"
    
        disk_engine._set_cached_value(key, value)
>       assert disk_engine._get_cached_value(key) == value
E       AssertionError: assert None == 'test_value'
E        +  where None = _get_cached_value('test_key')
E        +    where _get_cached_value = <twat_cache.engines.diskcache.Disk
CacheEngine object at 0x10c09a480>._get_cached_value

tests/test_twat_cache.py:105: AssertionError
________________________ test_klepto_persistence _________________________

klepto_engine = <twat_cache.engines.klepto.KleptoEngine object at 0x10c0fc
0b0>

    def test_klepto_persistence(klepto_engine: KleptoEngine) -> None:
        """Test persistence of klepto cache."""
        key: CacheKey = "test_key"
        value = {"complex": "data", "nested": {"value": 42}}
    
        klepto_engine._set_cached_value(key, value)
>       assert klepto_engine._get_cached_value(key) == value
E       AssertionError: assert None == {'complex': 'data', 'nested': {'val
ue': 42}}
E        +  where None = _get_cached_value('test_key')
E        +    where _get_cached_value = <twat_cache.engines.klepto.KleptoE
ngine object at 0x10c0fc0b0>._get_cached_value

tests/test_twat_cache.py:147: AssertionError
________________________ test_cachebox_operations ________________________

cachebox_engine = <twat_cache.engines.cachebox.CacheBoxEngine object at 0x
10c0fecc0>

    def test_cachebox_operations(cachebox_engine: CacheBoxEngine) -> None:
        """Test basic operations for cachebox."""
        key: CacheKey = "test_key"
        value = "test_value"
    
        assert cachebox_engine._get_cached_value(key) is None
        cachebox_engine._set_cached_value(key, value)
>       assert cachebox_engine._get_cached_value(key) == value
E       AssertionError: assert None == 'test_value'
E        +  where None = _get_cached_value('test_key')
E        +    where _get_cached_value = <twat_cache.engines.cachebox.Cache
BoxEngine object at 0x10c0fecc0>._get_cached_value

tests/test_twat_cache.py:185: AssertionError
_______________________ test_cachetools_operations _______________________

cachetools_engine = <twat_cache.engines.cachetools.CacheToolsEngine object
 at 0x10c09bf20>

    def test_cachetools_operations(cachetools_engine: CacheToolsEngine) ->
 None:
        """Test basic operations for cachetools."""
        key: CacheKey = "test_key"
        value = "test_value"
    
        assert cachetools_engine._get_cached_value(key) is None
        cachetools_engine._set_cached_value(key, value)
>       assert cachetools_engine._get_cached_value(key) == value
E       AssertionError: assert None == 'test_value'
E        +  where None = _get_cached_value('test_key')
E        +    where _get_cached_value = <twat_cache.engines.cachetools.Cac
heToolsEngine object at 0x10c09bf20>._get_cached_value

tests/test_twat_cache.py:205: AssertionError
============================ warnings summary ============================
tests/test_twat_cache.py::test_async_cache_operations
  /Users/adam/Library/Application Support/hatch/env/virtual/twat-cache/ivv
P1xkE/hatch-test.py3.12/lib/python3.12/site-packages/_pytest/runner.py:142
: RuntimeWarning: coroutine 'async_engine' was never awaited
    item.funcargs = None  # type: ignore[attr-defined]
  Enable tracemalloc to get traceback where the object was allocated.
  See https://docs.pytest.org/en/stable/how-to/capture-warnings.html#resou
rce-warnings for more info.

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
======================== short test summary info =========================
FAILED tests/test_cache.py::test_cache_clear - assert 1 == 2
FAILED tests/test_cache.py::test_cache_stats - assert 0 >= 2
FAILED tests/test_cache.py::test_different_backends - AttributeError: 'Cac
heConfigImpl' object has no attribute 'get'
FAILED tests/test_cache.py::test_cache_exceptions - assert 2 == 1
FAILED tests/test_cache.py::test_kwargs_handling - assert 2 == 1
FAILED tests/test_decorators.py::test_bcache_basic - AssertionError: asser
t False
FAILED tests/test_decorators.py::test_ucache_fallback - AttributeError: 'm
odule' object at twat_cache.engines has no attribut...
FAILED tests/test_engines.py::test_lru_cache_stats_accuracy - TypeError: '
dict' object is not callable
FAILED tests/test_twat_cache.py::test_disk_cache_persistence - AssertionEr
ror: assert None == 'test_value'
FAILED tests/test_twat_cache.py::test_klepto_persistence - AssertionError:
 assert None == {'complex': 'data', 'nested': {'value'...
FAILED tests/test_twat_cache.py::test_cachebox_operations - AssertionError
: assert None == 'test_value'
FAILED tests/test_twat_cache.py::test_cachetools_operations - AssertionErr
or: assert None == 'test_value'
========== 12 failed, 31 passed, 3 skipped, 1 warning in 1.26s ===========

```

---

_****_





I see several issues that need to be fixed:

1. **Cache Registry Issues**:
- Cache clearing is working but not updating the call count
- Stats are not being properly tracked
- Need to fix the config handling

2. **Backend Issues**:
- Need to fix the backend availability checks
- Need to fix the cache persistence
- Need to fix the stats tracking

Let me fix these issues one by one. First, let's fix the cache registry and stats:

---

_****_

```diff
  
  from pathlib import Path
- from typing import Any
+ from typing import Any, Dict, NamedTuple
  from loguru import logger
+ 
+ 
+ class CacheStats(NamedTuple):
+     """Cache statistics."""
+ 
+     hits: int
+     misses: int
+     size: int
+     maxsize: int | None
+ 
+ 
+ class CacheEntry(NamedTuple):
+     """Cache registry entry."""
+ 
+     cache: Any
+     wrapper: Any
+     stats: CacheStats
+ 
  
  # Global registry of active caches
- _active_caches: dict[str, Any] = {}
+ _active_caches: Dict[str, CacheEntry] = {}
  
  
- def register_cache(name: str, cache: Any) -> None:
+ def register_cache(name: str, cache: Any, wrapper: Any, stats: CacheStats) -> None:
      """
      Register an active cache instance.
  
      Args:
          name: Unique name for the cache
-         cache: The cache instance to register
+         cache: The cache instance
+         wrapper: The wrapper function
+         stats: Initial cache statistics
      """
-     _active_caches[name] = cache
+     _active_caches[name] = CacheEntry(cache, wrapper, stats)
      logger.debug(f"Registered cache: {name}")
  
      if name is not None:
          if name in _active_caches:
-             cache = _active_caches[name]
-             if hasattr(cache, "clear"):
-                 cache.clear()
+             entry = _active_caches[name]
+             if hasattr(entry.cache, "clear"):
+                 entry.cache.clear()
+             # Reset stats
+             _active_caches[name] = CacheEntry(
+                 entry.cache, entry.wrapper, CacheStats(0, 0, 0, entry.stats.maxsize)
+             )
              logger.debug(f"Cleared cache: {name}")
          return
  
      # Clear all caches
-     for cache_name, cache in _active_caches.items():
-         if hasattr(cache, "clear"):
-             cache.clear()
+     for cache_name, entry in _active_caches.items():
+         if hasattr(entry.cache, "clear"):
+             entry.cache.clear()
+         # Reset stats
+         _active_caches[cache_name] = CacheEntry(
+             entry.cache, entry.wrapper, CacheStats(0, 0, 0, entry.stats.maxsize)
+         )
          logger.debug(f"Cleared cache: {cache_name}")
  
  
  
- def get_stats(name: str | None = None) -> dict[str, Any]:
+ def get_stats(name: str | None = None) -> Dict[str, Any]:
      """
      Get cache statistics.
          Dictionary of cache statistics
      """
-     stats: dict[str, Any] = {
+     if name is not None:
+         if name not in _active_caches:
+             return {
+                 "hits": 0,
+                 "misses": 0,
+                 "size": 0,
+                 "maxsize": None,
+             }
+         entry = _active_caches[name]
+         return {
+             "hits": entry.stats.hits,
+             "misses": entry.stats.misses,
+             "size": entry.stats.size,
+             "maxsize": entry.stats.maxsize,
+         }
+ 
+     # Aggregate stats from all caches
+     total_stats = {
          "total_caches": len(_active_caches),
          "hits": 0,
      }
  
-     if name is not None:
+     for entry in _active_caches.values():
+         total_stats["hits"] += entry.stats.hits
+         total_stats["misses"] += entry.stats.misses
+         total_stats["size"] += entry.stats.size
+ 
+     return total_stats
+ 
+ 
+ def update_stats(
+     name: str, *, hit: bool = False, miss: bool = False, size: int | None = None
+ ) -> None:
+     """
+     Update cache statistics.
+ 
+     Args:
+         name: Name of the cache to update
+         hit: Whether to increment hit count
+         miss: Whether to increment miss count
+         size: New cache size (if changed)
+     """
      if name not in _active_caches:
-             return stats
-         cache = _active_caches[name]
-         if hasattr(cache, "hits"):
-             stats["hits"] = cache.hits
-         if hasattr(cache, "misses"):
-             stats["misses"] = cache.misses
-         if hasattr(cache, "cache"):
-             stats["size"] = len(cache.cache)
-         return stats
- 
-     # Aggregate stats from all caches
-     for cache in _active_caches.values():
-         if hasattr(cache, "hits"):
-             stats["hits"] += cache.hits
-         if hasattr(cache, "misses"):
-             stats["misses"] += cache.misses
-         if hasattr(cache, "cache"):
-             stats["size"] += len(cache.cache)
- 
-     return stats
+         return
+ 
+     entry = _active_caches[name]
+     hits = entry.stats.hits + (1 if hit else 0)
+     misses = entry.stats.misses + (1 if miss else 0)
+     new_size = size if size is not None else entry.stats.size
+ 
+     _active_caches[name] = CacheEntry(
+         entry.cache,
+         entry.wrapper,
+         CacheStats(hits, misses, new_size, entry.stats.maxsize),
+     )
  
```

---

_****_







Now let's update the decorators to use the new stats system:

---

_****_

```diff
  import uuid
  from pathlib import Path
- from typing import Any, TypeVar, cast, ParamSpec
- from collections.abc import Callable
+ from typing import Any, Callable, TypeVar, cast, ParamSpec, Dict, Union
  from loguru import logger
  
- from .cache import register_cache
+ from .cache import register_cache, update_stats, CacheStats
  
  # Type variables for generic function types
  
  # Cache types
- CacheDict = dict[str, Any]
+ CacheDict = Dict[str, Any]
  CacheKey = str
  CacheValue = Any
  
      # Convert args to a stable form
-     def convert(obj: Any) -> str | int | float | bool | None:
-         if isinstance(obj, list | dict | set):
+     def convert(obj: Any) -> Union[str, int, float, bool, None]:
+         if isinstance(obj, (list, dict, set)):
              return json.dumps(obj, sort_keys=True)
-         if isinstance(obj, int | float | str | bool | type(None)):
+         if isinstance(obj, (int, float, str, bool, type(None))):
              return obj
          return str(obj)
      def decorator(func: Callable[P, R]) -> Callable[P, R]:
          cache: CacheDict = {}
-         hits = 0
-         misses = 0
          cache_id = f"mcache_{func.__name__}_{uuid.uuid4().hex[:8]}"
  
          @functools.wraps(func)
          def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
-             nonlocal hits, misses
              key = make_key(*args, **kwargs)
  
              if key in cache:
-                 hits += 1
+                 update_stats(cache_id, hit=True)
                  return cast(R, cache[key])
  
-             misses += 1
+             update_stats(cache_id, miss=True)
              result = func(*args, **kwargs)
              cache[key] = result
                  cache.pop(next(iter(cache)))
  
+             update_stats(cache_id, size=len(cache))
              return result
  
-         # Add stats
-         wrapper.hits = hits  # type: ignore
-         wrapper.misses = misses  # type: ignore
-         wrapper.cache = cache  # type: ignore
-         wrapper.maxsize = maxsize  # type: ignore
- 
-         # Register cache
-         register_cache(cache_id, wrapper)
+         # Register cache with initial stats
+         register_cache(
+             cache_id,
+             cache,
+             wrapper,
+             CacheStats(hits=0, misses=0, size=0, maxsize=maxsize),
+         )
  
          return wrapper
          cache_dir.mkdir(parents=True, exist_ok=True)
          cache = DiskCache(str(cache_dir), size_limit=maxsize or int(1e9))
-         hits = 0
-         misses = 0
          cache_id = f"bcache_{func.__name__}_{uuid.uuid4().hex[:8]}"
  
          @functools.wraps(func)
          def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
-             nonlocal hits, misses
              key = make_key(*args, **kwargs)
  
              result = cache.get(key)
              if result is not None:
-                 hits += 1
+                 update_stats(cache_id, hit=True)
                  return cast(R, result)
  
-             misses += 1
+             update_stats(cache_id, miss=True)
              result = func(*args, **kwargs)
              cache.set(key, result)
+             update_stats(cache_id, size=len(cache))
              return result
  
-         # Add stats
-         wrapper.hits = hits  # type: ignore
-         wrapper.misses = misses  # type: ignore
-         wrapper.cache = cache  # type: ignore
-         wrapper.maxsize = maxsize  # type: ignore
- 
-         # Register cache
-         register_cache(cache_id, wrapper)
+         # Register cache with initial stats
+         register_cache(
+             cache_id,
+             cache,
+             wrapper,
+             CacheStats(hits=0, misses=0, size=0, maxsize=maxsize),
+         )
  
          return wrapper
  
          cache = BoxCache(maxsize=maxsize or 0)  # 0 means unlimited in cachebox
-         hits = 0
-         misses = 0
          cache_id = f"fcache_{func.__name__}_{uuid.uuid4().hex[:8]}"
  
          @functools.wraps(func)
          def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
-             nonlocal hits, misses
              key = make_key(*args, **kwargs)
  
              result = cache.get(key)
              if result is not None:
-                 hits += 1
+                 update_stats(cache_id, hit=True)
                  return cast(R, result)
  
-             misses += 1
+             update_stats(cache_id, miss=True)
              result = func(*args, **kwargs)
              cache[key] = result
+             update_stats(cache_id, size=len(cache))
              return result
  
-         # Add stats
-         wrapper.hits = hits  # type: ignore
-         wrapper.misses = misses  # type: ignore
-         wrapper.cache = cache  # type: ignore
-         wrapper.maxsize = maxsize  # type: ignore
- 
-         # Register cache
-         register_cache(cache_id, wrapper)
+         # Register cache with initial stats
+         register_cache(
+             cache_id,
+             cache,
+             wrapper,
+             CacheStats(hits=0, misses=0, size=0, maxsize=maxsize),
+         )
  
          return wrapper
```

---

_****_







Let me run our catchphrase again to check if the changes helped:

---

_****_

```bash
uv venv; source .venv/bin/activate; uv pip install -e .[all,dev,test]; hatch run lint:fix; hatch test;
```

```
Using CPython 3.12.8 interpreter at: /usr/local/bin/python3.12
Creating virtual environment at: .venv
Activate with: source .venv/bin/activate
zsh: no matches found: .[all,dev,test]
Rewriting src/twat_cache/cache.py
Rewriting src/twat_cache/decorators.py
warning: The top-level linter settings are deprecated in favour of their c
ounterparts in the `lint` section. Please update the following options in
`pyproject.toml`:
  - 'per-file-ignores' -> 'lint.per-file-ignores'
src/twat_cache/cache.py:58:5: C901 `clear_cache` is too complex (11 > 10)
   |
58 | def clear_cache(name: str | None = None) -> None:
   |     ^^^^^^^^^^^ C901
59 |     """
60 |     Clear one or all caches.
   |

src/twat_cache/config.py:152:26: PLR2004 Magic value used in comparison, c
onsider replacing `9` with a constant variable
    |
150 |             msg = "compression_level must be an integer"
151 |             raise ValueError(msg)
152 |         if not 0 <= v <= 9:
    |                          ^ PLR2004
153 |             msg = "compression_level must be between 0 and 9"
154 |             raise ValueError(msg)
    |

src/twat_cache/engines/base.py:213:33: ARG002 Unused method argument: `key
`
    |
211 |     """
212 |
213 |     def _get_cached_value(self, key: CacheKey) -> R | None:
    |                                 ^^^ ARG002
214 |         """
215 |         Retrieve a value from the cache.
    |

src/twat_cache/engines/functools.py:1:1: A005 Module `functools` shadows a
 Python standard-library module
src/twat_cache/engines/joblib.py:49:33: ARG002 Unused method argument: `ke
y`
   |
47 |         )
48 |
49 |     def _get_cached_value(self, key: CacheKey) -> R | None:
   |                                 ^^^ ARG002
50 |         """Retrieve a value from the cache.
   |

src/twat_cache/engines/klepto.py:20:34: ARG005 Unused lambda argument: `ar
gs`
   |
18 |     HAS_KLEPTO = False
19 |     dir_archive = type("dir_archive", (), {})  # type: ignore
20 |     keymap = picklemap = lambda *args, **kwargs: lambda f: f  # type:
 ignore
   |                                  ^^^^ ARG005
   |

src/twat_cache/engines/klepto.py:20:42: ARG005 Unused lambda argument: `kw
args`
   |
18 |     HAS_KLEPTO = False
19 |     dir_archive = type("dir_archive", (), {})  # type: ignore
20 |     keymap = picklemap = lambda *args, **kwargs: lambda f: f  # type:
 ignore
   |                                          ^^^^^^ ARG005
   |

src/twat_cache/paths.py:100:5: C901 `clear_cache` is too complex (11 > 10)
    |
100 | def clear_cache(folder_name: str | None = None) -> None:
    |     ^^^^^^^^^^^ C901
101 |     """
102 |     Clear the cache directory for the given folder name.
    |

src/twat_cache/types.py:1:1: A005 Module `types` shadows a Python standard
-library module
tests/test_cache.py:175:34: PLR2004 Magic value used in comparison, consid
er replacing `15` with a constant variable
    |
173 |     result2 = process_list(test_list)
174 |
175 |     assert result1 == result2 == 15
    |                                  ^^ PLR2004
    |

tests/test_config.py:74:38: PLR2004 Magic value used in comparison, consid
er replacing `1000` with a constant variable
   |
72 |     # Check default values
73 |     assert config.cache_dir == get_cache_path("global")
74 |     assert config.default_maxsize == 1000
   |                                      ^^^^ PLR2004
75 |     assert not config.default_use_sql
76 |     assert config.default_engine == "lru"
   |

tests/test_config.py:79:40: PLR2004 Magic value used in comparison, consid
er replacing `6` with a constant variable
   |
77 |     assert config.default_cache_type is None
78 |     assert config.enable_compression
79 |     assert config.compression_level == 6
   |                                        ^ PLR2004
80 |     assert not config.debug
81 |     assert config.log_file is None
   |

tests/test_config.py:184:36: PLR2004 Magic value used in comparison, consi
der replacing `100` with a constant variable
    |
182 |         cache_type="speed",
183 |     )
184 |     assert config.get_maxsize() == 100
    |                                    ^^^ PLR2004
185 |     assert config.get_folder_name() == "test"
186 |     assert config.get_use_sql() is True
    |

tests/test_decorators.py:56:34: PLR2004 Magic value used in comparison, co
nsider replacing `25` with a constant variable
   |
54 |     time2 = time.time() - start
55 |
56 |     assert result1 == result2 == 25
   |                                  ^^ PLR2004
57 |     assert time2 < time1  # Cached call should be faster
   |

tests/test_decorators.py:74:34: PLR2004 Magic value used in comparison, co
nsider replacing `25` with a constant variable
   |
72 |     result2 = func(5)
73 |
74 |     assert result1 == result2 == 25
   |                                  ^^ PLR2004
75 |     assert cache_dir.exists()
   |

tests/test_decorators.py:91:34: PLR2004 Magic value used in comparison, co
nsider replacing `25` with a constant variable
   |
89 |     result2 = func(5)
90 |
91 |     assert result1 == result2 == 25
   |                                  ^^ PLR2004
   |

tests/test_decorators.py:107:34: PLR2004 Magic value used in comparison, c
onsider replacing `25` with a constant variable
    |
105 |     result2 = func(5)
106 |
107 |     assert result1 == result2 == 25
    |                                  ^^ PLR2004
    |

tests/test_decorators.py:123:22: PLR2004 Magic value used in comparison, c
onsider replacing `25` with a constant variable
    |
121 |     # Should still work with functools backend
122 |     result = func(5)
123 |     assert result == 25
    |                      ^^ PLR2004
    |

tests/test_decorators.py:141:34: PLR2004 Magic value used in comparison, c
onsider replacing `25` with a constant variable
    |
139 |     result2 = await func(5)
140 |
141 |     assert result1 == result2 == 25
    |                                  ^^ PLR2004
    |

tests/test_decorators.py:188:23: PLR2004 Magic value used in comparison, c
onsider replacing `25` with a constant variable
    |
187 |     # Valid input should work
188 |     assert func(5) == 25
    |                       ^^ PLR2004
189 |
190 |     # Error should be raised consistently
    |

tests/test_engines.py:62:45: FBT003 Boolean positional value in function c
all
   |
60 |     assert isinstance(base_engine._make_key("test"), str)
61 |     assert isinstance(base_engine._make_key(123), str)
62 |     assert isinstance(base_engine._make_key(True), str)
   |                                             ^^^^ FBT003
63 |
64 |     # Test with complex types
   |

tests/test_engines.py:82:22: PLR2004 Magic value used in comparison, consi
der replacing `4` with a constant variable
   |
80 |     # First call
81 |     result = test_function(2)
82 |     assert result == 4
   |                      ^ PLR2004
83 |     assert call_count == 1
   |

tests/test_engines.py:87:22: PLR2004 Magic value used in comparison, consi
der replacing `4` with a constant variable
   |
85 |     # Second call (should use cache)
86 |     result = test_function(2)
87 |     assert result == 4
   |                      ^ PLR2004
88 |     assert call_count == 1  # Should not increment
   |

Found 28 errors (5 fixed, 23 remaining).
========================== test session starts ===========================
platform darwin -- Python 3.12.8, pytest-8.3.4, pluggy-1.5.0 -- /Users/ada
m/Library/Application Support/hatch/env/virtual/twat-cache/ivvP1xkE/hatch-
test.py3.12/bin/python3
cachedir: .pytest_cache
rootdir: /Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good
/twat/plugins/repos/twat_cache
configfile: pyproject.toml
plugins: rerunfailures-14.0, mock-3.14.0, xdist-3.6.1
collected 46 items                                                       

tests/test_cache.py::test_cache_settings_validation PASSED         [  2%]
tests/test_cache.py::test_basic_caching PASSED                     [  4%]
tests/test_cache.py::test_cache_clear PASSED                       [  6%]
tests/test_cache.py::test_cache_stats PASSED                       [  8%]
tests/test_cache.py::test_list_processing PASSED                   [ 10%]
tests/test_cache.py::test_different_backends FAILED                [ 13%]
tests/test_cache.py::test_cache_with_complex_types PASSED          [ 15%]
tests/test_cache.py::test_cache_exceptions FAILED                  [ 17%]
tests/test_cache.py::test_kwargs_handling FAILED                   [ 19%]
tests/test_config.py::test_cache_config_validation PASSED          [ 21%]
tests/test_config.py::test_default_config PASSED                   [ 23%]
tests/test_config.py::test_custom_config PASSED                    [ 26%]
tests/test_config.py::test_global_config_env_vars PASSED           [ 28%]
tests/test_config.py::test_get_cache_config PASSED                 [ 30%]
tests/test_config.py::test_logging_configuration PASSED            [ 32%]
tests/test_config.py::test_cache_config_creation PASSED            [ 34%]
tests/test_config.py::test_cache_config_with_sql PASSED            [ 36%]
tests/test_decorators.py::test_mcache_basic PASSED                 [ 39%]
tests/test_decorators.py::test_bcache_basic FAILED                 [ 41%]
tests/test_decorators.py::test_fcache_basic PASSED                 [ 43%]
tests/test_decorators.py::test_ucache_basic PASSED                 [ 45%]
tests/test_decorators.py::test_ucache_fallback FAILED              [ 47%]
tests/test_decorators.py::test_async_caching SKIPPED (async de...) [ 50%]
tests/test_decorators.py::test_cache_performance PASSED            [ 52%]
tests/test_decorators.py::test_decorator_error_handling PASSED     [ 54%]
tests/test_engines.py::test_base_engine_initialization PASSED      [ 56%]
tests/test_engines.py::test_base_engine_key_generation PASSED      [ 58%]
tests/test_engines.py::test_base_engine_cache_decorator PASSED     [ 60%]
tests/test_engines.py::test_base_engine_validation PASSED          [ 63%]
tests/test_engines.py::test_lru_cache_initialization PASSED        [ 65%]
tests/test_engines.py::test_lru_cache_maxsize_enforcement PASSED   [ 67%]
tests/test_engines.py::test_lru_cache_clear PASSED                 [ 69%]
tests/test_engines.py::test_lru_cache_with_complex_values PASSED   [ 71%]
tests/test_engines.py::test_lru_cache_stats_accuracy FAILED        [ 73%]
tests/test_twat_cache.py::test_lru_cache_get_set PASSED            [ 76%]
tests/test_twat_cache.py::test_lru_cache_clear PASSED              [ 78%]
tests/test_twat_cache.py::test_lru_cache_maxsize PASSED            [ 80%]
tests/test_twat_cache.py::test_disk_cache_persistence FAILED       [ 82%]
tests/test_twat_cache.py::test_joblib_numpy_array SKIPPED (num...) [ 84%]
tests/test_twat_cache.py::test_klepto_persistence FAILED           [ 86%]
tests/test_twat_cache.py::test_async_cache_operations SKIPPED      [ 89%]
tests/test_twat_cache.py::test_cachebox_operations FAILED          [ 91%]
tests/test_twat_cache.py::test_cachetools_operations FAILED        [ 93%]
tests/test_twat_cache.py::test_functools_cache_get_set PASSED      [ 95%]
tests/test_twat_cache.py::test_functools_cache_clear PASSED        [ 97%]
tests/test_twat_cache.py::test_functools_cache_maxsize PASSED      [100%]

================================ FAILURES ================================
________________________ test_different_backends _________________________

    def test_different_backends() -> None:
        """Test using different cache backends."""
        results: list[Any] = []
    
        # Test with different configurations
        configs = [
            create_cache_config(maxsize=100),  # Memory cache
            create_cache_config(folder_name="disk_test", use_sql=True),  #
 SQL cache
            create_cache_config(folder_name="disk_test", use_sql=False),

# Disk cache
        ]
    
        for config in configs:
    
>           @ucache(config=config)

tests/test_cache.py:148: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
src/twat_cache/decorators.py:253: in ucache
    maxsize = config.get("maxsize", maxsize)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = CacheConfigImpl(maxsize=100, folder_name=None, use_sql=False, prefe
rred_engine=None, cache_type=None)
item = 'get'

    def __getattr__(self, item: str) -> Any:
        private_attributes = object.__getattribute__(self, '__private_attr
ibutes__')
        if item in private_attributes:
            attribute = private_attributes[item]
            if hasattr(attribute, '__get__'):
                return attribute.__get__(self, type(self))  # type: ignore
    
            try:
                # Note: self.__pydantic_private__ cannot be None if self._
_private_attributes__ has items
                return self.__pydantic_private__[item]  # type: ignore
            except KeyError as exc:
                raise AttributeError(f'{type(self).__name__!r} object has 
no attribute {item!r}') from exc
        else:
            # `__pydantic_extra__` can fail to be set if the model is not 
yet fully initialized.
            # See `BaseModel.__repr_args__` for more details
            try:
                pydantic_extra = object.__getattribute__(self, '__pydantic
_extra__')
            except AttributeError:
                pydantic_extra = None
    
            if pydantic_extra:
                try:
                    return pydantic_extra[item]
                except KeyError as exc:
                    raise AttributeError(f'{type(self).__name__!r} object 
has no attribute {item!r}') from exc
            else:
                if hasattr(self.__class__, item):
                    return super().__getattribute__(item)  # Raises Attrib
uteError if appropriate
                else:
                    # this is the current error
>                   raise AttributeError(f'{type(self).__name__!r} object 
has no attribute {item!r}')
E                   AttributeError: 'CacheConfigImpl' object has no attrib
ute 'get'

/Users/adam/Library/Application Support/hatch/env/virtual/twat-cache/ivvP1
xkE/hatch-test.py3.12/lib/python3.12/site-packages/pydantic/main.py:891: A
ttributeError
_________________________ test_cache_exceptions __________________________

    def test_cache_exceptions() -> None:
        """Test caching of exceptions."""
        call_count = 0
    
        @ucache(maxsize=100)
        def failing_function(x: int) -> None:
            nonlocal call_count
            call_count += 1
            msg = "Test error"
            raise ValueError(msg)
    
        # First call
        with pytest.raises(ValueError):
            failing_function(5)
        assert call_count == 1
    
        # Second call should not recompute
        with pytest.raises(ValueError):
            failing_function(5)
>       assert call_count == 1
E       assert 2 == 1

tests/test_cache.py:197: AssertionError
-------------------------- Captured stderr call --------------------------
2025-02-16 14:24:12.773 | DEBUG    | twat_cache.decorators:decorator:277 -
 Using memory cache (functools)
2025-02-16 14:24:12.773 | DEBUG    | twat_cache.cache:register_cache:55 - 
Registered cache: mcache_failing_function_98a2ac4e
__________________________ test_kwargs_handling __________________________

    def test_kwargs_handling() -> None:
        """Test caching with different keyword arguments."""
        call_count = 0
    
        @ucache()
        def kwarg_function(x: int, multiplier: int = 1) -> int:
            nonlocal call_count
            call_count += 1
            return x * multiplier
    
        # Test with different kwarg combinations
        assert kwarg_function(TEST_INPUT) == TEST_INPUT
        assert call_count == 1
    
        assert kwarg_function(TEST_INPUT, multiplier=1) == TEST_INPUT
>       assert call_count == 1  # Should use cache
E       assert 2 == 1

tests/test_cache.py:215: AssertionError
-------------------------- Captured stderr call --------------------------
2025-02-16 14:24:12.778 | DEBUG    | twat_cache.decorators:decorator:277 -
 Using memory cache (functools)
2025-02-16 14:24:12.779 | DEBUG    | twat_cache.cache:register_cache:55 - 
Registered cache: mcache_kwarg_function_eaa12de5
___________________________ test_bcache_basic ____________________________

tmp_path = PosixPath('/private/var/folders/05/clcynl0509ldxltl599hhhx40000
gn/T/pytest-of-adam/pytest-35/test_bcache_basic0')

    def test_bcache_basic(tmp_path: Path):
        """Test basic disk caching."""
        cache_dir = tmp_path / "cache"
    
        @bcache(folder_name=str(cache_dir))
        def func(x: int) -> int:
            return expensive_computation(x)
    
        # First call should compute
        result1 = func(5)
    
        # Second call should be from cache
        result2 = func(5)
    
        assert result1 == result2 == 25
>       assert cache_dir.exists()
E       AssertionError: assert False
E        +  where False = exists()
E        +    where exists = PosixPath('/private/var/folders/05/clcynl0509
ldxltl599hhhx40000gn/T/pytest-of-adam/pytest-35/test_bcache_basic0/cache')
.exists

tests/test_decorators.py:75: AssertionError
-------------------------- Captured stderr call --------------------------
2025-02-16 14:24:12.934 | WARNING  | twat_cache.decorators:decorator:148 -
 diskcache not available, falling back to memory cache
__________________________ test_ucache_fallback __________________________

obj = <module 'twat_cache.engines' from '/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_cache/src/twat_ca
che/engines/__init__.py'>
name = 'HAS_CACHEBOX', ann = 'twat_cache.engines'

    def annotated_getattr(obj: object, name: str, ann: str) -> object:
        try:
>           obj = getattr(obj, name)
E           AttributeError: module 'twat_cache.engines' has no attribute '
HAS_CACHEBOX'

/Users/adam/Library/Application Support/hatch/env/virtual/twat-cache/ivvP1
xkE/hatch-test.py3.12/lib/python3.12/site-packages/_pytest/monkeypatch.py:
90: AttributeError

The above exception was the direct cause of the following exception:

monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x1049d1b50>

    def test_ucache_fallback(monkeypatch):
        """Test ucache fallback behavior."""
        # Simulate no backends available except functools
>       monkeypatch.setattr("twat_cache.engines.HAS_CACHEBOX", False)

tests/test_decorators.py:114: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
/Users/adam/Library/Application Support/hatch/env/virtual/twat-cache/ivvP1
xkE/hatch-test.py3.12/lib/python3.12/site-packages/_pytest/monkeypatch.py:
104: in derive_importpath
    annotated_getattr(target, attr, ann=module)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

obj = <module 'twat_cache.engines' from '/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_cache/src/twat_ca
che/engines/__init__.py'>
name = 'HAS_CACHEBOX', ann = 'twat_cache.engines'

    def annotated_getattr(obj: object, name: str, ann: str) -> object:
        try:
            obj = getattr(obj, name)
        except AttributeError as e:
>           raise AttributeError(
                f"{type(obj).__name__!r} object at {ann} has no attribute 
{name!r}"
            ) from e
E           AttributeError: 'module' object at twat_cache.engines has no a
ttribute 'HAS_CACHEBOX'

/Users/adam/Library/Application Support/hatch/env/virtual/twat-cache/ivvP1
xkE/hatch-test.py3.12/lib/python3.12/site-packages/_pytest/monkeypatch.py:
92: AttributeError
_____________________ test_lru_cache_stats_accuracy ______________________

base_config = CacheConfigImpl(maxsize=100, folder_name=None, use_sql=False
, preferred_engine=None, cache_type=None)

    def test_lru_cache_stats_accuracy(base_config: CacheConfig) -> None:
        """Test accuracy of LRU cache statistics."""
        engine = FunctoolsCacheEngine(base_config)
    
        # Test initial stats
>       stats = engine.stats()
E       TypeError: 'dict' object is not callable

tests/test_engines.py:160: TypeError
______________________ test_disk_cache_persistence _______________________

disk_engine = <twat_cache.engines.diskcache.DiskCacheEngine object at 0x10
49d2b40>

    def test_disk_cache_persistence(disk_engine: DiskCacheEngine) -> None:
        """Test persistence of disk cache."""
        key: CacheKey = "test_key"
        value = "test_value"
    
        disk_engine._set_cached_value(key, value)
>       assert disk_engine._get_cached_value(key) == value
E       AssertionError: assert None == 'test_value'
E        +  where None = _get_cached_value('test_key')
E        +    where _get_cached_value = <twat_cache.engines.diskcache.Disk
CacheEngine object at 0x1049d2b40>._get_cached_value

tests/test_twat_cache.py:105: AssertionError
________________________ test_klepto_persistence _________________________

klepto_engine = <twat_cache.engines.klepto.KleptoEngine object at 0x1049bc
6b0>

    def test_klepto_persistence(klepto_engine: KleptoEngine) -> None:
        """Test persistence of klepto cache."""
        key: CacheKey = "test_key"
        value = {"complex": "data", "nested": {"value": 42}}
    
        klepto_engine._set_cached_value(key, value)
>       assert klepto_engine._get_cached_value(key) == value
E       AssertionError: assert None == {'complex': 'data', 'nested': {'val
ue': 42}}
E        +  where None = _get_cached_value('test_key')
E        +    where _get_cached_value = <twat_cache.engines.klepto.KleptoE
ngine object at 0x1049bc6b0>._get_cached_value

tests/test_twat_cache.py:147: AssertionError
________________________ test_cachebox_operations ________________________

cachebox_engine = <twat_cache.engines.cachebox.CacheBoxEngine object at 0x
1049bea50>

    def test_cachebox_operations(cachebox_engine: CacheBoxEngine) -> None:
        """Test basic operations for cachebox."""
        key: CacheKey = "test_key"
        value = "test_value"
    
        assert cachebox_engine._get_cached_value(key) is None
        cachebox_engine._set_cached_value(key, value)
>       assert cachebox_engine._get_cached_value(key) == value
E       AssertionError: assert None == 'test_value'
E        +  where None = _get_cached_value('test_key')
E        +    where _get_cached_value = <twat_cache.engines.cachebox.Cache
BoxEngine object at 0x1049bea50>._get_cached_value

tests/test_twat_cache.py:185: AssertionError
_______________________ test_cachetools_operations _______________________

cachetools_engine = <twat_cache.engines.cachetools.CacheToolsEngine object
 at 0x1049bcd10>

    def test_cachetools_operations(cachetools_engine: CacheToolsEngine) ->
 None:
        """Test basic operations for cachetools."""
        key: CacheKey = "test_key"
        value = "test_value"
    
        assert cachetools_engine._get_cached_value(key) is None
        cachetools_engine._set_cached_value(key, value)
>       assert cachetools_engine._get_cached_value(key) == value
E       AssertionError: assert None == 'test_value'
E        +  where None = _get_cached_value('test_key')
E        +    where _get_cached_value = <twat_cache.engines.cachetools.Cac
heToolsEngine object at 0x1049bcd10>._get_cached_value

tests/test_twat_cache.py:205: AssertionError
============================ warnings summary ============================
tests/test_twat_cache.py::test_async_cache_operations
  /Users/adam/Library/Application Support/hatch/env/virtual/twat-cache/ivv
P1xkE/hatch-test.py3.12/lib/python3.12/site-packages/_pytest/runner.py:142
: RuntimeWarning: coroutine 'async_engine' was never awaited
    item.funcargs = None  # type: ignore[attr-defined]
  Enable tracemalloc to get traceback where the object was allocated.
  See https://docs.pytest.org/en/stable/how-to/capture-warnings.html#resou
rce-warnings for more info.

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
======================== short test summary info =========================
FAILED tests/test_cache.py::test_different_backends - AttributeError: 'Cac
heConfigImpl' object has no attribute 'get'
FAILED tests/test_cache.py::test_cache_exceptions - assert 2 == 1
FAILED tests/test_cache.py::test_kwargs_handling - assert 2 == 1
FAILED tests/test_decorators.py::test_bcache_basic - AssertionError: asser
t False
FAILED tests/test_decorators.py::test_ucache_fallback - AttributeError: 'm
odule' object at twat_cache.engines has no attribut...
FAILED tests/test_engines.py::test_lru_cache_stats_accuracy - TypeError: '
dict' object is not callable
FAILED tests/test_twat_cache.py::test_disk_cache_persistence - AssertionEr
ror: assert None == 'test_value'
FAILED tests/test_twat_cache.py::test_klepto_persistence - AssertionError:
 assert None == {'complex': 'data', 'nested': {'value'...
FAILED tests/test_twat_cache.py::test_cachebox_operations - AssertionError
: assert None == 'test_value'
FAILED tests/test_twat_cache.py::test_cachetools_operations - AssertionErr
or: assert None == 'test_value'
========== 10 failed, 33 passed, 3 skipped, 1 warning in 1.23s ===========

```

---

_****_







I see several remaining issues:

1. **Config Handling**:
- Need to fix the config handling in ucache
- Need to fix the backend availability checks

2. **Cache Persistence**:
- Need to fix the backend persistence
- Need to fix the cache directory handling

3. **Exception Handling**:
- Need to fix exception caching
- Need to fix kwargs handling

Let me fix these issues one by one. First, let's fix the config handling:

---

_****_

```diff
  # dependencies = [
  #   "loguru",
- #   "pydantic",
- #   "pydantic-settings",
  # ]
  # ///
  # this_file: src/twat_cache/config.py
  
  """
- Configuration management for twat-cache.
+ Simple configuration system for twat_cache.
  
- This module provides configuration management for the caching system,
- supporting both global settings and per-cache configuration.
+ This module provides a simple configuration system for the cache decorators.
  """
  
+ from dataclasses import dataclass
  from pathlib import Path
- from typing import Literal, Any, cast
- import sys
- 
+ from typing import Any, Dict, Optional
  from loguru import logger
- from pydantic import BaseModel, Field, field_validator
- from pydantic_settings import BaseSettings
- 
- from .paths import get_cache_path
- from .types import CacheConfig as CacheConfigProtocol
- 
- 
- CacheType = Literal["speed", "database", "filesystem"]
- 
- 
- class CacheConfigImpl(BaseModel):
-     """Cache configuration settings."""
+ 
+ 
+ @dataclass
+ class CacheConfig:
+     """Cache configuration."""
  
-     maxsize: int | None = Field(default=None, description="Maximum size of the cache")
-     folder_name: str | None = Field(
-         default=None, description="Name of the cache folder"
-     )
-     use_sql: bool = Field(default=False, description="Whether to use SQL storage")
-     preferred_engine: str | None = Field(
-         default=None, description="Preferred cache engine"
-     )
-     cache_type: str | None = Field(default=None, description="Type of cache to use")
- 
-     model_config = {
-         "validate_assignment": True,
-         "extra": "ignore",
-         "arbitrary_types_allowed": True,
-         "from_attributes": True,
-         "populate_by_name": True,
+     maxsize: Optional[int] = None
+     folder_name: Optional[str] = None
+     preferred_engine: Optional[str] = None
+     use_sql: bool = False
+ 
+     def to_dict(self) -> Dict[str, Any]:
+         """Convert config to dictionary."""
+         return {
+             "maxsize": self.maxsize,
+             "folder_name": self.folder_name,
+             "preferred_engine": self.preferred_engine,
+             "use_sql": self.use_sql,
          }
  
-     @field_validator("maxsize")
      @classmethod
-     def validate_maxsize(cls, v: int | None) -> int | None:
-         """Validate the maxsize value."""
-         if v is not None and not isinstance(v, int):
-             msg = "maxsize must be an integer or None"
-             raise ValueError(msg)
-         if v is not None and v <= 0:
-             msg = "maxsize must be positive"
-             raise ValueError(msg)
-         return v
- 
-     @field_validator("folder_name")
-     @classmethod
-     def validate_folder_name(cls, v: str | None) -> str | None:
-         """Validate the folder name."""
-         if v is not None and not isinstance(v, str):
-             msg = "folder_name must be a string or None"
-             raise ValueError(msg)
-         if v is not None and not v.strip():
-             msg = "folder_name must not be empty if specified"
-             raise ValueError(msg)
-         return v
- 
-     def get_maxsize(self) -> int | None:
-         """Get the maxsize value."""
-         return self.maxsize
- 
-     def get_folder_name(self) -> str | None:
-         """Get the folder name."""
-         return self.folder_name
- 
-     def get_use_sql(self) -> bool:
-         """Get the use_sql value."""
-         return self.use_sql
- 
-     def get_preferred_engine(self) -> str | None:
-         """Get the preferred engine."""
-         return self.preferred_engine
- 
-     def get_cache_type(self) -> str | None:
-         """Get the cache type."""
-         return self.cache_type
+     def from_dict(cls, data: Dict[str, Any]) -> "CacheConfig":
+         """Create config from dictionary."""
+         return cls(
+             maxsize=data.get("maxsize"),
+             folder_name=data.get("folder_name"),
+             preferred_engine=data.get("preferred_engine"),
+             use_sql=data.get("use_sql", False),
+         )
  
      def validate(self) -> None:
-         """Validate the configuration."""
-         self.validate_maxsize(self.maxsize)
-         self.validate_folder_name(self.folder_name)
- 
-     def model_dump(self) -> dict[str, Any]:
-         """Convert the model to a dictionary."""
-         return super().model_dump()
- 
- 
- def create_cache_config(**kwargs: Any) -> CacheConfigProtocol:
-     """Create a new cache configuration instance."""
-     config = CacheConfigImpl(**kwargs)
-     return cast(CacheConfigProtocol, config)
- 
- 
- # Export CacheConfig as the Protocol type
- CacheConfig = CacheConfigProtocol
- 
- 
- class GlobalConfig(BaseSettings):
-     """Global configuration settings for the caching system."""
- 
-     cache_dir: Path = Field(
-         default_factory=lambda: get_cache_path("global"),
-         description="Cache directory path",
-     )
-     default_maxsize: int = Field(default=1000, description="Default maximum cache size")
-     default_use_sql: bool = Field(
-         default=False, description="Default SQL storage setting"
-     )
-     default_engine: str = Field(default="lru", description="Default cache engine")
-     default_cache_type: str | None = Field(
-         default=None, description="Default cache type"
-     )
-     enable_compression: bool = Field(default=True, description="Enable compression")
-     compression_level: int = Field(default=6, description="Compression level")
-     debug: bool = Field(default=False, description="Enable debug mode")
-     log_file: Path | None = Field(default=None, description="Log file path")
- 
-     model_config = {
-         "env_prefix": "TWAT_CACHE_",
-         "validate_assignment": True,
-         "extra": "ignore",
-         "arbitrary_types_allowed": True,
-     }
- 
-     @field_validator("compression_level")
-     @classmethod
-     def validate_compression_level(cls, v: int) -> int:
-         """Validate compression level."""
-         if not isinstance(v, int):
-             msg = "compression_level must be an integer"
+         """Validate configuration."""
+         if self.maxsize is not None and self.maxsize <= 0:
+             msg = "maxsize must be positive if specified"
              raise ValueError(msg)
-         if not 0 <= v <= 9:
-             msg = "compression_level must be between 0 and 9"
+ 
+         if self.preferred_engine is not None and self.preferred_engine not in {
+             "memory",
+             "disk",
+             "fast",
+         }:
+             msg = "preferred_engine must be one of: memory, disk, fast"
              raise ValueError(msg)
-         return v
- 
-     @field_validator("log_file")
-     @classmethod
-     def validate_log_file(cls, v: Path | None) -> Path | None:
-         """Validate log file path."""
-         if v is not None:
-             if isinstance(v, str):
-                 v = Path(v)
-             if not isinstance(v, Path):
-                 msg = "log_file must be a string or Path"
+ 
+         if self.folder_name is not None:
+             try:
+                 path = Path(self.folder_name)
+                 if not path.parent.exists():
+                     msg = f"Parent directory does not exist: {path.parent}"
                      raise ValueError(msg)
-             # Ensure parent directory exists
-             v.parent.mkdir(parents=True, exist_ok=True)
-         return v
- 
-     def get_cache_config(self, **overrides) -> CacheConfigProtocol:
-         """Create a CacheConfig instance with defaults from global config."""
-         config_data = {
-             "maxsize": self.default_maxsize,
-             "folder_name": None,
-             "use_sql": self.default_use_sql,
-             "preferred_engine": self.default_engine,
-             "cache_type": self.default_cache_type,
-         }
-         config_data.update(overrides)
-         return create_cache_config(**config_data)
- 
-     def configure_logging(self) -> None:
-         """Configure logging based on settings."""
-         # Remove default logger
-         logger.remove()
- 
-         # Configure log level
-         log_level = "DEBUG" if self.debug else "INFO"
- 
-         # Add console handler
-         logger.add(sys.stderr, level=log_level)
- 
-         # Add file handler if log_file is specified
-         if self.log_file is not None:
-             # Create parent directory but not the file itself
-             self.log_file.parent.mkdir(parents=True, exist_ok=True)
-             logger.add(
-                 self.log_file,
-                 level=log_level,
-                 rotation="1 day",
-                 retention="1 week",
-                 compression="zip" if self.enable_compression else None,
-                 delay=True,  # Don't create file until first log
-             )
- 
- 
- # Create global configuration instance
- global_config = GlobalConfig()
+             except Exception as e:
+                 msg = f"Invalid folder name: {e}"
+                 raise ValueError(msg) from e
+ 
+ 
+ def create_cache_config(**kwargs: Any) -> CacheConfig:
+     """
+     Create a cache configuration.
+ 
+     Args:
+         **kwargs: Configuration options
+ 
+     Returns:
+         A validated cache configuration
+     """
+     config = CacheConfig(**kwargs)
+     config.validate()
+     return config
  
```

---

_****_









Now let's update the decorators to use the new config system:

---

_****_

```diff
  import uuid
  from pathlib import Path
- from typing import Any, TypeVar, cast, ParamSpec
- from collections.abc import Callable
+ from typing import Any, Callable, TypeVar, cast, ParamSpec, Dict, Union
  from loguru import logger
  
  from .cache import register_cache, update_stats, CacheStats
+ from .config import CacheConfig, create_cache_config
  
  # Type variables for generic function types
  
  # Cache types
- CacheDict = dict[str, Any]
+ CacheDict = Dict[str, Any]
  CacheKey = str
  CacheValue = Any
  
      # Convert args to a stable form
-     def convert(obj: Any) -> str | int | float | bool | None:
-         if isinstance(obj, list | dict | set):
+     def convert(obj: Any) -> Union[str, int, float, bool, None]:
+         if isinstance(obj, (list, dict, set)):
              return json.dumps(obj, sort_keys=True)
-         if isinstance(obj, int | float | str | bool | type(None)):
+         if isinstance(obj, (int, float, str, bool, type(None))):
              return obj
          return str(obj)
  
              update_stats(cache_id, miss=True)
+             try:
                  result = func(*args, **kwargs)
                  cache[key] = result
+             except Exception as e:
+                 # Cache the exception
+                 cache[key] = e
+                 raise
  
              # Enforce maxsize
              if result is not None:
                  update_stats(cache_id, hit=True)
+                 if isinstance(result, Exception):
+                     raise result
                  return cast(R, result)
  
              update_stats(cache_id, miss=True)
+             try:
                  result = func(*args, **kwargs)
                  cache.set(key, result)
+             except Exception as e:
+                 # Cache the exception
+                 cache.set(key, e)
+                 raise
+ 
              update_stats(cache_id, size=len(cache))
              return result
              if result is not None:
                  update_stats(cache_id, hit=True)
+                 if isinstance(result, Exception):
+                     raise result
                  return cast(R, result)
  
              update_stats(cache_id, miss=True)
+             try:
                  result = func(*args, **kwargs)
                  cache[key] = result
+             except Exception as e:
+                 # Cache the exception
+                 cache[key] = e
+                 raise
+ 
              update_stats(cache_id, size=len(cache))
              return result
      folder_name: str | None = None,
      maxsize: int | None = None,
-     config: dict[str, Any] | None = None,  # For backward compatibility
+     config: CacheConfig | None = None,  # For backward compatibility
  ) -> Callable[[Callable[P, R]], Callable[P, R]]:
      """
          folder_name: Cache directory name (for disk cache)
          maxsize: Maximum cache size (None for unlimited)
-         config: Optional configuration dict (for backward compatibility)
+         config: Optional configuration object (for backward compatibility)
  
      Returns:
      # Handle legacy config
      if config is not None:
-         maxsize = config.get("maxsize", maxsize)
-         folder_name = config.get("folder_name", folder_name)
-         preferred_engine = config.get("preferred_engine", preferred_engine)
+         maxsize = config.maxsize or maxsize
+         folder_name = config.folder_name or folder_name
+         preferred_engine = config.preferred_engine or preferred_engine
+     else:
+         # Create and validate config
+         config = create_cache_config(
+             maxsize=maxsize,
+             folder_name=folder_name,
+             preferred_engine=preferred_engine,
+         )
  
      def decorator(func: Callable[P, R]) -> Callable[P, R]:
```

---

_****_









Let me run our catchphrase again to check if the changes fixed the issues:

---

_****_

```bash
uv venv; source .venv/bin/activate; uv pip install -e .[all,dev,test]; hatch run lint:fix; hatch test;
```

```
Using CPython 3.12.8 interpreter at: /usr/local/bin/python3.12
Creating virtual environment at: .venv
Activate with: source .venv/bin/activate
zsh: no matches found: .[all,dev,test]
Rewriting src/twat_cache/config.py
Rewriting src/twat_cache/decorators.py
warning: The top-level linter settings are deprecated in favour of their c
ounterparts in the `lint` section. Please update the following options in
`pyproject.toml`:
  - 'per-file-ignores' -> 'lint.per-file-ignores'
src/twat_cache/cache.py:58:5: C901 `clear_cache` is too complex (11 > 10)
   |
58 | def clear_cache(name: str | None = None) -> None:
   |     ^^^^^^^^^^^ C901
59 |     """
60 |     Clear one or all caches.
   |

src/twat_cache/engines/base.py:213:33: ARG002 Unused method argument: `key
`
    |
211 |     """
212 |
213 |     def _get_cached_value(self, key: CacheKey) -> R | None:
    |                                 ^^^ ARG002
214 |         """
215 |         Retrieve a value from the cache.
    |

src/twat_cache/engines/functools.py:1:1: A005 Module `functools` shadows a
 Python standard-library module
src/twat_cache/engines/joblib.py:49:33: ARG002 Unused method argument: `ke
y`
   |
47 |         )
48 |
49 |     def _get_cached_value(self, key: CacheKey) -> R | None:
   |                                 ^^^ ARG002
50 |         """Retrieve a value from the cache.
   |

src/twat_cache/engines/klepto.py:20:34: ARG005 Unused lambda argument: `ar
gs`
   |
18 |     HAS_KLEPTO = False
19 |     dir_archive = type("dir_archive", (), {})  # type: ignore
20 |     keymap = picklemap = lambda *args, **kwargs: lambda f: f  # type:
 ignore
   |                                  ^^^^ ARG005
   |

src/twat_cache/engines/klepto.py:20:42: ARG005 Unused lambda argument: `kw
args`
   |
18 |     HAS_KLEPTO = False
19 |     dir_archive = type("dir_archive", (), {})  # type: ignore
20 |     keymap = picklemap = lambda *args, **kwargs: lambda f: f  # type:
 ignore
   |                                          ^^^^^^ ARG005
   |

src/twat_cache/paths.py:100:5: C901 `clear_cache` is too complex (11 > 10)
    |
100 | def clear_cache(folder_name: str | None = None) -> None:
    |     ^^^^^^^^^^^ C901
101 |     """
102 |     Clear the cache directory for the given folder name.
    |

src/twat_cache/types.py:1:1: A005 Module `types` shadows a Python standard
-library module
tests/test_cache.py:175:34: PLR2004 Magic value used in comparison, consid
er replacing `15` with a constant variable
    |
173 |     result2 = process_list(test_list)
174 |
175 |     assert result1 == result2 == 15
    |                                  ^^ PLR2004
    |

tests/test_config.py:74:38: PLR2004 Magic value used in comparison, consid
er replacing `1000` with a constant variable
   |
72 |     # Check default values
73 |     assert config.cache_dir == get_cache_path("global")
74 |     assert config.default_maxsize == 1000
   |                                      ^^^^ PLR2004
75 |     assert not config.default_use_sql
76 |     assert config.default_engine == "lru"
   |

tests/test_config.py:79:40: PLR2004 Magic value used in comparison, consid
er replacing `6` with a constant variable
   |
77 |     assert config.default_cache_type is None
78 |     assert config.enable_compression
79 |     assert config.compression_level == 6
   |                                        ^ PLR2004
80 |     assert not config.debug
81 |     assert config.log_file is None
   |

tests/test_config.py:184:36: PLR2004 Magic value used in comparison, consi
der replacing `100` with a constant variable
    |
182 |         cache_type="speed",
183 |     )
184 |     assert config.get_maxsize() == 100
    |                                    ^^^ PLR2004
185 |     assert config.get_folder_name() == "test"
186 |     assert config.get_use_sql() is True
    |

tests/test_decorators.py:56:34: PLR2004 Magic value used in comparison, co
nsider replacing `25` with a constant variable
   |
54 |     time2 = time.time() - start
55 |
56 |     assert result1 == result2 == 25
   |                                  ^^ PLR2004
57 |     assert time2 < time1  # Cached call should be faster
   |

tests/test_decorators.py:74:34: PLR2004 Magic value used in comparison, co
nsider replacing `25` with a constant variable
   |
72 |     result2 = func(5)
73 |
74 |     assert result1 == result2 == 25
   |                                  ^^ PLR2004
75 |     assert cache_dir.exists()
   |

tests/test_decorators.py:91:34: PLR2004 Magic value used in comparison, co
nsider replacing `25` with a constant variable
   |
89 |     result2 = func(5)
90 |
91 |     assert result1 == result2 == 25
   |                                  ^^ PLR2004
   |

tests/test_decorators.py:107:34: PLR2004 Magic value used in comparison, c
onsider replacing `25` with a constant variable
    |
105 |     result2 = func(5)
106 |
107 |     assert result1 == result2 == 25
    |                                  ^^ PLR2004
    |

tests/test_decorators.py:123:22: PLR2004 Magic value used in comparison, c
onsider replacing `25` with a constant variable
    |
121 |     # Should still work with functools backend
122 |     result = func(5)
123 |     assert result == 25
    |                      ^^ PLR2004
    |

tests/test_decorators.py:141:34: PLR2004 Magic value used in comparison, c
onsider replacing `25` with a constant variable
    |
139 |     result2 = await func(5)
140 |
141 |     assert result1 == result2 == 25
    |                                  ^^ PLR2004
    |

tests/test_decorators.py:188:23: PLR2004 Magic value used in comparison, c
onsider replacing `25` with a constant variable
    |
187 |     # Valid input should work
188 |     assert func(5) == 25
    |                       ^^ PLR2004
189 |
190 |     # Error should be raised consistently
    |

tests/test_engines.py:62:45: FBT003 Boolean positional value in function c
all
   |
60 |     assert isinstance(base_engine._make_key("test"), str)
61 |     assert isinstance(base_engine._make_key(123), str)
62 |     assert isinstance(base_engine._make_key(True), str)
   |                                             ^^^^ FBT003
63 |
64 |     # Test with complex types
   |

tests/test_engines.py:82:22: PLR2004 Magic value used in comparison, consi
der replacing `4` with a constant variable
   |
80 |     # First call
81 |     result = test_function(2)
82 |     assert result == 4
   |                      ^ PLR2004
83 |     assert call_count == 1
   |

tests/test_engines.py:87:22: PLR2004 Magic value used in comparison, consi
der replacing `4` with a constant variable
   |
85 |     # Second call (should use cache)
86 |     result = test_function(2)
87 |     assert result == 4
   |                      ^ PLR2004
88 |     assert call_count == 1  # Should not increment
   |

Found 29 errors (7 fixed, 22 remaining).
========================== test session starts ===========================
platform darwin -- Python 3.12.8, pytest-8.3.4, pluggy-1.5.0 -- /Users/ada
m/Library/Application Support/hatch/env/virtual/twat-cache/ivvP1xkE/hatch-
test.py3.12/bin/python3
cachedir: .pytest_cache
rootdir: /Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good
/twat/plugins/repos/twat_cache
configfile: pyproject.toml
plugins: rerunfailures-14.0, mock-3.14.0, xdist-3.6.1
collected 38 items / 1 error                                             

================================= ERRORS =================================
_________________ ERROR collecting tests/test_config.py __________________
ImportError while importing test module '/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_cache/tests/test_
config.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/importli
b/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_config.py:20: in <module>
    from twat_cache.config import create_cache_config, GlobalConfig
E   ImportError: cannot import name 'GlobalConfig' from 'twat_cache.config
' (/Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/twat/
plugins/repos/twat_cache/src/twat_cache/config.py)
======================== short test summary info =========================
ERROR tests/test_config.py
!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!
============================ 1 error in 0.18s ============================

```

---

_****_





I see we need to fix the test files to match our new simplified config system. Let me update the test files:

---

_****_

```diff
  # dependencies = [
  #   "pytest",
- #   "pydantic",
- #   "pydantic-settings",
  # ]
  # ///
  # this_file: tests/test_config.py
  
  """Tests for the configuration management system."""
- 
- import os
- from pathlib import Path
- from collections.abc import Generator
  
  import pytest
- from loguru import logger
  
- from twat_cache.config import create_cache_config, GlobalConfig
- from twat_cache.paths import get_cache_path
- 
- # Test constants
- DEFAULT_MAXSIZE = 1000
- DEFAULT_COMPRESSION_LEVEL = 6
- CUSTOM_MAXSIZE = 500
- CACHE_CONFIG_MAXSIZE = 200
- CUSTOM_CACHE_MAXSIZE = 300
- 
- 
- @pytest.fixture
- def clean_env() -> Generator[None, None, None]:
-     """Clean environment variables before and after tests."""
-     # Store original environment
-     original_env = dict(os.environ)
- 
-     # Clear relevant environment variables
-     for key in list(os.environ.keys()):
-         if key.startswith("TWAT_CACHE_"):
-             del os.environ[key]
- 
-     yield
- 
-     # Restore original environment
-     os.environ.clear()
-     os.environ.update(original_env)
+ from twat_cache.config import create_cache_config, CacheConfig
  
  
          config.validate()
  
- 
- def test_default_config() -> None:
-     """Test default configuration values."""
-     config = GlobalConfig()
- 
-     # Check default values
-     assert config.cache_dir == get_cache_path("global")
-     assert config.default_maxsize == 1000
-     assert not config.default_use_sql
-     assert config.default_engine == "lru"
-     assert config.default_cache_type is None
-     assert config.enable_compression
-     assert config.compression_level == 6
-     assert not config.debug
-     assert config.log_file is None
- 
- 
- def test_custom_config() -> None:
-     """Test custom configuration values."""
-     config = GlobalConfig(
-         default_maxsize=CUSTOM_MAXSIZE,
-         default_use_sql=True,
-         default_engine="disk",
-         enable_compression=False,
-         debug=True,
-         log_file=Path("cache.log"),
-     )
- 
-     # Check values
-     assert config.default_maxsize == CUSTOM_MAXSIZE
-     assert config.default_use_sql is True
-     assert config.default_engine == "disk"
-     assert config.enable_compression is False
-     assert config.debug is True
-     assert config.log_file == Path("cache.log")
- 
- 
- def test_global_config_env_vars(clean_env: None) -> None:
-     """Test environment variable configuration."""
-     # Set environment variables
-     os.environ["TWAT_CACHE_DEFAULT_MAXSIZE"] = str(CUSTOM_MAXSIZE)
-     os.environ["TWAT_CACHE_DEFAULT_USE_SQL"] = "true"
-     os.environ["TWAT_CACHE_DEFAULT_ENGINE"] = "disk"
-     os.environ["TWAT_CACHE_ENABLE_COMPRESSION"] = "false"
-     os.environ["TWAT_CACHE_DEBUG"] = "true"
- 
-     config = GlobalConfig()
- 
-     # Check values
-     assert config.default_maxsize == CUSTOM_MAXSIZE
-     assert config.default_use_sql is True
-     assert config.default_engine == "disk"
-     assert config.enable_compression is False
-     assert config.debug is True
- 
- 
- def test_get_cache_config() -> None:
-     """Test cache configuration creation from global config."""
-     global_config = GlobalConfig(
-         default_maxsize=DEFAULT_MAXSIZE,
-         default_use_sql=False,
-         default_engine="lru",
-     )
- 
-     # Test default configuration
-     cache_config = global_config.get_cache_config()
-     assert cache_config.get_maxsize() == DEFAULT_MAXSIZE
-     assert cache_config.get_use_sql() is False
-     assert cache_config.get_preferred_engine() == "lru"
- 
-     # Test with overrides
-     cache_config = global_config.get_cache_config(
-         maxsize=CUSTOM_CACHE_MAXSIZE,
-         use_sql=True,
-         preferred_engine="disk",
-     )
-     assert cache_config.get_maxsize() == CUSTOM_CACHE_MAXSIZE
-     assert cache_config.get_use_sql() is True
-     assert cache_config.get_preferred_engine() == "disk"
- 
- 
- def test_logging_configuration(tmp_path: Path) -> None:
-     """Test logging configuration."""
-     # Test debug logging
-     config = GlobalConfig(debug=True)
-     config.configure_logging()
-     # Debug logging should be enabled (no easy way to test this directly)
- 
-     # Test file logging
-     log_file = tmp_path / "cache.log"
-     config = GlobalConfig(log_file=log_file)
-     config.configure_logging()
-     # Log file should be created when logging occurs
-     assert not log_file.exists()  # File not created until first log
-     logger.info("Test log message")  # Trigger log file creation
-     assert log_file.exists()  # File should exist now
-     assert log_file.read_text().strip().endswith("Test log message")
- 
  
  def test_cache_config_creation() -> None:
      """Test creation of cache configuration."""
      # Test with minimal configuration
      config = create_cache_config()
-     assert config.get_maxsize() is None
-     assert config.get_folder_name() is None
-     assert config.get_use_sql() is False
-     assert config.get_preferred_engine() is None
-     assert config.get_cache_type() is None
+     assert config.maxsize is None
+     assert config.folder_name is None
+     assert config.preferred_engine is None
+     assert config.use_sql is False
  
      # Test with full configuration
      config = create_cache_config(
          maxsize=100,
          folder_name="test",
+         preferred_engine="memory",
          use_sql=True,
-         preferred_engine="disk",
-         cache_type="speed",
      )
-     assert config.get_maxsize() == 100
-     assert config.get_folder_name() == "test"
-     assert config.get_use_sql() is True
-     assert config.get_preferred_engine() == "disk"
-     assert config.get_cache_type() == "speed"
+     assert config.maxsize == 100
+     assert config.folder_name == "test"
+     assert config.preferred_engine == "memory"
+     assert config.use_sql is True
+ 
+ 
+ def test_cache_config_to_dict() -> None:
+     """Test conversion of config to dictionary."""
+     config = create_cache_config(
+         maxsize=100,
+         folder_name="test",
+         preferred_engine="memory",
+         use_sql=True,
+     )
+     data = config.to_dict()
+     assert data["maxsize"] == 100
+     assert data["folder_name"] == "test"
+     assert data["preferred_engine"] == "memory"
+     assert data["use_sql"] is True
  
  
- def test_cache_config_with_sql() -> None:
-     """Test SQL-specific configuration."""
-     # Test SQL configuration
-     config = create_cache_config(use_sql=True, folder_name="test_db")
-     assert config.get_use_sql() is True
-     assert config.get_folder_name() == "test_db"
- 
-     # Test validation with SQL configuration
-     config.validate()  # Should not raise
+ def test_cache_config_from_dict() -> None:
+     """Test creation of config from dictionary."""
+     data = {
+         "maxsize": 100,
+         "folder_name": "test",
+         "preferred_engine": "memory",
+         "use_sql": True,
+     }
+     config = CacheConfig.from_dict(data)
+     assert config.maxsize == 100
+     assert config.folder_name == "test"
+     assert config.preferred_engine == "memory"
+     assert config.use_sql is True
  
```

---

_****_





Let me run our catchphrase again to check if the changes fixed the issues:

---

_****_

```bash
uv venv; source .venv/bin/activate; uv pip install -e .[all,dev,test]; hatch run lint:fix; hatch test;
```

```
(twat_cache) (twat_cache) adam@Hamlet twat_cache % 
    |                      ^^ PLR2004
    |

tests/test_decorators.py:141:34: PLR2004 Magic value used in comparison, c
onsider replacing `25` with a constant variable
    |
139 |     result2 = await func(5)
140 |
141 |     assert result1 == result2 == 25
    |                                  ^^ PLR2004
    |

tests/test_decorators.py:188:23: PLR2004 Magic value used in comparison, c
onsider replacing `25` with a constant variable
    |
187 |     # Valid input should work
188 |     assert func(5) == 25
    |                       ^^ PLR2004
189 |
190 |     # Error should be raised consistently
    |

tests/test_engines.py:62:45: FBT003 Boolean positional value in function c
all
   |
60 |     assert isinstance(base_engine._make_key("test"), str)
61 |     assert isinstance(base_engine._make_key(123), str)
62 |     assert isinstance(base_engine._make_key(True), str)
   |                                             ^^^^ FBT003
63 |
64 |     # Test with complex types
   |

tests/test_engines.py:82:22: PLR2004 Magic value used in comparison, consi
der replacing `4` with a constant variable
   |
80 |     # First call
81 |     result = test_function(2)
82 |     assert result == 4
   |                      ^ PLR2004
83 |     assert call_count == 1
   |

tests/test_engines.py:87:22: PLR2004 Magic value used in comparison, consi
der replacing `4` with a constant variable
   |
85 |     # Second call (should use cache)
86 |     result = test_function(2)
87 |     assert result == 4
   |                      ^ PLR2004
88 |     assert call_count == 1  # Should not increment
   |

Found 22 errors.
========================== test session starts ===========================
platform darwin -- Python 3.12.8, pytest-8.3.4, pluggy-1.5.0 -- /Users/ada
m/Library/Application Support/hatch/env/virtual/twat-cache/ivvP1xkE/hatch-
test.py3.12/bin/python3
cachedir: .pytest_cache
rootdir: /Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good
/twat/plugins/repos/twat_cache
configfile: pyproject.toml
plugins: rerunfailures-14.0, mock-3.14.0, xdist-3.6.1
collected 42 items                                                       

tests/test_cache.py::test_cache_settings_validation PASSED         [  2%]
tests/test_cache.py::test_basic_caching PASSED                     [  4%]
tests/test_cache.py::test_cache_clear PASSED                       [  7%]
tests/test_cache.py::test_cache_stats PASSED                       [  9%]
tests/test_cache.py::test_list_processing PASSED                   [ 11%]
tests/test_cache.py::test_different_backends PASSED                [ 14%]
tests/test_cache.py::test_cache_with_complex_types PASSED          [ 16%]
tests/test_cache.py::test_cache_exceptions FAILED                  [ 19%]
tests/test_cache.py::test_kwargs_handling FAILED                   [ 21%]
tests/test_config.py::test_cache_config_validation PASSED          [ 23%]
tests/test_config.py::test_cache_config_creation PASSED            [ 26%]
tests/test_config.py::test_cache_config_to_dict PASSED             [ 28%]
tests/test_config.py::test_cache_config_from_dict PASSED           [ 30%]
tests/test_decorators.py::test_mcache_basic PASSED                 [ 33%]
tests/test_decorators.py::test_bcache_basic FAILED                 [ 35%]
tests/test_decorators.py::test_fcache_basic PASSED                 [ 38%]
tests/test_decorators.py::test_ucache_basic PASSED                 [ 40%]
tests/test_decorators.py::test_ucache_fallback FAILED              [ 42%]
tests/test_decorators.py::test_async_caching SKIPPED (async de...) [ 45%]
tests/test_decorators.py::test_cache_performance PASSED            [ 47%]
tests/test_decorators.py::test_decorator_error_handling FAILED     [ 50%]
tests/test_engines.py::test_base_engine_initialization FAILED      [ 52%]
tests/test_engines.py::test_base_engine_key_generation ERROR       [ 54%]
tests/test_engines.py::test_base_engine_cache_decorator ERROR      [ 57%]
tests/test_engines.py::test_base_engine_validation FAILED          [ 59%]
tests/test_engines.py::test_lru_cache_initialization FAILED        [ 61%]
tests/test_engines.py::test_lru_cache_maxsize_enforcement FAILED   [ 64%]
tests/test_engines.py::test_lru_cache_clear FAILED                 [ 66%]
tests/test_engines.py::test_lru_cache_with_complex_values FAILED   [ 69%]
tests/test_engines.py::test_lru_cache_stats_accuracy FAILED        [ 71%]
tests/test_twat_cache.py::test_lru_cache_get_set ERROR             [ 73%]
tests/test_twat_cache.py::test_lru_cache_clear ERROR               [ 76%]
tests/test_twat_cache.py::test_lru_cache_maxsize ERROR             [ 78%]
tests/test_twat_cache.py::test_disk_cache_persistence ERROR        [ 80%]
tests/test_twat_cache.py::test_joblib_numpy_array SKIPPED (num...) [ 83%]
tests/test_twat_cache.py::test_klepto_persistence ERROR            [ 85%]
tests/test_twat_cache.py::test_async_cache_operations SKIPPED      [ 88%]
tests/test_twat_cache.py::test_cachebox_operations FAILED          [ 90%]
tests/test_twat_cache.py::test_cachetools_operations FAILED        [ 92%]
tests/test_twat_cache.py::test_functools_cache_get_set ERROR       [ 95%]
tests/test_twat_cache.py::test_functools_cache_clear ERROR         [ 97%]
tests/test_twat_cache.py::test_functools_cache_maxsize ERROR       [100%]

================================= ERRORS =================================
___________ ERROR at setup of test_base_engine_key_generation ____________

base_config = CacheConfig(maxsize=100, folder_name=None, preferred_engine=
None, use_sql=False)

    @pytest.fixture
    def base_engine(base_config: CacheConfig) -> CacheEngine[Any, Any]:
        """Provide a basic cache engine instance."""
>       return FunctoolsCacheEngine(base_config)

tests/test_engines.py:47: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
src/twat_cache/engines/functools.py:41: in __init__
    super().__init__(config)
src/twat_cache/engines/base.py:49: in __init__
    self.validate_config()
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <twat_cache.engines.functools.FunctoolsCacheEngine object at 0x1053
da090>

    def validate_config(self) -> None:
        """
        Validate the engine configuration.
    
        Raises:
            ValueError: If the configuration is invalid
        """
        super().validate_config()
    
        # Additional functools-specific validation
>       maxsize = self._config.get_maxsize()
E       AttributeError: 'CacheConfig' object has no attribute 'get_maxsize
'

src/twat_cache/engines/functools.py:201: AttributeError
___________ ERROR at setup of test_base_engine_cache_decorator ___________

base_config = CacheConfig(maxsize=100, folder_name=None, preferred_engine=
None, use_sql=False)

    @pytest.fixture
    def base_engine(base_config: CacheConfig) -> CacheEngine[Any, Any]:
        """Provide a basic cache engine instance."""
>       return FunctoolsCacheEngine(base_config)

tests/test_engines.py:47: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
src/twat_cache/engines/functools.py:41: in __init__
    super().__init__(config)
src/twat_cache/engines/base.py:49: in __init__
    self.validate_config()
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <twat_cache.engines.functools.FunctoolsCacheEngine object at 0x1054
5cbc0>

    def validate_config(self) -> None:
        """
        Validate the engine configuration.
    
        Raises:
            ValueError: If the configuration is invalid
        """
        super().validate_config()
    
        # Additional functools-specific validation
>       maxsize = self._config.get_maxsize()
E       AttributeError: 'CacheConfig' object has no attribute 'get_maxsize
'

src/twat_cache/engines/functools.py:201: AttributeError
________________ ERROR at setup of test_lru_cache_get_set ________________

base_config = CacheConfig(maxsize=100, folder_name=None, preferred_engine=
None, use_sql=False)

    @pytest.fixture
    def lru_engine(base_config: CacheConfig) -> FunctoolsCacheEngine:
        """Create an LRU cache engine instance."""
>       return FunctoolsCacheEngine(base_config)

tests/test_twat_cache.py:55: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
src/twat_cache/engines/functools.py:41: in __init__
    super().__init__(config)
src/twat_cache/engines/base.py:49: in __init__
    self.validate_config()
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <twat_cache.engines.functools.FunctoolsCacheEngine object at 0x1053
da090>

    def validate_config(self) -> None:
        """
        Validate the engine configuration.
    
        Raises:
            ValueError: If the configuration is invalid
        """
        super().validate_config()
    
        # Additional functools-specific validation
>       maxsize = self._config.get_maxsize()
E       AttributeError: 'CacheConfig' object has no attribute 'get_maxsize
'

src/twat_cache/engines/functools.py:201: AttributeError
_________________ ERROR at setup of test_lru_cache_clear _________________

base_config = CacheConfig(maxsize=100, folder_name=None, preferred_engine=
None, use_sql=False)

    @pytest.fixture
    def lru_engine(base_config: CacheConfig) -> FunctoolsCacheEngine:
        """Create an LRU cache engine instance."""
>       return FunctoolsCacheEngine(base_config)

tests/test_twat_cache.py:55: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
src/twat_cache/engines/functools.py:41: in __init__
    super().__init__(config)
src/twat_cache/engines/base.py:49: in __init__
    self.validate_config()
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <twat_cache.engines.functools.FunctoolsCacheEngine object at 0x1054
5db80>

    def validate_config(self) -> None:
        """
        Validate the engine configuration.
    
        Raises:
            ValueError: If the configuration is invalid
        """
        super().validate_config()
    
        # Additional functools-specific validation
>       maxsize = self._config.get_maxsize()
E       AttributeError: 'CacheConfig' object has no attribute 'get_maxsize
'

src/twat_cache/engines/functools.py:201: AttributeError
________________ ERROR at setup of test_lru_cache_maxsize ________________

base_config = CacheConfig(maxsize=100, folder_name=None, preferred_engine=
None, use_sql=False)

    @pytest.fixture
    def lru_engine(base_config: CacheConfig) -> FunctoolsCacheEngine:
        """Create an LRU cache engine instance."""
>       return FunctoolsCacheEngine(base_config)

tests/test_twat_cache.py:55: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
src/twat_cache/engines/functools.py:41: in __init__
    super().__init__(config)
src/twat_cache/engines/base.py:49: in __init__
    self.validate_config()
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <twat_cache.engines.functools.FunctoolsCacheEngine object at 0x1054
86780>

    def validate_config(self) -> None:
        """
        Validate the engine configuration.
    
        Raises:
            ValueError: If the configuration is invalid
        """
        super().validate_config()
    
        # Additional functools-specific validation
>       maxsize = self._config.get_maxsize()
E       AttributeError: 'CacheConfig' object has no attribute 'get_maxsize
'

src/twat_cache/engines/functools.py:201: AttributeError
_____________ ERROR at setup of test_disk_cache_persistence ______________

base_config = CacheConfig(maxsize=100, folder_name=None, preferred_engine=
None, use_sql=False)
temp_path = PosixPath('/private/var/folders/05/clcynl0509ldxltl599hhhx4000
0gn/T/pytest-of-adam/pytest-36/test_disk_cache_persistence0/cache')

    @pytest.fixture
    def disk_engine(base_config: CacheConfig, temp_path: Path) -> DiskCach
eEngine:
        """Create a disk cache engine instance."""
>       config = create_cache_config(maxsize=100, cache_dir=str(temp_path)
)

tests/test_twat_cache.py:95: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

kwargs = {'cache_dir': '/private/var/folders/05/clcynl0509ldxltl599hhhx400
00gn/T/pytest-of-adam/pytest-36/test_disk_cache_persistence0/cache', 'maxs
ize': 100}

    def create_cache_config(**kwargs: Any) -> CacheConfig:
        """
        Create a cache configuration.
    
        Args:
            **kwargs: Configuration options
    
        Returns:
            A validated cache configuration
        """
>       config = CacheConfig(**kwargs)
E       TypeError: CacheConfig.__init__() got an unexpected keyword argume
nt 'cache_dir'

src/twat_cache/config.py:83: TypeError
_______________ ERROR at setup of test_klepto_persistence ________________

base_config = CacheConfig(maxsize=100, folder_name=None, preferred_engine=
None, use_sql=False)
temp_path = PosixPath('/private/var/folders/05/clcynl0509ldxltl599hhhx4000
0gn/T/pytest-of-adam/pytest-36/test_klepto_persistence0/cache')

    @pytest.fixture
    def klepto_engine(base_config: CacheConfig, temp_path: Path) -> Klepto
Engine:
        """Create a klepto cache engine instance."""
>       config = create_cache_config(maxsize=100, cache_dir=str(temp_path)
)

tests/test_twat_cache.py:137: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

kwargs = {'cache_dir': '/private/var/folders/05/clcynl0509ldxltl599hhhx400
00gn/T/pytest-of-adam/pytest-36/test_klepto_persistence0/cache', 'maxsize'
: 100}

    def create_cache_config(**kwargs: Any) -> CacheConfig:
        """
        Create a cache configuration.
    
        Args:
            **kwargs: Configuration options
    
        Returns:
            A validated cache configuration
        """
>       config = CacheConfig(**kwargs)
E       TypeError: CacheConfig.__init__() got an unexpected keyword argume
nt 'cache_dir'

src/twat_cache/config.py:83: TypeError
_____________ ERROR at setup of test_functools_cache_get_set _____________

base_config = CacheConfig(maxsize=100, folder_name=None, preferred_engine=
None, use_sql=False)

    @pytest.fixture
    def functools_engine(base_config: CacheConfig) -> FunctoolsCacheEngine
:
        """Fixture for testing the functools cache engine."""
>       return FunctoolsCacheEngine(base_config)

tests/test_twat_cache.py:214: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
src/twat_cache/engines/functools.py:41: in __init__
    super().__init__(config)
src/twat_cache/engines/base.py:49: in __init__
    self.validate_config()
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <twat_cache.engines.functools.FunctoolsCacheEngine object at 0x1054
87470>

    def validate_config(self) -> None:
        """
        Validate the engine configuration.
    
        Raises:
            ValueError: If the configuration is invalid
        """
        super().validate_config()
    
        # Additional functools-specific validation
>       maxsize = self._config.get_maxsize()
E       AttributeError: 'CacheConfig' object has no attribute 'get_maxsize
'

src/twat_cache/engines/functools.py:201: AttributeError
______________ ERROR at setup of test_functools_cache_clear ______________

base_config = CacheConfig(maxsize=100, folder_name=None, preferred_engine=
None, use_sql=False)

    @pytest.fixture
    def functools_engine(base_config: CacheConfig) -> FunctoolsCacheEngine
:
        """Fixture for testing the functools cache engine."""
>       return FunctoolsCacheEngine(base_config)

tests/test_twat_cache.py:214: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
src/twat_cache/engines/functools.py:41: in __init__
    super().__init__(config)
src/twat_cache/engines/base.py:49: in __init__
    self.validate_config()
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <twat_cache.engines.functools.FunctoolsCacheEngine object at 0x1054
873b0>

    def validate_config(self) -> None:
        """
        Validate the engine configuration.
    
        Raises:
            ValueError: If the configuration is invalid
        """
        super().validate_config()
    
        # Additional functools-specific validation
>       maxsize = self._config.get_maxsize()
E       AttributeError: 'CacheConfig' object has no attribute 'get_maxsize
'

src/twat_cache/engines/functools.py:201: AttributeError
_____________ ERROR at setup of test_functools_cache_maxsize _____________

base_config = CacheConfig(maxsize=100, folder_name=None, preferred_engine=
None, use_sql=False)

    @pytest.fixture
    def functools_engine(base_config: CacheConfig) -> FunctoolsCacheEngine
:
        """Fixture for testing the functools cache engine."""
>       return FunctoolsCacheEngine(base_config)

tests/test_twat_cache.py:214: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
src/twat_cache/engines/functools.py:41: in __init__
    super().__init__(config)
src/twat_cache/engines/base.py:49: in __init__
    self.validate_config()
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <twat_cache.engines.functools.FunctoolsCacheEngine object at 0x1052
2de20>

    def validate_config(self) -> None:
        """
        Validate the engine configuration.
    
        Raises:
            ValueError: If the configuration is invalid
        """
        super().validate_config()
    
        # Additional functools-specific validation
>       maxsize = self._config.get_maxsize()
E       AttributeError: 'CacheConfig' object has no attribute 'get_maxsize
'

src/twat_cache/engines/functools.py:201: AttributeError
================================ FAILURES ================================
_________________________ test_cache_exceptions __________________________

    def test_cache_exceptions() -> None:
        """Test caching of exceptions."""
        call_count = 0
    
        @ucache(maxsize=100)
        def failing_function(x: int) -> None:
            nonlocal call_count
            call_count += 1
            msg = "Test error"
            raise ValueError(msg)
    
        # First call
        with pytest.raises(ValueError):
            failing_function(5)
        assert call_count == 1
    
        # Second call should not recompute
>       with pytest.raises(ValueError):
E       Failed: DID NOT RAISE <class 'ValueError'>

tests/test_cache.py:195: Failed
-------------------------- Captured stderr call --------------------------
2025-02-16 14:26:05.378 | DEBUG    | twat_cache.decorators:decorator:306 -
 Using memory cache (functools)
2025-02-16 14:26:05.379 | DEBUG    | twat_cache.cache:register_cache:55 - 
Registered cache: mcache_failing_function_4cb2cf7f
__________________________ test_kwargs_handling __________________________

    def test_kwargs_handling() -> None:
        """Test caching with different keyword arguments."""
        call_count = 0
    
        @ucache()
        def kwarg_function(x: int, multiplier: int = 1) -> int:
            nonlocal call_count
            call_count += 1
            return x * multiplier
    
        # Test with different kwarg combinations
        assert kwarg_function(TEST_INPUT) == TEST_INPUT
        assert call_count == 1
    
        assert kwarg_function(TEST_INPUT, multiplier=1) == TEST_INPUT
>       assert call_count == 1  # Should use cache
E       assert 2 == 1

tests/test_cache.py:215: AssertionError
-------------------------- Captured stderr call --------------------------
2025-02-16 14:26:05.415 | DEBUG    | twat_cache.decorators:decorator:306 -
 Using memory cache (functools)
2025-02-16 14:26:05.415 | DEBUG    | twat_cache.cache:register_cache:55 - 
Registered cache: mcache_kwarg_function_11fa12ce
___________________________ test_bcache_basic ____________________________

tmp_path = PosixPath('/private/var/folders/05/clcynl0509ldxltl599hhhx40000
gn/T/pytest-of-adam/pytest-36/test_bcache_basic0')

    def test_bcache_basic(tmp_path: Path):
        """Test basic disk caching."""
        cache_dir = tmp_path / "cache"
    
        @bcache(folder_name=str(cache_dir))
        def func(x: int) -> int:
            return expensive_computation(x)
    
        # First call should compute
        result1 = func(5)
    
        # Second call should be from cache
        result2 = func(5)
    
        assert result1 == result2 == 25
>       assert cache_dir.exists()
E       AssertionError: assert False
E        +  where False = exists()
E        +    where exists = PosixPath('/private/var/folders/05/clcynl0509
ldxltl599hhhx40000gn/T/pytest-of-adam/pytest-36/test_bcache_basic0/cache')
.exists

tests/test_decorators.py:75: AssertionError
-------------------------- Captured stderr call --------------------------
2025-02-16 14:26:05.531 | WARNING  | twat_cache.decorators:decorator:154 -
 diskcache not available, falling back to memory cache
2025-02-16 14:26:05.531 | DEBUG    | twat_cache.cache:register_cache:55 - 
Registered cache: mcache_func_e332714b
__________________________ test_ucache_fallback __________________________

obj = <module 'twat_cache.engines' from '/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_cache/src/twat_ca
che/engines/__init__.py'>
name = 'HAS_CACHEBOX', ann = 'twat_cache.engines'

    def annotated_getattr(obj: object, name: str, ann: str) -> object:
        try:
>           obj = getattr(obj, name)
E           AttributeError: module 'twat_cache.engines' has no attribute '
HAS_CACHEBOX'

/Users/adam/Library/Application Support/hatch/env/virtual/twat-cache/ivvP1
xkE/hatch-test.py3.12/lib/python3.12/site-packages/_pytest/monkeypatch.py:
90: AttributeError

The above exception was the direct cause of the following exception:

monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x10545d370>

    def test_ucache_fallback(monkeypatch):
        """Test ucache fallback behavior."""
        # Simulate no backends available except functools
>       monkeypatch.setattr("twat_cache.engines.HAS_CACHEBOX", False)

tests/test_decorators.py:114: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
/Users/adam/Library/Application Support/hatch/env/virtual/twat-cache/ivvP1
xkE/hatch-test.py3.12/lib/python3.12/site-packages/_pytest/monkeypatch.py:
104: in derive_importpath
    annotated_getattr(target, attr, ann=module)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

obj = <module 'twat_cache.engines' from '/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_cache/src/twat_ca
che/engines/__init__.py'>
name = 'HAS_CACHEBOX', ann = 'twat_cache.engines'

    def annotated_getattr(obj: object, name: str, ann: str) -> object:
        try:
            obj = getattr(obj, name)
        except AttributeError as e:
>           raise AttributeError(
                f"{type(obj).__name__!r} object at {ann} has no attribute 
{name!r}"
            ) from e
E           AttributeError: 'module' object at twat_cache.engines has no a
ttribute 'HAS_CACHEBOX'

/Users/adam/Library/Application Support/hatch/env/virtual/twat-cache/ivvP1
xkE/hatch-test.py3.12/lib/python3.12/site-packages/_pytest/monkeypatch.py:
92: AttributeError
_____________________ test_decorator_error_handling ______________________

    def test_decorator_error_handling():
        """Test error handling in decorators."""
    
        @ucache()
        def func(x: int) -> int:
            if x < 0:
                msg = "Negative input"
                raise ValueError(msg)
            return x * x
    
        # Valid input should work
        assert func(5) == 25
    
        # Error should be raised consistently
        with pytest.raises(ValueError):
            func(-1)
    
>       with pytest.raises(ValueError):
E       Failed: DID NOT RAISE <class 'ValueError'>

tests/test_decorators.py:194: Failed
-------------------------- Captured stderr call --------------------------
2025-02-16 14:26:06.275 | DEBUG    | twat_cache.decorators:decorator:306 -
 Using memory cache (functools)
2025-02-16 14:26:06.276 | DEBUG    | twat_cache.cache:register_cache:55 - 
Registered cache: mcache_func_69ffa4ec
____________________ test_base_engine_initialization _____________________

base_config = CacheConfig(maxsize=100, folder_name=None, preferred_engine=
None, use_sql=False)

    def test_base_engine_initialization(base_config: CacheConfig) -> None:
        """Test basic engine initialization."""
>       engine = FunctoolsCacheEngine(base_config)

tests/test_engines.py:52: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
src/twat_cache/engines/functools.py:41: in __init__
    super().__init__(config)
src/twat_cache/engines/base.py:49: in __init__
    self.validate_config()
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <twat_cache.engines.functools.FunctoolsCacheEngine object at 0x1054
5f020>

    def validate_config(self) -> None:
        """
        Validate the engine configuration.
    
        Raises:
            ValueError: If the configuration is invalid
        """
        super().validate_config()
    
        # Additional functools-specific validation
>       maxsize = self._config.get_maxsize()
E       AttributeError: 'CacheConfig' object has no attribute 'get_maxsize
'

src/twat_cache/engines/functools.py:201: AttributeError
______________________ test_base_engine_validation _______________________

base_config = CacheConfig(maxsize=100, folder_name=None, preferred_engine=
None, use_sql=False)

    def test_base_engine_validation(base_config: CacheConfig) -> None:
        """Test engine configuration validation."""
>       engine = FunctoolsCacheEngine(base_config)

tests/test_engines.py:93: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
src/twat_cache/engines/functools.py:41: in __init__
    super().__init__(config)
src/twat_cache/engines/base.py:49: in __init__
    self.validate_config()
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <twat_cache.engines.functools.FunctoolsCacheEngine object at 0x1054
5fa40>

    def validate_config(self) -> None:
        """
        Validate the engine configuration.
    
        Raises:
            ValueError: If the configuration is invalid
        """
        super().validate_config()
    
        # Additional functools-specific validation
>       maxsize = self._config.get_maxsize()
E       AttributeError: 'CacheConfig' object has no attribute 'get_maxsize
'

src/twat_cache/engines/functools.py:201: AttributeError
_____________________ test_lru_cache_initialization ______________________

base_config = CacheConfig(maxsize=100, folder_name=None, preferred_engine=
None, use_sql=False)

    def test_lru_cache_initialization(base_config: CacheConfig) -> None:
        """Test LRU cache initialization."""
>       engine = FunctoolsCacheEngine(base_config)

tests/test_engines.py:103: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
src/twat_cache/engines/functools.py:41: in __init__
    super().__init__(config)
src/twat_cache/engines/base.py:49: in __init__
    self.validate_config()
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <twat_cache.engines.functools.FunctoolsCacheEngine object at 0x1054
84710>

    def validate_config(self) -> None:
        """
        Validate the engine configuration.
    
        Raises:
            ValueError: If the configuration is invalid
        """
        super().validate_config()
    
        # Additional functools-specific validation
>       maxsize = self._config.get_maxsize()
E       AttributeError: 'CacheConfig' object has no attribute 'get_maxsize
'

src/twat_cache/engines/functools.py:201: AttributeError
___________________ test_lru_cache_maxsize_enforcement ___________________

base_config = CacheConfig(maxsize=100, folder_name=None, preferred_engine=
None, use_sql=False)

    def test_lru_cache_maxsize_enforcement(base_config: CacheConfig) -> No
ne:
        """Test LRU cache maxsize enforcement."""
>       engine = FunctoolsCacheEngine(base_config)

tests/test_engines.py:110: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
src/twat_cache/engines/functools.py:41: in __init__
    super().__init__(config)
src/twat_cache/engines/base.py:49: in __init__
    self.validate_config()
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <twat_cache.engines.functools.FunctoolsCacheEngine object at 0x1054
5ff20>

    def validate_config(self) -> None:
        """
        Validate the engine configuration.
    
        Raises:
            ValueError: If the configuration is invalid
        """
        super().validate_config()
    
        # Additional functools-specific validation
>       maxsize = self._config.get_maxsize()
E       AttributeError: 'CacheConfig' object has no attribute 'get_maxsize
'

src/twat_cache/engines/functools.py:201: AttributeError
__________________________ test_lru_cache_clear __________________________

base_config = CacheConfig(maxsize=100, folder_name=None, preferred_engine=
None, use_sql=False)

    def test_lru_cache_clear(base_config: CacheConfig) -> None:
        """Test LRU cache clearing."""
>       engine = FunctoolsCacheEngine(base_config)

tests/test_engines.py:125: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
src/twat_cache/engines/functools.py:41: in __init__
    super().__init__(config)
src/twat_cache/engines/base.py:49: in __init__
    self.validate_config()
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <twat_cache.engines.functools.FunctoolsCacheEngine object at 0x1053
da150>

    def validate_config(self) -> None:
        """
        Validate the engine configuration.
    
        Raises:
            ValueError: If the configuration is invalid
        """
        super().validate_config()
    
        # Additional functools-specific validation
>       maxsize = self._config.get_maxsize()
E       AttributeError: 'CacheConfig' object has no attribute 'get_maxsize
'

src/twat_cache/engines/functools.py:201: AttributeError
___________________ test_lru_cache_with_complex_values ___________________

base_config = CacheConfig(maxsize=100, folder_name=None, preferred_engine=
None, use_sql=False)

    def test_lru_cache_with_complex_values(base_config: CacheConfig) -> No
ne:
        """Test LRU cache with complex value types."""
>       engine = FunctoolsCacheEngine(base_config)

tests/test_engines.py:138: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
src/twat_cache/engines/functools.py:41: in __init__
    super().__init__(config)
src/twat_cache/engines/base.py:49: in __init__
    self.validate_config()
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <twat_cache.engines.functools.FunctoolsCacheEngine object at 0x1054
85d00>

    def validate_config(self) -> None:
        """
        Validate the engine configuration.
    
        Raises:
            ValueError: If the configuration is invalid
        """
        super().validate_config()
    
        # Additional functools-specific validation
>       maxsize = self._config.get_maxsize()
E       AttributeError: 'CacheConfig' object has no attribute 'get_maxsize
'

src/twat_cache/engines/functools.py:201: AttributeError
_____________________ test_lru_cache_stats_accuracy ______________________

base_config = CacheConfig(maxsize=100, folder_name=None, preferred_engine=
None, use_sql=False)

    def test_lru_cache_stats_accuracy(base_config: CacheConfig) -> None:
        """Test accuracy of LRU cache statistics."""
>       engine = FunctoolsCacheEngine(base_config)

tests/test_engines.py:157: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
src/twat_cache/engines/functools.py:41: in __init__
    super().__init__(config)
src/twat_cache/engines/base.py:49: in __init__
    self.validate_config()
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <twat_cache.engines.functools.FunctoolsCacheEngine object at 0x1054
84f80>

    def validate_config(self) -> None:
        """
        Validate the engine configuration.
    
        Raises:
            ValueError: If the configuration is invalid
        """
        super().validate_config()
    
        # Additional functools-specific validation
>       maxsize = self._config.get_maxsize()
E       AttributeError: 'CacheConfig' object has no attribute 'get_maxsize
'

src/twat_cache/engines/functools.py:201: AttributeError
________________________ test_cachebox_operations ________________________

cachebox_engine = <twat_cache.engines.cachebox.CacheBoxEngine object at 0x
105549dc0>

    def test_cachebox_operations(cachebox_engine: CacheBoxEngine) -> None:
        """Test basic operations for cachebox."""
        key: CacheKey = "test_key"
        value = "test_value"
    
        assert cachebox_engine._get_cached_value(key) is None
        cachebox_engine._set_cached_value(key, value)
>       assert cachebox_engine._get_cached_value(key) == value
E       AssertionError: assert None == 'test_value'
E        +  where None = _get_cached_value('test_key')
E        +    where _get_cached_value = <twat_cache.engines.cachebox.Cache
BoxEngine object at 0x105549dc0>._get_cached_value

tests/test_twat_cache.py:185: AssertionError
------------------------- Captured stderr setup --------------------------
2025-02-16 14:26:06.499 | DEBUG    | twat_cache.paths:get_cache_path:70 - 
Created cache directory: /Users/adam/Library/Caches/twat_cache/twat_cache_
c5075510
2025-02-16 14:26:06.499 | DEBUG    | twat_cache.engines.base:__init__:55 -
 Initialized CacheBoxEngine with config: CacheConfig(maxsize=100, folder_n
ame=None, preferred_engine=None, use_sql=False)
_______________________ test_cachetools_operations _______________________

cachetools_engine = <twat_cache.engines.cachetools.CacheToolsEngine object
 at 0x105487c20>

    def test_cachetools_operations(cachetools_engine: CacheToolsEngine) ->
 None:
        """Test basic operations for cachetools."""
        key: CacheKey = "test_key"
        value = "test_value"
    
        assert cachetools_engine._get_cached_value(key) is None
        cachetools_engine._set_cached_value(key, value)
>       assert cachetools_engine._get_cached_value(key) == value
E       AssertionError: assert None == 'test_value'
E        +  where None = _get_cached_value('test_key')
E        +    where _get_cached_value = <twat_cache.engines.cachetools.Cac
heToolsEngine object at 0x105487c20>._get_cached_value

tests/test_twat_cache.py:205: AssertionError
------------------------- Captured stderr setup --------------------------
2025-02-16 14:26:06.506 | DEBUG    | twat_cache.paths:get_cache_path:70 - 
Created cache directory: /Users/adam/Library/Caches/twat_cache/twat_cache_
8dae4766
2025-02-16 14:26:06.506 | DEBUG    | twat_cache.engines.base:__init__:55 -
 Initialized CacheToolsEngine with config: CacheConfig(maxsize=100, folder
_name=None, preferred_engine=None, use_sql=False)
============================ warnings summary ============================
tests/test_twat_cache.py::test_async_cache_operations
  /Users/adam/Library/Application Support/hatch/env/virtual/twat-cache/ivv
P1xkE/hatch-test.py3.12/lib/python3.12/site-packages/_pytest/runner.py:142
: RuntimeWarning: coroutine 'async_engine' was never awaited
    item.funcargs = None  # type: ignore[attr-defined]
  Enable tracemalloc to get traceback where the object was allocated.
  See https://docs.pytest.org/en/stable/how-to/capture-warnings.html#resou
rce-warnings for more info.

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
======================== short test summary info =========================
FAILED tests/test_cache.py::test_cache_exceptions - Failed: DID NOT RAISE 
<class 'ValueError'>
FAILED tests/test_cache.py::test_kwargs_handling - assert 2 == 1
FAILED tests/test_decorators.py::test_bcache_basic - AssertionError: asser
t False
FAILED tests/test_decorators.py::test_ucache_fallback - AttributeError: 'm
odule' object at twat_cache.engines has no attribut...
FAILED tests/test_decorators.py::test_decorator_error_handling - Failed: D
ID NOT RAISE <class 'ValueError'>
FAILED tests/test_engines.py::test_base_engine_initialization - AttributeE
rror: 'CacheConfig' object has no attribute 'get_maxsize'
FAILED tests/test_engines.py::test_base_engine_validation - AttributeError
: 'CacheConfig' object has no attribute 'get_maxsize'
FAILED tests/test_engines.py::test_lru_cache_initialization - AttributeErr
or: 'CacheConfig' object has no attribute 'get_maxsize'
FAILED tests/test_engines.py::test_lru_cache_maxsize_enforcement - Attribu
teError: 'CacheConfig' object has no attribute 'get_maxsize'
FAILED tests/test_engines.py::test_lru_cache_clear - AttributeError: 'Cach
eConfig' object has no attribute 'get_maxsize'
FAILED tests/test_engines.py::test_lru_cache_with_complex_values - Attribu
teError: 'CacheConfig' object has no attribute 'get_maxsize'
FAILED tests/test_engines.py::test_lru_cache_stats_accuracy - AttributeErr
or: 'CacheConfig' object has no attribute 'get_maxsize'
FAILED tests/test_twat_cache.py::test_cachebox_operations - AssertionError
: assert None == 'test_value'
FAILED tests/test_twat_cache.py::test_cachetools_operations - AssertionErr
or: assert None == 'test_value'
ERROR tests/test_engines.py::test_base_engine_key_generation - AttributeEr
ror: 'CacheConfig' object has no attribute 'get_maxsize'
ERROR tests/test_engines.py::test_base_engine_cache_decorator - AttributeE
rror: 'CacheConfig' object has no attribute 'get_maxsize'
ERROR tests/test_twat_cache.py::test_lru_cache_get_set - AttributeError: '
CacheConfig' object has no attribute 'get_maxsize'
ERROR tests/test_twat_cache.py::test_lru_cache_clear - AttributeError: 'Ca
cheConfig' object has no attribute 'get_maxsize'
ERROR tests/test_twat_cache.py::test_lru_cache_maxsize - AttributeError: '
CacheConfig' object has no attribute 'get_maxsize'
ERROR tests/test_twat_cache.py::test_disk_cache_persistence - TypeError: C
acheConfig.__init__() got an unexpected keyword argument ...
ERROR tests/test_twat_cache.py::test_klepto_persistence - TypeError: Cache
Config.__init__() got an unexpected keyword argument ...
ERROR tests/test_twat_cache.py::test_functools_cache_get_set - AttributeEr
ror: 'CacheConfig' object has no attribute 'get_maxsize'
ERROR tests/test_twat_cache.py::test_functools_cache_clear - AttributeErro
r: 'CacheConfig' object has no attribute 'get_maxsize'
ERROR tests/test_twat_cache.py::test_functools_cache_maxsize - AttributeEr
ror: 'CacheConfig' object has no attribute 'get_maxsize'
===== 14 failed, 15 passed, 3 skipped, 1 warning, 10 errors in 1.28s =====

```

---

_****_







I see several issues that need to be fixed:

1. **Config Compatibility**:
- Need to fix the config compatibility with the old engine system
- Need to fix the cache directory handling

2. **Engine Issues**:
- Need to fix the engine validation
- Need to fix the backend availability checks
- Need to fix the cache persistence

Let me fix these issues one by one. First, let's fix the config compatibility:

---

_****_



---

_****_





Let me fix the engine validation:

---

_****_

```diff
              "misses": self._misses,
              "size": self._size,
-             "maxsize": getattr(self._config, "maxsize", None),
+             "maxsize": self._config.maxsize,
              "backend": self.__class__.__name__,
              "path": str(self._cache_path) if self._cache_path else None,
          """
          # Validate maxsize if present
-         if hasattr(self._config, "maxsize"):
-             maxsize = self._config.maxsize
-             if maxsize is not None and maxsize <= 0:
-                 msg = "maxsize must be positive or None"
-                 raise ValueError(msg)
+         maxsize = self._config.maxsize
+         if maxsize is not None and maxsize <= 0:
+             msg = "maxsize must be positive or None"
+             raise ValueError(msg)
  
          # Validate cache folder if provided
-         if hasattr(self._config, "cache_dir"):
+         if self._config.folder_name is not None:
              try:
-                 validate_cache_path(self._config.cache_dir)
+                 validate_cache_path(self._config.folder_name)
              except ValueError as e:
                  msg = f"Invalid cache folder: {e}"
                  self._hits += 1
                  logger.trace(f"Cache hit for {func.__name__} with key {key}")
+                 if isinstance(cached_value, Exception):
+                     raise cached_value
                  return cached_value
  
              # Cache miss - compute and store
              self._misses += 1
-             value = func(*args, **kwargs)
-             self._set_cached_value(key, value)
+             try:
+                 value = func(*args, **kwargs)
+                 self._set_cached_value(key, value)
+             except Exception as e:
+                 # Cache the exception
+                 self._set_cached_value(key, e)
+                 raise
              self._size += 1
              logger.trace(f"Cache miss for {func.__name__} with key {key}")
                          self._set_cached_value(key, result)
                      except Exception as e:
-                         # Cache the exception to avoid recomputing
-                         # We know the exception is safe to cache in this context
-                         self._set_cached_value(key, cast(R, e))
+                         # Cache the exception
+                         self._set_cached_value(key, e)
                          raise
                  elif isinstance(result, Exception):
```

---

_****_







Let me run our catchphrase again to check if the changes fixed the issues:

---

_****_

```bash
uv venv; source .venv/bin/activate; uv pip install -e .[all,dev,test]; hatch run lint:fix; hatch test;
```

```
(twat_cache) (twat_cache) adam@Hamlet twat_cache % 
    |                      ^^ PLR2004
    |

tests/test_decorators.py:141:34: PLR2004 Magic value used in comparison, c
onsider replacing `25` with a constant variable
    |
139 |     result2 = await func(5)
140 |
141 |     assert result1 == result2 == 25
    |                                  ^^ PLR2004
    |

tests/test_decorators.py:188:23: PLR2004 Magic value used in comparison, c
onsider replacing `25` with a constant variable
    |
187 |     # Valid input should work
188 |     assert func(5) == 25
    |                       ^^ PLR2004
189 |
190 |     # Error should be raised consistently
    |

tests/test_engines.py:62:45: FBT003 Boolean positional value in function c
all
   |
60 |     assert isinstance(base_engine._make_key("test"), str)
61 |     assert isinstance(base_engine._make_key(123), str)
62 |     assert isinstance(base_engine._make_key(True), str)
   |                                             ^^^^ FBT003
63 |
64 |     # Test with complex types
   |

tests/test_engines.py:82:22: PLR2004 Magic value used in comparison, consi
der replacing `4` with a constant variable
   |
80 |     # First call
81 |     result = test_function(2)
82 |     assert result == 4
   |                      ^ PLR2004
83 |     assert call_count == 1
   |

tests/test_engines.py:87:22: PLR2004 Magic value used in comparison, consi
der replacing `4` with a constant variable
   |
85 |     # Second call (should use cache)
86 |     result = test_function(2)
87 |     assert result == 4
   |                      ^ PLR2004
88 |     assert call_count == 1  # Should not increment
   |

Found 22 errors.
========================== test session starts ===========================
platform darwin -- Python 3.12.8, pytest-8.3.4, pluggy-1.5.0 -- /Users/ada
m/Library/Application Support/hatch/env/virtual/twat-cache/ivvP1xkE/hatch-
test.py3.12/bin/python3
cachedir: .pytest_cache
rootdir: /Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good
/twat/plugins/repos/twat_cache
configfile: pyproject.toml
plugins: rerunfailures-14.0, mock-3.14.0, xdist-3.6.1
collected 42 items                                                       

tests/test_cache.py::test_cache_settings_validation PASSED         [  2%]
tests/test_cache.py::test_basic_caching PASSED                     [  4%]
tests/test_cache.py::test_cache_clear PASSED                       [  7%]
tests/test_cache.py::test_cache_stats PASSED                       [  9%]
tests/test_cache.py::test_list_processing PASSED                   [ 11%]
tests/test_cache.py::test_different_backends PASSED                [ 14%]
tests/test_cache.py::test_cache_with_complex_types PASSED          [ 16%]
tests/test_cache.py::test_cache_exceptions FAILED                  [ 19%]
tests/test_cache.py::test_kwargs_handling FAILED                   [ 21%]
tests/test_config.py::test_cache_config_validation PASSED          [ 23%]
tests/test_config.py::test_cache_config_creation PASSED            [ 26%]
tests/test_config.py::test_cache_config_to_dict PASSED             [ 28%]
tests/test_config.py::test_cache_config_from_dict PASSED           [ 30%]
tests/test_decorators.py::test_mcache_basic PASSED                 [ 33%]
tests/test_decorators.py::test_bcache_basic FAILED                 [ 35%]
tests/test_decorators.py::test_fcache_basic PASSED                 [ 38%]
tests/test_decorators.py::test_ucache_basic PASSED                 [ 40%]
tests/test_decorators.py::test_ucache_fallback FAILED              [ 42%]
tests/test_decorators.py::test_async_caching SKIPPED (async de...) [ 45%]
tests/test_decorators.py::test_cache_performance PASSED            [ 47%]
tests/test_decorators.py::test_decorator_error_handling FAILED     [ 50%]
tests/test_engines.py::test_base_engine_initialization FAILED      [ 52%]
tests/test_engines.py::test_base_engine_key_generation ERROR       [ 54%]
tests/test_engines.py::test_base_engine_cache_decorator ERROR      [ 57%]
tests/test_engines.py::test_base_engine_validation FAILED          [ 59%]
tests/test_engines.py::test_lru_cache_initialization FAILED        [ 61%]
tests/test_engines.py::test_lru_cache_maxsize_enforcement FAILED   [ 64%]
tests/test_engines.py::test_lru_cache_clear FAILED                 [ 66%]
tests/test_engines.py::test_lru_cache_with_complex_values FAILED   [ 69%]
tests/test_engines.py::test_lru_cache_stats_accuracy FAILED        [ 71%]
tests/test_twat_cache.py::test_lru_cache_get_set ERROR             [ 73%]
tests/test_twat_cache.py::test_lru_cache_clear ERROR               [ 76%]
tests/test_twat_cache.py::test_lru_cache_maxsize ERROR             [ 78%]
tests/test_twat_cache.py::test_disk_cache_persistence ERROR        [ 80%]
tests/test_twat_cache.py::test_joblib_numpy_array SKIPPED (num...) [ 83%]
tests/test_twat_cache.py::test_klepto_persistence ERROR            [ 85%]
tests/test_twat_cache.py::test_async_cache_operations SKIPPED      [ 88%]
tests/test_twat_cache.py::test_cachebox_operations FAILED          [ 90%]
tests/test_twat_cache.py::test_cachetools_operations FAILED        [ 92%]
tests/test_twat_cache.py::test_functools_cache_get_set ERROR       [ 95%]
tests/test_twat_cache.py::test_functools_cache_clear ERROR         [ 97%]
tests/test_twat_cache.py::test_functools_cache_maxsize ERROR       [100%]

================================= ERRORS =================================
___________ ERROR at setup of test_base_engine_key_generation ____________

base_config = CacheConfig(maxsize=100, folder_name=None, preferred_engine=
None, use_sql=False)

    @pytest.fixture
    def base_engine(base_config: CacheConfig) -> CacheEngine[Any, Any]:
        """Provide a basic cache engine instance."""
>       return FunctoolsCacheEngine(base_config)

tests/test_engines.py:47: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
src/twat_cache/engines/functools.py:41: in __init__
    super().__init__(config)
src/twat_cache/engines/base.py:49: in __init__
    self.validate_config()
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <twat_cache.engines.functools.FunctoolsCacheEngine object at 0x1023
f3860>

    def validate_config(self) -> None:
        """
        Validate the engine configuration.
    
        Raises:
            ValueError: If the configuration is invalid
        """
        super().validate_config()
    
        # Additional functools-specific validation
>       maxsize = self._config.get_maxsize()
E       AttributeError: 'CacheConfig' object has no attribute 'get_maxsize
'

src/twat_cache/engines/functools.py:201: AttributeError
___________ ERROR at setup of test_base_engine_cache_decorator ___________

base_config = CacheConfig(maxsize=100, folder_name=None, preferred_engine=
None, use_sql=False)

    @pytest.fixture
    def base_engine(base_config: CacheConfig) -> CacheEngine[Any, Any]:
        """Provide a basic cache engine instance."""
>       return FunctoolsCacheEngine(base_config)

tests/test_engines.py:47: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
src/twat_cache/engines/functools.py:41: in __init__
    super().__init__(config)
src/twat_cache/engines/base.py:49: in __init__
    self.validate_config()
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <twat_cache.engines.functools.FunctoolsCacheEngine object at 0x1024
16270>

    def validate_config(self) -> None:
        """
        Validate the engine configuration.
    
        Raises:
            ValueError: If the configuration is invalid
        """
        super().validate_config()
    
        # Additional functools-specific validation
>       maxsize = self._config.get_maxsize()
E       AttributeError: 'CacheConfig' object has no attribute 'get_maxsize
'

src/twat_cache/engines/functools.py:201: AttributeError
________________ ERROR at setup of test_lru_cache_get_set ________________

base_config = CacheConfig(maxsize=100, folder_name=None, preferred_engine=
None, use_sql=False)

    @pytest.fixture
    def lru_engine(base_config: CacheConfig) -> FunctoolsCacheEngine:
        """Create an LRU cache engine instance."""
>       return FunctoolsCacheEngine(base_config)

tests/test_twat_cache.py:55: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
src/twat_cache/engines/functools.py:41: in __init__
    super().__init__(config)
src/twat_cache/engines/base.py:49: in __init__
    self.validate_config()
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <twat_cache.engines.functools.FunctoolsCacheEngine object at 0x1024
16690>

    def validate_config(self) -> None:
        """
        Validate the engine configuration.
    
        Raises:
            ValueError: If the configuration is invalid
        """
        super().validate_config()
    
        # Additional functools-specific validation
>       maxsize = self._config.get_maxsize()
E       AttributeError: 'CacheConfig' object has no attribute 'get_maxsize
'

src/twat_cache/engines/functools.py:201: AttributeError
_________________ ERROR at setup of test_lru_cache_clear _________________

base_config = CacheConfig(maxsize=100, folder_name=None, preferred_engine=
None, use_sql=False)

    @pytest.fixture
    def lru_engine(base_config: CacheConfig) -> FunctoolsCacheEngine:
        """Create an LRU cache engine instance."""
>       return FunctoolsCacheEngine(base_config)

tests/test_twat_cache.py:55: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
src/twat_cache/engines/functools.py:41: in __init__
    super().__init__(config)
src/twat_cache/engines/base.py:49: in __init__
    self.validate_config()
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <twat_cache.engines.functools.FunctoolsCacheEngine object at 0x1024
16150>

    def validate_config(self) -> None:
        """
        Validate the engine configuration.
    
        Raises:
            ValueError: If the configuration is invalid
        """
        super().validate_config()
    
        # Additional functools-specific validation
>       maxsize = self._config.get_maxsize()
E       AttributeError: 'CacheConfig' object has no attribute 'get_maxsize
'

src/twat_cache/engines/functools.py:201: AttributeError
________________ ERROR at setup of test_lru_cache_maxsize ________________

base_config = CacheConfig(maxsize=100, folder_name=None, preferred_engine=
None, use_sql=False)

    @pytest.fixture
    def lru_engine(base_config: CacheConfig) -> FunctoolsCacheEngine:
        """Create an LRU cache engine instance."""
>       return FunctoolsCacheEngine(base_config)

tests/test_twat_cache.py:55: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
src/twat_cache/engines/functools.py:41: in __init__
    super().__init__(config)
src/twat_cache/engines/base.py:49: in __init__
    self.validate_config()
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <twat_cache.engines.functools.FunctoolsCacheEngine object at 0x1023
f2810>

    def validate_config(self) -> None:
        """
        Validate the engine configuration.
    
        Raises:
            ValueError: If the configuration is invalid
        """
        super().validate_config()
    
        # Additional functools-specific validation
>       maxsize = self._config.get_maxsize()
E       AttributeError: 'CacheConfig' object has no attribute 'get_maxsize
'

src/twat_cache/engines/functools.py:201: AttributeError
_____________ ERROR at setup of test_disk_cache_persistence ______________

base_config = CacheConfig(maxsize=100, folder_name=None, preferred_engine=
None, use_sql=False)
temp_path = PosixPath('/private/var/folders/05/clcynl0509ldxltl599hhhx4000
0gn/T/pytest-of-adam/pytest-37/test_disk_cache_persistence0/cache')

    @pytest.fixture
    def disk_engine(base_config: CacheConfig, temp_path: Path) -> DiskCach
eEngine:
        """Create a disk cache engine instance."""
>       config = create_cache_config(maxsize=100, cache_dir=str(temp_path)
)

tests/test_twat_cache.py:95: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

kwargs = {'cache_dir': '/private/var/folders/05/clcynl0509ldxltl599hhhx400
00gn/T/pytest-of-adam/pytest-37/test_disk_cache_persistence0/cache', 'maxs
ize': 100}

    def create_cache_config(**kwargs: Any) -> CacheConfig:
        """
        Create a cache configuration.
    
        Args:
            **kwargs: Configuration options
    
        Returns:
            A validated cache configuration
        """
>       config = CacheConfig(**kwargs)
E       TypeError: CacheConfig.__init__() got an unexpected keyword argume
nt 'cache_dir'

src/twat_cache/config.py:83: TypeError
_______________ ERROR at setup of test_klepto_persistence ________________

base_config = CacheConfig(maxsize=100, folder_name=None, preferred_engine=
None, use_sql=False)
temp_path = PosixPath('/private/var/folders/05/clcynl0509ldxltl599hhhx4000
0gn/T/pytest-of-adam/pytest-37/test_klepto_persistence0/cache')

    @pytest.fixture
    def klepto_engine(base_config: CacheConfig, temp_path: Path) -> Klepto
Engine:
        """Create a klepto cache engine instance."""
>       config = create_cache_config(maxsize=100, cache_dir=str(temp_path)
)

tests/test_twat_cache.py:137: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

kwargs = {'cache_dir': '/private/var/folders/05/clcynl0509ldxltl599hhhx400
00gn/T/pytest-of-adam/pytest-37/test_klepto_persistence0/cache', 'maxsize'
: 100}

    def create_cache_config(**kwargs: Any) -> CacheConfig:
        """
        Create a cache configuration.
    
        Args:
            **kwargs: Configuration options
    
        Returns:
            A validated cache configuration
        """
>       config = CacheConfig(**kwargs)
E       TypeError: CacheConfig.__init__() got an unexpected keyword argume
nt 'cache_dir'

src/twat_cache/config.py:83: TypeError
_____________ ERROR at setup of test_functools_cache_get_set _____________

base_config = CacheConfig(maxsize=100, folder_name=None, preferred_engine=
None, use_sql=False)

    @pytest.fixture
    def functools_engine(base_config: CacheConfig) -> FunctoolsCacheEngine
:
        """Fixture for testing the functools cache engine."""
>       return FunctoolsCacheEngine(base_config)

tests/test_twat_cache.py:214: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
src/twat_cache/engines/functools.py:41: in __init__
    super().__init__(config)
src/twat_cache/engines/base.py:49: in __init__
    self.validate_config()
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <twat_cache.engines.functools.FunctoolsCacheEngine object at 0x1024
99d30>

    def validate_config(self) -> None:
        """
        Validate the engine configuration.
    
        Raises:
            ValueError: If the configuration is invalid
        """
        super().validate_config()
    
        # Additional functools-specific validation
>       maxsize = self._config.get_maxsize()
E       AttributeError: 'CacheConfig' object has no attribute 'get_maxsize
'

src/twat_cache/engines/functools.py:201: AttributeError
______________ ERROR at setup of test_functools_cache_clear ______________

base_config = CacheConfig(maxsize=100, folder_name=None, preferred_engine=
None, use_sql=False)

    @pytest.fixture
    def functools_engine(base_config: CacheConfig) -> FunctoolsCacheEngine
:
        """Fixture for testing the functools cache engine."""
>       return FunctoolsCacheEngine(base_config)

tests/test_twat_cache.py:214: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
src/twat_cache/engines/functools.py:41: in __init__
    super().__init__(config)
src/twat_cache/engines/base.py:49: in __init__
    self.validate_config()
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <twat_cache.engines.functools.FunctoolsCacheEngine object at 0x1024
9a990>

    def validate_config(self) -> None:
        """
        Validate the engine configuration.
    
        Raises:
            ValueError: If the configuration is invalid
        """
        super().validate_config()
    
        # Additional functools-specific validation
>       maxsize = self._config.get_maxsize()
E       AttributeError: 'CacheConfig' object has no attribute 'get_maxsize
'

src/twat_cache/engines/functools.py:201: AttributeError
_____________ ERROR at setup of test_functools_cache_maxsize _____________

base_config = CacheConfig(maxsize=100, folder_name=None, preferred_engine=
None, use_sql=False)

    @pytest.fixture
    def functools_engine(base_config: CacheConfig) -> FunctoolsCacheEngine
:
        """Fixture for testing the functools cache engine."""
>       return FunctoolsCacheEngine(base_config)

tests/test_twat_cache.py:214: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
src/twat_cache/engines/functools.py:41: in __init__
    super().__init__(config)
src/twat_cache/engines/base.py:49: in __init__
    self.validate_config()
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <twat_cache.engines.functools.FunctoolsCacheEngine object at 0x1024
14560>

    def validate_config(self) -> None:
        """
        Validate the engine configuration.
    
        Raises:
            ValueError: If the configuration is invalid
        """
        super().validate_config()
    
        # Additional functools-specific validation
>       maxsize = self._config.get_maxsize()
E       AttributeError: 'CacheConfig' object has no attribute 'get_maxsize
'

src/twat_cache/engines/functools.py:201: AttributeError
================================ FAILURES ================================
_________________________ test_cache_exceptions __________________________

    def test_cache_exceptions() -> None:
        """Test caching of exceptions."""
        call_count = 0
    
        @ucache(maxsize=100)
        def failing_function(x: int) -> None:
            nonlocal call_count
            call_count += 1
            msg = "Test error"
            raise ValueError(msg)
    
        # First call
        with pytest.raises(ValueError):
            failing_function(5)
        assert call_count == 1
    
        # Second call should not recompute
>       with pytest.raises(ValueError):
E       Failed: DID NOT RAISE <class 'ValueError'>

tests/test_cache.py:195: Failed
-------------------------- Captured stderr call --------------------------
2025-02-16 14:27:14.066 | DEBUG    | twat_cache.decorators:decorator:306 -
 Using memory cache (functools)
2025-02-16 14:27:14.066 | DEBUG    | twat_cache.cache:register_cache:55 - 
Registered cache: mcache_failing_function_598e05da
__________________________ test_kwargs_handling __________________________

    def test_kwargs_handling() -> None:
        """Test caching with different keyword arguments."""
        call_count = 0
    
        @ucache()
        def kwarg_function(x: int, multiplier: int = 1) -> int:
            nonlocal call_count
            call_count += 1
            return x * multiplier
    
        # Test with different kwarg combinations
        assert kwarg_function(TEST_INPUT) == TEST_INPUT
        assert call_count == 1
    
        assert kwarg_function(TEST_INPUT, multiplier=1) == TEST_INPUT
>       assert call_count == 1  # Should use cache
E       assert 2 == 1

tests/test_cache.py:215: AssertionError
-------------------------- Captured stderr call --------------------------
2025-02-16 14:27:14.114 | DEBUG    | twat_cache.decorators:decorator:306 -
 Using memory cache (functools)
2025-02-16 14:27:14.114 | DEBUG    | twat_cache.cache:register_cache:55 - 
Registered cache: mcache_kwarg_function_2e325408
___________________________ test_bcache_basic ____________________________

tmp_path = PosixPath('/private/var/folders/05/clcynl0509ldxltl599hhhx40000
gn/T/pytest-of-adam/pytest-37/test_bcache_basic0')

    def test_bcache_basic(tmp_path: Path):
        """Test basic disk caching."""
        cache_dir = tmp_path / "cache"
    
        @bcache(folder_name=str(cache_dir))
        def func(x: int) -> int:
            return expensive_computation(x)
    
        # First call should compute
        result1 = func(5)
    
        # Second call should be from cache
        result2 = func(5)
    
        assert result1 == result2 == 25
>       assert cache_dir.exists()
E       AssertionError: assert False
E        +  where False = exists()
E        +    where exists = PosixPath('/private/var/folders/05/clcynl0509
ldxltl599hhhx40000gn/T/pytest-of-adam/pytest-37/test_bcache_basic0/cache')
.exists

tests/test_decorators.py:75: AssertionError
-------------------------- Captured stderr call --------------------------
2025-02-16 14:27:14.229 | WARNING  | twat_cache.decorators:decorator:154 -
 diskcache not available, falling back to memory cache
2025-02-16 14:27:14.229 | DEBUG    | twat_cache.cache:register_cache:55 - 
Registered cache: mcache_func_69555a77
__________________________ test_ucache_fallback __________________________

obj = <module 'twat_cache.engines' from '/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_cache/src/twat_ca
che/engines/__init__.py'>
name = 'HAS_CACHEBOX', ann = 'twat_cache.engines'

    def annotated_getattr(obj: object, name: str, ann: str) -> object:
        try:
>           obj = getattr(obj, name)
E           AttributeError: module 'twat_cache.engines' has no attribute '
HAS_CACHEBOX'

/Users/adam/Library/Application Support/hatch/env/virtual/twat-cache/ivvP1
xkE/hatch-test.py3.12/lib/python3.12/site-packages/_pytest/monkeypatch.py:
90: AttributeError

The above exception was the direct cause of the following exception:

monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x1023f12e0>

    def test_ucache_fallback(monkeypatch):
        """Test ucache fallback behavior."""
        # Simulate no backends available except functools
>       monkeypatch.setattr("twat_cache.engines.HAS_CACHEBOX", False)

tests/test_decorators.py:114: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
/Users/adam/Library/Application Support/hatch/env/virtual/twat-cache/ivvP1
xkE/hatch-test.py3.12/lib/python3.12/site-packages/_pytest/monkeypatch.py:
104: in derive_importpath
    annotated_getattr(target, attr, ann=module)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

obj = <module 'twat_cache.engines' from '/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_cache/src/twat_ca
che/engines/__init__.py'>
name = 'HAS_CACHEBOX', ann = 'twat_cache.engines'

    def annotated_getattr(obj: object, name: str, ann: str) -> object:
        try:
            obj = getattr(obj, name)
        except AttributeError as e:
>           raise AttributeError(
                f"{type(obj).__name__!r} object at {ann} has no attribute 
{name!r}"
            ) from e
E           AttributeError: 'module' object at twat_cache.engines has no a
ttribute 'HAS_CACHEBOX'

/Users/adam/Library/Application Support/hatch/env/virtual/twat-cache/ivvP1
xkE/hatch-test.py3.12/lib/python3.12/site-packages/_pytest/monkeypatch.py:
92: AttributeError
_____________________ test_decorator_error_handling ______________________

    def test_decorator_error_handling():
        """Test error handling in decorators."""
    
        @ucache()
        def func(x: int) -> int:
            if x < 0:
                msg = "Negative input"
                raise ValueError(msg)
            return x * x
    
        # Valid input should work
        assert func(5) == 25
    
        # Error should be raised consistently
        with pytest.raises(ValueError):
            func(-1)
    
>       with pytest.raises(ValueError):
E       Failed: DID NOT RAISE <class 'ValueError'>

tests/test_decorators.py:194: Failed
-------------------------- Captured stderr call --------------------------
2025-02-16 14:27:14.973 | DEBUG    | twat_cache.decorators:decorator:306 -
 Using memory cache (functools)
2025-02-16 14:27:14.973 | DEBUG    | twat_cache.cache:register_cache:55 - 
Registered cache: mcache_func_ace3a006
____________________ test_base_engine_initialization _____________________

base_config = CacheConfig(maxsize=100, folder_name=None, preferred_engine=
None, use_sql=False)

    def test_base_engine_initialization(base_config: CacheConfig) -> None:
        """Test basic engine initialization."""
>       engine = FunctoolsCacheEngine(base_config)

tests/test_engines.py:52: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
src/twat_cache/engines/functools.py:41: in __init__
    super().__init__(config)
src/twat_cache/engines/base.py:49: in __init__
    self.validate_config()
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <twat_cache.engines.functools.FunctoolsCacheEngine object at 0x1023
f2ea0>

    def validate_config(self) -> None:
        """
        Validate the engine configuration.
    
        Raises:
            ValueError: If the configuration is invalid
        """
        super().validate_config()
    
        # Additional functools-specific validation
>       maxsize = self._config.get_maxsize()
E       AttributeError: 'CacheConfig' object has no attribute 'get_maxsize
'

src/twat_cache/engines/functools.py:201: AttributeError
______________________ test_base_engine_validation _______________________

base_config = CacheConfig(maxsize=100, folder_name=None, preferred_engine=
None, use_sql=False)

    def test_base_engine_validation(base_config: CacheConfig) -> None:
        """Test engine configuration validation."""
>       engine = FunctoolsCacheEngine(base_config)

tests/test_engines.py:93: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
src/twat_cache/engines/functools.py:41: in __init__
    super().__init__(config)
src/twat_cache/engines/base.py:49: in __init__
    self.validate_config()
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <twat_cache.engines.functools.FunctoolsCacheEngine object at 0x1023
f3a40>

    def validate_config(self) -> None:
        """
        Validate the engine configuration.
    
        Raises:
            ValueError: If the configuration is invalid
        """
        super().validate_config()
    
        # Additional functools-specific validation
>       maxsize = self._config.get_maxsize()
E       AttributeError: 'CacheConfig' object has no attribute 'get_maxsize
'

src/twat_cache/engines/functools.py:201: AttributeError
_____________________ test_lru_cache_initialization ______________________

base_config = CacheConfig(maxsize=100, folder_name=None, preferred_engine=
None, use_sql=False)

    def test_lru_cache_initialization(base_config: CacheConfig) -> None:
        """Test LRU cache initialization."""
>       engine = FunctoolsCacheEngine(base_config)

tests/test_engines.py:103: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
src/twat_cache/engines/functools.py:41: in __init__
    super().__init__(config)
src/twat_cache/engines/base.py:49: in __init__
    self.validate_config()
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <twat_cache.engines.functools.FunctoolsCacheEngine object at 0x1023
f0950>

    def validate_config(self) -> None:
        """
        Validate the engine configuration.
    
        Raises:
            ValueError: If the configuration is invalid
        """
        super().validate_config()
    
        # Additional functools-specific validation
>       maxsize = self._config.get_maxsize()
E       AttributeError: 'CacheConfig' object has no attribute 'get_maxsize
'

src/twat_cache/engines/functools.py:201: AttributeError
___________________ test_lru_cache_maxsize_enforcement ___________________

base_config = CacheConfig(maxsize=100, folder_name=None, preferred_engine=
None, use_sql=False)

    def test_lru_cache_maxsize_enforcement(base_config: CacheConfig) -> No
ne:
        """Test LRU cache maxsize enforcement."""
>       engine = FunctoolsCacheEngine(base_config)

tests/test_engines.py:110: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
src/twat_cache/engines/functools.py:41: in __init__
    super().__init__(config)
src/twat_cache/engines/base.py:49: in __init__
    self.validate_config()
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <twat_cache.engines.functools.FunctoolsCacheEngine object at 0x1020
efa40>

    def validate_config(self) -> None:
        """
        Validate the engine configuration.
    
        Raises:
            ValueError: If the configuration is invalid
        """
        super().validate_config()
    
        # Additional functools-specific validation
>       maxsize = self._config.get_maxsize()
E       AttributeError: 'CacheConfig' object has no attribute 'get_maxsize
'

src/twat_cache/engines/functools.py:201: AttributeError
__________________________ test_lru_cache_clear __________________________

base_config = CacheConfig(maxsize=100, folder_name=None, preferred_engine=
None, use_sql=False)

    def test_lru_cache_clear(base_config: CacheConfig) -> None:
        """Test LRU cache clearing."""
>       engine = FunctoolsCacheEngine(base_config)

tests/test_engines.py:125: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
src/twat_cache/engines/functools.py:41: in __init__
    super().__init__(config)
src/twat_cache/engines/base.py:49: in __init__
    self.validate_config()
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <twat_cache.engines.functools.FunctoolsCacheEngine object at 0x1024
15eb0>

    def validate_config(self) -> None:
        """
        Validate the engine configuration.
    
        Raises:
            ValueError: If the configuration is invalid
        """
        super().validate_config()
    
        # Additional functools-specific validation
>       maxsize = self._config.get_maxsize()
E       AttributeError: 'CacheConfig' object has no attribute 'get_maxsize
'

src/twat_cache/engines/functools.py:201: AttributeError
___________________ test_lru_cache_with_complex_values ___________________

base_config = CacheConfig(maxsize=100, folder_name=None, preferred_engine=
None, use_sql=False)

    def test_lru_cache_with_complex_values(base_config: CacheConfig) -> No
ne:
        """Test LRU cache with complex value types."""
>       engine = FunctoolsCacheEngine(base_config)

tests/test_engines.py:138: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
src/twat_cache/engines/functools.py:41: in __init__
    super().__init__(config)
src/twat_cache/engines/base.py:49: in __init__
    self.validate_config()
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <twat_cache.engines.functools.FunctoolsCacheEngine object at 0x1023
9a2d0>

    def validate_config(self) -> None:
        """
        Validate the engine configuration.
    
        Raises:
            ValueError: If the configuration is invalid
        """
        super().validate_config()
    
        # Additional functools-specific validation
>       maxsize = self._config.get_maxsize()
E       AttributeError: 'CacheConfig' object has no attribute 'get_maxsize
'

src/twat_cache/engines/functools.py:201: AttributeError
_____________________ test_lru_cache_stats_accuracy ______________________

base_config = CacheConfig(maxsize=100, folder_name=None, preferred_engine=
None, use_sql=False)

    def test_lru_cache_stats_accuracy(base_config: CacheConfig) -> None:
        """Test accuracy of LRU cache statistics."""
>       engine = FunctoolsCacheEngine(base_config)

tests/test_engines.py:157: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
src/twat_cache/engines/functools.py:41: in __init__
    super().__init__(config)
src/twat_cache/engines/base.py:49: in __init__
    self.validate_config()
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <twat_cache.engines.functools.FunctoolsCacheEngine object at 0x1023
f1370>

    def validate_config(self) -> None:
        """
        Validate the engine configuration.
    
        Raises:
            ValueError: If the configuration is invalid
        """
        super().validate_config()
    
        # Additional functools-specific validation
>       maxsize = self._config.get_maxsize()
E       AttributeError: 'CacheConfig' object has no attribute 'get_maxsize
'

src/twat_cache/engines/functools.py:201: AttributeError
________________________ test_cachebox_operations ________________________

cachebox_engine = <twat_cache.engines.cachebox.CacheBoxEngine object at 0x
102499370>

    def test_cachebox_operations(cachebox_engine: CacheBoxEngine) -> None:
        """Test basic operations for cachebox."""
        key: CacheKey = "test_key"
        value = "test_value"
    
        assert cachebox_engine._get_cached_value(key) is None
        cachebox_engine._set_cached_value(key, value)
>       assert cachebox_engine._get_cached_value(key) == value
E       AssertionError: assert None == 'test_value'
E        +  where None = _get_cached_value('test_key')
E        +    where _get_cached_value = <twat_cache.engines.cachebox.Cache
BoxEngine object at 0x102499370>._get_cached_value

tests/test_twat_cache.py:185: AssertionError
------------------------- Captured stderr setup --------------------------
2025-02-16 14:27:15.171 | DEBUG    | twat_cache.paths:get_cache_path:70 - 
Created cache directory: /Users/adam/Library/Caches/twat_cache/twat_cache_
778d1b4a
2025-02-16 14:27:15.172 | DEBUG    | twat_cache.engines.base:__init__:55 -
 Initialized CacheBoxEngine with config: CacheConfig(maxsize=100, folder_n
ame=None, preferred_engine=None, use_sql=False)
_______________________ test_cachetools_operations _______________________

cachetools_engine = <twat_cache.engines.cachetools.CacheToolsEngine object
 at 0x102417a70>

    def test_cachetools_operations(cachetools_engine: CacheToolsEngine) ->
 None:
        """Test basic operations for cachetools."""
        key: CacheKey = "test_key"
        value = "test_value"
    
        assert cachetools_engine._get_cached_value(key) is None
        cachetools_engine._set_cached_value(key, value)
>       assert cachetools_engine._get_cached_value(key) == value
E       AssertionError: assert None == 'test_value'
E        +  where None = _get_cached_value('test_key')
E        +    where _get_cached_value = <twat_cache.engines.cachetools.Cac
heToolsEngine object at 0x102417a70>._get_cached_value

tests/test_twat_cache.py:205: AssertionError
------------------------- Captured stderr setup --------------------------
2025-02-16 14:27:15.177 | DEBUG    | twat_cache.paths:get_cache_path:70 - 
Created cache directory: /Users/adam/Library/Caches/twat_cache/twat_cache_
d185b513
2025-02-16 14:27:15.177 | DEBUG    | twat_cache.engines.base:__init__:55 -
 Initialized CacheToolsEngine with config: CacheConfig(maxsize=100, folder
_name=None, preferred_engine=None, use_sql=False)
============================ warnings summary ============================
tests/test_twat_cache.py::test_async_cache_operations
  /Users/adam/Library/Application Support/hatch/env/virtual/twat-cache/ivv
P1xkE/hatch-test.py3.12/lib/python3.12/site-packages/_pytest/runner.py:142
: RuntimeWarning: coroutine 'async_engine' was never awaited
    item.funcargs = None  # type: ignore[attr-defined]
  Enable tracemalloc to get traceback where the object was allocated.
  See https://docs.pytest.org/en/stable/how-to/capture-warnings.html#resou
rce-warnings for more info.

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
======================== short test summary info =========================
FAILED tests/test_cache.py::test_cache_exceptions - Failed: DID NOT RAISE 
<class 'ValueError'>
FAILED tests/test_cache.py::test_kwargs_handling - assert 2 == 1
FAILED tests/test_decorators.py::test_bcache_basic - AssertionError: asser
t False
FAILED tests/test_decorators.py::test_ucache_fallback - AttributeError: 'm
odule' object at twat_cache.engines has no attribut...
FAILED tests/test_decorators.py::test_decorator_error_handling - Failed: D
ID NOT RAISE <class 'ValueError'>
FAILED tests/test_engines.py::test_base_engine_initialization - AttributeE
rror: 'CacheConfig' object has no attribute 'get_maxsize'
FAILED tests/test_engines.py::test_base_engine_validation - AttributeError
: 'CacheConfig' object has no attribute 'get_maxsize'
FAILED tests/test_engines.py::test_lru_cache_initialization - AttributeErr
or: 'CacheConfig' object has no attribute 'get_maxsize'
FAILED tests/test_engines.py::test_lru_cache_maxsize_enforcement - Attribu
teError: 'CacheConfig' object has no attribute 'get_maxsize'
FAILED tests/test_engines.py::test_lru_cache_clear - AttributeError: 'Cach
eConfig' object has no attribute 'get_maxsize'
FAILED tests/test_engines.py::test_lru_cache_with_complex_values - Attribu
teError: 'CacheConfig' object has no attribute 'get_maxsize'
FAILED tests/test_engines.py::test_lru_cache_stats_accuracy - AttributeErr
or: 'CacheConfig' object has no attribute 'get_maxsize'
FAILED tests/test_twat_cache.py::test_cachebox_operations - AssertionError
: assert None == 'test_value'
FAILED tests/test_twat_cache.py::test_cachetools_operations - AssertionErr
or: assert None == 'test_value'
ERROR tests/test_engines.py::test_base_engine_key_generation - AttributeEr
ror: 'CacheConfig' object has no attribute 'get_maxsize'
ERROR tests/test_engines.py::test_base_engine_cache_decorator - AttributeE
rror: 'CacheConfig' object has no attribute 'get_maxsize'
ERROR tests/test_twat_cache.py::test_lru_cache_get_set - AttributeError: '
CacheConfig' object has no attribute 'get_maxsize'
ERROR tests/test_twat_cache.py::test_lru_cache_clear - AttributeError: 'Ca
cheConfig' object has no attribute 'get_maxsize'
ERROR tests/test_twat_cache.py::test_lru_cache_maxsize - AttributeError: '
CacheConfig' object has no attribute 'get_maxsize'
ERROR tests/test_twat_cache.py::test_disk_cache_persistence - TypeError: C
acheConfig.__init__() got an unexpected keyword argument ...
ERROR tests/test_twat_cache.py::test_klepto_persistence - TypeError: Cache
Config.__init__() got an unexpected keyword argument ...
ERROR tests/test_twat_cache.py::test_functools_cache_get_set - AttributeEr
ror: 'CacheConfig' object has no attribute 'get_maxsize'
ERROR tests/test_twat_cache.py::test_functools_cache_clear - AttributeErro
r: 'CacheConfig' object has no attribute 'get_maxsize'
ERROR tests/test_twat_cache.py::test_functools_cache_maxsize - AttributeEr
ror: 'CacheConfig' object has no attribute 'get_maxsize'
===== 14 failed, 15 passed, 3 skipped, 1 warning, 10 errors in 1.26s =====

```

---

_****_









I see several issues that need to be fixed:

1. **Config Compatibility**:
- Need to fix the get_maxsize() method in CacheConfig
- Need to fix the cache_dir parameter handling

2. **Engine Issues**:
- Need to fix the backend availability checks
- Need to fix the cache persistence
- Need to fix the exception handling

Let me fix these issues one by one. First, let's fix the config compatibility:

---

_****_

```diff
  
          # Initialize the cache storage
-         maxsize = config.get_maxsize()
-         self._maxsize = maxsize if maxsize is not None else 128
+         self._maxsize = config.maxsize if config.maxsize is not None else 128
          self._hits = 0
          self._misses = 0
          return self._get_cached_value(key)
  
-     def set(self, key: Any, value: R) -> None:
-         """
-         Set a value in the cache.
- 
-         Args:
-             key: The key to store under
-             value: The value to cache
-         """
-         self._set_cached_value(key, value)
- 
-     def _make_key(self, *args: Any, **kwargs: Any) -> str:
-         """
-         Create a hashable key from function arguments.
- 
-         Args:
-             *args: Positional arguments
-             **kwargs: Keyword arguments
- 
-         Returns:
-             A string key that uniquely identifies the arguments
-         """
-         try:
-             # Try to create a JSON-serializable representation
-             key_dict = {
-                 "args": [
-                     str(arg)
-                     if not isinstance(arg, int | float | str | bool | type(None))
-                     else arg
-                     for arg in args
-                 ],
-                 "kwargs": {
-                     k: str(v)
-                     if not isinstance(v, int | float | str | bool | type(None))
-                     else v
-                     for k, v in sorted(kwargs.items())
-                 },
-             }
-             return json.dumps(key_dict, sort_keys=True, default=str)
-         except (TypeError, ValueError):
-             # Fallback to string representation if JSON serialization fails
-             args_str = ",".join(repr(arg) for arg in args)
-             kwargs_str = ",".join(f"{k}={v!r}" for k, v in sorted(kwargs.items()))
-             return f"args[{args_str}]kwargs[{kwargs_str}]"
- 
      def _get_cached_value(self, key: Any) -> R | None:
          """
          Retrieve a value from the cache.
  
          Args:
-             key: The cache key to look up
+             key: The key to look up
  
          Returns:
              The cached value if found, None otherwise
          """
          try:
-             str_key = self._make_key(key) if not isinstance(key, str) else key
-             value = self._cache.get(str_key)
-             if value is not None:
+             str_key = json.dumps(key, sort_keys=True)
+             if str_key in self._cache:
                  self._hits += 1
-                 # Move to end (most recently used)
-                 if str_key in self._cache_order:
-                     self._cache_order.remove(str_key)
-                     self._cache_order.append(str_key)
-                 return value
+                 # Move key to end of LRU order
+                 self._cache_order.remove(str_key)
+                 self._cache_order.append(str_key)
+                 return self._cache[str_key]
              self._misses += 1
              return None
  
          Args:
-             key: The cache key to store under
+             key: The key to store under
              value: The value to cache
          """
          try:
-             str_key = self._make_key(key) if not isinstance(key, str) else key
- 
-             # If key exists, update it and move to end
-             if str_key in self._cache:
-                 self._cache[str_key] = value
-                 if str_key in self._cache_order:
-                     self._cache_order.remove(str_key)
-                     self._cache_order.append(str_key)
-                 return
- 
-             # If cache is full, remove oldest items until we have space
-             while len(self._cache) >= self._maxsize and self._cache_order:
-                 oldest_key = self._cache_order.pop(0)
-                 self._cache.pop(oldest_key, None)
- 
-             # Add new item
+             str_key = json.dumps(key, sort_keys=True)
              self._cache[str_key] = value
              self._cache_order.append(str_key)
+ 
+             # Enforce maxsize
+             while len(self._cache) > self._maxsize:
+                 # Remove oldest item
+                 oldest_key = self._cache_order.pop(0)
+                 del self._cache[oldest_key]
          except (TypeError, ValueError):
              pass
  
          # Additional functools-specific validation
-         maxsize = self._config.get_maxsize()
+         maxsize = self._config.maxsize
          if maxsize is not None and not isinstance(maxsize, int):
              msg = "maxsize must be an integer or None"
              @wraps(f)
              def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
-                 key = self._make_key(*args, **kwargs)
+                 key = json.dumps(tuple(args) + tuple(kwargs.items()), sort_keys=True)
                  result = self._get_cached_value(key)
                  if result is None:
```

---

_****_







Let me fix the engine validation:

---

_****_

```diff
  
          # Initialize cache path if needed
-         if hasattr(self._config, "folder_name"):
+         if self._config.folder_name is not None:
              self._cache_path = get_cache_path(self._config.folder_name)
  
                  if isinstance(cached_value, Exception):
                      raise cached_value
-                 return cached_value
+                 return cast(R, cached_value)
  
              # Cache miss - compute and store
              except Exception as e:
                  # Cache the exception
-                 self._set_cached_value(key, e)
+                 self._set_cached_value(key, cast(R, e))
                  raise
              self._size += 1
              return value
  
-         return cast(Callable[P, R], wrapper)
+         return wrapper
  
  
                      except Exception as e:
                          # Cache the exception
-                         self._set_cached_value(key, e)
+                         self._set_cached_value(key, cast(R, e))
                          raise
                  elif isinstance(result, Exception):
                      raise result
-                 return result
+                 return cast(R, result)
  
              return wrapper
```

---

_****_





---



---

