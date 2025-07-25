---
# this_file: src_docs/getting-started.md
title: Getting Started with TWAT-Cache
description: Quick start guide to get up and running with TWAT-Cache in 5 minutes
---

# Getting Started

Welcome to TWAT-Cache! This guide will help you install the library and create your first cached function in just a few minutes.

## Prerequisites

- Python 3.10 or higher
- pip package manager

## Installation

### Basic Installation

The basic installation includes essential caching backends:

```bash
pip install twat-cache
```

This gives you:

- ✅ In-memory caching with `cachetools`
- ✅ Disk-based caching with `diskcache`
- ✅ File-based caching with `joblib`
- ✅ Configuration with `pydantic`
- ✅ Logging with `loguru`

### Installation with All Backends

For maximum flexibility, install all optional backends:

```bash
pip install "twat-cache[all]"
```

Additional backends include:

- 🚀 High-performance Rust-based caching with `cachebox`
- ⚡ Async caching support with `aiocache`
- 🔬 Scientific computing cache with `klepto`
- 📁 Platform-specific directories with `platformdirs`

### Verify Installation

Check that TWAT-Cache is installed correctly:

```python
import twat_cache
print(twat_cache.__version__)
```

## Your First Cached Function

Let's create a simple example to demonstrate the power of caching:

### Step 1: Import the Decorator

```python
from twat_cache import ucache
import time
```

### Step 2: Create a Slow Function

```python
def slow_fibonacci(n: int) -> int:
    """Calculate Fibonacci number (slow recursive version)."""
    if n <= 1:
        return n
    return slow_fibonacci(n - 1) + slow_fibonacci(n - 2)

# Time the slow version
start = time.time()
result = slow_fibonacci(35)
print(f"Result: {result}")
print(f"Time: {time.time() - start:.2f} seconds")
# Output: Time: ~5-10 seconds
```

### Step 3: Add Caching

```python
@ucache  # Just add this decorator!
def fast_fibonacci(n: int) -> int:
    """Calculate Fibonacci number (cached version)."""
    if n <= 1:
        return n
    return fast_fibonacci(n - 1) + fast_fibonacci(n - 2)

# Time the cached version
start = time.time()
result = fast_fibonacci(35)
print(f"Result: {result}")
print(f"Time: {time.time() - start:.2f} seconds")
# Output: Time: ~0.01 seconds - 1000x faster!
```

## Understanding What Happened

When you add the `@ucache` decorator:

1. **First Call**: The function executes normally, but the result is stored in cache
2. **Subsequent Calls**: If the same arguments are used, the cached result is returned instantly
3. **Automatic Key Generation**: Arguments are automatically converted to cache keys
4. **Smart Backend Selection**: `ucache` automatically picks the best available cache engine

## Basic Configuration

### Setting Cache Size

Limit the number of cached items:

```python
@ucache(maxsize=100)  # Keep only 100 most recent results
def process_data(data_id: str) -> dict:
    # Expensive processing...
    return processed_data
```

### Setting Time-to-Live (TTL)

Make cached results expire after a certain time:

```python
@ucache(ttl=300)  # Cache for 5 minutes (300 seconds)
def fetch_weather(city: str) -> dict:
    # API call to weather service...
    return weather_data
```

### Combining Options

```python
@ucache(maxsize=50, ttl=3600)  # 50 items, 1 hour TTL
def analyze_report(report_id: int, options: dict) -> dict:
    # Complex analysis...
    return results
```

## Async Functions

TWAT-Cache fully supports async functions:

```python
from twat_cache import acache
import asyncio
import aiohttp

@acache(ttl=60)  # Cache for 1 minute
async def fetch_user_data(user_id: int) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.example.com/users/{user_id}") as response:
            return await response.json()

# Use it
async def main():
    # First call hits the API
    user = await fetch_user_data(123)
    
    # Second call returns from cache instantly
    user_again = await fetch_user_data(123)

asyncio.run(main())
```

## Choosing the Right Decorator

TWAT-Cache provides several decorators for different use cases:

| Decorator | Use Case | Backend |
|-----------|----------|---------|
| `@ucache` | General purpose (recommended) | Auto-selected |
| `@acache` | Async functions | aiocache |
| `@mcache` | Memory-only caching | cachetools/cachebox |
| `@bcache` | Basic disk caching | diskcache |
| `@fcache` | Large objects (NumPy, pandas) | joblib |

!!! tip "Pro Tip"
    Start with `@ucache` - it automatically selects the best backend for your use case!

## Next Steps

Now that you've created your first cached function, explore more features:

<div class="grid cards" markdown>

- :material-book-open-variant: **[User Guide](user-guide/index.md)**
    
    Deep dive into all features and configuration options

- :material-cog: **[Configuration Guide](user-guide/configuration.md)**
    
    Learn about advanced configuration and environment variables

- :material-test-tube: **[Examples](examples/index.md)**
    
    See real-world examples and best practices

- :material-api: **[API Reference](api/index.md)**
    
    Complete API documentation

</div>

## Quick Tips

!!! success "Best Practices"
    - Use `@ucache` for most cases - it's smart about backend selection
    - Set appropriate `maxsize` to prevent memory issues
    - Use `ttl` for time-sensitive data like API responses
    - Monitor cache performance with debug logging

!!! warning "Common Pitfalls"
    - Don't cache functions with side effects
    - Be careful with mutable arguments (lists, dicts)
    - Remember that cached functions won't see database updates

## Getting Help

- 📖 Read the [FAQ](faq.md) for common questions
- 🐛 Report issues on [GitHub](https://github.com/twat-framework/twat-cache/issues)
- 💬 Join our community discussions
- 📧 Contact the maintainers

---

Ready to dive deeper? Head to the [User Guide](user-guide/index.md) to learn about all the features TWAT-Cache has to offer!