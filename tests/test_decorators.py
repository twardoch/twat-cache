#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "pytest",
#   "pytest-asyncio",
#   "loguru",
#   "diskcache",
#   "joblib",
#   "types-pytest",
#   "cachetools",
#   "cachebox",
#   "klepto",
#   "aiocache",
# ]
# ///
# this_file: tests/test_decorators.py

"""Tests for the cache decorators."""

import asyncio
import time
from typing import Any

import pytest

from twat_cache.decorators import mcache, bcache, fcache, ucache, acache
from .test_constants import (
    CACHE_SIZE,
    CACHE_TTL,
    EXPECTED_CALLS_SINGLE,
    EXPECTED_CALLS_DOUBLE,
    EXPECTED_CALLS_TRIPLE,
    EXPECTED_CALLS_QUAD,
    SQUARE_INPUT,
    SQUARE_RESULT,
    TEST_KEY,
    TEST_BOOL,
    TEST_INT,
)


def test_memory_cache_cachebox() -> None:
    """Test memory caching with cachebox (if available)."""
    try:
        import cachebox

    except ImportError:
        pytest.skip("cachebox not available")

    call_count = 0

    @mcache(maxsize=CACHE_SIZE)
    def expensive_func(x: int) -> int:
        nonlocal call_count
        call_count += 1
        return x * x

    # First calls
    expensive_func(1)
    expensive_func(2)
    assert call_count == EXPECTED_CALLS_DOUBLE

    # Should still be cached
    expensive_func(1)
    expensive_func(2)
    assert call_count == EXPECTED_CALLS_DOUBLE

    # Should evict oldest entry
    expensive_func(3)
    assert call_count == EXPECTED_CALLS_TRIPLE
    expensive_func(1)  # Should recompute
    assert call_count == EXPECTED_CALLS_QUAD


def test_memory_cache_cachetools() -> None:
    """Test memory caching with cachetools (if available)."""
    try:
        import cachetools

    except ImportError:
        pytest.skip("cachetools not available")

    call_count = 0

    @mcache(maxsize=CACHE_SIZE)
    def expensive_func(x: int) -> int:
        nonlocal call_count
        call_count += 1
        return x * x

    # Test caching behavior
    assert expensive_func(SQUARE_INPUT) == SQUARE_RESULT
    assert expensive_func(SQUARE_INPUT) == SQUARE_RESULT
    assert call_count == EXPECTED_CALLS_SINGLE


def test_basic_disk_cache() -> None:
    """Test basic disk caching with diskcache."""
    try:
        import diskcache

    except ImportError:
        pytest.skip("diskcache not available")

    call_count = 0

    @bcache(maxsize=CACHE_SIZE)
    def expensive_func(x: int) -> int:
        nonlocal call_count
        call_count += 1
        return x * x

    # Test caching behavior
    assert expensive_func(SQUARE_INPUT) == SQUARE_RESULT
    assert expensive_func(SQUARE_INPUT) == SQUARE_RESULT
    assert call_count == EXPECTED_CALLS_SINGLE


def test_basic_disk_cache_sql() -> None:
    """Test basic disk caching with klepto SQL backend."""
    try:
        import klepto

    except ImportError:
        pytest.skip("klepto not available")

    call_count = 0

    @bcache(maxsize=CACHE_SIZE, use_sql=True)
    def expensive_func(x: int) -> int:
        nonlocal call_count
        call_count += 1
        return x * x

    # Test caching behavior
    assert expensive_func(SQUARE_INPUT) == SQUARE_RESULT
    assert expensive_func(SQUARE_INPUT) == SQUARE_RESULT
    assert call_count == EXPECTED_CALLS_SINGLE


def test_file_cache_joblib() -> None:
    """Test file-based caching with joblib."""
    try:
        import joblib

    except ImportError:
        pytest.skip("joblib not available")

    call_count = 0

    @fcache(maxsize=CACHE_SIZE)
    def expensive_func(x: int) -> int:
        nonlocal call_count
        call_count += 1
        return x * x

    # Test caching behavior
    assert expensive_func(SQUARE_INPUT) == SQUARE_RESULT
    assert expensive_func(SQUARE_INPUT) == SQUARE_RESULT
    assert call_count == EXPECTED_CALLS_SINGLE


def test_file_cache_klepto() -> None:
    """Test file-based caching with klepto file backend."""
    try:
        import klepto

    except ImportError:
        pytest.skip("klepto not available")

    call_count = 0

    @fcache(maxsize=CACHE_SIZE)
    def expensive_func(x: int) -> int:
        nonlocal call_count
        call_count += 1
        return x * x

    # Test caching behavior
    assert expensive_func(SQUARE_INPUT) == SQUARE_RESULT
    assert expensive_func(SQUARE_INPUT) == SQUARE_RESULT
    assert call_count == EXPECTED_CALLS_SINGLE


def test_universal_cache() -> None:
    """Test universal caching with automatic backend selection."""
    call_count = 0

    @ucache(maxsize=CACHE_SIZE)
    def expensive_func(x: int) -> int:
        nonlocal call_count
        call_count += 1
        return x * x

    # Test caching behavior
    assert expensive_func(SQUARE_INPUT) == SQUARE_RESULT
    assert expensive_func(SQUARE_INPUT) == SQUARE_RESULT
    assert call_count == EXPECTED_CALLS_SINGLE


async def test_async_cache() -> None:
    """Test async caching with aiocache."""
    try:
        import aiocache

    except ImportError:
        pytest.skip("aiocache not available")

    call_count = 0

    @acache(maxsize=CACHE_SIZE)
    async def expensive_func(x: int) -> int:
        nonlocal call_count
        call_count += 1
        await asyncio.sleep(0.1)
        return x * x

    # Test caching behavior
    result1 = await expensive_func(SQUARE_INPUT)
    assert result1 == SQUARE_RESULT

    result2 = await expensive_func(SQUARE_INPUT)
    assert result2 == SQUARE_RESULT
    assert call_count == EXPECTED_CALLS_SINGLE


def test_key_generation() -> None:
    """Test cache key generation."""
    call_count = 0

    @mcache()
    def test_func(x: Any) -> str:
        nonlocal call_count
        call_count += 1
        return str(x)

    # Test with different types
    test_func(TEST_KEY)
    test_func(TEST_BOOL)
    test_func(TEST_INT)
    assert call_count == EXPECTED_CALLS_TRIPLE

    # Test with same values
    test_func(TEST_KEY)
    test_func(TEST_BOOL)
    test_func(TEST_INT)
    assert call_count == EXPECTED_CALLS_TRIPLE  # Should use cache


def test_ttl_cache() -> None:
    """Test time-to-live cache behavior."""
    call_count = 0

    @mcache(ttl=CACHE_TTL)
    def expensive_func(x: int) -> int:
        nonlocal call_count
        call_count += 1
        return x * x

    # First call
    assert expensive_func(SQUARE_INPUT) == SQUARE_RESULT
    assert call_count == EXPECTED_CALLS_SINGLE

    # Should still be cached
    assert expensive_func(SQUARE_INPUT) == SQUARE_RESULT
    assert call_count == EXPECTED_CALLS_SINGLE

    # Wait for TTL to expire
    time.sleep(CACHE_TTL + 0.1)

    # Should recompute
    assert expensive_func(SQUARE_INPUT) == SQUARE_RESULT
    assert call_count == EXPECTED_CALLS_DOUBLE
