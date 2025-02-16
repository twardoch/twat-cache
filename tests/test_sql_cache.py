#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "pytest",
#   "loguru",
#   "sqlalchemy",
#   "sqlalchemy-utils",
# ]
# ///
# this_file: tests/test_sql_cache.py

"""Test suite for SQL cache engine."""

import shutil
import time
from pathlib import Path
from typing import Any, Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from twat_cache.config import CacheConfig
from twat_cache.engines.sql import SQLCacheEngine

# Test constants
TEST_INPUT = 5
TEST_RESULT = TEST_INPUT * TEST_INPUT
TEST_INPUT_2 = 6
TEST_RESULT_2 = TEST_INPUT_2 * TEST_INPUT_2
EXPECTED_CALL_COUNT = 2
MIN_STATS_COUNT = 2
MAX_CACHE_SIZE = 100
TEST_LIST_SUM = 15
TEST_LIST_LEN = 5


@pytest.fixture
def test_cache_dir(tmp_path: Path) -> Generator[Path, None, None]:
    """Provide a temporary cache directory."""
    cache_dir = tmp_path / "test_cache"
    cache_dir.mkdir(parents=True)
    yield cache_dir
    shutil.rmtree(cache_dir)


@pytest.fixture
def db_path(tmp_path: Path) -> Path:
    """Provide a temporary database path."""
    return tmp_path / "test.db"


@pytest.fixture
def sql_cache(db_path: Path) -> SQLCacheEngine[Any, Any]:
    """Create an SQL cache engine instance."""
    config = CacheConfig(maxsize=MAX_CACHE_SIZE, cache_dir=str(db_path))
    return SQLCacheEngine(config)


def test_sql_init(sql_cache: SQLCacheEngine[Any, Any], db_path: Path) -> None:
    """Test SQL cache initialization."""
    # Check that tables were created
    db_engine = create_engine(f"sqlite:///{db_path}")
    session_factory = sessionmaker(bind=db_engine)
    with session_factory() as session:
        # Should not raise
        session.execute("SELECT * FROM cache_entries")


def test_sql_caching(sql_cache: SQLCacheEngine[Any, Any]) -> None:
    """Test basic SQL caching."""
    call_count = 0

    def test_func(x: int) -> int:
        nonlocal call_count
        call_count += 1
        return x * x

    cached_func = sql_cache.cache(test_func)

    # First call should compute
    assert cached_func(TEST_INPUT) == TEST_RESULT
    assert call_count == 1

    # Second call should use cache
    assert cached_func(TEST_INPUT) == TEST_RESULT
    assert call_count == 1

    # Different input should compute
    assert cached_func(TEST_INPUT_2) == TEST_RESULT_2
    assert call_count == EXPECTED_CALL_COUNT


def test_sql_pruning(sql_cache: SQLCacheEngine[Any, Any]) -> None:
    """Test SQL cache pruning."""
    # Fill cache beyond maxsize
    for i in range(MAX_CACHE_SIZE + 50):
        sql_cache._set_cached_value(f"key_{i}", i)

    # Check that cache was pruned
    stats = sql_cache.stats
    assert stats["size"] <= MAX_CACHE_SIZE


def test_sql_complex_data(sql_cache: SQLCacheEngine[Any, Any]) -> None:
    """Test SQL cache with complex data structures."""
    call_count = 0

    def process_list(data: list[int]) -> dict[str, int]:
        nonlocal call_count
        call_count += 1
        return {"sum": sum(data), "len": len(data)}

    cached_func = sql_cache.cache(process_list)

    test_list = [1, 2, 3, 4, 5]

    # First call
    result1 = cached_func(test_list)

    # Second call should use cache
    result2 = cached_func(test_list)

    assert result1 == result2
    assert result1["sum"] == TEST_LIST_SUM
    assert result1["len"] == TEST_LIST_LEN


def test_sql_stats(sql_cache: SQLCacheEngine[Any, Any]) -> None:
    """Test SQL cache statistics."""
    call_count = 0

    def test_func(x: int, multiplier: int = 1) -> int:
        nonlocal call_count
        call_count += 1
        return x * multiplier

    cached_func = sql_cache.cache(test_func)

    # Generate some cache activity
    cached_func(TEST_INPUT)
    cached_func(TEST_INPUT)  # Hit
    cached_func(TEST_INPUT_2)
    cached_func(TEST_INPUT_2)  # Hit

    # Check stats
    stats = sql_cache.stats
    assert stats["hits"] >= MIN_STATS_COUNT
    assert stats["misses"] >= MIN_STATS_COUNT
    assert stats["size"] == EXPECTED_CALL_COUNT


def test_sql_key_generation(sql_cache: SQLCacheEngine[Any, Any]) -> None:
    """Test SQL cache key generation."""
    call_count = 0

    def test_func(x: int, multiplier: int = 1) -> int:
        nonlocal call_count
        call_count += 1
        return x * multiplier

    cached_func = sql_cache.cache(test_func)

    # Different args should have different keys
    cached_func(TEST_INPUT)
    cached_func(TEST_INPUT_2)
    assert sql_cache.stats["size"] == EXPECTED_CALL_COUNT

    # Different kwargs should have different keys
    cached_func(TEST_INPUT, multiplier=2)
    assert sql_cache.stats["size"] == 3

    # Same args and kwargs should use same key
    cached_func(TEST_INPUT, multiplier=2)
    assert sql_cache.stats["size"] == 3


def test_sql_cache_exceptions(sql_cache: SQLCacheEngine[Any, Any]) -> None:
    """Test caching of exceptions."""
    call_count = 0

    @sql_cache.cache
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
