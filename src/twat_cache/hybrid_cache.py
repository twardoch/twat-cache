#!/usr/bin/env -S uv run -s
# /// script
# dependencies = [
#   "loguru",
#   "pydantic",
# ]
# ///
# this_file: src/twat_cache/hybrid_cache.py

"""
Hybrid caching implementation for twat_cache.

This module provides decorators that can dynamically select the most appropriate
cache backend based on the characteristics of the function's return value.
"""

import functools
import sys
from typing import Any, Callable, Dict, Optional, TypeVar, cast

from loguru import logger

from twat_cache.backend_selector import (
    detect_result_type,
    estimate_data_size,
    DataSize,
    SIZE_THRESHOLDS,
)
from twat_cache.decorators import cache
from twat_cache.config import CacheConfig
from twat_cache.type_defs import P, R, F

# Cache for storing function results with their selected backends
_RESULT_BACKEND_CACHE: Dict[str, str] = {}


def hybrid_cache(
    small_result_config: Optional[CacheConfig] = None,
    large_result_config: Optional[CacheConfig] = None,
    size_threshold: int = SIZE_THRESHOLDS[DataSize.MEDIUM],
    analyze_first_call: bool = True,
) -> Callable[[F], F]:
    """
    Decorator that selects the appropriate cache backend based on result size.

    This decorator will use the small_result_config for results smaller than
    the size_threshold, and large_result_config for larger results. If
    analyze_first_call is True, it will analyze the first call to determine
    the appropriate backend and then stick with it for subsequent calls.

    Args:
        small_result_config: Cache configuration for small results
        large_result_config: Cache configuration for large results
        size_threshold: Size threshold in bytes (default: 1MB)
        analyze_first_call: Whether to analyze the first call to determine backend

    Returns:
        Callable: Decorated function with hybrid caching
    """
    # Set default configurations if not provided
    if small_result_config is None:
        small_result_config = CacheConfig(preferred_engine="cachetools", maxsize=128)

    if large_result_config is None:
        large_result_config = CacheConfig(preferred_engine="diskcache", compress=True)

    def decorator(func: F) -> F:
        # Generate a unique key for this function
        func_key = f"{func.__module__}.{func.__qualname__}"

        # Initialize with small result config by default
        active_config = small_result_config

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            nonlocal active_config

            # Check if we've already determined the backend for this function
            if not analyze_first_call and func_key in _RESULT_BACKEND_CACHE:
                # Use the cached backend decision
                if _RESULT_BACKEND_CACHE[func_key] == "large":
                    active_config = large_result_config
                else:
                    active_config = small_result_config

            # Apply the current active configuration
            cached_func = cache(config=active_config)(func)
            result = cached_func(*args, **kwargs)

            # If this is the first call and we're analyzing, determine the appropriate backend
            if analyze_first_call and func_key not in _RESULT_BACKEND_CACHE:
                try:
                    # Estimate the size of the result
                    size = sys.getsizeof(result)

                    # For containers, add approximate size of contents
                    if isinstance(result, (list, tuple, set)):
                        for item in result:
                            size += sys.getsizeof(item)
                    elif isinstance(result, dict):
                        for key, value in result.items():
                            size += sys.getsizeof(key) + sys.getsizeof(value)

                    # Select the appropriate backend based on size
                    if size > size_threshold:
                        logger.debug(f"Using large result config for {func_key} (size: {size} bytes)")
                        active_config = large_result_config
                        _RESULT_BACKEND_CACHE[func_key] = "large"
                    else:
                        logger.debug(f"Using small result config for {func_key} (size: {size} bytes)")
                        active_config = small_result_config
                        _RESULT_BACKEND_CACHE[func_key] = "small"

                except (TypeError, AttributeError):
                    # If we can't determine size, default to small result config
                    logger.debug(f"Could not determine size for {func_key}, using small result config")
                    _RESULT_BACKEND_CACHE[func_key] = "small"

            return result

        return cast(F, wrapper)

    return decorator


def smart_cache(
    config: Optional[CacheConfig] = None,
    analyze_every_call: bool = False,
) -> Callable[[F], F]:
    """
    Decorator that automatically selects the most appropriate cache backend.

    This decorator uses the backend_selector module to determine the most
    appropriate backend based on the function's return value.

    Args:
        config: Base cache configuration (optional)
        analyze_every_call: Whether to analyze every call or just the first one

    Returns:
        Callable: Decorated function with smart caching
    """
    # Initialize with default configuration if not provided
    if config is None:
        config = CacheConfig()

    def decorator(func: F) -> F:
        # Generate a unique key for this function
        func_key = f"{func.__module__}.{func.__qualname__}"

        # Dictionary to store backend configurations for different result types
        backend_configs: Dict[str, CacheConfig] = {}

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            # Execute the function to get the result
            result = func(*args, **kwargs)

            # Determine the appropriate backend based on the result
            backend = detect_result_type(result)

            # If we've already created a configuration for this backend, use it
            if not analyze_every_call and backend in backend_configs:
                cached_func = cache(config=backend_configs[backend])(func)
                return cached_func(*args, **kwargs)

            # Create a new configuration for this backend
            backend_config = CacheConfig(
                preferred_engine=backend, **{k: v for k, v in config.model_dump().items() if v is not None}
            )

            # Store the configuration for future use
            backend_configs[backend] = backend_config

            # Apply the cache with the selected backend
            cached_func = cache(config=backend_config)(func)
            return cached_func(*args, **kwargs)

        return cast(F, wrapper)

    return decorator
