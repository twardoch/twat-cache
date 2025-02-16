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
#   "pydantic",
# ]
# ///
# this_file: tests/test_cache.py

"""Tests for the main cache interface."""

import asyncio
import os
import time
from pathlib import Path
from typing import Any, cast

import pytest
from pydantic import ValidationError

from twat_cache.cache import clear_cache, get_stats
from twat_cache.decorators import ucache, acache, mcache, bcache, fcache
from twat_cache.config import create_cache_config, CacheConfig


# Test constants
TEST_INPUT = 5
TEST_RESULT = TEST_INPUT * TEST_INPUT
TEST_INPUT_2 = 6
TEST_RESULT_2 = TEST_INPUT_2 * TEST_INPUT_2
EXPECTED_CALL_COUNT = 2
MIN_STATS_COUNT = 2
TEST_LIST_SUM = 15
TTL_DURATION = 0.5


def test_cache_settings_validation() -> None:
    """Test validation of cache settings."""
    # Valid settings
    config = create_cache_config(maxsize=100)
    assert config.maxsize == 100

    # Invalid maxsize
    with pytest.raises(ValidationError):
        create_cache_config(maxsize=-1)

    with pytest.raises(ValidationError):
        create_cache_config(maxsize=0)

    # Invalid TTL
    with pytest.raises(ValidationError):
        create_cache_config(ttl=-1)

    # Valid TTL and policy
    config = create_cache_config(ttl=1.0)
    assert config.policy == "ttl"  # Should auto-set policy to ttl

    # Valid eviction policies
    for policy in ["lru", "lfu", "fifo", "rr", "ttl"]:
        config = create_cache_config(policy=policy)
        assert config.policy == policy


def test_basic_caching() -> None:
    """Test basic caching functionality."""
    call_count = 0

    @ucache()
    def expensive_function(x: int) -> int:
        nonlocal call_count
        call_count += 1
        return x * x

    # First call should compute
    assert expensive_function(TEST_INPUT) == TEST_RESULT
    assert call_count == 1

    # Second call should use cache
    assert expensive_function(TEST_INPUT) == TEST_RESULT
    assert call_count == 1

    # Different input should compute
    assert expensive_function(TEST_INPUT_2) == TEST_RESULT_2
    assert call_count == EXPECTED_CALL_COUNT


def test_cache_clear() -> None:
    """Test cache clearing functionality."""
    call_count = 0

    @ucache()
    def cached_function(x: int) -> int:
        nonlocal call_count
        call_count += 1
        return x * x

    # First call
    assert cached_function(TEST_INPUT) == TEST_RESULT
    assert call_count == 1

    # Clear cache
    clear_cache()

    # Should recompute after clear
    assert cached_function(TEST_INPUT) == TEST_RESULT
    assert call_count == EXPECTED_CALL_COUNT


def test_cache_stats() -> None:
    """Test cache statistics."""
    call_count = 0

    @ucache()
    def cached_function(x: int) -> int:
        nonlocal call_count
        call_count += 1
        return x * x

    # Generate some cache activity
    for _i in range(3):
        cached_function(TEST_INPUT)
        cached_function(TEST_INPUT_2)

    # Get stats
    stats = get_stats()

    # Basic stats checks
    assert isinstance(stats, dict)
    assert stats["hits"] >= MIN_STATS_COUNT
    assert stats["misses"] >= MIN_STATS_COUNT
    assert "size" in stats
    assert "backend" in stats
    assert "policy" in stats
    assert "ttl" in stats


def test_list_processing() -> None:
    """Test caching with list processing."""
    call_count = 0

    @ucache()
    def process_list(data: list[int]) -> int:
        nonlocal call_count
        call_count += 1
        return sum(data)

    test_list = [1, 2, 3, 4, 5]

    # First call
    result1 = process_list(test_list)
    assert call_count == 1

    # Second call should use cache
    result2 = process_list(test_list)
    assert call_count == 1

    assert result1 == result2 == TEST_LIST_SUM


def test_different_backends() -> None:
    """Test using different cache backends."""
    results: list[Any] = []

    # Test with different configurations
    configs = [
        create_cache_config(maxsize=100),  # Memory cache
        create_cache_config(folder_name="disk_test", use_sql=True),  # SQL cache
        create_cache_config(folder_name="disk_test", use_sql=False),  # Disk cache
    ]

    for config in configs:

        @ucache(config=config)
        def cached_function(x: int) -> int:
            return x * x

        # Basic caching test
        result = cached_function(5)
        results.append(result)

        # Should be consistent across backends
        assert all(r == results[0] for r in results)

    # Clean up
    clear_cache()


