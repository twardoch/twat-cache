#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "loguru",
# ]
# ///
# this_file: src/twat_cache/context.py

"""
Context management utilities for twat_cache.

This module provides context managers for proper resource management
with different cache engines, ensuring that resources are cleaned up
properly when no longer needed.
"""

import contextlib
from typing import Any, TypeVar
from collections.abc import Generator

from loguru import logger

from twat_cache.config import CacheConfig, create_cache_config
from twat_cache.exceptions import EngineError
from twat_cache.engines.base import BaseCacheEngine
from twat_cache.engines.manager import get_engine_manager


# Type variable for engines
E = TypeVar("E", bound=BaseCacheEngine[Any, Any])


@contextlib.contextmanager
def engine_context(
    config: CacheConfig | None = None,
    engine_name: str | None = None,
    **kwargs: Any,
) -> Generator[BaseCacheEngine[Any, Any], None, None]:
    """
    Create a context manager for a cache engine.

    This context manager ensures that cache resources are properly cleaned up
    when the context is exited, even if an exception occurs.

    Args:
        config: Optional cache configuration to use.
        engine_name: Optional name of the specific engine to use.
        **kwargs: Additional configuration parameters if config is not provided.

    Yields:
        A cache engine instance.

    Raises:
        EngineError: If the requested engine is not available.
    """
    # Use provided config or create one from kwargs
    engine_config = config or create_cache_config(**kwargs)

    # Get the engine manager
    manager = get_engine_manager()

    # If a specific engine_name is given, set it as the preferred_engine in the config
    if engine_name:
        # We need to ensure engine_config is mutable here or create a new one
        # Pydantic models are immutable by default after creation unless configured otherwise.
        # Let's create a new config dictionary and update it.
        config_dict = engine_config.to_dict()
        config_dict['preferred_engine'] = engine_name
        final_engine_config = CacheConfig.from_dict(config_dict)
    else:
        final_engine_config = engine_config

    engine = manager.create_engine_instance(final_engine_config)

    if engine is None:
        logger.error(
            f"Failed to create engine. Engine name: {engine_name}, "
            f"Config preferred: {engine_config.preferred_engine}"
        )
        msg = "No suitable engine could be created for the given configuration"
        raise EngineError(msg)

    logger.debug(f"Created engine {engine.__class__.__name__} via engine_context")

    try:
        # Yield the engine for use in the context
        yield engine
    finally:
        # Always ensure cleanup happens
        try:
            logger.debug(f"Cleaning up engine {engine.__class__.__name__}")
            engine.cleanup()
        except Exception as e:
            logger.error(f"Error during engine cleanup: {e}")


class CacheContext:
    """
    A context manager class for cache operations.

    This class provides a reusable context manager for working with
    cache engines, with proper initialization and cleanup.
    """

    def __init__(
        self,
        config: CacheConfig | None = None,
        engine_name: str | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the cache context.

        Args:
            config: Optional cache configuration to use
            engine_name: Optional name of the specific engine to use
            **kwargs: Additional configuration parameters if config is not provided
        """
        self.config = config or create_cache_config(**kwargs)
        self.engine_name = engine_name
        self.engine: BaseCacheEngine[Any, Any] | None = None

    def __enter__(self) -> BaseCacheEngine[Any, Any]:
        """Enter the context and initialize the engine."""
        # Get the engine manager
        manager = get_engine_manager()

        current_config = self.config
        if self.engine_name:
            config_dict = self.config.to_dict()
            config_dict['preferred_engine'] = self.engine_name
            current_config = CacheConfig.from_dict(config_dict)

        self.engine = manager.create_engine_instance(current_config)

        if self.engine is None:
            logger.error(
                f"Failed to create engine in CacheContext. Engine name: {self.engine_name}, "
                f"Config preferred: {self.config.preferred_engine}"
            )
            msg = "No suitable engine could be created for the given configuration in CacheContext"
            raise EngineError(msg)

        logger.debug(f"Created engine {self.engine.__class__.__name__} via CacheContext")
        return self.engine

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit the context and clean up resources."""
        if self.engine:
            try:
                logger.debug(f"Cleaning up engine {self.engine.__class__.__name__}")
                self.engine.cleanup()
            except Exception as e:
                logger.error(f"Error during engine cleanup: {e}")
            finally:
                self.engine = None


def get_or_create_engine(
    config: CacheConfig | None = None,
    engine_name: str | None = None,
    **kwargs: Any,
) -> BaseCacheEngine[Any, Any]:
    """
    Get or create a cache engine instance.

    Note: The caller is responsible for calling cleanup() on the returned engine
    when it is no longer needed. For automatic cleanup, use engine_context or
    CacheContext instead.

    Args:
        config: Optional cache configuration to use
        engine_name: Optional name of the specific engine to use
        **kwargs: Additional configuration parameters if config is not provided

    Returns:
        A cache engine instance

    Raises:
        EngineError: If the requested engine is not available
    """
    # Use provided config or create one from kwargs
    engine_config = config or create_cache_config(**kwargs)

    # Get the engine manager
    manager = get_engine_manager()

    # If a specific engine_name is given, set it as the preferred_engine in the config
    if engine_name:
        config_dict = engine_config.to_dict()
        config_dict['preferred_engine'] = engine_name
        final_engine_config = CacheConfig.from_dict(config_dict)
    else:
        final_engine_config = engine_config

    engine = manager.create_engine_instance(final_engine_config)

    if engine is None:
        logger.error(
            f"Failed to create engine in get_or_create_engine. Engine name: {engine_name}, "
            f"Config preferred: {engine_config.preferred_engine}"
        )
        msg = "No suitable engine could be created for the given configuration in get_or_create_engine"
        raise EngineError(msg)

    logger.debug(f"Created engine {engine.__class__.__name__} via get_or_create_engine")
    return engine
