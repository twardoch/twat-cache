#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "loguru",
#   "pydantic",
# ]
# ///
# this_file: src/twat_cache/config.py

"""Cache configuration system."""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Optional, Union

from pydantic import BaseModel, Field, field_validator

# Type aliases
EvictionPolicy = Union[str, None]
CacheType = Union[str, None]


@dataclass
class CacheConfig(BaseModel):
    """Cache configuration settings."""

    maxsize: Optional[int] = Field(default=None, ge=1)
    folder_name: Optional[str] = None
    preferred_engine: Optional[str] = None
    serializer: Optional[Callable[[Any], str]] = None
    cache_type: Optional[CacheType] = None
    ttl: Optional[float] = Field(default=None, ge=0)
    policy: EvictionPolicy = "lru"
    cache_dir: Optional[str] = None  # For backward compatibility

    # Keyword-only boolean fields
    use_sql: bool = field(default=False, kw_only=True)
    compress: bool = field(default=False, kw_only=True)
    secure: bool = field(default=True, kw_only=True)

    class Config:
        """Pydantic model configuration."""

        validate_assignment = True
        extra = "forbid"

    @field_validator("maxsize")
    def validate_maxsize(cls, v: Optional[int]) -> Optional[int]:
        """Validate maxsize field."""
        if v is not None and v <= 0:
            raise ValueError("maxsize must be positive")
        return v

    @field_validator("ttl")
    def validate_ttl(cls, v: Optional[float]) -> Optional[float]:
        """Validate ttl field."""
        if v is not None and v < 0:
            raise ValueError("ttl must be non-negative")
        return v

    @field_validator("policy")
    def validate_policy(cls, v: EvictionPolicy) -> EvictionPolicy:
        """Validate policy field."""
        valid_policies = {"lru", "lfu", "fifo", "rr", "ttl"}
        if v is not None and v not in valid_policies:
            raise ValueError(f"policy must be one of {valid_policies}")
        return v

    def to_dict(self) -> Dict[str, Any]:
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
    def from_dict(cls, data: Dict[str, Any]) -> "CacheConfig":
        """Create configuration from dictionary."""
        return cls(**data)


def create_cache_config(
    maxsize: Optional[int] = None,
    folder_name: Optional[str] = None,
    preferred_engine: Optional[str] = None,
    serializer: Optional[Callable[[Any], str]] = None,
    cache_type: Optional[CacheType] = None,
    ttl: Optional[float] = None,
    policy: EvictionPolicy = "lru",
    cache_dir: Optional[str] = None,  # For backward compatibility
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