def test_cache_with_complex_types() -> None:
    """Test caching with complex types."""

    @ucache(maxsize=100)
    def process_list(items: list[int]) -> int:
        return sum(items)

    test_list = [1, 2, 3, 4, 5]

    # First call
    result1 = process_list(test_list)

    # Second call (should use cache)
    result2 = process_list(test_list)

    assert result1 == result2 == 15


def test_cache_exceptions() -> None:
    """Test caching of exceptions."""
    call_count = 0

    @ucache(maxsize=100)
    def failing_function(x: int) -> None:
        nonlocal call_count
        call_count += 1
        msg = "Test error"
        raise ValueError(msg)

    # First call
    with pytest.raises(ValueError):
        failing_function(5)
    assert call_count == 1

    # Second call should not recompute
    with pytest.raises(ValueError):
        failing_function(5)
    assert call_count == 1


def test_kwargs_handling() -> None:
    """Test caching with different keyword arguments."""
    call_count = 0

    @ucache()
    def kwarg_function(x: int, multiplier: int = 1) -> int:
        nonlocal call_count
        call_count += 1
        return x * multiplier

    # Test with different kwarg combinations
    assert kwarg_function(TEST_INPUT) == TEST_INPUT
    assert call_count == 1

    assert kwarg_function(TEST_INPUT, multiplier=1) == TEST_INPUT
    assert call_count == 1  # Should use cache

    assert kwarg_function(TEST_INPUT, multiplier=2) == TEST_INPUT * 2
    assert call_count == EXPECTED_CALL_COUNT  # Different kwargs = new computation


def test_ttl_caching(tmp_path: Path) -> None:
    """Test TTL (Time To Live) functionality."""
    call_count = 0

    @ucache(folder_name=str(tmp_path), ttl=TTL_DURATION)
    def cached_function(x: int) -> int:
        nonlocal call_count
        call_count += 1
        return x * x

    # First call
    assert cached_function(TEST_INPUT) == TEST_RESULT
    assert call_count == 1

    # Second call should use cache
    assert cached_function(TEST_INPUT) == TEST_RESULT
    assert call_count == 1

    # Wait for TTL to expire
    time.sleep(TTL_DURATION + 0.1)

    # Should recompute after TTL expires
    assert cached_function(TEST_INPUT) == TEST_RESULT
    assert call_count == EXPECTED_CALL_COUNT


def test_security_features(tmp_path: Path) -> None:
    """Test security features for disk caches."""

    @ucache(folder_name=str(tmp_path), secure=True)
    def cached_function(x: int) -> int:
        return x * x

    # Call function to create cache
    cached_function(TEST_INPUT)

    # Check cache directory permissions
    cache_path = tmp_path
    assert cache_path.exists()

    # On Unix-like systems, check permissions
    if os.name == "posix":
        mode = cache_path.stat().st_mode & 0o777
        assert mode == 0o700


@pytest.mark.asyncio
async def test_async_caching() -> None:
    """Test async caching functionality."""
    call_count = 0

    @acache()
    async def async_function(x: int) -> int:
        nonlocal call_count
        call_count += 1
        await asyncio.sleep(0.1)  # Simulate async work
        return x * x

    # First call
    result1 = await async_function(TEST_INPUT)
    assert result1 == TEST_RESULT
    assert call_count == 1

    # Second call should use cache
    result2 = await async_function(TEST_INPUT)
    assert result2 == TEST_RESULT
    assert call_count == 1


def test_specific_decorators() -> None:
    """Test each specific cache decorator."""

    # Test memory cache
    @mcache(maxsize=100)
    def mem_func(x: int) -> int:
        return x * x

    assert mem_func(5) == 25
    assert mem_func(5) == 25  # Should use cache

    # Test basic disk cache
    @bcache(folder_name="test_disk")
    def disk_func(x: int) -> int:
        return x * x

    assert disk_func(5) == 25
    assert disk_func(5) == 25  # Should use cache

    # Test file cache
    @fcache(folder_name="test_file")
    def file_func(x: int) -> int:
        return x * x

    assert file_func(5) == 25
    assert file_func(5) == 25  # Should use cache

    # Clean up
    clear_cache()
