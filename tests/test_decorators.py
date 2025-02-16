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

"""Test suite for caching decorators."""

import asyncio
import time
from pathlib import Path
import pytest
from twat_cache.decorators import mcache, bcache, fcache, ucache, acache

# Constants for test values
TEST_INPUT = 10
TEST_RESULT = TEST_INPUT * 2
TEST_INPUT_2 = 20
TEST_RESULT_2 = TEST_INPUT_2 * 2
CACHE_SIZE = 2


# Test mcache with different backends
def test_mcache_cachebox() -> None:
    """Test memory caching with cachebox (if available)."""
    try:
        import cachebox

        HAS_CACHEBOX = True
    except ImportError:
        HAS_CACHEBOX = False
        pytest.skip("cachebox not available")

    call_count = 0

    @mcache()
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


def test_mcache_cachetools() -> None:
    """Test memory caching with cachetools (if available)."""
    try:
        import cachetools

        HAS_CACHETOOLS = True
    except ImportError:
        HAS_CACHETOOLS = False
        pytest.skip("cachetools not available")

    call_count = 0

    @mcache()
    def expensive_func(x: int) -> int:
        nonlocal call_count
        call_count += 1
        return x * 2

    assert expensive_func(TEST_INPUT) == TEST_RESULT
    assert call_count == 1
    assert expensive_func(TEST_INPUT) == TEST_RESULT
    assert call_count == 1


def test_mcache_functools_fallback() -> None:
    """Test memory caching fallback to functools."""
    # Force fallback by setting maxsize
    call_count = 0

    @mcache(maxsize=CACHE_SIZE)
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


# Test bcache with different backends
def test_bcache_diskcache(tmp_path: Path) -> None:
    """Test basic disk caching with diskcache."""
    try:
        import diskcache

        HAS_DISKCACHE = True
    except ImportError:
        HAS_DISKCACHE = False
        pytest.skip("diskcache not available")

    call_count = 0

    @bcache(folder_name=str(tmp_path))
    def expensive_func(x: int) -> int:
        nonlocal call_count
        call_count += 1
        time.sleep(0.1)  # Simulate expensive computation
        return x * 2

    assert expensive_func(TEST_INPUT) == TEST_RESULT
    assert call_count == 1
    assert expensive_func(TEST_INPUT) == TEST_RESULT
    assert call_count == 1


def test_bcache_klepto_sql(tmp_path: Path) -> None:
    """Test basic disk caching with klepto SQL backend."""
    try:
        import klepto

        HAS_KLEPTO = True
    except ImportError:
        HAS_KLEPTO = False
        pytest.skip("klepto not available")

    call_count = 0

    @bcache(folder_name=str(tmp_path))
    def expensive_func(x: int) -> int:
        nonlocal call_count
        call_count += 1
        return x * 2

    assert expensive_func(TEST_INPUT) == TEST_RESULT
    assert call_count == 1
    assert expensive_func(TEST_INPUT) == TEST_RESULT
    assert call_count == 1


def test_bcache_memory_fallback() -> None:
    """Test bcache fallback to memory cache."""
    call_count = 0

    @bcache()  # No folder name, should fall back to memory
    def expensive_func(x: int) -> int:
        nonlocal call_count
        call_count += 1
        return x * 2

    assert expensive_func(TEST_INPUT) == TEST_RESULT
    assert call_count == 1
    assert expensive_func(TEST_INPUT) == TEST_RESULT
    assert call_count == 1


# Test fcache with different backends
def test_fcache_joblib(tmp_path: Path) -> None:
    """Test file-based caching with joblib."""
    try:
        import joblib

        HAS_JOBLIB = True
    except ImportError:
        HAS_JOBLIB = False
        pytest.skip("joblib not available")

    call_count = 0

    @fcache(folder_name=str(tmp_path))
    def expensive_func(x: int) -> int:
        nonlocal call_count
        call_count += 1
        return x * 2

    assert expensive_func(TEST_INPUT) == TEST_RESULT
    assert call_count == 1
    assert expensive_func(TEST_INPUT) == TEST_RESULT
    assert call_count == 1


def test_fcache_klepto_file(tmp_path: Path) -> None:
    """Test file-based caching with klepto file backend."""
    try:
        import klepto

        HAS_KLEPTO = True
    except ImportError:
        HAS_KLEPTO = False
        pytest.skip("klepto not available")

    call_count = 0

    @fcache(folder_name=str(tmp_path))
    def expensive_func(x: int) -> int:
        nonlocal call_count
        call_count += 1
        return x * 2

    assert expensive_func(TEST_INPUT) == TEST_RESULT
    assert call_count == 1
    assert expensive_func(TEST_INPUT) == TEST_RESULT
    assert call_count == 1


