#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "pytest",
# ]
# ///
# this_file: tests/test_config.py

"""Tests for the configuration system."""

import pytest
from pydantic import ValidationError

from twat_cache.config import CacheConfig, create_cache_config
from tests.test_constants import (
    SMALL_CACHE_SIZE,
    DEFAULT_CACHE_SIZE,
    SHORT_TTL,
    DEFAULT_TTL,
)


def test_cache_config_defaults():
    """Test default configuration values."""
    config = CacheConfig()
    assert config.maxsize is None
    assert config.folder_name is None
    assert config.ttl is None
    assert config.compress is False
    assert config.secure is True
    assert config.policy == "lru"
    assert config.preferred_engine is None


def test_cache_config_validation():
    """Test configuration validation."""
    config = create_cache_config(
        maxsize=DEFAULT_CACHE_SIZE,
        ttl=DEFAULT_TTL,
    )
    assert config.maxsize == DEFAULT_CACHE_SIZE
    assert config.ttl == DEFAULT_TTL

    # Test invalid maxsize
    with pytest.raises((ValidationError, ValueError)):
        create_cache_config(maxsize=-1)

    # Test invalid TTL
    with pytest.raises((ValidationError, ValueError)):
        create_cache_config(ttl=-1)


def test_cache_config_size_limits():
    """Test cache size limit validation."""
    config = create_cache_config(maxsize=SMALL_CACHE_SIZE)
    assert config.maxsize == SMALL_CACHE_SIZE

    config = create_cache_config(maxsize=DEFAULT_CACHE_SIZE)
    assert config.maxsize == DEFAULT_CACHE_SIZE

    config = create_cache_config(maxsize=None)
    assert config.maxsize is None


def test_cache_config_ttl():
    """Test TTL validation and handling."""
    config = create_cache_config(ttl=SHORT_TTL)
    assert config.ttl == SHORT_TTL

    config = create_cache_config(ttl=DEFAULT_TTL)
    assert config.ttl == DEFAULT_TTL

    config = create_cache_config(ttl=None)
    assert config.ttl is None


def test_cache_config_policy():
    """Test eviction policy options."""
    for policy in ("lru", "lfu", "rr"):
        config = create_cache_config(policy=policy)
        assert config.policy == policy


def test_cache_config_compress_secure():
    """Test compress and secure flags."""
    config = create_cache_config(compress=True, secure=False)
    assert config.compress is True
    assert config.secure is False

    config = create_cache_config(compress=False, secure=True)
    assert config.compress is False
    assert config.secure is True


def test_cache_config_preferred_engine():
    """Test preferred_engine field."""
    config = create_cache_config(preferred_engine="functools")
    assert config.preferred_engine == "functools"

    config = create_cache_config(preferred_engine=None)
    assert config.preferred_engine is None
