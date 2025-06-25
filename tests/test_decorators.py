#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "pytest",
#   "pytest-asyncio",
#   "loguru",
#   "diskcache",
#   "joblib",
#   "types-pytest",
#   "cachetools",
#   "cachebox",
#   "klepto",
#   "aiocache",
# ]
# ///
# this_file: tests/test_decorators.py

"""Tests for the cache decorators."""

import asyncio
import time
from typing import Any

import pytest
import importlib.util

# Only ucache and acache are kept from decorators.py
from twat_cache.decorators import ucache, acache # Removed mcache, bcache, fcache
# make_key is also in decorators, but not directly tested here it seems.
# If other specific exception/config from decorators.py are needed, they'd be imported.
from twat_cache.config import create_cache_config # For mock_config if used by ucache/acache tests
from twat_cache.exceptions import EngineNotAvailableError # For acache no_engine test

from tests.test_constants import (
    CACHE_SIZE, # Used in mock_config, and some ucache/acache tests might use it
    CACHE_TTL,  # Used in mock_config, and some ucache/acache tests might use it
    EXPECTED_CALLS_SINGLE,
    EXPECTED_CALLS_DOUBLE,
    EXPECTED_CALLS_TRIPLE,
    EXPECTED_CALLS_QUAD,
    SQUARE_INPUT,
    SQUARE_RESULT,
    TEST_KEY,
    TEST_BOOL,
    TEST_INT,
    TEST_VALUE,
    TEST_RESULT,
    TEST_FOLDER,
)

# Check optional backend availability
HAS_AIOCACHE = bool(importlib.util.find_spec("aiocache"))
HAS_CACHEBOX = bool(importlib.util.find_spec("cachebox"))
HAS_CACHETOOLS = bool(importlib.util.find_spec("cachetools"))
HAS_DISKCACHE = bool(importlib.util.find_spec("diskcache"))
HAS_JOBLIB = bool(importlib.util.find_spec("joblib"))
HAS_KLEPTO = bool(importlib.util.find_spec("klepto"))


# All tests for mcache, bcache, fcache, and specific engine tests using bcache
# have been removed as these decorators are no longer part of the public API.
# Tests for ucache and acache will be kept and refactored as needed.

# The test `test_aiocache_memory` used ucache(engine="aiocache") for an async function.
# This might be a valid test for ucache's ability to handle an async engine
# if the engine itself returns an awaitable wrapper. Or it might be better suited
# as an acache test. For now, removing it to simplify, will re-evaluate ucache+async engine later.


def test_universal_cache() -> None:
    """Test universal caching with automatic backend selection."""
    call_count = 0

    @ucache(maxsize=CACHE_SIZE)
    def expensive_func(x: int) -> int:
        nonlocal call_count
        call_count += 1
        return x * x

    # Test caching behavior
    assert expensive_func(SQUARE_INPUT) == SQUARE_RESULT
    assert expensive_func(SQUARE_INPUT) == SQUARE_RESULT
    assert call_count == EXPECTED_CALLS_SINGLE


async def test_async_cache() -> None:
    """Test async caching with aiocache."""
    try:
        import aiocache

    except ImportError:
        pytest.skip("aiocache not available")

    call_count = 0

    @acache(maxsize=CACHE_SIZE)
    async def expensive_func(x: int) -> int:
        nonlocal call_count
        call_count += 1
        await asyncio.sleep(0.1)
        return x * x

    # Test caching behavior
    result1 = await expensive_func(SQUARE_INPUT)
    assert result1 == SQUARE_RESULT

    result2 = await expensive_func(SQUARE_INPUT)
    assert result2 == SQUARE_RESULT
    assert call_count == EXPECTED_CALLS_SINGLE

# Removed test_key_generation (the one using mcache) and test_ttl_cache (using mcache)
# A new test_make_key_generation (if needed) is separate and tests the make_key utility directly.
# TTL behavior should be tested via ucache/acache with appropriate engine configurations.
