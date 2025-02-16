# twat-cache

A flexible caching utility package for Python functions that provides a unified interface for caching function results using various high-performance backends.

## Features

- Simple decorator interface for caching function results
- Multiple caching backends with automatic selection:
  1. `cachebox` - Very fast Rust-based cache (optional)
  2. `cachetools` - Flexible in-memory caching (optional)
  3. `aiocache` - Async-capable caching (optional)
  4. `klepto` - Scientific computing caching (optional)
  5. `diskcache` - SQL-based disk cache (optional)
  6. `joblib` - Efficient array caching (optional)
  7. Memory-based LRU cache (always available)
- Automatic cache directory management
- Type hints and modern Python features
- Lazy backend loading - only imports what you use
- Automatic backend selection based on availability and use case

## Installation

Basic installation with just LRU caching:
```bash
pip install twat-cache
```

With all optional backends:
```bash
pip install twat-cache[all]
```

Or install specific backends:
```bash
pip install twat-cache[cachebox]     # For Rust-based high-performance cache
pip install twat-cache[cachetools]   # For flexible in-memory caching
pip install twat-cache[aiocache]     # For async-capable caching
pip install twat-cache[klepto]       # For scientific computing caching
pip install twat-cache[diskcache]    # For SQL-based disk caching
pip install twat-cache[joblib]       # For efficient array caching
```

## Usage

Basic usage with automatic backend selection:

```python
from twat_cache import ucache

@ucache()
def expensive_computation(x):
    # Results will be cached automatically using the best available backend
    return x * x

result = expensive_computation(42)  # Computed
result = expensive_computation(42)  # Retrieved from cache
```

Using SQL-based disk cache:

```python
@ucache(folder_name="my_cache", use_sql=True)
def process_data(data):
    # Results will be cached to disk using SQL backend
    return data.process()
```

Using joblib for efficient array caching:

```python
import numpy as np
from twat_cache import ucache

@ucache(folder_name="array_cache", preferred_engine="joblib")
def matrix_operation(arr):
    # Large array operations will be efficiently cached
    return np.dot(arr, arr.T)
```

Using the high-performance Rust-based cache:

```python
@ucache(preferred_engine="cachebox")
def fast_computation(x):
    # Results will be cached using the fast Rust-based backend
    return x * x
```

Async function caching:

```python
@ucache(preferred_engine="aiocache")
async def fetch_data(url):
    # Results will be cached with async support
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
```

Scientific computing with klepto:

```python
@ucache(folder_name="science_cache", preferred_engine="klepto")
def compute_simulation(params):
    # Results will be cached with scientific computing optimizations
    return run_simulation(params)
```

## Cache Location

The package automatically manages cache directories using the following strategy:

1. If `platformdirs` is available, uses the platform-specific user cache directory
2. Otherwise, falls back to `~/.cache`

You can get the cache path programmatically:

```python
from twat_cache import get_cache_path

cache_dir = get_cache_path("my_cache")
```

## Dependencies

- Required: None (basic memory caching works without dependencies)
- Optional:
  - `platformdirs`: For platform-specific cache directories
  - `cachebox`: For Rust-based high-performance caching
  - `cachetools`: For flexible in-memory caching
  - `aiocache`: For async-capable caching
  - `klepto`: For scientific computing caching
  - `diskcache`: For SQL-based disk caching
  - `joblib`: For efficient array caching

## Backend Selection

The backend selection is prioritized in the following order:
1. User's preferred engine (if specified and available)
2. SQL-based engine (if `use_sql=True`)
3. Default priority:
   - `cachebox` (fastest, Rust-based)
   - `cachetools` (flexible in-memory)
   - `aiocache` (async support)
   - `klepto` (scientific computing)
   - `diskcache` (SQL-based)
   - `joblib` (array caching)
   - LRU cache (built-in fallback)

## License

MIT License

---

Current project file tree:

