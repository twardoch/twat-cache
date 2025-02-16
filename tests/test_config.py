#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "pytest",
#   "pydantic",
#   "pydantic-settings",
# ]
# ///
# this_file: tests/test_config.py

"""Tests for the configuration management system."""

import os
from pathlib import Path
from collections.abc import Generator

import pytest

from twat_cache.config import CacheConfig, GlobalConfig
from twat_cache.paths import get_cache_path

# Test constants
DEFAULT_MAXSIZE = 1000
DEFAULT_COMPRESSION_LEVEL = 6
CUSTOM_MAXSIZE = 500
CACHE_CONFIG_MAXSIZE = 200
CUSTOM_CACHE_MAXSIZE = 300


@pytest.fixture
def clean_env() -> Generator[None, None, None]:
    """Clean environment variables before and after tests."""
    # Store original environment
    original_env = dict(os.environ)

    # Clear relevant environment variables
    for key in list(os.environ.keys()):
        if key.startswith("TWAT_CACHE_"):
            del os.environ[key]

    yield

    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


def test_cache_config_validation() -> None:
    """Test validation of cache configuration."""
    # Valid configurations
    config = CacheConfig(maxsize=100)
    config.validate_maxsize()  # Should not raise

    config = CacheConfig(maxsize=None)
    config.validate_maxsize()  # Should not raise

    # Invalid configurations
    with pytest.raises(ValueError):
        config = CacheConfig(maxsize=-1)
        config.validate_maxsize()

    with pytest.raises(ValueError):
        config = CacheConfig(maxsize=0)
        config.validate_maxsize()


def test_default_config() -> None:
    """Test default configuration values."""
    config = GlobalConfig()

    # Check default values
    assert config.cache_dir == get_cache_path()
    assert config.default_maxsize == DEFAULT_MAXSIZE
    assert config.default_use_sql is False
    assert config.default_engine == "lru"
    assert config.enable_compression is True
    assert config.compression_level == DEFAULT_COMPRESSION_LEVEL
    assert config.debug is False
    assert config.log_file is None


def test_custom_config() -> None:
    """Test custom configuration values."""
    config = GlobalConfig(
        default_maxsize=CUSTOM_MAXSIZE,
        default_use_sql=True,
        default_engine="disk",
        enable_compression=False,
        debug=True,
        log_file="cache.log",
    )

    # Check values
    assert config.default_maxsize == CUSTOM_MAXSIZE
    assert config.default_use_sql is True
    assert config.default_engine == "disk"
    assert config.enable_compression is False
    assert config.debug is True
    assert config.log_file == "cache.log"


def test_global_config_env_vars(clean_env: None) -> None:
    """Test environment variable configuration."""
    # Set environment variables
    os.environ["TWAT_CACHE_DEFAULT_MAXSIZE"] = "500"
    os.environ["TWAT_CACHE_DEFAULT_USE_SQL"] = "true"
    os.environ["TWAT_CACHE_DEFAULT_ENGINE"] = "disk"
    os.environ["TWAT_CACHE_DEBUG"] = "true"

    # Create config with environment variables
    config = GlobalConfig()

    # Check values
    assert config.default_maxsize == 500
    assert config.default_use_sql is True
    assert config.default_engine == "disk"
    assert config.debug is True


def test_get_cache_config() -> None:
    """Test getting cache configuration with defaults."""
    global_config = GlobalConfig()

    # Test with no overrides
    cache_config = global_config.get_cache_config()
    assert cache_config.maxsize == global_config.default_maxsize
    assert cache_config.use_sql == global_config.default_use_sql
    assert cache_config.preferred_engine == global_config.default_engine

    # Test with partial overrides
    cache_config = global_config.get_cache_config(
        maxsize=200,
        folder_name="test_cache",
    )
    assert cache_config.maxsize == 200
    assert cache_config.folder_name == "test_cache"
    assert cache_config.use_sql == global_config.default_use_sql
    assert cache_config.preferred_engine == global_config.default_engine

    # Test with full overrides
    cache_config = global_config.get_cache_config(
        maxsize=300,
        folder_name="custom_cache",
        use_sql=True,
        preferred_engine="disk",
    )
    assert cache_config.maxsize == 300
    assert cache_config.folder_name == "custom_cache"
    assert cache_config.use_sql is True
    assert cache_config.preferred_engine == "disk"


def test_logging_configuration(tmp_path: Path) -> None:
    """Test logging configuration."""
    # Test debug logging
    config = GlobalConfig(debug=True)
    config.configure_logging()
    # Debug logging should be enabled (no easy way to test this directly)

    # Test file logging
    log_file = tmp_path / "cache.log"
    config = GlobalConfig(log_file=log_file)
    config.configure_logging()
    # Log file should be created when logging occurs

    assert not log_file.exists()  # File not created until first log

    # Clean up
    if log_file.exists():
        log_file.unlink()


def test_cache_config_creation() -> None:
    """Test cache configuration creation."""
    global_config = GlobalConfig()

    # Create cache config with some overrides
    cache_config = CacheConfig(
        maxsize=CACHE_CONFIG_MAXSIZE,
        folder_name="test_cache",
    )

    assert cache_config.maxsize == CACHE_CONFIG_MAXSIZE
    assert cache_config.folder_name == "test_cache"
    assert cache_config.use_sql == global_config.default_use_sql


def test_cache_config_with_sql() -> None:
    """Test cache configuration with SQL settings."""
    cache_config = CacheConfig(
        maxsize=CUSTOM_CACHE_MAXSIZE,
        folder_name="custom_cache",
        use_sql=True,
        preferred_engine="disk",
    )

    assert cache_config.maxsize == CUSTOM_CACHE_MAXSIZE
    assert cache_config.folder_name == "custom_cache"
    assert cache_config.use_sql is True
    assert cache_config.preferred_engine == "disk"
