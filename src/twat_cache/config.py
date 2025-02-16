#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "loguru",
# ]
# ///
# this_file: src/twat_cache/config.py

"""Simple configuration for twat_cache."""

from dataclasses import dataclass
from typing import Any
from collections.abc import Callable


@dataclass
class CacheConfig:
    """Basic cache configuration."""

    maxsize: int | None = None
    folder_name: str | None = None
    preferred_engine: str | None = None
    serializer: Callable[[Any], str] | None = None
    use_sql: bool = False
    cache_type: str | None = None

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
        if self.maxsize is not None and self.maxsize <= 0:
            msg = "maxsize must be positive or None"
            raise ValueError(msg)
        if self.folder_name is not None and not isinstance(self.folder_name, str):
            msg = "folder_name must be a string or None"
            raise ValueError(msg)

    def model_dump(self) -> dict[str, Any]:
        """Convert the model to a dictionary."""
        return {
            "maxsize": self.maxsize,
            "folder_name": self.folder_name,
            "preferred_engine": self.preferred_engine,
            "use_sql": self.use_sql,
            "cache_type": self.cache_type,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CacheConfig":
        """Create a config from a dictionary."""
        return cls(**data)


def create_cache_config(
    maxsize: int | None = None,
    folder_name: str | None = None,
    preferred_engine: str | None = None,
    serializer: Callable[[Any], str] | None = None,
    use_sql: bool = False,
    cache_type: str | None = None,
    cache_dir: str | None = None,  # For backward compatibility
) -> CacheConfig:
    """
    Create a cache configuration.

    Args:
        maxsize: Maximum cache size (None for unlimited)
        folder_name: Cache directory name
        preferred_engine: Preferred caching backend ('memory', 'disk', or 'file')
        serializer: Optional function to serialize non-JSON-serializable objects
        use_sql: Whether to use SQL-based disk cache
        cache_type: Type of cache to use
        cache_dir: Alias for folder_name (for backward compatibility)

    Returns:
        A validated cache configuration
    """
    # Handle backward compatibility
    if cache_dir is not None:
        folder_name = cache_dir

    config = CacheConfig(
        maxsize=maxsize,
        folder_name=folder_name,
        preferred_engine=preferred_engine,
        serializer=serializer,
        use_sql=use_sql,
        cache_type=cache_type,
    )
    config.validate()
    return config