.
├── .DS_Store
├── .github
│   └── workflows
│       ├── push.yml
│       └── release.yml
├── .gitignore
├── .pre-commit-config.yaml
├── .specstory
│   └── history
│       ├── .what-is-this.md
│       ├── codebase-improvement-and-dependency-management-plan.md
│       ├── implementing-todo-item.md
│       ├── merging-files-from-wrong-location.md
│       ├── project-documentation-and-command-execution.md
│       ├── project-review-and-implementation.md
│       ├── running-lint-fix-command.md
│       ├── todo-list-update-and-progress-logging.md
│       ├── untitled.md
│       ├── update-todo-and-log-for-project.md
│       └── updating-todos-and-project-documentation.md
├── .venv
│   ├── .gitignore
│   ├── .lock
│   ├── CACHEDIR.TAG
│   ├── bin
│   │   ├── activate
│   │   ├── activate.bat
│   │   ├── activate.csh
│   │   ├── activate.fish
│   │   ├── activate.nu
│   │   ├── activate.ps1
│   │   ├── activate_this.py
│   │   ├── coverage
│   │   ├── coverage-3.12
│   │   ├── coverage3
│   │   ├── cpuinfo
│   │   ├── deactivate.bat
│   │   ├── dmypy
│   │   ├── dotenv
│   │   ├── f2py
│   │   ├── get_gprof
│   │   ├── get_objgraph
│   │   ├── mypy
│   │   ├── mypyc
│   │   ├── numpy-config
│   │   ├── pox
│   │   ├── py.test
│   │   ├── py.test-benchmark
│   │   ├── pydoc.bat
│   │   ├── pygal_gen.py
│   │   ├── pytest
│   │   ├── pytest-benchmark
│   │   ├── python -> /Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12
│   │   ├── python3 -> python
│   │   ├── python3.12 -> python
│   │   ├── ruff
│   │   ├── stubgen
│   │   ├── stubtest
│   │   └── undill
│   ├── lib
│   │   └── python3.12
│   │       └── site-packages
│   │           ├── 3204bda914b7f2c6f497__mypyc.cpython-312-darwin.so
│   │           ├── __pycache__
│   │           │   └── _virtualenv.cpython-312.pyc
│   │           ├── _distutils_hack
│   │           │   ├── __init__.py
│   │           │   ├── __pycache__
│   │           │   │   └── __init__.cpython-312.pyc
│   │           │   └── override.py
│   │           ├── _pytest
│   │           │   ├── __init__.py
│   │           │   ├── _argcomplete.py
│   │           │   ├── _code
│   │           │   │   ├── __init__.py
│   │           │   │   ├── code.py
│   │           │   │   └── source.py
│   │           │   ├── _io
│   │           │   │   ├── __init__.py
│   │           │   │   ├── pprint.py
│   │           │   │   ├── saferepr.py
│   │           │   │   ├── terminalwriter.py
│   │           │   │   └── wcwidth.py
│   │           │   ├── _py
│   │           │   │   ├── __init__.py
│   │           │   │   ├── error.py
│   │           │   │   └── path.py
│   │           │   ├── _version.py
│   │           │   ├── assertion
│   │           │   │   ├── __init__.py
│   │           │   │   ├── rewrite.py
│   │           │   │   ├── truncate.py
│   │           │   │   └── util.py
│   │           │   ├── cacheprovider.py
│   │           │   ├── capture.py
│   │           │   ├── compat.py
│   │           │   ├── config
│   │           │   │   ├── __init__.py
│   │           │   │   ├── argparsing.py
│   │           │   │   ├── compat.py
│   │           │   │   ├── exceptions.py
│   │           │   │   └── findpaths.py
│   │           │   ├── debugging.py
│   │           │   ├── deprecated.py
│   │           │   ├── doctest.py
│   │           │   ├── faulthandler.py
│   │           │   ├── fixtures.py
│   │           │   ├── freeze_support.py
│   │           │   ├── helpconfig.py
│   │           │   ├── hookspec.py
│   │           │   ├── junitxml.py
│   │           │   ├── legacypath.py
│   │           │   ├── logging.py
│   │           │   ├── main.py
│   │           │   ├── mark
│   │           │   │   ├── __init__.py
│   │           │   │   ├── expression.py
│   │           │   │   └── structures.py
│   │           │   ├── monkeypatch.py
│   │           │   ├── nodes.py
│   │           │   ├── outcomes.py
│   │           │   ├── pastebin.py
│   │           │   ├── pathlib.py
│   │           │   ├── py.typed
│   │           │   ├── pytester.py
│   │           │   ├── pytester_assertions.py
│   │           │   ├── python.py
│   │           │   ├── python_api.py
│   │           │   ├── python_path.py
│   │           │   ├── recwarn.py
│   │           │   ├── reports.py
│   │           │   ├── runner.py
│   │           │   ├── scope.py
│   │           │   ├── setuponly.py
│   │           │   ├── setupplan.py
│   │           │   ├── skipping.py
│   │           │   ├── stash.py
│   │           │   ├── stepwise.py
│   │           │   ├── terminal.py
│   │           │   ├── threadexception.py
│   │           │   ├── timing.py
│   │           │   ├── tmpdir.py
│   │           │   ├── unittest.py
│   │           │   ├── unraisableexception.py
│   │           │   ├── warning_types.py
│   │           │   └── warnings.py
│   │           ├── _twat_cache.pth
│   │           ├── _virtualenv.pth
│   │           ├── _virtualenv.py
│   │           ├── aiocache
│   │           │   ├── __init__.py
│   │           │   ├── backends
│   │           │   │   ├── __init__.py
│   │           │   │   ├── memcached.py
│   │           │   │   ├── memory.py
│   │           │   │   └── redis.py
│   │           │   ├── base.py
│   │           │   ├── decorators.py
│   │           │   ├── exceptions.py
│   │           │   ├── factory.py
│   │           │   ├── lock.py
│   │           │   ├── plugins.py
│   │           │   └── serializers
│   │           │       ├── __init__.py
│   │           │       └── serializers.py
│   │           ├── aiocache-0.12.3.dist-info
│   │           │   ├── INSTALLER
│   │           │   ├── LICENSE
│   │           │   ├── METADATA
│   │           │   ├── RECORD
│   │           │   ├── REQUESTED
│   │           │   ├── WHEEL
│   │           │   └── top_level.txt
│   │           ├── annotated_types
│   │           │   ├── __init__.py
│   │           │   ├── py.typed
│   │           │   └── test_cases.py
│   │           ├── annotated_types-0.7.0.dist-info
│   │           │   ├── INSTALLER
│   │           │   ├── METADATA
│   │           │   ├── RECORD
│   │           │   ├── REQUESTED
│   │           │   ├── WHEEL
│   │           │   └── licenses
│   │           │       └── LICENSE
│   │           ├── cachebox
│   │           │   ├── __init__.py
│   │           │   ├── _cachebox.cpython-312-darwin.so
│   │           │   ├── _cachebox.pyi
│   │           │   ├── py.typed
│   │           │   └── utils.py
│   │           ├── cachebox-4.5.1.dist-info
│   │           │   ├── INSTALLER
│   │           │   ├── METADATA
│   │           │   ├── RECORD
│   │           │   ├── REQUESTED
│   │           │   ├── WHEEL
│   │           │   └── licenses
│   │           │       └── LICENSE
│   │           ├── cachetools
│   │           │   ├── __init__.py
│   │           │   ├── func.py
│   │           │   └── keys.py
│   │           ├── cachetools-5.5.1.dist-info
│   │           │   ├── INSTALLER
│   │           │   ├── LICENSE
│   │           │   ├── METADATA
│   │           │   ├── RECORD
│   │           │   ├── REQUESTED
│   │           │   ├── WHEEL
│   │           │   └── top_level.txt
│   │           ├── coverage
│   │           │   ├── __init__.py
│   │           │   ├── __main__.py
│   │           │   ├── annotate.py
│   │           │   ├── bytecode.py
│   │           │   ├── cmdline.py
│   │           │   ├── collector.py
│   │           │   ├── config.py
│   │           │   ├── context.py
│   │           │   ├── control.py
│   │           │   ├── core.py
│   │           │   ├── data.py
│   │           │   ├── debug.py
│   │           │   ├── disposition.py
│   │           │   ├── env.py
│   │           │   ├── exceptions.py
│   │           │   ├── execfile.py
│   │           │   ├── files.py
│   │           │   ├── html.py
│   │           │   ├── htmlfiles
│   │           │   │   ├── coverage_html.js
│   │           │   │   ├── favicon_32.png
│   │           │   │   ├── index.html
│   │           │   │   ├── keybd_closed.png
│   │           │   │   ├── pyfile.html
│   │           │   │   ├── style.css
│   │           │   │   └── style.scss
│   │           │   ├── inorout.py
│   │           │   ├── jsonreport.py
│   │           │   ├── lcovreport.py
│   │           │   ├── misc.py
│   │           │   ├── multiproc.py
│   │           │   ├── numbits.py
│   │           │   ├── parser.py
│   │           │   ├── phystokens.py
│   │           │   ├── plugin.py
│   │           │   ├── plugin_support.py
│   │           │   ├── py.typed
│   │           │   ├── python.py
│   │           │   ├── pytracer.py
│   │           │   ├── regions.py
│   │           │   ├── report.py
│   │           │   ├── report_core.py
│   │           │   ├── results.py
│   │           │   ├── sqldata.py
│   │           │   ├── sqlitedb.py
│   │           │   ├── sysmon.py
│   │           │   ├── templite.py
│   │           │   ├── tomlconfig.py
│   │           │   ├── tracer.cpython-312-darwin.so
│   │           │   ├── tracer.pyi
│   │           │   ├── types.py
│   │           │   ├── version.py
│   │           │   └── xmlreport.py
│   │           ├── coverage-7.6.12.dist-info
│   │           │   ├── INSTALLER
│   │           │   ├── LICENSE.txt
│   │           │   ├── METADATA
│   │           │   ├── RECORD
│   │           │   ├── REQUESTED
│   │           │   ├── WHEEL
│   │           │   ├── entry_points.txt
│   │           │   └── top_level.txt
│   │           ├── cpuinfo
│   │           │   ├── __init__.py
│   │           │   ├── __main__.py
│   │           │   └── cpuinfo.py
│   │           ├── dill
│   │           │   ├── __diff.py
│   │           │   ├── __info__.py
│   │           │   ├── __init__.py
│   │           │   ├── _dill.py
│   │           │   ├── _objects.py
│   │           │   ├── _shims.py
│   │           │   ├── detect.py
│   │           │   ├── logger.py
│   │           │   ├── objtypes.py
│   │           │   ├── pointers.py
│   │           │   ├── session.py
│   │           │   ├── settings.py
│   │           │   ├── source.py
│   │           │   ├── temp.py
│   │           │   └── tests
│   │           │       ├── __init__.py
│   │           │       ├── __main__.py
│   │           │       ├── test_abc.py
│   │           │       ├── test_check.py
│   │           │       ├── test_classdef.py
│   │           │       ├── test_dataclasses.py
│   │           │       ├── test_detect.py
│   │           │       ├── test_dictviews.py
│   │           │       ├── test_diff.py
│   │           │       ├── test_extendpickle.py
│   │           │       ├── test_fglobals.py
│   │           │       ├── test_file.py
│   │           │       ├── test_functions.py
│   │           │       ├── test_functors.py
│   │           │       ├── test_logger.py
│   │           │       ├── test_mixins.py
│   │           │       ├── test_module.py
│   │           │       ├── test_moduledict.py
│   │           │       ├── test_nested.py
│   │           │       ├── test_objects.py
│   │           │       ├── test_properties.py
│   │           │       ├── test_pycapsule.py
│   │           │       ├── test_recursive.py
│   │           │       ├── test_registered.py
│   │           │       ├── test_restricted.py
│   │           │       ├── test_selected.py
│   │           │       ├── test_session.py
│   │           │       ├── test_source.py
│   │           │       ├── test_sources.py
│   │           │       ├── test_temp.py
│   │           │       ├── test_threads.py
│   │           │       └── test_weakref.py
│   │           ├── dill-0.3.9.dist-info
│   │           │   ├── INSTALLER
│   │           │   ├── LICENSE
│   │           │   ├── METADATA
│   │           │   ├── RECORD
│   │           │   ├── REQUESTED
│   │           │   ├── WHEEL
│   │           │   └── top_level.txt
│   │           ├── diskcache
│   │           │   ├── __init__.py
│   │           │   ├── cli.py
│   │           │   ├── core.py
│   │           │   ├── djangocache.py
│   │           │   ├── fanout.py
│   │           │   ├── persistent.py
│   │           │   └── recipes.py
│   │           ├── diskcache-5.6.3.dist-info
│   │           │   ├── INSTALLER
│   │           │   ├── LICENSE
│   │           │   ├── METADATA
│   │           │   ├── RECORD
│   │           │   ├── REQUESTED
│   │           │   ├── WHEEL
│   │           │   └── top_level.txt
│   │           ├── distutils-precedence.pth
│   │           ├── dotenv
│   │           │   ├── __init__.py
│   │           │   ├── __main__.py
│   │           │   ├── cli.py
│   │           │   ├── ipython.py
│   │           │   ├── main.py
│   │           │   ├── parser.py
│   │           │   ├── py.typed
│   │           │   ├── variables.py
│   │           │   └── version.py
│   │           ├── execnet
│   │           │   ├── __init__.py
│   │           │   ├── _version.py
│   │           │   ├── gateway.py
│   │           │   ├── gateway_base.py
│   │           │   ├── gateway_bootstrap.py
│   │           │   ├── gateway_io.py
│   │           │   ├── gateway_socket.py
│   │           │   ├── multi.py
│   │           │   ├── py.typed
│   │           │   ├── rsync.py
│   │           │   ├── rsync_remote.py
│   │           │   ├── script
│   │           │   │   ├── __init__.py
│   │           │   │   ├── loop_socketserver.py
│   │           │   │   ├── quitserver.py
│   │           │   │   ├── shell.py
│   │           │   │   ├── socketserver.py
│   │           │   │   └── socketserverservice.py
│   │           │   └── xspec.py
│   │           ├── execnet-2.1.1.dist-info
│   │           │   ├── INSTALLER
│   │           │   ├── METADATA
│   │           │   ├── RECORD
│   │           │   ├── REQUESTED
│   │           │   ├── WHEEL
│   │           │   └── licenses
│   │           │       └── LICENSE
│   │           ├── importlib_metadata
│   │           │   ├── __init__.py
│   │           │   ├── _adapters.py
│   │           │   ├── _collections.py
│   │           │   ├── _compat.py
│   │           │   ├── _functools.py
│   │           │   ├── _itertools.py
│   │           │   ├── _meta.py
│   │           │   ├── _text.py
│   │           │   ├── compat
│   │           │   │   ├── __init__.py
│   │           │   │   ├── py311.py
│   │           │   │   └── py39.py
│   │           │   ├── diagnose.py
│   │           │   └── py.typed
│   │           ├── importlib_metadata-8.6.1.dist-info
│   │           │   ├── INSTALLER
│   │           │   ├── LICENSE
│   │           │   ├── METADATA
│   │           │   ├── RECORD
│   │           │   ├── REQUESTED
│   │           │   ├── WHEEL
│   │           │   └── top_level.txt
│   │           ├── iniconfig
│   │           │   ├── __init__.py
│   │           │   ├── _parse.py
│   │           │   ├── _version.py
│   │           │   ├── exceptions.py
│   │           │   └── py.typed
│   │           ├── iniconfig-2.0.0.dist-info
│   │           │   ├── INSTALLER
│   │           │   ├── METADATA
│   │           │   ├── RECORD
│   │           │   ├── REQUESTED
│   │           │   ├── WHEEL
│   │           │   └── licenses
│   │           │       └── LICENSE
│   │           ├── joblib
│   │           │   ├── __init__.py
│   │           │   ├── _cloudpickle_wrapper.py
│   │           │   ├── _dask.py
│   │           │   ├── _memmapping_reducer.py
│   │           │   ├── _multiprocessing_helpers.py
│   │           │   ├── _parallel_backends.py
│   │           │   ├── _store_backends.py
│   │           │   ├── _utils.py
│   │           │   ├── backports.py
│   │           │   ├── compressor.py
│   │           │   ├── disk.py
│   │           │   ├── executor.py
│   │           │   ├── externals
│   │           │   │   ├── __init__.py
│   │           │   │   ├── cloudpickle
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   ├── cloudpickle.py
│   │           │   │   │   └── cloudpickle_fast.py
│   │           │   │   └── loky
│   │           │   │       ├── __init__.py
│   │           │   │       ├── _base.py
│   │           │   │       ├── backend
│   │           │   │       │   ├── __init__.py
│   │           │   │       │   ├── _posix_reduction.py
│   │           │   │       │   ├── _win_reduction.py
│   │           │   │       │   ├── context.py
│   │           │   │       │   ├── fork_exec.py
│   │           │   │       │   ├── popen_loky_posix.py
│   │           │   │       │   ├── popen_loky_win32.py
│   │           │   │       │   ├── process.py
│   │           │   │       │   ├── queues.py
│   │           │   │       │   ├── reduction.py
│   │           │   │       │   ├── resource_tracker.py
│   │           │   │       │   ├── spawn.py
│   │           │   │       │   ├── synchronize.py
│   │           │   │       │   └── utils.py
│   │           │   │       ├── cloudpickle_wrapper.py
│   │           │   │       ├── initializers.py
│   │           │   │       ├── process_executor.py
│   │           │   │       └── reusable_executor.py
│   │           │   ├── func_inspect.py
│   │           │   ├── hashing.py
│   │           │   ├── logger.py
│   │           │   ├── memory.py
│   │           │   ├── numpy_pickle.py
│   │           │   ├── numpy_pickle_compat.py
│   │           │   ├── numpy_pickle_utils.py
│   │           │   ├── parallel.py
│   │           │   ├── pool.py
│   │           │   ├── test
│   │           │   │   ├── __init__.py
│   │           │   │   ├── common.py
│   │           │   │   ├── data
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   ├── create_numpy_pickle.py
│   │           │   │   │   ├── joblib_0.10.0_compressed_pickle_py27_np16.gz
│   │           │   │   │   ├── joblib_0.10.0_compressed_pickle_py27_np17.gz
│   │           │   │   │   ├── joblib_0.10.0_compressed_pickle_py33_np18.gz
│   │           │   │   │   ├── joblib_0.10.0_compressed_pickle_py34_np19.gz
│   │           │   │   │   ├── joblib_0.10.0_compressed_pickle_py35_np19.gz
│   │           │   │   │   ├── joblib_0.10.0_pickle_py27_np17.pkl
│   │           │   │   │   ├── joblib_0.10.0_pickle_py27_np17.pkl.bz2
│   │           │   │   │   ├── joblib_0.10.0_pickle_py27_np17.pkl.gzip
│   │           │   │   │   ├── joblib_0.10.0_pickle_py27_np17.pkl.lzma
│   │           │   │   │   ├── joblib_0.10.0_pickle_py27_np17.pkl.xz
│   │           │   │   │   ├── joblib_0.10.0_pickle_py33_np18.pkl
│   │           │   │   │   ├── joblib_0.10.0_pickle_py33_np18.pkl.bz2
│   │           │   │   │   ├── joblib_0.10.0_pickle_py33_np18.pkl.gzip
│   │           │   │   │   ├── joblib_0.10.0_pickle_py33_np18.pkl.lzma
│   │           │   │   │   ├── joblib_0.10.0_pickle_py33_np18.pkl.xz
│   │           │   │   │   ├── joblib_0.10.0_pickle_py34_np19.pkl
│   │           │   │   │   ├── joblib_0.10.0_pickle_py34_np19.pkl.bz2
│   │           │   │   │   ├── joblib_0.10.0_pickle_py34_np19.pkl.gzip
│   │           │   │   │   ├── joblib_0.10.0_pickle_py34_np19.pkl.lzma
│   │           │   │   │   ├── joblib_0.10.0_pickle_py34_np19.pkl.xz
│   │           │   │   │   ├── joblib_0.10.0_pickle_py35_np19.pkl
│   │           │   │   │   ├── joblib_0.10.0_pickle_py35_np19.pkl.bz2
│   │           │   │   │   ├── joblib_0.10.0_pickle_py35_np19.pkl.gzip
│   │           │   │   │   ├── joblib_0.10.0_pickle_py35_np19.pkl.lzma
│   │           │   │   │   ├── joblib_0.10.0_pickle_py35_np19.pkl.xz
│   │           │   │   │   ├── joblib_0.11.0_compressed_pickle_py36_np111.gz
│   │           │   │   │   ├── joblib_0.11.0_pickle_py36_np111.pkl
│   │           │   │   │   ├── joblib_0.11.0_pickle_py36_np111.pkl.bz2
│   │           │   │   │   ├── joblib_0.11.0_pickle_py36_np111.pkl.gzip
│   │           │   │   │   ├── joblib_0.11.0_pickle_py36_np111.pkl.lzma
│   │           │   │   │   ├── joblib_0.11.0_pickle_py36_np111.pkl.xz
│   │           │   │   │   ├── joblib_0.8.4_compressed_pickle_py27_np17.gz
│   │           │   │   │   ├── joblib_0.9.2_compressed_pickle_py27_np16.gz
│   │           │   │   │   ├── joblib_0.9.2_compressed_pickle_py27_np17.gz
│   │           │   │   │   ├── joblib_0.9.2_compressed_pickle_py34_np19.gz
│   │           │   │   │   ├── joblib_0.9.2_compressed_pickle_py35_np19.gz
│   │           │   │   │   ├── joblib_0.9.2_pickle_py27_np16.pkl
│   │           │   │   │   ├── joblib_0.9.2_pickle_py27_np16.pkl_01.npy
│   │           │   │   │   ├── joblib_0.9.2_pickle_py27_np16.pkl_02.npy
│   │           │   │   │   ├── joblib_0.9.2_pickle_py27_np16.pkl_03.npy
│   │           │   │   │   ├── joblib_0.9.2_pickle_py27_np16.pkl_04.npy
│   │           │   │   │   ├── joblib_0.9.2_pickle_py27_np17.pkl
│   │           │   │   │   ├── joblib_0.9.2_pickle_py27_np17.pkl_01.npy
│   │           │   │   │   ├── joblib_0.9.2_pickle_py27_np17.pkl_02.npy
│   │           │   │   │   ├── joblib_0.9.2_pickle_py27_np17.pkl_03.npy
│   │           │   │   │   ├── joblib_0.9.2_pickle_py27_np17.pkl_04.npy
│   │           │   │   │   ├── joblib_0.9.2_pickle_py33_np18.pkl
│   │           │   │   │   ├── joblib_0.9.2_pickle_py33_np18.pkl_01.npy
│   │           │   │   │   ├── joblib_0.9.2_pickle_py33_np18.pkl_02.npy
│   │           │   │   │   ├── joblib_0.9.2_pickle_py33_np18.pkl_03.npy
│   │           │   │   │   ├── joblib_0.9.2_pickle_py33_np18.pkl_04.npy
│   │           │   │   │   ├── joblib_0.9.2_pickle_py34_np19.pkl
│   │           │   │   │   ├── joblib_0.9.2_pickle_py34_np19.pkl_01.npy
│   │           │   │   │   ├── joblib_0.9.2_pickle_py34_np19.pkl_02.npy
│   │           │   │   │   ├── joblib_0.9.2_pickle_py34_np19.pkl_03.npy
│   │           │   │   │   ├── joblib_0.9.2_pickle_py34_np19.pkl_04.npy
│   │           │   │   │   ├── joblib_0.9.2_pickle_py35_np19.pkl
│   │           │   │   │   ├── joblib_0.9.2_pickle_py35_np19.pkl_01.npy
│   │           │   │   │   ├── joblib_0.9.2_pickle_py35_np19.pkl_02.npy
│   │           │   │   │   ├── joblib_0.9.2_pickle_py35_np19.pkl_03.npy
│   │           │   │   │   ├── joblib_0.9.2_pickle_py35_np19.pkl_04.npy
│   │           │   │   │   ├── joblib_0.9.4.dev0_compressed_cache_size_pickle_py35_np19.gz
│   │           │   │   │   ├── joblib_0.9.4.dev0_compressed_cache_size_pickle_py35_np19.gz_01.npy.z
│   │           │   │   │   ├── joblib_0.9.4.dev0_compressed_cache_size_pickle_py35_np19.gz_02.npy.z
│   │           │   │   │   └── joblib_0.9.4.dev0_compressed_cache_size_pickle_py35_np19.gz_03.npy.z
│   │           │   │   ├── test_backports.py
│   │           │   │   ├── test_cloudpickle_wrapper.py
│   │           │   │   ├── test_config.py
│   │           │   │   ├── test_dask.py
│   │           │   │   ├── test_disk.py
│   │           │   │   ├── test_func_inspect.py
│   │           │   │   ├── test_func_inspect_special_encoding.py
│   │           │   │   ├── test_hashing.py
│   │           │   │   ├── test_init.py
│   │           │   │   ├── test_logger.py
│   │           │   │   ├── test_memmapping.py
│   │           │   │   ├── test_memory.py
│   │           │   │   ├── test_memory_async.py
│   │           │   │   ├── test_missing_multiprocessing.py
│   │           │   │   ├── test_module.py
│   │           │   │   ├── test_numpy_pickle.py
│   │           │   │   ├── test_numpy_pickle_compat.py
│   │           │   │   ├── test_numpy_pickle_utils.py
│   │           │   │   ├── test_parallel.py
│   │           │   │   ├── test_store_backends.py
│   │           │   │   ├── test_testing.py
│   │           │   │   ├── test_utils.py
│   │           │   │   └── testutils.py
│   │           │   └── testing.py
│   │           ├── joblib-1.4.2.dist-info
│   │           │   ├── INSTALLER
│   │           │   ├── LICENSE.txt
│   │           │   ├── METADATA
│   │           │   ├── RECORD
│   │           │   ├── REQUESTED
│   │           │   ├── WHEEL
│   │           │   └── top_level.txt
│   │           ├── klepto
│   │           │   ├── __info__.py
│   │           │   ├── __init__.py
│   │           │   ├── _abc.py
│   │           │   ├── _archives.py
│   │           │   ├── _cache.py
│   │           │   ├── _inspect.py
│   │           │   ├── _pickle.py
│   │           │   ├── archives.py
│   │           │   ├── crypto.py
│   │           │   ├── keymaps.py
│   │           │   ├── rounding.py
│   │           │   ├── safe.py
│   │           │   ├── tests
│   │           │   │   ├── __init__.py
│   │           │   │   ├── __main__.py
│   │           │   │   ├── cleanup_basic.py
│   │           │   │   ├── test_alchemy.py
│   │           │   │   ├── test_basic.py
│   │           │   │   ├── test_bigdata.py
│   │           │   │   ├── test_cache.py
│   │           │   │   ├── test_cache_info.py
│   │           │   │   ├── test_cachekeys.py
│   │           │   │   ├── test_chaining.py
│   │           │   │   ├── test_crypto.py
│   │           │   │   ├── test_frame.py
│   │           │   │   ├── test_hdf.py
│   │           │   │   ├── test_ignore.py
│   │           │   │   ├── test_keymaps.py
│   │           │   │   ├── test_pickles.py
│   │           │   │   ├── test_readwrite.py
│   │           │   │   ├── test_rounding.py
│   │           │   │   ├── test_validate.py
│   │           │   │   └── test_workflow.py
│   │           │   └── tools.py
│   │           ├── klepto-0.2.6.dist-info
│   │           │   ├── INSTALLER
│   │           │   ├── LICENSE
│   │           │   ├── METADATA
│   │           │   ├── RECORD
│   │           │   ├── REQUESTED
│   │           │   ├── WHEEL
│   │           │   └── top_level.txt
│   │           ├── loguru
│   │           │   ├── __init__.py
│   │           │   ├── __init__.pyi
│   │           │   ├── _asyncio_loop.py
│   │           │   ├── _better_exceptions.py
│   │           │   ├── _colorama.py
│   │           │   ├── _colorizer.py
│   │           │   ├── _contextvars.py
│   │           │   ├── _ctime_functions.py
│   │           │   ├── _datetime.py
│   │           │   ├── _defaults.py
│   │           │   ├── _error_interceptor.py
│   │           │   ├── _file_sink.py
│   │           │   ├── _filters.py
│   │           │   ├── _get_frame.py
│   │           │   ├── _handler.py
│   │           │   ├── _locks_machinery.py
│   │           │   ├── _logger.py
│   │           │   ├── _recattrs.py
│   │           │   ├── _simple_sinks.py
│   │           │   ├── _string_parsers.py
│   │           │   └── py.typed
│   │           ├── loguru-0.7.3.dist-info
│   │           │   ├── INSTALLER
│   │           │   ├── METADATA
│   │           │   ├── RECORD
│   │           │   ├── REQUESTED
│   │           │   └── WHEEL
│   │           ├── mypy
│   │           │   ├── __init__.cpython-312-darwin.so
│   │           │   ├── __init__.py
│   │           │   ├── __main__.py
│   │           │   ├── api.cpython-312-darwin.so
│   │           │   ├── api.py
│   │           │   ├── applytype.cpython-312-darwin.so
│   │           │   ├── applytype.py
│   │           │   ├── argmap.cpython-312-darwin.so
│   │           │   ├── argmap.py
│   │           │   ├── binder.cpython-312-darwin.so
│   │           │   ├── binder.py
│   │           │   ├── bogus_type.py
│   │           │   ├── build.cpython-312-darwin.so
│   │           │   ├── build.py
│   │           │   ├── checker.cpython-312-darwin.so
│   │           │   ├── checker.py
│   │           │   ├── checkexpr.cpython-312-darwin.so
│   │           │   ├── checkexpr.py
│   │           │   ├── checkmember.cpython-312-darwin.so
│   │           │   ├── checkmember.py
│   │           │   ├── checkpattern.cpython-312-darwin.so
│   │           │   ├── checkpattern.py
│   │           │   ├── checkstrformat.cpython-312-darwin.so
│   │           │   ├── checkstrformat.py
│   │           │   ├── config_parser.cpython-312-darwin.so
│   │           │   ├── config_parser.py
│   │           │   ├── constant_fold.cpython-312-darwin.so
│   │           │   ├── constant_fold.py
│   │           │   ├── constraints.cpython-312-darwin.so
│   │           │   ├── constraints.py
│   │           │   ├── copytype.cpython-312-darwin.so
│   │           │   ├── copytype.py
│   │           │   ├── defaults.cpython-312-darwin.so
│   │           │   ├── defaults.py
│   │           │   ├── dmypy
│   │           │   │   ├── __init__.cpython-312-darwin.so
│   │           │   │   ├── __init__.py
│   │           │   │   ├── __main__.py
│   │           │   │   ├── client.cpython-312-darwin.so
│   │           │   │   └── client.py
│   │           │   ├── dmypy_os.cpython-312-darwin.so
│   │           │   ├── dmypy_os.py
│   │           │   ├── dmypy_server.cpython-312-darwin.so
│   │           │   ├── dmypy_server.py
│   │           │   ├── dmypy_util.cpython-312-darwin.so
│   │           │   ├── dmypy_util.py
│   │           │   ├── erasetype.cpython-312-darwin.so
│   │           │   ├── erasetype.py
│   │           │   ├── error_formatter.cpython-312-darwin.so
│   │           │   ├── error_formatter.py
│   │           │   ├── errorcodes.cpython-312-darwin.so
│   │           │   ├── errorcodes.py
│   │           │   ├── errors.cpython-312-darwin.so
│   │           │   ├── errors.py
│   │           │   ├── evalexpr.cpython-312-darwin.so
│   │           │   ├── evalexpr.py
│   │           │   ├── expandtype.cpython-312-darwin.so
│   │           │   ├── expandtype.py
│   │           │   ├── exprtotype.cpython-312-darwin.so
│   │           │   ├── exprtotype.py
│   │           │   ├── fastparse.cpython-312-darwin.so
│   │           │   ├── fastparse.py
│   │           │   ├── find_sources.cpython-312-darwin.so
│   │           │   ├── find_sources.py
│   │           │   ├── fixup.cpython-312-darwin.so
│   │           │   ├── fixup.py
│   │           │   ├── freetree.cpython-312-darwin.so
│   │           │   ├── freetree.py
│   │           │   ├── fscache.cpython-312-darwin.so
│   │           │   ├── fscache.py
│   │           │   ├── fswatcher.cpython-312-darwin.so
│   │           │   ├── fswatcher.py
│   │           │   ├── gclogger.cpython-312-darwin.so
│   │           │   ├── gclogger.py
│   │           │   ├── git.cpython-312-darwin.so
│   │           │   ├── git.py
│   │           │   ├── graph_utils.cpython-312-darwin.so
│   │           │   ├── graph_utils.py
│   │           │   ├── indirection.cpython-312-darwin.so
│   │           │   ├── indirection.py
│   │           │   ├── infer.cpython-312-darwin.so
│   │           │   ├── infer.py
│   │           │   ├── inspections.cpython-312-darwin.so
│   │           │   ├── inspections.py
│   │           │   ├── ipc.cpython-312-darwin.so
│   │           │   ├── ipc.py
│   │           │   ├── join.cpython-312-darwin.so
│   │           │   ├── join.py
│   │           │   ├── literals.cpython-312-darwin.so
│   │           │   ├── literals.py
│   │           │   ├── lookup.cpython-312-darwin.so
│   │           │   ├── lookup.py
│   │           │   ├── main.cpython-312-darwin.so
│   │           │   ├── main.py
│   │           │   ├── maptype.cpython-312-darwin.so
│   │           │   ├── maptype.py
│   │           │   ├── meet.cpython-312-darwin.so
│   │           │   ├── meet.py
│   │           │   ├── memprofile.cpython-312-darwin.so
│   │           │   ├── memprofile.py
│   │           │   ├── message_registry.cpython-312-darwin.so
│   │           │   ├── message_registry.py
│   │           │   ├── messages.cpython-312-darwin.so
│   │           │   ├── messages.py
│   │           │   ├── metastore.cpython-312-darwin.so
│   │           │   ├── metastore.py
│   │           │   ├── mixedtraverser.cpython-312-darwin.so
│   │           │   ├── mixedtraverser.py
│   │           │   ├── modulefinder.cpython-312-darwin.so
│   │           │   ├── modulefinder.py
│   │           │   ├── moduleinspect.cpython-312-darwin.so
│   │           │   ├── moduleinspect.py
│   │           │   ├── mro.cpython-312-darwin.so
│   │           │   ├── mro.py
│   │           │   ├── nodes.cpython-312-darwin.so
│   │           │   ├── nodes.py
│   │           │   ├── operators.cpython-312-darwin.so
│   │           │   ├── operators.py
│   │           │   ├── options.cpython-312-darwin.so
│   │           │   ├── options.py
│   │           │   ├── parse.cpython-312-darwin.so
│   │           │   ├── parse.py
│   │           │   ├── partially_defined.cpython-312-darwin.so
│   │           │   ├── partially_defined.py
│   │           │   ├── patterns.cpython-312-darwin.so
│   │           │   ├── patterns.py
│   │           │   ├── plugin.cpython-312-darwin.so
│   │           │   ├── plugin.py
│   │           │   ├── plugins
│   │           │   │   ├── __init__.cpython-312-darwin.so
│   │           │   │   ├── __init__.py
│   │           │   │   ├── attrs.cpython-312-darwin.so
│   │           │   │   ├── attrs.py
│   │           │   │   ├── common.cpython-312-darwin.so
│   │           │   │   ├── common.py
│   │           │   │   ├── ctypes.cpython-312-darwin.so
│   │           │   │   ├── ctypes.py
│   │           │   │   ├── dataclasses.cpython-312-darwin.so
│   │           │   │   ├── dataclasses.py
│   │           │   │   ├── default.cpython-312-darwin.so
│   │           │   │   ├── default.py
│   │           │   │   ├── enums.cpython-312-darwin.so
│   │           │   │   ├── enums.py
│   │           │   │   ├── functools.cpython-312-darwin.so
│   │           │   │   ├── functools.py
│   │           │   │   ├── proper_plugin.cpython-312-darwin.so
│   │           │   │   ├── proper_plugin.py
│   │           │   │   ├── singledispatch.cpython-312-darwin.so
│   │           │   │   └── singledispatch.py
│   │           │   ├── py.typed
│   │           │   ├── pyinfo.py
│   │           │   ├── reachability.cpython-312-darwin.so
│   │           │   ├── reachability.py
│   │           │   ├── refinfo.cpython-312-darwin.so
│   │           │   ├── refinfo.py
│   │           │   ├── renaming.cpython-312-darwin.so
│   │           │   ├── renaming.py
│   │           │   ├── report.cpython-312-darwin.so
│   │           │   ├── report.py
│   │           │   ├── scope.cpython-312-darwin.so
│   │           │   ├── scope.py
│   │           │   ├── semanal.cpython-312-darwin.so
│   │           │   ├── semanal.py
│   │           │   ├── semanal_classprop.cpython-312-darwin.so
│   │           │   ├── semanal_classprop.py
│   │           │   ├── semanal_enum.cpython-312-darwin.so
│   │           │   ├── semanal_enum.py
│   │           │   ├── semanal_infer.cpython-312-darwin.so
│   │           │   ├── semanal_infer.py
│   │           │   ├── semanal_main.cpython-312-darwin.so
│   │           │   ├── semanal_main.py
│   │           │   ├── semanal_namedtuple.cpython-312-darwin.so
│   │           │   ├── semanal_namedtuple.py
│   │           │   ├── semanal_newtype.cpython-312-darwin.so
│   │           │   ├── semanal_newtype.py
│   │           │   ├── semanal_pass1.cpython-312-darwin.so
│   │           │   ├── semanal_pass1.py
│   │           │   ├── semanal_shared.cpython-312-darwin.so
│   │           │   ├── semanal_shared.py
│   │           │   ├── semanal_typeargs.cpython-312-darwin.so
│   │           │   ├── semanal_typeargs.py
│   │           │   ├── semanal_typeddict.cpython-312-darwin.so
│   │           │   ├── semanal_typeddict.py
│   │           │   ├── server
│   │           │   │   ├── __init__.cpython-312-darwin.so
│   │           │   │   ├── __init__.py
│   │           │   │   ├── astdiff.cpython-312-darwin.so
│   │           │   │   ├── astdiff.py
│   │           │   │   ├── astmerge.cpython-312-darwin.so
│   │           │   │   ├── astmerge.py
│   │           │   │   ├── aststrip.cpython-312-darwin.so
│   │           │   │   ├── aststrip.py
│   │           │   │   ├── deps.cpython-312-darwin.so
│   │           │   │   ├── deps.py
│   │           │   │   ├── mergecheck.cpython-312-darwin.so
│   │           │   │   ├── mergecheck.py
│   │           │   │   ├── objgraph.cpython-312-darwin.so
│   │           │   │   ├── objgraph.py
│   │           │   │   ├── subexpr.cpython-312-darwin.so
│   │           │   │   ├── subexpr.py
│   │           │   │   ├── target.cpython-312-darwin.so
│   │           │   │   ├── target.py
│   │           │   │   ├── trigger.cpython-312-darwin.so
│   │           │   │   ├── trigger.py
│   │           │   │   ├── update.cpython-312-darwin.so
│   │           │   │   └── update.py
│   │           │   ├── sharedparse.cpython-312-darwin.so
│   │           │   ├── sharedparse.py
│   │           │   ├── solve.cpython-312-darwin.so
│   │           │   ├── solve.py
│   │           │   ├── split_namespace.py
│   │           │   ├── state.cpython-312-darwin.so
│   │           │   ├── state.py
│   │           │   ├── stats.cpython-312-darwin.so
│   │           │   ├── stats.py
│   │           │   ├── strconv.cpython-312-darwin.so
│   │           │   ├── strconv.py
│   │           │   ├── stubdoc.py
│   │           │   ├── stubgen.cpython-312-darwin.so
│   │           │   ├── stubgen.py
│   │           │   ├── stubgenc.py
│   │           │   ├── stubinfo.cpython-312-darwin.so
│   │           │   ├── stubinfo.py
│   │           │   ├── stubtest.py
│   │           │   ├── stubutil.cpython-312-darwin.so
│   │           │   ├── stubutil.py
│   │           │   ├── subtypes.cpython-312-darwin.so
│   │           │   ├── subtypes.py
│   │           │   ├── suggestions.cpython-312-darwin.so
│   │           │   ├── suggestions.py
│   │           │   ├── test
│   │           │   │   ├── __init__.py
│   │           │   │   ├── config.py
│   │           │   │   ├── data.py
│   │           │   │   ├── helpers.py
│   │           │   │   ├── meta
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   ├── _pytest.py
│   │           │   │   │   ├── test_diff_helper.py
│   │           │   │   │   ├── test_parse_data.py
│   │           │   │   │   └── test_update_data.py
│   │           │   │   ├── test_config_parser.py
│   │           │   │   ├── test_find_sources.py
│   │           │   │   ├── test_ref_info.py
│   │           │   │   ├── testapi.py
│   │           │   │   ├── testargs.py
│   │           │   │   ├── testcheck.py
│   │           │   │   ├── testcmdline.py
│   │           │   │   ├── testconstraints.py
│   │           │   │   ├── testdaemon.py
│   │           │   │   ├── testdeps.py
│   │           │   │   ├── testdiff.py
│   │           │   │   ├── testerrorstream.py
│   │           │   │   ├── testfinegrained.py
│   │           │   │   ├── testfinegrainedcache.py
│   │           │   │   ├── testformatter.py
│   │           │   │   ├── testfscache.py
│   │           │   │   ├── testgraph.py
│   │           │   │   ├── testinfer.py
│   │           │   │   ├── testipc.py
│   │           │   │   ├── testmerge.py
│   │           │   │   ├── testmodulefinder.py
│   │           │   │   ├── testmypyc.py
│   │           │   │   ├── testoutput.py
│   │           │   │   ├── testparse.py
│   │           │   │   ├── testpep561.py
│   │           │   │   ├── testpythoneval.py
│   │           │   │   ├── testreports.py
│   │           │   │   ├── testsemanal.py
│   │           │   │   ├── testsolve.py
│   │           │   │   ├── teststubgen.py
│   │           │   │   ├── teststubinfo.py
│   │           │   │   ├── teststubtest.py
│   │           │   │   ├── testsubtypes.py
│   │           │   │   ├── testtransform.py
│   │           │   │   ├── testtypegen.py
│   │           │   │   ├── testtypes.py
│   │           │   │   ├── testutil.py
│   │           │   │   ├── typefixture.py
│   │           │   │   ├── update_data.py
│   │           │   │   ├── visitors.cpython-312-darwin.so
│   │           │   │   └── visitors.py
│   │           │   ├── traverser.cpython-312-darwin.so
│   │           │   ├── traverser.py
│   │           │   ├── treetransform.cpython-312-darwin.so
│   │           │   ├── treetransform.py
│   │           │   ├── tvar_scope.cpython-312-darwin.so
│   │           │   ├── tvar_scope.py
│   │           │   ├── type_visitor.cpython-312-darwin.so
│   │           │   ├── type_visitor.py
│   │           │   ├── typeanal.cpython-312-darwin.so
│   │           │   ├── typeanal.py
│   │           │   ├── typeops.cpython-312-darwin.so
│   │           │   ├── typeops.py
│   │           │   ├── types.cpython-312-darwin.so
│   │           │   ├── types.py
│   │           │   ├── types_utils.cpython-312-darwin.so
│   │           │   ├── types_utils.py
│   │           │   ├── typeshed
│   │           │   │   ├── LICENSE
│   │           │   │   ├── stdlib
│   │           │   │   │   ├── VERSIONS
│   │           │   │   │   ├── __future__.pyi
│   │           │   │   │   ├── __main__.pyi
│   │           │   │   │   ├── _ast.pyi
│   │           │   │   │   ├── _asyncio.pyi
│   │           │   │   │   ├── _bisect.pyi
│   │           │   │   │   ├── _blake2.pyi
│   │           │   │   │   ├── _bootlocale.pyi
│   │           │   │   │   ├── _bz2.pyi
│   │           │   │   │   ├── _codecs.pyi
│   │           │   │   │   ├── _collections_abc.pyi
│   │           │   │   │   ├── _compat_pickle.pyi
│   │           │   │   │   ├── _compression.pyi
│   │           │   │   │   ├── _contextvars.pyi
│   │           │   │   │   ├── _csv.pyi
│   │           │   │   │   ├── _ctypes.pyi
│   │           │   │   │   ├── _curses.pyi
│   │           │   │   │   ├── _curses_panel.pyi
│   │           │   │   │   ├── _dbm.pyi
│   │           │   │   │   ├── _decimal.pyi
│   │           │   │   │   ├── _dummy_thread.pyi
│   │           │   │   │   ├── _dummy_threading.pyi
│   │           │   │   │   ├── _frozen_importlib.pyi
│   │           │   │   │   ├── _frozen_importlib_external.pyi
│   │           │   │   │   ├── _gdbm.pyi
│   │           │   │   │   ├── _hashlib.pyi
│   │           │   │   │   ├── _heapq.pyi
│   │           │   │   │   ├── _imp.pyi
│   │           │   │   │   ├── _interpchannels.pyi
│   │           │   │   │   ├── _interpqueues.pyi
│   │           │   │   │   ├── _interpreters.pyi
│   │           │   │   │   ├── _io.pyi
│   │           │   │   │   ├── _json.pyi
│   │           │   │   │   ├── _locale.pyi
│   │           │   │   │   ├── _lsprof.pyi
│   │           │   │   │   ├── _lzma.pyi
│   │           │   │   │   ├── _markupbase.pyi
│   │           │   │   │   ├── _msi.pyi
│   │           │   │   │   ├── _multibytecodec.pyi
│   │           │   │   │   ├── _operator.pyi
│   │           │   │   │   ├── _osx_support.pyi
│   │           │   │   │   ├── _pickle.pyi
│   │           │   │   │   ├── _posixsubprocess.pyi
│   │           │   │   │   ├── _py_abc.pyi
│   │           │   │   │   ├── _pydecimal.pyi
│   │           │   │   │   ├── _queue.pyi
│   │           │   │   │   ├── _random.pyi
│   │           │   │   │   ├── _sitebuiltins.pyi
│   │           │   │   │   ├── _socket.pyi
│   │           │   │   │   ├── _sqlite3.pyi
│   │           │   │   │   ├── _ssl.pyi
│   │           │   │   │   ├── _stat.pyi
│   │           │   │   │   ├── _struct.pyi
│   │           │   │   │   ├── _thread.pyi
│   │           │   │   │   ├── _threading_local.pyi
│   │           │   │   │   ├── _tkinter.pyi
│   │           │   │   │   ├── _tracemalloc.pyi
│   │           │   │   │   ├── _typeshed
│   │           │   │   │   │   ├── __init__.pyi
│   │           │   │   │   │   ├── dbapi.pyi
│   │           │   │   │   │   ├── importlib.pyi
│   │           │   │   │   │   ├── wsgi.pyi
│   │           │   │   │   │   └── xml.pyi
│   │           │   │   │   ├── _warnings.pyi
│   │           │   │   │   ├── _weakref.pyi
│   │           │   │   │   ├── _weakrefset.pyi
│   │           │   │   │   ├── _winapi.pyi
│   │           │   │   │   ├── abc.pyi
│   │           │   │   │   ├── aifc.pyi
│   │           │   │   │   ├── antigravity.pyi
│   │           │   │   │   ├── argparse.pyi
│   │           │   │   │   ├── array.pyi
│   │           │   │   │   ├── ast.pyi
│   │           │   │   │   ├── asynchat.pyi
│   │           │   │   │   ├── asyncio
│   │           │   │   │   │   ├── __init__.pyi
│   │           │   │   │   │   ├── base_events.pyi
│   │           │   │   │   │   ├── base_futures.pyi
│   │           │   │   │   │   ├── base_subprocess.pyi
│   │           │   │   │   │   ├── base_tasks.pyi
│   │           │   │   │   │   ├── constants.pyi
│   │           │   │   │   │   ├── coroutines.pyi
│   │           │   │   │   │   ├── events.pyi
│   │           │   │   │   │   ├── exceptions.pyi
│   │           │   │   │   │   ├── format_helpers.pyi
│   │           │   │   │   │   ├── futures.pyi
│   │           │   │   │   │   ├── locks.pyi
│   │           │   │   │   │   ├── log.pyi
│   │           │   │   │   │   ├── mixins.pyi
│   │           │   │   │   │   ├── proactor_events.pyi
│   │           │   │   │   │   ├── protocols.pyi
│   │           │   │   │   │   ├── queues.pyi
│   │           │   │   │   │   ├── runners.pyi
│   │           │   │   │   │   ├── selector_events.pyi
│   │           │   │   │   │   ├── sslproto.pyi
│   │           │   │   │   │   ├── staggered.pyi
│   │           │   │   │   │   ├── streams.pyi
│   │           │   │   │   │   ├── subprocess.pyi
│   │           │   │   │   │   ├── taskgroups.pyi
│   │           │   │   │   │   ├── tasks.pyi
│   │           │   │   │   │   ├── threads.pyi
│   │           │   │   │   │   ├── timeouts.pyi
│   │           │   │   │   │   ├── transports.pyi
│   │           │   │   │   │   ├── trsock.pyi
│   │           │   │   │   │   ├── unix_events.pyi
│   │           │   │   │   │   ├── windows_events.pyi
│   │           │   │   │   │   └── windows_utils.pyi
│   │           │   │   │   ├── asyncore.pyi
│   │           │   │   │   ├── atexit.pyi
│   │           │   │   │   ├── audioop.pyi
│   │           │   │   │   ├── base64.pyi
│   │           │   │   │   ├── bdb.pyi
│   │           │   │   │   ├── binascii.pyi
│   │           │   │   │   ├── binhex.pyi
│   │           │   │   │   ├── bisect.pyi
│   │           │   │   │   ├── builtins.pyi
│   │           │   │   │   ├── bz2.pyi
│   │           │   │   │   ├── cProfile.pyi
│   │           │   │   │   ├── calendar.pyi
│   │           │   │   │   ├── cgi.pyi
│   │           │   │   │   ├── cgitb.pyi
│   │           │   │   │   ├── chunk.pyi
│   │           │   │   │   ├── cmath.pyi
│   │           │   │   │   ├── cmd.pyi
│   │           │   │   │   ├── code.pyi
│   │           │   │   │   ├── codecs.pyi
│   │           │   │   │   ├── codeop.pyi
│   │           │   │   │   ├── collections
│   │           │   │   │   │   ├── __init__.pyi
│   │           │   │   │   │   └── abc.pyi
│   │           │   │   │   ├── colorsys.pyi
│   │           │   │   │   ├── compileall.pyi
│   │           │   │   │   ├── concurrent
│   │           │   │   │   │   ├── __init__.pyi
│   │           │   │   │   │   └── futures
│   │           │   │   │   │       ├── __init__.pyi
│   │           │   │   │   │       ├── _base.pyi
│   │           │   │   │   │       ├── process.pyi
│   │           │   │   │   │       └── thread.pyi
│   │           │   │   │   ├── configparser.pyi
│   │           │   │   │   ├── contextlib.pyi
│   │           │   │   │   ├── contextvars.pyi
│   │           │   │   │   ├── copy.pyi
│   │           │   │   │   ├── copyreg.pyi
│   │           │   │   │   ├── crypt.pyi
│   │           │   │   │   ├── csv.pyi
│   │           │   │   │   ├── ctypes
│   │           │   │   │   │   ├── __init__.pyi
│   │           │   │   │   │   ├── _endian.pyi
│   │           │   │   │   │   ├── macholib
│   │           │   │   │   │   │   ├── __init__.pyi
│   │           │   │   │   │   │   ├── dyld.pyi
│   │           │   │   │   │   │   ├── dylib.pyi
│   │           │   │   │   │   │   └── framework.pyi
│   │           │   │   │   │   ├── util.pyi
│   │           │   │   │   │   └── wintypes.pyi
│   │           │   │   │   ├── curses
│   │           │   │   │   │   ├── __init__.pyi
│   │           │   │   │   │   ├── ascii.pyi
│   │           │   │   │   │   ├── has_key.pyi
│   │           │   │   │   │   ├── panel.pyi
│   │           │   │   │   │   └── textpad.pyi
│   │           │   │   │   ├── dataclasses.pyi
│   │           │   │   │   ├── datetime.pyi
│   │           │   │   │   ├── dbm
│   │           │   │   │   │   ├── __init__.pyi
│   │           │   │   │   │   ├── dumb.pyi
│   │           │   │   │   │   ├── gnu.pyi
│   │           │   │   │   │   ├── ndbm.pyi
│   │           │   │   │   │   └── sqlite3.pyi
│   │           │   │   │   ├── decimal.pyi
│   │           │   │   │   ├── difflib.pyi
│   │           │   │   │   ├── dis.pyi
│   │           │   │   │   ├── distutils
│   │           │   │   │   │   ├── __init__.pyi
│   │           │   │   │   │   ├── _msvccompiler.pyi
│   │           │   │   │   │   ├── archive_util.pyi
│   │           │   │   │   │   ├── bcppcompiler.pyi
│   │           │   │   │   │   ├── ccompiler.pyi
│   │           │   │   │   │   ├── cmd.pyi
│   │           │   │   │   │   ├── command
│   │           │   │   │   │   │   ├── __init__.pyi
│   │           │   │   │   │   │   ├── bdist.pyi
│   │           │   │   │   │   │   ├── bdist_dumb.pyi
│   │           │   │   │   │   │   ├── bdist_msi.pyi
│   │           │   │   │   │   │   ├── bdist_packager.pyi
│   │           │   │   │   │   │   ├── bdist_rpm.pyi
│   │           │   │   │   │   │   ├── bdist_wininst.pyi
│   │           │   │   │   │   │   ├── build.pyi
│   │           │   │   │   │   │   ├── build_clib.pyi
│   │           │   │   │   │   │   ├── build_ext.pyi
│   │           │   │   │   │   │   ├── build_py.pyi
│   │           │   │   │   │   │   ├── build_scripts.pyi
│   │           │   │   │   │   │   ├── check.pyi
│   │           │   │   │   │   │   ├── clean.pyi
│   │           │   │   │   │   │   ├── config.pyi
│   │           │   │   │   │   │   ├── install.pyi
│   │           │   │   │   │   │   ├── install_data.pyi
│   │           │   │   │   │   │   ├── install_egg_info.pyi
│   │           │   │   │   │   │   ├── install_headers.pyi
│   │           │   │   │   │   │   ├── install_lib.pyi
│   │           │   │   │   │   │   ├── install_scripts.pyi
│   │           │   │   │   │   │   ├── register.pyi
│   │           │   │   │   │   │   ├── sdist.pyi
│   │           │   │   │   │   │   └── upload.pyi
│   │           │   │   │   │   ├── config.pyi
│   │           │   │   │   │   ├── core.pyi
│   │           │   │   │   │   ├── cygwinccompiler.pyi
│   │           │   │   │   │   ├── debug.pyi
│   │           │   │   │   │   ├── dep_util.pyi
│   │           │   │   │   │   ├── dir_util.pyi
│   │           │   │   │   │   ├── dist.pyi
│   │           │   │   │   │   ├── errors.pyi
│   │           │   │   │   │   ├── extension.pyi
│   │           │   │   │   │   ├── fancy_getopt.pyi
│   │           │   │   │   │   ├── file_util.pyi
│   │           │   │   │   │   ├── filelist.pyi
│   │           │   │   │   │   ├── log.pyi
│   │           │   │   │   │   ├── msvccompiler.pyi
│   │           │   │   │   │   ├── spawn.pyi
│   │           │   │   │   │   ├── sysconfig.pyi
│   │           │   │   │   │   ├── text_file.pyi
│   │           │   │   │   │   ├── unixccompiler.pyi
│   │           │   │   │   │   ├── util.pyi
│   │           │   │   │   │   └── version.pyi
│   │           │   │   │   ├── doctest.pyi
│   │           │   │   │   ├── dummy_threading.pyi
│   │           │   │   │   ├── email
│   │           │   │   │   │   ├── __init__.pyi
│   │           │   │   │   │   ├── _header_value_parser.pyi
│   │           │   │   │   │   ├── _policybase.pyi
│   │           │   │   │   │   ├── base64mime.pyi
│   │           │   │   │   │   ├── charset.pyi
│   │           │   │   │   │   ├── contentmanager.pyi
│   │           │   │   │   │   ├── encoders.pyi
│   │           │   │   │   │   ├── errors.pyi
│   │           │   │   │   │   ├── feedparser.pyi
│   │           │   │   │   │   ├── generator.pyi
│   │           │   │   │   │   ├── header.pyi
│   │           │   │   │   │   ├── headerregistry.pyi
│   │           │   │   │   │   ├── iterators.pyi
│   │           │   │   │   │   ├── message.pyi
│   │           │   │   │   │   ├── mime
│   │           │   │   │   │   │   ├── __init__.pyi
│   │           │   │   │   │   │   ├── application.pyi
│   │           │   │   │   │   │   ├── audio.pyi
│   │           │   │   │   │   │   ├── base.pyi
│   │           │   │   │   │   │   ├── image.pyi
│   │           │   │   │   │   │   ├── message.pyi
│   │           │   │   │   │   │   ├── multipart.pyi
│   │           │   │   │   │   │   ├── nonmultipart.pyi
│   │           │   │   │   │   │   └── text.pyi
│   │           │   │   │   │   ├── parser.pyi
│   │           │   │   │   │   ├── policy.pyi
│   │           │   │   │   │   ├── quoprimime.pyi
│   │           │   │   │   │   └── utils.pyi
│   │           │   │   │   ├── encodings
│   │           │   │   │   │   ├── __init__.pyi
│   │           │   │   │   │   ├── aliases.pyi
│   │           │   │   │   │   ├── ascii.pyi
│   │           │   │   │   │   ├── base64_codec.pyi
│   │           │   │   │   │   ├── big5.pyi
│   │           │   │   │   │   ├── big5hkscs.pyi
│   │           │   │   │   │   ├── bz2_codec.pyi
│   │           │   │   │   │   ├── charmap.pyi
│   │           │   │   │   │   ├── cp037.pyi
│   │           │   │   │   │   ├── cp1006.pyi
│   │           │   │   │   │   ├── cp1026.pyi
│   │           │   │   │   │   ├── cp1125.pyi
│   │           │   │   │   │   ├── cp1140.pyi
│   │           │   │   │   │   ├── cp1250.pyi
│   │           │   │   │   │   ├── cp1251.pyi
│   │           │   │   │   │   ├── cp1252.pyi
│   │           │   │   │   │   ├── cp1253.pyi
│   │           │   │   │   │   ├── cp1254.pyi
│   │           │   │   │   │   ├── cp1255.pyi
│   │           │   │   │   │   ├── cp1256.pyi
│   │           │   │   │   │   ├── cp1257.pyi
│   │           │   │   │   │   ├── cp1258.pyi
│   │           │   │   │   │   ├── cp273.pyi
│   │           │   │   │   │   ├── cp424.pyi
│   │           │   │   │   │   ├── cp437.pyi
│   │           │   │   │   │   ├── cp500.pyi
│   │           │   │   │   │   ├── cp720.pyi
│   │           │   │   │   │   ├── cp737.pyi
│   │           │   │   │   │   ├── cp775.pyi
│   │           │   │   │   │   ├── cp850.pyi
│   │           │   │   │   │   ├── cp852.pyi
│   │           │   │   │   │   ├── cp855.pyi
│   │           │   │   │   │   ├── cp856.pyi
│   │           │   │   │   │   ├── cp857.pyi
│   │           │   │   │   │   ├── cp858.pyi
│   │           │   │   │   │   ├── cp860.pyi
│   │           │   │   │   │   ├── cp861.pyi
│   │           │   │   │   │   ├── cp862.pyi
│   │           │   │   │   │   ├── cp863.pyi
│   │           │   │   │   │   ├── cp864.pyi
│   │           │   │   │   │   ├── cp865.pyi
│   │           │   │   │   │   ├── cp866.pyi
│   │           │   │   │   │   ├── cp869.pyi
│   │           │   │   │   │   ├── cp874.pyi
│   │           │   │   │   │   ├── cp875.pyi
│   │           │   │   │   │   ├── cp932.pyi
│   │           │   │   │   │   ├── cp949.pyi
│   │           │   │   │   │   ├── cp950.pyi
│   │           │   │   │   │   ├── euc_jis_2004.pyi
│   │           │   │   │   │   ├── euc_jisx0213.pyi
│   │           │   │   │   │   ├── euc_jp.pyi
│   │           │   │   │   │   ├── euc_kr.pyi
│   │           │   │   │   │   ├── gb18030.pyi
│   │           │   │   │   │   ├── gb2312.pyi
│   │           │   │   │   │   ├── gbk.pyi
│   │           │   │   │   │   ├── hex_codec.pyi
│   │           │   │   │   │   ├── hp_roman8.pyi
│   │           │   │   │   │   ├── hz.pyi
│   │           │   │   │   │   ├── idna.pyi
│   │           │   │   │   │   ├── iso2022_jp.pyi
│   │           │   │   │   │   ├── iso2022_jp_1.pyi
│   │           │   │   │   │   ├── iso2022_jp_2.pyi
│   │           │   │   │   │   ├── iso2022_jp_2004.pyi
│   │           │   │   │   │   ├── iso2022_jp_3.pyi
│   │           │   │   │   │   ├── iso2022_jp_ext.pyi
│   │           │   │   │   │   ├── iso2022_kr.pyi
│   │           │   │   │   │   ├── iso8859_1.pyi
│   │           │   │   │   │   ├── iso8859_10.pyi
│   │           │   │   │   │   ├── iso8859_11.pyi
│   │           │   │   │   │   ├── iso8859_13.pyi
│   │           │   │   │   │   ├── iso8859_14.pyi
│   │           │   │   │   │   ├── iso8859_15.pyi
│   │           │   │   │   │   ├── iso8859_16.pyi
│   │           │   │   │   │   ├── iso8859_2.pyi
│   │           │   │   │   │   ├── iso8859_3.pyi
│   │           │   │   │   │   ├── iso8859_4.pyi
│   │           │   │   │   │   ├── iso8859_5.pyi
│   │           │   │   │   │   ├── iso8859_6.pyi
│   │           │   │   │   │   ├── iso8859_7.pyi
│   │           │   │   │   │   ├── iso8859_8.pyi
│   │           │   │   │   │   ├── iso8859_9.pyi
│   │           │   │   │   │   ├── johab.pyi
│   │           │   │   │   │   ├── koi8_r.pyi
│   │           │   │   │   │   ├── koi8_t.pyi
│   │           │   │   │   │   ├── koi8_u.pyi
│   │           │   │   │   │   ├── kz1048.pyi
│   │           │   │   │   │   ├── latin_1.pyi
│   │           │   │   │   │   ├── mac_arabic.pyi
│   │           │   │   │   │   ├── mac_centeuro.pyi
│   │           │   │   │   │   ├── mac_croatian.pyi
│   │           │   │   │   │   ├── mac_cyrillic.pyi
│   │           │   │   │   │   ├── mac_farsi.pyi
│   │           │   │   │   │   ├── mac_greek.pyi
│   │           │   │   │   │   ├── mac_iceland.pyi
│   │           │   │   │   │   ├── mac_latin2.pyi
│   │           │   │   │   │   ├── mac_roman.pyi
│   │           │   │   │   │   ├── mac_romanian.pyi
│   │           │   │   │   │   ├── mac_turkish.pyi
│   │           │   │   │   │   ├── mbcs.pyi
│   │           │   │   │   │   ├── oem.pyi
│   │           │   │   │   │   ├── palmos.pyi
│   │           │   │   │   │   ├── ptcp154.pyi
│   │           │   │   │   │   ├── punycode.pyi
│   │           │   │   │   │   ├── quopri_codec.pyi
│   │           │   │   │   │   ├── raw_unicode_escape.pyi
│   │           │   │   │   │   ├── rot_13.pyi
│   │           │   │   │   │   ├── shift_jis.pyi
│   │           │   │   │   │   ├── shift_jis_2004.pyi
│   │           │   │   │   │   ├── shift_jisx0213.pyi
│   │           │   │   │   │   ├── tis_620.pyi
│   │           │   │   │   │   ├── undefined.pyi
│   │           │   │   │   │   ├── unicode_escape.pyi
│   │           │   │   │   │   ├── utf_16.pyi
│   │           │   │   │   │   ├── utf_16_be.pyi
│   │           │   │   │   │   ├── utf_16_le.pyi
│   │           │   │   │   │   ├── utf_32.pyi
│   │           │   │   │   │   ├── utf_32_be.pyi
│   │           │   │   │   │   ├── utf_32_le.pyi
│   │           │   │   │   │   ├── utf_7.pyi
│   │           │   │   │   │   ├── utf_8.pyi
│   │           │   │   │   │   ├── utf_8_sig.pyi
│   │           │   │   │   │   ├── uu_codec.pyi
│   │           │   │   │   │   └── zlib_codec.pyi
│   │           │   │   │   ├── ensurepip
│   │           │   │   │   │   └── __init__.pyi
│   │           │   │   │   ├── enum.pyi
│   │           │   │   │   ├── errno.pyi
│   │           │   │   │   ├── faulthandler.pyi
│   │           │   │   │   ├── fcntl.pyi
│   │           │   │   │   ├── filecmp.pyi
│   │           │   │   │   ├── fileinput.pyi
│   │           │   │   │   ├── fnmatch.pyi
│   │           │   │   │   ├── formatter.pyi
│   │           │   │   │   ├── fractions.pyi
│   │           │   │   │   ├── ftplib.pyi
│   │           │   │   │   ├── functools.pyi
│   │           │   │   │   ├── gc.pyi
│   │           │   │   │   ├── genericpath.pyi
│   │           │   │   │   ├── getopt.pyi
│   │           │   │   │   ├── getpass.pyi
│   │           │   │   │   ├── gettext.pyi
│   │           │   │   │   ├── glob.pyi
│   │           │   │   │   ├── graphlib.pyi
│   │           │   │   │   ├── grp.pyi
│   │           │   │   │   ├── gzip.pyi
│   │           │   │   │   ├── hashlib.pyi
│   │           │   │   │   ├── heapq.pyi
│   │           │   │   │   ├── hmac.pyi
│   │           │   │   │   ├── html
│   │           │   │   │   │   ├── __init__.pyi
│   │           │   │   │   │   ├── entities.pyi
│   │           │   │   │   │   └── parser.pyi
│   │           │   │   │   ├── http
│   │           │   │   │   │   ├── __init__.pyi
│   │           │   │   │   │   ├── client.pyi
│   │           │   │   │   │   ├── cookiejar.pyi
│   │           │   │   │   │   ├── cookies.pyi
│   │           │   │   │   │   └── server.pyi
│   │           │   │   │   ├── imaplib.pyi
│   │           │   │   │   ├── imghdr.pyi
│   │           │   │   │   ├── imp.pyi
│   │           │   │   │   ├── importlib
│   │           │   │   │   │   ├── __init__.pyi
│   │           │   │   │   │   ├── _abc.pyi
│   │           │   │   │   │   ├── _bootstrap.pyi
│   │           │   │   │   │   ├── _bootstrap_external.pyi
│   │           │   │   │   │   ├── abc.pyi
│   │           │   │   │   │   ├── machinery.pyi
│   │           │   │   │   │   ├── metadata
│   │           │   │   │   │   │   ├── __init__.pyi
│   │           │   │   │   │   │   ├── _meta.pyi
│   │           │   │   │   │   │   └── diagnose.pyi
│   │           │   │   │   │   ├── readers.pyi
│   │           │   │   │   │   ├── resources
│   │           │   │   │   │   │   ├── __init__.pyi
│   │           │   │   │   │   │   ├── _common.pyi
│   │           │   │   │   │   │   ├── _functional.pyi
│   │           │   │   │   │   │   ├── abc.pyi
│   │           │   │   │   │   │   ├── readers.pyi
│   │           │   │   │   │   │   └── simple.pyi
│   │           │   │   │   │   ├── simple.pyi
│   │           │   │   │   │   └── util.pyi
│   │           │   │   │   ├── inspect.pyi
│   │           │   │   │   ├── io.pyi
│   │           │   │   │   ├── ipaddress.pyi
│   │           │   │   │   ├── itertools.pyi
│   │           │   │   │   ├── json
│   │           │   │   │   │   ├── __init__.pyi
│   │           │   │   │   │   ├── decoder.pyi
│   │           │   │   │   │   ├── encoder.pyi
│   │           │   │   │   │   ├── scanner.pyi
│   │           │   │   │   │   └── tool.pyi
│   │           │   │   │   ├── keyword.pyi
│   │           │   │   │   ├── lib2to3
│   │           │   │   │   │   ├── __init__.pyi
│   │           │   │   │   │   ├── btm_matcher.pyi
│   │           │   │   │   │   ├── fixer_base.pyi
│   │           │   │   │   │   ├── fixes
│   │           │   │   │   │   │   ├── __init__.pyi
│   │           │   │   │   │   │   ├── fix_apply.pyi
│   │           │   │   │   │   │   ├── fix_asserts.pyi
│   │           │   │   │   │   │   ├── fix_basestring.pyi
│   │           │   │   │   │   │   ├── fix_buffer.pyi
│   │           │   │   │   │   │   ├── fix_dict.pyi
│   │           │   │   │   │   │   ├── fix_except.pyi
│   │           │   │   │   │   │   ├── fix_exec.pyi
│   │           │   │   │   │   │   ├── fix_execfile.pyi
│   │           │   │   │   │   │   ├── fix_exitfunc.pyi
│   │           │   │   │   │   │   ├── fix_filter.pyi
│   │           │   │   │   │   │   ├── fix_funcattrs.pyi
│   │           │   │   │   │   │   ├── fix_future.pyi
│   │           │   │   │   │   │   ├── fix_getcwdu.pyi
│   │           │   │   │   │   │   ├── fix_has_key.pyi
│   │           │   │   │   │   │   ├── fix_idioms.pyi
│   │           │   │   │   │   │   ├── fix_import.pyi
│   │           │   │   │   │   │   ├── fix_imports.pyi
│   │           │   │   │   │   │   ├── fix_imports2.pyi
│   │           │   │   │   │   │   ├── fix_input.pyi
│   │           │   │   │   │   │   ├── fix_intern.pyi
│   │           │   │   │   │   │   ├── fix_isinstance.pyi
│   │           │   │   │   │   │   ├── fix_itertools.pyi
│   │           │   │   │   │   │   ├── fix_itertools_imports.pyi
│   │           │   │   │   │   │   ├── fix_long.pyi
│   │           │   │   │   │   │   ├── fix_map.pyi
│   │           │   │   │   │   │   ├── fix_metaclass.pyi
│   │           │   │   │   │   │   ├── fix_methodattrs.pyi
│   │           │   │   │   │   │   ├── fix_ne.pyi
│   │           │   │   │   │   │   ├── fix_next.pyi
│   │           │   │   │   │   │   ├── fix_nonzero.pyi
│   │           │   │   │   │   │   ├── fix_numliterals.pyi
│   │           │   │   │   │   │   ├── fix_operator.pyi
│   │           │   │   │   │   │   ├── fix_paren.pyi
│   │           │   │   │   │   │   ├── fix_print.pyi
│   │           │   │   │   │   │   ├── fix_raise.pyi
│   │           │   │   │   │   │   ├── fix_raw_input.pyi
│   │           │   │   │   │   │   ├── fix_reduce.pyi
│   │           │   │   │   │   │   ├── fix_reload.pyi
│   │           │   │   │   │   │   ├── fix_renames.pyi
│   │           │   │   │   │   │   ├── fix_repr.pyi
│   │           │   │   │   │   │   ├── fix_set_literal.pyi
│   │           │   │   │   │   │   ├── fix_standarderror.pyi
│   │           │   │   │   │   │   ├── fix_sys_exc.pyi
│   │           │   │   │   │   │   ├── fix_throw.pyi
│   │           │   │   │   │   │   ├── fix_tuple_params.pyi
│   │           │   │   │   │   │   ├── fix_types.pyi
│   │           │   │   │   │   │   ├── fix_unicode.pyi
│   │           │   │   │   │   │   ├── fix_urllib.pyi
│   │           │   │   │   │   │   ├── fix_ws_comma.pyi
│   │           │   │   │   │   │   ├── fix_xrange.pyi
│   │           │   │   │   │   │   ├── fix_xreadlines.pyi
│   │           │   │   │   │   │   └── fix_zip.pyi
│   │           │   │   │   │   ├── main.pyi
│   │           │   │   │   │   ├── pgen2
│   │           │   │   │   │   │   ├── __init__.pyi
│   │           │   │   │   │   │   ├── driver.pyi
│   │           │   │   │   │   │   ├── grammar.pyi
│   │           │   │   │   │   │   ├── literals.pyi
│   │           │   │   │   │   │   ├── parse.pyi
│   │           │   │   │   │   │   ├── pgen.pyi
│   │           │   │   │   │   │   ├── token.pyi
│   │           │   │   │   │   │   └── tokenize.pyi
│   │           │   │   │   │   ├── pygram.pyi
│   │           │   │   │   │   ├── pytree.pyi
│   │           │   │   │   │   └── refactor.pyi
│   │           │   │   │   ├── linecache.pyi
│   │           │   │   │   ├── locale.pyi
│   │           │   │   │   ├── logging
│   │           │   │   │   │   ├── __init__.pyi
│   │           │   │   │   │   ├── config.pyi
│   │           │   │   │   │   └── handlers.pyi
│   │           │   │   │   ├── lzma.pyi
│   │           │   │   │   ├── mailbox.pyi
│   │           │   │   │   ├── mailcap.pyi
│   │           │   │   │   ├── marshal.pyi
│   │           │   │   │   ├── math.pyi
│   │           │   │   │   ├── mimetypes.pyi
│   │           │   │   │   ├── mmap.pyi
│   │           │   │   │   ├── modulefinder.pyi
│   │           │   │   │   ├── msilib
│   │           │   │   │   │   ├── __init__.pyi
│   │           │   │   │   │   ├── schema.pyi
│   │           │   │   │   │   ├── sequence.pyi
│   │           │   │   │   │   └── text.pyi
│   │           │   │   │   ├── msvcrt.pyi
│   │           │   │   │   ├── multiprocessing
│   │           │   │   │   │   ├── __init__.pyi
│   │           │   │   │   │   ├── connection.pyi
│   │           │   │   │   │   ├── context.pyi
│   │           │   │   │   │   ├── dummy
│   │           │   │   │   │   │   ├── __init__.pyi
│   │           │   │   │   │   │   └── connection.pyi
│   │           │   │   │   │   ├── forkserver.pyi
│   │           │   │   │   │   ├── heap.pyi
│   │           │   │   │   │   ├── managers.pyi
│   │           │   │   │   │   ├── pool.pyi
│   │           │   │   │   │   ├── popen_fork.pyi
│   │           │   │   │   │   ├── popen_forkserver.pyi
│   │           │   │   │   │   ├── popen_spawn_posix.pyi
│   │           │   │   │   │   ├── popen_spawn_win32.pyi
│   │           │   │   │   │   ├── process.pyi
│   │           │   │   │   │   ├── queues.pyi
│   │           │   │   │   │   ├── reduction.pyi
│   │           │   │   │   │   ├── resource_sharer.pyi
│   │           │   │   │   │   ├── resource_tracker.pyi
│   │           │   │   │   │   ├── shared_memory.pyi
│   │           │   │   │   │   ├── sharedctypes.pyi
│   │           │   │   │   │   ├── spawn.pyi
│   │           │   │   │   │   ├── synchronize.pyi
│   │           │   │   │   │   └── util.pyi
│   │           │   │   │   ├── netrc.pyi
│   │           │   │   │   ├── nis.pyi
│   │           │   │   │   ├── nntplib.pyi
│   │           │   │   │   ├── nt.pyi
│   │           │   │   │   ├── ntpath.pyi
│   │           │   │   │   ├── nturl2path.pyi
│   │           │   │   │   ├── numbers.pyi
│   │           │   │   │   ├── opcode.pyi
│   │           │   │   │   ├── operator.pyi
│   │           │   │   │   ├── optparse.pyi
│   │           │   │   │   ├── os
│   │           │   │   │   │   ├── __init__.pyi
│   │           │   │   │   │   └── path.pyi
│   │           │   │   │   ├── ossaudiodev.pyi
│   │           │   │   │   ├── parser.pyi
│   │           │   │   │   ├── pathlib.pyi
│   │           │   │   │   ├── pdb.pyi
│   │           │   │   │   ├── pickle.pyi
│   │           │   │   │   ├── pickletools.pyi
│   │           │   │   │   ├── pipes.pyi
│   │           │   │   │   ├── pkgutil.pyi
│   │           │   │   │   ├── platform.pyi
│   │           │   │   │   ├── plistlib.pyi
│   │           │   │   │   ├── poplib.pyi
│   │           │   │   │   ├── posix.pyi
│   │           │   │   │   ├── posixpath.pyi
│   │           │   │   │   ├── pprint.pyi
│   │           │   │   │   ├── profile.pyi
│   │           │   │   │   ├── pstats.pyi
│   │           │   │   │   ├── pty.pyi
│   │           │   │   │   ├── pwd.pyi
│   │           │   │   │   ├── py_compile.pyi
│   │           │   │   │   ├── pyclbr.pyi
│   │           │   │   │   ├── pydoc.pyi
│   │           │   │   │   ├── pydoc_data
│   │           │   │   │   │   ├── __init__.pyi
│   │           │   │   │   │   └── topics.pyi
│   │           │   │   │   ├── pyexpat
│   │           │   │   │   │   ├── __init__.pyi
│   │           │   │   │   │   ├── errors.pyi
│   │           │   │   │   │   └── model.pyi
│   │           │   │   │   ├── queue.pyi
│   │           │   │   │   ├── quopri.pyi
│   │           │   │   │   ├── random.pyi
│   │           │   │   │   ├── re.pyi
│   │           │   │   │   ├── readline.pyi
│   │           │   │   │   ├── reprlib.pyi
│   │           │   │   │   ├── resource.pyi
│   │           │   │   │   ├── rlcompleter.pyi
│   │           │   │   │   ├── runpy.pyi
│   │           │   │   │   ├── sched.pyi
│   │           │   │   │   ├── secrets.pyi
│   │           │   │   │   ├── select.pyi
│   │           │   │   │   ├── selectors.pyi
│   │           │   │   │   ├── shelve.pyi
│   │           │   │   │   ├── shlex.pyi
│   │           │   │   │   ├── shutil.pyi
│   │           │   │   │   ├── signal.pyi
│   │           │   │   │   ├── site.pyi
│   │           │   │   │   ├── smtpd.pyi
│   │           │   │   │   ├── smtplib.pyi
│   │           │   │   │   ├── sndhdr.pyi
│   │           │   │   │   ├── socket.pyi
│   │           │   │   │   ├── socketserver.pyi
│   │           │   │   │   ├── spwd.pyi
│   │           │   │   │   ├── sqlite3
│   │           │   │   │   │   ├── __init__.pyi
│   │           │   │   │   │   ├── dbapi2.pyi
│   │           │   │   │   │   └── dump.pyi
│   │           │   │   │   ├── sre_compile.pyi
│   │           │   │   │   ├── sre_constants.pyi
│   │           │   │   │   ├── sre_parse.pyi
│   │           │   │   │   ├── ssl.pyi
│   │           │   │   │   ├── stat.pyi
│   │           │   │   │   ├── statistics.pyi
│   │           │   │   │   ├── string.pyi
│   │           │   │   │   ├── stringprep.pyi
│   │           │   │   │   ├── struct.pyi
│   │           │   │   │   ├── subprocess.pyi
│   │           │   │   │   ├── sunau.pyi
│   │           │   │   │   ├── symbol.pyi
│   │           │   │   │   ├── symtable.pyi
│   │           │   │   │   ├── sys
│   │           │   │   │   │   ├── __init__.pyi
│   │           │   │   │   │   └── _monitoring.pyi
│   │           │   │   │   ├── sysconfig.pyi
│   │           │   │   │   ├── syslog.pyi
│   │           │   │   │   ├── tabnanny.pyi
│   │           │   │   │   ├── tarfile.pyi
│   │           │   │   │   ├── telnetlib.pyi
│   │           │   │   │   ├── tempfile.pyi
│   │           │   │   │   ├── termios.pyi
│   │           │   │   │   ├── textwrap.pyi
│   │           │   │   │   ├── this.pyi
│   │           │   │   │   ├── threading.pyi
│   │           │   │   │   ├── time.pyi
│   │           │   │   │   ├── timeit.pyi
│   │           │   │   │   ├── tkinter
│   │           │   │   │   │   ├── __init__.pyi
│   │           │   │   │   │   ├── colorchooser.pyi
│   │           │   │   │   │   ├── commondialog.pyi
│   │           │   │   │   │   ├── constants.pyi
│   │           │   │   │   │   ├── dialog.pyi
│   │           │   │   │   │   ├── dnd.pyi
│   │           │   │   │   │   ├── filedialog.pyi
│   │           │   │   │   │   ├── font.pyi
│   │           │   │   │   │   ├── messagebox.pyi
│   │           │   │   │   │   ├── scrolledtext.pyi
│   │           │   │   │   │   ├── simpledialog.pyi
│   │           │   │   │   │   ├── tix.pyi
│   │           │   │   │   │   └── ttk.pyi
│   │           │   │   │   ├── token.pyi
│   │           │   │   │   ├── tokenize.pyi
│   │           │   │   │   ├── tomllib.pyi
│   │           │   │   │   ├── trace.pyi
│   │           │   │   │   ├── traceback.pyi
│   │           │   │   │   ├── tracemalloc.pyi
│   │           │   │   │   ├── tty.pyi
│   │           │   │   │   ├── turtle.pyi
│   │           │   │   │   ├── types.pyi
│   │           │   │   │   ├── typing.pyi
│   │           │   │   │   ├── typing_extensions.pyi
│   │           │   │   │   ├── unicodedata.pyi
│   │           │   │   │   ├── unittest
│   │           │   │   │   │   ├── __init__.pyi
│   │           │   │   │   │   ├── _log.pyi
│   │           │   │   │   │   ├── async_case.pyi
│   │           │   │   │   │   ├── case.pyi
│   │           │   │   │   │   ├── loader.pyi
│   │           │   │   │   │   ├── main.pyi
│   │           │   │   │   │   ├── mock.pyi
│   │           │   │   │   │   ├── result.pyi
│   │           │   │   │   │   ├── runner.pyi
│   │           │   │   │   │   ├── signals.pyi
│   │           │   │   │   │   ├── suite.pyi
│   │           │   │   │   │   └── util.pyi
│   │           │   │   │   ├── urllib
│   │           │   │   │   │   ├── __init__.pyi
│   │           │   │   │   │   ├── error.pyi
│   │           │   │   │   │   ├── parse.pyi
│   │           │   │   │   │   ├── request.pyi
│   │           │   │   │   │   ├── response.pyi
│   │           │   │   │   │   └── robotparser.pyi
│   │           │   │   │   ├── uu.pyi
│   │           │   │   │   ├── uuid.pyi
│   │           │   │   │   ├── venv
│   │           │   │   │   │   └── __init__.pyi
│   │           │   │   │   ├── warnings.pyi
│   │           │   │   │   ├── wave.pyi
│   │           │   │   │   ├── weakref.pyi
│   │           │   │   │   ├── webbrowser.pyi
│   │           │   │   │   ├── winreg.pyi
│   │           │   │   │   ├── winsound.pyi
│   │           │   │   │   ├── wsgiref
│   │           │   │   │   │   ├── __init__.pyi
│   │           │   │   │   │   ├── handlers.pyi
│   │           │   │   │   │   ├── headers.pyi
│   │           │   │   │   │   ├── simple_server.pyi
│   │           │   │   │   │   ├── types.pyi
│   │           │   │   │   │   ├── util.pyi
│   │           │   │   │   │   └── validate.pyi
│   │           │   │   │   ├── xdrlib.pyi
│   │           │   │   │   ├── xml
│   │           │   │   │   │   ├── __init__.pyi
│   │           │   │   │   │   ├── dom
│   │           │   │   │   │   │   ├── NodeFilter.pyi
│   │           │   │   │   │   │   ├── __init__.pyi
│   │           │   │   │   │   │   ├── domreg.pyi
│   │           │   │   │   │   │   ├── expatbuilder.pyi
│   │           │   │   │   │   │   ├── minicompat.pyi
│   │           │   │   │   │   │   ├── minidom.pyi
│   │           │   │   │   │   │   ├── pulldom.pyi
│   │           │   │   │   │   │   └── xmlbuilder.pyi
│   │           │   │   │   │   ├── etree
│   │           │   │   │   │   │   ├── ElementInclude.pyi
│   │           │   │   │   │   │   ├── ElementPath.pyi
│   │           │   │   │   │   │   ├── ElementTree.pyi
│   │           │   │   │   │   │   ├── __init__.pyi
│   │           │   │   │   │   │   └── cElementTree.pyi
│   │           │   │   │   │   ├── parsers
│   │           │   │   │   │   │   ├── __init__.pyi
│   │           │   │   │   │   │   └── expat
│   │           │   │   │   │   │       ├── __init__.pyi
│   │           │   │   │   │   │       ├── errors.pyi
│   │           │   │   │   │   │       └── model.pyi
│   │           │   │   │   │   └── sax
│   │           │   │   │   │       ├── __init__.pyi
│   │           │   │   │   │       ├── _exceptions.pyi
│   │           │   │   │   │       ├── expatreader.pyi
│   │           │   │   │   │       ├── handler.pyi
│   │           │   │   │   │       ├── saxutils.pyi
│   │           │   │   │   │       └── xmlreader.pyi
│   │           │   │   │   ├── xmlrpc
│   │           │   │   │   │   ├── __init__.pyi
│   │           │   │   │   │   ├── client.pyi
│   │           │   │   │   │   └── server.pyi
│   │           │   │   │   ├── xxlimited.pyi
│   │           │   │   │   ├── zipapp.pyi
│   │           │   │   │   ├── zipfile
│   │           │   │   │   │   ├── __init__.pyi
│   │           │   │   │   │   └── _path
│   │           │   │   │   │       ├── __init__.pyi
│   │           │   │   │   │       └── glob.pyi
│   │           │   │   │   ├── zipimport.pyi
│   │           │   │   │   ├── zlib.pyi
│   │           │   │   │   └── zoneinfo
│   │           │   │   │       ├── __init__.pyi
│   │           │   │   │       ├── _common.pyi
│   │           │   │   │       └── _tzpath.pyi
│   │           │   │   └── stubs
│   │           │   │       └── mypy-extensions
│   │           │   │           └── mypy_extensions.pyi
│   │           │   ├── typestate.cpython-312-darwin.so
│   │           │   ├── typestate.py
│   │           │   ├── typetraverser.cpython-312-darwin.so
│   │           │   ├── typetraverser.py
│   │           │   ├── typevars.cpython-312-darwin.so
│   │           │   ├── typevars.py
│   │           │   ├── typevartuples.cpython-312-darwin.so
│   │           │   ├── typevartuples.py
│   │           │   ├── util.cpython-312-darwin.so
│   │           │   ├── util.py
│   │           │   ├── version.py
│   │           │   ├── visitor.cpython-312-darwin.so
│   │           │   ├── visitor.py
│   │           │   └── xml
│   │           │       ├── mypy-html.css
│   │           │       ├── mypy-html.xslt
│   │           │       ├── mypy-txt.xslt
│   │           │       └── mypy.xsd
│   │           ├── mypy-1.15.0.dist-info
│   │           │   ├── INSTALLER
│   │           │   ├── LICENSE
│   │           │   ├── METADATA
│   │           │   ├── RECORD
│   │           │   ├── REQUESTED
│   │           │   ├── WHEEL
│   │           │   ├── entry_points.txt
│   │           │   └── top_level.txt
│   │           ├── mypy_extensions-1.0.0.dist-info
│   │           │   ├── INSTALLER
│   │           │   ├── LICENSE
│   │           │   ├── METADATA
│   │           │   ├── RECORD
│   │           │   ├── REQUESTED
│   │           │   ├── WHEEL
│   │           │   └── top_level.txt
│   │           ├── mypy_extensions.py
│   │           ├── mypyc
│   │           │   ├── __init__.cpython-312-darwin.so
│   │           │   ├── __init__.py
│   │           │   ├── __main__.py
│   │           │   ├── analysis
│   │           │   │   ├── __init__.cpython-312-darwin.so
│   │           │   │   ├── __init__.py
│   │           │   │   ├── attrdefined.cpython-312-darwin.so
│   │           │   │   ├── attrdefined.py
│   │           │   │   ├── blockfreq.cpython-312-darwin.so
│   │           │   │   ├── blockfreq.py
│   │           │   │   ├── dataflow.cpython-312-darwin.so
│   │           │   │   ├── dataflow.py
│   │           │   │   ├── ircheck.cpython-312-darwin.so
│   │           │   │   ├── ircheck.py
│   │           │   │   ├── selfleaks.cpython-312-darwin.so
│   │           │   │   └── selfleaks.py
│   │           │   ├── build.cpython-312-darwin.so
│   │           │   ├── build.py
│   │           │   ├── codegen
│   │           │   │   ├── __init__.cpython-312-darwin.so
│   │           │   │   ├── __init__.py
│   │           │   │   ├── cstring.cpython-312-darwin.so
│   │           │   │   ├── cstring.py
│   │           │   │   ├── emit.cpython-312-darwin.so
│   │           │   │   ├── emit.py
│   │           │   │   ├── emitclass.cpython-312-darwin.so
│   │           │   │   ├── emitclass.py
│   │           │   │   ├── emitfunc.cpython-312-darwin.so
│   │           │   │   ├── emitfunc.py
│   │           │   │   ├── emitmodule.cpython-312-darwin.so
│   │           │   │   ├── emitmodule.py
│   │           │   │   ├── emitwrapper.cpython-312-darwin.so
│   │           │   │   ├── emitwrapper.py
│   │           │   │   ├── literals.cpython-312-darwin.so
│   │           │   │   └── literals.py
│   │           │   ├── common.cpython-312-darwin.so
│   │           │   ├── common.py
│   │           │   ├── crash.cpython-312-darwin.so
│   │           │   ├── crash.py
│   │           │   ├── errors.cpython-312-darwin.so
│   │           │   ├── errors.py
│   │           │   ├── ir
│   │           │   │   ├── __init__.cpython-312-darwin.so
│   │           │   │   ├── __init__.py
│   │           │   │   ├── class_ir.cpython-312-darwin.so
│   │           │   │   ├── class_ir.py
│   │           │   │   ├── func_ir.cpython-312-darwin.so
│   │           │   │   ├── func_ir.py
│   │           │   │   ├── module_ir.cpython-312-darwin.so
│   │           │   │   ├── module_ir.py
│   │           │   │   ├── ops.cpython-312-darwin.so
│   │           │   │   ├── ops.py
│   │           │   │   ├── pprint.cpython-312-darwin.so
│   │           │   │   ├── pprint.py
│   │           │   │   ├── rtypes.cpython-312-darwin.so
│   │           │   │   └── rtypes.py
│   │           │   ├── irbuild
│   │           │   │   ├── __init__.cpython-312-darwin.so
│   │           │   │   ├── __init__.py
│   │           │   │   ├── ast_helpers.cpython-312-darwin.so
│   │           │   │   ├── ast_helpers.py
│   │           │   │   ├── builder.cpython-312-darwin.so
│   │           │   │   ├── builder.py
│   │           │   │   ├── callable_class.cpython-312-darwin.so
│   │           │   │   ├── callable_class.py
│   │           │   │   ├── classdef.cpython-312-darwin.so
│   │           │   │   ├── classdef.py
│   │           │   │   ├── constant_fold.cpython-312-darwin.so
│   │           │   │   ├── constant_fold.py
│   │           │   │   ├── context.cpython-312-darwin.so
│   │           │   │   ├── context.py
│   │           │   │   ├── env_class.cpython-312-darwin.so
│   │           │   │   ├── env_class.py
│   │           │   │   ├── expression.cpython-312-darwin.so
│   │           │   │   ├── expression.py
│   │           │   │   ├── for_helpers.cpython-312-darwin.so
│   │           │   │   ├── for_helpers.py
│   │           │   │   ├── format_str_tokenizer.cpython-312-darwin.so
│   │           │   │   ├── format_str_tokenizer.py
│   │           │   │   ├── function.cpython-312-darwin.so
│   │           │   │   ├── function.py
│   │           │   │   ├── generator.cpython-312-darwin.so
│   │           │   │   ├── generator.py
│   │           │   │   ├── ll_builder.cpython-312-darwin.so
│   │           │   │   ├── ll_builder.py
│   │           │   │   ├── main.cpython-312-darwin.so
│   │           │   │   ├── main.py
│   │           │   │   ├── mapper.cpython-312-darwin.so
│   │           │   │   ├── mapper.py
│   │           │   │   ├── match.cpython-312-darwin.so
│   │           │   │   ├── match.py
│   │           │   │   ├── nonlocalcontrol.cpython-312-darwin.so
│   │           │   │   ├── nonlocalcontrol.py
│   │           │   │   ├── prebuildvisitor.cpython-312-darwin.so
│   │           │   │   ├── prebuildvisitor.py
│   │           │   │   ├── prepare.cpython-312-darwin.so
│   │           │   │   ├── prepare.py
│   │           │   │   ├── specialize.cpython-312-darwin.so
│   │           │   │   ├── specialize.py
│   │           │   │   ├── statement.cpython-312-darwin.so
│   │           │   │   ├── statement.py
│   │           │   │   ├── targets.cpython-312-darwin.so
│   │           │   │   ├── targets.py
│   │           │   │   ├── util.cpython-312-darwin.so
│   │           │   │   ├── util.py
│   │           │   │   ├── visitor.cpython-312-darwin.so
│   │           │   │   ├── visitor.py
│   │           │   │   ├── vtable.cpython-312-darwin.so
│   │           │   │   └── vtable.py
│   │           │   ├── lib-rt
│   │           │   │   ├── CPy.h
│   │           │   │   ├── bytes_ops.c
│   │           │   │   ├── dict_ops.c
│   │           │   │   ├── exc_ops.c
│   │           │   │   ├── float_ops.c
│   │           │   │   ├── generic_ops.c
│   │           │   │   ├── getargs.c
│   │           │   │   ├── getargsfast.c
│   │           │   │   ├── init.c
│   │           │   │   ├── int_ops.c
│   │           │   │   ├── list_ops.c
│   │           │   │   ├── misc_ops.c
│   │           │   │   ├── module_shim.tmpl
│   │           │   │   ├── mypyc_util.h
│   │           │   │   ├── pythoncapi_compat.h
│   │           │   │   ├── pythonsupport.c
│   │           │   │   ├── pythonsupport.h
│   │           │   │   ├── set_ops.c
│   │           │   │   ├── str_ops.c
│   │           │   │   └── tuple_ops.c
│   │           │   ├── lower
│   │           │   │   ├── __init__.cpython-312-darwin.so
│   │           │   │   ├── __init__.py
│   │           │   │   ├── int_ops.cpython-312-darwin.so
│   │           │   │   ├── int_ops.py
│   │           │   │   ├── list_ops.cpython-312-darwin.so
│   │           │   │   ├── list_ops.py
│   │           │   │   ├── misc_ops.cpython-312-darwin.so
│   │           │   │   ├── misc_ops.py
│   │           │   │   ├── registry.cpython-312-darwin.so
│   │           │   │   └── registry.py
│   │           │   ├── namegen.cpython-312-darwin.so
│   │           │   ├── namegen.py
│   │           │   ├── options.cpython-312-darwin.so
│   │           │   ├── options.py
│   │           │   ├── primitives
│   │           │   │   ├── __init__.cpython-312-darwin.so
│   │           │   │   ├── __init__.py
│   │           │   │   ├── bytes_ops.cpython-312-darwin.so
│   │           │   │   ├── bytes_ops.py
│   │           │   │   ├── dict_ops.cpython-312-darwin.so
│   │           │   │   ├── dict_ops.py
│   │           │   │   ├── exc_ops.cpython-312-darwin.so
│   │           │   │   ├── exc_ops.py
│   │           │   │   ├── float_ops.cpython-312-darwin.so
│   │           │   │   ├── float_ops.py
│   │           │   │   ├── generic_ops.cpython-312-darwin.so
│   │           │   │   ├── generic_ops.py
│   │           │   │   ├── int_ops.cpython-312-darwin.so
│   │           │   │   ├── int_ops.py
│   │           │   │   ├── list_ops.cpython-312-darwin.so
│   │           │   │   ├── list_ops.py
│   │           │   │   ├── misc_ops.cpython-312-darwin.so
│   │           │   │   ├── misc_ops.py
│   │           │   │   ├── registry.cpython-312-darwin.so
│   │           │   │   ├── registry.py
│   │           │   │   ├── set_ops.cpython-312-darwin.so
│   │           │   │   ├── set_ops.py
│   │           │   │   ├── str_ops.cpython-312-darwin.so
│   │           │   │   ├── str_ops.py
│   │           │   │   ├── tuple_ops.cpython-312-darwin.so
│   │           │   │   └── tuple_ops.py
│   │           │   ├── py.typed
│   │           │   ├── rt_subtype.cpython-312-darwin.so
│   │           │   ├── rt_subtype.py
│   │           │   ├── sametype.cpython-312-darwin.so
│   │           │   ├── sametype.py
│   │           │   ├── subtype.cpython-312-darwin.so
│   │           │   ├── subtype.py
│   │           │   ├── test
│   │           │   │   ├── __init__.py
│   │           │   │   ├── config.py
│   │           │   │   ├── test_alwaysdefined.py
│   │           │   │   ├── test_analysis.py
│   │           │   │   ├── test_cheader.py
│   │           │   │   ├── test_commandline.py
│   │           │   │   ├── test_emit.py
│   │           │   │   ├── test_emitclass.py
│   │           │   │   ├── test_emitfunc.py
│   │           │   │   ├── test_emitwrapper.py
│   │           │   │   ├── test_exceptions.py
│   │           │   │   ├── test_external.py
│   │           │   │   ├── test_irbuild.py
│   │           │   │   ├── test_ircheck.py
│   │           │   │   ├── test_literals.py
│   │           │   │   ├── test_lowering.py
│   │           │   │   ├── test_namegen.py
│   │           │   │   ├── test_optimizations.py
│   │           │   │   ├── test_pprint.py
│   │           │   │   ├── test_rarray.py
│   │           │   │   ├── test_refcount.py
│   │           │   │   ├── test_run.py
│   │           │   │   ├── test_serialization.py
│   │           │   │   ├── test_struct.py
│   │           │   │   ├── test_tuplename.py
│   │           │   │   ├── test_typeops.py
│   │           │   │   └── testutil.py
│   │           │   └── transform
│   │           │       ├── __init__.cpython-312-darwin.so
│   │           │       ├── __init__.py
│   │           │       ├── copy_propagation.cpython-312-darwin.so
│   │           │       ├── copy_propagation.py
│   │           │       ├── exceptions.cpython-312-darwin.so
│   │           │       ├── exceptions.py
│   │           │       ├── flag_elimination.cpython-312-darwin.so
│   │           │       ├── flag_elimination.py
│   │           │       ├── ir_transform.cpython-312-darwin.so
│   │           │       ├── ir_transform.py
│   │           │       ├── lower.cpython-312-darwin.so
│   │           │       ├── lower.py
│   │           │       ├── refcount.cpython-312-darwin.so
│   │           │       ├── refcount.py
│   │           │       ├── uninit.cpython-312-darwin.so
│   │           │       └── uninit.py
│   │           ├── numpy
│   │           │   ├── __config__.py
│   │           │   ├── __config__.pyi
│   │           │   ├── __init__.cython-30.pxd
│   │           │   ├── __init__.pxd
│   │           │   ├── __init__.py
│   │           │   ├── __init__.pyi
│   │           │   ├── _array_api_info.py
│   │           │   ├── _array_api_info.pyi
│   │           │   ├── _configtool.py
│   │           │   ├── _configtool.pyi
│   │           │   ├── _core
│   │           │   │   ├── __init__.py
│   │           │   │   ├── __init__.pyi
│   │           │   │   ├── _add_newdocs.py
│   │           │   │   ├── _add_newdocs_scalars.py
│   │           │   │   ├── _asarray.py
│   │           │   │   ├── _asarray.pyi
│   │           │   │   ├── _dtype.py
│   │           │   │   ├── _dtype_ctypes.py
│   │           │   │   ├── _exceptions.py
│   │           │   │   ├── _internal.py
│   │           │   │   ├── _internal.pyi
│   │           │   │   ├── _machar.py
│   │           │   │   ├── _methods.py
│   │           │   │   ├── _multiarray_tests.cpython-312-darwin.so
│   │           │   │   ├── _multiarray_umath.cpython-312-darwin.so
│   │           │   │   ├── _operand_flag_tests.cpython-312-darwin.so
│   │           │   │   ├── _rational_tests.cpython-312-darwin.so
│   │           │   │   ├── _simd.cpython-312-darwin.so
│   │           │   │   ├── _string_helpers.py
│   │           │   │   ├── _struct_ufunc_tests.cpython-312-darwin.so
│   │           │   │   ├── _type_aliases.py
│   │           │   │   ├── _type_aliases.pyi
│   │           │   │   ├── _ufunc_config.py
│   │           │   │   ├── _ufunc_config.pyi
│   │           │   │   ├── _umath_tests.cpython-312-darwin.so
│   │           │   │   ├── arrayprint.py
│   │           │   │   ├── arrayprint.pyi
│   │           │   │   ├── cversions.py
│   │           │   │   ├── defchararray.py
│   │           │   │   ├── defchararray.pyi
│   │           │   │   ├── einsumfunc.py
│   │           │   │   ├── einsumfunc.pyi
│   │           │   │   ├── fromnumeric.py
│   │           │   │   ├── fromnumeric.pyi
│   │           │   │   ├── function_base.py
│   │           │   │   ├── function_base.pyi
│   │           │   │   ├── getlimits.py
│   │           │   │   ├── getlimits.pyi
│   │           │   │   ├── include
│   │           │   │   │   └── numpy
│   │           │   │   │       ├── __multiarray_api.c
│   │           │   │   │       ├── __multiarray_api.h
│   │           │   │   │       ├── __ufunc_api.c
│   │           │   │   │       ├── __ufunc_api.h
│   │           │   │   │       ├── _neighborhood_iterator_imp.h
│   │           │   │   │       ├── _numpyconfig.h
│   │           │   │   │       ├── _public_dtype_api_table.h
│   │           │   │   │       ├── arrayobject.h
│   │           │   │   │       ├── arrayscalars.h
│   │           │   │   │       ├── dtype_api.h
│   │           │   │   │       ├── halffloat.h
│   │           │   │   │       ├── ndarrayobject.h
│   │           │   │   │       ├── ndarraytypes.h
│   │           │   │   │       ├── npy_1_7_deprecated_api.h
│   │           │   │   │       ├── npy_2_compat.h
│   │           │   │   │       ├── npy_2_complexcompat.h
│   │           │   │   │       ├── npy_3kcompat.h
│   │           │   │   │       ├── npy_common.h
│   │           │   │   │       ├── npy_cpu.h
│   │           │   │   │       ├── npy_endian.h
│   │           │   │   │       ├── npy_math.h
│   │           │   │   │       ├── npy_no_deprecated_api.h
│   │           │   │   │       ├── npy_os.h
│   │           │   │   │       ├── numpyconfig.h
│   │           │   │   │       ├── random
│   │           │   │   │       │   ├── LICENSE.txt
│   │           │   │   │       │   ├── bitgen.h
│   │           │   │   │       │   ├── distributions.h
│   │           │   │   │       │   └── libdivide.h
│   │           │   │   │       ├── ufuncobject.h
│   │           │   │   │       └── utils.h
│   │           │   │   ├── lib
│   │           │   │   │   ├── libnpymath.a
│   │           │   │   │   ├── npy-pkg-config
│   │           │   │   │   │   ├── mlib.ini
│   │           │   │   │   │   └── npymath.ini
│   │           │   │   │   └── pkgconfig
│   │           │   │   │       └── numpy.pc
│   │           │   │   ├── memmap.py
│   │           │   │   ├── memmap.pyi
│   │           │   │   ├── multiarray.py
│   │           │   │   ├── multiarray.pyi
│   │           │   │   ├── numeric.py
│   │           │   │   ├── numeric.pyi
│   │           │   │   ├── numerictypes.py
│   │           │   │   ├── numerictypes.pyi
│   │           │   │   ├── overrides.py
│   │           │   │   ├── printoptions.py
│   │           │   │   ├── records.py
│   │           │   │   ├── records.pyi
│   │           │   │   ├── shape_base.py
│   │           │   │   ├── shape_base.pyi
│   │           │   │   ├── strings.py
│   │           │   │   ├── strings.pyi
│   │           │   │   ├── tests
│   │           │   │   │   ├── _locales.py
│   │           │   │   │   ├── _natype.py
│   │           │   │   │   ├── data
│   │           │   │   │   │   ├── astype_copy.pkl
│   │           │   │   │   │   ├── generate_umath_validation_data.cpp
│   │           │   │   │   │   ├── recarray_from_file.fits
│   │           │   │   │   │   ├── umath-validation-set-README.txt
│   │           │   │   │   │   ├── umath-validation-set-arccos.csv
│   │           │   │   │   │   ├── umath-validation-set-arccosh.csv
│   │           │   │   │   │   ├── umath-validation-set-arcsin.csv
│   │           │   │   │   │   ├── umath-validation-set-arcsinh.csv
│   │           │   │   │   │   ├── umath-validation-set-arctan.csv
│   │           │   │   │   │   ├── umath-validation-set-arctanh.csv
│   │           │   │   │   │   ├── umath-validation-set-cbrt.csv
│   │           │   │   │   │   ├── umath-validation-set-cos.csv
│   │           │   │   │   │   ├── umath-validation-set-cosh.csv
│   │           │   │   │   │   ├── umath-validation-set-exp.csv
│   │           │   │   │   │   ├── umath-validation-set-exp2.csv
│   │           │   │   │   │   ├── umath-validation-set-expm1.csv
│   │           │   │   │   │   ├── umath-validation-set-log.csv
│   │           │   │   │   │   ├── umath-validation-set-log10.csv
│   │           │   │   │   │   ├── umath-validation-set-log1p.csv
│   │           │   │   │   │   ├── umath-validation-set-log2.csv
│   │           │   │   │   │   ├── umath-validation-set-sin.csv
│   │           │   │   │   │   ├── umath-validation-set-sinh.csv
│   │           │   │   │   │   ├── umath-validation-set-tan.csv
│   │           │   │   │   │   └── umath-validation-set-tanh.csv
│   │           │   │   │   ├── examples
│   │           │   │   │   │   ├── cython
│   │           │   │   │   │   │   ├── checks.pyx
│   │           │   │   │   │   │   ├── meson.build
│   │           │   │   │   │   │   └── setup.py
│   │           │   │   │   │   └── limited_api
│   │           │   │   │   │       ├── limited_api1.c
│   │           │   │   │   │       ├── limited_api2.pyx
│   │           │   │   │   │       ├── limited_api_latest.c
│   │           │   │   │   │       ├── meson.build
│   │           │   │   │   │       └── setup.py
│   │           │   │   │   ├── test__exceptions.py
│   │           │   │   │   ├── test_abc.py
│   │           │   │   │   ├── test_api.py
│   │           │   │   │   ├── test_argparse.py
│   │           │   │   │   ├── test_array_api_info.py
│   │           │   │   │   ├── test_array_coercion.py
│   │           │   │   │   ├── test_array_interface.py
│   │           │   │   │   ├── test_arraymethod.py
│   │           │   │   │   ├── test_arrayobject.py
│   │           │   │   │   ├── test_arrayprint.py
│   │           │   │   │   ├── test_casting_floatingpoint_errors.py
│   │           │   │   │   ├── test_casting_unittests.py
│   │           │   │   │   ├── test_conversion_utils.py
│   │           │   │   │   ├── test_cpu_dispatcher.py
│   │           │   │   │   ├── test_cpu_features.py
│   │           │   │   │   ├── test_custom_dtypes.py
│   │           │   │   │   ├── test_cython.py
│   │           │   │   │   ├── test_datetime.py
│   │           │   │   │   ├── test_defchararray.py
│   │           │   │   │   ├── test_deprecations.py
│   │           │   │   │   ├── test_dlpack.py
│   │           │   │   │   ├── test_dtype.py
│   │           │   │   │   ├── test_einsum.py
│   │           │   │   │   ├── test_errstate.py
│   │           │   │   │   ├── test_extint128.py
│   │           │   │   │   ├── test_function_base.py
│   │           │   │   │   ├── test_getlimits.py
│   │           │   │   │   ├── test_half.py
│   │           │   │   │   ├── test_hashtable.py
│   │           │   │   │   ├── test_indexerrors.py
│   │           │   │   │   ├── test_indexing.py
│   │           │   │   │   ├── test_item_selection.py
│   │           │   │   │   ├── test_limited_api.py
│   │           │   │   │   ├── test_longdouble.py
│   │           │   │   │   ├── test_machar.py
│   │           │   │   │   ├── test_mem_overlap.py
│   │           │   │   │   ├── test_mem_policy.py
│   │           │   │   │   ├── test_memmap.py
│   │           │   │   │   ├── test_multiarray.py
│   │           │   │   │   ├── test_multithreading.py
│   │           │   │   │   ├── test_nditer.py
│   │           │   │   │   ├── test_nep50_promotions.py
│   │           │   │   │   ├── test_numeric.py
│   │           │   │   │   ├── test_numerictypes.py
│   │           │   │   │   ├── test_overrides.py
│   │           │   │   │   ├── test_print.py
│   │           │   │   │   ├── test_protocols.py
│   │           │   │   │   ├── test_records.py
│   │           │   │   │   ├── test_regression.py
│   │           │   │   │   ├── test_scalar_ctors.py
│   │           │   │   │   ├── test_scalar_methods.py
│   │           │   │   │   ├── test_scalarbuffer.py
│   │           │   │   │   ├── test_scalarinherit.py
│   │           │   │   │   ├── test_scalarmath.py
│   │           │   │   │   ├── test_scalarprint.py
│   │           │   │   │   ├── test_shape_base.py
│   │           │   │   │   ├── test_simd.py
│   │           │   │   │   ├── test_simd_module.py
│   │           │   │   │   ├── test_stringdtype.py
│   │           │   │   │   ├── test_strings.py
│   │           │   │   │   ├── test_ufunc.py
│   │           │   │   │   ├── test_umath.py
│   │           │   │   │   ├── test_umath_accuracy.py
│   │           │   │   │   ├── test_umath_complex.py
│   │           │   │   │   └── test_unicode.py
│   │           │   │   └── umath.py
│   │           │   ├── _distributor_init.py
│   │           │   ├── _distributor_init.pyi
│   │           │   ├── _expired_attrs_2_0.py
│   │           │   ├── _expired_attrs_2_0.pyi
│   │           │   ├── _globals.py
│   │           │   ├── _globals.pyi
│   │           │   ├── _pyinstaller
│   │           │   │   ├── __init__.py
│   │           │   │   ├── hook-numpy.py
│   │           │   │   └── tests
│   │           │   │       ├── __init__.py
│   │           │   │       ├── pyinstaller-smoke.py
│   │           │   │       └── test_pyinstaller.py
│   │           │   ├── _pytesttester.py
│   │           │   ├── _pytesttester.pyi
│   │           │   ├── _typing
│   │           │   │   ├── __init__.py
│   │           │   │   ├── _add_docstring.py
│   │           │   │   ├── _array_like.py
│   │           │   │   ├── _callable.pyi
│   │           │   │   ├── _char_codes.py
│   │           │   │   ├── _dtype_like.py
│   │           │   │   ├── _extended_precision.py
│   │           │   │   ├── _nbit.py
│   │           │   │   ├── _nbit_base.py
│   │           │   │   ├── _nested_sequence.py
│   │           │   │   ├── _scalars.py
│   │           │   │   ├── _shape.py
│   │           │   │   ├── _ufunc.py
│   │           │   │   └── _ufunc.pyi
│   │           │   ├── _utils
│   │           │   │   ├── __init__.py
│   │           │   │   ├── _convertions.py
│   │           │   │   ├── _inspect.py
│   │           │   │   └── _pep440.py
│   │           │   ├── char
│   │           │   │   ├── __init__.py
│   │           │   │   └── __init__.pyi
│   │           │   ├── compat
│   │           │   │   ├── __init__.py
│   │           │   │   ├── py3k.py
│   │           │   │   └── tests
│   │           │   │       └── __init__.py
│   │           │   ├── conftest.py
│   │           │   ├── core
│   │           │   │   ├── __init__.py
│   │           │   │   ├── __init__.pyi
│   │           │   │   ├── _dtype.py
│   │           │   │   ├── _dtype_ctypes.py
│   │           │   │   ├── _internal.py
│   │           │   │   ├── _multiarray_umath.py
│   │           │   │   ├── _utils.py
│   │           │   │   ├── arrayprint.py
│   │           │   │   ├── defchararray.py
│   │           │   │   ├── einsumfunc.py
│   │           │   │   ├── fromnumeric.py
│   │           │   │   ├── function_base.py
│   │           │   │   ├── getlimits.py
│   │           │   │   ├── multiarray.py
│   │           │   │   ├── numeric.py
│   │           │   │   ├── numerictypes.py
│   │           │   │   ├── overrides.py
│   │           │   │   ├── records.py
│   │           │   │   ├── shape_base.py
│   │           │   │   └── umath.py
│   │           │   ├── ctypeslib.py
│   │           │   ├── ctypeslib.pyi
│   │           │   ├── doc
│   │           │   │   └── ufuncs.py
│   │           │   ├── dtypes.py
│   │           │   ├── dtypes.pyi
│   │           │   ├── exceptions.py
│   │           │   ├── exceptions.pyi
│   │           │   ├── f2py
│   │           │   │   ├── __init__.py
│   │           │   │   ├── __init__.pyi
│   │           │   │   ├── __main__.py
│   │           │   │   ├── __version__.py
│   │           │   │   ├── _backends
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   ├── _backend.py
│   │           │   │   │   ├── _distutils.py
│   │           │   │   │   ├── _meson.py
│   │           │   │   │   └── meson.build.template
│   │           │   │   ├── _isocbind.py
│   │           │   │   ├── _src_pyf.py
│   │           │   │   ├── auxfuncs.py
│   │           │   │   ├── capi_maps.py
│   │           │   │   ├── cb_rules.py
│   │           │   │   ├── cfuncs.py
│   │           │   │   ├── common_rules.py
│   │           │   │   ├── crackfortran.py
│   │           │   │   ├── diagnose.py
│   │           │   │   ├── f2py2e.py
│   │           │   │   ├── f90mod_rules.py
│   │           │   │   ├── func2subr.py
│   │           │   │   ├── rules.py
│   │           │   │   ├── setup.cfg
│   │           │   │   ├── src
│   │           │   │   │   ├── fortranobject.c
│   │           │   │   │   └── fortranobject.h
│   │           │   │   ├── symbolic.py
│   │           │   │   ├── tests
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   ├── src
│   │           │   │   │   │   ├── abstract_interface
│   │           │   │   │   │   │   ├── foo.f90
│   │           │   │   │   │   │   └── gh18403_mod.f90
│   │           │   │   │   │   ├── array_from_pyobj
│   │           │   │   │   │   │   └── wrapmodule.c
│   │           │   │   │   │   ├── assumed_shape
│   │           │   │   │   │   │   ├── .f2py_f2cmap
│   │           │   │   │   │   │   ├── foo_free.f90
│   │           │   │   │   │   │   ├── foo_mod.f90
│   │           │   │   │   │   │   ├── foo_use.f90
│   │           │   │   │   │   │   └── precision.f90
│   │           │   │   │   │   ├── block_docstring
│   │           │   │   │   │   │   └── foo.f
│   │           │   │   │   │   ├── callback
│   │           │   │   │   │   │   ├── foo.f
│   │           │   │   │   │   │   ├── gh17797.f90
│   │           │   │   │   │   │   ├── gh18335.f90
│   │           │   │   │   │   │   ├── gh25211.f
│   │           │   │   │   │   │   ├── gh25211.pyf
│   │           │   │   │   │   │   └── gh26681.f90
│   │           │   │   │   │   ├── cli
│   │           │   │   │   │   │   ├── gh_22819.pyf
│   │           │   │   │   │   │   ├── hi77.f
│   │           │   │   │   │   │   └── hiworld.f90
│   │           │   │   │   │   ├── common
│   │           │   │   │   │   │   ├── block.f
│   │           │   │   │   │   │   └── gh19161.f90
│   │           │   │   │   │   ├── crackfortran
│   │           │   │   │   │   │   ├── accesstype.f90
│   │           │   │   │   │   │   ├── data_common.f
│   │           │   │   │   │   │   ├── data_multiplier.f
│   │           │   │   │   │   │   ├── data_stmts.f90
│   │           │   │   │   │   │   ├── data_with_comments.f
│   │           │   │   │   │   │   ├── foo_deps.f90
│   │           │   │   │   │   │   ├── gh15035.f
│   │           │   │   │   │   │   ├── gh17859.f
│   │           │   │   │   │   │   ├── gh22648.pyf
│   │           │   │   │   │   │   ├── gh23533.f
│   │           │   │   │   │   │   ├── gh23598.f90
│   │           │   │   │   │   │   ├── gh23598Warn.f90
│   │           │   │   │   │   │   ├── gh23879.f90
│   │           │   │   │   │   │   ├── gh27697.f90
│   │           │   │   │   │   │   ├── gh2848.f90
│   │           │   │   │   │   │   ├── operators.f90
│   │           │   │   │   │   │   ├── privatemod.f90
│   │           │   │   │   │   │   ├── publicmod.f90
│   │           │   │   │   │   │   ├── pubprivmod.f90
│   │           │   │   │   │   │   └── unicode_comment.f90
│   │           │   │   │   │   ├── f2cmap
│   │           │   │   │   │   │   ├── .f2py_f2cmap
│   │           │   │   │   │   │   └── isoFortranEnvMap.f90
│   │           │   │   │   │   ├── isocintrin
│   │           │   │   │   │   │   └── isoCtests.f90
│   │           │   │   │   │   ├── kind
│   │           │   │   │   │   │   └── foo.f90
│   │           │   │   │   │   ├── mixed
│   │           │   │   │   │   │   ├── foo.f
│   │           │   │   │   │   │   ├── foo_fixed.f90
│   │           │   │   │   │   │   └── foo_free.f90
│   │           │   │   │   │   ├── modules
│   │           │   │   │   │   │   ├── gh25337
│   │           │   │   │   │   │   │   ├── data.f90
│   │           │   │   │   │   │   │   └── use_data.f90
│   │           │   │   │   │   │   ├── gh26920
│   │           │   │   │   │   │   │   ├── two_mods_with_no_public_entities.f90
│   │           │   │   │   │   │   │   └── two_mods_with_one_public_routine.f90
│   │           │   │   │   │   │   ├── module_data_docstring.f90
│   │           │   │   │   │   │   └── use_modules.f90
│   │           │   │   │   │   ├── negative_bounds
│   │           │   │   │   │   │   └── issue_20853.f90
│   │           │   │   │   │   ├── parameter
│   │           │   │   │   │   │   ├── constant_array.f90
│   │           │   │   │   │   │   ├── constant_both.f90
│   │           │   │   │   │   │   ├── constant_compound.f90
│   │           │   │   │   │   │   ├── constant_integer.f90
│   │           │   │   │   │   │   ├── constant_non_compound.f90
│   │           │   │   │   │   │   └── constant_real.f90
│   │           │   │   │   │   ├── quoted_character
│   │           │   │   │   │   │   └── foo.f
│   │           │   │   │   │   ├── regression
│   │           │   │   │   │   │   ├── AB.inc
│   │           │   │   │   │   │   ├── assignOnlyModule.f90
│   │           │   │   │   │   │   ├── datonly.f90
│   │           │   │   │   │   │   ├── f77comments.f
│   │           │   │   │   │   │   ├── f77fixedform.f95
│   │           │   │   │   │   │   ├── f90continuation.f90
│   │           │   │   │   │   │   ├── incfile.f90
│   │           │   │   │   │   │   ├── inout.f90
│   │           │   │   │   │   │   └── lower_f2py_fortran.f90
│   │           │   │   │   │   ├── return_character
│   │           │   │   │   │   │   ├── foo77.f
│   │           │   │   │   │   │   └── foo90.f90
│   │           │   │   │   │   ├── return_complex
│   │           │   │   │   │   │   ├── foo77.f
│   │           │   │   │   │   │   └── foo90.f90
│   │           │   │   │   │   ├── return_integer
│   │           │   │   │   │   │   ├── foo77.f
│   │           │   │   │   │   │   └── foo90.f90
│   │           │   │   │   │   ├── return_logical
│   │           │   │   │   │   │   ├── foo77.f
│   │           │   │   │   │   │   └── foo90.f90
│   │           │   │   │   │   ├── return_real
│   │           │   │   │   │   │   ├── foo77.f
│   │           │   │   │   │   │   └── foo90.f90
│   │           │   │   │   │   ├── routines
│   │           │   │   │   │   │   ├── funcfortranname.f
│   │           │   │   │   │   │   ├── funcfortranname.pyf
│   │           │   │   │   │   │   ├── subrout.f
│   │           │   │   │   │   │   └── subrout.pyf
│   │           │   │   │   │   ├── size
│   │           │   │   │   │   │   └── foo.f90
│   │           │   │   │   │   ├── string
│   │           │   │   │   │   │   ├── char.f90
│   │           │   │   │   │   │   ├── fixed_string.f90
│   │           │   │   │   │   │   ├── gh24008.f
│   │           │   │   │   │   │   ├── gh24662.f90
│   │           │   │   │   │   │   ├── gh25286.f90
│   │           │   │   │   │   │   ├── gh25286.pyf
│   │           │   │   │   │   │   ├── gh25286_bc.pyf
│   │           │   │   │   │   │   ├── scalar_string.f90
│   │           │   │   │   │   │   └── string.f
│   │           │   │   │   │   └── value_attrspec
│   │           │   │   │   │       └── gh21665.f90
│   │           │   │   │   ├── test_abstract_interface.py
│   │           │   │   │   ├── test_array_from_pyobj.py
│   │           │   │   │   ├── test_assumed_shape.py
│   │           │   │   │   ├── test_block_docstring.py
│   │           │   │   │   ├── test_callback.py
│   │           │   │   │   ├── test_character.py
│   │           │   │   │   ├── test_common.py
│   │           │   │   │   ├── test_crackfortran.py
│   │           │   │   │   ├── test_data.py
│   │           │   │   │   ├── test_docs.py
│   │           │   │   │   ├── test_f2cmap.py
│   │           │   │   │   ├── test_f2py2e.py
│   │           │   │   │   ├── test_isoc.py
│   │           │   │   │   ├── test_kind.py
│   │           │   │   │   ├── test_mixed.py
│   │           │   │   │   ├── test_modules.py
│   │           │   │   │   ├── test_parameter.py
│   │           │   │   │   ├── test_pyf_src.py
│   │           │   │   │   ├── test_quoted_character.py
│   │           │   │   │   ├── test_regression.py
│   │           │   │   │   ├── test_return_character.py
│   │           │   │   │   ├── test_return_complex.py
│   │           │   │   │   ├── test_return_integer.py
│   │           │   │   │   ├── test_return_logical.py
│   │           │   │   │   ├── test_return_real.py
│   │           │   │   │   ├── test_routines.py
│   │           │   │   │   ├── test_semicolon_split.py
│   │           │   │   │   ├── test_size.py
│   │           │   │   │   ├── test_string.py
│   │           │   │   │   ├── test_symbolic.py
│   │           │   │   │   ├── test_value_attrspec.py
│   │           │   │   │   └── util.py
│   │           │   │   └── use_rules.py
│   │           │   ├── fft
│   │           │   │   ├── __init__.py
│   │           │   │   ├── __init__.pyi
│   │           │   │   ├── _helper.py
│   │           │   │   ├── _helper.pyi
│   │           │   │   ├── _pocketfft.py
│   │           │   │   ├── _pocketfft.pyi
│   │           │   │   ├── _pocketfft_umath.cpython-312-darwin.so
│   │           │   │   ├── helper.py
│   │           │   │   └── tests
│   │           │   │       ├── __init__.py
│   │           │   │       ├── test_helper.py
│   │           │   │       └── test_pocketfft.py
│   │           │   ├── lib
│   │           │   │   ├── __init__.py
│   │           │   │   ├── __init__.pyi
│   │           │   │   ├── _array_utils_impl.py
│   │           │   │   ├── _array_utils_impl.pyi
│   │           │   │   ├── _arraypad_impl.py
│   │           │   │   ├── _arraypad_impl.pyi
│   │           │   │   ├── _arraysetops_impl.py
│   │           │   │   ├── _arraysetops_impl.pyi
│   │           │   │   ├── _arrayterator_impl.py
│   │           │   │   ├── _arrayterator_impl.pyi
│   │           │   │   ├── _datasource.py
│   │           │   │   ├── _datasource.pyi
│   │           │   │   ├── _function_base_impl.py
│   │           │   │   ├── _function_base_impl.pyi
│   │           │   │   ├── _histograms_impl.py
│   │           │   │   ├── _histograms_impl.pyi
│   │           │   │   ├── _index_tricks_impl.py
│   │           │   │   ├── _index_tricks_impl.pyi
│   │           │   │   ├── _iotools.py
│   │           │   │   ├── _iotools.pyi
│   │           │   │   ├── _nanfunctions_impl.py
│   │           │   │   ├── _nanfunctions_impl.pyi
│   │           │   │   ├── _npyio_impl.py
│   │           │   │   ├── _npyio_impl.pyi
│   │           │   │   ├── _polynomial_impl.py
│   │           │   │   ├── _polynomial_impl.pyi
│   │           │   │   ├── _scimath_impl.py
│   │           │   │   ├── _scimath_impl.pyi
│   │           │   │   ├── _shape_base_impl.py
│   │           │   │   ├── _shape_base_impl.pyi
│   │           │   │   ├── _stride_tricks_impl.py
│   │           │   │   ├── _stride_tricks_impl.pyi
│   │           │   │   ├── _twodim_base_impl.py
│   │           │   │   ├── _twodim_base_impl.pyi
│   │           │   │   ├── _type_check_impl.py
│   │           │   │   ├── _type_check_impl.pyi
│   │           │   │   ├── _ufunclike_impl.py
│   │           │   │   ├── _ufunclike_impl.pyi
│   │           │   │   ├── _user_array_impl.py
│   │           │   │   ├── _user_array_impl.pyi
│   │           │   │   ├── _utils_impl.py
│   │           │   │   ├── _utils_impl.pyi
│   │           │   │   ├── _version.py
│   │           │   │   ├── _version.pyi
│   │           │   │   ├── array_utils.py
│   │           │   │   ├── array_utils.pyi
│   │           │   │   ├── format.py
│   │           │   │   ├── format.pyi
│   │           │   │   ├── introspect.py
│   │           │   │   ├── introspect.pyi
│   │           │   │   ├── mixins.py
│   │           │   │   ├── mixins.pyi
│   │           │   │   ├── npyio.py
│   │           │   │   ├── npyio.pyi
│   │           │   │   ├── recfunctions.py
│   │           │   │   ├── recfunctions.pyi
│   │           │   │   ├── scimath.py
│   │           │   │   ├── scimath.pyi
│   │           │   │   ├── stride_tricks.py
│   │           │   │   ├── stride_tricks.pyi
│   │           │   │   ├── tests
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   ├── data
│   │           │   │   │   │   ├── py2-np0-objarr.npy
│   │           │   │   │   │   ├── py2-objarr.npy
│   │           │   │   │   │   ├── py2-objarr.npz
│   │           │   │   │   │   ├── py3-objarr.npy
│   │           │   │   │   │   ├── py3-objarr.npz
│   │           │   │   │   │   ├── python3.npy
│   │           │   │   │   │   └── win64python2.npy
│   │           │   │   │   ├── test__datasource.py
│   │           │   │   │   ├── test__iotools.py
│   │           │   │   │   ├── test__version.py
│   │           │   │   │   ├── test_array_utils.py
│   │           │   │   │   ├── test_arraypad.py
│   │           │   │   │   ├── test_arraysetops.py
│   │           │   │   │   ├── test_arrayterator.py
│   │           │   │   │   ├── test_format.py
│   │           │   │   │   ├── test_function_base.py
│   │           │   │   │   ├── test_histograms.py
│   │           │   │   │   ├── test_index_tricks.py
│   │           │   │   │   ├── test_io.py
│   │           │   │   │   ├── test_loadtxt.py
│   │           │   │   │   ├── test_mixins.py
│   │           │   │   │   ├── test_nanfunctions.py
│   │           │   │   │   ├── test_packbits.py
│   │           │   │   │   ├── test_polynomial.py
│   │           │   │   │   ├── test_recfunctions.py
│   │           │   │   │   ├── test_regression.py
│   │           │   │   │   ├── test_shape_base.py
│   │           │   │   │   ├── test_stride_tricks.py
│   │           │   │   │   ├── test_twodim_base.py
│   │           │   │   │   ├── test_type_check.py
│   │           │   │   │   ├── test_ufunclike.py
│   │           │   │   │   └── test_utils.py
│   │           │   │   ├── user_array.py
│   │           │   │   └── user_array.pyi
│   │           │   ├── linalg
│   │           │   │   ├── __init__.py
│   │           │   │   ├── __init__.pyi
│   │           │   │   ├── _linalg.py
│   │           │   │   ├── _linalg.pyi
│   │           │   │   ├── _umath_linalg.cpython-312-darwin.so
│   │           │   │   ├── lapack_lite.cpython-312-darwin.so
│   │           │   │   ├── linalg.py
│   │           │   │   └── tests
│   │           │   │       ├── __init__.py
│   │           │   │       ├── test_deprecations.py
│   │           │   │       ├── test_linalg.py
│   │           │   │       └── test_regression.py
│   │           │   ├── ma
│   │           │   │   ├── API_CHANGES.txt
│   │           │   │   ├── LICENSE
│   │           │   │   ├── README.rst
│   │           │   │   ├── __init__.py
│   │           │   │   ├── __init__.pyi
│   │           │   │   ├── core.py
│   │           │   │   ├── core.pyi
│   │           │   │   ├── extras.py
│   │           │   │   ├── extras.pyi
│   │           │   │   ├── mrecords.py
│   │           │   │   ├── mrecords.pyi
│   │           │   │   ├── tests
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   ├── test_arrayobject.py
│   │           │   │   │   ├── test_core.py
│   │           │   │   │   ├── test_deprecations.py
│   │           │   │   │   ├── test_extras.py
│   │           │   │   │   ├── test_mrecords.py
│   │           │   │   │   ├── test_old_ma.py
│   │           │   │   │   ├── test_regression.py
│   │           │   │   │   └── test_subclassing.py
│   │           │   │   ├── testutils.py
│   │           │   │   └── timer_comparison.py
│   │           │   ├── matlib.py
│   │           │   ├── matlib.pyi
│   │           │   ├── matrixlib
│   │           │   │   ├── __init__.py
│   │           │   │   ├── __init__.pyi
│   │           │   │   ├── defmatrix.py
│   │           │   │   ├── defmatrix.pyi
│   │           │   │   └── tests
│   │           │   │       ├── __init__.py
│   │           │   │       ├── test_defmatrix.py
│   │           │   │       ├── test_interaction.py
│   │           │   │       ├── test_masked_matrix.py
│   │           │   │       ├── test_matrix_linalg.py
│   │           │   │       ├── test_multiarray.py
│   │           │   │       ├── test_numeric.py
│   │           │   │       └── test_regression.py
│   │           │   ├── polynomial
│   │           │   │   ├── __init__.py
│   │           │   │   ├── __init__.pyi
│   │           │   │   ├── _polybase.py
│   │           │   │   ├── _polybase.pyi
│   │           │   │   ├── _polytypes.pyi
│   │           │   │   ├── chebyshev.py
│   │           │   │   ├── chebyshev.pyi
│   │           │   │   ├── hermite.py
│   │           │   │   ├── hermite.pyi
│   │           │   │   ├── hermite_e.py
│   │           │   │   ├── hermite_e.pyi
│   │           │   │   ├── laguerre.py
│   │           │   │   ├── laguerre.pyi
│   │           │   │   ├── legendre.py
│   │           │   │   ├── legendre.pyi
│   │           │   │   ├── polynomial.py
│   │           │   │   ├── polynomial.pyi
│   │           │   │   ├── polyutils.py
│   │           │   │   ├── polyutils.pyi
│   │           │   │   └── tests
│   │           │   │       ├── __init__.py
│   │           │   │       ├── test_chebyshev.py
│   │           │   │       ├── test_classes.py
│   │           │   │       ├── test_hermite.py
│   │           │   │       ├── test_hermite_e.py
│   │           │   │       ├── test_laguerre.py
│   │           │   │       ├── test_legendre.py
│   │           │   │       ├── test_polynomial.py
│   │           │   │       ├── test_polyutils.py
│   │           │   │       ├── test_printing.py
│   │           │   │       └── test_symbol.py
│   │           │   ├── py.typed
│   │           │   ├── random
│   │           │   │   ├── LICENSE.md
│   │           │   │   ├── __init__.pxd
│   │           │   │   ├── __init__.py
│   │           │   │   ├── __init__.pyi
│   │           │   │   ├── _bounded_integers.cpython-312-darwin.so
│   │           │   │   ├── _bounded_integers.pxd
│   │           │   │   ├── _common.cpython-312-darwin.so
│   │           │   │   ├── _common.pxd
│   │           │   │   ├── _examples
│   │           │   │   │   ├── cffi
│   │           │   │   │   │   ├── extending.py
│   │           │   │   │   │   └── parse.py
│   │           │   │   │   ├── cython
│   │           │   │   │   │   ├── extending.pyx
│   │           │   │   │   │   ├── extending_distributions.pyx
│   │           │   │   │   │   └── meson.build
│   │           │   │   │   └── numba
│   │           │   │   │       ├── extending.py
│   │           │   │   │       └── extending_distributions.py
│   │           │   │   ├── _generator.cpython-312-darwin.so
│   │           │   │   ├── _generator.pyi
│   │           │   │   ├── _mt19937.cpython-312-darwin.so
│   │           │   │   ├── _mt19937.pyi
│   │           │   │   ├── _pcg64.cpython-312-darwin.so
│   │           │   │   ├── _pcg64.pyi
│   │           │   │   ├── _philox.cpython-312-darwin.so
│   │           │   │   ├── _philox.pyi
│   │           │   │   ├── _pickle.py
│   │           │   │   ├── _sfc64.cpython-312-darwin.so
│   │           │   │   ├── _sfc64.pyi
│   │           │   │   ├── bit_generator.cpython-312-darwin.so
│   │           │   │   ├── bit_generator.pxd
│   │           │   │   ├── bit_generator.pyi
│   │           │   │   ├── c_distributions.pxd
│   │           │   │   ├── lib
│   │           │   │   │   └── libnpyrandom.a
│   │           │   │   ├── mtrand.cpython-312-darwin.so
│   │           │   │   ├── mtrand.pyi
│   │           │   │   └── tests
│   │           │   │       ├── __init__.py
│   │           │   │       ├── data
│   │           │   │       │   ├── __init__.py
│   │           │   │       │   ├── generator_pcg64_np121.pkl.gz
│   │           │   │       │   ├── generator_pcg64_np126.pkl.gz
│   │           │   │       │   ├── mt19937-testset-1.csv
│   │           │   │       │   ├── mt19937-testset-2.csv
│   │           │   │       │   ├── pcg64-testset-1.csv
│   │           │   │       │   ├── pcg64-testset-2.csv
│   │           │   │       │   ├── pcg64dxsm-testset-1.csv
│   │           │   │       │   ├── pcg64dxsm-testset-2.csv
│   │           │   │       │   ├── philox-testset-1.csv
│   │           │   │       │   ├── philox-testset-2.csv
│   │           │   │       │   ├── sfc64-testset-1.csv
│   │           │   │       │   ├── sfc64-testset-2.csv
│   │           │   │       │   └── sfc64_np126.pkl.gz
│   │           │   │       ├── test_direct.py
│   │           │   │       ├── test_extending.py
│   │           │   │       ├── test_generator_mt19937.py
│   │           │   │       ├── test_generator_mt19937_regressions.py
│   │           │   │       ├── test_random.py
│   │           │   │       ├── test_randomstate.py
│   │           │   │       ├── test_randomstate_regression.py
│   │           │   │       ├── test_regression.py
│   │           │   │       ├── test_seed_sequence.py
│   │           │   │       └── test_smoke.py
│   │           │   ├── rec
│   │           │   │   ├── __init__.py
│   │           │   │   └── __init__.pyi
│   │           │   ├── strings
│   │           │   │   ├── __init__.py
│   │           │   │   └── __init__.pyi
│   │           │   ├── testing
│   │           │   │   ├── __init__.py
│   │           │   │   ├── __init__.pyi
│   │           │   │   ├── _private
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   ├── __init__.pyi
│   │           │   │   │   ├── extbuild.py
│   │           │   │   │   ├── extbuild.pyi
│   │           │   │   │   ├── utils.py
│   │           │   │   │   └── utils.pyi
│   │           │   │   ├── overrides.py
│   │           │   │   ├── overrides.pyi
│   │           │   │   ├── print_coercion_tables.py
│   │           │   │   ├── print_coercion_tables.pyi
│   │           │   │   └── tests
│   │           │   │       ├── __init__.py
│   │           │   │       └── test_utils.py
│   │           │   ├── tests
│   │           │   │   ├── __init__.py
│   │           │   │   ├── test__all__.py
│   │           │   │   ├── test_configtool.py
│   │           │   │   ├── test_ctypeslib.py
│   │           │   │   ├── test_lazyloading.py
│   │           │   │   ├── test_matlib.py
│   │           │   │   ├── test_numpy_config.py
│   │           │   │   ├── test_numpy_version.py
│   │           │   │   ├── test_public_api.py
│   │           │   │   ├── test_reloading.py
│   │           │   │   ├── test_scripts.py
│   │           │   │   └── test_warnings.py
│   │           │   ├── typing
│   │           │   │   ├── __init__.py
│   │           │   │   ├── mypy_plugin.py
│   │           │   │   └── tests
│   │           │   │       ├── __init__.py
│   │           │   │       ├── data
│   │           │   │       │   ├── fail
│   │           │   │       │   │   ├── arithmetic.pyi
│   │           │   │       │   │   ├── array_constructors.pyi
│   │           │   │       │   │   ├── array_like.pyi
│   │           │   │       │   │   ├── array_pad.pyi
│   │           │   │       │   │   ├── arrayprint.pyi
│   │           │   │       │   │   ├── arrayterator.pyi
│   │           │   │       │   │   ├── bitwise_ops.pyi
│   │           │   │       │   │   ├── char.pyi
│   │           │   │       │   │   ├── chararray.pyi
│   │           │   │       │   │   ├── comparisons.pyi
│   │           │   │       │   │   ├── constants.pyi
│   │           │   │       │   │   ├── datasource.pyi
│   │           │   │       │   │   ├── dtype.pyi
│   │           │   │       │   │   ├── einsumfunc.pyi
│   │           │   │       │   │   ├── flatiter.pyi
│   │           │   │       │   │   ├── fromnumeric.pyi
│   │           │   │       │   │   ├── histograms.pyi
│   │           │   │       │   │   ├── index_tricks.pyi
│   │           │   │       │   │   ├── lib_function_base.pyi
│   │           │   │       │   │   ├── lib_polynomial.pyi
│   │           │   │       │   │   ├── lib_utils.pyi
│   │           │   │       │   │   ├── lib_version.pyi
│   │           │   │       │   │   ├── linalg.pyi
│   │           │   │       │   │   ├── memmap.pyi
│   │           │   │       │   │   ├── modules.pyi
│   │           │   │       │   │   ├── multiarray.pyi
│   │           │   │       │   │   ├── ndarray.pyi
│   │           │   │       │   │   ├── ndarray_misc.pyi
│   │           │   │       │   │   ├── nditer.pyi
│   │           │   │       │   │   ├── nested_sequence.pyi
│   │           │   │       │   │   ├── npyio.pyi
│   │           │   │       │   │   ├── numerictypes.pyi
│   │           │   │       │   │   ├── random.pyi
│   │           │   │       │   │   ├── rec.pyi
│   │           │   │       │   │   ├── scalars.pyi
│   │           │   │       │   │   ├── shape.pyi
│   │           │   │       │   │   ├── shape_base.pyi
│   │           │   │       │   │   ├── stride_tricks.pyi
│   │           │   │       │   │   ├── strings.pyi
│   │           │   │       │   │   ├── testing.pyi
│   │           │   │       │   │   ├── twodim_base.pyi
│   │           │   │       │   │   ├── type_check.pyi
│   │           │   │       │   │   ├── ufunc_config.pyi
│   │           │   │       │   │   ├── ufunclike.pyi
│   │           │   │       │   │   ├── ufuncs.pyi
│   │           │   │       │   │   └── warnings_and_errors.pyi
│   │           │   │       │   ├── misc
│   │           │   │       │   │   └── extended_precision.pyi
│   │           │   │       │   ├── mypy.ini
│   │           │   │       │   ├── pass
│   │           │   │       │   │   ├── arithmetic.py
│   │           │   │       │   │   ├── array_constructors.py
│   │           │   │       │   │   ├── array_like.py
│   │           │   │       │   │   ├── arrayprint.py
│   │           │   │       │   │   ├── arrayterator.py
│   │           │   │       │   │   ├── bitwise_ops.py
│   │           │   │       │   │   ├── comparisons.py
│   │           │   │       │   │   ├── dtype.py
│   │           │   │       │   │   ├── einsumfunc.py
│   │           │   │       │   │   ├── flatiter.py
│   │           │   │       │   │   ├── fromnumeric.py
│   │           │   │       │   │   ├── index_tricks.py
│   │           │   │       │   │   ├── lib_user_array.py
│   │           │   │       │   │   ├── lib_utils.py
│   │           │   │       │   │   ├── lib_version.py
│   │           │   │       │   │   ├── literal.py
│   │           │   │       │   │   ├── ma.py
│   │           │   │       │   │   ├── mod.py
│   │           │   │       │   │   ├── modules.py
│   │           │   │       │   │   ├── multiarray.py
│   │           │   │       │   │   ├── ndarray_conversion.py
│   │           │   │       │   │   ├── ndarray_misc.py
│   │           │   │       │   │   ├── ndarray_shape_manipulation.py
│   │           │   │       │   │   ├── nditer.py
│   │           │   │       │   │   ├── numeric.py
│   │           │   │       │   │   ├── numerictypes.py
│   │           │   │       │   │   ├── random.py
│   │           │   │       │   │   ├── recfunctions.py
│   │           │   │       │   │   ├── scalars.py
│   │           │   │       │   │   ├── shape.py
│   │           │   │       │   │   ├── simple.py
│   │           │   │       │   │   ├── simple_py3.py
│   │           │   │       │   │   ├── ufunc_config.py
│   │           │   │       │   │   ├── ufunclike.py
│   │           │   │       │   │   ├── ufuncs.py
│   │           │   │       │   │   └── warnings_and_errors.py
│   │           │   │       │   └── reveal
│   │           │   │       │       ├── arithmetic.pyi
│   │           │   │       │       ├── array_api_info.pyi
│   │           │   │       │       ├── array_constructors.pyi
│   │           │   │       │       ├── arraypad.pyi
│   │           │   │       │       ├── arrayprint.pyi
│   │           │   │       │       ├── arraysetops.pyi
│   │           │   │       │       ├── arrayterator.pyi
│   │           │   │       │       ├── bitwise_ops.pyi
│   │           │   │       │       ├── char.pyi
│   │           │   │       │       ├── chararray.pyi
│   │           │   │       │       ├── comparisons.pyi
│   │           │   │       │       ├── constants.pyi
│   │           │   │       │       ├── ctypeslib.pyi
│   │           │   │       │       ├── datasource.pyi
│   │           │   │       │       ├── dtype.pyi
│   │           │   │       │       ├── einsumfunc.pyi
│   │           │   │       │       ├── emath.pyi
│   │           │   │       │       ├── fft.pyi
│   │           │   │       │       ├── flatiter.pyi
│   │           │   │       │       ├── fromnumeric.pyi
│   │           │   │       │       ├── getlimits.pyi
│   │           │   │       │       ├── histograms.pyi
│   │           │   │       │       ├── index_tricks.pyi
│   │           │   │       │       ├── lib_function_base.pyi
│   │           │   │       │       ├── lib_polynomial.pyi
│   │           │   │       │       ├── lib_utils.pyi
│   │           │   │       │       ├── lib_version.pyi
│   │           │   │       │       ├── linalg.pyi
│   │           │   │       │       ├── matrix.pyi
│   │           │   │       │       ├── memmap.pyi
│   │           │   │       │       ├── mod.pyi
│   │           │   │       │       ├── modules.pyi
│   │           │   │       │       ├── multiarray.pyi
│   │           │   │       │       ├── nbit_base_example.pyi
│   │           │   │       │       ├── ndarray_assignability.pyi
│   │           │   │       │       ├── ndarray_conversion.pyi
│   │           │   │       │       ├── ndarray_misc.pyi
│   │           │   │       │       ├── ndarray_shape_manipulation.pyi
│   │           │   │       │       ├── nditer.pyi
│   │           │   │       │       ├── nested_sequence.pyi
│   │           │   │       │       ├── npyio.pyi
│   │           │   │       │       ├── numeric.pyi
│   │           │   │       │       ├── numerictypes.pyi
│   │           │   │       │       ├── polynomial_polybase.pyi
│   │           │   │       │       ├── polynomial_polyutils.pyi
│   │           │   │       │       ├── polynomial_series.pyi
│   │           │   │       │       ├── random.pyi
│   │           │   │       │       ├── rec.pyi
│   │           │   │       │       ├── scalars.pyi
│   │           │   │       │       ├── shape.pyi
│   │           │   │       │       ├── shape_base.pyi
│   │           │   │       │       ├── stride_tricks.pyi
│   │           │   │       │       ├── strings.pyi
│   │           │   │       │       ├── testing.pyi
│   │           │   │       │       ├── twodim_base.pyi
│   │           │   │       │       ├── type_check.pyi
│   │           │   │       │       ├── ufunc_config.pyi
│   │           │   │       │       ├── ufunclike.pyi
│   │           │   │       │       ├── ufuncs.pyi
│   │           │   │       │       └── warnings_and_errors.pyi
│   │           │   │       ├── test_isfile.py
│   │           │   │       ├── test_runtime.py
│   │           │   │       └── test_typing.py
│   │           │   ├── version.py
│   │           │   └── version.pyi
│   │           ├── numpy-2.2.3.dist-info
│   │           │   ├── INSTALLER
│   │           │   ├── LICENSE.txt
│   │           │   ├── METADATA
│   │           │   ├── RECORD
│   │           │   ├── REQUESTED
│   │           │   ├── WHEEL
│   │           │   └── entry_points.txt
│   │           ├── packaging
│   │           │   ├── __init__.py
│   │           │   ├── _elffile.py
│   │           │   ├── _manylinux.py
│   │           │   ├── _musllinux.py
│   │           │   ├── _parser.py
│   │           │   ├── _structures.py
│   │           │   ├── _tokenizer.py
│   │           │   ├── licenses
│   │           │   │   ├── __init__.py
│   │           │   │   └── _spdx.py
│   │           │   ├── markers.py
│   │           │   ├── metadata.py
│   │           │   ├── py.typed
│   │           │   ├── requirements.py
│   │           │   ├── specifiers.py
│   │           │   ├── tags.py
│   │           │   ├── utils.py
│   │           │   └── version.py
│   │           ├── packaging-24.2.dist-info
│   │           │   ├── INSTALLER
│   │           │   ├── LICENSE
│   │           │   ├── LICENSE.APACHE
│   │           │   ├── LICENSE.BSD
│   │           │   ├── METADATA
│   │           │   ├── RECORD
│   │           │   ├── REQUESTED
│   │           │   └── WHEEL
│   │           ├── pkg_resources
│   │           │   ├── __init__.py
│   │           │   ├── api_tests.txt
│   │           │   ├── py.typed
│   │           │   └── tests
│   │           │       ├── __init__.py
│   │           │       ├── data
│   │           │       │   ├── my-test-package-source
│   │           │       │   │   ├── setup.cfg
│   │           │       │   │   └── setup.py
│   │           │       │   ├── my-test-package-zip
│   │           │       │   │   └── my-test-package.zip
│   │           │       │   ├── my-test-package_unpacked-egg
│   │           │       │   │   └── my_test_package-1.0-py3.7.egg
│   │           │       │   │       └── EGG-INFO
│   │           │       │   │           ├── PKG-INFO
│   │           │       │   │           ├── SOURCES.txt
│   │           │       │   │           ├── dependency_links.txt
│   │           │       │   │           ├── top_level.txt
│   │           │       │   │           └── zip-safe
│   │           │       │   └── my-test-package_zipped-egg
│   │           │       │       └── my_test_package-1.0-py3.7.egg
│   │           │       ├── test_find_distributions.py
│   │           │       ├── test_integration_zope_interface.py
│   │           │       ├── test_markers.py
│   │           │       ├── test_pkg_resources.py
│   │           │       ├── test_resources.py
│   │           │       └── test_working_set.py
│   │           ├── platformdirs
│   │           │   ├── __init__.py
│   │           │   ├── __main__.py
│   │           │   ├── android.py
│   │           │   ├── api.py
│   │           │   ├── macos.py
│   │           │   ├── py.typed
│   │           │   ├── unix.py
│   │           │   ├── version.py
│   │           │   └── windows.py
│   │           ├── platformdirs-4.3.6.dist-info
│   │           │   ├── INSTALLER
│   │           │   ├── METADATA
│   │           │   ├── RECORD
│   │           │   ├── REQUESTED
│   │           │   ├── WHEEL
│   │           │   └── licenses
│   │           │       └── LICENSE
│   │           ├── pluggy
│   │           │   ├── __init__.py
│   │           │   ├── _callers.py
│   │           │   ├── _hooks.py
│   │           │   ├── _manager.py
│   │           │   ├── _result.py
│   │           │   ├── _tracing.py
│   │           │   ├── _version.py
│   │           │   ├── _warnings.py
│   │           │   └── py.typed
│   │           ├── pluggy-1.5.0.dist-info
│   │           │   ├── INSTALLER
│   │           │   ├── LICENSE
│   │           │   ├── METADATA
│   │           │   ├── RECORD
│   │           │   ├── REQUESTED
│   │           │   ├── WHEEL
│   │           │   └── top_level.txt
│   │           ├── pox
│   │           │   ├── __info__.py
│   │           │   ├── __init__.py
│   │           │   ├── __main__.py
│   │           │   ├── _disk.py
│   │           │   ├── shutils.py
│   │           │   ├── tests
│   │           │   │   ├── __init__.py
│   │           │   │   ├── __main__.py
│   │           │   │   ├── test_shutils.py
│   │           │   │   └── test_utils.py
│   │           │   └── utils.py
│   │           ├── pox-0.3.5.dist-info
│   │           │   ├── INSTALLER
│   │           │   ├── LICENSE
│   │           │   ├── METADATA
│   │           │   ├── RECORD
│   │           │   ├── REQUESTED
│   │           │   ├── WHEEL
│   │           │   └── top_level.txt
│   │           ├── py.py
│   │           ├── py_cpuinfo-9.0.0.dist-info
│   │           │   ├── INSTALLER
│   │           │   ├── LICENSE
│   │           │   ├── METADATA
│   │           │   ├── RECORD
│   │           │   ├── REQUESTED
│   │           │   ├── WHEEL
│   │           │   ├── entry_points.txt
│   │           │   └── top_level.txt
│   │           ├── pydantic
│   │           │   ├── __init__.py
│   │           │   ├── _internal
│   │           │   │   ├── __init__.py
│   │           │   │   ├── _config.py
│   │           │   │   ├── _core_metadata.py
│   │           │   │   ├── _core_utils.py
│   │           │   │   ├── _dataclasses.py
│   │           │   │   ├── _decorators.py
│   │           │   │   ├── _decorators_v1.py
│   │           │   │   ├── _discriminated_union.py
│   │           │   │   ├── _docs_extraction.py
│   │           │   │   ├── _fields.py
│   │           │   │   ├── _forward_ref.py
│   │           │   │   ├── _generate_schema.py
│   │           │   │   ├── _generics.py
│   │           │   │   ├── _git.py
│   │           │   │   ├── _import_utils.py
│   │           │   │   ├── _internal_dataclass.py
│   │           │   │   ├── _known_annotated_metadata.py
│   │           │   │   ├── _mock_val_ser.py
│   │           │   │   ├── _model_construction.py
│   │           │   │   ├── _namespace_utils.py
│   │           │   │   ├── _repr.py
│   │           │   │   ├── _schema_generation_shared.py
│   │           │   │   ├── _serializers.py
│   │           │   │   ├── _signature.py
│   │           │   │   ├── _std_types_schema.py
│   │           │   │   ├── _typing_extra.py
│   │           │   │   ├── _utils.py
│   │           │   │   ├── _validate_call.py
│   │           │   │   └── _validators.py
│   │           │   ├── _migration.py
│   │           │   ├── alias_generators.py
│   │           │   ├── aliases.py
│   │           │   ├── annotated_handlers.py
│   │           │   ├── class_validators.py
│   │           │   ├── color.py
│   │           │   ├── config.py
│   │           │   ├── dataclasses.py
│   │           │   ├── datetime_parse.py
│   │           │   ├── decorator.py
│   │           │   ├── deprecated
│   │           │   │   ├── __init__.py
│   │           │   │   ├── class_validators.py
│   │           │   │   ├── config.py
│   │           │   │   ├── copy_internals.py
│   │           │   │   ├── decorator.py
│   │           │   │   ├── json.py
│   │           │   │   ├── parse.py
│   │           │   │   └── tools.py
│   │           │   ├── env_settings.py
│   │           │   ├── error_wrappers.py
│   │           │   ├── errors.py
│   │           │   ├── experimental
│   │           │   │   ├── __init__.py
│   │           │   │   └── pipeline.py
│   │           │   ├── fields.py
│   │           │   ├── functional_serializers.py
│   │           │   ├── functional_validators.py
│   │           │   ├── generics.py
│   │           │   ├── json.py
│   │           │   ├── json_schema.py
│   │           │   ├── main.py
│   │           │   ├── mypy.py
│   │           │   ├── networks.py
│   │           │   ├── parse.py
│   │           │   ├── plugin
│   │           │   │   ├── __init__.py
│   │           │   │   ├── _loader.py
│   │           │   │   └── _schema_validator.py
│   │           │   ├── py.typed
│   │           │   ├── root_model.py
│   │           │   ├── schema.py
│   │           │   ├── tools.py
│   │           │   ├── type_adapter.py
│   │           │   ├── types.py
│   │           │   ├── typing.py
│   │           │   ├── utils.py
│   │           │   ├── v1
│   │           │   │   ├── __init__.py
│   │           │   │   ├── _hypothesis_plugin.py
│   │           │   │   ├── annotated_types.py
│   │           │   │   ├── class_validators.py
│   │           │   │   ├── color.py
│   │           │   │   ├── config.py
│   │           │   │   ├── dataclasses.py
│   │           │   │   ├── datetime_parse.py
│   │           │   │   ├── decorator.py
│   │           │   │   ├── env_settings.py
│   │           │   │   ├── error_wrappers.py
│   │           │   │   ├── errors.py
│   │           │   │   ├── fields.py
│   │           │   │   ├── generics.py
│   │           │   │   ├── json.py
│   │           │   │   ├── main.py
│   │           │   │   ├── mypy.py
│   │           │   │   ├── networks.py
│   │           │   │   ├── parse.py
│   │           │   │   ├── py.typed
│   │           │   │   ├── schema.py
│   │           │   │   ├── tools.py
│   │           │   │   ├── types.py
│   │           │   │   ├── typing.py
│   │           │   │   ├── utils.py
│   │           │   │   ├── validators.py
│   │           │   │   └── version.py
│   │           │   ├── validate_call_decorator.py
│   │           │   ├── validators.py
│   │           │   ├── version.py
│   │           │   └── warnings.py
│   │           ├── pydantic-2.10.6.dist-info
│   │           │   ├── INSTALLER
│   │           │   ├── METADATA
│   │           │   ├── RECORD
│   │           │   ├── REQUESTED
│   │           │   ├── WHEEL
│   │           │   └── licenses
│   │           │       └── LICENSE
│   │           ├── pydantic_core
│   │           │   ├── __init__.py
│   │           │   ├── _pydantic_core.cpython-312-darwin.so
│   │           │   ├── _pydantic_core.pyi
│   │           │   ├── core_schema.py
│   │           │   └── py.typed
│   │           ├── pydantic_core-2.27.2.dist-info
│   │           │   ├── INSTALLER
│   │           │   ├── METADATA
│   │           │   ├── RECORD
│   │           │   ├── REQUESTED
│   │           │   ├── WHEEL
│   │           │   └── licenses
│   │           │       └── LICENSE
│   │           ├── pydantic_settings
│   │           │   ├── __init__.py
│   │           │   ├── main.py
│   │           │   ├── py.typed
│   │           │   ├── sources.py
│   │           │   ├── utils.py
│   │           │   └── version.py
│   │           ├── pydantic_settings-2.7.1.dist-info
│   │           │   ├── INSTALLER
│   │           │   ├── METADATA
│   │           │   ├── RECORD
│   │           │   ├── REQUESTED
│   │           │   ├── WHEEL
│   │           │   └── licenses
│   │           │       └── LICENSE
│   │           ├── pygal
│   │           │   ├── __about__.py
│   │           │   ├── __init__.py
│   │           │   ├── _compat.py
│   │           │   ├── adapters.py
│   │           │   ├── colors.py
│   │           │   ├── config.py
│   │           │   ├── css
│   │           │   │   ├── base.css
│   │           │   │   ├── graph.css
│   │           │   │   └── style.css
│   │           │   ├── etree.py
│   │           │   ├── formatters.py
│   │           │   ├── graph
│   │           │   │   ├── __init__.py
│   │           │   │   ├── bar.py
│   │           │   │   ├── base.py
│   │           │   │   ├── box.py
│   │           │   │   ├── dot.py
│   │           │   │   ├── dual.py
│   │           │   │   ├── funnel.py
│   │           │   │   ├── gauge.py
│   │           │   │   ├── graph.py
│   │           │   │   ├── histogram.py
│   │           │   │   ├── horizontal.py
│   │           │   │   ├── horizontalbar.py
│   │           │   │   ├── horizontalline.py
│   │           │   │   ├── horizontalstackedbar.py
│   │           │   │   ├── horizontalstackedline.py
│   │           │   │   ├── line.py
│   │           │   │   ├── map.py
│   │           │   │   ├── pie.py
│   │           │   │   ├── public.py
│   │           │   │   ├── pyramid.py
│   │           │   │   ├── radar.py
│   │           │   │   ├── solidgauge.py
│   │           │   │   ├── stackedbar.py
│   │           │   │   ├── stackedline.py
│   │           │   │   ├── time.py
│   │           │   │   ├── treemap.py
│   │           │   │   └── xy.py
│   │           │   ├── interpolate.py
│   │           │   ├── maps
│   │           │   │   └── __init__.py
│   │           │   ├── serie.py
│   │           │   ├── state.py
│   │           │   ├── stats.py
│   │           │   ├── style.py
│   │           │   ├── svg.py
│   │           │   ├── table.py
│   │           │   ├── test
│   │           │   │   ├── __init__.py
│   │           │   │   ├── conftest.py
│   │           │   │   ├── test_bar.py
│   │           │   │   ├── test_box.py
│   │           │   │   ├── test_colors.py
│   │           │   │   ├── test_config.py
│   │           │   │   ├── test_date.py
│   │           │   │   ├── test_formatters.py
│   │           │   │   ├── test_graph.py
│   │           │   │   ├── test_histogram.py
│   │           │   │   ├── test_interpolate.py
│   │           │   │   ├── test_line.py
│   │           │   │   ├── test_line_log_none_max_solved.py
│   │           │   │   ├── test_maps.py
│   │           │   │   ├── test_pie.py
│   │           │   │   ├── test_serie_config.py
│   │           │   │   ├── test_sparktext.py
│   │           │   │   ├── test_stacked.py
│   │           │   │   ├── test_style.py
│   │           │   │   ├── test_table.py
│   │           │   │   ├── test_util.py
│   │           │   │   ├── test_view.py
│   │           │   │   ├── test_xml_filters.py
│   │           │   │   └── utils.py
│   │           │   ├── util.py
│   │           │   └── view.py
│   │           ├── pygal-3.0.5.dist-info
│   │           │   ├── COPYING
│   │           │   ├── INSTALLER
│   │           │   ├── METADATA
│   │           │   ├── RECORD
│   │           │   ├── REQUESTED
│   │           │   ├── WHEEL
│   │           │   └── top_level.txt
│   │           ├── pygaljs
│   │           │   ├── __init__.py
│   │           │   └── static
│   │           │       ├── 2.0.x
│   │           │       │   ├── pygal-tooltips.js
│   │           │       │   └── pygal-tooltips.min.js
│   │           │       ├── Gruntfile.coffee
│   │           │       ├── README.md
│   │           │       ├── bower.json
│   │           │       ├── coffee
│   │           │       │   └── pygal-tooltips.coffee
│   │           │       ├── javascripts
│   │           │       │   ├── pygal-tooltips.js
│   │           │       │   └── svg.jquery.js
│   │           │       ├── latest
│   │           │       │   ├── pygal-tooltips.js
│   │           │       │   └── pygal-tooltips.min.js
│   │           │       └── package.json
│   │           ├── pygaljs-1.0.2.dist-info
│   │           │   ├── INSTALLER
│   │           │   ├── LICENSE
│   │           │   ├── METADATA
│   │           │   ├── RECORD
│   │           │   ├── REQUESTED
│   │           │   ├── WHEEL
│   │           │   └── top_level.txt
│   │           ├── pytest
│   │           │   ├── __init__.py
│   │           │   ├── __main__.py
│   │           │   └── py.typed
│   │           ├── pytest-8.3.4.dist-info
│   │           │   ├── AUTHORS
│   │           │   ├── INSTALLER
│   │           │   ├── LICENSE
│   │           │   ├── METADATA
│   │           │   ├── RECORD
│   │           │   ├── REQUESTED
│   │           │   ├── WHEEL
│   │           │   ├── entry_points.txt
│   │           │   └── top_level.txt
│   │           ├── pytest-cov.pth
│   │           ├── pytest_asyncio
│   │           │   ├── __init__.py
│   │           │   ├── _version.py
│   │           │   ├── plugin.py
│   │           │   └── py.typed
│   │           ├── pytest_asyncio-0.25.3.dist-info
│   │           │   ├── INSTALLER
│   │           │   ├── LICENSE
│   │           │   ├── METADATA
│   │           │   ├── RECORD
│   │           │   ├── REQUESTED
│   │           │   ├── WHEEL
│   │           │   ├── entry_points.txt
│   │           │   └── top_level.txt
│   │           ├── pytest_benchmark
│   │           │   ├── __init__.py
│   │           │   ├── __main__.py
│   │           │   ├── cli.py
│   │           │   ├── compat.py
│   │           │   ├── csv.py
│   │           │   ├── fixture.py
│   │           │   ├── histogram.py
│   │           │   ├── hookspec.py
│   │           │   ├── logger.py
│   │           │   ├── plugin.py
│   │           │   ├── session.py
│   │           │   ├── stats.py
│   │           │   ├── storage
│   │           │   │   ├── __init__.py
│   │           │   │   ├── elasticsearch.py
│   │           │   │   └── file.py
│   │           │   ├── table.py
│   │           │   ├── timers.py
│   │           │   └── utils.py
│   │           ├── pytest_benchmark-5.1.0.dist-info
│   │           │   ├── AUTHORS.rst
│   │           │   ├── INSTALLER
│   │           │   ├── LICENSE
│   │           │   ├── METADATA
│   │           │   ├── RECORD
│   │           │   ├── REQUESTED
│   │           │   ├── WHEEL
│   │           │   ├── entry_points.txt
│   │           │   └── top_level.txt
│   │           ├── pytest_cov
│   │           │   ├── __init__.py
│   │           │   ├── compat.py
│   │           │   ├── embed.py
│   │           │   ├── engine.py
│   │           │   └── plugin.py
│   │           ├── pytest_cov-6.0.0.dist-info
│   │           │   ├── AUTHORS.rst
│   │           │   ├── INSTALLER
│   │           │   ├── LICENSE
│   │           │   ├── METADATA
│   │           │   ├── RECORD
│   │           │   ├── REQUESTED
│   │           │   ├── WHEEL
│   │           │   ├── entry_points.txt
│   │           │   └── top_level.txt
│   │           ├── pytest_xdist-3.6.1.dist-info
│   │           │   ├── INSTALLER
│   │           │   ├── LICENSE
│   │           │   ├── METADATA
│   │           │   ├── RECORD
│   │           │   ├── REQUESTED
│   │           │   ├── WHEEL
│   │           │   ├── entry_points.txt
│   │           │   └── top_level.txt
│   │           ├── python_dotenv-1.0.1.dist-info
│   │           │   ├── INSTALLER
│   │           │   ├── LICENSE
│   │           │   ├── METADATA
│   │           │   ├── RECORD
│   │           │   ├── REQUESTED
│   │           │   ├── WHEEL
│   │           │   ├── entry_points.txt
│   │           │   └── top_level.txt
│   │           ├── ruff
│   │           │   ├── __init__.py
│   │           │   └── __main__.py
│   │           ├── ruff-0.9.6.dist-info
│   │           │   ├── INSTALLER
│   │           │   ├── METADATA
│   │           │   ├── RECORD
│   │           │   ├── REQUESTED
│   │           │   ├── WHEEL
│   │           │   └── licenses
│   │           │       └── LICENSE
│   │           ├── setuptools
│   │           │   ├── __init__.py
│   │           │   ├── _core_metadata.py
│   │           │   ├── _distutils
│   │           │   │   ├── __init__.py
│   │           │   │   ├── _log.py
│   │           │   │   ├── _macos_compat.py
│   │           │   │   ├── _modified.py
│   │           │   │   ├── _msvccompiler.py
│   │           │   │   ├── archive_util.py
│   │           │   │   ├── ccompiler.py
│   │           │   │   ├── cmd.py
│   │           │   │   ├── command
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   ├── _framework_compat.py
│   │           │   │   │   ├── bdist.py
│   │           │   │   │   ├── bdist_dumb.py
│   │           │   │   │   ├── bdist_rpm.py
│   │           │   │   │   ├── build.py
│   │           │   │   │   ├── build_clib.py
│   │           │   │   │   ├── build_ext.py
│   │           │   │   │   ├── build_py.py
│   │           │   │   │   ├── build_scripts.py
│   │           │   │   │   ├── check.py
│   │           │   │   │   ├── clean.py
│   │           │   │   │   ├── config.py
│   │           │   │   │   ├── install.py
│   │           │   │   │   ├── install_data.py
│   │           │   │   │   ├── install_egg_info.py
│   │           │   │   │   ├── install_headers.py
│   │           │   │   │   ├── install_lib.py
│   │           │   │   │   ├── install_scripts.py
│   │           │   │   │   └── sdist.py
│   │           │   │   ├── compat
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   └── py39.py
│   │           │   │   ├── core.py
│   │           │   │   ├── cygwinccompiler.py
│   │           │   │   ├── debug.py
│   │           │   │   ├── dep_util.py
│   │           │   │   ├── dir_util.py
│   │           │   │   ├── dist.py
│   │           │   │   ├── errors.py
│   │           │   │   ├── extension.py
│   │           │   │   ├── fancy_getopt.py
│   │           │   │   ├── file_util.py
│   │           │   │   ├── filelist.py
│   │           │   │   ├── log.py
│   │           │   │   ├── spawn.py
│   │           │   │   ├── sysconfig.py
│   │           │   │   ├── tests
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   ├── compat
│   │           │   │   │   │   ├── __init__.py
│   │           │   │   │   │   └── py39.py
│   │           │   │   │   ├── support.py
│   │           │   │   │   ├── test_archive_util.py
│   │           │   │   │   ├── test_bdist.py
│   │           │   │   │   ├── test_bdist_dumb.py
│   │           │   │   │   ├── test_bdist_rpm.py
│   │           │   │   │   ├── test_build.py
│   │           │   │   │   ├── test_build_clib.py
│   │           │   │   │   ├── test_build_ext.py
│   │           │   │   │   ├── test_build_py.py
│   │           │   │   │   ├── test_build_scripts.py
│   │           │   │   │   ├── test_ccompiler.py
│   │           │   │   │   ├── test_check.py
│   │           │   │   │   ├── test_clean.py
│   │           │   │   │   ├── test_cmd.py
│   │           │   │   │   ├── test_config_cmd.py
│   │           │   │   │   ├── test_core.py
│   │           │   │   │   ├── test_cygwinccompiler.py
│   │           │   │   │   ├── test_dir_util.py
│   │           │   │   │   ├── test_dist.py
│   │           │   │   │   ├── test_extension.py
│   │           │   │   │   ├── test_file_util.py
│   │           │   │   │   ├── test_filelist.py
│   │           │   │   │   ├── test_install.py
│   │           │   │   │   ├── test_install_data.py
│   │           │   │   │   ├── test_install_headers.py
│   │           │   │   │   ├── test_install_lib.py
│   │           │   │   │   ├── test_install_scripts.py
│   │           │   │   │   ├── test_log.py
│   │           │   │   │   ├── test_mingwccompiler.py
│   │           │   │   │   ├── test_modified.py
│   │           │   │   │   ├── test_msvccompiler.py
│   │           │   │   │   ├── test_sdist.py
│   │           │   │   │   ├── test_spawn.py
│   │           │   │   │   ├── test_sysconfig.py
│   │           │   │   │   ├── test_text_file.py
│   │           │   │   │   ├── test_unixccompiler.py
│   │           │   │   │   ├── test_util.py
│   │           │   │   │   ├── test_version.py
│   │           │   │   │   ├── test_versionpredicate.py
│   │           │   │   │   └── unix_compat.py
│   │           │   │   ├── text_file.py
│   │           │   │   ├── unixccompiler.py
│   │           │   │   ├── util.py
│   │           │   │   ├── version.py
│   │           │   │   ├── versionpredicate.py
│   │           │   │   └── zosccompiler.py
│   │           │   ├── _entry_points.py
│   │           │   ├── _imp.py
│   │           │   ├── _importlib.py
│   │           │   ├── _itertools.py
│   │           │   ├── _normalization.py
│   │           │   ├── _path.py
│   │           │   ├── _reqs.py
│   │           │   ├── _shutil.py
│   │           │   ├── _static.py
│   │           │   ├── _vendor
│   │           │   │   ├── autocommand
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   ├── autoasync.py
│   │           │   │   │   ├── autocommand.py
│   │           │   │   │   ├── automain.py
│   │           │   │   │   ├── autoparse.py
│   │           │   │   │   └── errors.py
│   │           │   │   ├── autocommand-2.2.2.dist-info
│   │           │   │   │   ├── INSTALLER
│   │           │   │   │   ├── LICENSE
│   │           │   │   │   ├── METADATA
│   │           │   │   │   ├── RECORD
│   │           │   │   │   ├── WHEEL
│   │           │   │   │   └── top_level.txt
│   │           │   │   ├── backports
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   └── tarfile
│   │           │   │   │       ├── __init__.py
│   │           │   │   │       ├── __main__.py
│   │           │   │   │       └── compat
│   │           │   │   │           ├── __init__.py
│   │           │   │   │           └── py38.py
│   │           │   │   ├── backports.tarfile-1.2.0.dist-info
│   │           │   │   │   ├── INSTALLER
│   │           │   │   │   ├── LICENSE
│   │           │   │   │   ├── METADATA
│   │           │   │   │   ├── RECORD
│   │           │   │   │   ├── REQUESTED
│   │           │   │   │   ├── WHEEL
│   │           │   │   │   └── top_level.txt
│   │           │   │   ├── importlib_metadata
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   ├── _adapters.py
│   │           │   │   │   ├── _collections.py
│   │           │   │   │   ├── _compat.py
│   │           │   │   │   ├── _functools.py
│   │           │   │   │   ├── _itertools.py
│   │           │   │   │   ├── _meta.py
│   │           │   │   │   ├── _text.py
│   │           │   │   │   ├── compat
│   │           │   │   │   │   ├── __init__.py
│   │           │   │   │   │   ├── py311.py
│   │           │   │   │   │   └── py39.py
│   │           │   │   │   ├── diagnose.py
│   │           │   │   │   └── py.typed
│   │           │   │   ├── importlib_metadata-8.0.0.dist-info
│   │           │   │   │   ├── INSTALLER
│   │           │   │   │   ├── LICENSE
│   │           │   │   │   ├── METADATA
│   │           │   │   │   ├── RECORD
│   │           │   │   │   ├── REQUESTED
│   │           │   │   │   ├── WHEEL
│   │           │   │   │   └── top_level.txt
│   │           │   │   ├── inflect
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   ├── compat
│   │           │   │   │   │   ├── __init__.py
│   │           │   │   │   │   └── py38.py
│   │           │   │   │   └── py.typed
│   │           │   │   ├── inflect-7.3.1.dist-info
│   │           │   │   │   ├── INSTALLER
│   │           │   │   │   ├── LICENSE
│   │           │   │   │   ├── METADATA
│   │           │   │   │   ├── RECORD
│   │           │   │   │   ├── WHEEL
│   │           │   │   │   └── top_level.txt
│   │           │   │   ├── jaraco
│   │           │   │   │   ├── collections
│   │           │   │   │   │   ├── __init__.py
│   │           │   │   │   │   └── py.typed
│   │           │   │   │   ├── context.py
│   │           │   │   │   ├── functools
│   │           │   │   │   │   ├── __init__.py
│   │           │   │   │   │   ├── __init__.pyi
│   │           │   │   │   │   └── py.typed
│   │           │   │   │   └── text
│   │           │   │   │       ├── Lorem ipsum.txt
│   │           │   │   │       ├── __init__.py
│   │           │   │   │       ├── layouts.py
│   │           │   │   │       ├── show-newlines.py
│   │           │   │   │       ├── strip-prefix.py
│   │           │   │   │       ├── to-dvorak.py
│   │           │   │   │       └── to-qwerty.py
│   │           │   │   ├── jaraco.collections-5.1.0.dist-info
│   │           │   │   │   ├── INSTALLER
│   │           │   │   │   ├── LICENSE
│   │           │   │   │   ├── METADATA
│   │           │   │   │   ├── RECORD
│   │           │   │   │   ├── REQUESTED
│   │           │   │   │   ├── WHEEL
│   │           │   │   │   └── top_level.txt
│   │           │   │   ├── jaraco.context-5.3.0.dist-info
│   │           │   │   │   ├── INSTALLER
│   │           │   │   │   ├── LICENSE
│   │           │   │   │   ├── METADATA
│   │           │   │   │   ├── RECORD
│   │           │   │   │   ├── WHEEL
│   │           │   │   │   └── top_level.txt
│   │           │   │   ├── jaraco.functools-4.0.1.dist-info
│   │           │   │   │   ├── INSTALLER
│   │           │   │   │   ├── LICENSE
│   │           │   │   │   ├── METADATA
│   │           │   │   │   ├── RECORD
│   │           │   │   │   ├── WHEEL
│   │           │   │   │   └── top_level.txt
│   │           │   │   ├── jaraco.text-3.12.1.dist-info
│   │           │   │   │   ├── INSTALLER
│   │           │   │   │   ├── LICENSE
│   │           │   │   │   ├── METADATA
│   │           │   │   │   ├── RECORD
│   │           │   │   │   ├── REQUESTED
│   │           │   │   │   ├── WHEEL
│   │           │   │   │   └── top_level.txt
│   │           │   │   ├── more_itertools
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   ├── __init__.pyi
│   │           │   │   │   ├── more.py
│   │           │   │   │   ├── more.pyi
│   │           │   │   │   ├── py.typed
│   │           │   │   │   ├── recipes.py
│   │           │   │   │   └── recipes.pyi
│   │           │   │   ├── more_itertools-10.3.0.dist-info
│   │           │   │   │   ├── INSTALLER
│   │           │   │   │   ├── LICENSE
│   │           │   │   │   ├── METADATA
│   │           │   │   │   ├── RECORD
│   │           │   │   │   ├── REQUESTED
│   │           │   │   │   └── WHEEL
│   │           │   │   ├── packaging
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   ├── _elffile.py
│   │           │   │   │   ├── _manylinux.py
│   │           │   │   │   ├── _musllinux.py
│   │           │   │   │   ├── _parser.py
│   │           │   │   │   ├── _structures.py
│   │           │   │   │   ├── _tokenizer.py
│   │           │   │   │   ├── licenses
│   │           │   │   │   │   ├── __init__.py
│   │           │   │   │   │   └── _spdx.py
│   │           │   │   │   ├── markers.py
│   │           │   │   │   ├── metadata.py
│   │           │   │   │   ├── py.typed
│   │           │   │   │   ├── requirements.py
│   │           │   │   │   ├── specifiers.py
│   │           │   │   │   ├── tags.py
│   │           │   │   │   ├── utils.py
│   │           │   │   │   └── version.py
│   │           │   │   ├── packaging-24.2.dist-info
│   │           │   │   │   ├── INSTALLER
│   │           │   │   │   ├── LICENSE
│   │           │   │   │   ├── LICENSE.APACHE
│   │           │   │   │   ├── LICENSE.BSD
│   │           │   │   │   ├── METADATA
│   │           │   │   │   ├── RECORD
│   │           │   │   │   ├── REQUESTED
│   │           │   │   │   └── WHEEL
│   │           │   │   ├── platformdirs
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   ├── __main__.py
│   │           │   │   │   ├── android.py
│   │           │   │   │   ├── api.py
│   │           │   │   │   ├── macos.py
│   │           │   │   │   ├── py.typed
│   │           │   │   │   ├── unix.py
│   │           │   │   │   ├── version.py
│   │           │   │   │   └── windows.py
│   │           │   │   ├── platformdirs-4.2.2.dist-info
│   │           │   │   │   ├── INSTALLER
│   │           │   │   │   ├── METADATA
│   │           │   │   │   ├── RECORD
│   │           │   │   │   ├── REQUESTED
│   │           │   │   │   ├── WHEEL
│   │           │   │   │   └── licenses
│   │           │   │   │       └── LICENSE
│   │           │   │   ├── tomli
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   ├── _parser.py
│   │           │   │   │   ├── _re.py
│   │           │   │   │   ├── _types.py
│   │           │   │   │   └── py.typed
│   │           │   │   ├── tomli-2.0.1.dist-info
│   │           │   │   │   ├── INSTALLER
│   │           │   │   │   ├── LICENSE
│   │           │   │   │   ├── METADATA
│   │           │   │   │   ├── RECORD
│   │           │   │   │   ├── REQUESTED
│   │           │   │   │   └── WHEEL
│   │           │   │   ├── typeguard
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   ├── _checkers.py
│   │           │   │   │   ├── _config.py
│   │           │   │   │   ├── _decorators.py
│   │           │   │   │   ├── _exceptions.py
│   │           │   │   │   ├── _functions.py
│   │           │   │   │   ├── _importhook.py
│   │           │   │   │   ├── _memo.py
│   │           │   │   │   ├── _pytest_plugin.py
│   │           │   │   │   ├── _suppression.py
│   │           │   │   │   ├── _transformer.py
│   │           │   │   │   ├── _union_transformer.py
│   │           │   │   │   ├── _utils.py
│   │           │   │   │   └── py.typed
│   │           │   │   ├── typeguard-4.3.0.dist-info
│   │           │   │   │   ├── INSTALLER
│   │           │   │   │   ├── LICENSE
│   │           │   │   │   ├── METADATA
│   │           │   │   │   ├── RECORD
│   │           │   │   │   ├── WHEEL
│   │           │   │   │   ├── entry_points.txt
│   │           │   │   │   └── top_level.txt
│   │           │   │   ├── typing_extensions-4.12.2.dist-info
│   │           │   │   │   ├── INSTALLER
│   │           │   │   │   ├── LICENSE
│   │           │   │   │   ├── METADATA
│   │           │   │   │   ├── RECORD
│   │           │   │   │   └── WHEEL
│   │           │   │   ├── typing_extensions.py
│   │           │   │   ├── wheel
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   ├── __main__.py
│   │           │   │   │   ├── _setuptools_logging.py
│   │           │   │   │   ├── bdist_wheel.py
│   │           │   │   │   ├── cli
│   │           │   │   │   │   ├── __init__.py
│   │           │   │   │   │   ├── convert.py
│   │           │   │   │   │   ├── pack.py
│   │           │   │   │   │   ├── tags.py
│   │           │   │   │   │   └── unpack.py
│   │           │   │   │   ├── macosx_libfile.py
│   │           │   │   │   ├── metadata.py
│   │           │   │   │   ├── util.py
│   │           │   │   │   ├── vendored
│   │           │   │   │   │   ├── __init__.py
│   │           │   │   │   │   ├── packaging
│   │           │   │   │   │   │   ├── __init__.py
│   │           │   │   │   │   │   ├── _elffile.py
│   │           │   │   │   │   │   ├── _manylinux.py
│   │           │   │   │   │   │   ├── _musllinux.py
│   │           │   │   │   │   │   ├── _parser.py
│   │           │   │   │   │   │   ├── _structures.py
│   │           │   │   │   │   │   ├── _tokenizer.py
│   │           │   │   │   │   │   ├── markers.py
│   │           │   │   │   │   │   ├── requirements.py
│   │           │   │   │   │   │   ├── specifiers.py
│   │           │   │   │   │   │   ├── tags.py
│   │           │   │   │   │   │   ├── utils.py
│   │           │   │   │   │   │   └── version.py
│   │           │   │   │   │   └── vendor.txt
│   │           │   │   │   └── wheelfile.py
│   │           │   │   ├── wheel-0.43.0.dist-info
│   │           │   │   │   ├── INSTALLER
│   │           │   │   │   ├── LICENSE.txt
│   │           │   │   │   ├── METADATA
│   │           │   │   │   ├── RECORD
│   │           │   │   │   ├── REQUESTED
│   │           │   │   │   ├── WHEEL
│   │           │   │   │   └── entry_points.txt
│   │           │   │   ├── zipp
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   ├── compat
│   │           │   │   │   │   ├── __init__.py
│   │           │   │   │   │   └── py310.py
│   │           │   │   │   └── glob.py
│   │           │   │   └── zipp-3.19.2.dist-info
│   │           │   │       ├── INSTALLER
│   │           │   │       ├── LICENSE
│   │           │   │       ├── METADATA
│   │           │   │       ├── RECORD
│   │           │   │       ├── REQUESTED
│   │           │   │       ├── WHEEL
│   │           │   │       └── top_level.txt
│   │           │   ├── archive_util.py
│   │           │   ├── build_meta.py
│   │           │   ├── cli-32.exe
│   │           │   ├── cli-64.exe
│   │           │   ├── cli-arm64.exe
│   │           │   ├── cli.exe
│   │           │   ├── command
│   │           │   │   ├── __init__.py
│   │           │   │   ├── _requirestxt.py
│   │           │   │   ├── alias.py
│   │           │   │   ├── bdist_egg.py
│   │           │   │   ├── bdist_rpm.py
│   │           │   │   ├── bdist_wheel.py
│   │           │   │   ├── build.py
│   │           │   │   ├── build_clib.py
│   │           │   │   ├── build_ext.py
│   │           │   │   ├── build_py.py
│   │           │   │   ├── develop.py
│   │           │   │   ├── dist_info.py
│   │           │   │   ├── easy_install.py
│   │           │   │   ├── editable_wheel.py
│   │           │   │   ├── egg_info.py
│   │           │   │   ├── install.py
│   │           │   │   ├── install_egg_info.py
│   │           │   │   ├── install_lib.py
│   │           │   │   ├── install_scripts.py
│   │           │   │   ├── launcher manifest.xml
│   │           │   │   ├── rotate.py
│   │           │   │   ├── saveopts.py
│   │           │   │   ├── sdist.py
│   │           │   │   ├── setopt.py
│   │           │   │   └── test.py
│   │           │   ├── compat
│   │           │   │   ├── __init__.py
│   │           │   │   ├── py310.py
│   │           │   │   ├── py311.py
│   │           │   │   ├── py312.py
│   │           │   │   └── py39.py
│   │           │   ├── config
│   │           │   │   ├── NOTICE
│   │           │   │   ├── __init__.py
│   │           │   │   ├── _apply_pyprojecttoml.py
│   │           │   │   ├── _validate_pyproject
│   │           │   │   │   ├── NOTICE
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   ├── error_reporting.py
│   │           │   │   │   ├── extra_validations.py
│   │           │   │   │   ├── fastjsonschema_exceptions.py
│   │           │   │   │   ├── fastjsonschema_validations.py
│   │           │   │   │   └── formats.py
│   │           │   │   ├── distutils.schema.json
│   │           │   │   ├── expand.py
│   │           │   │   ├── pyprojecttoml.py
│   │           │   │   ├── setupcfg.py
│   │           │   │   └── setuptools.schema.json
│   │           │   ├── depends.py
│   │           │   ├── discovery.py
│   │           │   ├── dist.py
│   │           │   ├── errors.py
│   │           │   ├── extension.py
│   │           │   ├── glob.py
│   │           │   ├── gui-32.exe
│   │           │   ├── gui-64.exe
│   │           │   ├── gui-arm64.exe
│   │           │   ├── gui.exe
│   │           │   ├── installer.py
│   │           │   ├── launch.py
│   │           │   ├── logging.py
│   │           │   ├── modified.py
│   │           │   ├── monkey.py
│   │           │   ├── msvc.py
│   │           │   ├── namespaces.py
│   │           │   ├── package_index.py
│   │           │   ├── sandbox.py
│   │           │   ├── script (dev).tmpl
│   │           │   ├── script.tmpl
│   │           │   ├── tests
│   │           │   │   ├── __init__.py
│   │           │   │   ├── compat
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   └── py39.py
│   │           │   │   ├── config
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   ├── downloads
│   │           │   │   │   │   ├── __init__.py
│   │           │   │   │   │   └── preload.py
│   │           │   │   │   ├── setupcfg_examples.txt
│   │           │   │   │   ├── test_apply_pyprojecttoml.py
│   │           │   │   │   ├── test_expand.py
│   │           │   │   │   ├── test_pyprojecttoml.py
│   │           │   │   │   ├── test_pyprojecttoml_dynamic_deps.py
│   │           │   │   │   └── test_setupcfg.py
│   │           │   │   ├── contexts.py
│   │           │   │   ├── environment.py
│   │           │   │   ├── fixtures.py
│   │           │   │   ├── indexes
│   │           │   │   │   └── test_links_priority
│   │           │   │   │       ├── external.html
│   │           │   │   │       └── simple
│   │           │   │   │           └── foobar
│   │           │   │   │               └── index.html
│   │           │   │   ├── integration
│   │           │   │   │   ├── __init__.py
│   │           │   │   │   ├── helpers.py
│   │           │   │   │   └── test_pip_install_sdist.py
│   │           │   │   ├── mod_with_constant.py
│   │           │   │   ├── namespaces.py
│   │           │   │   ├── script-with-bom.py
│   │           │   │   ├── server.py
│   │           │   │   ├── test_archive_util.py
│   │           │   │   ├── test_bdist_deprecations.py
│   │           │   │   ├── test_bdist_egg.py
│   │           │   │   ├── test_bdist_wheel.py
│   │           │   │   ├── test_build.py
│   │           │   │   ├── test_build_clib.py
│   │           │   │   ├── test_build_ext.py
│   │           │   │   ├── test_build_meta.py
│   │           │   │   ├── test_build_py.py
│   │           │   │   ├── test_config_discovery.py
│   │           │   │   ├── test_core_metadata.py
│   │           │   │   ├── test_depends.py
│   │           │   │   ├── test_develop.py
│   │           │   │   ├── test_dist.py
│   │           │   │   ├── test_dist_info.py
│   │           │   │   ├── test_distutils_adoption.py
│   │           │   │   ├── test_easy_install.py
│   │           │   │   ├── test_editable_install.py
│   │           │   │   ├── test_egg_info.py
│   │           │   │   ├── test_extern.py
│   │           │   │   ├── test_find_packages.py
│   │           │   │   ├── test_find_py_modules.py
│   │           │   │   ├── test_glob.py
│   │           │   │   ├── test_install_scripts.py
│   │           │   │   ├── test_logging.py
│   │           │   │   ├── test_manifest.py
│   │           │   │   ├── test_namespaces.py
│   │           │   │   ├── test_packageindex.py
│   │           │   │   ├── test_sandbox.py
│   │           │   │   ├── test_sdist.py
│   │           │   │   ├── test_setopt.py
│   │           │   │   ├── test_setuptools.py
│   │           │   │   ├── test_shutil_wrapper.py
│   │           │   │   ├── test_unicode_utils.py
│   │           │   │   ├── test_virtualenv.py
│   │           │   │   ├── test_warnings.py
│   │           │   │   ├── test_wheel.py
│   │           │   │   ├── test_windows_wrappers.py
│   │           │   │   ├── text.py
│   │           │   │   └── textwrap.py
│   │           │   ├── unicode_utils.py
│   │           │   ├── version.py
│   │           │   ├── warnings.py
│   │           │   ├── wheel.py
│   │           │   └── windows_support.py
│   │           ├── setuptools-75.8.0.dist-info
│   │           │   ├── INSTALLER
│   │           │   ├── LICENSE
│   │           │   ├── METADATA
│   │           │   ├── RECORD
│   │           │   ├── REQUESTED
│   │           │   ├── WHEEL
│   │           │   ├── entry_points.txt
│   │           │   └── top_level.txt
│   │           ├── twat_cache-0.1.0.dist-info
│   │           │   ├── INSTALLER
│   │           │   ├── METADATA
│   │           │   ├── RECORD
│   │           │   ├── REQUESTED
│   │           │   ├── WHEEL
│   │           │   ├── direct_url.json
│   │           │   ├── entry_points.txt
│   │           │   ├── licenses
│   │           │   │   └── LICENSE
│   │           │   └── uv_cache.json
│   │           ├── typing_extensions-4.12.2.dist-info
│   │           │   ├── INSTALLER
│   │           │   ├── LICENSE
│   │           │   ├── METADATA
│   │           │   ├── RECORD
│   │           │   ├── REQUESTED
│   │           │   └── WHEEL
│   │           ├── typing_extensions.py
│   │           ├── xdist
│   │           │   ├── __init__.py
│   │           │   ├── _path.py
│   │           │   ├── _version.py
│   │           │   ├── dsession.py
│   │           │   ├── looponfail.py
│   │           │   ├── newhooks.py
│   │           │   ├── plugin.py
│   │           │   ├── remote.py
│   │           │   ├── report.py
│   │           │   ├── scheduler
│   │           │   │   ├── __init__.py
│   │           │   │   ├── each.py
│   │           │   │   ├── load.py
│   │           │   │   ├── loadfile.py
│   │           │   │   ├── loadgroup.py
│   │           │   │   ├── loadscope.py
│   │           │   │   ├── protocol.py
│   │           │   │   └── worksteal.py
│   │           │   └── workermanage.py
│   │           ├── zipp
│   │           │   ├── __init__.py
│   │           │   ├── _functools.py
│   │           │   ├── compat
│   │           │   │   ├── __init__.py
│   │           │   │   ├── overlay.py
│   │           │   │   └── py310.py
│   │           │   └── glob.py
│   │           └── zipp-3.21.0.dist-info
│   │               ├── INSTALLER
│   │               ├── LICENSE
│   │               ├── METADATA
│   │               ├── RECORD
│   │               ├── REQUESTED
│   │               ├── WHEEL
│   │               └── top_level.txt
│   └── pyvenv.cfg
├── DEPENDENCIES.txt
├── LICENSE
├── LOG.md
├── README.md
├── TODO.md
├── VERSION.txt
├── dist
│   ├── .gitignore
│   ├── twat_cache-0.1.0-py3-none-any.whl
│   ├── twat_cache-0.1.0.tar.gz
│   ├── twat_cache-1.8.1-py3-none-any.whl
│   └── twat_cache-1.8.1.tar.gz
├── pyproject.toml
├── src
│   ├── .DS_Store
│   └── twat_cache
│       ├── .DS_Store
│       ├── __init__.py
│       ├── __main__.py
│       ├── __pycache__
│       │   ├── __init__.cpython-312.pyc
│       │   ├── __version__.cpython-312.pyc
│       │   ├── cache.cpython-312.pyc
│       │   ├── config.cpython-312.pyc
│       │   ├── decorators.cpython-312.pyc
│       │   ├── paths.cpython-312.pyc
│       │   ├── types.cpython-312.pyc
│       │   └── utils.cpython-312.pyc
│       ├── __version__.py
│       ├── cache.py
│       ├── config.py
│       ├── decorators.py
│       ├── engines
│       │   ├── __init__.py
│       │   ├── __pycache__
│       │   │   ├── __init__.cpython-312.pyc
│       │   │   ├── aiocache.cpython-312.pyc
│       │   │   ├── base.cpython-312.pyc
│       │   │   ├── cachebox.cpython-312.pyc
│       │   │   ├── cachetools.cpython-312.pyc
│       │   │   ├── diskcache.cpython-312.pyc
│       │   │   ├── functools.cpython-312.pyc
│       │   │   ├── joblib.cpython-312.pyc
│       │   │   ├── klepto.cpython-312.pyc
│       │   │   ├── lru.cpython-312.pyc
│       │   │   └── manager.cpython-312.pyc
│       │   ├── aiocache.py
│       │   ├── base.py
│       │   ├── cachebox.py
│       │   ├── cachetools.py
│       │   ├── diskcache.py
│       │   ├── functools.py
│       │   ├── joblib.py
│       │   ├── klepto.py
│       │   ├── manager.py
│       │   └── py.typed
│       ├── paths.py
│       ├── py.typed
│       ├── types.py
│       └── utils.py
└── tests
    ├── .DS_Store
    ├── __pycache__
    │   ├── test_cache.cpython-312-pytest-8.3.4.pyc
    │   ├── test_config.cpython-312-pytest-8.3.4.pyc
    │   ├── test_engines.cpython-312-pytest-8.3.4.pyc
    │   └── test_twat_cache.cpython-312-pytest-8.3.4.pyc
    ├── test_cache.py
    ├── test_config.py
    ├── test_engines.py
    └── test_twat_cache.py

366 directories, 3721 files