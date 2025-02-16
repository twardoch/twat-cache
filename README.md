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
.
