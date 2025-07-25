---
# this_file: src_docs/user-guide/index.md
title: User Guide - TWAT-Cache
description: Comprehensive guide to using TWAT-Cache in your Python projects
---

# User Guide

Welcome to the TWAT-Cache User Guide! This comprehensive guide will walk you through all features and capabilities of TWAT-Cache, from basic usage to advanced patterns.

## What You'll Learn

This guide is organized to take you from beginner to expert:

<div class="grid cards" markdown>

- :material-package-variant: **[Installation](installation.md)**
    
    Detailed installation options and troubleshooting

- :material-rocket: **[Quick Start](quickstart.md)**
    
    Get up and running in 5 minutes

- :material-function: **[Decorators](decorators.md)**
    
    Master all cache decorators and their options

- :material-cog: **[Configuration](configuration.md)**
    
    Configure caching behavior and policies

- :material-folder-cog: **[Context Management](context-management.md)**
    
    Fine-grained cache control with contexts

- :material-engine: **[Cache Engines](engines.md)**
    
    Understand different caching backends

- :material-professional-hexagon: **[Advanced Usage](advanced-usage.md)**
    
    Patterns for complex scenarios

</div>

## Learning Path

### 🎯 For Beginners

If you're new to caching or TWAT-Cache:

1. Start with [Installation](installation.md) to set up your environment
2. Follow the [Quick Start](quickstart.md) tutorial
3. Learn about basic [Decorators](decorators.md) usage
4. Understand [Configuration](configuration.md) options

### 🚀 For Intermediate Users

If you're comfortable with basic caching:

1. Explore different [Cache Engines](engines.md) and their trade-offs
2. Learn about [Context Management](context-management.md) for dynamic configuration
3. Dive into [Advanced Usage](advanced-usage.md) patterns

### 🏆 For Advanced Users

If you want to master TWAT-Cache:

1. Study the [API Reference](../api/index.md) for detailed documentation
2. Review [Examples](../examples/index.md) for real-world patterns
3. Contribute to the project using the [Developer Guide](../dev-guide/index.md)

## Core Concepts

Before diving in, let's review the core concepts:

### Cache Decorators

TWAT-Cache provides decorators that wrap your functions to add caching:

```python
from twat_cache import ucache

@ucache
def expensive_function(x: int) -> int:
    return x ** 2
```

### Cache Engines

Different backends for storing cached data:

- **Memory**: Fast, volatile storage
- **Disk**: Persistent storage between runs
- **File**: Optimized for large objects
- **Async**: For async/await functions

### Configuration

Control cache behavior:

```python
@ucache(
    maxsize=100,      # Maximum items in cache
    ttl=3600,         # Time-to-live in seconds
    cache_engine="disk"  # Specific engine
)
```

### Context Management

Dynamic cache control:

```python
from twat_cache import CacheContext

with CacheContext(engine="memory", ttl=60):
    # All caching in this block uses these settings
    result = cached_function()
```

## Quick Examples

### Basic Caching

```python
from twat_cache import ucache

@ucache
def fetch_data(user_id: int) -> dict:
    # Expensive database query
    return db.query(f"SELECT * FROM users WHERE id = {user_id}")
```

### Async Caching

```python
from twat_cache import acache

@acache(ttl=300)
async def fetch_api_data(endpoint: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(endpoint) as response:
            return await response.json()
```

### Large Object Caching

```python
from twat_cache import fcache
import numpy as np

@fcache  # Uses joblib for efficient array storage
def process_image(image_path: str) -> np.ndarray:
    image = load_image(image_path)
    return apply_filters(image)
```

## Best Practices

!!! tip "Do's"
    - ✅ Use `@ucache` as your default decorator
    - ✅ Set appropriate `maxsize` to prevent memory issues
    - ✅ Use `ttl` for time-sensitive data
    - ✅ Monitor cache hit rates in production
    - ✅ Test cache behavior in your unit tests

!!! warning "Don'ts"
    - ❌ Don't cache functions with side effects
    - ❌ Don't cache functions that return different results for same inputs
    - ❌ Don't ignore memory usage with large caches
    - ❌ Don't cache sensitive data without encryption

## Getting Help

- Check the [FAQ](../faq.md) for common questions
- Review [Examples](../examples/index.md) for patterns
- Read the [API Reference](../api/index.md) for details
- Open an [issue](https://github.com/twat-framework/twat-cache/issues) for bugs

## Ready to Start?

Head to the [Installation](installation.md) guide to begin your journey with TWAT-Cache!