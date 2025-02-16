#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "pytest",
# ]
# ///
# this_file: tests/test_config.py

"""Tests for cache configuration."""

import pytest

from twat_cache.config import create_cache_config, CacheConfig
from twat_cache.test_constants import (
    CACHE_SIZE,
    CACHE_TTL,
    TEST_KEY,
    TEST_BOOL,
    TEST_INT,
)


def test_config_creation() -> None:
    """Test cache configuration creation."""
    # Test with minimal settings
    config = create_cache_config()
    assert config.maxsize is None
    assert config.ttl is None
    assert config.folder_name is None

    # Test with all settings
    config = create_cache_config(
        maxsize=CACHE_SIZE,
        folder_name=TEST_KEY,
        preferred_engine="memory",
        ttl=CACHE_TTL,
        use_sql=True,
    )
    assert config.maxsize == CACHE_SIZE
    assert config.folder_name == TEST_KEY
    assert config.preferred_engine == "memory"
    assert config.ttl == CACHE_TTL
    assert config.use_sql is True


def test_config_validation() -> None:
    """Test configuration validation."""
    # Test invalid maxsize
    with pytest.raises(ValueError):
        create_cache_config(maxsize=-1)

    # Test invalid ttl
    with pytest.raises(ValueError):
        create_cache_config(ttl=-1)

    # Test valid eviction policies
    policies = ["lru", "lfu", "fifo", "rr", "ttl"]
    for policy in policies:
        config = create_cache_config(policy=policy)
        assert config.policy == policy


def test_config_serialization() -> None:
    """Test configuration serialization."""
    # Create a config
    config = create_cache_config(
        maxsize=CACHE_SIZE,
        folder_name=TEST_KEY,
        preferred_engine="memory",
        ttl=CACHE_TTL,
        use_sql=True,
    )

    # Convert to dict
    data = config.to_dict()
    assert data["maxsize"] == CACHE_SIZE
    assert data["folder_name"] == TEST_KEY
    assert data["preferred_engine"] == "memory"
    assert data["ttl"] == CACHE_TTL
    assert data["use_sql"] is True

    # Create from dict
    data = {
        "maxsize": CACHE_SIZE,
        "folder_name": TEST_KEY,
        "preferred_engine": "memory",
        "ttl": CACHE_TTL,
        "use_sql": True,
    }
    config = CacheConfig.from_dict(data)
    assert config.maxsize == CACHE_SIZE
    assert config.folder_name == TEST_KEY
    assert config.preferred_engine == "memory"
    assert config.ttl == CACHE_TTL
    assert config.use_sql is True
