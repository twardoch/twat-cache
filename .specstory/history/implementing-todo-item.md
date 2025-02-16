## SpecStory

## Implementing TODO Item (16/02/2025, 05:59:16)

_**User**_

@TODO.md Implement TODO

---

_**Assistant**_

I'll help you implement the next TODO item from the list. Let me analyze the TODO.md file and determine what needs to be done next.

According to TODO.md, we're currently at Phase 2, and the next item marked with "**<-- NEXT**" is:

2.1.3. Add unit tests for each of these methods in `tests/test_twat_cache.py`

Let me first check if this file exists and what other test files we have to understand the testing structure.

---

_****_



---

_****_



Let me check the existing test files to understand our testing structure and patterns.

---

_****_

<details>
            <summary>Listed directory tests • **7** results</summary>
        
| Name |
|-------|
| 📄 `__pycache__` |
| 📄 `test_cache.py` |
| 📄 `test_sql_cache.py` |
| 📄 `test_redis_cache.py` |
| 📄 `test_engines.py` |
| 📄 `test_config.py` |
| 📄 `test_twat_cache.py` |

</details>

---

_****_



I see that `test_twat_cache.py` exists but is very small. Let me check its current content:

---

_****_

Read file: tests/test_twat_cache.py

---

_****_



Now let me check one of the existing test files to understand our testing patterns:

---

_****_

Read file: tests/test_engines.py

---

_****_



I apologize for the timeout. Let me try reading a smaller portion:

---

_****_

Read file: tests/test_engines.py

---

_****_



Based on the analysis of the existing code and TODO list, I'll now implement the required test cases in `test_twat_cache.py`. We'll need to test each cache engine's core functionality.

---

_****_

```diff
- """Test suite for twat_cache."""
- 
- 
- def test_version():
-     """Verify package exposes version."""
-     import twat_cache
- 
-     assert twat_cache.__version__
+ #!/usr/bin/env -S uv run
+ # /// script
+ # dependencies = [
+ #   "pytest",
+ #   "pytest-asyncio",
+ #   "numpy",
+ #   "loguru",
+ # ]
+ # ///
+ # this_file: tests/test_twat_cache.py
+ 
+ """Test suite for twat_cache core functionality.
+ 
+ This module contains comprehensive tests for all cache engine implementations,
+ focusing on the core _get, _set, and clear methods.
+ """
+ 
+ from pathlib import Path
+ import numpy as np
+ import pytest
+ from typing import Any
+ 
+ from twat_cache.engines.lru import LRUCacheEngine
+ from twat_cache.engines.cachebox import CacheBoxEngine
+ from twat_cache.engines.cachetools import CacheToolsEngine
+ from twat_cache.engines.diskcache import DiskCacheEngine
+ from twat_cache.engines.joblib import JoblibEngine
+ from twat_cache.engines.klepto import KleptoEngine
+ from twat_cache.engines.aiocache import AioCacheEngine
+ from twat_cache.types import CacheConfig, CacheKey
+ 
+ 
+ # Test configurations
+ @pytest.fixture
+ def base_config() -> CacheConfig:
+     """Provide a basic cache configuration."""
+     return CacheConfig(maxsize=100)
+ 
+ 
+ @pytest.fixture
+ def temp_path(tmp_path: Path) -> Path:
+     """Provide a temporary directory for disk-based caches."""
+     return tmp_path / "cache"
+ 
+ 
+ # LRU Cache Tests
+ @pytest.fixture
+ def lru_engine(base_config: CacheConfig) -> LRUCacheEngine:
+     """Create an LRU cache engine instance."""
+     return LRUCacheEngine(base_config)
+ 
+ 
+ def test_lru_cache_get_set(lru_engine: LRUCacheEngine) -> None:
+     """Test basic get/set operations for LRU cache."""
+     key: CacheKey = "test_key"
+     value = "test_value"
+ 
+     # Test cache miss
+     assert lru_engine._get_cached_value(key) is None
+ 
+     # Test cache hit
+     lru_engine._set_cached_value(key, value)
+     assert lru_engine._get_cached_value(key) == value
+ 
+ 
+ def test_lru_cache_clear(lru_engine: LRUCacheEngine) -> None:
+     """Test clear operation for LRU cache."""
+     key: CacheKey = "test_key"
+     value = "test_value"
+ 
+     lru_engine._set_cached_value(key, value)
+     lru_engine.clear()
+     assert lru_engine._get_cached_value(key) is None
+ 
+ 
+ def test_lru_cache_maxsize(lru_engine: LRUCacheEngine) -> None:
+     """Test maxsize enforcement for LRU cache."""
+     for i in range(150):  # More than maxsize
+         lru_engine._set_cached_value(f"key_{i}", f"value_{i}")
+ 
+     # Oldest entries should be evicted
+     assert lru_engine._get_cached_value("key_0") is None
+     assert lru_engine._get_cached_value("key_149") is not None
+ 
+ 
+ # DiskCache Tests
+ @pytest.fixture
+ def disk_engine(base_config: CacheConfig, temp_path: Path) -> DiskCacheEngine:
+     """Create a disk cache engine instance."""
+     config = CacheConfig(maxsize=100, cache_dir=str(temp_path))
+     return DiskCacheEngine(config)
+ 
+ 
+ def test_disk_cache_persistence(disk_engine: DiskCacheEngine) -> None:
+     """Test persistence of disk cache."""
+     key: CacheKey = "test_key"
+     value = "test_value"
+ 
+     disk_engine._set_cached_value(key, value)
+     assert disk_engine._get_cached_value(key) == value
+ 
+     # Create new instance with same path
+     config = disk_engine.config
+     new_engine = DiskCacheEngine(config)
+     assert new_engine._get_cached_value(key) == value
+ 
+ 
+ # Joblib Tests
+ @pytest.fixture
+ def joblib_engine(base_config: CacheConfig, temp_path: Path) -> JoblibEngine:
+     """Create a joblib cache engine instance."""
+     config = CacheConfig(maxsize=100, cache_dir=str(temp_path))
+     return JoblibEngine(config)
+ 
+ 
+ def test_joblib_numpy_array(joblib_engine: JoblibEngine) -> None:
+     """Test joblib cache with NumPy arrays."""
+     key: CacheKey = "array_key"
+     value = np.array([[1, 2], [3, 4]])
+ 
+     joblib_engine._set_cached_value(key, value)
+     cached = joblib_engine._get_cached_value(key)
+     assert isinstance(cached, np.ndarray)
+     assert np.array_equal(cached, value)
+ 
+ 
+ # Klepto Tests
+ @pytest.fixture
+ def klepto_engine(base_config: CacheConfig, temp_path: Path) -> KleptoEngine:
+     """Create a klepto cache engine instance."""
+     config = CacheConfig(maxsize=100, cache_dir=str(temp_path))
+     return KleptoEngine(config)
+ 
+ 
+ def test_klepto_persistence(klepto_engine: KleptoEngine) -> None:
+     """Test persistence of klepto cache."""
+     key: CacheKey = "test_key"
+     value = {"complex": "data", "nested": {"value": 42}}
+ 
+     klepto_engine._set_cached_value(key, value)
+     assert klepto_engine._get_cached_value(key) == value
+ 
+ 
+ # Async Cache Tests
+ @pytest.fixture
+ async def async_engine(base_config: CacheConfig) -> AioCacheEngine:
+     """Create an async cache engine instance."""
+     return AioCacheEngine(base_config)
+ 
+ 
+ @pytest.mark.asyncio
+ async def test_async_cache_operations(async_engine: AioCacheEngine) -> None:
+     """Test async cache operations."""
+     key: CacheKey = "test_key"
+     value = "test_value"
+ 
+     assert await async_engine._get_cached_value(key) is None
+     await async_engine._set_cached_value(key, value)
+     assert await async_engine._get_cached_value(key) == value
+ 
+     await async_engine.clear()
+     assert await async_engine._get_cached_value(key) is None
+ 
+ 
+ # CacheBox Tests
+ @pytest.fixture
+ def cachebox_engine(base_config: CacheConfig) -> CacheBoxEngine:
+     """Create a cachebox engine instance."""
+     return CacheBoxEngine(base_config)
+ 
+ 
+ def test_cachebox_operations(cachebox_engine: CacheBoxEngine) -> None:
+     """Test basic operations for cachebox."""
+     key: CacheKey = "test_key"
+     value = "test_value"
+ 
+     assert cachebox_engine._get_cached_value(key) is None
+     cachebox_engine._set_cached_value(key, value)
+     assert cachebox_engine._get_cached_value(key) == value
+ 
+     cachebox_engine.clear()
+     assert cachebox_engine._get_cached_value(key) is None
+ 
+ 
+ # CacheTools Tests
+ @pytest.fixture
+ def cachetools_engine(base_config: CacheConfig) -> CacheToolsEngine:
+     """Create a cachetools engine instance."""
+     return CacheToolsEngine(base_config)
+ 
+ 
+ def test_cachetools_operations(cachetools_engine: CacheToolsEngine) -> None:
+     """Test basic operations for cachetools."""
+     key: CacheKey = "test_key"
+     value = "test_value"
+ 
+     assert cachetools_engine._get_cached_value(key) is None
+     cachetools_engine._set_cached_value(key, value)
+     assert cachetools_engine._get_cached_value(key) == value
+ 
+     cachetools_engine.clear()
+     assert cachetools_engine._get_cached_value(key) is None
  
```

---

_****_



I notice that we need to fix the linter errors related to missing `py.typed` markers. Let me check if we already have a `py.typed` file in the right location:

---

_****_

<details>
            <summary>Listed directory src/twat_cache • **13** results</summary>
        
| Name |
|-------|
| 📄 `types.py` |
| 📄 `engines` |
| 📄 `__main__.py` |
| 📄 `paths.py` |
| 📄 `__version__.py` |
| 📄 `__pycache__` |
| 📄 `cache.py` |
| 📄 `config.py` |
| 📄 `__init__.py` |
| 📄 `utils.py` |
| 📄 `py.typed` |
| 📄 `decorators.py` |
| 📄 `.DS_Store` |

</details>

---

_****_

<details>
            <summary>Listed directory src/twat_cache/engines • **12** results</summary>
        
| Name |
|-------|
| 📄 `klepto.py` |
| 📄 `cachebox.py` |
| 📄 `cachetools.py` |
| 📄 `diskcache.py` |
| 📄 `joblib.py` |
| 📄 `aiocache.py` |
| 📄 `manager.py` |
| 📄 `base.py` |
| 📄 `lru.py` |
| 📄 `py.typed` |
| 📄 `__init__.py` |
| 📄 `__pycache__` |

</details>

---

_****_



I see that we already have `py.typed` files in both the main package directory and the engines directory. The linter errors are likely due to the packages not being properly installed in development mode. Let me check if we have a development installation command in the project:

---

_****_

Read file: pyproject.toml

---

_****_



I see that we have a development environment setup using Hatch. Let me install the package in development mode:

---

_****_

```bash
uv pip install -e .
```

```
Resolved 1 package in 23ms
Prepared 1 package in 1.31s
Uninstalled 1 package in 3ms
Installed 1 package in 2ms
 ~ twat-cache==0.1.0 (from file:///Users/adam/Developer/vcs/github.twardoc
h/pub/twat-packages/_good/twat/plugins/repos/twat_cache)                  
```

---

_****_



Now let me install the test dependencies:

---

_****_

```bash
uv pip install pytest pytest-asyncio numpy loguru
```

```
adam@Hamlet twat_cache % uv pip install pytest pytest-asyncio numpy loguru
                         uv pip install pytest pytest-asyncio numpy loguru
 
Resolved 7 packages in 200ms
Installed 7 packages in 72ms
 + iniconfig==2.0.0
 + loguru==0.7.3
 + numpy==2.2.3
 + packaging==24.2
 + pluggy==1.5.0
 + pytest==8.3.4
 + pytest-asyncio==0.25.3
adam@Hamlet twat_cache %
```

---

_****_





Now let me install the optional dependencies needed for testing all cache backends:

---

_****_

```bash
uv pip install cachebox cachetools aiocache klepto diskcache joblib
```

```
adam@Hamlet twat_cache % uv pip install cachebox cachetools aiocache klept
o diskcache joblib       uv pip install cachebox cachetools aiocache klept
o diskcache joblib
Audited 6 packages in 3ms
adam@Hamlet twat_cache %
```

---

_****_





Now let's run the tests to see if they work:

---

_****_

```bash
python -m pytest tests/test_twat_cache.py -v
```

