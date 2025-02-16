#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "pytest",
#   "loguru",
#   "diskcache",
#   "joblib",
#   "types-pytest",
# ]
# ///
# this_file: tests/test_decorators.py

"""Test suite for caching decorators."""

import time
from pathlib import Path
from twat_cache.decorators import mcache, bcache, fcache, ucache

# Constants for test values
TEST_INPUT = 10
TEST_RESULT = TEST_INPUT * 2
TEST_INPUT_2 = 20
TEST_RESULT_2 = TEST_INPUT_2 * 2
CACHE_SIZE = 2


def test_mcache_basic() -> None:
    """Test basic memory caching functionality."""
    call_count = 0

    @mcache()  # type: ignore
    def expensive_func(x: int) -> int:
        nonlocal call_count
        call_count += 1
        return x * 2

    # First call should compute
    assert expensive_func(TEST_INPUT) == TEST_RESULT
    assert call_count == 1

    # Second call should use cache
    assert expensive_func(TEST_INPUT) == TEST_RESULT
    assert call_count == 1

    # Different input should compute
    assert expensive_func(TEST_INPUT_2) == TEST_RESULT_2
    assert call_count == 2


def test_mcache_maxsize() -> None:
    """Test memory cache size limiting."""
    call_count = 0

    @mcache(maxsize=CACHE_SIZE)  # type: ignore
    def expensive_func(x: int) -> int:
        nonlocal call_count
        call_count += 1
        return x * 2

    # Fill cache
    expensive_func(1)
    expensive_func(2)
    assert call_count == 2

    # Should still be cached
    expensive_func(1)
    expensive_func(2)
    assert call_count == 2

    # Should evict oldest entry
    expensive_func(3)
    assert call_count == 3
    expensive_func(1)  # Should recompute
    assert call_count == 4


def test_bcache_basic(tmp_path: Path) -> None:
    """Test basic disk caching functionality."""
    call_count = 0

    @bcache(folder_name=str(tmp_path))  # type: ignore
    def expensive_func(x: int) -> int:
        nonlocal call_count
        call_count += 1
        time.sleep(0.1)  # Simulate expensive computation
        return x * 2

    # First call should compute
    assert expensive_func(TEST_INPUT) == TEST_RESULT
    assert call_count == 1

    # Second call should use cache
    assert expensive_func(TEST_INPUT) == TEST_RESULT
    assert call_count == 1

    # Different input should compute
    assert expensive_func(TEST_INPUT_2) == TEST_RESULT_2
    assert call_count == 2


def test_fcache_basic(tmp_path: Path) -> None:
    """Test basic file-based caching functionality."""
    call_count = 0

    @fcache(folder_name=str(tmp_path))  # type: ignore
    def expensive_func(x: int) -> int:
        nonlocal call_count
        call_count += 1
        time.sleep(0.1)  # Simulate expensive computation
        return x * 2

    # First call should compute
    assert expensive_func(TEST_INPUT) == TEST_RESULT
    assert call_count == 1

    # Second call should use cache
    assert expensive_func(TEST_INPUT) == TEST_RESULT
    assert call_count == 1

    # Different input should compute
    assert expensive_func(TEST_INPUT_2) == TEST_RESULT_2
    assert call_count == 2


def test_ucache_basic(tmp_path: Path) -> None:
    """Test universal caching with different preferences."""
    call_count = 0

    @ucache(folder_name=str(tmp_path), preferred_engine="disk")  # type: ignore
    def expensive_func(x: int) -> int:
        nonlocal call_count
        call_count += 1
        return x * 2

    # First call should compute
    assert expensive_func(TEST_INPUT) == TEST_RESULT
    assert call_count == 1

    # Second call should use cache
    assert expensive_func(TEST_INPUT) == TEST_RESULT
    assert call_count == 1

    # Different input should compute
    assert expensive_func(TEST_INPUT_2) == TEST_RESULT_2
    assert call_count == 2


def test_ucache_fallback() -> None:
    """Test universal caching fallback behavior."""
    call_count = 0

    @ucache(preferred_engine="nonexistent")  # type: ignore
    def expensive_func(x: int) -> int:
        nonlocal call_count
        call_count += 1
        return x * 2

    # Should fall back to memory cache
    assert expensive_func(TEST_INPUT) == TEST_RESULT
    assert call_count == 1
    assert expensive_func(TEST_INPUT) == TEST_RESULT
    assert call_count == 1
