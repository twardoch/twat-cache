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

"""Test suite for twat_cache core functionality."""

import asyncio
import os
import time
import tempfile
from pathlib import Path
from typing import Any

import pytest

from twat_cache.cache import clear_cache, get_stats
from twat_cache.decorators import ucache, acache # acache added for consistency, though not used here
from twat_cache.config import create_cache_config
from twat_cache.paths import get_cache_path
from tests.test_constants import (
    TEST_VALUE,
    TEST_RESULT,
    SMALL_CACHE_SIZE,
    DIR_PERMISSIONS,
    TEST_CACHE_DIR,
    CACHE_SIZE,
    FILE_PERMISSIONS,
    SQUARE_INPUT,
    SQUARE_RESULT,
    TEST_LIST,
    TEST_LIST_SUM,
    EXPECTED_CALLS_SINGLE,
)


# Test constants
TEST_INPUT = 5
TEST_INPUT_2 = 6
EXPECTED_CALL_COUNT = 2
MIN_STATS_COUNT = 2
TTL_DURATION = 0.5


def test_config_validation() -> None:
    """Test configuration validation."""
    # Valid settings
    config = create_cache_config(maxsize=CACHE_SIZE)
    assert config.maxsize == CACHE_SIZE

    # Invalid maxsize
    with pytest.raises(ValueError):
        create_cache_config(maxsize=-1)

    # Invalid ttl
    with pytest.raises(ValueError):
        create_cache_config(ttl=-1)


def test_cache_path() -> None:
    """Test cache path generation."""
    # Default path
    path = get_cache_path()
    assert path.exists()
    assert path.is_dir()

    # Custom path
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        path = get_cache_path(folder_name="test", cache_dir=str(temp_path))
        assert path.parent == temp_path
        assert "test" in path.name


def test_cache_clear() -> None:
    """Test cache clearing."""
    # Create a test cache file
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        test_file = temp_path / "test.cache"
        test_file.touch()

        # Clear cache
        clear_cache(folder_name="test", cache_dir=str(temp_path))
        assert not test_file.exists()


# Removed test_cache_stats that used mcache

def test_cache_security() -> None:
    """Test cache security features."""
    # Test file permissions
    if os.name == "posix":
        cache_path = get_cache_path()
        mode = cache_path.stat().st_mode & 0o777
        assert mode == FILE_PERMISSIONS


# Removed test_cache_decorators (used mcache, bcache, fcache)
# Removed test_cache_basic (used mcache)
# Removed test_cache_size (used mcache)
# Removed test_cache_clear (the one that used mcache and square.cache_clear())
# Removed the third test_cache_stats (the one that used mcache and square.cache_info())
# Removed test_cache_permissions (used bcache)
# Removed test_cache_types (used mcache, bcache, fcache)


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

        @ucache(
            maxsize=config.maxsize,
            folder_name=config.folder_name,
            use_sql=config.use_sql,
        )
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

    @ucache(use_async=True)
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


# Removed duplicated test_basic_memory_cache (used bcache)
# Removed duplicated test_cache_clear (used bcache and square.clear())
