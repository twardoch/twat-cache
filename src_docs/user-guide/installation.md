---
# this_file: src_docs/user-guide/installation.md
title: Installation Guide - TWAT-Cache
description: Detailed installation instructions for TWAT-Cache
---

# Installation Guide

This guide covers all installation options for TWAT-Cache, including troubleshooting common issues.

## Requirements

### Python Version

TWAT-Cache requires Python 3.10 or higher. Check your Python version:

```bash
python --version
# or
python3 --version
```

### Operating System

TWAT-Cache is tested on:

- ✅ Linux (Ubuntu, Debian, RHEL, etc.)
- ✅ macOS (10.15+)
- ✅ Windows (10, 11)

## Installation Methods

### Using pip (Recommended)

#### Basic Installation

Install TWAT-Cache with essential dependencies:

```bash
pip install twat-cache
```

This includes:

- `pydantic` - Configuration and validation
- `loguru` - Advanced logging
- `diskcache` - Disk-based caching
- `joblib` - File caching for large objects
- `cachetools` - In-memory caching algorithms

#### Full Installation

Install with all optional backends:

```bash
pip install "twat-cache[all]"
```

Additional backends:

- `cachebox` - High-performance Rust-based caching
- `aiocache` - Async caching support
- `klepto` - Scientific computing cache
- `platformdirs` - Platform-specific directories

#### Development Installation

For contributors and developers:

```bash
pip install "twat-cache[dev,test]"
```

Includes:

- Testing tools (pytest, coverage)
- Development tools (pre-commit, mypy, ruff)
- Documentation tools (mkdocs, mkdocs-material)

### Using UV (Fast Alternative)

[UV](https://github.com/astral-sh/uv) is a fast Python package installer:

```bash
# Install uv first
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install twat-cache
uv pip install twat-cache

# Or with all extras
uv pip install "twat-cache[all]"
```

### Using Poetry

If your project uses Poetry:

```toml
# pyproject.toml
[tool.poetry.dependencies]
twat-cache = "^1.0"

# Or with extras
twat-cache = {version = "^1.0", extras = ["all"]}
```

Then install:

```bash
poetry install
```

### From Source

For the latest development version:

```bash
# Clone the repository
git clone https://github.com/twat-framework/twat-cache.git
cd twat-cache

# Install with pip
pip install -e .

# Or with all extras
pip install -e ".[all,dev,test]"
```

## Verifying Installation

### Basic Check

```python
import twat_cache
print(f"TWAT-Cache version: {twat_cache.__version__}")
```

### Backend Availability

Check which backends are available:

```python
from twat_cache.engines.manager import CacheEngineManager

# List available engines
engines = CacheEngineManager.list_engines()
print("Available engines:", engines)

# Check specific engine
if CacheEngineManager.is_engine_available("cachebox"):
    print("CacheBox (Rust) backend is available!")
```

### Run a Simple Test

```python
from twat_cache import ucache

@ucache
def test_function(x: int) -> int:
    return x * 2

# Test caching
result1 = test_function(5)  # Computed
result2 = test_function(5)  # From cache

print(f"Results: {result1}, {result2}")
```

## Platform-Specific Notes

### Linux

Most distributions work out of the box. For some backends:

```bash
# For aiocache Redis backend (optional)
sudo apt-get install redis-server  # Debian/Ubuntu
sudo yum install redis             # RHEL/CentOS
```

### macOS

If you encounter issues with Rust-based backends:

```bash
# Install Rust compiler
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Retry installation
pip install "twat-cache[all]"
```

### Windows

Some backends may require Visual C++ build tools:

1. Download [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022)
2. Install "Desktop development with C++"
3. Retry installation

## Troubleshooting

### Import Errors

If you get import errors:

```python
# Check installed packages
pip list | grep twat-cache

# Reinstall
pip install --force-reinstall twat-cache
```

### Missing Backends

If specific backends aren't available:

```bash
# Install specific backend
pip install cachebox  # For Rust backend
pip install aiocache  # For async support

# Or reinstall with all extras
pip install --upgrade "twat-cache[all]"
```

### Permission Errors

On Unix systems, you might need user-level installation:

```bash
pip install --user twat-cache
```

Or use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install twat-cache
```

### Compilation Errors

For Rust-based backends on Linux:

```bash
# Install development tools
sudo apt-get install build-essential  # Debian/Ubuntu
sudo yum groupinstall "Development Tools"  # RHEL/CentOS
```

## Docker Installation

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

# Install build dependencies for all backends
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install TWAT-Cache
RUN pip install "twat-cache[all]"

# Your application
COPY . /app
WORKDIR /app

CMD ["python", "app.py"]
```

## Next Steps

Now that you have TWAT-Cache installed:

- Follow the [Quick Start](quickstart.md) tutorial
- Learn about [Decorators](decorators.md)
- Configure your [Cache Settings](configuration.md)

## Getting Help

If you encounter issues:

1. Check the [FAQ](../faq.md)
2. Search [existing issues](https://github.com/twat-framework/twat-cache/issues)
3. Open a new issue with:
   - Python version
   - Operating system
   - Full error message
   - Installation command used