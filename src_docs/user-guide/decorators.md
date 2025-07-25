---
# this_file: src_docs/user-guide/decorators.md
title: Decorators Guide - TWAT-Cache
description: Complete guide to all caching decorators in TWAT-Cache
---

# Decorators Guide

TWAT-Cache provides five main decorators, each optimized for specific use cases. This guide covers everything you need to know about using them effectively.

## Overview

| Decorator | Purpose | Best For | Persistence |
|-----------|---------|----------|-------------|
| `@ucache` | Universal (auto-selects backend) | General use (recommended) | Varies |
| `@mcache` | Memory caching | Speed-critical operations | No |
| `@bcache` | Basic disk caching | Persistent storage | Yes |
| `@fcache` | File caching | Large objects | Yes |
| `@acache` | Async caching | Async/await functions | No |

## Universal Cache: `@ucache`

The Swiss Army knife of caching - automatically selects the best backend.

### Basic Usage

```python
from twat_cache import ucache

@ucache
def compute(x, y):
    return x ** y
```

### Full Parameters

```python
@ucache(
    folder_name="my_cache",      # Cache folder (for disk backends)
    maxsize=100,                 # Maximum cached items
    ttl=3600,                    # Time-to-live in seconds
    policy="lru",                # Eviction policy
    preferred_engine="disk",     # Preferred backend
    use_sql=False,               # Use SQL storage (disk)
    compress=False,              # Compress cached values
    secure=True                  # Secure key generation
)
def my_function(x):
    return expensive_computation(x)
```

### Parameter Details

- **`folder_name`** (str | None): Directory for disk/file caches. Auto-generated if None.
- **`maxsize`** (int | None): Maximum items to cache. None = unlimited.
- **`ttl`** (float | None): Time-to-live in seconds. None = no expiration.
- **`policy`** (str): Eviction policy when cache is full:
  - `"lru"`: Least Recently Used (default)
  - `"lfu"`: Least Frequently Used
  - `"fifo"`: First In, First Out
  - `"lifo"`: Last In, First Out
  - `"mru"`: Most Recently Used
- **`preferred_engine`** (str | None): Backend preference:
  - `"memory"`: In-memory caching
  - `"disk"`: Persistent disk storage
  - `"file"`: File-based for large objects
  - `None`: Auto-select based on function
- **`compress`** (bool): Enable compression (disk/file backends)
- **`secure`** (bool): Use secure key generation (handles more types but slower)

### Smart Backend Selection

`@ucache` automatically selects backends based on:

1. Function characteristics (sync/async)
2. Available backends
3. Your preferred_engine setting

```python
# Automatically uses async backend
@ucache
async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        return await session.get(url)

# Force specific backend
@ucache(preferred_engine="disk")
def persistent_compute(x):
    return complex_calculation(x)
```

## Memory Cache: `@mcache`

Fastest caching for frequently accessed data.

### Basic Usage

```python
from twat_cache import mcache

@mcache
def quick_lookup(key):
    return database.get(key)
```

### Full Parameters

```python
@mcache(
    maxsize=128,      # LRU cache size
    ttl=300,          # 5-minute expiration
    policy="lru",     # Eviction policy
    secure=True       # Secure mode
)
def cached_function(x):
    return computation(x)
```

### Backend Priority

1. **CacheBox** (Rust): Fastest, if installed
2. **CacheTools**: Feature-rich Python implementation
3. **functools.lru_cache**: Built-in fallback

### Use Cases

```python
# API response caching with TTL
@mcache(ttl=60)
def get_exchange_rate(currency):
    return fetch_from_api(currency)

# Computation memoization
@mcache(maxsize=1000)
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Session data caching
@mcache(maxsize=100, ttl=1800)  # 30-minute sessions
def get_user_session(session_id):
    return load_session_from_db(session_id)
```

## Disk Cache: `@bcache`

Persistent caching that survives restarts.

### Basic Usage

```python
from twat_cache import bcache

@bcache
def expensive_analysis(data_id):
    return analyze_dataset(data_id)
```

### Full Parameters

