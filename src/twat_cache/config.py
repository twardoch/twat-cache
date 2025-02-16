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
from typing import Literal, Any, cast
import sys

from loguru import logger
from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings

from .paths import get_cache_path
from .types import CacheConfig as CacheConfigProtocol


CacheType = Literal["speed", "database", "filesystem"]


class CacheConfigImpl(BaseModel):
    """Cache configuration settings."""

    maxsize: int | None = Field(default=None, description="Maximum size of the cache")
    folder_name: str | None = Field(
        default=None, description="Name of the cache folder"
    )
    use_sql: bool = Field(default=False, description="Whether to use SQL storage")
    preferred_engine: str | None = Field(
        default=None, description="Preferred cache engine"
    )
    cache_type: str | None = Field(default=None, description="Type of cache to use")

    model_config = {
        "validate_assignment": True,
        "extra": "ignore",
        "arbitrary_types_allowed": True,
        "from_attributes": True,
        "populate_by_name": True,
    }

    @field_validator("maxsize")
    @classmethod
    def validate_maxsize(cls, v: int | None) -> int | None:
        """Validate the maxsize value."""
        if v is not None and not isinstance(v, int):
            msg = "maxsize must be an integer or None"
            raise ValueError(msg)
        if v is not None and v <= 0:
            msg = "maxsize must be positive"
            raise ValueError(msg)
        return v

    @field_validator("folder_name")
    @classmethod
    def validate_folder_name(cls, v: str | None) -> str | None:
        """Validate the folder name."""
        if v is not None and not isinstance(v, str):
            msg = "folder_name must be a string or None"
            raise ValueError(msg)
        if v is not None and not v.strip():
            msg = "folder_name must not be empty if specified"
            raise ValueError(msg)
        return v

    def get_maxsize(self) -> int | None:
        """Get the maxsize value."""
        return self.maxsize

    def get_folder_name(self) -> str | None:
        """Get the folder name."""
        return self.folder_name

    def get_use_sql(self) -> bool:
        """Get the use_sql value."""
        return self.use_sql

    def get_preferred_engine(self) -> str | None:
        """Get the preferred engine."""
        return self.preferred_engine

    def get_cache_type(self) -> str | None:
        """Get the cache type."""
        return self.cache_type

    def validate(self) -> None:
        """Validate the configuration."""
        self.validate_maxsize(self.maxsize)
        self.validate_folder_name(self.folder_name)

    def model_dump(self) -> dict[str, Any]:
        """Convert the model to a dictionary."""
        return super().model_dump()


def create_cache_config(**kwargs: Any) -> CacheConfigProtocol:
    """Create a new cache configuration instance."""
    config = CacheConfigImpl(**kwargs)
    return cast(CacheConfigProtocol, config)


# Export CacheConfig as the Protocol type
CacheConfig = CacheConfigProtocol


class GlobalConfig(BaseSettings):
    """Global configuration settings for the caching system."""

    cache_dir: Path = Field(
        default_factory=lambda: get_cache_path("global"),
        description="Cache directory path",
    )
    default_maxsize: int = Field(default=1000, description="Default maximum cache size")
    default_use_sql: bool = Field(
        default=False, description="Default SQL storage setting"
    )
    default_engine: str = Field(default="lru", description="Default cache engine")
    default_cache_type: str | None = Field(
        default=None, description="Default cache type"
    )
    enable_compression: bool = Field(default=True, description="Enable compression")
    compression_level: int = Field(default=6, description="Compression level")
    debug: bool = Field(default=False, description="Enable debug mode")
    log_file: Path | None = Field(default=None, description="Log file path")

    model_config = {
        "env_prefix": "TWAT_CACHE_",
        "validate_assignment": True,
        "extra": "ignore",
        "arbitrary_types_allowed": True,
    }

    @field_validator("compression_level")
    @classmethod
    def validate_compression_level(cls, v: int) -> int:
        """Validate compression level."""
        if not isinstance(v, int):
            msg = "compression_level must be an integer"
            raise ValueError(msg)
        if not 0 <= v <= 9:
            msg = "compression_level must be between 0 and 9"
            raise ValueError(msg)
        return v

    @field_validator("log_file")
    @classmethod
    def validate_log_file(cls, v: Path | None) -> Path | None:
        """Validate log file path."""
        if v is not None:
            if isinstance(v, str):
                v = Path(v)
            if not isinstance(v, Path):
                msg = "log_file must be a string or Path"
                raise ValueError(msg)
            # Ensure parent directory exists
            v.parent.mkdir(parents=True, exist_ok=True)
        return v

    def get_cache_config(self, **overrides) -> CacheConfigProtocol:
        """Create a CacheConfig instance with defaults from global config."""
        config_data = {
            "maxsize": self.default_maxsize,
            "folder_name": None,
            "use_sql": self.default_use_sql,
            "preferred_engine": self.default_engine,
            "cache_type": self.default_cache_type,
        }
        config_data.update(overrides)
        return create_cache_config(**config_data)

    def configure_logging(self) -> None:
        """Configure logging based on settings."""
        # Remove default logger
        logger.remove()

        # Configure log level
        log_level = "DEBUG" if self.debug else "INFO"

        # Add console handler
        logger.add(sys.stderr, level=log_level)

        # Add file handler if log_file is specified
        if self.log_file is not None:
            # Create parent directory but not the file itself
            self.log_file.parent.mkdir(parents=True, exist_ok=True)
            logger.add(
                self.log_file,
                level=log_level,
                rotation="1 day",
                retention="1 week",
                compression="zip" if self.enable_compression else None,
                delay=True,  # Don't create file until first log
            )


# Create global configuration instance
global_config = GlobalConfig()
