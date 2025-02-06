"""Core caching functionality for the twat_cache package."""

from typing import Callable, Optional, TypeVar, cast

from .engines import CacheEngine, DiskCacheEngine, JoblibEngine, LRUEngine

F = TypeVar("F", bound=Callable[..., object])


def ucache(
    folder_name: Optional[str] = None,
    use_sql: bool = False,
    maxsize: Optional[int] = None,
) -> Callable[[F], F]:
    """A universal caching decorator that supports multiple backends.

    This decorator provides a unified interface for caching function results using
    different backends based on availability and requirements:
    - SQL-based caching using diskcache (if use_sql=True and available)
    - Joblib caching for numpy arrays and large objects (if available)
    - LRU caching in memory as fallback

    Args:
        folder_name: Optional name for the cache folder
        use_sql: Whether to use SQL-based caching (requires diskcache)
        maxsize: Maximum size for LRU cache (None means unlimited)

    Returns:
        A decorator function that wraps the target function with caching

    Example:
        @ucache(folder_name="my_cache")
        def expensive_function(x):
            return x * x
    """
    # Initialize engines with configuration
    engines = [
        DiskCacheEngine(folder_name) if use_sql else None,
        JoblibEngine(folder_name),
        LRUEngine(maxsize),
    ]

    # Select first available engine
    engine = next(
        (eng for eng in engines if eng is not None and eng.is_available),
        LRUEngine(maxsize),  # Fallback to LRU cache
    )

    def decorator(func: F) -> F:
        return cast(F, engine.cache(func))

    return decorator