```
adam@Hamlet twat_cache % 
        exception = None
        only_new_style_wrappers = True
        try:  # run impl and wrapper setup functions in a loop
            teardowns: list[Teardown] = []
            try:
                for hook_impl in reversed(hook_impls):
                    try:
                        args = [caller_kwargs[argname] for argname in hook
_impl.argnames]
                    except KeyError:
                        for argname in hook_impl.argnames:
                            if argname not in caller_kwargs:
                                raise HookCallError(
                                    f"hook call must provide argument {arg
name!r}"
                                )
    
                    if hook_impl.hookwrapper:
                        only_new_style_wrappers = False
                        try:
                            # If this cast is not valid, a type error is r
aised below,
                            # which is the desired response.
                            res = hook_impl.function(*args)
                            wrapper_gen = cast(Generator[None, Result[obje
ct], None], res)
                            next(wrapper_gen)  # first yield
                            teardowns.append((wrapper_gen, hook_impl))
                        except StopIteration:
                            _raise_wrapfail(wrapper_gen, "did not yield")
                    elif hook_impl.wrapper:
                        try:
                            # If this cast is not valid, a type error is r
aised below,
                            # which is the desired response.
                            res = hook_impl.function(*args)
                            function_gen = cast(Generator[None, object, ob
ject], res)
                            next(function_gen)  # first yield
                            teardowns.append(function_gen)
                        except StopIteration:
                            _raise_wrapfail(function_gen, "did not yield")
                    else:
                        res = hook_impl.function(*args)
                        if res is not None:
                            results.append(res)
                            if firstresult:  # halt further impl calls
                                break
            except BaseException as exc:
                exception = exc
        finally:
            # Fast path - only new-style wrappers, no Result.
            if only_new_style_wrappers:
                if firstresult:  # first result hooks return a single valu
e
                    result = results[0] if results else None
                else:
                    result = results
    
                # run all wrapper post-yield blocks
                for teardown in reversed(teardowns):
                    try:
                        if exception is not None:
                            teardown.throw(exception)  # type: ignore[unio
n-attr]
                        else:
                            teardown.send(result)  # type: ignore[union-at
tr]
                        # Following is unreachable for a well behaved hook
 wrapper.
                        # Try to force finalizers otherwise postponed till
 GC action.
                        # Note: close() may raise if generator handles Gen
eratorExit.
                        teardown.close()  # type: ignore[union-attr]
                    except StopIteration as si:
                        result = si.value
                        exception = None
                        continue
                    except BaseException as e:
                        exception = e
                        continue
                    _raise_wrapfail(teardown, "has second yield")  # type:
 ignore[arg-type]
    
                if exception is not None:
                    raise exception.with_traceback(exception.__traceback__
)
                else:
                    return result
    
            # Slow path - need to support old-style wrappers.
            else:
                if firstresult:  # first result hooks return a single valu
e
                    outcome: Result[object | list[object]] = Result(
                        results[0] if results else None, exception
                    )
                else:
                    outcome = Result(results, exception)
    
                # run all wrapper post-yield blocks
                for teardown in reversed(teardowns):
                    if isinstance(teardown, tuple):
                        try:
                            teardown[0].send(outcome)
                        except StopIteration:
                            pass
                        except BaseException as e:
                            _warn_teardown_exception(hook_name, teardown[1
], e)
                            raise
                        else:
                            _raise_wrapfail(teardown[0], "has second yield
")
                    else:
                        try:
                            if outcome._exception is not None:
>                               teardown.throw(outcome._exception)

/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/pluggy/_callers.py:167:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

    @pytest.hookimpl(wrapper=True, tryfirst=True)
    def pytest_runtest_call() -> Generator[None]:
>       yield from thread_exception_runtest_hook()

/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/_pytest/threadexception.py:92:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

    def thread_exception_runtest_hook() -> Generator[None]:
        with catch_threading_exception() as cm:
            try:
>               yield

/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/_pytest/threadexception.py:68:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

hook_name = 'pytest_runtest_call'
hook_impls = [<HookImpl plugin_name='runner', plugin=<module '_pytest.runn
er' from '/Library/Frameworks/Python.framework/Versions/3...pper name='/de
v/null' mode='r' encoding='utf-8'>> _state='suspended' _in_suspended=False
> _capture_fixture=None>>, ...]
caller_kwargs = {'item': <RuffItem ruff>}, firstresult = False

    def _multicall(
        hook_name: str,
        hook_impls: Sequence[HookImpl],
        caller_kwargs: Mapping[str, object],
        firstresult: bool,
    ) -> object | list[object]:
        """Execute a call into multiple python functions/methods and retur
n the
        result(s).
    
        ``caller_kwargs`` comes from HookCaller.__call__().
        """
        __tracebackhide__ = True
        results: list[object] = []
        exception = None
        only_new_style_wrappers = True
        try:  # run impl and wrapper setup functions in a loop
            teardowns: list[Teardown] = []
            try:
                for hook_impl in reversed(hook_impls):
                    try:
                        args = [caller_kwargs[argname] for argname in hook
_impl.argnames]
                    except KeyError:
                        for argname in hook_impl.argnames:
                            if argname not in caller_kwargs:
                                raise HookCallError(
                                    f"hook call must provide argument {arg
name!r}"
                                )
    
                    if hook_impl.hookwrapper:
                        only_new_style_wrappers = False
                        try:
                            # If this cast is not valid, a type error is r
aised below,
                            # which is the desired response.
                            res = hook_impl.function(*args)
                            wrapper_gen = cast(Generator[None, Result[obje
ct], None], res)
                            next(wrapper_gen)  # first yield
                            teardowns.append((wrapper_gen, hook_impl))
                        except StopIteration:
                            _raise_wrapfail(wrapper_gen, "did not yield")
                    elif hook_impl.wrapper:
                        try:
                            # If this cast is not valid, a type error is r
aised below,
                            # which is the desired response.
                            res = hook_impl.function(*args)
                            function_gen = cast(Generator[None, object, ob
ject], res)
                            next(function_gen)  # first yield
                            teardowns.append(function_gen)
                        except StopIteration:
                            _raise_wrapfail(function_gen, "did not yield")
                    else:
                        res = hook_impl.function(*args)
                        if res is not None:
                            results.append(res)
                            if firstresult:  # halt further impl calls
                                break
            except BaseException as exc:
                exception = exc
        finally:
            # Fast path - only new-style wrappers, no Result.
            if only_new_style_wrappers:
                if firstresult:  # first result hooks return a single valu
e
                    result = results[0] if results else None
                else:
                    result = results
    
                # run all wrapper post-yield blocks
                for teardown in reversed(teardowns):
                    try:
                        if exception is not None:
                            teardown.throw(exception)  # type: ignore[unio
n-attr]
                        else:
                            teardown.send(result)  # type: ignore[union-at
tr]
                        # Following is unreachable for a well behaved hook
 wrapper.
                        # Try to force finalizers otherwise postponed till
 GC action.
                        # Note: close() may raise if generator handles Gen
eratorExit.
                        teardown.close()  # type: ignore[union-attr]
                    except StopIteration as si:
                        result = si.value
                        exception = None
                        continue
                    except BaseException as e:
                        exception = e
                        continue
                    _raise_wrapfail(teardown, "has second yield")  # type:
 ignore[arg-type]
    
                if exception is not None:
                    raise exception.with_traceback(exception.__traceback__
)
                else:
                    return result
    
            # Slow path - need to support old-style wrappers.
            else:
                if firstresult:  # first result hooks return a single valu
e
                    outcome: Result[object | list[object]] = Result(
                        results[0] if results else None, exception
                    )
                else:
                    outcome = Result(results, exception)
    
                # run all wrapper post-yield blocks
                for teardown in reversed(teardowns):
                    if isinstance(teardown, tuple):
                        try:
                            teardown[0].send(outcome)
                        except StopIteration:
                            pass
                        except BaseException as e:
                            _warn_teardown_exception(hook_name, teardown[1
], e)
                            raise
                        else:
                            _raise_wrapfail(teardown[0], "has second yield
")
                    else:
                        try:
                            if outcome._exception is not None:
>                               teardown.throw(outcome._exception)

/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/pluggy/_callers.py:167:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

    @pytest.hookimpl(wrapper=True, tryfirst=True)
    def pytest_runtest_call() -> Generator[None]:
>       yield from unraisable_exception_runtest_hook()

/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/_pytest/unraisableexception.py:95:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

    def unraisable_exception_runtest_hook() -> Generator[None]:
        with catch_unraisable_exception() as cm:
            try:
>               yield

/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/_pytest/unraisableexception.py:70:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

hook_name = 'pytest_runtest_call'
hook_impls = [<HookImpl plugin_name='runner', plugin=<module '_pytest.runn
er' from '/Library/Frameworks/Python.framework/Versions/3...pper name='/de
v/null' mode='r' encoding='utf-8'>> _state='suspended' _in_suspended=False
> _capture_fixture=None>>, ...]
caller_kwargs = {'item': <RuffItem ruff>}, firstresult = False

    def _multicall(
        hook_name: str,
        hook_impls: Sequence[HookImpl],
        caller_kwargs: Mapping[str, object],
        firstresult: bool,
    ) -> object | list[object]:
        """Execute a call into multiple python functions/methods and retur
n the
        result(s).
    
        ``caller_kwargs`` comes from HookCaller.__call__().
        """
        __tracebackhide__ = True
        results: list[object] = []
        exception = None
        only_new_style_wrappers = True
        try:  # run impl and wrapper setup functions in a loop
            teardowns: list[Teardown] = []
            try:
                for hook_impl in reversed(hook_impls):
                    try:
                        args = [caller_kwargs[argname] for argname in hook
_impl.argnames]
                    except KeyError:
                        for argname in hook_impl.argnames:
                            if argname not in caller_kwargs:
                                raise HookCallError(
                                    f"hook call must provide argument {arg
name!r}"
                                )
    
                    if hook_impl.hookwrapper:
                        only_new_style_wrappers = False
                        try:
                            # If this cast is not valid, a type error is r
aised below,
                            # which is the desired response.
                            res = hook_impl.function(*args)
                            wrapper_gen = cast(Generator[None, Result[obje
ct], None], res)
                            next(wrapper_gen)  # first yield
                            teardowns.append((wrapper_gen, hook_impl))
                        except StopIteration:
                            _raise_wrapfail(wrapper_gen, "did not yield")
                    elif hook_impl.wrapper:
                        try:
                            # If this cast is not valid, a type error is r
aised below,
                            # which is the desired response.
                            res = hook_impl.function(*args)
                            function_gen = cast(Generator[None, object, ob
ject], res)
                            next(function_gen)  # first yield
                            teardowns.append(function_gen)
                        except StopIteration:
                            _raise_wrapfail(function_gen, "did not yield")
                    else:
                        res = hook_impl.function(*args)
                        if res is not None:
                            results.append(res)
                            if firstresult:  # halt further impl calls
                                break
            except BaseException as exc:
                exception = exc
        finally:
            # Fast path - only new-style wrappers, no Result.
            if only_new_style_wrappers:
                if firstresult:  # first result hooks return a single valu
e
                    result = results[0] if results else None
                else:
                    result = results
    
                # run all wrapper post-yield blocks
                for teardown in reversed(teardowns):
                    try:
                        if exception is not None:
                            teardown.throw(exception)  # type: ignore[unio
n-attr]
                        else:
                            teardown.send(result)  # type: ignore[union-at
tr]
                        # Following is unreachable for a well behaved hook
 wrapper.
                        # Try to force finalizers otherwise postponed till
 GC action.
                        # Note: close() may raise if generator handles Gen
eratorExit.
                        teardown.close()  # type: ignore[union-attr]
                    except StopIteration as si:
                        result = si.value
                        exception = None
                        continue
                    except BaseException as e:
                        exception = e
                        continue
                    _raise_wrapfail(teardown, "has second yield")  # type:
 ignore[arg-type]
    
                if exception is not None:
                    raise exception.with_traceback(exception.__traceback__
)
                else:
                    return result
    
            # Slow path - need to support old-style wrappers.
            else:
                if firstresult:  # first result hooks return a single valu
e
                    outcome: Result[object | list[object]] = Result(
                        results[0] if results else None, exception
                    )
                else:
                    outcome = Result(results, exception)
    
                # run all wrapper post-yield blocks
                for teardown in reversed(teardowns):
                    if isinstance(teardown, tuple):
                        try:
                            teardown[0].send(outcome)
                        except StopIteration:
                            pass
                        except BaseException as e:
                            _warn_teardown_exception(hook_name, teardown[1
], e)
                            raise
                        else:
                            _raise_wrapfail(teardown[0], "has second yield
")
                    else:
                        try:
                            if outcome._exception is not None:
>                               teardown.throw(outcome._exception)

/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/pluggy/_callers.py:167:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <_pytest.logging.LoggingPlugin object at 0x111e21700>
item = <RuffItem ruff>

    @hookimpl(wrapper=True)
    def pytest_runtest_call(self, item: nodes.Item) -> Generator[None]:
        self.log_cli_handler.set_when("call")
    
>       yield from self._runtest_for(item, "call")

/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/_pytest/logging.py:846:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <_pytest.logging.LoggingPlugin object at 0x111e21700>
item = <RuffItem ruff>, when = 'call'

    def _runtest_for(self, item: nodes.Item, when: str) -> Generator[None]
:
        """Implement the internals of the pytest_runtest_xxx() hooks."""
        with catching_logs(
            self.caplog_handler,
            level=self.log_level,
        ) as caplog_handler, catching_logs(
            self.report_handler,
            level=self.log_level,
        ) as report_handler:
            caplog_handler.reset()
            report_handler.reset()
            item.stash[caplog_records_key][when] = caplog_handler.records
            item.stash[caplog_handler_key] = caplog_handler
    
            try:
>               yield

/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/_pytest/logging.py:829:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

hook_name = 'pytest_runtest_call'
hook_impls = [<HookImpl plugin_name='runner', plugin=<module '_pytest.runn
er' from '/Library/Frameworks/Python.framework/Versions/3...pper name='/de
v/null' mode='r' encoding='utf-8'>> _state='suspended' _in_suspended=False
> _capture_fixture=None>>, ...]
caller_kwargs = {'item': <RuffItem ruff>}, firstresult = False

    def _multicall(
        hook_name: str,
        hook_impls: Sequence[HookImpl],
        caller_kwargs: Mapping[str, object],
        firstresult: bool,
    ) -> object | list[object]:
        """Execute a call into multiple python functions/methods and retur
n the
        result(s).
    
        ``caller_kwargs`` comes from HookCaller.__call__().
        """
        __tracebackhide__ = True
        results: list[object] = []
        exception = None
        only_new_style_wrappers = True
        try:  # run impl and wrapper setup functions in a loop
            teardowns: list[Teardown] = []
            try:
                for hook_impl in reversed(hook_impls):
                    try:
                        args = [caller_kwargs[argname] for argname in hook
_impl.argnames]
                    except KeyError:
                        for argname in hook_impl.argnames:
                            if argname not in caller_kwargs:
                                raise HookCallError(
                                    f"hook call must provide argument {arg
name!r}"
                                )
    
                    if hook_impl.hookwrapper:
                        only_new_style_wrappers = False
                        try:
                            # If this cast is not valid, a type error is r
aised below,
                            # which is the desired response.
                            res = hook_impl.function(*args)
                            wrapper_gen = cast(Generator[None, Result[obje
ct], None], res)
                            next(wrapper_gen)  # first yield
                            teardowns.append((wrapper_gen, hook_impl))
                        except StopIteration:
                            _raise_wrapfail(wrapper_gen, "did not yield")
                    elif hook_impl.wrapper:
                        try:
                            # If this cast is not valid, a type error is r
aised below,
                            # which is the desired response.
                            res = hook_impl.function(*args)
                            function_gen = cast(Generator[None, object, ob
ject], res)
                            next(function_gen)  # first yield
                            teardowns.append(function_gen)
                        except StopIteration:
                            _raise_wrapfail(function_gen, "did not yield")
                    else:
                        res = hook_impl.function(*args)
                        if res is not None:
                            results.append(res)
                            if firstresult:  # halt further impl calls
                                break
            except BaseException as exc:
                exception = exc
        finally:
            # Fast path - only new-style wrappers, no Result.
            if only_new_style_wrappers:
                if firstresult:  # first result hooks return a single valu
e
                    result = results[0] if results else None
                else:
                    result = results
    
                # run all wrapper post-yield blocks
                for teardown in reversed(teardowns):
                    try:
                        if exception is not None:
                            teardown.throw(exception)  # type: ignore[unio
n-attr]
                        else:
                            teardown.send(result)  # type: ignore[union-at
tr]
                        # Following is unreachable for a well behaved hook
 wrapper.
                        # Try to force finalizers otherwise postponed till
 GC action.
                        # Note: close() may raise if generator handles Gen
eratorExit.
                        teardown.close()  # type: ignore[union-attr]
                    except StopIteration as si:
                        result = si.value
                        exception = None
                        continue
                    except BaseException as e:
                        exception = e
                        continue
                    _raise_wrapfail(teardown, "has second yield")  # type:
 ignore[arg-type]
    
                if exception is not None:
                    raise exception.with_traceback(exception.__traceback__
)
                else:
                    return result
    
            # Slow path - need to support old-style wrappers.
            else:
                if firstresult:  # first result hooks return a single valu
e
                    outcome: Result[object | list[object]] = Result(
                        results[0] if results else None, exception
                    )
                else:
                    outcome = Result(results, exception)
    
                # run all wrapper post-yield blocks
                for teardown in reversed(teardowns):
                    if isinstance(teardown, tuple):
                        try:
                            teardown[0].send(outcome)
                        except StopIteration:
                            pass
                        except BaseException as e:
                            _warn_teardown_exception(hook_name, teardown[1
], e)
                            raise
                        else:
                            _raise_wrapfail(teardown[0], "has second yield
")
                    else:
                        try:
                            if outcome._exception is not None:
>                               teardown.throw(outcome._exception)

/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/pluggy/_callers.py:167:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <CaptureManager _method='fd' _global_capturing=<MultiCapture out=<F
DCapture 1 oldfd=7 _state='suspended' tmpfile=<_io....xtIOWrapper name='/d
ev/null' mode='r' encoding='utf-8'>> _state='suspended' _in_suspended=Fals
e> _capture_fixture=None>
item = <RuffItem ruff>

    @hookimpl(wrapper=True)
    def pytest_runtest_call(self, item: Item) -> Generator[None]:
        with self.item_capture("call", item):
>           return (yield)

/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/_pytest/capture.py:880:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

hook_name = 'pytest_runtest_call'
hook_impls = [<HookImpl plugin_name='runner', plugin=<module '_pytest.runn
er' from '/Library/Frameworks/Python.framework/Versions/3...pper name='/de
v/null' mode='r' encoding='utf-8'>> _state='suspended' _in_suspended=False
> _capture_fixture=None>>, ...]
caller_kwargs = {'item': <RuffItem ruff>}, firstresult = False

    def _multicall(
        hook_name: str,
        hook_impls: Sequence[HookImpl],
        caller_kwargs: Mapping[str, object],
        firstresult: bool,
    ) -> object | list[object]:
        """Execute a call into multiple python functions/methods and retur
n the
        result(s).
    
        ``caller_kwargs`` comes from HookCaller.__call__().
        """
        __tracebackhide__ = True
        results: list[object] = []
        exception = None
        only_new_style_wrappers = True
        try:  # run impl and wrapper setup functions in a loop
            teardowns: list[Teardown] = []
            try:
                for hook_impl in reversed(hook_impls):
                    try:
                        args = [caller_kwargs[argname] for argname in hook
_impl.argnames]
                    except KeyError:
                        for argname in hook_impl.argnames:
                            if argname not in caller_kwargs:
                                raise HookCallError(
                                    f"hook call must provide argument {arg
name!r}"
                                )
    
                    if hook_impl.hookwrapper:
                        only_new_style_wrappers = False
                        try:
                            # If this cast is not valid, a type error is r
aised below,
                            # which is the desired response.
                            res = hook_impl.function(*args)
                            wrapper_gen = cast(Generator[None, Result[obje
ct], None], res)
                            next(wrapper_gen)  # first yield
                            teardowns.append((wrapper_gen, hook_impl))
                        except StopIteration:
                            _raise_wrapfail(wrapper_gen, "did not yield")
                    elif hook_impl.wrapper:
                        try:
                            # If this cast is not valid, a type error is r
aised below,
                            # which is the desired response.
                            res = hook_impl.function(*args)
                            function_gen = cast(Generator[None, object, ob
ject], res)
                            next(function_gen)  # first yield
                            teardowns.append(function_gen)
                        except StopIteration:
                            _raise_wrapfail(function_gen, "did not yield")
                    else:
                        res = hook_impl.function(*args)
                        if res is not None:
                            results.append(res)
                            if firstresult:  # halt further impl calls
                                break
            except BaseException as exc:
                exception = exc
        finally:
            # Fast path - only new-style wrappers, no Result.
            if only_new_style_wrappers:
                if firstresult:  # first result hooks return a single valu
e
                    result = results[0] if results else None
                else:
                    result = results
    
                # run all wrapper post-yield blocks
                for teardown in reversed(teardowns):
                    try:
                        if exception is not None:
                            teardown.throw(exception)  # type: ignore[unio
n-attr]
                        else:
                            teardown.send(result)  # type: ignore[union-at
tr]
                        # Following is unreachable for a well behaved hook
 wrapper.
                        # Try to force finalizers otherwise postponed till
 GC action.
                        # Note: close() may raise if generator handles Gen
eratorExit.
                        teardown.close()  # type: ignore[union-attr]
                    except StopIteration as si:
                        result = si.value
                        exception = None
                        continue
                    except BaseException as e:
                        exception = e
                        continue
                    _raise_wrapfail(teardown, "has second yield")  # type:
 ignore[arg-type]
    
                if exception is not None:
                    raise exception.with_traceback(exception.__traceback__
)
                else:
                    return result
    
            # Slow path - need to support old-style wrappers.
            else:
                if firstresult:  # first result hooks return a single valu
e
                    outcome: Result[object | list[object]] = Result(
                        results[0] if results else None, exception
                    )
                else:
                    outcome = Result(results, exception)
    
                # run all wrapper post-yield blocks
                for teardown in reversed(teardowns):
                    if isinstance(teardown, tuple):
                        try:
                            teardown[0].send(outcome)
                        except StopIteration:
                            pass
                        except BaseException as e:
                            _warn_teardown_exception(hook_name, teardown[1
], e)
                            raise
                        else:
                            _raise_wrapfail(teardown[0], "has second yield
")
                    else:
                        try:
                            if outcome._exception is not None:
>                               teardown.throw(outcome._exception)

/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/pluggy/_callers.py:167:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

item = <RuffItem ruff>

    @hookimpl(wrapper=True)
    def pytest_runtest_call(item: Item) -> Generator[None]:
        xfailed = item.stash.get(xfailed_key, None)
        if xfailed is None:
            item.stash[xfailed_key] = xfailed = evaluate_xfail_marks(item)
    
        if xfailed and not item.config.option.runxfail and not xfailed.run
:
            xfail("[NOTRUN] " + xfailed.reason)
    
        try:
>           return (yield)

/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/_pytest/skipping.py:257:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

hook_name = 'pytest_runtest_call'
hook_impls = [<HookImpl plugin_name='runner', plugin=<module '_pytest.runn
er' from '/Library/Frameworks/Python.framework/Versions/3...pper name='/de
v/null' mode='r' encoding='utf-8'>> _state='suspended' _in_suspended=False
> _capture_fixture=None>>, ...]
caller_kwargs = {'item': <RuffItem ruff>}, firstresult = False

    def _multicall(
        hook_name: str,
        hook_impls: Sequence[HookImpl],
        caller_kwargs: Mapping[str, object],
        firstresult: bool,
    ) -> object | list[object]:
        """Execute a call into multiple python functions/methods and retur
n the
        result(s).
    
        ``caller_kwargs`` comes from HookCaller.__call__().
        """
        __tracebackhide__ = True
        results: list[object] = []
        exception = None
        only_new_style_wrappers = True
        try:  # run impl and wrapper setup functions in a loop
            teardowns: list[Teardown] = []
            try:
                for hook_impl in reversed(hook_impls):
                    try:
                        args = [caller_kwargs[argname] for argname in hook
_impl.argnames]
                    except KeyError:
                        for argname in hook_impl.argnames:
                            if argname not in caller_kwargs:
                                raise HookCallError(
                                    f"hook call must provide argument {arg
name!r}"
                                )
    
                    if hook_impl.hookwrapper:
                        only_new_style_wrappers = False
                        try:
                            # If this cast is not valid, a type error is r
aised below,
                            # which is the desired response.
                            res = hook_impl.function(*args)
                            wrapper_gen = cast(Generator[None, Result[obje
ct], None], res)
                            next(wrapper_gen)  # first yield
                            teardowns.append((wrapper_gen, hook_impl))
                        except StopIteration:
                            _raise_wrapfail(wrapper_gen, "did not yield")
                    elif hook_impl.wrapper:
                        try:
                            # If this cast is not valid, a type error is r
aised below,
                            # which is the desired response.
                            res = hook_impl.function(*args)
                            function_gen = cast(Generator[None, object, ob
ject], res)
                            next(function_gen)  # first yield
                            teardowns.append(function_gen)
                        except StopIteration:
                            _raise_wrapfail(function_gen, "did not yield")
                    else:
>                       res = hook_impl.function(*args)

/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/pluggy/_callers.py:103:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

item = <RuffItem ruff>

    def pytest_runtest_call(item: Item) -> None:
        _update_current_test_var(item, "call")
        try:
            del sys.last_type
            del sys.last_value
            del sys.last_traceback
            if sys.version_info >= (3, 12, 0):
                del sys.last_exc  # type:ignore[attr-defined]
        except AttributeError:
            pass
        try:
>           item.runtest()

/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/_pytest/runner.py:174:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <RuffItem ruff>

    def runtest(self):
>       self.handler(path=self.fspath)

/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/pytest_ruff/__init__.py:141:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <RuffItem ruff>
path = local('/Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/
_good/twat/plugins/repos/twat_cache/tests/test_twat_cache.py')

    def handler(self, path):
>       return check_file(path)

/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/pytest_ruff/__init__.py:151:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

path = local('/Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/
_good/twat/plugins/repos/twat_cache/tests/test_twat_cache.py')

    def check_file(path):
        ruff = find_ruff_bin()
        command = [
            ruff,
            "check",
            path,
            "--quiet",
            "--output-format=full",
            "--force-exclude",
        ]
        child = Popen(command, stdout=PIPE, stderr=PIPE)
        stdout, stderr = child.communicate()
    
        if child.returncode == 1:
>           raise RuffError(stdout.decode())
E           pytest_ruff.RuffError: tests/test_twat_cache.py:21:20: F401 [*
] `typing.Any` imported but unused
E              |
E           19 | import numpy as np
E           20 | import pytest
E           21 | from typing import Any
E              |                    ^^^ F401
E           22 |
E           23 | from twat_cache.engines.lru import LRUCacheEngine
E              |
E              = help: Remove unused import: `typing.Any`

/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/pytest_ruff/__init__.py:101: RuffError

 tests/test_twat_cache.py:: ⨯                               67% ██████▋

[gw0] FAILED tests/test_twat_cache.py 
 tests/test_twat_cache.py::Black format check ✓            100% ██████████
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/coverage/inorout.py:508: CoverageWarning: Module tests was never imp
orted. (module-not-imported)
  self.warn(f"Module {pkg} was never imported.", slug="module-not-imported
")


---------- coverage: platform darwin, python 3.12.8-final-0 ----------
Name

                                        Stmts   Miss Branch BrPart  Cover
--------------------------------------------------------------------------
-------------------------------------------------------------------------
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/__init__.py                8      0      0      0   100%
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/__main__.py               44     44      6      0     0%
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/__version__.py             8      0      0      0   100%
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/cache.py                  17      9      2      0    42%
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/engines/__init__.py        5      0      0      0   100%
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/engines/base.py           16      4      0      0    75%
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/engines/diskcache.py      27     12      4      0    48%
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/engines/joblib.py         29     11      0      0    62%
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/engines/lru.py            16      4      0      0    75%
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/paths.py                  20     12      2      0    36%
--------------------------------------------------------------------------
-------------------------------------------------------------------------
TOTAL

                                          190     96     14      0    46% 

======================== short test summary info =========================
FAILED tests/test_twat_cache.py::ruff - pytest_ruff.RuffError: tests/test_
twat_cache.py:21:20: F401 [*] `typing.Any` imported but unused
   |
19 | import numpy as np
20 | import pytest
21 | from typing import Any
   |                    ^^^ F401
22 |
23 | from twat_cache.engines.lru import LRUCacheEngine
   |
   = help: Remove unused import: `typing.Any`
FAILED tests/test_twat_cache.py

Results (14.61s):
       2 passed
       1 failed
         - tests/test_twat_cache.py:? 

```

---

_****_





I see we have a linting error. Let me fix that by removing the unused import:

---

_****_

```diff
  import numpy as np
  import pytest
- from typing import Any
  
  from twat_cache.engines.lru import LRUCacheEngine
```

---

_****_



---

_**User**_

you can also run

hatch run lint:fix; hatch test

---

_**Assistant**_

I'll run the suggested command to fix linting issues and run tests:

---

_****_

```bash
hatch run lint:fix; hatch test
```

