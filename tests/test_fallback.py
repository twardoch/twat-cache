# this_file: tests/test_fallback.py
"""Tests for backend selection and fallback behaviour.

These tests verify observable outcomes — correct return values, caching hits —
without mocking internal symbols that may change.  Engine-specific tests live
in test_engines.py; here we test the public decorators ``ucache`` and ``acache``.
"""

import asyncio

import pytest

from twat_cache.decorators import acache, ucache

from tests.test_constants import (
    CACHE_SIZE,
    EXPECTED_CALLS_SINGLE,
    SQUARE_INPUT,
    SQUARE_RESULT,
)


@pytest.mark.asyncio
async def test_async_cache_fallback() -> None:
    """Test that acache returns correct results (uses aiocache if available)."""
    pytest.importorskip("aiocache")

    call_count = 0

    @acache(maxsize=CACHE_SIZE)
    async def test_func(x: int) -> int:
        nonlocal call_count
        call_count += 1
        await asyncio.sleep(0)
        return x * x

    result = await test_func(SQUARE_INPUT)
    assert result == SQUARE_RESULT
    assert call_count == EXPECTED_CALLS_SINGLE


def test_universal_cache_fallback() -> None:
    """Test that ucache falls back to an available engine when preferred is unknown."""
    call_count = 0

    # "nonexistent_engine" is not registered; ucache must select an available fallback.
    @ucache(maxsize=CACHE_SIZE, preferred_engine="nonexistent_engine")
    def test_func(x: int) -> int:
        nonlocal call_count
        call_count += 1
        return x * x

    result = test_func(SQUARE_INPUT)
    assert result == SQUARE_RESULT
    assert call_count == EXPECTED_CALLS_SINGLE
