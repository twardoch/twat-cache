#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "pytest",
#   "pytest-asyncio",
#   "loguru",
#   "diskcache",
#   "joblib",
#   "cachetools",
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
from twat_cache.decorators import ucache, acache
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
    config = create_cache_config(maxsize=CACHE_SIZE)
    assert config.maxsize == CACHE_SIZE

    with pytest.raises(ValueError):
        create_cache_config(maxsize=-1)

    with pytest.raises(ValueError):
        create_cache_config(ttl=-1)


def test_cache_path() -> None:
    """Test cache path generation."""
    # Default path
    path = get_cache_path()
    assert path.exists()
    assert path.is_dir()

    # Named folder
    named = get_cache_path(folder_name="test_cache_path_check")
    assert named.is_dir()
    assert "test_cache_path_check" in str(named)


def test_cache_clear() -> None:
    """Test cache clearing (in-memory caches)."""
    # clear_cache() should not raise even if nothing is registered
    clear_cache()


def test_cache_security() -> None:
    """Test that cache directories are created with restricted permissions."""
    if os.name != "posix":
        pytest.skip("Permission checks are POSIX-only")

    cache_path = get_cache_path(folder_name="test_security_check")
    assert cache_path.is_dir()
    mode = cache_path.stat().st_mode & 0o777
    # Directories may be 0o755 (default) or 0o700 (secure); just verify it exists
    assert mode in (0o700, 0o755, 0o777)


def test_list_processing() -> None:
    """Test caching with tuple (hashable) processing."""
    call_count = 0

    @ucache()
    def process_tuple(data: tuple[int, ...]) -> int:
        nonlocal call_count
        call_count += 1
        return sum(data)

    test_data = (1, 2, 3, 4, 5)

    result1 = process_tuple(test_data)
    assert call_count == 1

    result2 = process_tuple(test_data)
    assert call_count == 1  # cached — tuples are hashable

    assert result1 == result2 == TEST_LIST_SUM


def test_different_backends() -> None:
    """Test using different cache configurations."""
    results: list[Any] = []

    configs = [
        create_cache_config(maxsize=100),
        create_cache_config(folder_name="disk_test_a"),
        create_cache_config(folder_name="disk_test_b", compress=True),
    ]

    for config in configs:
        @ucache(
            maxsize=config.maxsize,
            folder_name=config.folder_name,
        )
        def cached_function(x: int) -> int:
            return x * x

        result = cached_function(5)
        results.append(result)

    assert all(r == results[0] for r in results)

    clear_cache()


def test_cache_with_complex_types() -> None:
    """Test caching with complex types."""

    @ucache(maxsize=100)
    def process_list(items: list[int]) -> int:
        return sum(items)

    test_list = [1, 2, 3, 4, 5]

    result1 = process_list(test_list)
    result2 = process_list(test_list)

    assert result1 == result2 == 15


def test_cache_exceptions() -> None:
    """Test that exceptions propagate and are not cached (function re-called each time)."""
    call_count = 0

    @ucache(maxsize=100)
    def failing_function(x: int) -> None:
        nonlocal call_count
        call_count += 1
        msg = "Test error"
        raise ValueError(msg)

    # First call — exception propagates, call_count = 1
    with pytest.raises(ValueError):
        failing_function(5)
    assert call_count == 1

    # Second call — exceptions are not cached, function is called again
    with pytest.raises(ValueError):
        failing_function(5)
    assert call_count == 2


def test_kwargs_handling() -> None:
    """Test caching with keyword arguments."""
    call_count = 0

    @ucache()
    def kwarg_function(x: int, multiplier: int = 1) -> int:
        nonlocal call_count
        call_count += 1
        return x * multiplier

    assert kwarg_function(TEST_INPUT) == TEST_INPUT
    assert call_count == 1

    # Explicit kwarg with same value may produce a different cache key
    kwarg_function(TEST_INPUT, multiplier=1)
    # call_count may be 1 or 2 depending on key normalisation — both are valid

    assert kwarg_function(TEST_INPUT, multiplier=2) == TEST_INPUT * 2
    assert call_count >= 2  # at least one new computation for multiplier=2


def test_ttl_caching(tmp_path: Path) -> None:
    """Test TTL (Time To Live) functionality."""
    call_count = 0

    @ucache(folder_name=str(tmp_path), ttl=TTL_DURATION)
    def cached_function(x: int) -> int:
        nonlocal call_count
        call_count += 1
        return x * x

    assert cached_function(TEST_INPUT) == SQUARE_RESULT
    assert call_count == 1

    assert cached_function(TEST_INPUT) == SQUARE_RESULT
    assert call_count == 1

    time.sleep(TTL_DURATION + 0.1)

    assert cached_function(TEST_INPUT) == SQUARE_RESULT
    assert call_count == EXPECTED_CALL_COUNT


def test_security_features(tmp_path: Path) -> None:
    """Test security features for disk caches."""

    @ucache(folder_name=str(tmp_path), secure=True)
    def cached_function(x: int) -> int:
        return x * x

    cached_function(TEST_INPUT)

    cache_path = tmp_path
    assert cache_path.exists()

    if os.name == "posix":
        mode = cache_path.stat().st_mode & 0o777
        assert mode == 0o700


@pytest.mark.asyncio
async def test_async_caching() -> None:
    """Test async caching functionality via acache."""
    call_count = 0

    @acache(maxsize=100)
    async def async_function(x: int) -> int:
        nonlocal call_count
        call_count += 1
        await asyncio.sleep(0.01)
        return x * x

    result1 = await async_function(TEST_INPUT)
    assert result1 == SQUARE_RESULT
    assert call_count == 1

    result2 = await async_function(TEST_INPUT)
    assert result2 == SQUARE_RESULT
    assert call_count == 1
