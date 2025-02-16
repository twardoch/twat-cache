#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "pytest",
#   "loguru",
#   "redis",
#   "msgpack",
#   "fakeredis",
# ]
# ///
# this_file: tests/test_redis_cache.py

"""Test suite for Redis cache engine."""

import os
import time
from typing import Any, Callable
from collections.abc import Generator

import pytest
from fakeredis import FakeRedis, FakeServer
import redis

from twat_cache.config import CacheConfig
from twat_cache.engines.redis import RedisCacheEngine, RedisConnectionManager

# Test constants
DEFAULT_PORT = 6379
DEFAULT_TTL = 60
TEST_INPUT = 5
TEST_RESULT = TEST_INPUT * TEST_INPUT
TEST_INPUT_2 = 6
TEST_RESULT_2 = TEST_INPUT_2 * TEST_INPUT_2
EXPECTED_CALL_COUNT = 2
MIN_STATS_COUNT = 2
TEST_LIST_SUM = 15
TEST_LIST_LEN = 5


@pytest.fixture
def fake_redis() -> Generator[FakeServer, None, None]:
    """Provide a fake Redis server."""
    server = FakeServer()
    yield server
    server.connected = False


@pytest.fixture
def redis_cache(
    fake_redis: FakeServer,
) -> Generator[RedisCacheEngine[Any, Any], None, None]:
    """Provide a Redis cache engine instance with fake Redis."""
    # Set environment variables for Redis configuration
    os.environ["TWAT_CACHE_REDIS_HOST"] = "localhost"
    os.environ["TWAT_CACHE_REDIS_PORT"] = "6379"
    os.environ["TWAT_CACHE_REDIS_DB"] = "0"
    os.environ["TWAT_CACHE_REDIS_TTL"] = "60"  # 1 minute for testing

    # Create cache engine
    config = CacheConfig(
        folder_name="redis_test",
        maxsize=100,
    )

    # Patch Redis client creation
    def fake_redis_factory(*args: Any, **kwargs: Any) -> FakeRedis:
        return FakeRedis(server=fake_redis)

    RedisCacheEngine._create_client = fake_redis_factory  # type: ignore

    engine = RedisCacheEngine(config)
    yield engine

    # Clean up
    engine.clear()
    RedisConnectionManager.clear_pools()


def test_redis_init(redis_cache: RedisCacheEngine[Any, Any]) -> None:
    """Test Redis cache initialization."""
    assert redis_cache.host == "localhost"
    assert redis_cache.port == DEFAULT_PORT
    assert redis_cache.db == 0
    assert redis_cache.ttl == DEFAULT_TTL


def test_redis_caching(redis_cache: RedisCacheEngine[Any, Any]) -> None:
    """Test basic Redis caching."""
    call_count = 0

    def test_func(x: int) -> int:
        nonlocal call_count
        call_count += 1
        return x * x

    cached_func = redis_cache.cache(test_func)

    # First call should compute
    assert cached_func(TEST_INPUT) == TEST_RESULT
    assert call_count == 1

    # Second call should use cache
    assert cached_func(TEST_INPUT) == TEST_RESULT
    assert call_count == 1

    # Different input should compute
    assert cached_func(TEST_INPUT_2) == TEST_RESULT_2
    assert call_count == EXPECTED_CALL_COUNT


