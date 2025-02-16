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
from typing import Literal, Any

from loguru import logger
from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings

from .paths import get_cache_path
from .types import CacheConfig as CacheConfigBase


CacheType = Literal["speed", "database", "filesystem"]


class CacheConfig(BaseModel, CacheConfigBase):
    """
    Cache configuration model.

    This class implements the CacheConfig base class and provides validation
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

    model_config = {
        "validate_assignment": True,
        "extra": "ignore",
        "arbitrary_types_allowed": True,
        "from_attributes": True,
        "populate_by_name": True,
    }

    @field_validator("maxsize")
    def validate_maxsize(cls, v: int | None) -> int | None:
        """Validate maxsize setting."""
        if v is not None and v <= 0:
            msg = "maxsize must be positive if specified"
            raise ValueError(msg)
        return v

    @field_validator("folder_name")
    def validate_folder_name(cls, v: str | None) -> str | None:
        """Validate folder name setting."""
        if v is not None and not v.strip():
            msg = "folder_name must not be empty if specified"
            raise ValueError(msg)
        return v

    @field_validator("cache_type")
    def validate_cache_type(cls, v: CacheType | None) -> CacheType | None:
        """Validate cache type setting."""
        valid_types = {"speed", "database", "filesystem", None}
        if v not in valid_types:
            msg = f"cache_type must be one of {valid_types}"
            raise ValueError(msg)
        return v

    def validate(self) -> None:
        """Validate all configuration settings."""
        if self.maxsize is not None:
            self.validate_maxsize(self.maxsize)
        if self.folder_name is not None:
            self.validate_folder_name(self.folder_name)
        if self.cache_type is not None:
            self.validate_cache_type(self.cache_type)

    def model_post_init(self, __context: Any) -> None:
        """Post-initialization validation."""
        super().model_post_init(__context)
        self.validate()

    # CacheConfigBase interface implementation
    def get_maxsize(self) -> int | None:
        """Get maximum cache size."""
        return self.maxsize

    def get_folder_name(self) -> str | None:
        """Get cache folder name."""
        return self.folder_name

    def get_use_sql(self) -> bool:
        """Get SQL storage setting."""
        return self.use_sql

    def get_preferred_engine(self) -> str | None:
        """Get preferred cache engine."""
        return self.preferred_engine

    def get_cache_type(self) -> CacheType | None:
        """Get cache type."""
        return self.cache_type


class GlobalConfig(BaseSettings):
    """
    Global configuration settings.

    This class manages global settings for the caching system, including
    defaults and environment variable configuration.
    """

    model_config = {
        "env_prefix": "TWAT_CACHE_",
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "validate_assignment": True,
        "extra": "ignore",
        "arbitrary_types_allowed": True,
        "from_attributes": True,
        "use_enum_values": True,
        "populate_by_name": True,
    }

    # Cache directory settings
    cache_dir: Path = Field(
        default_factory=get_cache_path,
        description="Base directory for cache storage",
        validation_alias="CACHE_DIR",
    )

    # Default cache settings
    default_maxsize: int = Field(
        default=1000,
        description="Default maximum cache size",
        validation_alias="DEFAULT_MAXSIZE",
    )
    default_use_sql: bool = Field(
        default=False,
        description="Default SQL storage setting",
        validation_alias="DEFAULT_USE_SQL",
    )
    default_engine: str = Field(
        default="lru",
        description="Default cache engine",
        validation_alias="DEFAULT_ENGINE",
    )
    default_cache_type: CacheType | None = Field(
        default=None,
        description="Default cache type (speed, database, filesystem)",
        validation_alias="DEFAULT_TYPE",
    )

    # Performance settings
    enable_compression: bool = Field(
        default=True,
        description="Enable data compression",
        validation_alias="ENABLE_COMPRESSION",
    )
    compression_level: int = Field(
        default=6,
        description="Compression level (1-9)",
        validation_alias="COMPRESSION_LEVEL",
    )

    # Logging settings
    debug: bool = Field(
        default=False,
        description="Enable debug logging",
        validation_alias="DEBUG",
    )
    log_file: Path | None = Field(
        default=None,
        description="Log file path",
        validation_alias="LOG_FILE",
    )

    def get_cache_config(
        self,
        maxsize: int | None = None,
        folder_name: str | None = None,
        use_sql: bool | None = None,
        preferred_engine: str | None = None,
        cache_type: CacheType | None = None,
    ) -> CacheConfig:
        """
        Get cache configuration with defaults.

        Args:
            maxsize: Maximum cache size
            folder_name: Cache folder name
            use_sql: Whether to use SQL storage
            preferred_engine: Preferred cache engine
            cache_type: Type of cache to use

        Returns:
            CacheConfig: Cache configuration with defaults applied
        """
        return CacheConfig(
            maxsize=maxsize if maxsize is not None else self.default_maxsize,
            folder_name=folder_name,
            use_sql=use_sql if use_sql is not None else self.default_use_sql,
            preferred_engine=preferred_engine
            if preferred_engine is not None
            else self.default_engine,
            cache_type=cache_type
            if cache_type is not None
            else self.default_cache_type,
        )

    @field_validator("compression_level")
    def validate_compression_level(cls, v: int) -> int:
        """Validate compression level."""
        if not 1 <= v <= 9:
            msg = "compression_level must be between 1 and 9"
            raise ValueError(msg)
        return v

    @field_validator("log_file")
    def validate_log_file(cls, v: Path | None | str) -> Path | None:
        """Validate log file path."""
        if v is None:
            return None
        if isinstance(v, str):
            v = Path(v)
        if not v.parent.exists():
            v.parent.mkdir(parents=True, exist_ok=True)
        return v

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
