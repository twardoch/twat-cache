#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "loguru",
#   "pydantic",
# ]
# ///
# this_file: src/twat_cache/config.py

"""Cache configuration system."""

from typing import Any, Dict, Optional
from collections.abc import Callable

from pydantic import BaseModel, Field, field_validator

# Type aliases
EvictionPolicy = str | None
CacheType = str | None


class CacheConfig(BaseModel):
    """Cache configuration settings."""

    maxsize: int | None = Field(default=None, ge=1)
    folder_name: str | None = None
    preferred_engine: str | None = None
    serializer: Callable[[Any], str] | None = None
    cache_type: CacheType | None = None
    ttl: float | None = Field(default=None, ge=0)
    policy: EvictionPolicy = "lru"
    cache_dir: str | None = None  # For backward compatibility

    # Boolean fields
    use_sql: bool = False
    compress: bool = False
    secure: bool = True

    class Config:
        """Pydantic model configuration."""

        validate_assignment = True
        extra = "forbid"

    @classmethod
    @field_validator("maxsize")
    def validate_maxsize(cls, v: int | None) -> int | None:
        """Validate maxsize field."""
        if v is not None and v <= 0:
            msg = "maxsize must be positive"
            raise ValueError(msg)
        return v

    @classmethod
    @field_validator("ttl")
    def validate_ttl(cls, v: float | None) -> float | None:
        """Validate ttl field."""
        if v is not None and v < 0:
            msg = "ttl must be non-negative"
            raise ValueError(msg)
        return v

    @classmethod
    @field_validator("policy")
    def validate_policy(cls, v: EvictionPolicy) -> EvictionPolicy:
        """Validate policy field."""
        valid_policies = {"lru", "lfu", "fifo", "rr", "ttl"}
        if v is not None and v not in valid_policies:
            msg = f"policy must be one of {valid_policies}"
            raise ValueError(msg)
        return v

    def to_dict(self) -> dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "maxsize": self.maxsize,
            "folder_name": self.folder_name,
            "preferred_engine": self.preferred_engine,
            "serializer": self.serializer,
            "cache_type": self.cache_type,
            "ttl": self.ttl,
            "policy": self.policy,
            "use_sql": self.use_sql,
            "compress": self.compress,
            "secure": self.secure,
            "cache_dir": self.cache_dir,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CacheConfig":
        """Create configuration from dictionary."""
        return cls(**data)

    # Methods required by the CacheConfig protocol
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

    def validate_config(self) -> None:
        """Validate the configuration (protocol compatibility method)."""
        # This is handled by Pydantic validators
        pass


def create_cache_config(
    maxsize: int | None = None,
    folder_name: str | None = None,
    preferred_engine: str | None = None,
    serializer: Callable[[Any], str] | None = None,
    cache_type: CacheType | None = None,
    ttl: float | None = None,
    policy: EvictionPolicy = "lru",
    cache_dir: str | None = None,  # For backward compatibility
    *,  # Force remaining arguments to be keyword-only
    use_sql: bool = False,
    compress: bool = False,
    secure: bool = True,
) -> CacheConfig:
    """Create a cache configuration.

    Args:
        maxsize: Maximum size of the cache. None means unlimited.
        folder_name: Name of the cache folder.
        preferred_engine: Preferred cache engine.
        serializer: Function to serialize cache keys.
        cache_type: Type of cache to use.
        ttl: Time-to-live in seconds.
        policy: Cache eviction policy.
        cache_dir: Cache directory (deprecated).
        use_sql: Whether to use SQL backend.
        compress: Whether to compress cached data.
        secure: Whether to use secure file permissions.

    Returns:
        CacheConfig: Cache configuration object.

    Raises:
        ValueError: If configuration is invalid.
    """
    return CacheConfig(
        maxsize=maxsize,
        folder_name=folder_name,
        preferred_engine=preferred_engine,
        serializer=serializer,
        cache_type=cache_type,
        ttl=ttl,
        policy=policy,
        use_sql=use_sql,
        compress=compress,
        secure=secure,
        cache_dir=cache_dir,
    )
