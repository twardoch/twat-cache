#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "pytest",
#   "pydantic",
#   "pydantic-settings",
# ]
# ///
# this_file: tests/test_engines.py

"""Tests for cache engine implementations."""

from pathlib import Path
from typing import Any

import pytest

from twat_cache.engines.base import CacheEngine
from twat_cache.engines.functools import FunctoolsCacheEngine
from twat_cache.engines.manager import EngineManager
from twat_cache.config import create_cache_config
from twat_cache.types import CacheConfig

# Test constants
TEST_KEY = "test_key"
TEST_VALUE = "test_value"
TEST_MAXSIZE = 100
TEST_FOLDER = "test_cache"
TEST_FUNCTION_RESULT = 42


@pytest.fixture
def engine_manager() -> EngineManager:
    """Provide a clean engine manager instance."""
    return EngineManager()


@pytest.fixture
def base_config() -> CacheConfig:
    """Provide a basic cache configuration."""
    return create_cache_config(maxsize=TEST_MAXSIZE)


@pytest.fixture
def base_engine(base_config: CacheConfig) -> CacheEngine[Any, Any]:
    """Provide a basic cache engine instance."""
    return FunctoolsCacheEngine(base_config)


def test_base_engine_initialization(base_config: CacheConfig) -> None:
    """Test basic engine initialization."""
    engine = FunctoolsCacheEngine(base_config)
    assert isinstance(engine, CacheEngine)
    assert engine._config == base_config


def test_base_engine_key_generation(base_engine: CacheEngine[Any, Any]) -> None:
    """Test key generation for different input types."""
    # Test with simple types
    assert isinstance(base_engine._make_key("test"), str)
    assert isinstance(base_engine._make_key(123), str)
    assert isinstance(base_engine._make_key(True), str)

    # Test with complex types
    assert isinstance(base_engine._make_key({"a": 1}), str)
    assert isinstance(base_engine._make_key([1, 2, 3]), str)
    assert isinstance(base_engine._make_key((1, "test")), str)


def test_base_engine_cache_decorator(base_engine: CacheEngine[Any, Any]) -> None:
    """Test the cache decorator functionality."""
    call_count = 0

    @base_engine.cache()
    def test_function(x: int) -> int:
        nonlocal call_count
        call_count += 1
        return x * 2

    # First call
    result = test_function(2)
    assert result == 4
    assert call_count == 1

    # Second call (should use cache)
    result = test_function(2)
    assert result == 4
    assert call_count == 1  # Should not increment


def test_base_engine_validation(base_config: CacheConfig) -> None:
    """Test engine configuration validation."""
    engine = FunctoolsCacheEngine(base_config)
    engine.validate_config()  # Should not raise

    # Test with invalid configuration
    with pytest.raises(ValueError, match="maxsize must be positive"):
        create_cache_config(maxsize=-1)


def test_lru_cache_initialization(base_config: CacheConfig) -> None:
    """Test LRU cache initialization."""
    engine = FunctoolsCacheEngine(base_config)
    assert isinstance(engine, FunctoolsCacheEngine)
    assert engine._config == base_config


def test_lru_cache_maxsize_enforcement(base_config: CacheConfig) -> None:
    """Test LRU cache maxsize enforcement."""
    engine = FunctoolsCacheEngine(base_config)

    # Add items up to maxsize
    for i in range(TEST_MAXSIZE):
        engine.set(str(i), i)

    # Add one more item
    engine.set("overflow", TEST_MAXSIZE)

    # First item should be evicted
    assert engine.get("0") is None


def test_lru_cache_clear(base_config: CacheConfig) -> None:
    """Test LRU cache clearing."""
    engine = FunctoolsCacheEngine(base_config)

    # Add some items
    engine.set(TEST_KEY, TEST_VALUE)
    assert engine.get(TEST_KEY) == TEST_VALUE

    # Clear cache
    engine.clear()
    assert engine.get(TEST_KEY) is None


def test_lru_cache_with_complex_values(base_config: CacheConfig) -> None:
    """Test LRU cache with complex value types."""
    engine = FunctoolsCacheEngine(base_config)

    # Test with different value types
    test_values = [
        {"key": "value"},
        [1, 2, 3],
        (4, 5, 6),
        Path("test.txt"),
        lambda x: x * 2,  # Functions should work too
    ]

    for i, value in enumerate(test_values):
        key = f"test_key_{i}"
        engine.set(key, value)
        assert engine.get(key) == value


def test_lru_cache_stats_accuracy(base_config: CacheConfig) -> None:
    """Test accuracy of LRU cache statistics."""
    engine = FunctoolsCacheEngine(base_config)

    # Test initial stats
    stats = engine.stats()
    assert stats.hits == 0
    assert stats.misses == 0
    assert stats.size == 0

    # Add an item and test
    engine.set(TEST_KEY, TEST_VALUE)
    stats = engine.stats()
    assert stats.size == 1

    # Test hit
    engine.get(TEST_KEY)
    stats = engine.stats()
    assert stats.hits == 1

    # Test miss
    engine.get("nonexistent")
    stats = engine.stats()
    assert stats.misses == 1
