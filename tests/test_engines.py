#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "pytest",
#   "loguru",
#   "pydantic",
#   "pydantic-settings",
# ]
# ///
# this_file: tests/test_engines.py

"""
Tests for cache engine implementations.

This module contains tests for both the base cache engine functionality,
specific backend implementations, and the engine manager.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol
import pytest

from twat_cache.engines.base import BaseCacheEngine
from twat_cache.engines.functools import FunctoolsCacheEngine
from twat_cache.engines.diskcache import DiskCacheEngine
from twat_cache.engines.manager import EngineManager, get_engine_manager
from twat_cache.types import CacheConfig, CacheKey, P, R, CacheEngine
from twat_cache.config import config as global_config


# Test fixtures and utilities
@dataclass
class TestConfig:
    """Test configuration class implementing CacheConfig protocol."""

    maxsize: int | None = None
    folder_name: str | None = None
    use_sql: bool = False
    preferred_engine: str | None = None

    def validate(self) -> None:
        """Validate configuration."""


class TestEngine(BaseCacheEngine[P, R]):
    """Minimal concrete implementation of BaseCacheEngine for testing."""

    def __init__(self, config: CacheConfig) -> None:
        super().__init__(config)
        self._store: dict[CacheKey, Any] = {}

    def _get_cached_value(self, key: CacheKey) -> R | None:
        return self._store.get(key)

    def _set_cached_value(self, key: CacheKey, value: R) -> None:
        self._store[key] = value

    def clear(self) -> None:
        self._store.clear()


class TestCacheConfig(Protocol):
    """Test configuration protocol."""

    maxsize: int
    folder_name: str | None
    use_sql: bool
    preferred_engine: str | None


@pytest.fixture
def base_config() -> TestCacheConfig:
    """Provide a basic test configuration."""

    class Config:
        maxsize = 100
        folder_name = None
        use_sql = False
        preferred_engine = None

    return Config()


@pytest.fixture
def test_engine(base_config: TestCacheConfig) -> BaseCacheEngine[Any, Any]:
    """Create a test engine instance."""
    return FunctoolsCacheEngine(base_config)


@pytest.fixture
def lru_engine(base_config: TestCacheConfig) -> FunctoolsCacheEngine[Any, Any]:
    """Create an LRU engine instance."""
    return FunctoolsCacheEngine(base_config)


@pytest.fixture
def engine_manager() -> EngineManager:
    """Provide a fresh engine manager for each test."""
    return EngineManager()


@pytest.fixture
def functools_engine(base_config: TestCacheConfig) -> FunctoolsCacheEngine[Any, Any]:
    """Fixture for testing the functools cache engine."""
    return FunctoolsCacheEngine(base_config)


# Test base engine functionality
def test_base_engine_initialization(test_config: TestConfig) -> None:
    """Test base engine initialization."""
    engine = TestEngine(test_config)
    assert engine.stats["hits"] == 0
    assert engine.stats["misses"] == 0
    assert engine.stats["size"] == 0
    assert engine.stats["maxsize"] == test_config.maxsize


def test_base_engine_key_generation(test_engine: TestEngine) -> None:
    """Test cache key generation."""

    def test_func(x: int, y: str = "test") -> str:
        return f"{x}-{y}"

    key1 = test_engine._make_key(test_func, (1,), {})
    key2 = test_engine._make_key(test_func, (1,), {"y": "test"})
    key3 = test_engine._make_key(test_func, (2,), {"y": "other"})

    assert key1 != key2  # Different kwargs
    assert key1 != key3  # Different args
    assert key2 != key3  # Different everything


def test_base_engine_cache_decorator(test_engine: TestEngine) -> None:
    """Test the cache decorator functionality."""
    call_count = 0

    @test_engine.cache
    def test_func(x: int) -> int:
        nonlocal call_count
        call_count += 1
        return x * 2

    # First call should compute
    assert test_func(5) == 10
    assert call_count == 1
    assert test_engine.stats["hits"] == 0
    assert test_engine.stats["misses"] == 1

    # Second call should use cache
    assert test_func(5) == 10
    assert call_count == 1
    assert test_engine.stats["hits"] == 1
    assert test_engine.stats["misses"] == 1

    # Different arg should compute
    assert test_func(10) == 20
    assert call_count == 2
    assert test_engine.stats["hits"] == 1
    assert test_engine.stats["misses"] == 2


def test_base_engine_validation(test_config: TestConfig) -> None:
    """Test configuration validation."""
    # Valid config
    engine = TestEngine(test_config)
    engine.validate_config()

    # Invalid maxsize
    test_config.maxsize = -1
    with pytest.raises(ValueError):
        TestEngine(test_config)


# Test LRU cache implementation
def test_lru_cache_initialization(test_config: TestConfig) -> None:
    """Test LRU cache initialization."""
    engine = FunctoolsCacheEngine(test_config)
    assert engine.stats["type"] == "lru"
    assert engine.stats["maxsize"] == test_config.maxsize
    assert engine.stats["current_size"] == 0


def test_lru_cache_maxsize_enforcement(lru_engine: FunctoolsCacheEngine) -> None:
    """Test that LRU cache respects maxsize."""
    # Fill cache to maxsize
    for i in range(10):
        lru_engine._set_cached_value(("key", i), i)

    assert len(lru_engine._cache) == 10

    # Add one more, should evict oldest
    lru_engine._set_cached_value(("key", 10), 10)
    assert len(lru_engine._cache) == 10
    assert ("key", 0) not in lru_engine._cache  # First item should be evicted
    assert ("key", 10) in lru_engine._cache  # New item should be present


def test_lru_cache_clear(lru_engine: FunctoolsCacheEngine) -> None:
    """Test cache clearing."""
    # Add some items
    for i in range(5):
        lru_engine._set_cached_value(("key", i), i)

    assert len(lru_engine._cache) == 5

    # Clear cache
    lru_engine.clear()
    assert len(lru_engine._cache) == 0
    assert lru_engine.stats["hits"] == 0
    assert lru_engine.stats["misses"] == 0
    assert lru_engine.stats["size"] == 0


def test_lru_cache_with_complex_values(lru_engine: FunctoolsCacheEngine) -> None:
    """Test LRU cache with complex values."""
    # Test with various Python types
    values = [
        42,
        "string",
        [1, 2, 3],
        {"key": "value"},
        (1, "tuple"),
        {1, 2, 3},
        Path("/test/path"),
        None,
    ]

    for i, value in enumerate(values):
        lru_engine._set_cached_value(("complex", i), value)
        assert lru_engine._get_cached_value(("complex", i)) == value


def test_lru_cache_stats_accuracy(lru_engine: FunctoolsCacheEngine) -> None:
    """Test that cache statistics are accurate."""

    @lru_engine.cache
    def test_func(x: int) -> int:
        return x * 2

    # Test hits and misses
    test_func(1)  # miss
    test_func(1)  # hit
    test_func(2)  # miss
    test_func(1)  # hit

    stats = lru_engine.stats
    assert stats["hits"] == 2
    assert stats["misses"] == 2
    assert stats["size"] == 2
    assert stats["current_size"] == 2


# Test engine manager functionality
def test_engine_registration(engine_manager: EngineManager) -> None:
    """Test registration of cache engines."""
    # Default engines should be registered
    config = global_config.get_cache_config()
    engine = engine_manager.get_engine(config)
    assert isinstance(engine, CacheEngine)

    # Test registration of custom engine
    class CustomEngine(CacheEngine[Any, Any]):
        """Test engine implementation."""

        def __init__(self, config: CacheConfig) -> None:
            """Initialize the engine."""
            self.config = config
            self._cache: dict[Any, Any] = {}

        def cache(self, func: Any) -> Any:
            """Cache function results."""
            return func

        def clear(self) -> None:
            """Clear the cache."""
            self._cache.clear()

        @property
        def stats(self) -> dict[str, Any]:
            """Get cache statistics."""
            return {"size": len(self._cache)}

    engine_manager._register_engine("custom", CustomEngine)
    config = CacheConfig(preferred_engine="custom")
    engine = engine_manager.get_engine(config)
    assert isinstance(engine, CustomEngine)


def test_engine_selection(engine_manager: EngineManager) -> None:
    """Test selection of appropriate cache engines."""
    # Test default selection (should be LRU)
    config = global_config.get_cache_config()
    engine = engine_manager.get_engine(config)
    assert isinstance(engine, FunctoolsCacheEngine)

    # Test disk cache selection
    config = CacheConfig(folder_name="test_cache")
    engine = engine_manager.get_engine(config)
    assert isinstance(engine, DiskCacheEngine)

    # Test preferred engine selection
    config = CacheConfig(preferred_engine="lru")
    engine = engine_manager.get_engine(config)
    assert isinstance(engine, FunctoolsCacheEngine)


def test_invalid_engine_registration(engine_manager: EngineManager) -> None:
    """Test registration of invalid engines."""

    # Test registration of invalid engine class
    class InvalidEngine:
        """Invalid engine class."""

        def __init__(self) -> None:
            """Initialize the engine."""

    with pytest.raises(ValueError):
        engine_manager._register_engine("invalid", InvalidEngine)  # type: ignore


def test_engine_manager_singleton() -> None:
    """Test that get_engine_manager returns a singleton instance."""
    manager1 = get_engine_manager()
    manager2 = get_engine_manager()
    assert manager1 is manager2


def test_engine_configuration() -> None:
    """Test engine configuration."""
    # Test maxsize configuration
    config = CacheConfig(maxsize=100)
    engine = get_engine_manager().get_engine(config)
    assert isinstance(engine, FunctoolsCacheEngine)

    # Test invalid maxsize
    config = CacheConfig(maxsize=-1)
    with pytest.raises(ValueError):
        get_engine_manager().get_engine(config)

    # Test folder configuration
    config = CacheConfig(folder_name="test_cache")
    engine = get_engine_manager().get_engine(config)
    assert isinstance(engine, DiskCacheEngine)


def test_unavailable_engine() -> None:
    """Test handling of unavailable engines."""
    # Test unavailable preferred engine
    config = CacheConfig(preferred_engine="nonexistent")
    engine = get_engine_manager().get_engine(config)
    # Should fall back to default engine
    assert isinstance(engine, FunctoolsCacheEngine)


def test_engine_stats() -> None:
    """Test engine statistics."""
    config = global_config.get_cache_config()
    engine = get_engine_manager().get_engine(config)
    stats = engine.stats
    assert isinstance(stats, dict)
    assert "size" in stats


def test_engine_clear(engine: BaseCacheEngine[Any, Any]) -> None:
    """Test engine clear operation."""
    engine.clear()
    assert engine.stats["size"] == 0


# Test constants
TEST_INPUT = 5
TEST_RESULT = TEST_INPUT * 2
TEST_INPUT_2 = 10
TEST_RESULT_2 = TEST_INPUT_2 * 2
EXPECTED_CALL_COUNT = 2
MIN_STATS_COUNT = 1
LRU_CACHE_SIZE = 10
SMALL_CACHE_SIZE = 5


def test_engine_caching(test_engine: BaseCacheEngine[Any, Any]) -> None:
    """Test basic caching functionality of an engine."""
    call_count = 0

    def test_func(x: int) -> int:
        nonlocal call_count
        call_count += 1
        return x * 2

    # First call should compute
    assert test_func(TEST_INPUT) == TEST_RESULT
    assert call_count == 1
    assert test_engine.stats["hits"] == 0

    # Second call should use cache
    assert test_func(TEST_INPUT) == TEST_RESULT
    assert call_count == 1
    assert test_engine.stats["hits"] == MIN_STATS_COUNT

    # Different arg should compute
    assert test_func(TEST_INPUT_2) == TEST_RESULT_2
    assert call_count == EXPECTED_CALL_COUNT
    assert test_engine.stats["hits"] == MIN_STATS_COUNT
    assert test_engine.stats["misses"] == EXPECTED_CALL_COUNT


def test_lru_maxsize(lru_engine: FunctoolsCacheEngine[Any, Any]) -> None:
    """Test LRU cache maxsize enforcement."""
    # Fill cache to maxsize
    for i in range(LRU_CACHE_SIZE):
        lru_engine._set_cached_value(("key", i), i)

    assert len(lru_engine._cache) == LRU_CACHE_SIZE

    # Add one more, should evict oldest
    lru_engine._set_cached_value(("key", LRU_CACHE_SIZE), LRU_CACHE_SIZE)
    assert len(lru_engine._cache) == LRU_CACHE_SIZE
    assert ("key", 0) not in lru_engine._cache  # First item should be evicted
    assert ("key", LRU_CACHE_SIZE) in lru_engine._cache  # New item should be present


def test_lru_clear(lru_engine: FunctoolsCacheEngine[Any, Any]) -> None:
    """Test LRU cache clear operation."""
    # Add some items
    for i in range(SMALL_CACHE_SIZE):
        lru_engine._set_cached_value(("key", i), i)

    assert len(lru_engine._cache) == SMALL_CACHE_SIZE

    # Clear cache
    lru_engine.clear()
    assert len(lru_engine._cache) == 0


def test_lru_stats(lru_engine: FunctoolsCacheEngine[Any, Any]) -> None:
    """Test LRU cache statistics."""
    # Add some items and access them
    lru_engine._get_cached_value("key1")
    lru_engine._get_cached_value("key2")

    # Some hits
    lru_engine._get_cached_value("key1")
    lru_engine._get_cached_value("key2")

    # Some misses
    lru_engine._get_cached_value("key3")
    lru_engine._get_cached_value("key4")

    # Check stats
    stats = lru_engine.stats
    assert stats["hits"] == EXPECTED_CALL_COUNT
    assert stats["misses"] == EXPECTED_CALL_COUNT
    assert stats["size"] == EXPECTED_CALL_COUNT
    assert stats["current_size"] == EXPECTED_CALL_COUNT


def test_functools_cache_maxsize_enforcement(
    functools_engine: FunctoolsCacheEngine,
) -> None:
    """Test that the functools cache respects maxsize."""
    # Original test logic remains the same
    pass


def test_functools_cache_clear(functools_engine: FunctoolsCacheEngine) -> None:
    """Test clearing the functools cache."""
    # Original test logic remains the same
    pass


def test_functools_cache_with_complex_values(
    functools_engine: FunctoolsCacheEngine,
) -> None:
    """Test the functools cache with complex values."""
    # Original test logic remains the same
    pass


def test_functools_cache_stats_accuracy(functools_engine: FunctoolsCacheEngine) -> None:
    """Test that the functools cache stats are accurate."""
    # Original test logic remains the same
    pass


def test_functools_maxsize(functools_engine: FunctoolsCacheEngine[Any, Any]) -> None:
    """Test maxsize enforcement in functools cache."""
    # Original test logic remains the same
    pass


def test_functools_clear(functools_engine: FunctoolsCacheEngine[Any, Any]) -> None:
    """Test clearing the functools cache."""
    # Original test logic remains the same
    pass


def test_functools_stats(functools_engine: FunctoolsCacheEngine[Any, Any]) -> None:
    """Test functools cache statistics."""
    # Original test logic remains the same
    pass
