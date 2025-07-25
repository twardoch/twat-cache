---
# this_file: src_docs/user-guide/configuration.md
title: Configuration Guide - TWAT-Cache
description: Complete guide to configuring TWAT-Cache behavior
---

# Configuration Guide

TWAT-Cache offers flexible configuration options at multiple levels. This guide covers all configuration methods, from simple decorator parameters to advanced environment-based settings.

## Configuration Levels

TWAT-Cache supports configuration at three levels, with increasing precedence:

1. **Default Configuration** - Built-in sensible defaults
2. **Environment Variables** - System-wide settings
3. **Decorator Parameters** - Function-specific overrides

## Quick Configuration Examples

### Simple Size and TTL

```python
from twat_cache import ucache

# Cache 100 items for 5 minutes
@ucache(maxsize=100, ttl=300)
def fetch_data(key):
    return expensive_lookup(key)
```

### Persistent Storage

```python
from twat_cache import bcache

# Persistent cache with custom folder
@bcache(folder_name="my_app_cache", maxsize=1000)
def process_report(report_id):
    return generate_report(report_id)
```

### High-Performance Memory Cache

```python
from twat_cache import mcache

# LFU eviction for frequently accessed data
@mcache(maxsize=500, policy="lfu", ttl=3600)
def get_user_preferences(user_id):
    return load_preferences(user_id)
```

## Configuration Parameters

### Core Parameters

#### `maxsize` (int | None)

Maximum number of items to cache.

- **Default**: `None` (unlimited)
- **Range**: `1` to system memory limits
- **None**: No size limit (use with caution)

```python
# Limited cache
@ucache(maxsize=100)
def limited_cache(x): ...

# Unlimited cache (careful!)
@ucache(maxsize=None)
def unlimited_cache(x): ...
```

#### `ttl` (float | None)

Time-to-live in seconds.

- **Default**: `None` (no expiration)
- **Range**: `0` to infinity
- **None**: Items never expire

```python
# 5-minute TTL
@ucache(ttl=300)
def api_cache(endpoint): ...

# 24-hour TTL
@ucache(ttl=86400)
def daily_cache(date): ...

# No expiration
@ucache(ttl=None)
def permanent_cache(x): ...
```

#### `policy` (str)

Cache eviction policy when maxsize is reached.

- **Default**: `"lru"`
- **Options**:
  - `"lru"`: Least Recently Used
  - `"lfu"`: Least Frequently Used
  - `"fifo"`: First In, First Out
  - `"lifo"`: Last In, First Out
  - `"mru"`: Most Recently Used

```python
# LRU for general use
@ucache(maxsize=100, policy="lru")
def general_cache(x): ...

# LFU for hot data
@ucache(maxsize=100, policy="lfu")
def popular_items(item_id): ...

# FIFO for time-series
@ucache(maxsize=100, policy="fifo")
def time_series_data(timestamp): ...
```

### Storage Parameters

#### `folder_name` (str | None)

Directory name for disk/file caches.

- **Default**: `None` (auto-generated)
- **Location**: `~/.cache/twat_cache/{folder_name}`

```python
# Custom folder
@bcache(folder_name="reports")
def generate_report(id): ...

# Auto-generated folder
@bcache()  # Uses function name
def process_data(x): ...
```

#### `compress` (bool)

Enable compression for cached values.

- **Default**: `False`
- **Backends**: Disk and file caches only
- **Trade-off**: Saves space, costs CPU time

```python
# Compress large objects
@fcache(compress=True)
def load_dataset(name):
    return pandas.read_csv(f"{name}.csv")
```

#### `use_sql` (bool)

Use SQL-based storage (disk cache).

- **Default**: `True` for disk cache
- **Backend**: DiskCache with SQLite

```python
# SQL storage (default)
@bcache(use_sql=True)
def with_sql(x): ...

# File storage (legacy)
@bcache(use_sql=False)
def without_sql(x): ...
```

### Advanced Parameters

#### `preferred_engine` (str | None)

Preferred cache backend for `@ucache`.

- **Default**: `None` (auto-select)
- **Options**: `"memory"`, `"disk"`, `"file"`, backend names

```python
# Force disk storage
@ucache(preferred_engine="disk")
def persistent_func(x): ...

# Prefer CacheBox if available
@ucache(preferred_engine="cachebox")
def fast_func(x): ...
```

#### `secure` (bool)

Use secure key generation.

- **Default**: `True`
- **True**: Handles more types, slightly slower
- **False**: Faster, limited type support