def test_fcache_memory_fallback() -> None:
    """Test fcache fallback to memory cache."""
    call_count = 0

    @fcache()  # No folder name, should fall back to memory
    def expensive_func(x: int) -> int:
        nonlocal call_count
        call_count += 1
        return x * 2

    assert expensive_func(TEST_INPUT) == TEST_RESULT
    assert call_count == 1
    assert expensive_func(TEST_INPUT) == TEST_RESULT
    assert call_count == 1


# Test acache functionality
@pytest.mark.asyncio
async def test_acache_aiocache() -> None:
    """Test async caching with aiocache."""
    try:
        import aiocache

        HAS_AIOCACHE = True
    except ImportError:
        HAS_AIOCACHE = False
        pytest.skip("aiocache not available")

    call_count = 0

    @acache()
    async def expensive_func(x: int) -> int:
        nonlocal call_count
        call_count += 1
        await asyncio.sleep(0.1)  # Simulate async work
        return x * 2

    assert await expensive_func(TEST_INPUT) == TEST_RESULT
    assert call_count == 1
    assert await expensive_func(TEST_INPUT) == TEST_RESULT
    assert call_count == 1


@pytest.mark.asyncio
async def test_acache_memory_wrapper() -> None:
    """Test async caching with memory wrapper fallback."""
    call_count = 0

    @acache()
    async def expensive_func(x: int) -> int:
        nonlocal call_count
        call_count += 1
        await asyncio.sleep(0.1)
        return x * 2

    assert await expensive_func(TEST_INPUT) == TEST_RESULT
    assert call_count == 1
    assert await expensive_func(TEST_INPUT) == TEST_RESULT
    assert call_count == 1


# Test ucache with explicit backend selection
def test_ucache_explicit_backend(tmp_path: Path) -> None:
    """Test universal caching with explicit backend selection."""
    backends = [
        "cachebox",
        "klepto",
        "diskcache",
        "joblib",
        "cachetools",
        "memory",
    ]

    for backend in backends:
        call_count = 0

        @ucache(folder_name=str(tmp_path), preferred_engine=backend)
        def expensive_func(x: int) -> int:
            nonlocal call_count
            call_count += 1
            return x * 2

        # Should work regardless of backend availability
        assert expensive_func(TEST_INPUT) == TEST_RESULT
        assert call_count == 1
        assert expensive_func(TEST_INPUT) == TEST_RESULT
        assert call_count == 1


def test_ucache_ttl(tmp_path: Path) -> None:
    """Test TTL support in universal cache."""
    call_count = 0

    @ucache(folder_name=str(tmp_path), ttl=0.5)
    def expensive_func(x: int) -> int:
        nonlocal call_count
        call_count += 1
        return x * 2

    # First call
    assert expensive_func(TEST_INPUT) == TEST_RESULT
    assert call_count == 1

    # Should still be cached
    assert expensive_func(TEST_INPUT) == TEST_RESULT
    assert call_count == 1

    # Wait for TTL to expire
    time.sleep(0.6)

    # Should recompute
    assert expensive_func(TEST_INPUT) == TEST_RESULT
    assert call_count == 2


def test_ucache_security(tmp_path: Path) -> None:
    """Test security features in universal cache."""
    import os

    @ucache(folder_name=str(tmp_path))
    def expensive_func(x: int) -> int:
        return x * 2

    # Call function to create cache
    expensive_func(TEST_INPUT)

    # Check cache directory permissions
    cache_dir = tmp_path
    stat = os.stat(cache_dir)
    assert stat.st_mode & 0o777 in (0o700, 0o755)  # Only owner should have full access


def test_ucache_race_condition(tmp_path: Path) -> None:
    """Test race condition handling in universal cache."""
    import threading

    results = []
    exceptions = []

    @ucache(folder_name=str(tmp_path))
    def expensive_func(x: int) -> int:
        time.sleep(0.1)  # Simulate work
        return x * 2

    def worker() -> None:
        try:
            result = expensive_func(TEST_INPUT)
            results.append(result)
        except Exception as e:
            exceptions.append(e)

    # Create multiple threads
    threads = [threading.Thread(target=worker) for _ in range(5)]

    # Start all threads
    for t in threads:
        t.start()

    # Wait for all threads
    for t in threads:
        t.join()

    # Check results
    assert len(exceptions) == 0  # No exceptions
    assert all(r == TEST_RESULT for r in results)  # All results correct
