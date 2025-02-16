#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "pytest",
#   "pytest-asyncio",
#   "loguru",
# ]
# ///
# this_file: tests/test_decorators.py

"""Tests for twat_cache decorators.

This module tests the core decorators (mcache, bcache, fcache, ucache)
and their fallback behavior.
"""

import asyncio
import pytest
from pathlib import Path
import time

from twat_cache.decorators import mcache, bcache, fcache, ucache


# Test utilities
def expensive_computation(x: int) -> int:
    """Simulate an expensive computation."""
    time.sleep(0.1)  # Simulate work
    return x * x


async def async_computation(x: int) -> int:
    """Simulate an async computation."""
    await asyncio.sleep(0.1)  # Simulate work
    return x * x


# Basic decorator tests
def test_mcache_basic():
    """Test basic memory caching."""

    @mcache()
    def func(x: int) -> int:
        return expensive_computation(x)

    # First call should compute
    start = time.time()
    result1 = func(5)
    time1 = time.time() - start

    # Second call should be from cache
    start = time.time()
    result2 = func(5)
    time2 = time.time() - start

    assert result1 == result2 == 25
    assert time2 < time1  # Cached call should be faster


def test_bcache_basic(tmp_path: Path):
    """Test basic disk caching."""
    cache_dir = tmp_path / "cache"

    @bcache(folder_name=str(cache_dir))
    def func(x: int) -> int:
        return expensive_computation(x)

    # First call should compute
    result1 = func(5)

    # Second call should be from cache
    result2 = func(5)

    assert result1 == result2 == 25
    assert cache_dir.exists()


def test_fcache_basic():
    """Test fast caching with cachebox."""

    @fcache()
    def func(x: int) -> int:
        return expensive_computation(x)

    # First call should compute
    result1 = func(5)

    # Second call should be from cache
    result2 = func(5)

    assert result1 == result2 == 25


def test_ucache_basic():
    """Test universal caching."""

    @ucache()
    def func(x: int) -> int:
        return expensive_computation(x)

    # First call should compute
    result1 = func(5)

    # Second call should be from cache
    result2 = func(5)

    assert result1 == result2 == 25


# Fallback tests
def test_ucache_fallback(monkeypatch):
    """Test ucache fallback behavior."""
    # Simulate no backends available except functools
    monkeypatch.setattr("twat_cache.engines.HAS_CACHEBOX", False)
    monkeypatch.setattr("twat_cache.engines.HAS_DISKCACHE", False)

    @ucache()
    def func(x: int) -> int:
        return expensive_computation(x)

    # Should still work with functools backend
    result = func(5)
    assert result == 25


# Async tests
@pytest.mark.asyncio
async def test_async_caching():
    """Test caching with async functions."""

    @ucache()
    async def func(x: int) -> int:
        return await async_computation(x)

    # First call
    result1 = await func(5)

    # Second call
    result2 = await func(5)

    assert result1 == result2 == 25


# Performance tests
def test_cache_performance():
    """Basic performance comparison of different caches."""
    results = {}
    times = {}

    # Test each decorator
    for decorator in [mcache(), bcache(), fcache(), ucache()]:

        @decorator
        def func(x: int) -> int:
            return expensive_computation(x)

        # Time first call
        start = time.time()
        results[decorator.__name__] = func(5)
        times[decorator.__name__] = time.time() - start

        # Time cached call
        start = time.time()
        _ = func(5)
        times[f"{decorator.__name__}_cached"] = time.time() - start

    # All results should be the same
    assert len(set(results.values())) == 1

    # Cached calls should be faster
    for name, time_taken in times.items():
        if name.endswith("_cached"):
            assert time_taken < times[name[:-7]]


# Error handling tests
def test_decorator_error_handling():
    """Test error handling in decorators."""

    @ucache()
    def func(x: int) -> int:
        if x < 0:
            msg = "Negative input"
            raise ValueError(msg)
        return x * x

    # Valid input should work
    assert func(5) == 25

    # Error should be raised consistently
    with pytest.raises(ValueError):
        func(-1)

    with pytest.raises(ValueError):
        func(-1)  # Same error from cache
