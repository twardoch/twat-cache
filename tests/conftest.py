"""
Pytest configuration and fixtures for twat-cache tests.
"""
# this_file: tests/conftest.py

import pytest
import tempfile
import shutil
from pathlib import Path
from typing import Generator, Any

from twat_cache.cache import clear_cache


@pytest.fixture(autouse=True)
def cleanup_caches():
    """Automatically clean up caches after each test."""
    yield
    clear_cache()


@pytest.fixture
def temp_cache_dir() -> Generator[Path, None, None]:
    """Provide a temporary directory for cache testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def sample_data():
    """Provide sample data for testing."""
    return {
        'users': [
            {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
            {'id': 2, 'name': 'Bob', 'email': 'bob@example.com'},
            {'id': 3, 'name': 'Charlie', 'email': 'charlie@example.com'},
        ],
        'orders': [
            {'id': 1, 'user_id': 1, 'total': 100.0},
            {'id': 2, 'user_id': 2, 'total': 250.0},
            {'id': 3, 'user_id': 1, 'total': 50.0},
        ]
    }


@pytest.fixture
def mock_expensive_function():
    """Mock expensive function for testing."""
    call_count = 0
    
    def expensive_function(x: int) -> int:
        nonlocal call_count
        call_count += 1
        # Simulate expensive computation
        import time
        time.sleep(0.001)
        return x * x
    
    expensive_function.call_count = lambda: call_count
    expensive_function.reset_count = lambda: setattr(expensive_function, 'call_count', lambda: 0)
    
    return expensive_function


@pytest.fixture
async def async_mock_function():
    """Mock async function for testing."""
    call_count = 0
    
    async def async_function(x: int) -> int:
        nonlocal call_count
        call_count += 1
        # Simulate async expensive computation
        import asyncio
        await asyncio.sleep(0.001)
        return x * 2
    
    async_function.call_count = lambda: call_count
    async_function.reset_count = lambda: setattr(async_function, 'call_count', lambda: 0)
    
    return async_function


@pytest.fixture
def benchmark_data():
    """Provide data for benchmark tests."""
    import random
    import string
    
    def generate_data(size: int = 1000):
        return [
            {
                'id': i,
                'name': ''.join(random.choices(string.ascii_letters, k=10)),
                'value': random.randint(1, 1000),
                'data': [random.random() for _ in range(10)]
            }
            for i in range(size)
        ]
    
    return generate_data


# Test markers
def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line("markers", "slow: marks tests as slow")
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "benchmark: marks tests as benchmark tests")
    config.addinivalue_line("markers", "requires_redis: marks tests that require Redis")
    config.addinivalue_line("markers", "requires_numpy: marks tests that require NumPy")


# Skip tests based on available dependencies
def pytest_collection_modifyitems(config, items):
    """Modify test collection to skip tests based on dependencies."""
    
    # Check for optional dependencies
    try:
        import redis
        has_redis = True
    except ImportError:
        has_redis = False
    
    try:
        import numpy
        has_numpy = True
    except ImportError:
        has_numpy = False
    
    try:
        import cachebox
        has_cachebox = True
    except ImportError:
        has_cachebox = False
    
    try:
        import aiocache
        has_aiocache = True
    except ImportError:
        has_aiocache = False
    
    # Apply skips
    for item in items:
        if "requires_redis" in item.keywords and not has_redis:
            item.add_marker(pytest.mark.skip(reason="Redis not available"))
        
        if "requires_numpy" in item.keywords and not has_numpy:
            item.add_marker(pytest.mark.skip(reason="NumPy not available"))
        
        if "requires_cachebox" in item.keywords and not has_cachebox:
            item.add_marker(pytest.mark.skip(reason="CacheBox not available"))
        
        if "requires_aiocache" in item.keywords and not has_aiocache:
            item.add_marker(pytest.mark.skip(reason="AioCache not available"))


# Custom pytest hooks for better test reporting
@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    """Setup hook for each test."""
    # Clear caches before each test
    clear_cache()


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_teardown(item):
    """Teardown hook for each test."""
    # Clear caches after each test
    clear_cache()


# Performance testing utilities
@pytest.fixture
def performance_timer():
    """Utility for timing operations in tests."""
    import time
    
    class Timer:
        def __init__(self):
            self.start_time = None
            self.end_time = None
        
        def __enter__(self):
            self.start_time = time.time()
            return self
        
        def __exit__(self, *args):
            self.end_time = time.time()
        
        @property
        def elapsed(self):
            if self.start_time and self.end_time:
                return self.end_time - self.start_time
            return None
    
    return Timer


# Mock data generators
@pytest.fixture
def data_generator():
    """Generate various types of test data."""
    import random
    import string
    
    class DataGenerator:
        @staticmethod
        def random_string(length: int = 10) -> str:
            return ''.join(random.choices(string.ascii_letters, k=length))
        
        @staticmethod
        def random_dict(size: int = 5) -> dict:
            return {
                DataGenerator.random_string(5): random.randint(1, 100)
                for _ in range(size)
            }
        
        @staticmethod
        def random_list(size: int = 10) -> list:
            return [random.randint(1, 1000) for _ in range(size)]
        
        @staticmethod
        def nested_data(depth: int = 3) -> dict:
            if depth == 0:
                return DataGenerator.random_dict()
            
            return {
                'level': depth,
                'data': DataGenerator.random_dict(),
                'nested': DataGenerator.nested_data(depth - 1)
            }
    
    return DataGenerator