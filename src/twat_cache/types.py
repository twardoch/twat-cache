#!/usr/bin/env -S uv run
# /// script
# dependencies = []
# ///
# this_file: src/twat_cache/types.py

"""
Core type definitions for twat-cache.

This module defines the fundamental types and type variables used throughout
the caching system, ensuring type safety and providing clear interfaces.
"""

from abc import ABC, abstractmethod
from typing import (
    Any,
    Generic,
    Protocol,
    TypeVar,
    Literal,
    runtime_checkable,
)
from collections.abc import Callable
from pathlib import Path

# Type variables for generic cache types
T = TypeVar("T")
P = TypeVar("P")
R = TypeVar("R")

# Cache key and value types
CacheKey = str | int | float | tuple[Any, ...]
CacheValue = Any  # Consider constraining this in future versions


@runtime_checkable
class CacheConfig(Protocol):
    """Protocol defining the required configuration interface for cache engines."""

    maxsize: int | None
    folder_name: str | None
    use_sql: bool
    preferred_engine: str | None

    def validate(self) -> None:
        """Validate the configuration settings."""
        ...


class CacheStats(ABC):
    """Base class defining the interface for cache statistics."""

    @property
    @abstractmethod
    def hits(self) -> int:
        """Number of cache hits."""
        ...

    @property
    @abstractmethod
    def misses(self) -> int:
        """Number of cache misses."""
        ...

    @property
    @abstractmethod
    def size(self) -> int:
        """Current cache size."""
        ...

    @property
    @abstractmethod
    def maxsize(self) -> int | None:
        """Maximum cache size."""
        ...

    @abstractmethod
    def clear(self) -> None:
        """Clear all statistics."""
        ...


class CacheEngine(ABC, Generic[P, R]):
    """
    Abstract base class defining the required interface for cache engine implementations.

    This class provides the foundation for all cache backend implementations,
    ensuring they provide the necessary functionality.
    """

    @abstractmethod
    def cache(self, func: Callable[P, R]) -> Callable[P, R]:
        """
        Decorate a function with caching capability.

        Args:
            func: The function to cache

        Returns:
            A wrapped function that will use the cache
        """
        ...

    @abstractmethod
    def clear(self) -> None:
        """Clear all cached values."""
        ...

    @abstractmethod
    def validate_config(self) -> None:
        """
        Validate the engine configuration.

        Raises:
            ValueError: If the configuration is invalid
        """
        ...

    @property
    @abstractmethod
    def stats(self) -> dict[str, Any]:
        """Get cache statistics."""
        ...


# Cache backend types
BackendType = Literal[
    "cachebox",  # Rust-based
    "cachetools",  # Flexible in-memory
    "aiocache",  # Async support with Redis
    "klepto",  # Scientific computing
    "diskcache",  # SQL-based disk cache
    "joblib",  # Array caching
    "memory",  # Always available
]

# Cache path types
CachePath = str | Path
CachePathFactory = Callable[[], CachePath]


@runtime_checkable
class KeyMaker(Protocol):
    """Protocol defining the interface for cache key generation."""

    def __call__(self, *args: Any, **kwargs: Any) -> CacheKey:
        """Generate a cache key from function arguments."""
        ...


@runtime_checkable
class Serializer(Protocol):
    """Protocol defining the interface for cache value serialization."""

    def dumps(self, obj: Any) -> bytes:
        """Serialize an object to bytes."""
        ...

    def loads(self, data: bytes) -> Any:
        """Deserialize bytes to an object."""
        ...


# Export all types
__all__ = [
    "BackendType",
    "CacheConfig",
    "CacheEngine",
    "CacheKey",
    "CachePath",
    "CachePathFactory",
    "CacheStats",
    "CacheValue",
    "KeyMaker",
    "P",
    "R",
    "Serializer",
]
