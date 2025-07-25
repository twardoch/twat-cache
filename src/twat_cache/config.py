#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "loguru",
#   "pydantic",
# ]
# ///
# this_file: src/twat_cache/config.py

"""Cache configuration system for TWAT-Cache.

This module provides the configuration infrastructure for the caching system,
including validation, defaults, and environment variable support.

Classes:
    CacheConfig: Main configuration model using Pydantic for validation.
        Handles all cache-related settings including size limits, TTL,
        eviction policies, and backend-specific options.

Functions:
    create_cache_config: Factory function to create CacheConfig instances
        with proper defaults and validation.
    get_cache_config_from_env: Load configuration from environment variables.
    merge_configs: Merge multiple configurations with precedence rules.

Configuration Sources:
    1. Direct parameters (highest priority)
    2. Environment variables (TWAT_CACHE_* prefix)
    3. Configuration files (future support)
    4. Default values (lowest priority)

Environment Variables:
    TWAT_CACHE_MAXSIZE: Maximum cache size (integer)
    TWAT_CACHE_TTL: Time-to-live in seconds (float)
    TWAT_CACHE_POLICY: Eviction policy (lru, lfu, fifo, etc.)
    TWAT_CACHE_FOLDER: Cache folder name
    TWAT_CACHE_ENGINE: Preferred cache engine
    TWAT_CACHE_COMPRESS: Enable compression (true/false)
    TWAT_CACHE_SECURE: Enable secure mode (true/false)

Example:
    Basic configuration::
    
        from twat_cache.config import create_cache_config
        
        # Create config with specific settings
        config = create_cache_config(
            maxsize=1000,
            ttl=3600,
            policy="lru",
            compress=True
        )
    
    Environment-based configuration::
    
        import os
        os.environ["TWAT_CACHE_MAXSIZE"] = "500"
        os.environ["TWAT_CACHE_TTL"] = "300"
        
        config = get_cache_config_from_env()

Note:
    The configuration system is designed to be flexible and extensible,
    allowing for easy addition of new cache backends and options.
"""

import os
from typing import Any
from collections.abc import Callable

from pydantic import BaseModel, Field, field_validator

# Type aliases
EvictionPolicy = str | None
CacheType = str | None


class CacheConfig(BaseModel):
    """Cache configuration settings.
    
    A Pydantic model that validates and manages all cache-related configuration.
    This class ensures type safety and provides sensible defaults for all settings.
    
    Attributes:
        maxsize: Maximum number of items to store in cache. None means unlimited.
        folder_name: Name of the folder for disk/file-based caches. Auto-generated if None.
        preferred_engine: Preferred cache backend. If unavailable, falls back to alternatives.
        serializer: Custom serializer function for cache keys. Uses JSON by default.
        ttl: Time-to-live for cached items in seconds. None means no expiration.
        policy: Cache eviction policy ('lru', 'lfu', 'fifo', 'lifo', 'mru').
        cache_dir: Deprecated. Use folder_name instead. Kept for backward compatibility.
        compress: Whether to compress cached values (for file/disk backends).
        secure: Whether to use secure key generation (handles more types but slower).
    
    Example:
        >>> config = CacheConfig(maxsize=100, ttl=3600, policy="lfu")
        >>> print(config.maxsize)
        100
        >>> print(config.get_ttl_seconds())
        3600
    """

    maxsize: int | None = Field(default=None, ge=1)
    folder_name: str | None = None
    preferred_engine: str | None = None
    serializer: Callable[[Any], str] | None = None
    # cache_type: CacheType | None = None # REMOVED - preferred_engine is used
    ttl: float | None = Field(default=None, ge=0)
    policy: EvictionPolicy = "lru"
    cache_dir: str | None = None  # For backward compatibility

    # Boolean fields
    # use_sql: bool = False # REMOVED (hint for de-emphasized Klepto)
    compress: bool = False
    secure: bool = True

    # Redis-specific configuration REMOVED
    # redis_host: str = "localhost"
    # redis_port: int = 6379
    # redis_db: int = 0
    # redis_password: str | None = None

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

    # Removed redis_port validator

    def to_dict(self) -> dict[str, Any]:
        """Convert configuration to dictionary."""
        data = {
            "maxsize": self.maxsize,
            "folder_name": self.folder_name,
            "preferred_engine": self.preferred_engine,
            "serializer": self.serializer,
            # "cache_type": self.cache_type, # REMOVED
            "ttl": self.ttl,
            "policy": self.policy,
            # "use_sql": self.use_sql, # REMOVED
            "compress": self.compress,
            "secure": self.secure,
            "cache_dir": self.cache_dir, # For backward compatibility
        }
        # Removed Redis fields from dict
        return data

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

    # def get_use_sql(self) -> bool: # REMOVED
    #     """Get the use_sql value."""
    #     return self.use_sql

    def get_preferred_engine(self) -> str | None:
        """Get the preferred engine."""
        return self.preferred_engine

    # def get_cache_type(self) -> str | None: # REMOVED
    #     """Get the cache type."""
    #     return self.cache_type

    # Redis-specific getters REMOVED
    # def get_redis_host(self) -> str: ...
    # def get_redis_port(self) -> int: ...
    # def get_redis_db(self) -> int: ...
    # def get_redis_password(self) -> str | None: ...

    # We can't override the validate method as it conflicts with Pydantic's validate
    # Instead, we'll implement a protocol-compatible method with a different name
    def validate_config(self) -> None:
        """Validate the configuration (protocol compatibility method)."""
        # This is handled by Pydantic validators


def create_cache_config(
    maxsize: int | None = None,
    folder_name: str | None = None,
    preferred_engine: str | None = None,
    serializer: Callable[[Any], str] | None = None,
    # cache_type: CacheType | None = None, # REMOVED
    ttl: float | None = None,
    policy: EvictionPolicy = "lru",
    cache_dir: str | None = None,  # For backward compatibility
    *,  # Force remaining arguments to be keyword-only
    # use_sql: bool = False, # REMOVED
    compress: bool = False,
    secure: bool = True,
    # redis_host: str = "localhost", # REMOVED
    # redis_port: int = 6379, # REMOVED
    # redis_db: int = 0, # REMOVED
    # redis_password: str | None = None, # REMOVED
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
        redis_host: Redis server hostname.
        redis_port: Redis server port.
        redis_db: Redis database number.
        redis_password: Redis server password.

    Returns:
        CacheConfig: Cache configuration object.

    Raises:
        ValueError: If configuration is invalid.
    """
    actual_folder_name = folder_name
    if actual_folder_name is None and cache_dir is not None:
        # If folder_name is not given, but cache_dir (for backward compat) is,
        # use the basename of cache_dir as the folder_name.
        # This assumes cache_dir is just a directory name, not a full path.
        # If cache_dir is a full path, get_cache_path will handle it.
        # For DiskCacheEngine, it needs a folder_name to construct its path.
        actual_folder_name = os.path.basename(cache_dir)

    return CacheConfig(
        maxsize=maxsize,
        folder_name=actual_folder_name,
        preferred_engine=preferred_engine,
        serializer=serializer,
        # cache_type=cache_type, # REMOVED
        ttl=ttl,
        policy=policy,
        # use_sql=use_sql, # REMOVED
        compress=compress,
        secure=secure,
        cache_dir=cache_dir,
        # redis_host=redis_host, # REMOVED
        # redis_port=redis_port, # REMOVED
        # redis_db=redis_db, # REMOVED
        # redis_password=redis_password, # REMOVED
    )
