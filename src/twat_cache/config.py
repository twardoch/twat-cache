#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "loguru",
# ]
# ///
# this_file: src/twat_cache/config.py

"""
Simple configuration system for twat_cache.

This module provides a simple configuration system for the cache decorators.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable


@dataclass
class CacheConfig:
    """Cache configuration."""

    maxsize: int | None = None
    folder_name: str | None = None
    preferred_engine: str | None = None
    serializer: Callable[[Any], str] | None = None
    use_sql: bool = field(default=False, init=False)

    def to_dict(self) -> dict[str, Any]:
        """Convert config to dictionary."""
        return {
            "maxsize": self.maxsize,
            "folder_name": self.folder_name,
            "preferred_engine": self.preferred_engine,
            "use_sql": self.use_sql,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CacheConfig":
        """Create config from dictionary."""
        return cls(
            maxsize=data.get("maxsize"),
            folder_name=data.get("folder_name"),
            preferred_engine=data.get("preferred_engine"),
            use_sql=data.get("use_sql", False),
        )

    def validate(self) -> None:
        """Validate configuration."""
        if self.maxsize is not None and self.maxsize <= 0:
            msg = "maxsize must be positive if specified"
            raise ValueError(msg)

        if self.preferred_engine is not None and self.preferred_engine not in {
            "memory",
            "disk",
            "fast",
        }:
            msg = "preferred_engine must be one of: memory, disk, fast"
            raise ValueError(msg)

        if self.folder_name is not None:
            try:
                path = Path(self.folder_name)
                if not path.parent.exists():
                    msg = f"Parent directory does not exist: {path.parent}"
                    raise ValueError(msg)
            except Exception as e:
                msg = f"Invalid folder name: {e}"
                raise ValueError(msg) from e


def create_cache_config(**kwargs: Any) -> CacheConfig:
    """
    Create a cache configuration.

    Args:
        **kwargs: Configuration options

    Returns:
        A validated cache configuration
    """
    config = CacheConfig(**kwargs)
    config.validate()
    return config
