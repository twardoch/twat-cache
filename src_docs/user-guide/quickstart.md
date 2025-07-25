---
# this_file: src_docs/user-guide/quickstart.md
title: Quick Start Tutorial - TWAT-Cache
description: Get up and running with TWAT-Cache in 5 minutes
---

# Quick Start Tutorial

This tutorial will get you caching in 5 minutes! We'll cover the essentials and show you how powerful TWAT-Cache can be with minimal setup.

## Prerequisites

- Python 3.10 or higher installed
- Basic familiarity with Python decorators

## Step 1: Installation (30 seconds)

Open your terminal and install TWAT-Cache:

```bash
pip install twat-cache
```

That's it! You now have access to powerful caching capabilities.

## Step 2: Your First Cache (1 minute)

Create a new Python file called `cache_demo.py`:

```python
from twat_cache import ucache
import time

# Add @ucache to any function you want to cache
@ucache
def slow_calculation(n):
    """Simulates an expensive calculation."""
    print(f"Computing {n}... (this takes 2 seconds)")
    time.sleep(2)  # Simulate slow computation
    return n ** 2

# First call - will be slow
start = time.time()
result1 = slow_calculation(10)
print(f"Result: {result1}, Time: {time.time() - start:.2f}s")

# Second call - instant from cache!
start = time.time()
result2 = slow_calculation(10)
print(f"Result: {result2}, Time: {time.time() - start:.2f}s")
```

Run it:

```bash
python cache_demo.py
```

Output:
```
Computing 10... (this takes 2 seconds)
Result: 100, Time: 2.00s
Result: 100, Time: 0.00s
```

🎉 **Congratulations!** You just made your function 1000x faster with one decorator!

## Step 3: Cache Configuration (1 minute)

Let's add some configuration to control cache behavior:

```python
from twat_cache import ucache

# Cache up to 100 items for 5 minutes each
@ucache(maxsize=100, ttl=300)
def fetch_user_data(user_id):
    print(f"Fetching data for user {user_id}")
    # Simulate database query
    return {"id": user_id, "name": f"User {user_id}"}

# Test it
user = fetch_user_data(123)  # Prints: Fetching data for user 123
user = fetch_user_data(123)  # No print - from cache!
user = fetch_user_data(456)  # Prints: Fetching data for user 456
```

## Step 4: Different Cache Types (1 minute)

TWAT-Cache provides specialized decorators for different use cases:

```python
from twat_cache import mcache, bcache, fcache
import numpy as np

# Memory cache - fastest, no persistence
@mcache(maxsize=50)
def memory_cached_function(x):
    return x * 2

# Disk cache - survives program restarts
@bcache(folder_name="my_cache")
def persistent_function(x):
    return x ** 3

# File cache - great for large objects
@fcache(compress=True)
def process_array(size):
    return np.random.rand(size, size)

# Test them
print(memory_cached_function(5))    # Fast memory cache
print(persistent_function(5))       # Persisted to disk
array = process_array(1000)         # Efficiently cached large array
```

## Step 5: Async Functions (30 seconds)

Caching async functions is just as easy:

```python
from twat_cache import acache
import asyncio

@acache(ttl=60)
async def fetch_api_data(endpoint):
    print(f"Fetching {endpoint}")
    # Simulate API call
    await asyncio.sleep(1)
    return {"endpoint": endpoint, "data": "example"}

async def main():
    # First call - slow
    data1 = await fetch_api_data("/users")  # Prints: Fetching /users
    
    # Second call - instant!
    data2 = await fetch_api_data("/users")  # No print - from cache!

asyncio.run(main())
```

## Step 6: Cache Management (30 seconds)

You can inspect and control your caches:

```python
from twat_cache import ucache

@ucache
def my_function(x):
    return x ** 2

# Use the function
results = [my_function(i) for i in range(5)]

# Check cache statistics
info = my_function.cache_info()
print(f"Hits: {info.hits}, Misses: {info.misses}")

# Clear the cache
my_function.cache_clear()
print("Cache cleared!")

# Delete specific entry
my_function.cache_delete(3)
print("Removed entry for x=3")
```

