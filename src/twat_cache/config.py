#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "loguru",
#   "pydantic",
# ]
# ///
# this_file: src/twat_cache/config.py

"""Simple configuration for twat_cache."""

from typing import Any, Callable, Literal, Optional
from pydantic import BaseModel, Field, field_validator, model_validator

CacheType = Literal["memory", "disk", "file", "async"]
EvictionPolicy = Literal["lru", "lfu", "fifo", "rr", "ttl"]


class CacheConfig(BaseModel):
    """Cache configuration using Pydantic for validation."""

    maxsize: Optional[int] = Field(
        default=None, description="Maximum cache size (None for unlimited)", ge=1
    )
    folder_name: Optional[str] = Field(default=None, description="Cache directory name")
    preferred_engine: Optional[str] = Field(
        default=None, description="Preferred caching backend"
    )
    serializer: Optional[Callable[[Any], str]] = Field(
        default=None, description="Function to serialize non-JSON-serializable objects"
    )
    use_sql: bool = Field(
        default=False, description="Whether to use SQL-based disk cache"
    )
    cache_type: Optional[CacheType] = Field(
        default=None, description="Type of cache to use"
    )
    ttl: Optional[float] = Field(
        default=None, description="Time-to-live in seconds", ge=0
    )
    policy: EvictionPolicy = Field(default="lru", description="Cache eviction policy")
    compress: bool = Field(default=False, description="Whether to compress cached data")
    secure: bool = Field(
        default=True,
        description="Whether to use secure file permissions for disk cache",
    )

    model_config = {
        "arbitrary_types_allowed": True,
        "validate_assignment": True,
        "extra": "forbid",
    }

    @field_validator("folder_name")
    @classmethod
    def validate_folder_name(cls, v: Optional[str]) -> Optional[str]:
        """Validate folder name if provided."""
        if v is not None and not isinstance(v, str):
            raise ValueError("folder_name must be a string or None")
        return v

    @field_validator("preferred_engine")
    @classmethod
    def validate_preferred_engine(cls, v: Optional[str]) -> Optional[str]:
        """Validate preferred engine if provided."""
        valid_engines = {
            "cachebox",
            "cachetools",
            "diskcache",
            "joblib",
            "klepto",
            "functools",
            "aiocache",
        }
        if v is not None and v not in valid_engines:
            raise ValueError(f"preferred_engine must be one of {valid_engines}")
        return v

    @model_validator(mode="after")
    def validate_ttl_policy(self) -> "CacheConfig":
        """Validate TTL and policy compatibility."""
        if self.ttl is not None and self.policy != "ttl":
            self.policy = "ttl"
        return self


def create_cache_config(
    maxsize: Optional[int] = None,
    folder_name: Optional[str] = None,
    preferred_engine: Optional[str] = None,
    serializer: Optional[Callable[[Any], str]] = None,
    use_sql: bool = False,
    cache_type: Optional[CacheType] = None,
    ttl: Optional[float] = None,
    policy: EvictionPolicy = "lru",
    compress: bool = False,
    secure: bool = True,
    cache_dir: Optional[str] = None,  # For backward compatibility
) -> CacheConfig:
    """
    Create a validated cache configuration.

    Args:
        maxsize: Maximum cache size (None for unlimited)
        folder_name: Cache directory name
        preferred_engine: Preferred caching backend
        serializer: Function to serialize non-JSON-serializable objects
        use_sql: Whether to use SQL-based disk cache
        cache_type: Type of cache to use
        ttl: Time-to-live in seconds
        policy: Cache eviction policy
        compress: Whether to compress cached data
        secure: Whether to use secure file permissions
        cache_dir: Alias for folder_name (for backward compatibility)

    Returns:
        A validated CacheConfig instance
    """
    # Handle backward compatibility
    if cache_dir is not None:
        folder_name = cache_dir

    return CacheConfig(
        maxsize=maxsize,
        folder_name=folder_name,
        preferred_engine=preferred_engine,
        serializer=serializer,
        use_sql=use_sql,
        cache_type=cache_type,
        ttl=ttl,
        policy=policy,
        compress=compress,
        secure=secure,
    )