```
warning: The top-level linter settings are deprecated in favour of their c
ounterparts in the `lint` section. Please update the following options in
`pyproject.toml`:
  - 'per-file-ignores' -> 'lint.per-file-ignores'
src/twat_cache/cache.py:51:5: FBT001 Boolean-typed positional argument in 
function definition
   |
49 |     maxsize: int | None = None,
50 |     folder_name: str | None = None,
51 |     use_sql: bool = False,
   |     ^^^^^^^ FBT001
52 |     preferred_engine: str | None = None,
53 | ) -> Callable[[Callable[P, R]], Callable[P, R]]:
   |

src/twat_cache/cache.py:51:5: FBT002 Boolean default positional argument i
n function definition
   |
49 |     maxsize: int | None = None,
50 |     folder_name: str | None = None,
51 |     use_sql: bool = False,
   |     ^^^^^^^ FBT002
52 |     preferred_engine: str | None = None,
53 | ) -> Callable[[Callable[P, R]], Callable[P, R]]:
   |

src/twat_cache/config.py:158:30: T201 `print` found
    |
156 |         level = "DEBUG" if self.debug else "INFO"
157 |         logger.add(
158 |             sink=lambda msg: print(msg, end=""),
    |                              ^^^^^ T201
159 |             level=level,
160 |             format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    |
    = help: Remove `print`

src/twat_cache/engines/base.py:89:17: B904 Within an `except` clause, rais
e exceptions with `raise ... from err` or `raise ... from None` to disting
uish them from errors in exception handling
   |
87 |             except ValueError as e:
88 |                 msg = f"Invalid cache folder: {e}"
89 |                 raise ValueError(msg)
   |                 ^^^^^^^^^^^^^^^^^^^^^ B904
90 |
91 |     def _make_key(self, func: Callable[P, R], args: tuple, kwargs: di
ct) -> CacheKey:
   |

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

src/twat_cache/engines/manager.py:91:25: F821 Undefined name `EngineManage
r`
   |
89 |     """
90 |
91 |     _instance: ClassVar[EngineManager | None] = None
   |                         ^^^^^^^^^^^^^ F821
92 |
93 |     def __new__(cls) -> EngineManager:
   |

src/twat_cache/engines/manager.py:93:25: F821 Undefined name `EngineManage
r`
   |
91 |     _instance: ClassVar[EngineManager | None] = None
92 |
93 |     def __new__(cls) -> EngineManager:
   |                         ^^^^^^^^^^^^^ F821
94 |         """Create or return the singleton instance."""
95 |         if cls._instance is None:
   |

src/twat_cache/paths.py:99:9: B904 Within an `except` clause, raise except
ions with `raise ... from err` or `raise ... from None` to distinguish the
m from errors in exception handling
   |
97 |     except Exception as e:
98 |         msg = f"Invalid cache path {path}: {e}"
99 |         raise ValueError(msg)
   |         ^^^^^^^^^^^^^^^^^^^^^ B904
   |

src/twat_cache/paths.py:102:5: C901 `clear_cache` is too complex (11 > 10)
    |
102 | def clear_cache(folder_name: str | None = None) -> None:
    |     ^^^^^^^^^^^ C901
103 |     """
104 |     Clear the cache directory for the given folder name.
    |

src/twat_cache/types.py:1:1: A005 Module `types` shadows a Python standard
-library module
src/twat_cache/types.py:174:5: F822 Undefined name `F` in `__all__`
    |
172 |     "CacheStats",
173 |     "CacheValue",
174 |     "F",
    |     ^^^ F822
175 |     "KeyMaker",
176 |     "P",
    |

tests/test_cache.py:54:37: PLR2004 Magic value used in comparison, conside
r replacing `25` with a constant variable
   |
53 |     # First call should compute
54 |     assert expensive_function(5) == 25
   |                                     ^^ PLR2004
55 |     assert call_count == 1
   |

tests/test_cache.py:58:37: PLR2004 Magic value used in comparison, conside
r replacing `25` with a constant variable
   |
57 |     # Second call should use cache
58 |     assert expensive_function(5) == 25
   |                                     ^^ PLR2004
59 |     assert call_count == 1
   |

tests/test_cache.py:62:37: PLR2004 Magic value used in comparison, conside
r replacing `36` with a constant variable
   |
61 |     # Different input should compute
62 |     assert expensive_function(6) == 36
   |                                     ^^ PLR2004
63 |     assert call_count == 2
   |

tests/test_cache.py:63:26: PLR2004 Magic value used in comparison, conside
r replacing `2` with a constant variable
   |
61 |     # Different input should compute
62 |     assert expensive_function(6) == 36
63 |     assert call_count == 2
   |                          ^ PLR2004
   |

tests/test_cache.py:77:34: PLR2004 Magic value used in comparison, conside
r replacing `25` with a constant variable
   |
76 |     # First call
77 |     assert cached_function(5) == 25
   |                                  ^^ PLR2004
78 |     assert call_count == 1
   |

tests/test_cache.py:84:34: PLR2004 Magic value used in comparison, conside
r replacing `25` with a constant variable
   |
83 |     # Should recompute after clear
84 |     assert cached_function(5) == 25
   |                                  ^^ PLR2004
85 |     assert call_count == 2
   |

tests/test_cache.py:85:26: PLR2004 Magic value used in comparison, conside
r replacing `2` with a constant variable
   |
83 |     # Should recompute after clear
84 |     assert cached_function(5) == 25
85 |     assert call_count == 2
   |                          ^ PLR2004
   |

tests/test_cache.py:107:29: PLR2004 Magic value used in comparison, consid
er replacing `2` with a constant variable
    |
105 |     # Basic stats checks
106 |     assert isinstance(stats, dict)
107 |     assert stats["hits"] >= 2
    |                             ^ PLR2004
108 |     assert stats["misses"] >= 2
109 |     assert "size" in stats
    |

tests/test_cache.py:108:31: PLR2004 Magic value used in comparison, consid
er replacing `2` with a constant variable
    |
106 |     assert isinstance(stats, dict)
107 |     assert stats["hits"] >= 2
108 |     assert stats["misses"] >= 2
    |                               ^ PLR2004
109 |     assert "size" in stats
    |

tests/test_cache.py:152:34: PLR2004 Magic value used in comparison, consid
er replacing `15` with a constant variable
    |
150 |     result2 = process_list(test_list)
151 |
152 |     assert result1 == result2 == 15
    |                                  ^^ PLR2004
    |

tests/test_cache.py:188:33: PLR2004 Magic value used in comparison, consid
er replacing `5` with a constant variable
    |
187 |     # Test with different kwarg combinations
188 |     assert kwarg_function(5) == 5
    |                                 ^ PLR2004
189 |     assert call_count == 1
    |

tests/test_cache.py:191:47: PLR2004 Magic value used in comparison, consid
er replacing `5` with a constant variable
    |
189 |     assert call_count == 1
190 |
191 |     assert kwarg_function(5, multiplier=1) == 5
    |                                               ^ PLR2004
192 |     assert call_count == 1  # Should use cache
    |

tests/test_cache.py:194:47: PLR2004 Magic value used in comparison, consid
er replacing `10` with a constant variable
    |
192 |     assert call_count == 1  # Should use cache
193 |
194 |     assert kwarg_function(5, multiplier=2) == 10
    |                                               ^^ PLR2004
195 |     assert call_count == 2  # Different kwargs = new computation
    |

tests/test_cache.py:195:26: PLR2004 Magic value used in comparison, consid
er replacing `2` with a constant variable
    |
194 |     assert kwarg_function(5, multiplier=2) == 10
195 |     assert call_count == 2  # Different kwargs = new computation
    |                          ^ PLR2004
    |

tests/test_config.py:65:38: PLR2004 Magic value used in comparison, consid
er replacing `1000` with a constant variable
   |
64 |     assert config.cache_dir == get_cache_dir()
65 |     assert config.default_maxsize == 1000
   |                                      ^^^^ PLR2004
66 |     assert config.default_use_sql is False
67 |     assert config.default_engine == "lru"
   |

tests/test_config.py:69:40: PLR2004 Magic value used in comparison, consid
er replacing `6` with a constant variable
   |
67 |     assert config.default_engine == "lru"
68 |     assert config.enable_compression is True
69 |     assert config.compression_level == 6
   |                                        ^ PLR2004
70 |     assert config.debug is False
71 |     assert config.log_file is None
   |

tests/test_config.py:86:38: PLR2004 Magic value used in comparison, consid
er replacing `500` with a constant variable
   |
85 |     # Check values
86 |     assert config.default_maxsize == 500
   |                                      ^^^ PLR2004
87 |     assert config.default_use_sql is True
88 |     assert config.default_engine == "disk"
   |

tests/test_config.py:107:36: PLR2004 Magic value used in comparison, consi
der replacing `200` with a constant variable
    |
105 |         folder_name="test_cache",
106 |     )
107 |     assert cache_config.maxsize == 200
    |                                    ^^^ PLR2004
108 |     assert cache_config.folder_name == "test_cache"
109 |     assert cache_config.use_sql == global_config.default_use_sql
    |

tests/test_config.py:119:36: PLR2004 Magic value used in comparison, consi
der replacing `300` with a constant variable
    |
117 |         preferred_engine="disk",
118 |     )
119 |     assert cache_config.maxsize == 300
    |                                    ^^^ PLR2004
120 |     assert cache_config.folder_name == "custom_cache"
121 |     assert cache_config.use_sql is True
    |

tests/test_engines.py:123:28: PLR2004 Magic value used in comparison, cons
ider replacing `10` with a constant variable
    |
122 |     # First call should compute
123 |     assert test_func(5) == 10
    |                            ^^ PLR2004
124 |     assert call_count == 1
125 |     assert test_engine.stats["hits"] == 0
    |

tests/test_engines.py:129:28: PLR2004 Magic value used in comparison, cons
ider replacing `10` with a constant variable
    |
128 |     # Second call should use cache
129 |     assert test_func(5) == 10
    |                            ^^ PLR2004
130 |     assert call_count == 1
131 |     assert test_engine.stats["hits"] == 1
    |

tests/test_engines.py:135:29: PLR2004 Magic value used in comparison, cons
ider replacing `20` with a constant variable
    |
134 |     # Different arg should compute
135 |     assert test_func(10) == 20
    |                             ^^ PLR2004
136 |     assert call_count == 2
137 |     assert test_engine.stats["hits"] == 1
    |

tests/test_engines.py:136:26: PLR2004 Magic value used in comparison, cons
ider replacing `2` with a constant variable
    |
134 |     # Different arg should compute
135 |     assert test_func(10) == 20
136 |     assert call_count == 2
    |                          ^ PLR2004
137 |     assert test_engine.stats["hits"] == 1
138 |     assert test_engine.stats["misses"] == 2
    |

tests/test_engines.py:138:43: PLR2004 Magic value used in comparison, cons
ider replacing `2` with a constant variable
    |
136 |     assert call_count == 2
137 |     assert test_engine.stats["hits"] == 1
138 |     assert test_engine.stats["misses"] == 2
    |                                           ^ PLR2004
    |

tests/test_engines.py:168:38: PLR2004 Magic value used in comparison, cons
ider replacing `10` with a constant variable
    |
166 |         lru_engine._set_cached_value(("key", i), i)
167 |
168 |     assert len(lru_engine._cache) == 10
    |                                      ^^ PLR2004
169 |
170 |     # Add one more, should evict oldest
    |

tests/test_engines.py:172:38: PLR2004 Magic value used in comparison, cons
ider replacing `10` with a constant variable
    |
170 |     # Add one more, should evict oldest
171 |     lru_engine._set_cached_value(("key", 10), 10)
172 |     assert len(lru_engine._cache) == 10
    |                                      ^^ PLR2004
173 |     assert ("key", 0) not in lru_engine._cache  # First item should 
be evicted
174 |     assert ("key", 10) in lru_engine._cache  # New item should be pr
esent
    |

tests/test_engines.py:183:38: PLR2004 Magic value used in comparison, cons
ider replacing `5` with a constant variable
    |
181 |         lru_engine._set_cached_value(("key", i), i)
182 |
183 |     assert len(lru_engine._cache) == 5
    |                                      ^ PLR2004
184 |
185 |     # Clear cache
    |

tests/test_engines.py:226:29: PLR2004 Magic value used in comparison, cons
ider replacing `2` with a constant variable
    |
225 |     stats = lru_engine.stats
226 |     assert stats["hits"] == 2
    |                             ^ PLR2004
227 |     assert stats["misses"] == 2
228 |     assert stats["size"] == 2
    |

tests/test_engines.py:227:31: PLR2004 Magic value used in comparison, cons
ider replacing `2` with a constant variable
    |
225 |     stats = lru_engine.stats
226 |     assert stats["hits"] == 2
227 |     assert stats["misses"] == 2
    |                               ^ PLR2004
228 |     assert stats["size"] == 2
229 |     assert stats["current_size"] == 2
    |

tests/test_engines.py:228:29: PLR2004 Magic value used in comparison, cons
ider replacing `2` with a constant variable
    |
226 |     assert stats["hits"] == 2
227 |     assert stats["misses"] == 2
228 |     assert stats["size"] == 2
    |                             ^ PLR2004
229 |     assert stats["current_size"] == 2
    |

tests/test_engines.py:229:37: PLR2004 Magic value used in comparison, cons
ider replacing `2` with a constant variable
    |
227 |     assert stats["misses"] == 2
228 |     assert stats["size"] == 2
229 |     assert stats["current_size"] == 2
    |                                     ^ PLR2004
    |

tests/test_redis_cache.py:69:32: PLR2004 Magic value used in comparison, c
onsider replacing `6379` with a constant variable
   |
67 |     """Test Redis cache initialization."""
68 |     assert redis_cache.host == "localhost"
69 |     assert redis_cache.port == 6379
   |                                ^^^^ PLR2004
70 |     assert redis_cache.db == 0
71 |     assert redis_cache.ttl == 60
   |

tests/test_redis_cache.py:71:31: PLR2004 Magic value used in comparison, c
onsider replacing `60` with a constant variable
   |
69 |     assert redis_cache.port == 6379
70 |     assert redis_cache.db == 0
71 |     assert redis_cache.ttl == 60
   |                               ^^ PLR2004
   |

tests/test_redis_cache.py:85:28: PLR2004 Magic value used in comparison, c
onsider replacing `25` with a constant variable
   |
84 |     # First call should compute
85 |     assert test_func(5) == 25
   |                            ^^ PLR2004
86 |     assert call_count == 1
   |

tests/test_redis_cache.py:89:28: PLR2004 Magic value used in comparison, c
onsider replacing `25` with a constant variable
   |
88 |     # Second call should use cache
89 |     assert test_func(5) == 25
   |                            ^^ PLR2004
90 |     assert call_count == 1
   |

tests/test_redis_cache.py:93:28: PLR2004 Magic value used in comparison, c
onsider replacing `36` with a constant variable
   |
92 |     # Different input should compute
93 |     assert test_func(6) == 36
   |                            ^^ PLR2004
94 |     assert call_count == 2
   |

tests/test_redis_cache.py:94:26: PLR2004 Magic value used in comparison, c
onsider replacing `2` with a constant variable
   |
92 |     # Different input should compute
93 |     assert test_func(6) == 36
94 |     assert call_count == 2
   |                          ^ PLR2004
   |

tests/test_redis_cache.py:108:28: PLR2004 Magic value used in comparison, 
consider replacing `25` with a constant variable
    |
107 |     # First call
108 |     assert test_func(5) == 25
    |                            ^^ PLR2004
109 |     assert call_count == 1
    |

tests/test_redis_cache.py:112:28: PLR2004 Magic value used in comparison, 
consider replacing `25` with a constant variable
    |
111 |     # Second call (within TTL)
112 |     assert test_func(5) == 25
    |                            ^^ PLR2004
113 |     assert call_count == 1
    |

tests/test_redis_cache.py:119:28: PLR2004 Magic value used in comparison, 
consider replacing `25` with a constant variable
    |
118 |     # Call after TTL expiration
119 |     assert test_func(5) == 25
    |                            ^^ PLR2004
120 |     assert call_count == 2
    |

tests/test_redis_cache.py:120:26: PLR2004 Magic value used in comparison, 
consider replacing `2` with a constant variable
    |
118 |     # Call after TTL expiration
119 |     assert test_func(5) == 25
120 |     assert call_count == 2
    |                          ^ PLR2004
    |

tests/test_redis_cache.py:160:29: PLR2004 Magic value used in comparison, 
consider replacing `2` with a constant variable
    |
158 |     # Check stats
159 |     stats = redis_cache.stats
160 |     assert stats["hits"] >= 2
    |                             ^ PLR2004
161 |     assert stats["misses"] >= 2
162 |     assert stats["size"] == 2
    |

tests/test_redis_cache.py:161:31: PLR2004 Magic value used in comparison, 
consider replacing `2` with a constant variable
    |
159 |     stats = redis_cache.stats
160 |     assert stats["hits"] >= 2
161 |     assert stats["misses"] >= 2
    |                               ^ PLR2004
162 |     assert stats["size"] == 2
    |

tests/test_redis_cache.py:162:29: PLR2004 Magic value used in comparison, 
consider replacing `2` with a constant variable
    |
160 |     assert stats["hits"] >= 2
161 |     assert stats["misses"] >= 2
162 |     assert stats["size"] == 2
    |                             ^ PLR2004
    |

tests/test_redis_cache.py:184:30: PLR2004 Magic value used in comparison, 
consider replacing `15` with a constant variable
    |
183 |     assert result1 == result2
184 |     assert result1["sum"] == 15
    |                              ^^ PLR2004
185 |     assert result1["len"] == 5
    |

tests/test_redis_cache.py:185:30: PLR2004 Magic value used in comparison, 
consider replacing `5` with a constant variable
    |
183 |     assert result1 == result2
184 |     assert result1["sum"] == 15
185 |     assert result1["len"] == 5
    |                              ^ PLR2004
    |

tests/test_redis_cache.py:220:41: PLR2004 Magic value used in comparison, 
consider replacing `2` with a constant variable
    |
218 |     test_func(5)
219 |     test_func(6)
220 |     assert redis_cache.stats["size"] == 2
    |                                         ^ PLR2004
221 |
222 |     # Different kwargs should have different keys
    |

tests/test_redis_cache.py:224:41: PLR2004 Magic value used in comparison, 
consider replacing `3` with a constant variable
    |
222 |     # Different kwargs should have different keys
223 |     test_func(5, multiplier=2)
224 |     assert redis_cache.stats["size"] == 3
    |                                         ^ PLR2004
225 |
226 |     # Same args and kwargs should use same key
    |

tests/test_redis_cache.py:228:41: PLR2004 Magic value used in comparison, 
consider replacing `3` with a constant variable
    |
226 |     # Same args and kwargs should use same key
227 |     test_func(5, multiplier=2)
228 |     assert redis_cache.stats["size"] == 3
    |                                         ^ PLR2004
    |

tests/test_redis_cache.py:242:28: PLR2004 Magic value used in comparison, 
consider replacing `25` with a constant variable
    |
241 |     # First call (normal operation)
242 |     assert test_func(5) == 25
    |                            ^^ PLR2004
243 |     assert call_count == 1
    |

tests/test_redis_cache.py:249:28: PLR2004 Magic value used in comparison, 
consider replacing `25` with a constant variable
    |
248 |     # Call should still work (fallback to computing)
249 |     assert test_func(5) == 25
    |                            ^^ PLR2004
250 |     assert call_count == 2
    |

tests/test_redis_cache.py:250:26: PLR2004 Magic value used in comparison, 
consider replacing `2` with a constant variable
    |
248 |     # Call should still work (fallback to computing)
249 |     assert test_func(5) == 25
250 |     assert call_count == 2
    |                          ^ PLR2004
    |

tests/test_sql_cache.py:61:5: N806 Variable `Session` in function should b
e lowercase
   |
59 |     # Check that tables were created
60 |     db_engine = create_engine(f"sqlite:///{db_path}")
61 |     Session = sessionmaker(bind=db_engine)
   |     ^^^^^^^ N806
62 |     with Session() as session:
63 |         # Should not raise
   |

tests/test_sql_cache.py:78:28: PLR2004 Magic value used in comparison, con
sider replacing `25` with a constant variable
   |
77 |     # First call should compute
78 |     assert test_func(5) == 25
   |                            ^^ PLR2004
79 |     assert call_count == 1
   |

tests/test_sql_cache.py:82:28: PLR2004 Magic value used in comparison, con
sider replacing `25` with a constant variable
   |
81 |     # Second call should use cache
82 |     assert test_func(5) == 25
   |                            ^^ PLR2004
83 |     assert call_count == 1
   |

tests/test_sql_cache.py:86:28: PLR2004 Magic value used in comparison, con
sider replacing `36` with a constant variable
   |
85 |     # Different input should compute
86 |     assert test_func(6) == 36
   |                            ^^ PLR2004
87 |     assert call_count == 2
   |

tests/test_sql_cache.py:87:26: PLR2004 Magic value used in comparison, con
sider replacing `2` with a constant variable
   |
85 |     # Different input should compute
86 |     assert test_func(6) == 36
87 |     assert call_count == 2
   |                          ^ PLR2004
   |

tests/test_sql_cache.py:103:29: PLR2004 Magic value used in comparison, co
nsider replacing `100` with a constant variable
    |
101 |     # Check that cache was pruned
102 |     stats = sql_cache.stats
103 |     assert stats["size"] <= 100
    |                             ^^^ PLR2004
    |

tests/test_sql_cache.py:143:29: PLR2004 Magic value used in comparison, co
nsider replacing `2` with a constant variable
    |
141 |     # Check stats
142 |     stats = sql_cache.stats
143 |     assert stats["hits"] >= 2
    |                             ^ PLR2004
144 |     assert stats["misses"] >= 2
145 |     assert stats["size"] == 2
    |

tests/test_sql_cache.py:144:31: PLR2004 Magic value used in comparison, co
nsider replacing `2` with a constant variable
    |
142 |     stats = sql_cache.stats
143 |     assert stats["hits"] >= 2
144 |     assert stats["misses"] >= 2
    |                               ^ PLR2004
145 |     assert stats["size"] == 2
    |

tests/test_sql_cache.py:145:29: PLR2004 Magic value used in comparison, co
nsider replacing `2` with a constant variable
    |
143 |     assert stats["hits"] >= 2
144 |     assert stats["misses"] >= 2
145 |     assert stats["size"] == 2
    |                             ^ PLR2004
    |

tests/test_sql_cache.py:167:30: PLR2004 Magic value used in comparison, co
nsider replacing `15` with a constant variable
    |
166 |     assert result1 == result2
167 |     assert result1["sum"] == 15
    |                              ^^ PLR2004
168 |     assert result1["len"] == 5
    |

tests/test_sql_cache.py:168:30: PLR2004 Magic value used in comparison, co
nsider replacing `5` with a constant variable
    |
166 |     assert result1 == result2
167 |     assert result1["sum"] == 15
168 |     assert result1["len"] == 5
    |                              ^ PLR2004
    |

tests/test_sql_cache.py:203:39: PLR2004 Magic value used in comparison, co
nsider replacing `2` with a constant variable
    |
201 |     test_func(5)
202 |     test_func(6)
203 |     assert sql_cache.stats["size"] == 2
    |                                       ^ PLR2004
204 |
205 |     # Different kwargs should have different keys
    |

tests/test_sql_cache.py:207:39: PLR2004 Magic value used in comparison, co
nsider replacing `3` with a constant variable
    |
205 |     # Different kwargs should have different keys
206 |     test_func(5, multiplier=2)
207 |     assert sql_cache.stats["size"] == 3
    |                                       ^ PLR2004
208 |
209 |     # Same args and kwargs should use same key
    |

tests/test_sql_cache.py:211:39: PLR2004 Magic value used in comparison, co
nsider replacing `3` with a constant variable
    |
209 |     # Same args and kwargs should use same key
210 |     test_func(5, multiplier=2)
211 |     assert sql_cache.stats["size"] == 3
    |                                       ^ PLR2004
    |

Found 79 errors.
========================== test session starts ===========================
platform darwin -- Python 3.12.8, pytest-8.3.4, pluggy-1.5.0 -- /Users/ada
m/Library/Application Support/hatch/env/virtual/twat-cache/ivvP1xkE/hatch-
test.py3.12/bin/python3
cachedir: .pytest_cache
rootdir: /Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good
/twat/plugins/repos/twat_cache
configfile: pyproject.toml
plugins: rerunfailures-14.0, mock-3.14.0, xdist-3.6.1
collected 0 items / 6 errors                                             

================================= ERRORS =================================
__________________ ERROR collecting tests/test_cache.py __________________
ImportError while importing test module '/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_cache/tests/test_
cache.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/importli
b/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_cache.py:16: in <module>
    from twat_cache.cache import CacheSettings, clear_cache, get_stats, uc
ache
src/twat_cache/__init__.py:5: in <module>
    from twat_cache.cache import ucache
src/twat_cache/cache.py:21: in <module>
    from loguru import logger
E   ModuleNotFoundError: No module named 'loguru'
_________________ ERROR collecting tests/test_config.py __________________
ImportError while importing test module '/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_cache/tests/test_
config.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/importli
b/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_config.py:19: in <module>
    from twat_cache.config import CacheConfig, GlobalConfig
src/twat_cache/__init__.py:5: in <module>
    from twat_cache.cache import ucache
src/twat_cache/cache.py:21: in <module>
    from loguru import logger
E   ModuleNotFoundError: No module named 'loguru'
_________________ ERROR collecting tests/test_engines.py _________________
ImportError while importing test module '/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_cache/tests/test_
engines.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/importli
b/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_engines.py:24: in <module>
    from twat_cache.engines.base import BaseCacheEngine
src/twat_cache/__init__.py:5: in <module>
    from twat_cache.cache import ucache
src/twat_cache/cache.py:21: in <module>
    from loguru import logger
E   ModuleNotFoundError: No module named 'loguru'
_______________ ERROR collecting tests/test_redis_cache.py _______________
ImportError while importing test module '/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_cache/tests/test_
redis_cache.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/importli
b/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_redis_cache.py:21: in <module>
    from fakeredis import FakeRedis, FakeServer
E   ModuleNotFoundError: No module named 'fakeredis'
________________ ERROR collecting tests/test_sql_cache.py ________________
ImportError while importing test module '/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_cache/tests/test_
sql_cache.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/importli
b/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_sql_cache.py:21: in <module>
    from sqlalchemy import create_engine
E   ModuleNotFoundError: No module named 'sqlalchemy'
_______________ ERROR collecting tests/test_twat_cache.py ________________
ImportError while importing test module '/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_cache/tests/test_
twat_cache.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/importli
b/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_twat_cache.py:19: in <module>
    import numpy as np
E   ModuleNotFoundError: No module named 'numpy'
======================== short test summary info =========================
ERROR tests/test_cache.py
ERROR tests/test_config.py
ERROR tests/test_engines.py
ERROR tests/test_redis_cache.py
ERROR tests/test_sql_cache.py
ERROR tests/test_twat_cache.py
!!!!!!!!!!!!!!!! Interrupted: 6 errors during collection !!!!!!!!!!!!!!!!!
=========================== 6 errors in 0.17s ============================

```

---

_****_



I see we're missing some dependencies. Let me install them:

---

_****_

```bash
uv pip install loguru fakeredis sqlalchemy numpy
```

```
Resolved 8 packages in 627ms
Prepared 2 packages in 203ms
Installed 6 packages in 44ms
 + fakeredis==2.27.0
 + greenlet==3.1.1
 + redis==5.2.1
 + sortedcontainers==2.4.0
 + sqlalchemy==2.0.38
 + typing-extensions==4.12.2

```

---

_****_





Now let's try running the tests again:

---

_****_

```bash
hatch run lint:fix; hatch test
```