## Complete Example: Real-World Usage

Here's a practical example showing how TWAT-Cache can speed up a data processing pipeline:

```python
from twat_cache import ucache, fcache
import pandas as pd
import time

# Cache expensive data loading
@fcache(folder_name="data_cache")
def load_dataset(filename):
    """Loads and preprocesses a dataset."""
    print(f"Loading {filename}...")
    # Simulate loading large CSV
    time.sleep(2)
    return pd.DataFrame({
        'id': range(1000),
        'value': range(1000)
    })

# Cache data transformations
@ucache(maxsize=10)
def transform_data(df, column, operation):
    """Apply transformation to dataframe."""
    print(f"Transforming {column} with {operation}")
    if operation == "square":
        df[f"{column}_squared"] = df[column] ** 2
    elif operation == "normalize":
        df[f"{column}_norm"] = df[column] / df[column].max()
    return df

# Use the cached functions
start_time = time.time()

# First run - everything computed
df = load_dataset("sales_2024.csv")
df = transform_data(df, "value", "square")
df = transform_data(df, "value", "normalize")

print(f"First run: {time.time() - start_time:.2f}s")

# Second run - all from cache!
start_time = time.time()

df = load_dataset("sales_2024.csv")  # Instant!
df = transform_data(df, "value", "square")  # Instant!
df = transform_data(df, "value", "normalize")  # Instant!

print(f"Second run: {time.time() - start_time:.2f}s")
```

Output:
```
Loading sales_2024.csv...
Transforming value with square
Transforming value with normalize
First run: 2.01s
Second run: 0.00s
```

## What's Next?

You've learned the basics! Here's where to go next:

### Explore More Features

- **[Decorators Guide](decorators.md)**: Deep dive into all decorators
- **[Configuration Guide](configuration.md)**: Advanced configuration options
- **[Context Management](context-management.md)**: Dynamic cache control

### Advanced Topics

- **[Cache Engines](engines.md)**: Understanding different backends
- **[Performance Tuning](advanced-usage.md)**: Optimize for your use case
- **[API Reference](../api/index.md)**: Complete documentation

### Best Practices

1. **Start with `@ucache`** - it automatically picks the best backend
2. **Set appropriate `maxsize`** to prevent memory issues
3. **Use `ttl` for time-sensitive data** like API responses
4. **Choose the right decorator** for your data type:
   - `@mcache` for small, frequently accessed data
   - `@bcache` for data that should persist
   - `@fcache` for large objects like arrays
   - `@acache` for async functions

## Common Patterns

### API Response Caching
```python
@ucache(ttl=300)  # 5-minute cache
def get_weather(city):
    return requests.get(f"https://api.weather.com/{city}").json()
```

### Database Query Caching
```python
@bcache(folder_name="db_cache", ttl=3600)  # 1-hour persistent cache
def get_user_profile(user_id):
    return db.query(f"SELECT * FROM users WHERE id = {user_id}")
```

### Computation Caching
```python
@mcache(maxsize=1000)  # Keep last 1000 results
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

## Troubleshooting

### Cache Not Working?

1. Check that function arguments are hashable
2. Verify the cache backend is installed
3. Enable debug logging:

```python
import os
os.environ["TWAT_CACHE_DEBUG"] = "1"
```

### Performance Issues?

1. Monitor cache hit rate with `cache_info()`
2. Adjust `maxsize` based on memory usage
3. Consider different backends for your use case

## Summary

You've learned how to:

- ✅ Install and import TWAT-Cache
- ✅ Add caching with a single decorator
- ✅ Configure cache size and TTL
- ✅ Use different cache types
- ✅ Cache async functions
- ✅ Manage and inspect caches

With just `@ucache`, you can make your Python applications significantly faster. Happy caching! 🚀