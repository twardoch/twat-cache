# twat-cache

(work in progress)

A flexible caching utility package for Python functions that provides a unified interface for caching function results using various backends (memory, disk, SQL).

## Features

- Simple decorator interface for caching function results
- Multiple caching backends:
  - Memory-based LRU cache (always available)
  - SQL-based disk cache using `diskcache` (optional)
  - Efficient array caching using `joblib` (optional)
- Automatic cache directory management
- Type hints and modern Python features

## Installation

```bash
pip install twat-cache
```

## Usage

Basic usage with default memory caching:

```python
from twat_cache import ucache

@ucache()
def expensive_computation(x):
    # Results will be cached automatically
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

@ucache(folder_name="array_cache")
def matrix_operation(arr):
    # Large array operations will be efficiently cached
    return np.dot(arr, arr.T)
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
  - `diskcache`: For SQL-based disk caching
  - `joblib`: For efficient array caching

## License

MIT License  
.