```
warning: The top-level linter settings are deprecated in favour of their c
ounterparts in the `lint` section. Please update the following options in
`pyproject.toml`:
  - 'per-file-ignores' -> 'lint.per-file-ignores'
src/twat_cache/cache.py:51:5: FBT001 Boolean-typed positional argument in 
function definition
   |
49 |     maxsize: int | None = None,
50 |     folder_name: str | None = None,
51 |     use_sql: bool = False,
   |     ^^^^^^^ FBT001
52 |     preferred_engine: str | None = None,
53 | ) -> Callable[[Callable[P, R]], Callable[P, R]]:
   |

src/twat_cache/cache.py:51:5: FBT002 Boolean default positional argument i
n function definition
   |
49 |     maxsize: int | None = None,
50 |     folder_name: str | None = None,
51 |     use_sql: bool = False,
   |     ^^^^^^^ FBT002
52 |     preferred_engine: str | None = None,
53 | ) -> Callable[[Callable[P, R]], Callable[P, R]]:
   |

src/twat_cache/config.py:158:30: T201 `print` found
    |
156 |         level = "DEBUG" if self.debug else "INFO"
157 |         logger.add(
158 |             sink=lambda msg: print(msg, end=""),
    |                              ^^^^^ T201
159 |             level=level,
160 |             format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    |
    = help: Remove `print`

src/twat_cache/engines/base.py:89:17: B904 Within an `except` clause, rais
e exceptions with `raise ... from err` or `raise ... from None` to disting
uish them from errors in exception handling
   |
87 |             except ValueError as e:
88 |                 msg = f"Invalid cache folder: {e}"
89 |                 raise ValueError(msg)
   |                 ^^^^^^^^^^^^^^^^^^^^^ B904
90 |
91 |     def _make_key(self, func: Callable[P, R], args: tuple, kwargs: di
ct) -> CacheKey:
   |

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

src/twat_cache/engines/manager.py:91:25: F821 Undefined name `EngineManage
r`
   |
89 |     """
90 |
91 |     _instance: ClassVar[EngineManager | None] = None
   |                         ^^^^^^^^^^^^^ F821
92 |
93 |     def __new__(cls) -> EngineManager:
   |

src/twat_cache/engines/manager.py:93:25: F821 Undefined name `EngineManage
r`
   |
91 |     _instance: ClassVar[EngineManager | None] = None
92 |
93 |     def __new__(cls) -> EngineManager:
   |                         ^^^^^^^^^^^^^ F821
94 |         """Create or return the singleton instance."""
95 |         if cls._instance is None:
   |

src/twat_cache/paths.py:99:9: B904 Within an `except` clause, raise except
ions with `raise ... from err` or `raise ... from None` to distinguish the
m from errors in exception handling
   |
97 |     except Exception as e:
98 |         msg = f"Invalid cache path {path}: {e}"
99 |         raise ValueError(msg)
   |         ^^^^^^^^^^^^^^^^^^^^^ B904
   |

src/twat_cache/paths.py:102:5: C901 `clear_cache` is too complex (11 > 10)
    |
102 | def clear_cache(folder_name: str | None = None) -> None:
    |     ^^^^^^^^^^^ C901
103 |     """
104 |     Clear the cache directory for the given folder name.
    |

src/twat_cache/types.py:1:1: A005 Module `types` shadows a Python standard
-library module
src/twat_cache/types.py:174:5: F822 Undefined name `F` in `__all__`
    |
172 |     "CacheStats",
173 |     "CacheValue",
174 |     "F",
    |     ^^^ F822
175 |     "KeyMaker",
176 |     "P",
    |

tests/test_cache.py:54:37: PLR2004 Magic value used in comparison, conside
r replacing `25` with a constant variable
   |
53 |     # First call should compute
54 |     assert expensive_function(5) == 25
   |                                     ^^ PLR2004
55 |     assert call_count == 1
   |

tests/test_cache.py:58:37: PLR2004 Magic value used in comparison, conside
r replacing `25` with a constant variable
   |
57 |     # Second call should use cache
58 |     assert expensive_function(5) == 25
   |                                     ^^ PLR2004
59 |     assert call_count == 1
   |

tests/test_cache.py:62:37: PLR2004 Magic value used in comparison, conside
r replacing `36` with a constant variable
   |
61 |     # Different input should compute
62 |     assert expensive_function(6) == 36
   |                                     ^^ PLR2004
63 |     assert call_count == 2
   |

tests/test_cache.py:63:26: PLR2004 Magic value used in comparison, conside
r replacing `2` with a constant variable
   |
61 |     # Different input should compute
62 |     assert expensive_function(6) == 36
63 |     assert call_count == 2
   |                          ^ PLR2004
   |

tests/test_cache.py:77:34: PLR2004 Magic value used in comparison, conside
r replacing `25` with a constant variable
   |
76 |     # First call
77 |     assert cached_function(5) == 25
   |                                  ^^ PLR2004
78 |     assert call_count == 1
   |

tests/test_cache.py:84:34: PLR2004 Magic value used in comparison, conside
r replacing `25` with a constant variable
   |
83 |     # Should recompute after clear
84 |     assert cached_function(5) == 25
   |                                  ^^ PLR2004
85 |     assert call_count == 2
   |

tests/test_cache.py:85:26: PLR2004 Magic value used in comparison, conside
r replacing `2` with a constant variable
   |
83 |     # Should recompute after clear
84 |     assert cached_function(5) == 25
85 |     assert call_count == 2
   |                          ^ PLR2004
   |

tests/test_cache.py:107:29: PLR2004 Magic value used in comparison, consid
er replacing `2` with a constant variable
    |
105 |     # Basic stats checks
106 |     assert isinstance(stats, dict)
107 |     assert stats["hits"] >= 2
    |                             ^ PLR2004
108 |     assert stats["misses"] >= 2
109 |     assert "size" in stats
    |

tests/test_cache.py:108:31: PLR2004 Magic value used in comparison, consid
er replacing `2` with a constant variable
    |
106 |     assert isinstance(stats, dict)
107 |     assert stats["hits"] >= 2
108 |     assert stats["misses"] >= 2
    |                               ^ PLR2004
109 |     assert "size" in stats
    |

tests/test_cache.py:152:34: PLR2004 Magic value used in comparison, consid
er replacing `15` with a constant variable
    |
150 |     result2 = process_list(test_list)
151 |
152 |     assert result1 == result2 == 15
    |                                  ^^ PLR2004
    |

tests/test_cache.py:188:33: PLR2004 Magic value used in comparison, consid
er replacing `5` with a constant variable
    |
187 |     # Test with different kwarg combinations
188 |     assert kwarg_function(5) == 5
    |                                 ^ PLR2004
189 |     assert call_count == 1
    |

tests/test_cache.py:191:47: PLR2004 Magic value used in comparison, consid
er replacing `5` with a constant variable
    |
189 |     assert call_count == 1
190 |
191 |     assert kwarg_function(5, multiplier=1) == 5
    |                                               ^ PLR2004
192 |     assert call_count == 1  # Should use cache
    |

tests/test_cache.py:194:47: PLR2004 Magic value used in comparison, consid
er replacing `10` with a constant variable
    |
192 |     assert call_count == 1  # Should use cache
193 |
194 |     assert kwarg_function(5, multiplier=2) == 10
    |                                               ^^ PLR2004
195 |     assert call_count == 2  # Different kwargs = new computation
    |

tests/test_cache.py:195:26: PLR2004 Magic value used in comparison, consid
er replacing `2` with a constant variable
    |
194 |     assert kwarg_function(5, multiplier=2) == 10
195 |     assert call_count == 2  # Different kwargs = new computation
    |                          ^ PLR2004
    |

tests/test_config.py:65:38: PLR2004 Magic value used in comparison, consid
er replacing `1000` with a constant variable
   |
64 |     assert config.cache_dir == get_cache_dir()
65 |     assert config.default_maxsize == 1000
   |                                      ^^^^ PLR2004
66 |     assert config.default_use_sql is False
67 |     assert config.default_engine == "lru"
   |

tests/test_config.py:69:40: PLR2004 Magic value used in comparison, consid
er replacing `6` with a constant variable
   |
67 |     assert config.default_engine == "lru"
68 |     assert config.enable_compression is True
69 |     assert config.compression_level == 6
   |                                        ^ PLR2004
70 |     assert config.debug is False
71 |     assert config.log_file is None
   |

tests/test_config.py:86:38: PLR2004 Magic value used in comparison, consid
er replacing `500` with a constant variable
   |
85 |     # Check values
86 |     assert config.default_maxsize == 500
   |                                      ^^^ PLR2004
87 |     assert config.default_use_sql is True
88 |     assert config.default_engine == "disk"
   |

tests/test_config.py:107:36: PLR2004 Magic value used in comparison, consi
der replacing `200` with a constant variable
    |
105 |         folder_name="test_cache",
106 |     )
107 |     assert cache_config.maxsize == 200
    |                                    ^^^ PLR2004
108 |     assert cache_config.folder_name == "test_cache"
109 |     assert cache_config.use_sql == global_config.default_use_sql
    |

tests/test_config.py:119:36: PLR2004 Magic value used in comparison, consi
der replacing `300` with a constant variable
    |
117 |         preferred_engine="disk",
118 |     )
119 |     assert cache_config.maxsize == 300
    |                                    ^^^ PLR2004
120 |     assert cache_config.folder_name == "custom_cache"
121 |     assert cache_config.use_sql is True
    |

tests/test_engines.py:123:28: PLR2004 Magic value used in comparison, cons
ider replacing `10` with a constant variable
    |
122 |     # First call should compute
123 |     assert test_func(5) == 10
    |                            ^^ PLR2004
124 |     assert call_count == 1
125 |     assert test_engine.stats["hits"] == 0
    |

tests/test_engines.py:129:28: PLR2004 Magic value used in comparison, cons
ider replacing `10` with a constant variable
    |
128 |     # Second call should use cache
129 |     assert test_func(5) == 10
    |                            ^^ PLR2004
130 |     assert call_count == 1
131 |     assert test_engine.stats["hits"] == 1
    |

tests/test_engines.py:135:29: PLR2004 Magic value used in comparison, cons
ider replacing `20` with a constant variable
    |
134 |     # Different arg should compute
135 |     assert test_func(10) == 20
    |                             ^^ PLR2004
136 |     assert call_count == 2
137 |     assert test_engine.stats["hits"] == 1
    |

tests/test_engines.py:136:26: PLR2004 Magic value used in comparison, cons
ider replacing `2` with a constant variable
    |
134 |     # Different arg should compute
135 |     assert test_func(10) == 20
136 |     assert call_count == 2
    |                          ^ PLR2004
137 |     assert test_engine.stats["hits"] == 1
138 |     assert test_engine.stats["misses"] == 2
    |

tests/test_engines.py:138:43: PLR2004 Magic value used in comparison, cons
ider replacing `2` with a constant variable
    |
136 |     assert call_count == 2
137 |     assert test_engine.stats["hits"] == 1
138 |     assert test_engine.stats["misses"] == 2
    |                                           ^ PLR2004
    |

tests/test_engines.py:168:38: PLR2004 Magic value used in comparison, cons
ider replacing `10` with a constant variable
    |
166 |         lru_engine._set_cached_value(("key", i), i)
167 |
168 |     assert len(lru_engine._cache) == 10
    |                                      ^^ PLR2004
169 |
170 |     # Add one more, should evict oldest
    |

tests/test_engines.py:172:38: PLR2004 Magic value used in comparison, cons
ider replacing `10` with a constant variable
    |
170 |     # Add one more, should evict oldest
171 |     lru_engine._set_cached_value(("key", 10), 10)
172 |     assert len(lru_engine._cache) == 10
    |                                      ^^ PLR2004
173 |     assert ("key", 0) not in lru_engine._cache  # First item should 
be evicted
174 |     assert ("key", 10) in lru_engine._cache  # New item should be pr
esent
    |

tests/test_engines.py:183:38: PLR2004 Magic value used in comparison, cons
ider replacing `5` with a constant variable
    |
181 |         lru_engine._set_cached_value(("key", i), i)
182 |
183 |     assert len(lru_engine._cache) == 5
    |                                      ^ PLR2004
184 |
185 |     # Clear cache
    |

tests/test_engines.py:226:29: PLR2004 Magic value used in comparison, cons
ider replacing `2` with a constant variable
    |
225 |     stats = lru_engine.stats
226 |     assert stats["hits"] == 2
    |                             ^ PLR2004
227 |     assert stats["misses"] == 2
228 |     assert stats["size"] == 2
    |

tests/test_engines.py:227:31: PLR2004 Magic value used in comparison, cons
ider replacing `2` with a constant variable
    |
225 |     stats = lru_engine.stats
226 |     assert stats["hits"] == 2
227 |     assert stats["misses"] == 2
    |                               ^ PLR2004
228 |     assert stats["size"] == 2
229 |     assert stats["current_size"] == 2
    |

tests/test_engines.py:228:29: PLR2004 Magic value used in comparison, cons
ider replacing `2` with a constant variable
    |
226 |     assert stats["hits"] == 2
227 |     assert stats["misses"] == 2
228 |     assert stats["size"] == 2
    |                             ^ PLR2004
229 |     assert stats["current_size"] == 2
    |

tests/test_engines.py:229:37: PLR2004 Magic value used in comparison, cons
ider replacing `2` with a constant variable
    |
227 |     assert stats["misses"] == 2
228 |     assert stats["size"] == 2
229 |     assert stats["current_size"] == 2
    |                                     ^ PLR2004
    |

tests/test_redis_cache.py:69:32: PLR2004 Magic value used in comparison, c
onsider replacing `6379` with a constant variable
   |
67 |     """Test Redis cache initialization."""
68 |     assert redis_cache.host == "localhost"
69 |     assert redis_cache.port == 6379
   |                                ^^^^ PLR2004
70 |     assert redis_cache.db == 0
71 |     assert redis_cache.ttl == 60
   |

tests/test_redis_cache.py:71:31: PLR2004 Magic value used in comparison, c
onsider replacing `60` with a constant variable
   |
69 |     assert redis_cache.port == 6379
70 |     assert redis_cache.db == 0
71 |     assert redis_cache.ttl == 60
   |                               ^^ PLR2004
   |

tests/test_redis_cache.py:85:28: PLR2004 Magic value used in comparison, c
onsider replacing `25` with a constant variable
   |
84 |     # First call should compute
85 |     assert test_func(5) == 25
   |                            ^^ PLR2004
86 |     assert call_count == 1
   |

tests/test_redis_cache.py:89:28: PLR2004 Magic value used in comparison, c
onsider replacing `25` with a constant variable
   |
88 |     # Second call should use cache
89 |     assert test_func(5) == 25
   |                            ^^ PLR2004
90 |     assert call_count == 1
   |

tests/test_redis_cache.py:93:28: PLR2004 Magic value used in comparison, c
onsider replacing `36` with a constant variable
   |
92 |     # Different input should compute
93 |     assert test_func(6) == 36
   |                            ^^ PLR2004
94 |     assert call_count == 2
   |

tests/test_redis_cache.py:94:26: PLR2004 Magic value used in comparison, c
onsider replacing `2` with a constant variable
   |
92 |     # Different input should compute
93 |     assert test_func(6) == 36
94 |     assert call_count == 2
   |                          ^ PLR2004
   |

tests/test_redis_cache.py:108:28: PLR2004 Magic value used in comparison, 
consider replacing `25` with a constant variable
    |
107 |     # First call
108 |     assert test_func(5) == 25
    |                            ^^ PLR2004
109 |     assert call_count == 1
    |

tests/test_redis_cache.py:112:28: PLR2004 Magic value used in comparison, 
consider replacing `25` with a constant variable
    |
111 |     # Second call (within TTL)
112 |     assert test_func(5) == 25
    |                            ^^ PLR2004
113 |     assert call_count == 1
    |

tests/test_redis_cache.py:119:28: PLR2004 Magic value used in comparison, 
consider replacing `25` with a constant variable
    |
118 |     # Call after TTL expiration
119 |     assert test_func(5) == 25
    |                            ^^ PLR2004
120 |     assert call_count == 2
    |

tests/test_redis_cache.py:120:26: PLR2004 Magic value used in comparison, 
consider replacing `2` with a constant variable
    |
118 |     # Call after TTL expiration
119 |     assert test_func(5) == 25
120 |     assert call_count == 2
    |                          ^ PLR2004
    |

tests/test_redis_cache.py:160:29: PLR2004 Magic value used in comparison, 
consider replacing `2` with a constant variable
    |
158 |     # Check stats
159 |     stats = redis_cache.stats
160 |     assert stats["hits"] >= 2
    |                             ^ PLR2004
161 |     assert stats["misses"] >= 2
162 |     assert stats["size"] == 2
    |

tests/test_redis_cache.py:161:31: PLR2004 Magic value used in comparison, 
consider replacing `2` with a constant variable
    |
159 |     stats = redis_cache.stats
160 |     assert stats["hits"] >= 2
161 |     assert stats["misses"] >= 2
    |                               ^ PLR2004
162 |     assert stats["size"] == 2
    |

tests/test_redis_cache.py:162:29: PLR2004 Magic value used in comparison, 
consider replacing `2` with a constant variable
    |
160 |     assert stats["hits"] >= 2
161 |     assert stats["misses"] >= 2
162 |     assert stats["size"] == 2
    |                             ^ PLR2004
    |

tests/test_redis_cache.py:184:30: PLR2004 Magic value used in comparison, 
consider replacing `15` with a constant variable
    |
183 |     assert result1 == result2
184 |     assert result1["sum"] == 15
    |                              ^^ PLR2004
185 |     assert result1["len"] == 5
    |

tests/test_redis_cache.py:185:30: PLR2004 Magic value used in comparison, 
consider replacing `5` with a constant variable
    |
183 |     assert result1 == result2
184 |     assert result1["sum"] == 15
185 |     assert result1["len"] == 5
    |                              ^ PLR2004
    |

tests/test_redis_cache.py:220:41: PLR2004 Magic value used in comparison, 
consider replacing `2` with a constant variable
    |
218 |     test_func(5)
219 |     test_func(6)
220 |     assert redis_cache.stats["size"] == 2
    |                                         ^ PLR2004
221 |
222 |     # Different kwargs should have different keys
    |

tests/test_redis_cache.py:224:41: PLR2004 Magic value used in comparison, 
consider replacing `3` with a constant variable
    |
222 |     # Different kwargs should have different keys
223 |     test_func(5, multiplier=2)
224 |     assert redis_cache.stats["size"] == 3
    |                                         ^ PLR2004
225 |
226 |     # Same args and kwargs should use same key
    |

tests/test_redis_cache.py:228:41: PLR2004 Magic value used in comparison, 
consider replacing `3` with a constant variable
    |
226 |     # Same args and kwargs should use same key
227 |     test_func(5, multiplier=2)
228 |     assert redis_cache.stats["size"] == 3
    |                                         ^ PLR2004
    |

tests/test_redis_cache.py:242:28: PLR2004 Magic value used in comparison, 
consider replacing `25` with a constant variable
    |
241 |     # First call (normal operation)
242 |     assert test_func(5) == 25
    |                            ^^ PLR2004
243 |     assert call_count == 1
    |

tests/test_redis_cache.py:249:28: PLR2004 Magic value used in comparison, 
consider replacing `25` with a constant variable
    |
248 |     # Call should still work (fallback to computing)
249 |     assert test_func(5) == 25
    |                            ^^ PLR2004
250 |     assert call_count == 2
    |

tests/test_redis_cache.py:250:26: PLR2004 Magic value used in comparison, 
consider replacing `2` with a constant variable
    |
248 |     # Call should still work (fallback to computing)
249 |     assert test_func(5) == 25
250 |     assert call_count == 2
    |                          ^ PLR2004
    |

tests/test_sql_cache.py:61:5: N806 Variable `Session` in function should b
e lowercase
   |
59 |     # Check that tables were created
60 |     db_engine = create_engine(f"sqlite:///{db_path}")
61 |     Session = sessionmaker(bind=db_engine)
   |     ^^^^^^^ N806
62 |     with Session() as session:
63 |         # Should not raise
   |

tests/test_sql_cache.py:78:28: PLR2004 Magic value used in comparison, con
sider replacing `25` with a constant variable
   |
77 |     # First call should compute
78 |     assert test_func(5) == 25
   |                            ^^ PLR2004
79 |     assert call_count == 1
   |

tests/test_sql_cache.py:82:28: PLR2004 Magic value used in comparison, con
sider replacing `25` with a constant variable
   |
81 |     # Second call should use cache
82 |     assert test_func(5) == 25
   |                            ^^ PLR2004
83 |     assert call_count == 1
   |

tests/test_sql_cache.py:86:28: PLR2004 Magic value used in comparison, con
sider replacing `36` with a constant variable
   |
85 |     # Different input should compute
86 |     assert test_func(6) == 36
   |                            ^^ PLR2004
87 |     assert call_count == 2
   |

tests/test_sql_cache.py:87:26: PLR2004 Magic value used in comparison, con
sider replacing `2` with a constant variable
   |
85 |     # Different input should compute
86 |     assert test_func(6) == 36
87 |     assert call_count == 2
   |                          ^ PLR2004
   |

tests/test_sql_cache.py:103:29: PLR2004 Magic value used in comparison, co
nsider replacing `100` with a constant variable
    |
101 |     # Check that cache was pruned
102 |     stats = sql_cache.stats
103 |     assert stats["size"] <= 100
    |                             ^^^ PLR2004
    |

tests/test_sql_cache.py:143:29: PLR2004 Magic value used in comparison, co
nsider replacing `2` with a constant variable
    |
141 |     # Check stats
142 |     stats = sql_cache.stats
143 |     assert stats["hits"] >= 2
    |                             ^ PLR2004
144 |     assert stats["misses"] >= 2
145 |     assert stats["size"] == 2
    |

tests/test_sql_cache.py:144:31: PLR2004 Magic value used in comparison, co
nsider replacing `2` with a constant variable
    |
142 |     stats = sql_cache.stats
143 |     assert stats["hits"] >= 2
144 |     assert stats["misses"] >= 2
    |                               ^ PLR2004
145 |     assert stats["size"] == 2
    |

tests/test_sql_cache.py:145:29: PLR2004 Magic value used in comparison, co
nsider replacing `2` with a constant variable
    |
143 |     assert stats["hits"] >= 2
144 |     assert stats["misses"] >= 2
145 |     assert stats["size"] == 2
    |                             ^ PLR2004
    |

tests/test_sql_cache.py:167:30: PLR2004 Magic value used in comparison, co
nsider replacing `15` with a constant variable
    |
166 |     assert result1 == result2
167 |     assert result1["sum"] == 15
    |                              ^^ PLR2004
168 |     assert result1["len"] == 5
    |

tests/test_sql_cache.py:168:30: PLR2004 Magic value used in comparison, co
nsider replacing `5` with a constant variable
    |
166 |     assert result1 == result2
167 |     assert result1["sum"] == 15
168 |     assert result1["len"] == 5
    |                              ^ PLR2004
    |

tests/test_sql_cache.py:203:39: PLR2004 Magic value used in comparison, co
nsider replacing `2` with a constant variable
    |
201 |     test_func(5)
202 |     test_func(6)
203 |     assert sql_cache.stats["size"] == 2
    |                                       ^ PLR2004
204 |
205 |     # Different kwargs should have different keys
    |

tests/test_sql_cache.py:207:39: PLR2004 Magic value used in comparison, co
nsider replacing `3` with a constant variable
    |
205 |     # Different kwargs should have different keys
206 |     test_func(5, multiplier=2)
207 |     assert sql_cache.stats["size"] == 3
    |                                       ^ PLR2004
208 |
209 |     # Same args and kwargs should use same key
    |

tests/test_sql_cache.py:211:39: PLR2004 Magic value used in comparison, co
nsider replacing `3` with a constant variable
    |
209 |     # Same args and kwargs should use same key
210 |     test_func(5, multiplier=2)
211 |     assert sql_cache.stats["size"] == 3
    |                                       ^ PLR2004
    |

Found 79 errors.
========================== test session starts ===========================
platform darwin -- Python 3.12.8, pytest-8.3.4, pluggy-1.5.0 -- /Users/ada
m/Library/Application Support/hatch/env/virtual/twat-cache/ivvP1xkE/hatch-
test.py3.12/bin/python3
cachedir: .pytest_cache
rootdir: /Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good
/twat/plugins/repos/twat_cache
configfile: pyproject.toml
plugins: rerunfailures-14.0, mock-3.14.0, xdist-3.6.1
collected 0 items / 6 errors                                             

================================= ERRORS =================================
__________________ ERROR collecting tests/test_cache.py __________________
ImportError while importing test module '/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_cache/tests/test_
cache.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/importli
b/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_cache.py:16: in <module>
    from twat_cache.cache import CacheSettings, clear_cache, get_stats, uc
ache
src/twat_cache/__init__.py:5: in <module>
    from twat_cache.cache import ucache
src/twat_cache/cache.py:21: in <module>
    from loguru import logger
E   ModuleNotFoundError: No module named 'loguru'
_________________ ERROR collecting tests/test_config.py __________________
ImportError while importing test module '/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_cache/tests/test_
config.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/importli
b/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_config.py:19: in <module>
    from twat_cache.config import CacheConfig, GlobalConfig
src/twat_cache/__init__.py:5: in <module>
    from twat_cache.cache import ucache
src/twat_cache/cache.py:21: in <module>
    from loguru import logger
E   ModuleNotFoundError: No module named 'loguru'
_________________ ERROR collecting tests/test_engines.py _________________
ImportError while importing test module '/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_cache/tests/test_
engines.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/importli
b/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_engines.py:24: in <module>
    from twat_cache.engines.base import BaseCacheEngine
src/twat_cache/__init__.py:5: in <module>
    from twat_cache.cache import ucache
src/twat_cache/cache.py:21: in <module>
    from loguru import logger
E   ModuleNotFoundError: No module named 'loguru'
_______________ ERROR collecting tests/test_redis_cache.py _______________
ImportError while importing test module '/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_cache/tests/test_
redis_cache.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/importli
b/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_redis_cache.py:21: in <module>
    from fakeredis import FakeRedis, FakeServer
E   ModuleNotFoundError: No module named 'fakeredis'
________________ ERROR collecting tests/test_sql_cache.py ________________
ImportError while importing test module '/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_cache/tests/test_
sql_cache.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/importli
b/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_sql_cache.py:21: in <module>
    from sqlalchemy import create_engine
E   ModuleNotFoundError: No module named 'sqlalchemy'
_______________ ERROR collecting tests/test_twat_cache.py ________________
ImportError while importing test module '/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_cache/tests/test_
twat_cache.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/importli
b/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_twat_cache.py:19: in <module>
    import numpy as np
E   ModuleNotFoundError: No module named 'numpy'
======================== short test summary info =========================
ERROR tests/test_cache.py
ERROR tests/test_config.py
ERROR tests/test_engines.py
ERROR tests/test_redis_cache.py
ERROR tests/test_sql_cache.py
ERROR tests/test_twat_cache.py
!!!!!!!!!!!!!!!! Interrupted: 6 errors during collection !!!!!!!!!!!!!!!!!
=========================== 6 errors in 0.17s ============================

```

---

_****_





Let me install the package in development mode with all its dependencies:

---

_****_

```bash
uv pip install -e ".[all]"
```

```
Audited 1 package in 8ms

```

---

_****_





Now let's try running the tests again:

---

_****_

```bash
python -m pytest tests/test_twat_cache.py -v
```

