---
# this_file: src_docs/faq.md
title: FAQ - TWAT-Cache
description: Frequently asked questions about TWAT-Cache
---

# Frequently Asked Questions

## General Questions

### What is TWAT-Cache?

TWAT-Cache is a flexible caching library for Python that provides a unified interface to multiple caching backends. It allows you to add caching to your functions with simple decorators, automatically handling cache management, serialization, and backend selection.

### Why should I use TWAT-Cache instead of other caching libraries?

TWAT-Cache offers several unique advantages:

- **Unified Interface**: One API for multiple backends
- **Automatic Fallback**: Gracefully handles missing dependencies
- **Async Support**: First-class support for async/await
- **Type Safe**: Full type hints and runtime validation
- **Zero Config**: Works out of the box with sensible defaults
- **Flexible**: Easy to switch between backends without code changes

### Is TWAT-Cache production-ready?

Yes! TWAT-Cache is:

- Thoroughly tested with 90%+ code coverage
- Used in production environments
- Actively maintained with regular updates
- Built on proven libraries like `diskcache`, `cachetools`, and `joblib`

## Installation Issues

### ImportError: No module named 'twat_cache'

Make sure you've installed the package:

```bash
pip install twat-cache  # Note the hyphen!
```

Then import with underscore:

```python
import twat_cache  # Note the underscore!
```

### Some backends are not available

Install with all extras:

```bash
pip install "twat-cache[all]"
```

Or install specific backends:

```bash
pip install cachebox  # Rust backend
pip install aiocache  # Async support
```

### Installation fails on Windows

You may need Visual C++ build tools:

1. Download [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/)
2. Install "Desktop development with C++"
3. Retry installation

## Usage Questions

### How do I cache a function?

Simply add the `@ucache` decorator:

```python
from twat_cache import ucache

@ucache
def expensive_function(x: int) -> int:
    return x ** 2
```

### How do I set cache expiration?

Use the `ttl` (time-to-live) parameter:

```python
@ucache(ttl=3600)  # Cache for 1 hour
def get_user_data(user_id: int) -> dict:
    return fetch_from_database(user_id)
```

### How do I limit cache size?

Use the `maxsize` parameter:

```python
@ucache(maxsize=100)  # Keep only 100 items
def process_data(item_id: str) -> Result:
    return heavy_computation(item_id)
```

### How do I cache async functions?

Use the `@acache` decorator:

```python
from twat_cache import acache

@acache
async def fetch_api_data(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
```

### How do I clear the cache?

Access the cache instance:

```python
@ucache
def my_function(x: int) -> int:
    return x * 2

# Clear entire cache
my_function.cache_clear()

# Remove specific entry
my_function.cache_delete(5)

# Get cache info
info = my_function.cache_info()
```

### Can I use different caches for different functions?

Yes! Use different decorators or specify engines:

```python
@ucache(cache_engine="memory")  # In-memory only
def fast_function(x): ...

@ucache(cache_engine="disk")    # Persistent disk cache
def persistent_function(x): ...

@fcache  # Optimized for large objects
def process_dataframe(df): ...
```

## Performance Questions

### Is caching always faster?

Not always. Caching is beneficial when:

- Function execution is slower than cache lookup
- Function is called repeatedly with same arguments
- Results are deterministic (same input = same output)

Avoid caching:

- Very fast functions
- Functions with side effects
- Functions returning different results each time

### Which backend is fastest?

Performance depends on use case:

- **Memory (cachebox)**: Fastest for small objects
- **Memory (cachetools)**: Good balance of speed and features
- **Disk (diskcache)**: Persistent, good for medium data
- **File (joblib)**: Best for large NumPy arrays, pandas DataFrames

### How much memory will caching use?

Memory usage depends on:

- Cache backend (memory vs disk)
- Object sizes
- `maxsize` setting

Monitor with:

```python
@ucache(maxsize=1000)
def my_function(x): ...

# Check cache statistics
stats = my_function.cache_info()
print(f"Cache size: {stats.currsize}")
print(f"Hit rate: {stats.hits / (stats.hits + stats.misses):.2%}")
```

## Advanced Questions

### Can I use custom serialization?

Yes, configure serialization in the cache config:

```python
from twat_cache import CacheConfig, ucache

config = CacheConfig(
    serializer="pickle",  # or "json", "msgpack"
    compression=True
)

@ucache(config=config)
def my_function(x): ...
```

### How do I implement a custom cache engine?

Implement the `CacheEngineProtocol`:

```python
from twat_cache.engines.base import CacheEngineProtocol

class MyCustomEngine:
    def get(self, key: str) -> Any: ...
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None: ...
    def delete(self, key: str) -> None: ...
    def clear(self) -> None: ...
    def exists(self, key: str) -> bool: ...
```

### Can I use TWAT-Cache with Django/Flask/FastAPI?

Yes! TWAT-Cache works with any Python framework:

```python
# FastAPI example
from fastapi import FastAPI
from twat_cache import acache

app = FastAPI()

@app.get("/users/{user_id}")
@acache(ttl=60)
async def get_user(user_id: int):
    return await fetch_user_from_db(user_id)
```

### How do I handle cache errors?

TWAT-Cache is designed to fail gracefully:

```python
from twat_cache import ucache
from twat_cache.exceptions import CacheError

@ucache(fallback=True)  # Continue on cache errors
def my_function(x):
    return expensive_computation(x)

# Or handle explicitly
try:
    result = my_function(5)
except CacheError as e:
    logger.error(f"Cache error: {e}")
    result = expensive_computation(5)
```

## Debugging Questions

### How do I debug cache behavior?

Enable debug logging:

```python
import os
os.environ["TWAT_CACHE_DEBUG"] = "1"

# Or programmatically
from twat_cache.logging import logger
logger.enable("DEBUG")
```

### How do I profile cache performance?

Use the built-in statistics:

```python
@ucache
def my_function(x): ...

# After some usage
stats = my_function.cache_info()
print(f"Hits: {stats.hits}")
print(f"Misses: {stats.misses}")
print(f"Hit rate: {stats.hits / (stats.hits + stats.misses):.2%}")
print(f"Size: {stats.currsize}/{stats.maxsize}")
```

## Contributing Questions

### How can I contribute?

We welcome contributions! See our [Contributing Guide](dev-guide/contributing.md) for:

- Setting up development environment
- Running tests
- Submitting pull requests
- Code style guidelines

### Where can I report bugs?

Please report bugs on our [GitHub Issues](https://github.com/twat-framework/twat-cache/issues) page with:

- Python version
- TWAT-Cache version
- Minimal reproducible example
- Full error traceback

### Can I sponsor the project?

Yes! Check our [GitHub Sponsors](https://github.com/sponsors/twat-framework) page for sponsorship options.

---

Still have questions? Feel free to:

- Open a [discussion](https://github.com/twat-framework/twat-cache/discussions)
- Join our [Discord community](#)
- Email the maintainers