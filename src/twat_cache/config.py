#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "loguru",
#   "pydantic",
#   "pydantic-settings",
# ]
# ///
# this_file: src/twat_cache/config.py

"""
Configuration management for twat-cache.

This module provides configuration management for the caching system,
supporting both global settings and per-cache configuration.
"""

from pathlib import Path
from typing import Literal

from loguru import logger
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

from .paths import get_cache_dir
from .types import CacheConfig as CacheConfigProtocol


CacheType = Literal["speed", "database", "filesystem"]


class CacheConfig(BaseModel):
    """
    Cache configuration model.

    This class implements the CacheConfig protocol and provides validation
    for cache configuration settings.
    """

    maxsize: int | None = Field(
        default=None,
        description="Maximum number of items to store in the cache",
    )
    folder_name: str | None = Field(
        default=None,
        description="Name of the folder to store cache files in",
    )
    use_sql: bool = Field(
        default=False,
        description="Whether to use SQL-based storage",
    )
    preferred_engine: str | None = Field(
        default=None,
        description="Preferred cache engine to use",
    )
    cache_type: CacheType | None = Field(
        default=None,
        description="Type of cache to use (speed, database, filesystem)",
    )

    def validate(self) -> None:
        """
        Validate the configuration settings.

        Raises:
            ValueError: If any settings are invalid
        """
        if self.maxsize is not None and self.maxsize <= 0:
            msg = "maxsize must be positive if specified"
            raise ValueError(msg)


class GlobalConfig(BaseSettings):
    """
    Global configuration settings.

    This class manages global settings for the caching system, including
    defaults and environment variable configuration.
    """

    # Cache directory settings
    cache_dir: Path = Field(
        default_factory=get_cache_dir,
        description="Base directory for cache storage",
    )

    # Default cache settings
    default_maxsize: int = Field(
        default=1000,
        description="Default maximum cache size",
        env="TWAT_CACHE_DEFAULT_MAXSIZE",
    )
    default_use_sql: bool = Field(
        default=False,
        description="Default SQL storage setting",
        env="TWAT_CACHE_DEFAULT_USE_SQL",
    )
    default_engine: str = Field(
        default="lru",
        description="Default cache engine",
        env="TWAT_CACHE_DEFAULT_ENGINE",
    )
    default_cache_type: CacheType | None = Field(
        default=None,
        description="Default cache type (speed, database, filesystem)",
        env="TWAT_CACHE_DEFAULT_TYPE",
    )

    # Performance settings
    enable_compression: bool = Field(
        default=True,
        description="Enable data compression",
        env="TWAT_CACHE_ENABLE_COMPRESSION",
    )
    compression_level: int = Field(
        default=6,
        description="Compression level (1-9)",
        env="TWAT_CACHE_COMPRESSION_LEVEL",
    )

    # Logging settings
    debug: bool = Field(
        default=False,
        description="Enable debug logging",
        env="TWAT_CACHE_DEBUG",
    )
    log_file: Path | None = Field(
        default=None,
        description="Log file path",
        env="TWAT_CACHE_LOG_FILE",
    )

    def get_cache_config(
        self,
        maxsize: int | None = None,
        folder_name: str | None = None,
        use_sql: bool | None = None,
        preferred_engine: str | None = None,
        cache_type: CacheType | None = None,
    ) -> CacheConfigProtocol:
        """
        Get cache configuration with defaults.

        Args:
            maxsize: Maximum cache size
            folder_name: Cache folder name
            use_sql: Whether to use SQL storage
            preferred_engine: Preferred cache engine
            cache_type: Type of cache to use

        Returns:
            Cache configuration object
        """
        return CacheConfig(
            maxsize=maxsize if maxsize is not None else self.default_maxsize,
            folder_name=folder_name,
            use_sql=use_sql if use_sql is not None else self.default_use_sql,
            preferred_engine=(
                preferred_engine
                if preferred_engine is not None
                else self.default_engine
            ),
            cache_type=(
                cache_type if cache_type is not None else self.default_cache_type
            ),
        )

    def configure_logging(self) -> None:
        """Configure logging based on settings."""
        # Remove default logger
        logger.remove()

        # Configure console logging
        level = "DEBUG" if self.debug else "INFO"
        logger.add(
            sink=lambda msg: print(msg, end=""),
            level=level,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>",
        )

        # Configure file logging if enabled
        if self.log_file:
            logger.add(
                sink=str(self.log_file),
                level=level,
                rotation="10 MB",
                retention="1 week",
            )


# Global configuration instance
config = GlobalConfig()
