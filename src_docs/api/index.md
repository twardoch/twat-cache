---
# this_file: src_docs/api/index.md
title: API Reference - TWAT-Cache
description: Complete API documentation for TWAT-Cache
---

# API Reference

This section provides detailed API documentation for all TWAT-Cache modules, classes, and functions.

## Core Modules

### Decorators

The main caching decorators that form the public API.

::: twat_cache.decorators
    options:
        show_source: false
        members:
            - ucache
            - mcache
            - bcache
            - fcache
            - acache

**Quick Reference:**

- [`ucache`](decorators.md#ucache) - Universal cache with auto backend selection
- [`mcache`](decorators.md#mcache) - Memory-based caching
- [`bcache`](decorators.md#bcache) - Basic disk caching
- [`fcache`](decorators.md#fcache) - File caching for large objects
- [`acache`](decorators.md#acache) - Async function caching

### Configuration

Configuration system for cache behavior.

::: twat_cache.config
    options:
        show_source: false
        members:
            - CacheConfig
            - create_cache_config
            - get_cache_config_from_env

**Key Classes:**

- [`CacheConfig`](config.md#cacheconfig) - Main configuration model
- [`create_cache_config`](config.md#create_cache_config) - Factory function

### Context Management

Advanced context managers for cache lifecycle.

::: twat_cache.context
    options:
        show_source: false
        members:
            - CacheContext
            - engine_context

**Context Managers:**

- [`CacheContext`](context.md#cachecontext) - Class-based context manager
- [`engine_context`](context.md#engine_context) - Function-based context

### Cache Management

Global cache registry and management utilities.

::: twat_cache.cache
    options:
        show_source: false
        members:
            - CacheStats
            - register_cache
            - list_caches
            - clear_all_caches
            - get_all_stats

## Engine System

### Base Classes

Abstract base classes and protocols for cache engines.

::: twat_cache.engines.base
    options:
        show_source: false
        members:
            - BaseCacheEngine
            - CacheEngineProtocol

### Engine Manager

Engine registration and selection system.

::: twat_cache.engines.manager
    options:
        show_source: false
        members:
            - CacheEngineManager
            - register_engine
            - list_engines

### Available Engines

| Engine | Module | Description | Optional |
|--------|--------|-------------|----------|
| FuncTools | `twat_cache.engines.functools_engine` | Built-in Python LRU cache | No |
| CacheTools | `twat_cache.engines.cachetools` | Advanced memory caching | No |
| CacheBox | `twat_cache.engines.cachebox` | High-performance Rust backend | Yes |
| DiskCache | `twat_cache.engines.diskcache` | SQLite-based disk storage | No |
| Joblib | `twat_cache.engines.joblib` | File caching for arrays | No |
| AioCache | `twat_cache.engines.aiocache` | Async caching support | Yes |
| Klepto | `twat_cache.engines.klepto` | Scientific computing cache | Yes |

## Type System

### Type Definitions

Core type definitions and protocols.

::: twat_cache.type_defs
    options:
        show_source: false
        members:
            - CacheKey
            - CacheValue
            - CacheDecorator
            - AsyncCacheDecorator
            - P
            - R
            - AsyncR

**Type Variables:**

- `P` - ParamSpec for function parameters
- `R` - Return type for sync functions
- `AsyncR` - Return type for async functions

## Utilities

### Exceptions

Custom exceptions for error handling.

::: twat_cache.exceptions
    options:
        show_source: false
        members:
            - CacheError
            - ConfigError
            - EngineError
            - KeyError

### Logging

Logging configuration and utilities.

::: twat_cache.logging
    options:
        show_source: false
        members:
            - logger
            - configure_logging
            - set_log_level

### Path Utilities

Cache directory and file management.

::: twat_cache.paths
    options:
        show_source: false
        members:
            - get_cache_dir
            - ensure_cache_dir
            - clear_cache_dir

## Public API Summary

### Main Decorators

```python
from twat_cache import ucache, mcache, bcache, fcache, acache

# Universal cache (recommended)
@ucache(maxsize=100, ttl=300)
def my_function(x): ...

# Memory cache
@mcache(maxsize=50, policy="lfu")
def memory_function(x): ...

# Disk cache
@bcache(folder_name="cache", ttl=3600)
def disk_function(x): ...

# File cache
@fcache(compress=True)
def file_function(x): ...

# Async cache
@acache(ttl=60)
async def async_function(x): ...
```

### Configuration

```python
from twat_cache import CacheConfig, create_cache_config

# Create configuration
config = create_cache_config(
    maxsize=1000,
    ttl=3600,
    policy="lru"
)

# Use with decorator
@ucache(config=config)
def configured_function(x): ...
```

### Context Management

```python
from twat_cache import CacheContext

# Temporary configuration
with CacheContext(maxsize=50, ttl=60):
    result = cached_function()
```

### Cache Management

```python
from twat_cache import list_caches, clear_all_caches

# List all active caches
caches = list_caches()

# Clear all caches
clear_all_caches()
```

## Module Structure

```
twat_cache/
├── __init__.py          # Public API exports
├── decorators.py        # Main cache decorators
├── config.py            # Configuration system
├── context.py           # Context managers
├── cache.py             # Global cache management
├── engines/             # Cache engine implementations
│   ├── base.py          # Base classes and protocols
│   ├── manager.py       # Engine registration
│   ├── functools_engine.py
│   ├── cachetools.py
│   ├── cachebox.py
│   ├── diskcache.py
│   ├── joblib.py
│   ├── aiocache.py
│   └── klepto.py
├── exceptions.py        # Custom exceptions
├── logging.py           # Logging utilities
├── paths.py             # Path management
├── type_defs.py         # Type definitions
└── utils.py             # General utilities
```

## Version Information

```python
import twat_cache

# Get version
print(twat_cache.__version__)

# Check available engines
from twat_cache.engines.manager import CacheEngineManager
print(CacheEngineManager.list_engines())
```

## Import Examples

### Basic Import

```python
# Most common imports
from twat_cache import ucache, mcache, bcache, fcache, acache
```

### Advanced Import

```python
# Configuration
from twat_cache import CacheConfig, create_cache_config

# Context management
from twat_cache import CacheContext, engine_context

# Cache management
from twat_cache import list_caches, clear_all_caches, get_all_stats

# Exceptions
from twat_cache.exceptions import CacheError, ConfigError
```

### Engine-Specific Import

```python
# Direct engine access (advanced usage)
from twat_cache.engines.manager import CacheEngineManager
from twat_cache.engines.base import BaseCacheEngine

# Create engine directly
engine = CacheEngineManager.create_engine("memory", config)
```

## See Also

- [User Guide](../user-guide/index.md) - Learn how to use TWAT-Cache
- [Examples](../examples/index.md) - Practical code examples
- [Developer Guide](../dev-guide/index.md) - Contributing and internals