```python
# Secure mode (default)
@ucache(secure=True)
def handles_any_type(obj): ...

# Fast mode
@ucache(secure=False)
def simple_types_only(x: int, y: str): ...
```

## Environment Variables

Configure TWAT-Cache globally using environment variables:

### Basic Settings

```bash
# Cache size limits
export TWAT_CACHE_MAXSIZE=1000

# Default TTL (seconds)
export TWAT_CACHE_TTL=3600

# Eviction policy
export TWAT_CACHE_POLICY=lfu

# Cache folder
export TWAT_CACHE_FOLDER=my_app_cache

# Preferred engine
export TWAT_CACHE_ENGINE=disk

# Compression
export TWAT_CACHE_COMPRESS=true

# Secure mode
export TWAT_CACHE_SECURE=false
```

### Debug Settings

```bash
# Enable debug logging
export TWAT_CACHE_DEBUG=1

# Log level (DEBUG, INFO, WARNING, ERROR)
export TWAT_CACHE_LOG_LEVEL=DEBUG

# Log to file
export TWAT_CACHE_LOG_FILE=/var/log/twat_cache.log
```

### Using in Python

```python
import os
from twat_cache import ucache

# Set environment variables
os.environ["TWAT_CACHE_MAXSIZE"] = "500"
os.environ["TWAT_CACHE_TTL"] = "300"

# These will use environment settings
@ucache
def func1(x): ...

# Override environment with decorator
@ucache(maxsize=100)  # Overrides env
def func2(x): ...
```

## Configuration Objects

For complex scenarios, use `CacheConfig` objects:

```python
from twat_cache import CacheConfig, ucache

# Create reusable configuration
config = CacheConfig(
    maxsize=1000,
    ttl=3600,
    policy="lfu",
    folder_name="shared_cache",
    compress=True
)

# Apply to multiple functions
@ucache(config=config)
def func1(x): ...

@ucache(config=config)
def func2(x): ...
```

### Configuration Inheritance

```python
# Base configuration
base_config = CacheConfig(maxsize=100, ttl=300)

# Extended configuration
api_config = base_config.model_copy(update={"ttl": 60})
db_config = base_config.model_copy(update={"maxsize": 1000})

@ucache(config=api_config)
def api_call(endpoint): ...

@ucache(config=db_config)
def db_query(sql): ...
```

## Context-Based Configuration

Use context managers for temporary configuration:

```python
from twat_cache import CacheContext, ucache

# Temporary configuration
with CacheContext(maxsize=50, ttl=60):
    @ucache
    def temp_func(x):
        return x ** 2
    
    # Uses context configuration
    result = temp_func(5)

# Outside context, uses defaults
result2 = temp_func(5)
```

### Nested Contexts

```python
# Global context
with CacheContext(engine="memory", maxsize=100):
    # Function uses memory engine
    
    with CacheContext(ttl=30):
        # Inherits memory engine, adds TTL
        result = cached_function()
```

## Backend-Specific Configuration

### Memory Cache (CacheTools/CacheBox)

```python
@mcache(
    maxsize=100,
    policy="lru",  # LRU, LFU, FIFO, LIFO, MRU
    ttl=300
)
def memory_cached(x): ...
```

### Disk Cache (DiskCache)

```python
@bcache(
    folder_name="disk_cache",
    maxsize=10000,  # Items
    size_limit=1e9,  # 1GB total size
    ttl=86400,       # 24 hours
    use_sql=True     # SQLite backend
)
def disk_cached(x): ...
```

### File Cache (Joblib)

```python
@fcache(
    folder_name="arrays",
    compress=True,        # Compression level 1-9
    mmap_mode="r",       # Memory mapping for large files
    cache_validation=True # Validate cache integrity
)
def file_cached(x): ...
```

### Async Cache (AioCache)

```python
@acache(
    maxsize=100,
    ttl=60,
    namespace="api",  # Cache namespace
    key_builder=custom_key_func  # Custom key generation
)
async def async_cached(x): ...
```

## Configuration Patterns

### Per-Environment Configuration

```python
import os
from twat_cache import ucache

# Development
if os.getenv("ENV") == "development":
    cache_config = {"maxsize": 10, "ttl": 60}
# Production
else:
    cache_config = {"maxsize": 1000, "ttl": 3600}

@ucache(**cache_config)
def environment_aware(x): ...
```

### Feature Flags

```python
ENABLE_CACHE = os.getenv("ENABLE_CACHE", "true").lower() == "true"
CACHE_TTL = int(os.getenv("CACHE_TTL", "300"))

if ENABLE_CACHE:
    from twat_cache import ucache
    cache_decorator = ucache(ttl=CACHE_TTL)
else:
    # No-op decorator
    cache_decorator = lambda f: f

@cache_decorator
def conditional_cache(x): ...
```

