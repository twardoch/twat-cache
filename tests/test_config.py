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
from loguru import logger

from twat_cache.config import create_cache_config, GlobalConfig
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


def test_default_config() -> None:
    """Test default configuration values."""
    config = GlobalConfig()

    # Check default values
    assert config.cache_dir == get_cache_path("global")
    assert config.default_maxsize == 1000
    assert not config.default_use_sql
    assert config.default_engine == "lru"
    assert config.default_cache_type is None
    assert config.enable_compression
    assert config.compression_level == 6
    assert not config.debug
    assert config.log_file is None


def test_custom_config() -> None:
    """Test custom configuration values."""
    config = GlobalConfig(
        default_maxsize=CUSTOM_MAXSIZE,
        default_use_sql=True,
        default_engine="disk",
        enable_compression=False,
        debug=True,
        log_file=Path("cache.log"),
    )

    # Check values
    assert config.default_maxsize == CUSTOM_MAXSIZE
    assert config.default_use_sql is True
    assert config.default_engine == "disk"
    assert config.enable_compression is False
    assert config.debug is True
    assert config.log_file == Path("cache.log")


def test_global_config_env_vars(clean_env: None) -> None:
    """Test environment variable configuration."""
    # Set environment variables
    os.environ["TWAT_CACHE_DEFAULT_MAXSIZE"] = str(CUSTOM_MAXSIZE)
    os.environ["TWAT_CACHE_DEFAULT_USE_SQL"] = "true"
    os.environ["TWAT_CACHE_DEFAULT_ENGINE"] = "disk"
    os.environ["TWAT_CACHE_ENABLE_COMPRESSION"] = "false"
    os.environ["TWAT_CACHE_DEBUG"] = "true"

    config = GlobalConfig()

    # Check values
    assert config.default_maxsize == CUSTOM_MAXSIZE
    assert config.default_use_sql is True
    assert config.default_engine == "disk"
    assert config.enable_compression is False
    assert config.debug is True


def test_get_cache_config() -> None:
    """Test cache configuration creation from global config."""
    global_config = GlobalConfig(
        default_maxsize=DEFAULT_MAXSIZE,
        default_use_sql=False,
        default_engine="lru",
    )

    # Test default configuration
    cache_config = global_config.get_cache_config()
    assert cache_config.get_maxsize() == DEFAULT_MAXSIZE
    assert cache_config.get_use_sql() is False
    assert cache_config.get_preferred_engine() == "lru"

    # Test with overrides
    cache_config = global_config.get_cache_config(
        maxsize=CUSTOM_CACHE_MAXSIZE,
        use_sql=True,
        preferred_engine="disk",
    )
    assert cache_config.get_maxsize() == CUSTOM_CACHE_MAXSIZE
    assert cache_config.get_use_sql() is True
    assert cache_config.get_preferred_engine() == "disk"


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
    logger.info("Test log message")  # Trigger log file creation
    assert log_file.exists()  # File should exist now
    assert log_file.read_text().strip().endswith("Test log message")


def test_cache_config_creation() -> None:
    """Test creation of cache configuration."""
    # Test with minimal configuration
    config = create_cache_config()
    assert config.get_maxsize() is None
    assert config.get_folder_name() is None
    assert config.get_use_sql() is False
    assert config.get_preferred_engine() is None
    assert config.get_cache_type() is None

    # Test with full configuration
    config = create_cache_config(
        maxsize=100,
        folder_name="test",
        use_sql=True,
        preferred_engine="disk",
        cache_type="speed",
    )
    assert config.get_maxsize() == 100
    assert config.get_folder_name() == "test"
    assert config.get_use_sql() is True
    assert config.get_preferred_engine() == "disk"
    assert config.get_cache_type() == "speed"


def test_cache_config_with_sql() -> None:
    """Test SQL-specific configuration."""
    # Test SQL configuration
    config = create_cache_config(use_sql=True, folder_name="test_db")
    assert config.get_use_sql() is True
    assert config.get_folder_name() == "test_db"

    # Test validation with SQL configuration
    config.validate()  # Should not raise