```python
@bcache(
    folder_name="analysis_cache",  # Cache directory
    maxsize=1000,                  # Max cached items
    ttl=86400,                     # 24-hour expiration
    policy="lru",                  # Eviction policy
    use_sql=True,                  # SQLite storage
    secure=True                    # Secure mode
)
def process_report(report_id):
    return generate_report(report_id)
```

### Features

- **SQLite Backend**: Efficient storage and queries
- **Atomic Operations**: Safe for concurrent access
- **Automatic Cleanup**: Expired items removed
- **Size Management**: Respects maxsize limits

### Use Cases

```python
# ML model predictions
@bcache(folder_name="model_cache", ttl=3600)
def predict(model_name, input_data):
    model = load_model(model_name)
    return model.predict(input_data)

# Web scraping results
@bcache(folder_name="scrape_cache", ttl=86400)
def scrape_website(url):
    response = requests.get(url)
    return parse_html(response.text)

# Report generation
@bcache(folder_name="reports", maxsize=100)
def generate_monthly_report(year, month):
    data = fetch_month_data(year, month)
    return create_report(data)
```

## File Cache: `@fcache`

Optimized for large objects like arrays and dataframes.

### Basic Usage

```python
from twat_cache import fcache
import numpy as np

@fcache
def load_embeddings(model_name):
    return np.load(f"{model_name}_embeddings.npy")
```

### Full Parameters

```python
@fcache(
    folder_name="array_cache",  # Cache directory
    maxsize=50,                 # Max cached files
    ttl=None,                   # No expiration
    compress=True,              # Compress large objects
    secure=True                 # Secure mode
)
def process_image(image_path):
    return apply_filters(load_image(image_path))
```

### Optimizations

- **Binary Serialization**: Efficient for NumPy/Pandas
- **Compression Support**: Reduces disk usage
- **Memory Mapping**: For very large arrays
- **Parallel Access**: Thread-safe operations

### Use Cases

```python
# NumPy array caching
@fcache(compress=True)
def compute_correlation_matrix(dataset_id):
    data = load_dataset(dataset_id)
    return np.corrcoef(data.T)

# Pandas DataFrame caching
@fcache(folder_name="dataframes")
def merge_datasets(ids):
    dfs = [pd.read_csv(f"data_{id}.csv") for id in ids]
    return pd.concat(dfs, ignore_index=True)

# Image processing
@fcache(compress=True, maxsize=100)
def process_image_batch(image_urls):
    images = [download_image(url) for url in image_urls]
    return np.array([preprocess(img) for img in images])
```

## Async Cache: `@acache`

Native async support for modern Python applications.

### Basic Usage

```python
from twat_cache import acache

@acache
async def fetch_user(user_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"/api/users/{user_id}") as resp:
            return await resp.json()
```

### Full Parameters

```python
@acache(
    maxsize=100,      # Cache size
    ttl=60,           # 1-minute TTL
    policy="lru"      # Eviction policy
)
async def async_computation(x):
    await asyncio.sleep(1)  # Simulate async work
    return x ** 2
```

### Features

- **Non-blocking**: Cache operations don't block the event loop
- **Coroutine Support**: Works with any async function
- **Automatic Fallback**: Uses wrapped sync cache if aiocache unavailable

### Use Cases

```python
# API client with rate limiting
@acache(ttl=60, maxsize=1000)
async def api_request(endpoint, params):
    async with rate_limiter:
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint, params=params) as resp:
                return await resp.json()

# Database queries
@acache(ttl=300)
async def get_user_profile(user_id):
    async with db.acquire() as conn:
        return await conn.fetchone(
            "SELECT * FROM users WHERE id = $1", user_id
        )

# WebSocket data caching
@acache(maxsize=50, ttl=5)
async def get_live_price(symbol):
    async with websockets.connect(f"wss://stream/{symbol}") as ws:
        data = await ws.recv()
        return json.loads(data)
```

## Advanced Patterns

### Conditional Caching

```python
from twat_cache import ucache

def should_cache(result):
    return result is not None and result.status == "success"

@ucache(maxsize=100)
def fetch_data(item_id):
    result = api.get(item_id)
    if should_cache(result):
        return result
    # Don't cache failures
    raise ValueError("Failed to fetch")
```

