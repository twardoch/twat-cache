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
Cache engine manager.

This module provides a centralized manager for cache engines, handling
registration, selection, and instantiation of appropriate cache backends
based on configuration and availability.
"""

from typing import Any, cast, ClassVar
import os

from loguru import logger

from twat_cache.types import BackendType, CacheConfig, CacheEngine
from .base import BaseCacheEngine
from .functools import FunctoolsCacheEngine

# Try to import optional backends
try:
    from .aiocache import AioCacheEngine

    HAS_AIOCACHE = True
except ImportError:
    HAS_AIOCACHE = False
    logger.debug("aiocache not available")

try:
    from .diskcache import DiskCacheEngine

    HAS_DISKCACHE = True
except ImportError:
    HAS_DISKCACHE = False
    logger.debug("diskcache not available")

try:
    from .cachebox import CacheBoxEngine

    HAS_CACHEBOX = True
except ImportError:
    HAS_CACHEBOX = False
    logger.debug("cachebox not available")

try:
    from .cachetools import CacheToolsEngine

    HAS_CACHETOOLS = True
except ImportError:
    HAS_CACHETOOLS = False
    logger.debug("cachetools not available")

try:
    from .klepto import KleptoEngine

    HAS_KLEPTO = True
except ImportError:
    HAS_KLEPTO = False
    logger.debug("klepto not available")

try:
    from .joblib import JoblibEngine

    HAS_JOBLIB = True
except ImportError:
    HAS_JOBLIB = False
    logger.debug("joblib not available")


# Type alias for concrete cache engine class
EngineType = type[BaseCacheEngine[Any, Any]]


class EngineManager:
    """
    Singleton manager for cache engine selection and instantiation.

    This class manages the selection and instantiation of cache engines based on
    configuration and availability. It ensures only one instance exists.
    """

    _instance: ClassVar["EngineManager | None"] = None

    def __new__(cls) -> "EngineManager":
        """Create or return the singleton instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Initialize the engine manager."""
        if not hasattr(self, "_initialized"):
            self._engines: dict[str, type[CacheEngine[Any, Any]]] = {}
            self._register_available_engines()
            self._initialized = True

    def _register_available_engines(self) -> None:
        """Register all available cache engines."""
        # Always register memory cache
        self._register_engine("memory", FunctoolsCacheEngine)

        # Register optional engines
        if HAS_CACHEBOX:
            self._register_engine("cachebox", CacheBoxEngine)
        if HAS_CACHETOOLS:
            self._register_engine("cachetools", CacheToolsEngine)
        if HAS_AIOCACHE:
            self._register_engine("aiocache", AioCacheEngine)
        if HAS_KLEPTO:
            self._register_engine("klepto", KleptoEngine)
        if HAS_DISKCACHE:
            self._register_engine("diskcache", DiskCacheEngine)
        if HAS_JOBLIB:
            self._register_engine("joblib", JoblibEngine)

        logger.debug(
            "Registered cache engines: {}",
            list(self._engines.keys()),
        )

    def _register_engine(self, name: str, engine_cls: type[Any]) -> None:
        """
        Register a cache engine.

        Args:
            name: Name of the engine
            engine_cls: Engine class to register

        Raises:
            ValueError: If engine is invalid
        """
        if not issubclass(engine_cls, BaseCacheEngine):
            msg = (
                f"Invalid engine class {engine_cls.__name__}, "
                "must be a subclass of BaseCacheEngine"
            )
            raise ValueError(msg)

        self._engines[name] = cast(EngineType, engine_cls)
        logger.debug("Registered cache engine: {}", name)

    def _validate_config(self, config: CacheConfig) -> None:
        """
        Validate the cache configuration.

        Args:
            config: Cache configuration to validate

        Raises:
            ValueError: If configuration is invalid
        """
        if config.maxsize is not None and config.maxsize <= 0:
            msg = "maxsize must be positive if specified"
            raise ValueError(msg)

    def _try_preferred_engine(
        self, config: CacheConfig
    ) -> CacheEngine[Any, Any] | None:
        """
        Try to create the preferred engine instance.

        Args:
            config: Cache configuration

        Returns:
            The preferred engine instance if available, None otherwise
        """
        if config.preferred_engine:
            engine_cls = self._engines.get(config.preferred_engine)
            if engine_cls:
                logger.debug("Using preferred engine: {}", config.preferred_engine)
                return engine_cls(config)
            logger.warning(
                "Preferred engine {} not available",
                config.preferred_engine,
            )
        return None

    def _try_redis_engine(self, config: CacheConfig) -> CacheEngine[Any, Any] | None:
        """
        Try to create a Redis engine instance if conditions are met.

        Args:
            config: Cache configuration

        Returns:
            A Redis engine instance if available and requested, None otherwise
        """
        if HAS_AIOCACHE and os.environ.get("TWAT_CACHE_USE_REDIS") == "1":
            logger.debug("Using Redis cache via aiocache")
            return self._engines["aiocache"](config)
        return None

    def _try_sql_engine(self, config: CacheConfig) -> CacheEngine[Any, Any] | None:
        """
        Try to create an SQL engine instance if conditions are met.

        Args:
            config: Cache configuration

        Returns:
            An SQL engine instance if requested, None otherwise
        """
        if config.use_sql and HAS_DISKCACHE:
            logger.debug("Using SQL-based disk cache")
            return self._engines["diskcache"](config)
        return None

    def _create_fallback_engine(self, config: CacheConfig) -> CacheEngine[Any, Any]:
        """
        Create a fallback engine instance.

        Args:
            config: Cache configuration

        Returns:
            A fallback engine instance (LRU by default)
        """
        logger.debug("Using LRU cache")
        return self._engines["memory"](config)

    def get_engine(self, config: CacheConfig) -> CacheEngine[Any, Any]:
        """
        Get an appropriate cache engine based on configuration.

        Args:
            config: Cache configuration object

        Returns:
            An instance of the appropriate cache engine

        Raises:
            ValueError: If configuration is invalid
        """
        self._validate_config(config)

        # Try engines in priority order
        engine = (
            self._try_preferred_engine(config)
            or self._try_redis_engine(config)
            or self._try_sql_engine(config)
            or self._create_fallback_engine(config)
        )

        return engine

    def _get_prioritized_engines(self) -> list[BackendType]:
        """Get list of engine types in priority order."""
        return [
            "cachebox",  # Fastest (Rust-based)
            "cachetools",  # Flexible in-memory
            "aiocache",  # Async support
            "klepto",  # Scientific computing
            "diskcache",  # SQL-based disk cache
            "joblib",  # Array caching
            "memory",  # Always available
        ]

    @property
    def available_engines(self) -> list[BackendType]:
        """Get list of available engine types."""
        return cast(list[BackendType], list(self._engines.keys()))


def get_engine_manager() -> EngineManager:
    """
    Get the global engine manager instance.

    Returns:
        The global engine manager instance
    """
    return EngineManager()