```
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/pytest_asyncio/plugin.py:207: PytestDeprecationWarning: The configur
ation option "asyncio_default_fixture_loop_scope" is unset.
The event loop scope for asynchronous fixtures will default to the fixture
 caching scope. Future versions of pytest-asyncio will default the loop sc
ope for asynchronous fixtures to function scope. Set the default fixture l
oop scope explicitly in order to avoid unexpected behavior in the future.
Valid fixture loop scopes are: "function", "class", "module", "package", "
session"

  warnings.warn(PytestDeprecationWarning(_DEFAULT_FIXTURE_LOOP_SCOPE_UNSET
))
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/pytest_benchmark/logger.py:39: PytestBenchmarkWarning: Benchmarks ar
e automatically disabled because xdist plugin is active.Benchmarks cannot
be performed reliably in a parallelized environment.
  warner(PytestBenchmarkWarning(text))
Test session starts (platform: darwin, Python 3.12.8, pytest 8.3.4, pytest
-sugar 1.0.0)
cachedir: .pytest_cache
hypothesis profile 'default' -> database=DirectoryBasedExampleDatabase(Pos
ixPath('/Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/
twat/plugins/repos/twat_cache/.hypothesis/examples'))
benchmark: 5.1.0 (defaults: timer=time.perf_counter disable_gc=False min_r
ounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=Fal
se warmup_iterations=100000)
Fugue tests will be initialized with options:
rootdir: /Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good
/twat/plugins/repos/twat_cache
configfile: pyproject.toml
plugins: recording-0.13.2, jaxtyping-0.2.37, cov-6.0.0, flake8-1.3.0, subt
ests-0.14.1, typeguard-4.4.1, instafail-0.5.0, docker-3.1.2, jaraco.mongod
b-12.1.2, enabler-3.3.0, ignore-flaky-2.2.1, integration-0.2.3, sugar-1.0.
0, langchain-0.1.0, env-1.1.5, socket-0.7.0, flaky-3.8.1, time-machine-2.1
6.0, shutil-1.8.1, asyncio-0.25.3, checkdocs-2.13.0, hypothesis-6.124.7, b
lack-0.6.0, anyio-4.8.0, darkgraylib-1.2.1, ruff-0.4.1, benchmark-5.1.0, p
mxbot-1122.17.0, virtualenv-1.8.1, jaraco.vcs-2.4.0, perf-0.15.0, rerunfai
lures-15.0, fugue-0.9.2.dev1, timeout-2.3.1, mock-3.14.0, logfire-3.4.0, d
ash-2.18.2, xdist-3.6.1, depends-1.0.1, requests-mock-1.12.1, syrupy-4.8.1
asyncio: mode=Mode.AUTO, asyncio_default_fixture_loop_scope=None
initialized: 8/8 workers/Library/Frameworks/Python.framework/Versions/3.12
/lib/python3.12/site-packages/pytest_asyncio/plugin.py:207: PytestDeprecat
ionWarning: The configuration option "asyncio_default_fixture_loop_scope"
is unset.
The event loop scope for asynchronous fixtures will default to the fixture
 caching scope. Future versions of pytest-asyncio will default the loop sc
ope for asynchronous fixtures to function scope. Set the default fixture l
oop scope explicitly in order to avoid unexpected behavior in the future.
Valid fixture loop scopes are: "function", "class", "module", "package", "
session"

  warnings.warn(PytestDeprecationWarning(_DEFAULT_FIXTURE_LOOP_SCOPE_UNSET
))
ready: 1/8 workers      /Library/Frameworks/Python.framework/Versions/3.12
/lib/python3.12/site-packages/pytest_asyncio/plugin.py:207: PytestDeprecat
ionWarning: The configuration option "asyncio_default_fixture_loop_scope"
is unset.
The event loop scope for asynchronous fixtures will default to the fixture
 caching scope. Future versions of pytest-asyncio will default the loop sc
ope for asynchronous fixtures to function scope. Set the default fixture l
oop scope explicitly in order to avoid unexpected behavior in the future.
Valid fixture loop scopes are: "function", "class", "module", "package", "
session"

  warnings.warn(PytestDeprecationWarning(_DEFAULT_FIXTURE_LOOP_SCOPE_UNSET
))
ready: 2/8 workers/Library/Frameworks/Python.framework/Versions/3.12/lib/p
ython3.12/site-packages/pytest_asyncio/plugin.py:207: PytestDeprecationWar
ning: The configuration option "asyncio_default_fixture_loop_scope" is uns
et.
The event loop scope for asynchronous fixtures will default to the fixture
 caching scope. Future versions of pytest-asyncio will default the loop sc
ope for asynchronous fixtures to function scope. Set the default fixture l
oop scope explicitly in order to avoid unexpected behavior in the future.
Valid fixture loop scopes are: "function", "class", "module", "package", "
session"

  warnings.warn(PytestDeprecationWarning(_DEFAULT_FIXTURE_LOOP_SCOPE_UNSET
))
ready: 3/8 workers/Library/Frameworks/Python.framework/Versions/3.12/lib/p
ython3.12/site-packages/pytest_asyncio/plugin.py:207: PytestDeprecationWar
ning: The configuration option "asyncio_default_fixture_loop_scope" is uns
et.
The event loop scope for asynchronous fixtures will default to the fixture
 caching scope. Future versions of pytest-asyncio will default the loop sc
ope for asynchronous fixtures to function scope. Set the default fixture l
oop scope explicitly in order to avoid unexpected behavior in the future.
Valid fixture loop scopes are: "function", "class", "module", "package", "
session"

  warnings.warn(PytestDeprecationWarning(_DEFAULT_FIXTURE_LOOP_SCOPE_UNSET
))
ready: 4/8 workers/Library/Frameworks/Python.framework/Versions/3.12/lib/p
ython3.12/site-packages/pytest_asyncio/plugin.py:207: PytestDeprecationWar
ning: The configuration option "asyncio_default_fixture_loop_scope" is uns
et.
The event loop scope for asynchronous fixtures will default to the fixture
 caching scope. Future versions of pytest-asyncio will default the loop sc
ope for asynchronous fixtures to function scope. Set the default fixture l
oop scope explicitly in order to avoid unexpected behavior in the future.
Valid fixture loop scopes are: "function", "class", "module", "package", "
session"

  warnings.warn(PytestDeprecationWarning(_DEFAULT_FIXTURE_LOOP_SCOPE_UNSET
))
ready: 5/8 workers/Library/Frameworks/Python.framework/Versions/3.12/lib/p
ython3.12/site-packages/pytest_asyncio/plugin.py:207: PytestDeprecationWar
ning: The configuration option "asyncio_default_fixture_loop_scope" is uns
et.
The event loop scope for asynchronous fixtures will default to the fixture
 caching scope. Future versions of pytest-asyncio will default the loop sc
ope for asynchronous fixtures to function scope. Set the default fixture l
oop scope explicitly in order to avoid unexpected behavior in the future.
Valid fixture loop scopes are: "function", "class", "module", "package", "
session"

  warnings.warn(PytestDeprecationWarning(_DEFAULT_FIXTURE_LOOP_SCOPE_UNSET
))
ready: 6/8 workers/Library/Frameworks/Python.framework/Versions/3.12/lib/p
ython3.12/site-packages/pytest_asyncio/plugin.py:207: PytestDeprecationWar
ning: The configuration option "asyncio_default_fixture_loop_scope" is uns
et.
The event loop scope for asynchronous fixtures will default to the fixture
 caching scope. Future versions of pytest-asyncio will default the loop sc
ope for asynchronous fixtures to function scope. Set the default fixture l
oop scope explicitly in order to avoid unexpected behavior in the future.
Valid fixture loop scopes are: "function", "class", "module", "package", "
session"

  warnings.warn(PytestDeprecationWarning(_DEFAULT_FIXTURE_LOOP_SCOPE_UNSET
))
ready: 7/8 workers/Library/Frameworks/Python.framework/Versions/3.12/lib/p
ython3.12/site-packages/pytest_asyncio/plugin.py:207: PytestDeprecationWar
ning: The configuration option "asyncio_default_fixture_loop_scope" is uns
et.
The event loop scope for asynchronous fixtures will default to the fixture
 caching scope. Future versions of pytest-asyncio will default the loop sc
ope for asynchronous fixtures to function scope. Set the default fixture l
oop scope explicitly in order to avoid unexpected behavior in the future.
Valid fixture loop scopes are: "function", "class", "module", "package", "
session"

  warnings.warn(PytestDeprecationWarning(_DEFAULT_FIXTURE_LOOP_SCOPE_UNSET
))
collecting 0 items / 1 error                                             
――――――――――――――― ERROR collecting tests/test_twat_cache.py ――――――――――――――――
ImportError while importing test module '/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_cache/tests/test_
twat_cache.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/_pytest/python.py:493: in importtestmodule
    mod = import_path(
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/_pytest/pathlib.py:587: in import_path
    importlib.import_module(module_name)
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/importli
b/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
<frozen importlib._bootstrap>:1387: in _gcd_import
    ???
<frozen importlib._bootstrap>:1360: in _find_and_load
    ???
<frozen importlib._bootstrap>:1331: in _find_and_load_unlocked
    ???
<frozen importlib._bootstrap>:935: in _load_unlocked
    ???
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/_pytest/assertion/rewrite.py:184: in exec_module
    exec(co, module.__dict__)
tests/test_twat_cache.py:22: in <module>
    from twat_cache.engines.lru import LRUCacheEngine
E   ImportError: cannot import name 'LRUCacheEngine' from 'twat_cache.engi
nes.lru' (/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.1
2/site-packages/twat_cache/engines/lru.py)
8 workers [3 items]    
scheduling tests via LoadScheduling
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/coverage/inorout.py:508: CoverageWarning: Module tests was never imp
orted. (module-not-imported)
  self.warn(f"Module {pkg} was never imported.", slug="module-not-imported
")
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/coverage/inorout.py:508: CoverageWarning: Module tests was never imp
orted. (module-not-imported)
  self.warn(f"Module {pkg} was never imported.", slug="module-not-imported
")
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/coverage/inorout.py:508: CoverageWarning: Module tests was never imp
orted. (module-not-imported)
  self.warn(f"Module {pkg} was never imported.", slug="module-not-imported
")
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/coverage/inorout.py:508: CoverageWarning: Module tests was never imp
orted. (module-not-imported)
  self.warn(f"Module {pkg} was never imported.", slug="module-not-imported
")
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/coverage/inorout.py:508: CoverageWarning: Module tests was never imp
orted. (module-not-imported)
  self.warn(f"Module {pkg} was never imported.", slug="module-not-imported
")


 tests/test_twat_cache.py:: ✓✓                              67% ██████▋

/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/coverage/inorout.py:508: CoverageWarning: Module tests was never imp
orted. (module-not-imported)
  self.warn(f"Module {pkg} was never imported.", slug="module-not-imported
")
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/coverage/inorout.py:508: CoverageWarning: Module tests was never imp
orted. (module-not-imported)
  self.warn(f"Module {pkg} was never imported.", slug="module-not-imported
")

 tests/test_twat_cache.py::Black format check ✓            100% ██████████
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/coverage/inorout.py:508: CoverageWarning: Module tests was never imp
orted. (module-not-imported)
  self.warn(f"Module {pkg} was never imported.", slug="module-not-imported
")


---------- coverage: platform darwin, python 3.12.8-final-0 ----------
Name

                                        Stmts   Miss Branch BrPart  Cover
--------------------------------------------------------------------------
-------------------------------------------------------------------------
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/__init__.py                8      0      0      0   100%
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/__main__.py               44     44      6      0     0%
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/__version__.py             8      0      0      0   100%
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/cache.py                  17      9      2      0    42%
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/engines/__init__.py        5      0      0      0   100%
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/engines/base.py           16      4      0      0    75%
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/engines/diskcache.py      27     12      4      0    48%
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/engines/joblib.py         29     11      0      0    62%
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/engines/lru.py            16      4      0      0    75%
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/paths.py                  20     12      2      0    36%
--------------------------------------------------------------------------
-------------------------------------------------------------------------
TOTAL

                                          190     96     14      0    46% 

======================== short test summary info =========================
FAILED tests/test_twat_cache.py

Results (16.25s):
       3 passed

```

---

_****_





I see we have an issue with importing `LRUCacheEngine`. Let me check the `lru.py` file:

---

_****_

Read file: src/twat_cache/engines/lru.py

---

_****_





Let me check if the class is properly exported in the `__init__.py` file:

---

_****_

Read file: src/twat_cache/engines/__init__.py

---

_****_





I see the issue - in `__init__.py` it's importing `LRUEngine` but in `lru.py` the class is named `LRUCacheEngine`. Let me fix this:

---

_****_

```diff
  from twat_cache.engines.joblib import JoblibEngine
  from twat_cache.engines.klepto import KleptoEngine
- from twat_cache.engines.lru import LRUEngine
+ from twat_cache.engines.lru import LRUCacheEngine
  from twat_cache.engines.manager import EngineManager, manager
  
      "JoblibEngine",
      "KleptoEngine",
-     "LRUEngine",
+     "LRUCacheEngine",
      "manager",
  ]
```

---

_****_







Let me check the base.py file to see what's exported:

---

_****_

Read file: src/twat_cache/engines/base.py

---

_****_







I see we need to fix a few things in the imports. Let me update the `__init__.py` file:

---

_****_

```diff
  
  from twat_cache.engines.aiocache import AioCacheEngine
- from twat_cache.engines.base import CacheEngine
+ from twat_cache.engines.base import BaseCacheEngine
  from twat_cache.engines.cachebox import CacheBoxEngine
  from twat_cache.engines.cachetools import CacheToolsEngine
  from twat_cache.engines.klepto import KleptoEngine
  from twat_cache.engines.lru import LRUCacheEngine
- from twat_cache.engines.manager import EngineManager, manager
+ from twat_cache.engines.manager import EngineManager
  
  __all__ = [
      "AioCacheEngine",
+     "BaseCacheEngine",
      "CacheBoxEngine",
-     "CacheEngine",
      "CacheToolsEngine",
      "DiskCacheEngine",
      "KleptoEngine",
      "LRUCacheEngine",
-     "manager",
  ]
  
```

---

_****_







Now let's try running the tests again:

---

_****_

```bash
python -m pytest tests/test_twat_cache.py -v
```

```
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/pytest_asyncio/plugin.py:207: PytestDeprecationWarning: The configur
ation option "asyncio_default_fixture_loop_scope" is unset.
The event loop scope for asynchronous fixtures will default to the fixture
 caching scope. Future versions of pytest-asyncio will default the loop sc
ope for asynchronous fixtures to function scope. Set the default fixture l
oop scope explicitly in order to avoid unexpected behavior in the future.
Valid fixture loop scopes are: "function", "class", "module", "package", "
session"

  warnings.warn(PytestDeprecationWarning(_DEFAULT_FIXTURE_LOOP_SCOPE_UNSET
))
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/pytest_benchmark/logger.py:39: PytestBenchmarkWarning: Benchmarks ar
e automatically disabled because xdist plugin is active.Benchmarks cannot
be performed reliably in a parallelized environment.
  warner(PytestBenchmarkWarning(text))
Test session starts (platform: darwin, Python 3.12.8, pytest 8.3.4, pytest
-sugar 1.0.0)
cachedir: .pytest_cache
hypothesis profile 'default' -> database=DirectoryBasedExampleDatabase(Pos
ixPath('/Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/
twat/plugins/repos/twat_cache/.hypothesis/examples'))
benchmark: 5.1.0 (defaults: timer=time.perf_counter disable_gc=False min_r
ounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=Fal
se warmup_iterations=100000)
Fugue tests will be initialized with options:
rootdir: /Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good
/twat/plugins/repos/twat_cache
configfile: pyproject.toml
plugins: recording-0.13.2, jaxtyping-0.2.37, cov-6.0.0, flake8-1.3.0, subt
ests-0.14.1, typeguard-4.4.1, instafail-0.5.0, docker-3.1.2, jaraco.mongod
b-12.1.2, enabler-3.3.0, ignore-flaky-2.2.1, integration-0.2.3, sugar-1.0.
0, langchain-0.1.0, env-1.1.5, socket-0.7.0, flaky-3.8.1, time-machine-2.1
6.0, shutil-1.8.1, asyncio-0.25.3, checkdocs-2.13.0, hypothesis-6.124.7, b
lack-0.6.0, anyio-4.8.0, darkgraylib-1.2.1, ruff-0.4.1, benchmark-5.1.0, p
mxbot-1122.17.0, virtualenv-1.8.1, jaraco.vcs-2.4.0, perf-0.15.0, rerunfai
lures-15.0, fugue-0.9.2.dev1, timeout-2.3.1, mock-3.14.0, logfire-3.4.0, d
ash-2.18.2, xdist-3.6.1, depends-1.0.1, requests-mock-1.12.1, syrupy-4.8.1
asyncio: mode=Mode.AUTO, asyncio_default_fixture_loop_scope=None
initialized: 8/8 workers/Library/Frameworks/Python.framework/Versions/3.12
/lib/python3.12/site-packages/pytest_asyncio/plugin.py:207: PytestDeprecat
ionWarning: The configuration option "asyncio_default_fixture_loop_scope"
is unset.
The event loop scope for asynchronous fixtures will default to the fixture
 caching scope. Future versions of pytest-asyncio will default the loop sc
ope for asynchronous fixtures to function scope. Set the default fixture l
oop scope explicitly in order to avoid unexpected behavior in the future.
Valid fixture loop scopes are: "function", "class", "module", "package", "
session"

  warnings.warn(PytestDeprecationWarning(_DEFAULT_FIXTURE_LOOP_SCOPE_UNSET
))
ready: 1/8 workers      /Library/Frameworks/Python.framework/Versions/3.12
/lib/python3.12/site-packages/pytest_asyncio/plugin.py:207: PytestDeprecat
ionWarning: The configuration option "asyncio_default_fixture_loop_scope"
is unset.
The event loop scope for asynchronous fixtures will default to the fixture
 caching scope. Future versions of pytest-asyncio will default the loop sc
ope for asynchronous fixtures to function scope. Set the default fixture l
oop scope explicitly in order to avoid unexpected behavior in the future.
Valid fixture loop scopes are: "function", "class", "module", "package", "
session"

  warnings.warn(PytestDeprecationWarning(_DEFAULT_FIXTURE_LOOP_SCOPE_UNSET
))
ready: 2/8 workers/Library/Frameworks/Python.framework/Versions/3.12/lib/p
ython3.12/site-packages/pytest_asyncio/plugin.py:207: PytestDeprecationWar
ning: The configuration option "asyncio_default_fixture_loop_scope" is uns
et.
The event loop scope for asynchronous fixtures will default to the fixture
 caching scope. Future versions of pytest-asyncio will default the loop sc
ope for asynchronous fixtures to function scope. Set the default fixture l
oop scope explicitly in order to avoid unexpected behavior in the future.
Valid fixture loop scopes are: "function", "class", "module", "package", "
session"

  warnings.warn(PytestDeprecationWarning(_DEFAULT_FIXTURE_LOOP_SCOPE_UNSET
))
ready: 3/8 workers/Library/Frameworks/Python.framework/Versions/3.12/lib/p
ython3.12/site-packages/pytest_asyncio/plugin.py:207: PytestDeprecationWar
ning: The configuration option "asyncio_default_fixture_loop_scope" is uns
et.
The event loop scope for asynchronous fixtures will default to the fixture
 caching scope. Future versions of pytest-asyncio will default the loop sc
ope for asynchronous fixtures to function scope. Set the default fixture l
oop scope explicitly in order to avoid unexpected behavior in the future.
Valid fixture loop scopes are: "function", "class", "module", "package", "
session"

  warnings.warn(PytestDeprecationWarning(_DEFAULT_FIXTURE_LOOP_SCOPE_UNSET
))
ready: 4/8 workers/Library/Frameworks/Python.framework/Versions/3.12/lib/p
ython3.12/site-packages/pytest_asyncio/plugin.py:207: PytestDeprecationWar
ning: The configuration option "asyncio_default_fixture_loop_scope" is uns
et.
The event loop scope for asynchronous fixtures will default to the fixture
 caching scope. Future versions of pytest-asyncio will default the loop sc
ope for asynchronous fixtures to function scope. Set the default fixture l
oop scope explicitly in order to avoid unexpected behavior in the future.
Valid fixture loop scopes are: "function", "class", "module", "package", "
session"

  warnings.warn(PytestDeprecationWarning(_DEFAULT_FIXTURE_LOOP_SCOPE_UNSET
))
ready: 5/8 workers/Library/Frameworks/Python.framework/Versions/3.12/lib/p
ython3.12/site-packages/pytest_asyncio/plugin.py:207: PytestDeprecationWar
ning: The configuration option "asyncio_default_fixture_loop_scope" is uns
et.
The event loop scope for asynchronous fixtures will default to the fixture
 caching scope. Future versions of pytest-asyncio will default the loop sc
ope for asynchronous fixtures to function scope. Set the default fixture l
oop scope explicitly in order to avoid unexpected behavior in the future.
Valid fixture loop scopes are: "function", "class", "module", "package", "
session"

  warnings.warn(PytestDeprecationWarning(_DEFAULT_FIXTURE_LOOP_SCOPE_UNSET
))
ready: 6/8 workers/Library/Frameworks/Python.framework/Versions/3.12/lib/p
ython3.12/site-packages/pytest_asyncio/plugin.py:207: PytestDeprecationWar
ning: The configuration option "asyncio_default_fixture_loop_scope" is uns
et.
The event loop scope for asynchronous fixtures will default to the fixture
 caching scope. Future versions of pytest-asyncio will default the loop sc
ope for asynchronous fixtures to function scope. Set the default fixture l
oop scope explicitly in order to avoid unexpected behavior in the future.
Valid fixture loop scopes are: "function", "class", "module", "package", "
session"

  warnings.warn(PytestDeprecationWarning(_DEFAULT_FIXTURE_LOOP_SCOPE_UNSET
))
ready: 7/8 workers/Library/Frameworks/Python.framework/Versions/3.12/lib/p
ython3.12/site-packages/pytest_asyncio/plugin.py:207: PytestDeprecationWar
ning: The configuration option "asyncio_default_fixture_loop_scope" is uns
et.
The event loop scope for asynchronous fixtures will default to the fixture
 caching scope. Future versions of pytest-asyncio will default the loop sc
ope for asynchronous fixtures to function scope. Set the default fixture l
oop scope explicitly in order to avoid unexpected behavior in the future.
Valid fixture loop scopes are: "function", "class", "module", "package", "
session"

  warnings.warn(PytestDeprecationWarning(_DEFAULT_FIXTURE_LOOP_SCOPE_UNSET
))
collecting 0 items / 1 error                                             
――――――――――――――― ERROR collecting tests/test_twat_cache.py ――――――――――――――――
ImportError while importing test module '/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_cache/tests/test_
twat_cache.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/_pytest/python.py:493: in importtestmodule
    mod = import_path(
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/_pytest/pathlib.py:587: in import_path
    importlib.import_module(module_name)
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/importli
b/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
<frozen importlib._bootstrap>:1387: in _gcd_import
    ???
<frozen importlib._bootstrap>:1360: in _find_and_load
    ???
<frozen importlib._bootstrap>:1331: in _find_and_load_unlocked
    ???
<frozen importlib._bootstrap>:935: in _load_unlocked
    ???
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/_pytest/assertion/rewrite.py:184: in exec_module
    exec(co, module.__dict__)
tests/test_twat_cache.py:22: in <module>
    from twat_cache.engines.lru import LRUCacheEngine
E   ImportError: cannot import name 'LRUCacheEngine' from 'twat_cache.engi
nes.lru' (/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.1
2/site-packages/twat_cache/engines/lru.py)
8 workers [3 items]    
scheduling tests via LoadScheduling
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/coverage/inorout.py:508: CoverageWarning: Module tests was never imp
orted. (module-not-imported)
  self.warn(f"Module {pkg} was never imported.", slug="module-not-imported
")
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/coverage/inorout.py:508: CoverageWarning: Module tests was never imp
orted. (module-not-imported)
  self.warn(f"Module {pkg} was never imported.", slug="module-not-imported
")
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/coverage/inorout.py:508: CoverageWarning: Module tests was never imp
orted. (module-not-imported)
  self.warn(f"Module {pkg} was never imported.", slug="module-not-imported
")
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/coverage/inorout.py:508: CoverageWarning: Module tests was never imp
orted. (module-not-imported)
  self.warn(f"Module {pkg} was never imported.", slug="module-not-imported
")
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/coverage/inorout.py:508: CoverageWarning: Module tests was never imp
orted. (module-not-imported)
  self.warn(f"Module {pkg} was never imported.", slug="module-not-imported
")

 tests/test_twat_cache.py:: ✓                               33% ███▍

 tests/test_twat_cache.py:: ✓✓                              67% ██████▋

/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/coverage/inorout.py:508: CoverageWarning: Module tests was never imp
orted. (module-not-imported)
  self.warn(f"Module {pkg} was never imported.", slug="module-not-imported
")
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/coverage/inorout.py:508: CoverageWarning: Module tests was never imp
orted. (module-not-imported)
  self.warn(f"Module {pkg} was never imported.", slug="module-not-imported
")

 tests/test_twat_cache.py::Black format check ✓            100% ██████████
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/coverage/inorout.py:508: CoverageWarning: Module tests was never imp
orted. (module-not-imported)
  self.warn(f"Module {pkg} was never imported.", slug="module-not-imported
")


---------- coverage: platform darwin, python 3.12.8-final-0 ----------
Name

                                        Stmts   Miss Branch BrPart  Cover
--------------------------------------------------------------------------
-------------------------------------------------------------------------
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/__init__.py                8      0      0      0   100%
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/__main__.py               44     44      6      0     0%
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/__version__.py             8      0      0      0   100%
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/cache.py                  17      9      2      0    42%
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/engines/__init__.py        5      0      0      0   100%
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/engines/base.py           16      4      0      0    75%
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/engines/diskcache.py      27     12      4      0    48%
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/engines/joblib.py         29     11      0      0    62%
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/engines/lru.py            16      4      0      0    75%
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/paths.py                  20     12      2      0    36%
--------------------------------------------------------------------------
-------------------------------------------------------------------------
TOTAL

                                          190     96     14      0    46% 

======================== short test summary info =========================
FAILED tests/test_twat_cache.py

Results (16.38s):
       3 passed

```