### Dynamic Configuration

```python
from twat_cache import ucache
from functools import partial

# Configuration factory
def make_cache(cache_type="memory", **kwargs):
    defaults = {
        "memory": {"maxsize": 100, "ttl": 300},
        "disk": {"maxsize": 1000, "ttl": 3600},
        "api": {"maxsize": 50, "ttl": 60}
    }
    
    config = defaults.get(cache_type, {})
    config.update(kwargs)
    return partial(ucache, **config)

# Use dynamic configuration
api_cache = make_cache("api")
disk_cache = make_cache("disk", folder_name="persistent")

@api_cache()
def api_function(x): ...

@disk_cache()
def disk_function(x): ...
```

## Performance Tuning

### Memory Optimization

```python
# Small, hot cache
@mcache(maxsize=50, policy="lfu")
def hot_path(x): ...

# Large, cooler cache
@bcache(maxsize=10000, policy="lru")
def cold_path(x): ...
```

### TTL Strategies

```python
# Short TTL for real-time data
@ucache(ttl=5)  # 5 seconds
def live_price(symbol): ...

# Medium TTL for user data
@ucache(ttl=300)  # 5 minutes
def user_profile(user_id): ...

# Long TTL for reference data
@ucache(ttl=86400)  # 24 hours
def country_list(): ...
```

### Eviction Policies

```python
# LRU: General purpose
@ucache(policy="lru")
def general(x): ...

# LFU: Popular items
@ucache(policy="lfu")
def trending(x): ...

# FIFO: Time-ordered
@ucache(policy="fifo")
def queue_like(x): ...
```

## Monitoring Configuration

### Cache Statistics

```python
@ucache(maxsize=100)
def monitored_func(x):
    return x ** 2

# Check configuration
info = monitored_func.cache_info()
print(f"Max size: {info.maxsize}")
print(f"Current size: {info.currsize}")
print(f"Hit rate: {info.hits / (info.hits + info.misses):.2%}")
```

### Debug Logging

```python
import os
import logging

# Enable debug mode
os.environ["TWAT_CACHE_DEBUG"] = "1"
logging.basicConfig(level=logging.DEBUG)

# Now all cache operations are logged
@ucache
def debug_func(x):
    return x ** 2
```

## Best Practices

### 1. Start Simple

```python
# Start with defaults
@ucache
def my_func(x): ...

# Add configuration as needed
@ucache(maxsize=100, ttl=300)
def my_func(x): ...
```

### 2. Monitor and Adjust

```python
# Regular monitoring
def check_cache_health(func):
    info = func.cache_info()
    if info.hits + info.misses > 1000:
        hit_rate = info.hits / (info.hits + info.misses)
        if hit_rate < 0.8:
            logger.warning(f"Low hit rate: {hit_rate:.2%}")
```

### 3. Environment-Based Defaults

```python
# .env file
TWAT_CACHE_MAXSIZE=1000
TWAT_CACHE_TTL=3600
TWAT_CACHE_POLICY=lru

# Python code uses env defaults
@ucache  # Uses environment settings
def uses_defaults(x): ...
```

### 4. Validate Configuration

```python
from twat_cache import CacheConfig

try:
    config = CacheConfig(
        maxsize=-1,  # Invalid!
        ttl="invalid"  # Type error!
    )
except ValueError as e:
    print(f"Invalid config: {e}")
```

## Troubleshooting

### Configuration Not Applied?

1. Check precedence: Decorator > Environment > Defaults
2. Verify environment variables are set before import
3. Ensure configuration object is valid

### Performance Issues?

1. Monitor hit rates - aim for >80%
2. Adjust maxsize based on memory usage
3. Use appropriate eviction policy
4. Consider TTL vs maxsize trade-offs

### Debug Configuration

```python
from twat_cache import ucache
from twat_cache.config import get_cache_config_from_env

# Check environment config
env_config = get_cache_config_from_env()
print(f"Environment config: {env_config}")

# Check effective config
@ucache(maxsize=100)
def my_func(x): ...

print(f"Effective maxsize: {my_func.cache_info().maxsize}")
```

## Next Steps

- Explore [Context Management](context-management.md) for dynamic configuration
- Learn about [Cache Engines](engines.md) and their specific options
- See [Advanced Usage](advanced-usage.md) for complex scenarios
- Review [Examples](../examples/index.md) for real-world patterns