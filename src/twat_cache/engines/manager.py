#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "loguru",
#   "aiocache",
#   "diskcache",
# ]
# ///
# this_file: src/twat_cache/engines/manager.py

"""
Cache engine manager module.

This module provides the CacheEngineManager class which handles registration,
selection and management of cache engine implementations.
"""

from typing import Any, TypeVar, cast

from loguru import logger

from twat_cache.type_defs import (
    CacheConfig,
)
# Import engine classes directly for registration
from .aiocache import AioCacheEngine
from .base import BaseCacheEngine
from .cachebox import CacheBoxEngine
from .cachetools import CacheToolsEngine
from .diskcache import DiskCacheEngine
from .functools_engine import FunctoolsCacheEngine # Corrected import to functools_engine.py
from .joblib import JoblibEngine
from .klepto import KleptoEngine
# RedisEngine and HAS_REDIS related imports removed.

# Type variable for concrete cache engine
E = TypeVar("E", bound=BaseCacheEngine[Any, Any])


class CacheEngineManager:
    """Manages cache engine implementations and handles engine selection and instantiation."""

    def __init__(self) -> None:
        """Initialize the cache engine manager."""
        self._engines: dict[str, type[BaseCacheEngine[Any, Any]]] = {}
        self._register_builtin_engines()

    def _register_builtin_engines(self) -> None:
        """Register built-in cache engine implementations."""
        # MVP Focus: functools, diskcache, aiocache
        self.register_engine("functools", FunctoolsCacheEngine)
        self.register_engine("diskcache", DiskCacheEngine)
        self.register_engine("aiocache", AioCacheEngine)

        # Non-MVP engines, still registered if available but not primary focus
        self.register_engine("cachetools", CacheToolsEngine)
        self.register_engine("klepto", KleptoEngine)
        self.register_engine("joblib", JoblibEngine)
        self.register_engine("cachebox", CacheBoxEngine)

        # HAS_REDIS and RedisCacheEngine registration block removed.

    def register_engine(self, name: str, engine_cls: type[BaseCacheEngine[Any, Any]]) -> None:
        """
        Register a new cache engine implementation.

        Args:
            name: Unique name for the engine
            engine_cls: Cache engine class to register
        """
        if name in self._engines:
            logger.warning(f"Overwriting existing engine registration for {name}")
        self._engines[name] = engine_cls # No cast needed due to type hint on engine_cls

    def get_engine_class(self, name: str) -> type[BaseCacheEngine[Any, Any]] | None:
        """
        Get a registered cache engine class by name.

        Args:
            name: Name of the engine to retrieve

        Returns:
            The cache engine class if found, None otherwise
        """
        return self._engines.get(name)

    def list_available_engines(self) -> list[str]:
        """
        Get a list of registered and available (importable) engine names.

        Returns:
            List of registered engine names
        """
        return [name for name, engine_cls in self._engines.items() if engine_cls.is_available()]

    def create_engine_instance(
        self,
        config: CacheConfig,
    ) -> BaseCacheEngine[Any, Any] | None:
        """
        Selects and instantiates an appropriate cache engine based on configuration.

        Priority for selection:
        1. `config.preferred_engine` if specified and available.
        2. Default to "functools" engine if no preference or preferred is unavailable.

        Args:
            config: Cache configuration object.

        Returns:
            An instantiated cache engine (BaseCacheEngine instance) or None if no suitable
            engine can be created.
        """
        available_engines = self.list_available_engines()

        if not available_engines:
            logger.warning("No cache engines are available in the system.")
            return None

        selected_engine_name: str | None = None
        engine_cls_to_instantiate: type[BaseCacheEngine[Any, Any]] | None = None

        # 1. Try config.preferred_engine
        if config.preferred_engine:
            if config.preferred_engine in available_engines:
                selected_engine_name = config.preferred_engine
                engine_cls_to_instantiate = self.get_engine_class(selected_engine_name)
            else:
                logger.warning(
                    f"Preferred engine '{config.preferred_engine}' is not available. "
                    f"Available engines: {available_engines}. Falling back."
                )

        # 2. Fallback to "functools" if no suitable engine found yet
        if not engine_cls_to_instantiate:
            if "functools" in available_engines:
                selected_engine_name = "functools"
                engine_cls_to_instantiate = self.get_engine_class(selected_engine_name)
                if config.preferred_engine: # Log if we fell back from a specific preference
                    logger.info(f"Using 'functools' engine as fallback for '{config.preferred_engine}'.")
                else:
                    logger.info("Using 'functools' engine as default.")
            else:
                # This case should be rare, as functools is always available.
                logger.error(
                    "'functools' engine is not available, and no other engine could be selected."
                )
                return None

        if engine_cls_to_instantiate:
            try:
                logger.debug(f"Instantiating '{selected_engine_name}' engine with config: {config.to_dict()}")
                return engine_cls_to_instantiate(config)
            except Exception as e:
                logger.error(
                    f"Failed to instantiate engine '{selected_engine_name}' with config {config.to_dict()}: {e}",
                    exc_info=True
                )
                return None

        logger.error("Could not select or instantiate any cache engine.")
        return None

# Singleton instance of the engine manager
_engine_manager_instance: CacheEngineManager | None = None

def get_engine_manager() -> CacheEngineManager:
    """
    Get the global singleton CacheEngineManager instance.

    Returns:
        The global CacheEngineManager instance.
    """
    global _engine_manager_instance
    if _engine_manager_instance is None:
        _engine_manager_instance = CacheEngineManager()
    return _engine_manager_instance
