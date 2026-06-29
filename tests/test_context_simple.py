#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "pytest",
#   "loguru",
# ]
# ///
# this_file: tests/test_context_simple.py

"""Simple test suite for twat_cache context management."""

import pytest
from unittest.mock import patch, MagicMock

# Import context directly
from twat_cache.context import CacheContext
from twat_cache.config import CacheConfig


def test_cache_context_init():
    """Test that CacheContext can be initialized."""
    # Create a mock config
    config = CacheConfig(maxsize=100)

    # Initialize the context with engine_name
    context = CacheContext(config=config, engine_name="memory")

    # Check that the config was set correctly
    assert context.config == config
    assert context.engine_name == "memory"


@patch("twat_cache.context.get_engine_manager")
def test_cache_context_enter_exit(mock_get_engine_manager):
    """Test that CacheContext can be used as a context manager."""
    # create_engine_instance returns an engine instance directly
    mock_manager = MagicMock()
    mock_engine = MagicMock()
    mock_manager.create_engine_instance.return_value = mock_engine
    mock_get_engine_manager.return_value = mock_manager

    config = CacheConfig(maxsize=100)

    with CacheContext(config=config) as engine:
        assert engine == mock_engine

    mock_engine.cleanup.assert_called_once()


@patch("twat_cache.context.get_engine_manager")
def test_cache_context_error_handling(mock_get_engine_manager):
    """Test that CacheContext handles errors correctly."""
    mock_manager = MagicMock()
    mock_engine = MagicMock()
    mock_engine.cleanup.side_effect = Exception("Test exception")
    mock_manager.create_engine_instance.return_value = mock_engine
    mock_get_engine_manager.return_value = mock_manager

    config = CacheConfig(maxsize=100)

    # cleanup exception should be swallowed internally
    with CacheContext(config=config) as engine:
        assert engine == mock_engine

    mock_engine.cleanup.assert_called_once()


if __name__ == "__main__":
    pytest.main(["-v", __file__])