---

_****_







Let me try reinstalling the package to make sure the changes are picked up:

---

_****_

```bash
uv pip uninstall twat-cache -y && uv pip install -e ".[all]"
```

```
error: unexpected argument '-y' found

  tip: to pass '-y' as a value, use '-- -y'

Usage: uv pip uninstall [OPTIONS] <PACKAGE|--requirements <REQUIREMENTS>>

For more information, try '--help'.

```

---

_****_





Sorry, let me fix that command:

---

_****_

```bash
uv pip uninstall twat-cache && uv pip install -e ".[all]"
```

```
Uninstalled 1 package in 2ms
 - twat-cache==0.1.0 (from file:///Users/adam/Developer/vcs/github.twardoc
h/pub/twat-packages/_good/twat/plugins/repos/twat_cache)
Resolved 10 packages in 312ms
Prepared 1 package in 846ms
Installed 1 package in 2ms
 + twat-cache==0.1.0 (from file:///Users/adam/Developer/vcs/github.twardoc
h/pub/twat-packages/_good/twat/plugins/repos/twat_cache)

```

---

_****_







Now let's try running the tests again:

---

_****_

```bash
python -m pytest tests/test_twat_cache.py -v
```

```
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/pytest_asyncio/plugin.py:207: PytestDeprecationWarning: The configur
ation option "asyncio_default_fixture_loop_scope" is unset.
The event loop scope for asynchronous fixtures will default to the fixture
 caching scope. Future versions of pytest-asyncio will default the loop sc
ope for asynchronous fixtures to function scope. Set the default fixture l
oop scope explicitly in order to avoid unexpected behavior in the future.
Valid fixture loop scopes are: "function", "class", "module", "package", "
session"

  warnings.warn(PytestDeprecationWarning(_DEFAULT_FIXTURE_LOOP_SCOPE_UNSET
))
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/pytest_benchmark/logger.py:39: PytestBenchmarkWarning: Benchmarks ar
e automatically disabled because xdist plugin is active.Benchmarks cannot
be performed reliably in a parallelized environment.
  warner(PytestBenchmarkWarning(text))
Test session starts (platform: darwin, Python 3.12.8, pytest 8.3.4, pytest
-sugar 1.0.0)
cachedir: .pytest_cache
hypothesis profile 'default' -> database=DirectoryBasedExampleDatabase(Pos
ixPath('/Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/
twat/plugins/repos/twat_cache/.hypothesis/examples'))
benchmark: 5.1.0 (defaults: timer=time.perf_counter disable_gc=False min_r
ounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=Fal
se warmup_iterations=100000)
Fugue tests will be initialized with options:
rootdir: /Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good
/twat/plugins/repos/twat_cache
configfile: pyproject.toml
plugins: recording-0.13.2, jaxtyping-0.2.37, cov-6.0.0, flake8-1.3.0, subt
ests-0.14.1, typeguard-4.4.1, instafail-0.5.0, docker-3.1.2, jaraco.mongod
b-12.1.2, enabler-3.3.0, ignore-flaky-2.2.1, integration-0.2.3, sugar-1.0.
0, langchain-0.1.0, env-1.1.5, socket-0.7.0, flaky-3.8.1, time-machine-2.1
6.0, shutil-1.8.1, asyncio-0.25.3, checkdocs-2.13.0, hypothesis-6.124.7, b
lack-0.6.0, anyio-4.8.0, darkgraylib-1.2.1, ruff-0.4.1, benchmark-5.1.0, p
mxbot-1122.17.0, virtualenv-1.8.1, jaraco.vcs-2.4.0, perf-0.15.0, rerunfai
lures-15.0, fugue-0.9.2.dev1, timeout-2.3.1, mock-3.14.0, logfire-3.4.0, d
ash-2.18.2, xdist-3.6.1, depends-1.0.1, requests-mock-1.12.1, syrupy-4.8.1
asyncio: mode=Mode.AUTO, asyncio_default_fixture_loop_scope=None
initialized: 8/8 workers/Library/Frameworks/Python.framework/Versions/3.12
/lib/python3.12/site-packages/pytest_asyncio/plugin.py:207: PytestDeprecat
ionWarning: The configuration option "asyncio_default_fixture_loop_scope"
is unset.
The event loop scope for asynchronous fixtures will default to the fixture
 caching scope. Future versions of pytest-asyncio will default the loop sc
ope for asynchronous fixtures to function scope. Set the default fixture l
oop scope explicitly in order to avoid unexpected behavior in the future.
Valid fixture loop scopes are: "function", "class", "module", "package", "
session"

  warnings.warn(PytestDeprecationWarning(_DEFAULT_FIXTURE_LOOP_SCOPE_UNSET
))
ready: 1/8 workers      /Library/Frameworks/Python.framework/Versions/3.12
/lib/python3.12/site-packages/pytest_asyncio/plugin.py:207: PytestDeprecat
ionWarning: The configuration option "asyncio_default_fixture_loop_scope"
is unset.
The event loop scope for asynchronous fixtures will default to the fixture
 caching scope. Future versions of pytest-asyncio will default the loop sc
ope for asynchronous fixtures to function scope. Set the default fixture l
oop scope explicitly in order to avoid unexpected behavior in the future.
Valid fixture loop scopes are: "function", "class", "module", "package", "
session"

  warnings.warn(PytestDeprecationWarning(_DEFAULT_FIXTURE_LOOP_SCOPE_UNSET
))
ready: 2/8 workers/Library/Frameworks/Python.framework/Versions/3.12/lib/p
ython3.12/site-packages/pytest_asyncio/plugin.py:207: PytestDeprecationWar
ning: The configuration option "asyncio_default_fixture_loop_scope" is uns
et.
The event loop scope for asynchronous fixtures will default to the fixture
 caching scope. Future versions of pytest-asyncio will default the loop sc
ope for asynchronous fixtures to function scope. Set the default fixture l
oop scope explicitly in order to avoid unexpected behavior in the future.
Valid fixture loop scopes are: "function", "class", "module", "package", "
session"

  warnings.warn(PytestDeprecationWarning(_DEFAULT_FIXTURE_LOOP_SCOPE_UNSET
))
ready: 3/8 workers/Library/Frameworks/Python.framework/Versions/3.12/lib/p
ython3.12/site-packages/pytest_asyncio/plugin.py:207: PytestDeprecationWar
ning: The configuration option "asyncio_default_fixture_loop_scope" is uns
et.
The event loop scope for asynchronous fixtures will default to the fixture
 caching scope. Future versions of pytest-asyncio will default the loop sc
ope for asynchronous fixtures to function scope. Set the default fixture l
oop scope explicitly in order to avoid unexpected behavior in the future.
Valid fixture loop scopes are: "function", "class", "module", "package", "
session"

  warnings.warn(PytestDeprecationWarning(_DEFAULT_FIXTURE_LOOP_SCOPE_UNSET
))
ready: 4/8 workers/Library/Frameworks/Python.framework/Versions/3.12/lib/p
ython3.12/site-packages/pytest_asyncio/plugin.py:207: PytestDeprecationWar
ning: The configuration option "asyncio_default_fixture_loop_scope" is uns
et.
The event loop scope for asynchronous fixtures will default to the fixture
 caching scope. Future versions of pytest-asyncio will default the loop sc
ope for asynchronous fixtures to function scope. Set the default fixture l
oop scope explicitly in order to avoid unexpected behavior in the future.
Valid fixture loop scopes are: "function", "class", "module", "package", "
session"

  warnings.warn(PytestDeprecationWarning(_DEFAULT_FIXTURE_LOOP_SCOPE_UNSET
))
ready: 5/8 workers/Library/Frameworks/Python.framework/Versions/3.12/lib/p
ython3.12/site-packages/pytest_asyncio/plugin.py:207: PytestDeprecationWar
ning: The configuration option "asyncio_default_fixture_loop_scope" is uns
et.
The event loop scope for asynchronous fixtures will default to the fixture
 caching scope. Future versions of pytest-asyncio will default the loop sc
ope for asynchronous fixtures to function scope. Set the default fixture l
oop scope explicitly in order to avoid unexpected behavior in the future.
Valid fixture loop scopes are: "function", "class", "module", "package", "
session"

  warnings.warn(PytestDeprecationWarning(_DEFAULT_FIXTURE_LOOP_SCOPE_UNSET
))
ready: 6/8 workers/Library/Frameworks/Python.framework/Versions/3.12/lib/p
ython3.12/site-packages/pytest_asyncio/plugin.py:207: PytestDeprecationWar
ning: The configuration option "asyncio_default_fixture_loop_scope" is uns
et.
The event loop scope for asynchronous fixtures will default to the fixture
 caching scope. Future versions of pytest-asyncio will default the loop sc
ope for asynchronous fixtures to function scope. Set the default fixture l
oop scope explicitly in order to avoid unexpected behavior in the future.
Valid fixture loop scopes are: "function", "class", "module", "package", "
session"

  warnings.warn(PytestDeprecationWarning(_DEFAULT_FIXTURE_LOOP_SCOPE_UNSET
))
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/pytest_asyncio/plugin.py:207: PytestDeprecationWarning: The configur
ation option "asyncio_default_fixture_loop_scope" is unset.
The event loop scope for asynchronous fixtures will default to the fixture
 caching scope. Future versions of pytest-asyncio will default the loop sc
ope for asynchronous fixtures to function scope. Set the default fixture l
oop scope explicitly in order to avoid unexpected behavior in the future.
Valid fixture loop scopes are: "function", "class", "module", "package", "
session"

  warnings.warn(PytestDeprecationWarning(_DEFAULT_FIXTURE_LOOP_SCOPE_UNSET
))
collecting 0 items / 1 error                                             
――――――――――――――― ERROR collecting tests/test_twat_cache.py ――――――――――――――――
ImportError while importing test module '/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_cache/tests/test_
twat_cache.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/_pytest/python.py:493: in importtestmodule
    mod = import_path(
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/_pytest/pathlib.py:587: in import_path
    importlib.import_module(module_name)
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/importli
b/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
<frozen importlib._bootstrap>:1387: in _gcd_import
    ???
<frozen importlib._bootstrap>:1360: in _find_and_load
    ???
<frozen importlib._bootstrap>:1331: in _find_and_load_unlocked
    ???
<frozen importlib._bootstrap>:935: in _load_unlocked
    ???
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/_pytest/assertion/rewrite.py:184: in exec_module
    exec(co, module.__dict__)
tests/test_twat_cache.py:22: in <module>
    from twat_cache.engines.lru import LRUCacheEngine
E   ImportError: cannot import name 'LRUCacheEngine' from 'twat_cache.engi
nes.lru' (/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.1
2/site-packages/twat_cache/engines/lru.py)
8 workers [3 items]    
scheduling tests via LoadScheduling
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/coverage/inorout.py:508: CoverageWarning: Module tests was never imp
orted. (module-not-imported)
  self.warn(f"Module {pkg} was never imported.", slug="module-not-imported
")
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/coverage/inorout.py:508: CoverageWarning: Module tests was never imp
orted. (module-not-imported)
  self.warn(f"Module {pkg} was never imported.", slug="module-not-imported
")
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/coverage/inorout.py:508: CoverageWarning: Module tests was never imp
orted. (module-not-imported)
  self.warn(f"Module {pkg} was never imported.", slug="module-not-imported
")
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/coverage/inorout.py:508: CoverageWarning: Module tests was never imp
orted. (module-not-imported)
  self.warn(f"Module {pkg} was never imported.", slug="module-not-imported
")
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/coverage/inorout.py:508: CoverageWarning: Module tests was never imp
orted. (module-not-imported)
  self.warn(f"Module {pkg} was never imported.", slug="module-not-imported
")

 tests/test_twat_cache.py:: ✓                               33% ███▍

 tests/test_twat_cache.py:: ✓✓                              67% ██████▋

/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/coverage/inorout.py:508: CoverageWarning: Module tests was never imp
orted. (module-not-imported)
  self.warn(f"Module {pkg} was never imported.", slug="module-not-imported
")
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/coverage/inorout.py:508: CoverageWarning: Module tests was never imp
orted. (module-not-imported)
  self.warn(f"Module {pkg} was never imported.", slug="module-not-imported
")

 tests/test_twat_cache.py::Black format check ✓            100% ██████████
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/coverage/inorout.py:508: CoverageWarning: Module tests was never imp
orted. (module-not-imported)
  self.warn(f"Module {pkg} was never imported.", slug="module-not-imported
")


---------- coverage: platform darwin, python 3.12.8-final-0 ----------
Name

                                        Stmts   Miss Branch BrPart  Cover
--------------------------------------------------------------------------
-------------------------------------------------------------------------
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/__init__.py                8      0      0      0   100%
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/__main__.py               44     44      6      0     0%
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/__version__.py             8      0      0      0   100%
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/cache.py                  17      9      2      0    42%
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/engines/__init__.py        5      0      0      0   100%
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/engines/base.py           16      4      0      0    75%
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/engines/diskcache.py      27     12      4      0    48%
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/engines/joblib.py         29     11      0      0    62%
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/engines/lru.py            16      4      0      0    75%
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/paths.py                  20     12      2      0    36%
--------------------------------------------------------------------------
-------------------------------------------------------------------------
TOTAL

                                          190     96     14      0    46% 

======================== short test summary info =========================
FAILED tests/test_twat_cache.py

Results (17.95s):
       3 passed

```

---

_****_



I see we're still having an issue with importing `LRUCacheEngine`. Let me check the contents of the `lru.py` file again to see what might be wrong:

---

_****_

Read file: src/twat_cache/engines/lru.py

---

_****_



Let me also check the `__init__.py` file again to see how we're importing and exporting the class:

---

_****_

Read file: src/twat_cache/engines/__init__.py

---

_****_



I see the issue now. The import and export in `__init__.py` looks correct, but we need to reinstall the package in development mode to make sure the changes are picked up. Let's try that:

---

_****_

```bash
pip uninstall -y twat-cache && pip install -e .
```

```
WARNING: Skipping twat-cache as it is not installed.
Obtaining file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packag
es/_good/twat/plugins/repos/twat_cache
  Installing build dependencies ... done
  Checking if build backend supports build_editable ... done
  Getting requirements to build editable ... done
  Installing backend dependencies ... done
  Preparing editable metadata (pyproject.toml) ... error
  error: subprocess-exited-with-error
  
  × Preparing editable metadata (pyproject.toml) did not run successfully.
  │ exit code: 1
  ╰─> [37 lines of output]
      Traceback (most recent call last):
        File "/usr/local/lib/python3.10/site-packages/pip/_vendor/pyprojec
t_hooks/_in_process/_in_process.py", line 167, in prepare_metadata_for_bui
ld_editable
          hook = backend.prepare_metadata_for_build_editable
      AttributeError: module 'hatchling.build' has no attribute 'prepare_m
etadata_for_build_editable'
      
      During handling of the above exception, another exception occurred:
      
      Traceback (most recent call last):
        File "/usr/local/lib/python3.10/site-packages/pip/_vendor/pyprojec
t_hooks/_in_process/_in_process.py", line 353, in <module>
          main()
        File "/usr/local/lib/python3.10/site-packages/pip/_vendor/pyprojec
t_hooks/_in_process/_in_process.py", line 335, in main
          json_out['return_val'] = hook(**hook_input['kwargs'])
        File "/usr/local/lib/python3.10/site-packages/pip/_vendor/pyprojec
t_hooks/_in_process/_in_process.py", line 176, in prepare_metadata_for_bui
ld_editable
          whl_basename = build_hook(metadata_directory, config_settings)
        File "/usr/local/Cellar/python@3.10/3.10.16/Frameworks/Python.fram
ework/Versions/3.10/lib/python3.10/site-packages/hatchling/build.py", line
 83, in build_editable
          return os.path.basename(next(builder.build(directory=wheel_direc
tory, versions=['editable'])))
        File "/usr/local/Cellar/python@3.10/3.10.16/Frameworks/Python.fram
ework/Versions/3.10/lib/python3.10/site-packages/hatchling/builders/plugin
/interface.py", line 147, in build
          build_hook.initialize(version, build_data)
        File "/usr/local/Cellar/python@3.10/3.10.16/Frameworks/Python.fram
ework/Versions/3.10/lib/python3.10/site-packages/hatch_vcs/build_hook.py",
 line 30, in initialize
          from setuptools_scm import dump_version
        File "/usr/local/Cellar/python@3.10/3.10.16/Frameworks/Python.fram
ework/Versions/3.10/lib/python3.10/site-packages/setuptools_scm/__init__.p
y", line 8, in <module>
          from ._config import DEFAULT_LOCAL_SCHEME
        File "/usr/local/Cellar/python@3.10/3.10.16/Frameworks/Python.fram
ework/Versions/3.10/lib/python3.10/site-packages/setuptools_scm/_config.py
", line 17, in <module>
          from ._integration.pyproject_reading import (
        File "/usr/local/Cellar/python@3.10/3.10.16/Frameworks/Python.fram
ework/Versions/3.10/lib/python3.10/site-packages/setuptools_scm/_integrati
on/pyproject_reading.py", line 9, in <module>
          from .setuptools import read_dist_name_from_setup_cfg
        File "/usr/local/Cellar/python@3.10/3.10.16/Frameworks/Python.fram
ework/Versions/3.10/lib/python3.10/site-packages/setuptools_scm/_integrati
on/setuptools.py", line 10, in <module>
          import setuptools
        File "/usr/local/Cellar/python@3.10/3.10.16/Frameworks/Python.fram
ework/Versions/3.10/lib/python3.10/site-packages/setuptools/__init__.py",
line 22, in <module>
          import _distutils_hack.override  # noqa: F401
        File "/usr/local/Cellar/python@3.10/3.10.16/Frameworks/Python.fram
ework/Versions/3.10/lib/python3.10/site-packages/_distutils_hack/override.
py", line 1, in <module>
          __import__('_distutils_hack').do_override()
        File "/usr/local/Cellar/python@3.10/3.10.16/Frameworks/Python.fram
ework/Versions/3.10/lib/python3.10/site-packages/_distutils_hack/__init__.
py", line 89, in do_override
          ensure_local_distutils()
        File "/usr/local/Cellar/python@3.10/3.10.16/Frameworks/Python.fram
ework/Versions/3.10/lib/python3.10/site-packages/_distutils_hack/__init__.
py", line 76, in ensure_local_distutils
          assert '_distutils' in core.__file__, core.__file__
      AssertionError: /usr/local/Cellar/python@3.10/3.10.16/Frameworks/Pyt
hon.framework/Versions/3.10/lib/python3.10/distutils/core.py
      [end of output]
  
  note: This error originates from a subprocess, and is likely not a probl
em with pip.

[notice] A new release of pip is available: 24.3.1 -> 25.0.1
[notice] To update, run: /usr/local/opt/python@3.10/bin/python3.10 -m pip 
install --upgrade pip
error: metadata-generation-failed

× Encountered error while generating package metadata.
╰─> See above for output.

note: This is an issue with the package mentioned above, not pip.
hint: See above for details.

```

---

_****_



I see we're having some issues with the package installation. Let's try using `uv` as specified in the custom instructions:

---

_****_

```bash
uv pip uninstall -y twat-cache && uv pip install -e .
```

```
error: unexpected argument '-y' found

  tip: to pass '-y' as a value, use '-- -y'

Usage: uv pip uninstall [OPTIONS] <PACKAGE|--requirements <REQUIREMENTS>>

For more information, try '--help'.

```

---

_****_





Let me try the command with the correct syntax:

---

_****_

```bash
uv pip uninstall twat-cache -- -y && uv pip install -e .
```

```
error: Failed to parse: `-y`
  Caused by: Expected package name starting with an alphanumeric character
, found `-`
-y
^

```

---

_****_





Let me try a different approach with `uv`:

---

_****_

```bash
uv pip install -e . --force-reinstall
```

```
Resolved 1 package in 2ms
Prepared 1 package in 1.17s
Uninstalled 1 package in 1ms
Installed 1 package in 2ms
 ~ twat-cache==0.1.0 (from file:///Users/adam/Developer/vcs/github.twardoc
h/pub/twat-packages/_good/twat/plugins/repos/twat_cache)

```

---

_****_





Great! Now let's try running the tests again:

---

_****_

```bash
python -m pytest tests/test_twat_cache.py -v
```

