"""Specialized cache decorators for different use cases."""

# this_file: src/twat_cache/decorators.py

from collections.abc import Callable
from typing import Any, TypeVar

from loguru import logger

from twat_cache.engines.manager import get_engine_manager
from twat_cache.config import create_cache_config
from twat_cache.types import CacheConfig

F = TypeVar("F", bound=Callable[..., Any])


def ucache(
    maxsize: int | None = None,
    folder_name: str | None = None,
    use_sql: bool = False,
    preferred_engine: str | None = None,
    cache_type: str | None = None,
    config: CacheConfig | None = None,
) -> Callable[[F], F]:
    """Universal cache decorator that can use any available cache engine.

    This is the recommended general-purpose cache decorator. It will automatically
    select the most appropriate and efficient caching engine based on the parameters
    and available backends.

    If no specific preferences are given, it defaults to using the fastest available
    memory-based cache.

    Args:
        maxsize: Maximum size for cache (None means unlimited)
        folder_name: Optional name for persistent cache folder
        preferred_engine: Optional name of preferred engine
        use_sql: Whether to prefer SQL-based caching
        cache_type: Optional cache type hint ("speed", "database", "filesystem")
        config: Optional pre-configured CacheConfig instance

    Returns:
        A decorator function that caches the decorated function's results

    Example:
        ```python
        @ucache(maxsize=100)
        def expensive_computation(x: int) -> int:
            return x * x

        # Results will be cached automatically
        result = expensive_computation(42)
        ```
    """
    # Use provided config or create new one
    if config is None:
        config = create_cache_config(
            maxsize=maxsize,
            folder_name=folder_name,
            use_sql=use_sql,
            preferred_engine=preferred_engine,
            cache_type=cache_type,
        )

    # Get engine manager
    manager = get_engine_manager()

    def decorator(func: F) -> F:
        """Wrap the function with caching."""
        # Get appropriate engine
        engine = manager.get_engine(config)
        logger.debug(f"Using cache engine: {engine.__class__.__name__}")

        # Apply caching
        return engine.cache(func)

    return decorator


def mcache(
    maxsize: int | None = None,
    preferred_engine: str | None = None,
) -> Callable[[F], F]:
    """Speed-optimized in-memory cache decorator.

    Prioritizes fastest in-memory engines:
    1. cachebox (Rust-based, fastest)
    2. cachetools (flexible in-memory)
    3. LRU cache (built-in)

    Args:
        maxsize: Maximum size for cache (None means unlimited)
        preferred_engine: Optional name of preferred engine (must be memory-based)

    Returns:
        A decorator function that caches the decorated function's results
    """
    return ucache(
        maxsize=maxsize,
        preferred_engine=preferred_engine,
        cache_type="speed",
    )


def bcache(
    folder_name: str | None = None,
    maxsize: int | None = None,
    preferred_engine: str | None = None,
) -> Callable[[F], F]:
    """Database-persistent cache decorator.

    Prioritizes database-backed engines:
    1. diskcache (SQLite-based)
    2. aiocache (with Redis/Memcached backends)

    Args:
        folder_name: Optional name for the cache folder
        maxsize: Maximum size for cache (None means unlimited)
        preferred_engine: Optional name of preferred engine (must be DB-based)

    Returns:
        A decorator function that caches the decorated function's results
    """
    return ucache(
        folder_name=folder_name,
        maxsize=maxsize,
        use_sql=True,
        preferred_engine=preferred_engine,
        cache_type="database",
    )


def fcache(
    folder_name: str | None = None,
    maxsize: int | None = None,
    preferred_engine: str | None = None,
) -> Callable[[F], F]:
    """Filesystem-persistent cache decorator.

    Prioritizes filesystem-based engines:
    1. joblib (optimized for arrays/large data)
    2. klepto (scientific computing)
    3. diskcache (file-based mode)

    Args:
        folder_name: Optional name for the cache folder
        maxsize: Maximum size for cache (None means unlimited)
        preferred_engine: Optional name of preferred engine (must be filesystem-based)

    Returns:
        A decorator function that caches the decorated function's results
    """
    return ucache(
        folder_name=folder_name,
        maxsize=maxsize,
        preferred_engine=preferred_engine,
        cache_type="filesystem",
    )
