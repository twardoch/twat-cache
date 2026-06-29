#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "pytest",
#   "pydantic",
# ]
# ///
# this_file: tests/test_engines.py

"""Tests for cache engine implementations."""

import time
from typing import Any

import pytest

from twat_cache.engines.base import BaseCacheEngine
from twat_cache.engines.functools_engine import FunctoolsCacheEngine
from twat_cache.engines.manager import CacheEngineManager
from twat_cache.config import create_cache_config, CacheConfig
from .test_constants import (
    CACHE_SIZE,
    EXPECTED_CALLS_SINGLE,
    SQUARE_INPUT,
    SQUARE_RESULT,
    TEST_KEY,
    TEST_BOOL,
    TEST_INT,
    TEST_LIST,
)

# Test constants
TEST_VALUE = "test_value"
TEST_FOLDER = "test_cache"
TEST_FUNCTION_RESULT = 42


@pytest.fixture
def engine_manager() -> CacheEngineManager:
    """Provide a clean engine manager instance."""
    return CacheEngineManager()


@pytest.fixture
def base_config() -> CacheConfig:
    """Provide a basic cache configuration."""
    return create_cache_config(maxsize=CACHE_SIZE)


@pytest.fixture
def base_engine(base_config: CacheConfig) -> FunctoolsCacheEngine[Any, Any]:
    """Provide a basic cache engine instance."""
    return FunctoolsCacheEngine(base_config)


def create_test_engine() -> FunctoolsCacheEngine:
    """Create a test cache engine instance."""
    config = CacheConfig(
        maxsize=CACHE_SIZE,
        folder_name="test",
        secure=True,
    )
    return FunctoolsCacheEngine(config)


def test_engine_initialization() -> None:
    """Test cache engine initialization."""
    engine = create_test_engine()
    assert isinstance(engine, FunctoolsCacheEngine)
    assert engine._config.maxsize == CACHE_SIZE


def test_key_generation() -> None:
    """Test cache key generation."""
    engine = create_test_engine()

    def dummy() -> None:
        pass

    # _make_key returns a CacheKey; verify it is not None and differs across args
    keys = set()
    for arg in (TEST_KEY, TEST_INT, TEST_BOOL, (1, 2, 3)):
        key = engine._make_key(dummy, (arg,), {})
        assert key is not None
        keys.add(str(key))  # str() is always hashable; just verify distinctness
    assert len(keys) == 4  # each distinct arg yields a distinct key


def test_cache_operations() -> None:
    """Test basic cache operations via engine.cache decorator."""
    engine = create_test_engine()
    call_count = 0

    @engine.cache
    def test_function(x: int) -> int:
        nonlocal call_count
        call_count += 1
        return x * x

    # First call — cache miss
    result = test_function(SQUARE_INPUT)
    assert result == SQUARE_RESULT
    assert call_count == EXPECTED_CALLS_SINGLE

    # Second call — cache hit
    result = test_function(SQUARE_INPUT)
    assert result == SQUARE_RESULT
    assert call_count == EXPECTED_CALLS_SINGLE  # not incremented


def test_cache_eviction() -> None:
    """Test cache eviction when maxsize is exceeded."""
    engine = create_test_engine()

    for i in range(CACHE_SIZE + 1):
        engine.set(str(i), i)

    assert len(engine._cache) <= CACHE_SIZE


def test_cache_ttl() -> None:
    """Test time-to-live behaviour."""
    config = CacheConfig(maxsize=CACHE_SIZE, ttl=0.1)
    engine = FunctoolsCacheEngine(config)
    call_count = 0

    @engine.cache
    def test_function(x: int) -> int:
        nonlocal call_count
        call_count += 1
        return x * x

    # First call — cache miss
    result = test_function(SQUARE_INPUT)
    assert result == SQUARE_RESULT
    assert call_count == EXPECTED_CALLS_SINGLE

    # Wait for TTL to expire
    time.sleep(0.2)

    # Should recompute after TTL
    result = test_function(SQUARE_INPUT)
    assert result == SQUARE_RESULT
    assert call_count == EXPECTED_CALLS_SINGLE + 1


def test_cache_clear() -> None:
    """Test cache clearing."""
    engine = create_test_engine()

    for i in range(CACHE_SIZE):
        engine.set(str(i), i)

    engine.clear()
    assert len(engine._cache) == 0


def test_cache_stats() -> None:
    """Test cache statistics tracking via engine.cache decorator."""
    engine = create_test_engine()
    call_count = 0

    @engine.cache
    def test_function(x: int) -> int:
        nonlocal call_count
        call_count += 1
        return x * x

    # First call (miss)
    result = test_function(SQUARE_INPUT)
    assert result == SQUARE_RESULT
    assert engine.stats["misses"] == 1

    # Second call (hit)
    result = test_function(SQUARE_INPUT)
    assert result == SQUARE_RESULT
    assert engine.stats["hits"] == 1
