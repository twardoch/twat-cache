#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "pytest",
# ]
# ///
# this_file: tests/test_config.py

"""Tests for the configuration management system."""

import pytest

from twat_cache.config import create_cache_config, CacheConfig


def test_cache_config_validation() -> None:
    """Test validation of cache configuration."""
    # Valid configurations
    config = create_cache_config(maxsize=100)
    config.validate()  # Should not raise

    config = create_cache_config(maxsize=None)
    config.validate()  # Should not raise

    # Invalid configurations
    with pytest.raises(ValueError):
        config = create_cache_config(maxsize=-1)
        config.validate()

    with pytest.raises(ValueError):
        config = create_cache_config(maxsize=0)
        config.validate()


def test_cache_config_creation() -> None:
    """Test creation of cache configuration."""
    # Test with minimal configuration
    config = create_cache_config()
    assert config.maxsize is None
    assert config.folder_name is None
    assert config.preferred_engine is None
    assert config.use_sql is False

    # Test with full configuration
    config = create_cache_config(
        maxsize=100,
        folder_name="test",
        preferred_engine="memory",
        use_sql=True,
    )
    assert config.maxsize == 100
    assert config.folder_name == "test"
    assert config.preferred_engine == "memory"
    assert config.use_sql is True


def test_cache_config_to_dict() -> None:
    """Test conversion of config to dictionary."""
    config = create_cache_config(
        maxsize=100,
        folder_name="test",
        preferred_engine="memory",
        use_sql=True,
    )
    data = config.to_dict()
    assert data["maxsize"] == 100
    assert data["folder_name"] == "test"
    assert data["preferred_engine"] == "memory"
    assert data["use_sql"] is True


def test_cache_config_from_dict() -> None:
    """Test creation of config from dictionary."""
    data = {
        "maxsize": 100,
        "folder_name": "test",
        "preferred_engine": "memory",
        "use_sql": True,
    }
    config = CacheConfig.from_dict(data)
    assert config.maxsize == 100
    assert config.folder_name == "test"
    assert config.preferred_engine == "memory"
    assert config.use_sql is True