def test_redis_ttl(
    redis_cache: RedisCacheEngine[Any, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test Redis cache TTL functionality."""
    call_count = 0
    time_value = [0]  # Use a list to allow modification in nested scope

    def mock_time() -> float:
        return time_value[0]

    monkeypatch.setattr("time.time", mock_time)

    def test_func(x: int) -> int:
        nonlocal call_count
        call_count += 1
        return x * x

    cached_func = redis_cache.cache(test_func)

    # First call
    assert cached_func(TEST_INPUT) == TEST_RESULT
    assert call_count == 1

    # Second call (within TTL)
    assert cached_func(TEST_INPUT) == TEST_RESULT
    assert call_count == 1

    # Advance time past TTL
    time_value[0] = DEFAULT_TTL + 1

    # Call after TTL expiration
    assert cached_func(TEST_INPUT) == TEST_RESULT
    assert call_count == EXPECTED_CALL_COUNT


def test_redis_complex_data(redis_cache: RedisCacheEngine[Any, Any]) -> None:
    """Test Redis cache with complex data structures."""
    call_count = 0

    def process_list(data: list[int]) -> dict[str, int]:
        nonlocal call_count
        call_count += 1
        return {"sum": sum(data), "len": len(data)}

    cached_func = redis_cache.cache(process_list)

    test_list = [1, 2, 3, 4, 5]

    # First call
    result1 = cached_func(test_list)

    # Second call should use cache
    result2 = cached_func(test_list)

    assert result1 == result2
    assert result1["sum"] == TEST_LIST_SUM
    assert result1["len"] == TEST_LIST_LEN


def test_redis_stats(redis_cache: RedisCacheEngine[Any, Any]) -> None:
    """Test Redis cache statistics."""
    call_count = 0

    def test_func(x: int, multiplier: int = 1) -> int:
        nonlocal call_count
        call_count += 1
        return x * multiplier

    cached_func = redis_cache.cache(test_func)

    # Generate some cache activity
    cached_func(TEST_INPUT)
    cached_func(TEST_INPUT)  # Hit
    cached_func(TEST_INPUT_2)
    cached_func(TEST_INPUT_2)  # Hit

    # Check stats
    stats = redis_cache.stats
    assert stats["hits"] >= MIN_STATS_COUNT
    assert stats["misses"] >= MIN_STATS_COUNT
    assert stats["size"] == EXPECTED_CALL_COUNT


def test_redis_key_generation(redis_cache: RedisCacheEngine[Any, Any]) -> None:
    """Test Redis cache key generation."""
    call_count = 0

    def test_func(x: int, multiplier: int = 1) -> int:
        nonlocal call_count
        call_count += 1
        return x * multiplier

    cached_func = redis_cache.cache(test_func)

    # Different args should have different keys
    cached_func(TEST_INPUT)
    cached_func(TEST_INPUT_2)
    assert redis_cache.stats["size"] == EXPECTED_CALL_COUNT

    # Different kwargs should have different keys
    cached_func(TEST_INPUT, multiplier=2)
    assert redis_cache.stats["size"] == 3

    # Same args and kwargs should use same key
    cached_func(TEST_INPUT, multiplier=2)
    assert redis_cache.stats["size"] == 3


def test_redis_error_handling(
    redis_cache: RedisCacheEngine[Any, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test Redis cache error handling."""
    call_count = 0

    def test_func(x: int) -> int:
        nonlocal call_count
        call_count += 1
        return x * x

    cached_func = redis_cache.cache(test_func)

    # First call (normal operation)
    assert cached_func(TEST_INPUT) == TEST_RESULT
    assert call_count == 1

    # Simulate Redis error
    def mock_get(*args: Any, **kwargs: Any) -> None:
        raise redis.RedisError("Test error")

    monkeypatch.setattr(redis_cache._redis, "get", mock_get)

    # Call should still work (fallback to computing)
    assert cached_func(TEST_INPUT) == TEST_RESULT
    assert call_count == EXPECTED_CALL_COUNT


def test_redis_cache_clear(redis_cache: RedisCacheEngine[Any, Any]) -> None:
    """Test cache clearing."""

    def test_func(x: int) -> int:
        return x * x

    # Fill cache
    for i in range(10):
        test_func(i)

    # Check that cache has entries
    assert redis_cache.stats["size"] > 0

    # Clear cache
    redis_cache.clear()

    # Check that cache is empty
    assert redis_cache.stats["size"] == 0


def test_redis_cache_exceptions(redis_cache: RedisCacheEngine[Any, Any]) -> None:
    """Test caching of exceptions."""
    call_count = 0

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


def test_redis_connection_failure(redis_cache: RedisCacheEngine[Any, Any]) -> None:
    """Test handling of Redis connection failures."""
    call_count = 0

    def test_func(x: int) -> int:
        nonlocal call_count
        call_count += 1
        return x * x

    # First call (normal operation)
    assert test_func(5) == 25
    assert call_count == 1

    # Simulate Redis failure
    redis_cache._redis.connection_pool.disconnect()  # type: ignore

    # Call should still work (fallback to computing)
    assert test_func(5) == 25
    assert call_count == 2
