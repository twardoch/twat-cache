"""Base protocol and utilities for cache engines."""

from typing import Any, Protocol, TypeVar, runtime_checkable
from collections.abc import Callable

T = TypeVar("T")
F = TypeVar("F", bound=Callable[..., Any])


@runtime_checkable
class CacheEngine(Protocol):
    """Protocol defining the interface for cache engines."""

    def cache(self, func: F) -> F:
        """Cache decorator for the function.

        Args:
            func: Function to be cached

        Returns:
            Cached function wrapper
        """
        ...

    def clear(self) -> None:
        """Clear all cached values."""
        ...

    @property
    def is_available(self) -> bool:
        """Check if this cache engine is available in current environment."""
        ...

    @property
    def name(self) -> str:
        """Get the name of the cache engine."""
        ...
