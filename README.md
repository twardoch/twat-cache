# twat-cache: Flexible Caching for Python

**Part of the [twat](https://pypi.org/project/twat/) collection of Python utilities.**

`twat-cache` is a versatile and high-performance Python library designed to simplify caching for your functions. It provides a unified and easy-to-use interface to various caching backends, allowing you to speed up your applications by storing and retrieving the results of expensive computations without significant code changes.

## What is `twat-cache`?

At its core, `twat-cache` offers a set of decorators that you can apply to your Python functions. When a decorated function is called, `twat-cache` checks if the result for the given arguments already exists in its cache. If so, it returns the cached result immediately, bypassing the actual function execution. If not, the function executes, and its result is stored in the cache for future calls.

This mechanism can drastically reduce execution time for functions that are called repeatedly with the same inputs, especially if those functions perform I/O operations (like web requests or database queries) or complex calculations.

## Who is it for?

`twat-cache` is for Python developers who want to:

*   Improve the performance and responsiveness of their applications.
*   Reduce redundant computations or data fetching.
*   Simplify the implementation of caching logic.
*   Have the flexibility to choose from different caching strategies (in-memory, disk-based, file-based) without rewriting their code.
*   Work with both synchronous and asynchronous Python code.

Whether you're building web applications, data processing pipelines, scientific computing tools, or any Python project where performance matters, `twat-cache` can be a valuable addition.

## Why is it useful?

*   **Unified Interface:** Learn one way to cache, and apply it across multiple cache engines.
*   **Automatic Engine Selection:** The `ucache` (universal cache) decorator can intelligently pick a suitable cache engine, or you can explicitly choose one.
*   **Multiple Cache Engines & Backends:** Supports several caching strategies by integrating with robust backend libraries:
    *   In-memory (LRU, LFU, FIFO policies via `cachetools` library, or high-performance `cachebox` library)
    *   Disk-based (persistent caching via `diskcache` library)
    *   File-based (efficient for large objects like NumPy arrays via `joblib` library)
    *   Asynchronous caching (for `async/await` functions via `aiocache` library)
*   **Fallback Mechanism:** If a preferred cache engine or its underlying backend library isn't available, `twat-cache` gracefully falls back to a functional alternative.
*   **Configurable:** Control cache size (`maxsize`), time-to-live (`ttl`) for entries, eviction policies, and more.
*   **Context Management:** Provides `CacheContext` for fine-grained control over cache engine lifecycles and configurations within specific code blocks.
*   **Modern Python:** Built with type hints and supports modern Python features.
*   **Part of a Larger Ecosystem:** As a component of the `twat` project, it aims for consistency and quality within that suite of tools.

## Installation

You can install `twat-cache` using pip.

**Basic Installation (includes in-memory and basic disk caching capabilities):**

```bash
pip install twat-cache
```

This installs `twat-cache` along with `pydantic`, `loguru`, `diskcache`, `joblib`, and `cachetools`.

**To include all optional backend libraries for extended capabilities:**

```bash
pip install twat-cache[all]
```
This adds support for `cachebox`, `aiocache`, `klepto`, and `platformdirs`.

**To install support for specific optional backend libraries:**

Choose the backend libraries that enable the cache engines you need:

*   **cachebox (High-performance Rust-based in-memory cache):**
    ```bash
    pip install twat-cache[cachebox]
    ```
*   **aiocache (Async-capable caching):**
    ```bash
    pip install twat-cache[aiocache]
    ```
*   **klepto (Scientific computing caching, various storage options):**
    ```bash
    pip install twat-cache[klepto]
    ```

*Note on Redis:* Previous versions or documentation might have mentioned a Redis cache engine. Currently, the direct implementation for a Redis engine (`redis.py`) is not present in the core `twat_cache.engines` directory. While `pyproject.toml` might list a `redis` extra, ensure the `redis-py` (or equivalent) package is installed and that `twat-cache` explicitly supports it in the version you are using if Redis is a requirement. The `CacheEngineManager` has a provision to load a Redis engine, but the engine code itself must be available.

## How to Use `twat-cache`

`twat-cache` is primarily used as a library by importing its decorators and context managers into your Python code. It does not currently offer a standalone command-line interface for direct cache manipulation outside of a Python script.

### Programmatic Usage (Examples)

Here are some common ways to use `twat-cache`:

**1. In-Memory Caching (`mcache`)**

Ideal for fast, temporary caching of frequently accessed, small-to-medium sized data within a single process.

```python
from twat_cache import mcache
import time

@mcache(maxsize=128, ttl=60) # Cache up to 128 items, expire after 60 seconds
def get_user_details(user_id: int) -> dict:
    print(f"Fetching details for user {user_id}...")
    time.sleep(1) # Simulate expensive operation
    return {"id": user_id, "name": f"User {user_id}", "email": f"user{user_id}@example.com"}

# First call: fetches and caches
user1 = get_user_details(1)
print(user1)

# Second call: result comes from cache
user1_cached = get_user_details(1)
print(user1_cached)

# After 60 seconds, or if maxsize is exceeded, the cache entry might be evicted.
```

**2. Disk-Based Caching (`bcache`)**

Useful for persistent caching across application restarts or for larger datasets that don't fit comfortably in memory. Uses the `diskcache` library.

```python
from twat_cache import bcache
import time

@bcache(folder_name="user_data_cache", ttl=3600) # Cache in '.cache/twat_cache/user_data_cache', expire after 1 hour
def get_report_data(report_id: str) -> list:
    print(f"Generating report {report_id}...")
    time.sleep(2) # Simulate expensive report generation
    return [{"report": report_id, "data_point": i} for i in range(5)]

# First call: generates and caches to disk
report_A = get_report_data("A")
print(report_A)

# Second call (even after script restart): result comes from disk cache
report_A_cached = get_report_data("A")
print(report_A_cached)
```

**3. File-Based Caching for Large Objects (`fcache`)**

Optimized for caching large objects like NumPy arrays or machine learning models, typically using the `joblib` library.

```python
from twat_cache import fcache
import numpy as np
import time

@fcache(folder_name="array_processing_cache", compress=True) # Compress cached files
def process_large_array(size: int) -> np.ndarray:
    print(f"Processing large array of size {size}x{size}...")
    time.sleep(3) # Simulate heavy computation
    return np.random.rand(size, size)

# First call: computes and caches the array to a file
array_data = process_large_array(1000)
print(array_data.shape)

# Second call: loads the array from the cached file
array_data_cached = process_large_array(1000)
print(array_data_cached.shape)
```

**4. Asynchronous Caching (`acache`)**

For caching results of `async` functions, typically using the `aiocache` library.

```python
from twat_cache import acache
import asyncio
import time

@acache(ttl=300) # Cache async results for 5 minutes
async def fetch_external_data(url: str) -> dict:
    print(f"Fetching data from {url}...")
    await asyncio.sleep(1) # Simulate async HTTP request
    return {"url": url, "content": f"Data from {url}"}

async def main():
    # First call: fetches and caches
    data1 = await fetch_external_data("https://api.example.com/data")
    print(data1)

    # Second call: result comes from cache
    data1_cached = await fetch_external_data("https://api.example.com/data")
    print(data1_cached)

if __name__ == "__main__":
    asyncio.run(main())
```

**5. Universal Caching (`ucache`)**

Let `twat-cache` attempt to pick the best cache engine based on availability and function characteristics.

```python
from twat_cache import ucache
import time

@ucache(ttl=1800, compress=True) # Universal cache, expire after 30 mins, try compression
def complex_calculation(a: int, b: float, c: str) -> str:
    print(f"Performing complex calculation with {a}, {b}, {c}...")
    time.sleep(1.5)
    return f"Result: {a * b} - {c.upper()}"

# twat-cache will choose an appropriate engine (e.g., DiskCacheEngine if available and suitable)
res1 = complex_calculation(10, 2.5, "hello")
print(res1)

res1_cached = complex_calculation(10, 2.5, "hello")
print(res1_cached)
```

**6. Using Cache Context (`CacheContext`)**

For more explicit control over caching within a specific block of code, or for using cache engines directly.

```python
from twat_cache import CacheContext
import time # Ensure time is imported for the example

def process_user_session(user_id: str, data: dict):
    # Use a specific disk cache for this operation
    with CacheContext(engine_name="diskcache", folder_name="session_cache", ttl=600) as cache:
        # 'cache' is the cache engine instance, allowing direct get/set.
        # For DiskCacheEngine, this would be a diskcache.Cache object.
        cache_key = f"session_data_{user_id}"

        cached_data = cache.get(cache_key)
        if cached_data:
            print(f"Using cached session data for {user_id}")
            return cached_data

        print(f"Processing and caching session data for {user_id}")
        # Simulate processing
        processed_data = {**data, "processed_at": time.time()}
        cache.set(cache_key, processed_data)
        return processed_data

user_data = {"preferences": "dark_mode"}
session_info = process_user_session("user123", user_data)
print(session_info)

session_info_cached = process_user_session("user123", user_data) # Should hit cache
print(session_info_cached)
```

## Technical Details

This section delves into the internal workings of `twat-cache`, its architecture, and guidelines for coding and contributing.

### How `twat-cache` Works

`twat-cache` is structured around a few key components: decorators, configuration objects, cache engines, and management utilities.

**1. Core Decorators (`src/twat_cache/decorators.py`)**

The primary interface for users. These decorators wrap user functions to inject caching logic.

*   **`@mcache` (Memory Cache):**
    *   Prioritizes fast in-memory cache engines.
    *   Order of preference: `CacheBoxEngine` (if `cachebox` library is available), then `CacheToolsEngine` (if `cachetools` is available), finally falls back to Python's built-in `functools.lru_cache` (via `FunctoolsEngine`).
    *   Configuration: `maxsize`, `ttl`, `policy` (LRU, LFU, FIFO, etc.), `secure` (key generation).
*   **`@bcache` (Basic Disk Cache):**
    *   Primarily uses `DiskCacheEngine` (which leverages the `diskcache` library) for persistent, SQLite-backed disk storage.
    *   If `diskcache` is unavailable but `klepto` is (and `use_sql=True` was passed, though this option is being de-emphasized), it can use `KleptoEngine` for SQL-based storage.
    *   Falls back to `@mcache` if no suitable disk-caching engine is found.
    *   Configuration: `folder_name`, `maxsize` (bytes on disk), `ttl`, `policy`, `use_sql` (for Klepto), `secure`.
*   **`@fcache` (File Cache):**
    *   Designed for large objects, often using serialization strategies suited for items like NumPy arrays.
    *   Prefers `JoblibEngine` (using `joblib.Memory`) for efficient file-based caching.
    *   Can fall back to `KleptoEngine` if `joblib` is not available.
    *   If neither is available, it falls back to `@mcache`.
    *   Configuration: `folder_name`, `maxsize`, `ttl`, `compress`, `secure`.
*   **`@acache` (Asynchronous Cache):**
    *   Specifically for `async def` functions.
    *   Uses `AioCacheEngine` (leveraging the `aiocache` library) if available.
    *   If `aiocache` is not available, it uses a synchronous memory cache (`mcache`) to wrap the async function. The caching mechanism then stores the result *after* the initial await, so subsequent calls with the same arguments will return the cached result without re-executing the async operation.
    *   Configuration: `maxsize`, `ttl`, `policy`.
*   **`@ucache` (Universal Cache):**
    *   The most flexible decorator. It attempts to select the "best" available cache engine.
    *   Selection logic (`_select_best_backend`): Considers if the function is async (prefers `AioCacheEngine`), if disk persistence seems beneficial (e.g., if `folder_name` is provided, hinting at `DiskCacheEngine`, `JoblibEngine`, or `KleptoEngine`), or defaults to fast in-memory options (`CacheBoxEngine`, `CacheToolsEngine`).
    *   Takes a wide range of configuration options applicable to various engines.
    *   The actual engine is instantiated via `_create_engine` based on the resolved configuration and selected backend name.

**2. Configuration (`src/twat_cache/config.py`)**

*   **`CacheConfig` (Pydantic Model):** A Pydantic model defines the structure for all cache configurations. This ensures type safety and validation for parameters like `maxsize`, `ttl`, `policy`, `folder_name`, `compress`, `secure`, and `preferred_engine`.
*   **`create_cache_config(...)`:** A factory function to easily construct `CacheConfig` objects.
*   Environment variables are not directly used for configuration by default, but `CacheConfig` could be extended or instantiated with values from environment variables programmatically if needed.
*   Redis-specific configurations were previously part of `CacheConfig` but have been removed, indicating a potential shift or pending refactor for Redis support.

**3. Cache Engines (`src/twat_cache/engines/`)**

This directory contains the actual caching logic implementations, abstracted via a common interface.

*   **`BaseCacheEngine` (Protocol):** Defines the contract for all cache engines. It's expected to have an `__init__(self, config: CacheConfig)` method and a `cache(self, func)` method that returns a wrapped, cached version of the input function. It also has an `is_available()` class method to check if the engine's dependencies (the underlying backend library) are met.
*   **Engine Implementations:**
    *   **`FunctoolsEngine`:** Wraps Python's `functools.lru_cache` or `functools.cache`. Always available.
    *   **`CacheBoxEngine`:** Uses the `cachebox` library for high-performance in-memory caching.
    *   **`CacheToolsEngine`:** Uses the `cachetools` library for various in-memory eviction policies (LRU, LFU, TTL, FIFO, RR).
    *   **`DiskCacheEngine`:** Uses the `diskcache` library for persistent, transactional, disk-backed caching (typically SQLite + file system).
    *   **`JoblibEngine`:** Uses `joblib.Memory` for file-system based caching, particularly efficient for Python objects like NumPy arrays.
    *   **`KleptoEngine`:** Uses the `klepto` library, which offers a wide range of serialization and storage backends (including file, SQL, HDF5). Its usage in `twat-cache` seems to be de-emphasized in recent changes.
    *   **`AioCacheEngine`:** Uses the `aiocache` library for caching results of asynchronous functions.
    *   **`RedisCacheEngine`:** (Potentially) An engine for Redis. As noted, `redis.py` is currently missing from the source tree, so this engine is not practically available unless provided externally or by a specific package version.
*   **`CacheEngineManager` (`src/twat_cache/engines/manager.py`):**
    *   Responsible for registering and discovering available cache engine classes.
    *   `_register_builtin_engines()`: Registers all standard engine types known to `twat-cache`.
    *   `select_engine()`: Provides logic to pick an engine based on availability and optional preferences. This is used by context managers. Decorators have their own specific fallback chains.

**4. Cache Management (`src/twat_cache/cache.py`)**

*   **Global Cache Registry (`_active_caches`):** A dictionary that keeps track of active cache instances created by the decorators. This allows for global operations.
*   **`register_cache(name, cache_engine_instance, wrapper, stats)`:** Adds a newly created cache instance to the global registry.
*   **`clear_cache(name=None)`:** Clears a specific cache by name or all registered caches if no name is provided. It also attempts to clean up associated disk directories.
*   **`get_stats(name=None)`:** Retrieves statistics (hits, misses, size, maxsize) for a specific cache or aggregated stats for all caches.
*   **`update_stats(...)`:** Internal helper to update hit/miss counts for a cache.

**5. Context Management (`src/twat_cache/context.py`)**

*   **`CacheContext`:** A class-based context manager.
    *   Allows for explicit selection of a cache engine (`engine_name`) and configuration for a specific block of code.
    *   Example: `with CacheContext(engine_name="diskcache", folder_name="my_temp_cache") as cache_instance:`
    *   The `cache_instance` provided by `as` is intended to be the underlying cache object from the chosen backend library (e.g., a `diskcache.Cache` object) if the `twat-cache` engine wrapper exposes it directly (often via a `_cache` attribute or `cache_instance` property). If not, it will be the `twat-cache` engine wrapper instance itself, which should still provide basic cache operations like `get`, `set`, `delete`.
    *   Ensures resources (like database connections for `DiskCacheEngine`) are properly initialized and closed.
*   **`engine_context`:** A function-based context manager, similar in purpose to `CacheContext`, providing a more concise way to achieve the same.

**6. Backend Selection Logic (`_select_best_backend` in `decorators.py`)**

This internal function is used by `@ucache` and potentially by context managers if no engine is explicitly specified.

*   Checks availability of backend libraries (`_get_available_backends`).
*   Considers `preferred_engine` from config.
*   Factors in `is_async` (favors `AioCacheEngine`).
*   Factors in `needs_disk` (favors `DiskCacheEngine`, `KleptoEngine`, `JoblibEngine`).
*   Has a fallback order if specific requirements aren't met (e.g., `CacheBoxEngine` -> `CacheToolsEngine` -> `FunctoolsEngine` for general in-memory needs).

**7. Key Generation (`make_key` in `decorators.py`)**

*   Responsible for creating a consistent, hashable cache key from the function's arguments (`*args`, `**kwargs`).
*   Serializes arguments to JSON by default to handle various data types and ensure order doesn't affect the key for keyword arguments.
*   A custom `serializer` can be provided in `CacheConfig` for handling non-JSON-serializable objects or for custom keying strategies. The `secure=True` option (default) likely implies a more robust serialization.

### Coding and Contributing

**Coding Conventions & Style:**

*   **Python Version:** Requires Python 3.10 or newer (as per `pyproject.toml`).
*   **Formatting:** Code is formatted using `Black` and `Ruff`. Adherence to these formatters is expected.
    *   Run `ruff format .` and `ruff check --fix .`
*   **Linting:** `Ruff` is used for extensive linting, covering rules from Flake8, isort, pep8-naming, and more.
    *   Run `ruff check .`
*   **Type Checking:** Static type checking is enforced using `MyPy`. All new code should include type hints.
    *   Run `mypy src/twat_cache tests`
*   **Imports:** `isort` (via Ruff) is used to sort imports. Known first-party is `twat_cache`. Relative imports are generally banned in `src` but allowed in `tests`.
*   **Line Length:** 88 characters, enforced by Black/Ruff.

**Dependencies:**

*   **Core:** `pydantic` (for configuration), `loguru` (for logging), `diskcache`, `joblib`, `cachetools`.
*   **Optional Backend Libraries & Their Engines:**
    *   `cachebox` (for `CacheBoxEngine`)
    *   `aiocache` (for `AioCacheEngine`)
    *   `klepto` (for `KleptoEngine`)
    These are installed via extras like `twat-cache[all]` or `twat-cache[cachebox]`.
*   **Development & Testing:** `pytest`, `pytest-cov`, `pytest-benchmark`, `mypy`, `ruff`, `hatch`, `pre-commit`.

**Testing:**

*   Tests are located in the `tests/` directory and use `pytest`.
*   Run tests with `python -m pytest -n auto tests` (or via `hatch env run test:test`).
*   Coverage is monitored: `python -m pytest -n auto --cov=src/twat_cache ...` (or `hatch env run test:test-cov`).
*   Strive for high test coverage for new features and bug fixes.
*   Benchmarks are present in `tests/test_benchmark.py` and can be run with `pytest-benchmark`.

**Contribution Process:**

1.  **Fork the repository** on GitHub.
2.  **Create a new branch** for your feature or bug fix: `git checkout -b feature/your-feature-name` or `bugfix/issue-description`.
3.  **Make your changes.** Ensure you add tests for any new functionality or bug fixes.
4.  **Run linters, formatters, and type checkers locally:**
    *   `hatch env run lint:fmt` (or `ruff format . && ruff check --fix .`)
    *   `hatch env run lint:typing` (or `mypy src/twat_cache tests`)
    *   Or use `pre-commit` hooks.
5.  **Run tests:** `hatch env run test:test` (or `pytest -n auto tests`)
6.  **Commit your changes** with a clear and descriptive commit message.
7.  **Push your branch** to your fork: `git push origin feature/your-feature-name`.
8.  **Open a Pull Request (PR)** against the main branch of the original repository.
9.  Address any feedback or CI failures.

**Pre-commit Hooks:**

The project uses `pre-commit` (as indicated by `.pre-commit-config.yaml`) to automatically run linters and formatters before commits. Install and set it up in your local clone:

```bash
pip install pre-commit
pre-commit install
```

This helps ensure that contributions meet the project's coding standards.

**Logging:**

The `loguru` library is used for logging. Import the logger from `twat_cache.logging` for consistent logging within the library.

**Project Structure (`src/twat_cache`):**

*   `__init__.py`: Exports main public interface (decorators, context managers).
*   `__main__.py`: Contains some utility functions, but not a primary CLI entry point for the cache library itself.
*   `cache.py`: Global cache registration and management utilities.
*   `config.py`: `CacheConfig` Pydantic model and configuration factory.
*   `context.py`: `CacheContext` and `engine_context` for explicit cache management.
*   `decorators.py`: Core caching decorators (`mcache`, `bcache`, etc.) and backend selection logic.
*   `engines/`: Directory for different cache backend implementations.
    *   `base.py`: `BaseCacheEngine` protocol.
    *   `manager.py`: `CacheEngineManager`.
    *   Individual engine files (e.g., `diskcache.py`, `joblib.py`).
*   `exceptions.py`: Custom exceptions.
*   `logging.py`: Logging setup.
*   `paths.py`: Path utilities (though `__main__.py` also has some path logic).
*   `type_defs.py`: Common type definitions and protocols.