### Cache Key Customization

```python
from twat_cache import ucache
import hashlib

def custom_key(*args, **kwargs):
    # Create custom cache key
    key_str = f"{args}{sorted(kwargs.items())}"
    return hashlib.md5(key_str.encode()).hexdigest()

@ucache(maxsize=100)
def complex_function(obj, options=None):
    # obj might not be hashable
    cache_key = custom_key(obj.id, options)
    return process(obj, options)
```

### Decorator Stacking

```python
from twat_cache import mcache, bcache
import functools

# Memory cache with disk backup
@mcache(maxsize=50, ttl=300)
@bcache(folder_name="backup", ttl=3600)
def hybrid_cache(x):
    return expensive_computation(x)

# With other decorators
@functools.lru_cache(maxsize=10)
@ucache(ttl=60)
@timing_decorator
def multi_decorated(x):
    return compute(x)
```

### Dynamic Configuration

```python
from twat_cache import ucache
import os

# Configure via environment
cache_size = int(os.getenv("CACHE_SIZE", "100"))
cache_ttl = int(os.getenv("CACHE_TTL", "300"))

@ucache(maxsize=cache_size, ttl=cache_ttl)
def configurable_function(x):
    return process(x)
```

## Cache Management

All decorators provide these methods on decorated functions:

### Cache Information

```python
@ucache
def my_func(x):
    return x ** 2

# Get cache statistics
info = my_func.cache_info()
print(f"Hits: {info.hits}")
print(f"Misses: {info.misses}")
print(f"Size: {info.currsize}/{info.maxsize}")
print(f"Hit Rate: {info.hits / (info.hits + info.misses):.2%}")
```

### Cache Control

```python
# Clear entire cache
my_func.cache_clear()

# Remove specific entry
my_func.cache_delete(42)

# Check if key exists
if my_func.cache_contains(42):
    print("Value is cached")

# Get cached value directly
try:
    value = my_func.cache_get(42)
except KeyError:
    print("Not in cache")
```

## Performance Tips

### 1. Choose the Right Decorator

- **Small, frequent**: Use `@mcache`
- **Large objects**: Use `@fcache`  
- **Persistence needed**: Use `@bcache`
- **Async code**: Use `@acache`
- **Not sure**: Use `@ucache`

### 2. Set Appropriate Limits

```python
# Prevent memory issues
@mcache(maxsize=1000)  # Limit cache size

# Prevent stale data
@ucache(ttl=300)  # 5-minute expiration

# Balance both
@bcache(maxsize=100, ttl=3600)  # Limited size + expiration
```

### 3. Monitor Performance

```python
def print_cache_stats(func):
    info = func.cache_info()
    hit_rate = info.hits / (info.hits + info.misses) if info.misses else 1.0
    print(f"{func.__name__}:")
    print(f"  Hit rate: {hit_rate:.1%}")
    print(f"  Size: {info.currsize}/{info.maxsize}")
    
# Regular monitoring
print_cache_stats(my_cached_func)
```

## Common Pitfalls

### 1. Unhashable Arguments

```python
# ❌ Won't work - list is unhashable
@ucache
def process_list(items):
    return sum(items)

# ✅ Convert to hashable type
@ucache
def process_list(items):
    return sum(tuple(items))  # Convert list to tuple
```

### 2. Mutable Default Arguments

```python
# ❌ Dangerous - mutable default
@ucache
def add_item(item, items=[]):
    items.append(item)
    return items

# ✅ Safe approach
@ucache
def add_item(item, items=None):
    if items is None:
        items = []
    return items + [item]  # Return new list
```

### 3. Side Effects

```python
# ❌ Don't cache functions with side effects
@ucache
def update_database(user_id, data):
    db.update(user_id, data)  # Side effect!
    return "success"

# ✅ Cache only pure computations
@ucache
def calculate_score(user_data):
    return compute_score(user_data)  # No side effects
```

## Next Steps

- Learn about [Configuration](configuration.md) options
- Explore [Context Management](context-management.md)
- Understand [Cache Engines](engines.md)
- See practical [Examples](../examples/index.md)