```
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/pytest_asyncio/plugin.py:207: PytestDeprecationWarning: The configur
ation option "asyncio_default_fixture_loop_scope" is unset.
The event loop scope for asynchronous fixtures will default to the fixture
 caching scope. Future versions of pytest-asyncio will default the loop sc
ope for asynchronous fixtures to function scope. Set the default fixture l
oop scope explicitly in order to avoid unexpected behavior in the future.
Valid fixture loop scopes are: "function", "class", "module", "package", "
session"

  warnings.warn(PytestDeprecationWarning(_DEFAULT_FIXTURE_LOOP_SCOPE_UNSET
))
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/pytest_benchmark/logger.py:39: PytestBenchmarkWarning: Benchmarks ar
e automatically disabled because xdist plugin is active.Benchmarks cannot
be performed reliably in a parallelized environment.
  warner(PytestBenchmarkWarning(text))
Test session starts (platform: darwin, Python 3.12.8, pytest 8.3.4, pytest
-sugar 1.0.0)
cachedir: .pytest_cache
hypothesis profile 'default' -> database=DirectoryBasedExampleDatabase(Pos
ixPath('/Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good/
twat/plugins/repos/twat_cache/.hypothesis/examples'))
benchmark: 5.1.0 (defaults: timer=time.perf_counter disable_gc=False min_r
ounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=Fal
se warmup_iterations=100000)
Fugue tests will be initialized with options:
rootdir: /Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/_good
/twat/plugins/repos/twat_cache
configfile: pyproject.toml
plugins: recording-0.13.2, jaxtyping-0.2.37, cov-6.0.0, flake8-1.3.0, subt
ests-0.14.1, typeguard-4.4.1, instafail-0.5.0, docker-3.1.2, jaraco.mongod
b-12.1.2, enabler-3.3.0, ignore-flaky-2.2.1, integration-0.2.3, sugar-1.0.
0, langchain-0.1.0, env-1.1.5, socket-0.7.0, flaky-3.8.1, time-machine-2.1
6.0, shutil-1.8.1, asyncio-0.25.3, checkdocs-2.13.0, hypothesis-6.124.7, b
lack-0.6.0, anyio-4.8.0, darkgraylib-1.2.1, ruff-0.4.1, benchmark-5.1.0, p
mxbot-1122.17.0, virtualenv-1.8.1, jaraco.vcs-2.4.0, perf-0.15.0, rerunfai
lures-15.0, fugue-0.9.2.dev1, timeout-2.3.1, mock-3.14.0, logfire-3.4.0, d
ash-2.18.2, xdist-3.6.1, depends-1.0.1, requests-mock-1.12.1, syrupy-4.8.1
asyncio: mode=Mode.AUTO, asyncio_default_fixture_loop_scope=None
initialized: 8/8 workers/Library/Frameworks/Python.framework/Versions/3.12
/lib/python3.12/site-packages/pytest_asyncio/plugin.py:207: PytestDeprecat
ionWarning: The configuration option "asyncio_default_fixture_loop_scope"
is unset.
The event loop scope for asynchronous fixtures will default to the fixture
 caching scope. Future versions of pytest-asyncio will default the loop sc
ope for asynchronous fixtures to function scope. Set the default fixture l
oop scope explicitly in order to avoid unexpected behavior in the future.
Valid fixture loop scopes are: "function", "class", "module", "package", "
session"

  warnings.warn(PytestDeprecationWarning(_DEFAULT_FIXTURE_LOOP_SCOPE_UNSET
))
ready: 1/8 workers      /Library/Frameworks/Python.framework/Versions/3.12
/lib/python3.12/site-packages/pytest_asyncio/plugin.py:207: PytestDeprecat
ionWarning: The configuration option "asyncio_default_fixture_loop_scope"
is unset.
The event loop scope for asynchronous fixtures will default to the fixture
 caching scope. Future versions of pytest-asyncio will default the loop sc
ope for asynchronous fixtures to function scope. Set the default fixture l
oop scope explicitly in order to avoid unexpected behavior in the future.
Valid fixture loop scopes are: "function", "class", "module", "package", "
session"

  warnings.warn(PytestDeprecationWarning(_DEFAULT_FIXTURE_LOOP_SCOPE_UNSET
))
ready: 2/8 workers/Library/Frameworks/Python.framework/Versions/3.12/lib/p
ython3.12/site-packages/pytest_asyncio/plugin.py:207: PytestDeprecationWar
ning: The configuration option "asyncio_default_fixture_loop_scope" is uns
et.
The event loop scope for asynchronous fixtures will default to the fixture
 caching scope. Future versions of pytest-asyncio will default the loop sc
ope for asynchronous fixtures to function scope. Set the default fixture l
oop scope explicitly in order to avoid unexpected behavior in the future.
Valid fixture loop scopes are: "function", "class", "module", "package", "
session"

  warnings.warn(PytestDeprecationWarning(_DEFAULT_FIXTURE_LOOP_SCOPE_UNSET
))
ready: 3/8 workers/Library/Frameworks/Python.framework/Versions/3.12/lib/p
ython3.12/site-packages/pytest_asyncio/plugin.py:207: PytestDeprecationWar
ning: The configuration option "asyncio_default_fixture_loop_scope" is uns
et.
The event loop scope for asynchronous fixtures will default to the fixture
 caching scope. Future versions of pytest-asyncio will default the loop sc
ope for asynchronous fixtures to function scope. Set the default fixture l
oop scope explicitly in order to avoid unexpected behavior in the future.
Valid fixture loop scopes are: "function", "class", "module", "package", "
session"

  warnings.warn(PytestDeprecationWarning(_DEFAULT_FIXTURE_LOOP_SCOPE_UNSET
))
ready: 4/8 workers/Library/Frameworks/Python.framework/Versions/3.12/lib/p
ython3.12/site-packages/pytest_asyncio/plugin.py:207: PytestDeprecationWar
ning: The configuration option "asyncio_default_fixture_loop_scope" is uns
et.
The event loop scope for asynchronous fixtures will default to the fixture
 caching scope. Future versions of pytest-asyncio will default the loop sc
ope for asynchronous fixtures to function scope. Set the default fixture l
oop scope explicitly in order to avoid unexpected behavior in the future.
Valid fixture loop scopes are: "function", "class", "module", "package", "
session"

  warnings.warn(PytestDeprecationWarning(_DEFAULT_FIXTURE_LOOP_SCOPE_UNSET
))
ready: 5/8 workers/Library/Frameworks/Python.framework/Versions/3.12/lib/p
ython3.12/site-packages/pytest_asyncio/plugin.py:207: PytestDeprecationWar
ning: The configuration option "asyncio_default_fixture_loop_scope" is uns
et.
The event loop scope for asynchronous fixtures will default to the fixture
 caching scope. Future versions of pytest-asyncio will default the loop sc
ope for asynchronous fixtures to function scope. Set the default fixture l
oop scope explicitly in order to avoid unexpected behavior in the future.
Valid fixture loop scopes are: "function", "class", "module", "package", "
session"

  warnings.warn(PytestDeprecationWarning(_DEFAULT_FIXTURE_LOOP_SCOPE_UNSET
))
ready: 6/8 workers/Library/Frameworks/Python.framework/Versions/3.12/lib/p
ython3.12/site-packages/pytest_asyncio/plugin.py:207: PytestDeprecationWar
ning: The configuration option "asyncio_default_fixture_loop_scope" is uns
et.
The event loop scope for asynchronous fixtures will default to the fixture
 caching scope. Future versions of pytest-asyncio will default the loop sc
ope for asynchronous fixtures to function scope. Set the default fixture l
oop scope explicitly in order to avoid unexpected behavior in the future.
Valid fixture loop scopes are: "function", "class", "module", "package", "
session"

  warnings.warn(PytestDeprecationWarning(_DEFAULT_FIXTURE_LOOP_SCOPE_UNSET
))
ready: 7/8 workers/Library/Frameworks/Python.framework/Versions/3.12/lib/p
ython3.12/site-packages/pytest_asyncio/plugin.py:207: PytestDeprecationWar
ning: The configuration option "asyncio_default_fixture_loop_scope" is uns
et.
The event loop scope for asynchronous fixtures will default to the fixture
 caching scope. Future versions of pytest-asyncio will default the loop sc
ope for asynchronous fixtures to function scope. Set the default fixture l
oop scope explicitly in order to avoid unexpected behavior in the future.
Valid fixture loop scopes are: "function", "class", "module", "package", "
session"

  warnings.warn(PytestDeprecationWarning(_DEFAULT_FIXTURE_LOOP_SCOPE_UNSET
))
collecting 0 items / 1 error                                             
――――――――――――――― ERROR collecting tests/test_twat_cache.py ――――――――――――――――
ImportError while importing test module '/Users/adam/Developer/vcs/github.
twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_cache/tests/test_
twat_cache.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/_pytest/python.py:493: in importtestmodule
    mod = import_path(
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/_pytest/pathlib.py:587: in import_path
    importlib.import_module(module_name)
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/importli
b/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
<frozen importlib._bootstrap>:1387: in _gcd_import
    ???
<frozen importlib._bootstrap>:1360: in _find_and_load
    ???
<frozen importlib._bootstrap>:1331: in _find_and_load_unlocked
    ???
<frozen importlib._bootstrap>:935: in _load_unlocked
    ???
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/_pytest/assertion/rewrite.py:184: in exec_module
    exec(co, module.__dict__)
tests/test_twat_cache.py:22: in <module>
    from twat_cache.engines.lru import LRUCacheEngine
E   ImportError: cannot import name 'LRUCacheEngine' from 'twat_cache.engi
nes.lru' (/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.1
2/site-packages/twat_cache/engines/lru.py)
8 workers [3 items]    
scheduling tests via LoadScheduling
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/coverage/inorout.py:508: CoverageWarning: Module tests was never imp
orted. (module-not-imported)
  self.warn(f"Module {pkg} was never imported.", slug="module-not-imported
")
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/coverage/inorout.py:508: CoverageWarning: Module tests was never imp
orted. (module-not-imported)
  self.warn(f"Module {pkg} was never imported.", slug="module-not-imported
")
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/coverage/inorout.py:508: CoverageWarning: Module tests was never imp
orted. (module-not-imported)
  self.warn(f"Module {pkg} was never imported.", slug="module-not-imported
")
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/coverage/inorout.py:508: CoverageWarning: Module tests was never imp
orted. (module-not-imported)
  self.warn(f"Module {pkg} was never imported.", slug="module-not-imported
")
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/coverage/inorout.py:508: CoverageWarning: Module tests was never imp
orted. (module-not-imported)
  self.warn(f"Module {pkg} was never imported.", slug="module-not-imported
")

 tests/test_twat_cache.py:: ✓                               33% ███▍

 tests/test_twat_cache.py:: ✓✓                              67% ██████▋

/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/coverage/inorout.py:508: CoverageWarning: Module tests was never imp
orted. (module-not-imported)
  self.warn(f"Module {pkg} was never imported.", slug="module-not-imported
")
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/coverage/inorout.py:508: CoverageWarning: Module tests was never imp
orted. (module-not-imported)
  self.warn(f"Module {pkg} was never imported.", slug="module-not-imported
")

 tests/test_twat_cache.py::Black format check ✓            100% ██████████
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/coverage/inorout.py:508: CoverageWarning: Module tests was never imp
orted. (module-not-imported)
  self.warn(f"Module {pkg} was never imported.", slug="module-not-imported
")


---------- coverage: platform darwin, python 3.12.8-final-0 ----------
Name

                                        Stmts   Miss Branch BrPart  Cover
--------------------------------------------------------------------------
-------------------------------------------------------------------------
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/__init__.py                8      0      0      0   100%
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/__main__.py               44     44      6      0     0%
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/__version__.py             8      0      0      0   100%
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/cache.py                  17      9      2      0    42%
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/engines/__init__.py        5      0      0      0   100%
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/engines/base.py           16      4      0      0    75%
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/engines/diskcache.py      27     12      4      0    48%
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/engines/joblib.py         29     11      0      0    62%
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/engines/lru.py            16      4      0      0    75%
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-pac
kages/twat_cache/paths.py                  20     12      2      0    36%
--------------------------------------------------------------------------
-------------------------------------------------------------------------
TOTAL

                                          190     96     14      0    46% 

======================== short test summary info =========================
FAILED tests/test_twat_cache.py

Results (15.14s):
       3 passed

```

---

_****_





We're still having the same issue with importing `LRUCacheEngine`. Let me check the test file to see how it's importing the class:

---

_****_

Read file: tests/test_twat_cache.py

---

_****_







Let me check if the package is installed correctly:

---

_****_

```bash
pip show twat-cache
```

```
WARNING: Package(s) not found: twat-cache
adam@Hamlet twat_cache %
```

---

_****_







Let me try installing with `pip` directly:

---

_****_

```bash
pip install -e .
```

```
Obtaining file:///Users/adam/Developer/vcs/github.twardoch/pub/twat-packag
es/_good/twat/plugins/repos/twat_cache
  Installing build dependencies ... done
  Checking if build backend supports build_editable ... done
  Getting requirements to build editable ... done
  Installing backend dependencies ... done
  Preparing editable metadata (pyproject.toml) ... error
  error: subprocess-exited-with-error
  
  × Preparing editable metadata (pyproject.toml) did not run successfully.
  │ exit code: 1
  ╰─> [37 lines of output]
      Traceback (most recent call last):
        File "/usr/local/lib/python3.10/site-packages/pip/_vendor/pyprojec
t_hooks/_in_process/_in_process.py", line 167, in prepare_metadata_for_bui
ld_editable
          hook = backend.prepare_metadata_for_build_editable
      AttributeError: module 'hatchling.build' has no attribute 'prepare_m
etadata_for_build_editable'
      
      During handling of the above exception, another exception occurred:
      
      Traceback (most recent call last):
        File "/usr/local/lib/python3.10/site-packages/pip/_vendor/pyprojec
t_hooks/_in_process/_in_process.py", line 353, in <module>
          main()
        File "/usr/local/lib/python3.10/site-packages/pip/_vendor/pyprojec
t_hooks/_in_process/_in_process.py", line 335, in main
          json_out['return_val'] = hook(**hook_input['kwargs'])
        File "/usr/local/lib/python3.10/site-packages/pip/_vendor/pyprojec
t_hooks/_in_process/_in_process.py", line 176, in prepare_metadata_for_bui
ld_editable
          whl_basename = build_hook(metadata_directory, config_settings)
        File "/usr/local/Cellar/python@3.10/3.10.16/Frameworks/Python.fram
ework/Versions/3.10/lib/python3.10/site-packages/hatchling/build.py", line
 83, in build_editable
          return os.path.basename(next(builder.build(directory=wheel_direc
tory, versions=['editable'])))
        File "/usr/local/Cellar/python@3.10/3.10.16/Frameworks/Python.fram
ework/Versions/3.10/lib/python3.10/site-packages/hatchling/builders/plugin
/interface.py", line 147, in build
          build_hook.initialize(version, build_data)
        File "/usr/local/Cellar/python@3.10/3.10.16/Frameworks/Python.fram
ework/Versions/3.10/lib/python3.10/site-packages/hatch_vcs/build_hook.py",
 line 30, in initialize
          from setuptools_scm import dump_version
        File "/usr/local/Cellar/python@3.10/3.10.16/Frameworks/Python.fram
ework/Versions/3.10/lib/python3.10/site-packages/setuptools_scm/__init__.p
y", line 8, in <module>
          from ._config import DEFAULT_LOCAL_SCHEME
        File "/usr/local/Cellar/python@3.10/3.10.16/Frameworks/Python.fram
ework/Versions/3.10/lib/python3.10/site-packages/setuptools_scm/_config.py
", line 17, in <module>
          from ._integration.pyproject_reading import (
        File "/usr/local/Cellar/python@3.10/3.10.16/Frameworks/Python.fram
ework/Versions/3.10/lib/python3.10/site-packages/setuptools_scm/_integrati
on/pyproject_reading.py", line 9, in <module>
          from .setuptools import read_dist_name_from_setup_cfg
        File "/usr/local/Cellar/python@3.10/3.10.16/Frameworks/Python.fram
ework/Versions/3.10/lib/python3.10/site-packages/setuptools_scm/_integrati
on/setuptools.py", line 10, in <module>
          import setuptools
        File "/usr/local/Cellar/python@3.10/3.10.16/Frameworks/Python.fram
ework/Versions/3.10/lib/python3.10/site-packages/setuptools/__init__.py",
line 22, in <module>
          import _distutils_hack.override  # noqa: F401
        File "/usr/local/Cellar/python@3.10/3.10.16/Frameworks/Python.fram
ework/Versions/3.10/lib/python3.10/site-packages/_distutils_hack/override.
py", line 1, in <module>
          __import__('_distutils_hack').do_override()
        File "/usr/local/Cellar/python@3.10/3.10.16/Frameworks/Python.fram
ework/Versions/3.10/lib/python3.10/site-packages/_distutils_hack/__init__.
py", line 89, in do_override
          ensure_local_distutils()
        File "/usr/local/Cellar/python@3.10/3.10.16/Frameworks/Python.fram
ework/Versions/3.10/lib/python3.10/site-packages/_distutils_hack/__init__.
py", line 76, in ensure_local_distutils
          assert '_distutils' in core.__file__, core.__file__
      AssertionError: /usr/local/Cellar/python@3.10/3.10.16/Frameworks/Pyt
hon.framework/Versions/3.10/lib/python3.10/distutils/core.py
      [end of output]
  
  note: This error originates from a subprocess, and is likely not a probl
em with pip.

[notice] A new release of pip is available: 24.3.1 -> 25.0.1
[notice] To update, run: /usr/local/opt/python@3.10/bin/python3.10 -m pip 
install --upgrade pip
error: metadata-generation-failed

× Encountered error while generating package metadata.
╰─> See above for output.

note: This is an issue with the package mentioned above, not pip.
hint: See above for details.

```

---

_****_







Let me check the `pyproject.toml` file to see if there might be an issue with the build configuration:

---

_****_

Read file: pyproject.toml

---

_****_







I see that we're using Hatchling as the build backend. Let me try installing with `hatch` directly:

---

_****_

```bash
python -m pip install hatch && hatch build && pip install dist/*.whl
```

```
Requirement already satisfied: hatch in /Library/Frameworks/Python.framewo
rk/Versions/3.12/lib/python3.12/site-packages (1.14.0)
Requirement already satisfied: click>=8.0.6 in /Library/Frameworks/Python.
framework/Versions/3.12/lib/python3.12/site-packages (from hatch) (8.1.8)
Requirement already satisfied: hatchling>=1.26.3 in /Library/Frameworks/Py
thon.framework/Versions/3.12/lib/python3.12/site-packages (from hatch) (1.
27.0)
Requirement already satisfied: httpx>=0.22.0 in /Library/Frameworks/Python
.framework/Versions/3.12/lib/python3.12/site-packages (from hatch) (0.28.1
)
Requirement already satisfied: hyperlink>=21.0.0 in /Library/Frameworks/Py
thon.framework/Versions/3.12/lib/python3.12/site-packages (from hatch) (21
.0.0)
Requirement already satisfied: keyring>=23.5.0 in /Library/Frameworks/Pyth
on.framework/Versions/3.12/lib/python3.12/site-packages (from hatch) (25.6
.0)
Requirement already satisfied: packaging>=23.2 in /Library/Frameworks/Pyth
on.framework/Versions/3.12/lib/python3.12/site-packages (from hatch) (24.2
)
Requirement already satisfied: pexpect~=4.8 in /Library/Frameworks/Python.
framework/Versions/3.12/lib/python3.12/site-packages (from hatch) (4.9.0)
Requirement already satisfied: platformdirs>=2.5.0 in /Library/Frameworks/
Python.framework/Versions/3.12/lib/python3.12/site-packages (from hatch) (
4.3.6)
Requirement already satisfied: rich>=11.2.0 in /Library/Frameworks/Python.
framework/Versions/3.12/lib/python3.12/site-packages (from hatch) (13.9.4)
Requirement already satisfied: shellingham>=1.4.0 in /Library/Frameworks/P
ython.framework/Versions/3.12/lib/python3.12/site-packages (from hatch) (1
.5.4)
Requirement already satisfied: tomli-w>=1.0 in /Library/Frameworks/Python.
framework/Versions/3.12/lib/python3.12/site-packages (from hatch) (1.2.0)
Requirement already satisfied: tomlkit>=0.11.1 in /Library/Frameworks/Pyth
on.framework/Versions/3.12/lib/python3.12/site-packages (from hatch) (0.13
.2)
Requirement already satisfied: userpath~=1.7 in /Library/Frameworks/Python
.framework/Versions/3.12/lib/python3.12/site-packages (from hatch) (1.9.2)
Requirement already satisfied: uv>=0.1.35 in /Library/Frameworks/Python.fr
amework/Versions/3.12/lib/python3.12/site-packages (from hatch) (0.6.0)
Requirement already satisfied: virtualenv>=20.26.6 in /Library/Frameworks/
Python.framework/Versions/3.12/lib/python3.12/site-packages (from hatch) (
20.29.2)
Requirement already satisfied: zstandard<1 in /Library/Frameworks/Python.f
ramework/Versions/3.12/lib/python3.12/site-packages (from hatch) (0.23.0)
Requirement already satisfied: pathspec>=0.10.1 in /Library/Frameworks/Pyt
hon.framework/Versions/3.12/lib/python3.12/site-packages (from hatchling>=
1.26.3->hatch) (0.12.1)
Requirement already satisfied: pluggy>=1.0.0 in /Library/Frameworks/Python
.framework/Versions/3.12/lib/python3.12/site-packages (from hatchling>=1.2
6.3->hatch) (1.5.0)
Requirement already satisfied: trove-classifiers in /Library/Frameworks/Py
thon.framework/Versions/3.12/lib/python3.12/site-packages (from hatchling>
=1.26.3->hatch) (2025.1.15.22)
Requirement already satisfied: anyio in /Library/Frameworks/Python.framewo
rk/Versions/3.12/lib/python3.12/site-packages (from httpx>=0.22.0->hatch)
(4.8.0)
Requirement already satisfied: certifi in /Library/Frameworks/Python.frame
work/Versions/3.12/lib/python3.12/site-packages (from httpx>=0.22.0->hatch
) (2025.1.31)
Requirement already satisfied: httpcore==1.* in /Library/Frameworks/Python
.framework/Versions/3.12/lib/python3.12/site-packages (from httpx>=0.22.0-
>hatch) (1.0.7)
Requirement already satisfied: idna in /Library/Frameworks/Python.framewor
k/Versions/3.12/lib/python3.12/site-packages (from httpx>=0.22.0->hatch) (
3.10)
Requirement already satisfied: h11<0.15,>=0.13 in /Library/Frameworks/Pyth
on.framework/Versions/3.12/lib/python3.12/site-packages (from httpcore==1.
*->httpx>=0.22.0->hatch) (0.14.0)
Requirement already satisfied: jaraco.classes in /Library/Frameworks/Pytho
n.framework/Versions/3.12/lib/python3.12/site-packages (from keyring>=23.5
.0->hatch) (3.4.0)
Requirement already satisfied: jaraco.functools in /Library/Frameworks/Pyt
hon.framework/Versions/3.12/lib/python3.12/site-packages (from keyring>=23
.5.0->hatch) (4.1.0)
Requirement already satisfied: jaraco.context in /Library/Frameworks/Pytho
n.framework/Versions/3.12/lib/python3.12/site-packages (from keyring>=23.5
.0->hatch) (6.0.1)
Requirement already satisfied: ptyprocess>=0.5 in /Library/Frameworks/Pyth
on.framework/Versions/3.12/lib/python3.12/site-packages (from pexpect~=4.8
->hatch) (0.7.0)
Requirement already satisfied: markdown-it-py>=2.2.0 in /Library/Framework
s/Python.framework/Versions/3.12/lib/python3.12/site-packages (from rich>=
11.2.0->hatch) (3.0.0)
Requirement already satisfied: pygments<3.0.0,>=2.13.0 in /Library/Framewo
rks/Python.framework/Versions/3.12/lib/python3.12/site-packages (from rich
>=11.2.0->hatch) (2.19.1)
Requirement already satisfied: distlib<1,>=0.3.7 in /Library/Frameworks/Py
thon.framework/Versions/3.12/lib/python3.12/site-packages (from virtualenv
>=20.26.6->hatch) (0.3.9)
Requirement already satisfied: filelock<4,>=3.12.2 in /Library/Frameworks/
Python.framework/Versions/3.12/lib/python3.12/site-packages (from virtuale
nv>=20.26.6->hatch) (3.17.0)
Requirement already satisfied: mdurl~=0.1 in /Library/Frameworks/Python.fr
amework/Versions/3.12/lib/python3.12/site-packages (from markdown-it-py>=2
.2.0->rich>=11.2.0->hatch) (0.1.2)
Requirement already satisfied: sniffio>=1.1 in /Library/Frameworks/Python.
framework/Versions/3.12/lib/python3.12/site-packages (from anyio->httpx>=0
.22.0->hatch) (1.3.1)
Requirement already satisfied: typing_extensions>=4.5 in /Library/Framewor
ks/Python.framework/Versions/3.12/lib/python3.12/site-packages (from anyio
->httpx>=0.22.0->hatch) (4.12.2)
Requirement already satisfied: more-itertools in /Library/Frameworks/Pytho
n.framework/Versions/3.12/lib/python3.12/site-packages (from jaraco.classe
s->keyring>=23.5.0->hatch) (10.6.0)
───────────────────────────────── sdist ──────────────────────────────────
... Setting up build environment
dist/twat_cache-0.1.0.tar.gz
───────────────────────────────── wheel ──────────────────────────────────
dist/twat_cache-0.1.0-py3-none-any.whl
Processing ./dist/twat_cache-0.1.0-py3-none-any.whl
Processing ./dist/twat_cache-1.8.1-py3-none-any.whl
ERROR: Cannot install twat-cache 0.1.0 (from /Users/adam/Developer/vcs/git
hub.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_cache/dist/tw
at_cache-0.1.0-py3-none-any.whl) and twat-cache 1.8.1 (from /Users/adam/De
veloper/vcs/github.twardoch/pub/twat-packages/_good/twat/plugins/repos/twa
t_cache/dist/twat_cache-1.8.1-py3-none-any.whl) because these package vers
ions have conflicting dependencies.

The conflict is caused by:
    The user requested twat-cache 0.1.0 (from /Users/adam/Developer/vcs/gi
thub.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_cache/dist/t
wat_cache-0.1.0-py3-none-any.whl)
    The user requested twat-cache 1.8.1 (from /Users/adam/Developer/vcs/gi
thub.twardoch/pub/twat-packages/_good/twat/plugins/repos/twat_cache/dist/t
wat_cache-1.8.1-py3-none-any.whl)

To fix this you could try to:
1. loosen the range of package versions you've specified
2. remove package versions to allow pip to attempt to solve the dependency
 conflict


[notice] A new release of pip is available: 24.3.1 -> 25.0.1
[notice] To update, run: /usr/local/opt/python@3.10/bin/python3.10 -m pip 
install --upgrade pip
ERROR: ResolutionImpossible: for help visit https://pip.pypa.io/en/latest/
topics/dependency-resolution/#dealing-with-dependency-conflicts

```

---

_****_





---

_**User**_

Do: 

uv pip install -e .[all,dev,test]; hatch run lint:fix; hatch test

---

_**Assistant**_

I'll help you run those commands:

---

_****_

```bash
uv pip install -e .[all,dev,test] && hatch run lint:fix && hatch test
```

```
zsh: no matches found: .[all,dev,test]

```

---

_****_



I see the issue - we need to quote the argument to prevent shell expansion. Let me try again:

---

_****_

```bash
uv pip install -e ".[all,dev,test]" && hatch run lint:fix && hatch test
```

```
Audited 1 package in 2ms
warning: The top-level linter settings are deprecated in favour of their c
ounterparts in the `lint` section. Please update the following options in
`pyproject.toml`:
  - 'per-file-ignores' -> 'lint.per-file-ignores'
src/twat_cache/cache.py:51:5: FBT001 Boolean-typed positional argument in 
function definition
   |
49 |     maxsize: int | None = None,
50 |     folder_name: str | None = None,
51 |     use_sql: bool = False,
   |     ^^^^^^^ FBT001
52 |     preferred_engine: str | None = None,
53 | ) -> Callable[[Callable[P, R]], Callable[P, R]]:
   |

src/twat_cache/cache.py:51:5: FBT002 Boolean default positional argument i
n function definition
   |
49 |     maxsize: int | None = None,
50 |     folder_name: str | None = None,
51 |     use_sql: bool = False,
   |     ^^^^^^^ FBT002
52 |     preferred_engine: str | None = None,
53 | ) -> Callable[[Callable[P, R]], Callable[P, R]]:
   |

src/twat_cache/config.py:158:30: T201 `print` found
    |
156 |         level = "DEBUG" if self.debug else "INFO"
157 |         logger.add(
158 |             sink=lambda msg: print(msg, end=""),
    |                              ^^^^^ T201
159 |             level=level,
160 |             format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    |
    = help: Remove `print`

src/twat_cache/engines/base.py:89:17: B904 Within an `except` clause, rais
e exceptions with `raise ... from err` or `raise ... from None` to disting
uish them from errors in exception handling
   |
87 |             except ValueError as e:
88 |                 msg = f"Invalid cache folder: {e}"
89 |                 raise ValueError(msg)
   |                 ^^^^^^^^^^^^^^^^^^^^^ B904
90 |
91 |     def _make_key(self, func: Callable[P, R], args: tuple, kwargs: di
ct) -> CacheKey:
   |

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

src/twat_cache/engines/manager.py:91:25: F821 Undefined name `EngineManage
r`
   |
89 |     """
90 |
91 |     _instance: ClassVar[EngineManager | None] = None
   |                         ^^^^^^^^^^^^^ F821
92 |
93 |     def __new__(cls) -> EngineManager:
   |

src/twat_cache/engines/manager.py:93:25: F821 Undefined name `EngineManage
r`
   |
91 |     _instance: ClassVar[EngineManager | None] = None
92 |
93 |     def __new__(cls) -> EngineManager:
   |                         ^^^^^^^^^^^^^ F821
94 |         """Create or return the singleton instance."""
95 |         if cls._instance is None:
   |

src/twat_cache/paths.py:99:9: B904 Within an `except` clause, raise except
ions with `raise ... from err` or `raise ... from None` to distinguish the
m from errors in exception handling
   |
97 |     except Exception as e:
98 |         msg = f"Invalid cache path {path}: {e}"
99 |         raise ValueError(msg)
   |         ^^^^^^^^^^^^^^^^^^^^^ B904
   |

src/twat_cache/paths.py:102:5: C901 `clear_cache` is too complex (11 > 10)
    |
102 | def clear_cache(folder_name: str | None = None) -> None:
    |     ^^^^^^^^^^^ C901
103 |     """
104 |     Clear the cache directory for the given folder name.
    |

src/twat_cache/types.py:1:1: A005 Module `types` shadows a Python standard
-library module
src/twat_cache/types.py:174:5: F822 Undefined name `F` in `__all__`
    |
172 |     "CacheStats",
173 |     "CacheValue",
174 |     "F",
    |     ^^^ F822
175 |     "KeyMaker",
176 |     "P",
    |

tests/test_cache.py:54:37: PLR2004 Magic value used in comparison, conside
r replacing `25` with a constant variable
   |
53 |     # First call should compute
54 |     assert expensive_function(5) == 25
   |                                     ^^ PLR2004
55 |     assert call_count == 1
   |

tests/test_cache.py:58:37: PLR2004 Magic value used in comparison, conside
r replacing `25` with a constant variable
   |
57 |     # Second call should use cache
58 |     assert expensive_function(5) == 25
   |                                     ^^ PLR2004
59 |     assert call_count == 1
   |

tests/test_cache.py:62:37: PLR2004 Magic value used in comparison, conside
r replacing `36` with a constant variable
   |
61 |     # Different input should compute
62 |     assert expensive_function(6) == 36
   |                                     ^^ PLR2004
63 |     assert call_count == 2
   |

tests/test_cache.py:63:26: PLR2004 Magic value used in comparison, conside
r replacing `2` with a constant variable
   |
61 |     # Different input should compute
62 |     assert expensive_function(6) == 36
63 |     assert call_count == 2
   |                          ^ PLR2004
   |

tests/test_cache.py:77:34: PLR2004 Magic value used in comparison, conside
r replacing `25` with a constant variable
   |
76 |     # First call
77 |     assert cached_function(5) == 25
   |                                  ^^ PLR2004
78 |     assert call_count == 1
   |

tests/test_cache.py:84:34: PLR2004 Magic value used in comparison, conside
r replacing `25` with a constant variable
   |
83 |     # Should recompute after clear
84 |     assert cached_function(5) == 25
   |                                  ^^ PLR2004
85 |     assert call_count == 2
   |

tests/test_cache.py:85:26: PLR2004 Magic value used in comparison, conside
r replacing `2` with a constant variable
   |
83 |     # Should recompute after clear
84 |     assert cached_function(5) == 25
85 |     assert call_count == 2
   |                          ^ PLR2004
   |

tests/test_cache.py:107:29: PLR2004 Magic value used in comparison, consid
er replacing `2` with a constant variable
    |
105 |     # Basic stats checks
106 |     assert isinstance(stats, dict)
107 |     assert stats["hits"] >= 2
    |                             ^ PLR2004
108 |     assert stats["misses"] >= 2
109 |     assert "size" in stats
    |

tests/test_cache.py:108:31: PLR2004 Magic value used in comparison, consid
er replacing `2` with a constant variable
    |
106 |     assert isinstance(stats, dict)
107 |     assert stats["hits"] >= 2
108 |     assert stats["misses"] >= 2
    |                               ^ PLR2004
109 |     assert "size" in stats
    |

tests/test_cache.py:152:34: PLR2004 Magic value used in comparison, consid
er replacing `15` with a constant variable
    |
150 |     result2 = process_list(test_list)
151 |
152 |     assert result1 == result2 == 15
    |                                  ^^ PLR2004
    |

tests/test_cache.py:188:33: PLR2004 Magic value used in comparison, consid
er replacing `5` with a constant variable
    |
187 |     # Test with different kwarg combinations
188 |     assert kwarg_function(5) == 5
    |                                 ^ PLR2004
189 |     assert call_count == 1
    |

tests/test_cache.py:191:47: PLR2004 Magic value used in comparison, consid
er replacing `5` with a constant variable
    |
189 |     assert call_count == 1
190 |
191 |     assert kwarg_function(5, multiplier=1) == 5
    |                                               ^ PLR2004
192 |     assert call_count == 1  # Should use cache
    |

tests/test_cache.py:194:47: PLR2004 Magic value used in comparison, consid
er replacing `10` with a constant variable
    |
192 |     assert call_count == 1  # Should use cache
193 |
194 |     assert kwarg_function(5, multiplier=2) == 10
    |                                               ^^ PLR2004
195 |     assert call_count == 2  # Different kwargs = new computation
    |

tests/test_cache.py:195:26: PLR2004 Magic value used in comparison, consid
er replacing `2` with a constant variable
    |
194 |     assert kwarg_function(5, multiplier=2) == 10
195 |     assert call_count == 2  # Different kwargs = new computation
    |                          ^ PLR2004
    |

tests/test_config.py:65:38: PLR2004 Magic value used in comparison, consid
er replacing `1000` with a constant variable
   |
64 |     assert config.cache_dir == get_cache_dir()
65 |     assert config.default_maxsize == 1000
   |                                      ^^^^ PLR2004
66 |     assert config.default_use_sql is False
67 |     assert config.default_engine == "lru"
   |

tests/test_config.py:69:40: PLR2004 Magic value used in comparison, consid
er replacing `6` with a constant variable
   |
67 |     assert config.default_engine == "lru"
68 |     assert config.enable_compression is True
69 |     assert config.compression_level == 6
   |                                        ^ PLR2004
70 |     assert config.debug is False
71 |     assert config.log_file is None
   |

tests/test_config.py:86:38: PLR2004 Magic value used in comparison, consid
er replacing `500` with a constant variable
   |
85 |     # Check values
86 |     assert config.default_maxsize == 500
   |                                      ^^^ PLR2004
87 |     assert config.default_use_sql is True
88 |     assert config.default_engine == "disk"
   |

tests/test_config.py:107:36: PLR2004 Magic value used in comparison, consi
der replacing `200` with a constant variable
    |
105 |         folder_name="test_cache",
106 |     )
107 |     assert cache_config.maxsize == 200
    |                                    ^^^ PLR2004
108 |     assert cache_config.folder_name == "test_cache"
109 |     assert cache_config.use_sql == global_config.default_use_sql
    |

tests/test_config.py:119:36: PLR2004 Magic value used in comparison, consi
der replacing `300` with a constant variable
    |
117 |         preferred_engine="disk",
118 |     )
119 |     assert cache_config.maxsize == 300
    |                                    ^^^ PLR2004
120 |     assert cache_config.folder_name == "custom_cache"
121 |     assert cache_config.use_sql is True
    |

tests/test_engines.py:123:28: PLR2004 Magic value used in comparison, cons
ider replacing `10` with a constant variable
    |
122 |     # First call should compute
123 |     assert test_func(5) == 10
    |                            ^^ PLR2004
124 |     assert call_count == 1
125 |     assert test_engine.stats["hits"] == 0
    |

tests/test_engines.py:129:28: PLR2004 Magic value used in comparison, cons
ider replacing `10` with a constant variable
    |
128 |     # Second call should use cache
129 |     assert test_func(5) == 10
    |                            ^^ PLR2004
130 |     assert call_count == 1
131 |     assert test_engine.stats["hits"] == 1
    |

tests/test_engines.py:135:29: PLR2004 Magic value used in comparison, cons
ider replacing `20` with a constant variable
    |
134 |     # Different arg should compute
135 |     assert test_func(10) == 20
    |                             ^^ PLR2004
136 |     assert call_count == 2
137 |     assert test_engine.stats["hits"] == 1
    |

tests/test_engines.py:136:26: PLR2004 Magic value used in comparison, cons
ider replacing `2` with a constant variable
    |
134 |     # Different arg should compute
135 |     assert test_func(10) == 20
136 |     assert call_count == 2
    |                          ^ PLR2004
137 |     assert test_engine.stats["hits"] == 1
138 |     assert test_engine.stats["misses"] == 2
    |

tests/test_engines.py:138:43: PLR2004 Magic value used in comparison, cons
ider replacing `2` with a constant variable
    |
136 |     assert call_count == 2
137 |     assert test_engine.stats["hits"] == 1
138 |     assert test_engine.stats["misses"] == 2
    |                                           ^ PLR2004
    |

tests/test_engines.py:168:38: PLR2004 Magic value used in comparison, cons
ider replacing `10` with a constant variable
    |
166 |         lru_engine._set_cached_value(("key", i), i)
167 |
168 |     assert len(lru_engine._cache) == 10
    |                                      ^^ PLR2004
169 |
170 |     # Add one more, should evict oldest
    |

tests/test_engines.py:172:38: PLR2004 Magic value used in comparison, cons
ider replacing `10` with a constant variable
    |
170 |     # Add one more, should evict oldest
171 |     lru_engine._set_cached_value(("key", 10), 10)
172 |     assert len(lru_engine._cache) == 10
    |                                      ^^ PLR2004
173 |     assert ("key", 0) not in lru_engine._cache  # First item should 
be evicted
174 |     assert ("key", 10) in lru_engine._cache  # New item should be pr
esent
    |

tests/test_engines.py:183:38: PLR2004 Magic value used in comparison, cons
ider replacing `5` with a constant variable
    |
181 |         lru_engine._set_cached_value(("key", i), i)
182 |
183 |     assert len(lru_engine._cache) == 5
    |                                      ^ PLR2004
184 |
185 |     # Clear cache
    |

tests/test_engines.py:226:29: PLR2004 Magic value used in comparison, cons
ider replacing `2` with a constant variable
    |
225 |     stats = lru_engine.stats
226 |     assert stats["hits"] == 2
    |                             ^ PLR2004
227 |     assert stats["misses"] == 2
228 |     assert stats["size"] == 2
    |

tests/test_engines.py:227:31: PLR2004 Magic value used in comparison, cons
ider replacing `2` with a constant variable
    |
225 |     stats = lru_engine.stats
226 |     assert stats["hits"] == 2
227 |     assert stats["misses"] == 2
    |                               ^ PLR2004
228 |     assert stats["size"] == 2
229 |     assert stats["current_size"] == 2
    |

tests/test_engines.py:228:29: PLR2004 Magic value used in comparison, cons
ider replacing `2` with a constant variable
    |
226 |     assert stats["hits"] == 2
227 |     assert stats["misses"] == 2
228 |     assert stats["size"] == 2
    |                             ^ PLR2004
229 |     assert stats["current_size"] == 2
    |

tests/test_engines.py:229:37: PLR2004 Magic value used in comparison, cons
ider replacing `2` with a constant variable
    |
227 |     assert stats["misses"] == 2
228 |     assert stats["size"] == 2
229 |     assert stats["current_size"] == 2
    |                                     ^ PLR2004
    |

tests/test_redis_cache.py:69:32: PLR2004 Magic value used in comparison, c
onsider replacing `6379` with a constant variable
   |
67 |     """Test Redis cache initialization."""
68 |     assert redis_cache.host == "localhost"
69 |     assert redis_cache.port == 6379
   |                                ^^^^ PLR2004
70 |     assert redis_cache.db == 0
71 |     assert redis_cache.ttl == 60
   |

tests/test_redis_cache.py:71:31: PLR2004 Magic value used in comparison, c
onsider replacing `60` with a constant variable
   |
69 |     assert redis_cache.port == 6379
70 |     assert redis_cache.db == 0
71 |     assert redis_cache.ttl == 60
   |                               ^^ PLR2004
   |

tests/test_redis_cache.py:85:28: PLR2004 Magic value used in comparison, c
onsider replacing `25` with a constant variable
   |
84 |     # First call should compute
85 |     assert test_func(5) == 25
   |                            ^^ PLR2004
86 |     assert call_count == 1
   |

tests/test_redis_cache.py:89:28: PLR2004 Magic value used in comparison, c
onsider replacing `25` with a constant variable
   |
88 |     # Second call should use cache
89 |     assert test_func(5) == 25
   |                            ^^ PLR2004
90 |     assert call_count == 1
   |

tests/test_redis_cache.py:93:28: PLR2004 Magic value used in comparison, c
onsider replacing `36` with a constant variable
   |
92 |     # Different input should compute
93 |     assert test_func(6) == 36
   |                            ^^ PLR2004
94 |     assert call_count == 2
   |

tests/test_redis_cache.py:94:26: PLR2004 Magic value used in comparison, c
onsider replacing `2` with a constant variable
   |
92 |     # Different input should compute
93 |     assert test_func(6) == 36
94 |     assert call_count == 2
   |                          ^ PLR2004
   |

tests/test_redis_cache.py:108:28: PLR2004 Magic value used in comparison, 
consider replacing `25` with a constant variable
    |
107 |     # First call
108 |     assert test_func(5) == 25
    |                            ^^ PLR2004
109 |     assert call_count == 1
    |

tests/test_redis_cache.py:112:28: PLR2004 Magic value used in comparison, 
consider replacing `25` with a constant variable
    |
111 |     # Second call (within TTL)
112 |     assert test_func(5) == 25
    |                            ^^ PLR2004
113 |     assert call_count == 1
    |

tests/test_redis_cache.py:119:28: PLR2004 Magic value used in comparison, 
consider replacing `25` with a constant variable
    |
118 |     # Call after TTL expiration
119 |     assert test_func(5) == 25
    |                            ^^ PLR2004
120 |     assert call_count == 2
    |

tests/test_redis_cache.py:120:26: PLR2004 Magic value used in comparison, 
consider replacing `2` with a constant variable
    |
118 |     # Call after TTL expiration
119 |     assert test_func(5) == 25
120 |     assert call_count == 2
    |                          ^ PLR2004
    |

tests/test_redis_cache.py:160:29: PLR2004 Magic value used in comparison, 
consider replacing `2` with a constant variable
    |
158 |     # Check stats
159 |     stats = redis_cache.stats
160 |     assert stats["hits"] >= 2
    |                             ^ PLR2004
161 |     assert stats["misses"] >= 2
162 |     assert stats["size"] == 2
    |

tests/test_redis_cache.py:161:31: PLR2004 Magic value used in comparison, 
consider replacing `2` with a constant variable
    |
159 |     stats = redis_cache.stats
160 |     assert stats["hits"] >= 2
161 |     assert stats["misses"] >= 2
    |                               ^ PLR2004
162 |     assert stats["size"] == 2
    |

tests/test_redis_cache.py:162:29: PLR2004 Magic value used in comparison, 
consider replacing `2` with a constant variable
    |
160 |     assert stats["hits"] >= 2
161 |     assert stats["misses"] >= 2
162 |     assert stats["size"] == 2
    |                             ^ PLR2004
    |

tests/test_redis_cache.py:184:30: PLR2004 Magic value used in comparison, 
consider replacing `15` with a constant variable
    |
183 |     assert result1 == result2
184 |     assert result1["sum"] == 15
    |                              ^^ PLR2004
185 |     assert result1["len"] == 5
    |

tests/test_redis_cache.py:185:30: PLR2004 Magic value used in comparison, 
consider replacing `5` with a constant variable
    |
183 |     assert result1 == result2
184 |     assert result1["sum"] == 15
185 |     assert result1["len"] == 5
    |                              ^ PLR2004
    |

tests/test_redis_cache.py:220:41: PLR2004 Magic value used in comparison, 
consider replacing `2` with a constant variable
    |
218 |     test_func(5)
219 |     test_func(6)
220 |     assert redis_cache.stats["size"] == 2
    |                                         ^ PLR2004
221 |
222 |     # Different kwargs should have different keys
    |

tests/test_redis_cache.py:224:41: PLR2004 Magic value used in comparison, 
consider replacing `3` with a constant variable
    |
222 |     # Different kwargs should have different keys
223 |     test_func(5, multiplier=2)
224 |     assert redis_cache.stats["size"] == 3
    |                                         ^ PLR2004
225 |
226 |     # Same args and kwargs should use same key
    |

tests/test_redis_cache.py:228:41: PLR2004 Magic value used in comparison, 
consider replacing `3` with a constant variable
    |
226 |     # Same args and kwargs should use same key
227 |     test_func(5, multiplier=2)
228 |     assert redis_cache.stats["size"] == 3
    |                                         ^ PLR2004
    |

tests/test_redis_cache.py:242:28: PLR2004 Magic value used in comparison, 
consider replacing `25` with a constant variable
    |
241 |     # First call (normal operation)
242 |     assert test_func(5) == 25
    |                            ^^ PLR2004
243 |     assert call_count == 1
    |

tests/test_redis_cache.py:249:28: PLR2004 Magic value used in comparison, 
consider replacing `25` with a constant variable
    |
248 |     # Call should still work (fallback to computing)
249 |     assert test_func(5) == 25
    |                            ^^ PLR2004
250 |     assert call_count == 2
    |

tests/test_redis_cache.py:250:26: PLR2004 Magic value used in comparison, 
consider replacing `2` with a constant variable
    |
248 |     # Call should still work (fallback to computing)
249 |     assert test_func(5) == 25
250 |     assert call_count == 2
    |                          ^ PLR2004
    |

tests/test_sql_cache.py:61:5: N806 Variable `Session` in function should b
e lowercase
   |
59 |     # Check that tables were created
60 |     db_engine = create_engine(f"sqlite:///{db_path}")
61 |     Session = sessionmaker(bind=db_engine)
   |     ^^^^^^^ N806
62 |     with Session() as session:
63 |         # Should not raise
   |

tests/test_sql_cache.py:78:28: PLR2004 Magic value used in comparison, con
sider replacing `25` with a constant variable
   |
77 |     # First call should compute
78 |     assert test_func(5) == 25
   |                            ^^ PLR2004
79 |     assert call_count == 1
   |

tests/test_sql_cache.py:82:28: PLR2004 Magic value used in comparison, con
sider replacing `25` with a constant variable
   |
81 |     # Second call should use cache
82 |     assert test_func(5) == 25
   |                            ^^ PLR2004
83 |     assert call_count == 1
   |

tests/test_sql_cache.py:86:28: PLR2004 Magic value used in comparison, con
sider replacing `36` with a constant variable
   |
85 |     # Different input should compute
86 |     assert test_func(6) == 36
   |                            ^^ PLR2004
87 |     assert call_count == 2
   |

tests/test_sql_cache.py:87:26: PLR2004 Magic value used in comparison, con
sider replacing `2` with a constant variable
   |
85 |     # Different input should compute
86 |     assert test_func(6) == 36
87 |     assert call_count == 2
   |                          ^ PLR2004
   |

tests/test_sql_cache.py:103:29: PLR2004 Magic value used in comparison, co
nsider replacing `100` with a constant variable
    |
101 |     # Check that cache was pruned
102 |     stats = sql_cache.stats
103 |     assert stats["size"] <= 100
    |                             ^^^ PLR2004
    |

tests/test_sql_cache.py:143:29: PLR2004 Magic value used in comparison, co
nsider replacing `2` with a constant variable
    |
141 |     # Check stats
142 |     stats = sql_cache.stats
143 |     assert stats["hits"] >= 2
    |                             ^ PLR2004
144 |     assert stats["misses"] >= 2
145 |     assert stats["size"] == 2
    |

tests/test_sql_cache.py:144:31: PLR2004 Magic value used in comparison, co
nsider replacing `2` with a constant variable
    |
142 |     stats = sql_cache.stats
143 |     assert stats["hits"] >= 2
144 |     assert stats["misses"] >= 2
    |                               ^ PLR2004
145 |     assert stats["size"] == 2
    |

tests/test_sql_cache.py:145:29: PLR2004 Magic value used in comparison, co
nsider replacing `2` with a constant variable
    |
143 |     assert stats["hits"] >= 2
144 |     assert stats["misses"] >= 2
145 |     assert stats["size"] == 2
    |                             ^ PLR2004
    |

tests/test_sql_cache.py:167:30: PLR2004 Magic value used in comparison, co
nsider replacing `15` with a constant variable
    |
166 |     assert result1 == result2
167 |     assert result1["sum"] == 15
    |                              ^^ PLR2004
168 |     assert result1["len"] == 5
    |

tests/test_sql_cache.py:168:30: PLR2004 Magic value used in comparison, co
nsider replacing `5` with a constant variable
    |
166 |     assert result1 == result2
167 |     assert result1["sum"] == 15
168 |     assert result1["len"] == 5
    |                              ^ PLR2004
    |

tests/test_sql_cache.py:203:39: PLR2004 Magic value used in comparison, co
nsider replacing `2` with a constant variable
    |
201 |     test_func(5)
202 |     test_func(6)
203 |     assert sql_cache.stats["size"] == 2
    |                                       ^ PLR2004
204 |
205 |     # Different kwargs should have different keys
    |

tests/test_sql_cache.py:207:39: PLR2004 Magic value used in comparison, co
nsider replacing `3` with a constant variable
    |
205 |     # Different kwargs should have different keys
206 |     test_func(5, multiplier=2)
207 |     assert sql_cache.stats["size"] == 3
    |                                       ^ PLR2004
208 |
209 |     # Same args and kwargs should use same key
    |

tests/test_sql_cache.py:211:39: PLR2004 Magic value used in comparison, co
nsider replacing `3` with a constant variable
    |
209 |     # Same args and kwargs should use same key
210 |     test_func(5, multiplier=2)
211 |     assert sql_cache.stats["size"] == 3
    |                                       ^ PLR2004
    |

Found 79 errors.

```

---

_****_





I see we have a lot of linting errors to fix. Let me help you fix them systematically. First, let's check the `LOG.md` file to understand the project's progress:

---

_****_

Read file: LOG.md

---

_****_







Now let's check the README to understand the project better:

---

_****_

Read file: README.md

---

_****_



---



---

