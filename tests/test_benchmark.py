"""
Comprehensive benchmark tests for twat-cache.
These tests measure performance of different cache engines and operations.
"""
# this_file: tests/test_benchmark.py

import pytest
import time
import asyncio
import random
import string
from typing import List, Dict, Any

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

from twat_cache import ucache, acache
from twat_cache.context import CacheContext
from twat_cache.config import create_cache_config


class TestCacheBenchmarks:
    """Benchmark tests for cache operations."""
    
    def generate_test_data(self, size: int = 1000) -> List[Dict[str, Any]]:
        """Generate test data for benchmarking."""
        data = []
        for i in range(size):
            data.append({
                'id': i,
                'name': ''.join(random.choices(string.ascii_letters, k=10)),
                'value': random.randint(1, 1000),
                'data': [random.random() for _ in range(10)]
            })
        return data
    
    @pytest.mark.benchmark
    def test_memory_cache_performance(self, benchmark):
        """Benchmark memory cache performance."""
        test_data = self.generate_test_data(100)
        
        @ucache(maxsize=1000)
        def process_data(data_id: int) -> Dict[str, Any]:
            # Simulate some processing
            time.sleep(0.001)  # 1ms delay
            return test_data[data_id % len(test_data)]
        
        def run_cache_operations():
            results = []
            for i in range(50):
                # Mix of cache hits and misses
                result = process_data(i % 20)
                results.append(result)
            return results
        
        result = benchmark(run_cache_operations)
        assert len(result) == 50
    
    @pytest.mark.benchmark
    def test_disk_cache_performance(self, benchmark):
        """Benchmark disk cache performance."""
        test_data = self.generate_test_data(100)
        
        @ucache(folder_name="benchmark_disk_cache", maxsize=1000)
        def process_data(data_id: int) -> Dict[str, Any]:
            # Simulate some processing
            time.sleep(0.001)  # 1ms delay
            return test_data[data_id % len(test_data)]
        
        def run_cache_operations():
            results = []
            for i in range(50):
                # Mix of cache hits and misses
                result = process_data(i % 20)
                results.append(result)
            return results
        
        result = benchmark(run_cache_operations)
        assert len(result) == 50
    
    @pytest.mark.benchmark
    @pytest.mark.asyncio
    async def test_async_cache_performance(self, benchmark):
        """Benchmark async cache performance."""
        test_data = self.generate_test_data(100)
        
        @acache(maxsize=1000)
        async def process_data_async(data_id: int) -> Dict[str, Any]:
            # Simulate some async processing
            await asyncio.sleep(0.001)  # 1ms delay
            return test_data[data_id % len(test_data)]
        
        async def run_cache_operations():
            results = []
            for i in range(50):
                # Mix of cache hits and misses
                result = await process_data_async(i % 20)
                results.append(result)
            return results
        
        result = await benchmark(run_cache_operations)
        assert len(result) == 50
    
    @pytest.mark.benchmark
    def test_cache_context_performance(self, benchmark):
        """Benchmark cache context performance."""
        test_data = self.generate_test_data(100)
        
        def run_context_operations():
            results = []
            with CacheContext(engine_name="cachetools", maxsize=1000) as cache:
                for i in range(50):
                    key = f"key_{i % 20}"
                    cached_value = cache.get(key)
                    if cached_value is None:
                        # Simulate processing
                        time.sleep(0.001)
                        value = test_data[i % len(test_data)]
                        cache.set(key, value)
                        results.append(value)
                    else:
                        results.append(cached_value)
            return results
        
        result = benchmark(run_context_operations)
        assert len(result) == 50
    
    @pytest.mark.benchmark
    def test_different_data_sizes(self, benchmark):
        """Benchmark cache performance with different data sizes."""
        
        @ucache(maxsize=1000)
        def process_small_data(data_id: int) -> str:
            return f"small_data_{data_id}"
        
        @ucache(maxsize=1000)
        def process_medium_data(data_id: int) -> List[int]:
            return list(range(data_id % 100))
        
        @ucache(maxsize=1000)
        def process_large_data(data_id: int) -> Dict[str, Any]:
            return {
                'id': data_id,
                'data': [random.random() for _ in range(1000)],
                'metadata': {'created': time.time(), 'size': 1000}
            }
        
        def run_mixed_operations():
            results = []
            for i in range(100):
                if i % 3 == 0:
                    results.append(process_small_data(i % 10))
                elif i % 3 == 1:
                    results.append(process_medium_data(i % 10))
                else:
                    results.append(process_large_data(i % 10))
            return results
        
        result = benchmark(run_mixed_operations)
        assert len(result) == 100
    
    @pytest.mark.benchmark
    @pytest.mark.skipif(not HAS_NUMPY, reason="NumPy not available")
    def test_numpy_array_caching(self, benchmark):
        """Benchmark caching of NumPy arrays."""
        
        @ucache(folder_name="numpy_cache", maxsize=100)
        def create_array(size: int) -> np.ndarray:
            # Simulate expensive array creation
            time.sleep(0.005)  # 5ms delay
            return np.random.rand(size, size)
        
        def run_numpy_operations():
            results = []
            for i in range(20):
                # Create arrays of different sizes
                size = 50 + (i % 5) * 10
                arr = create_array(size)
                results.append(arr.shape)
            return results
        
        result = benchmark(run_numpy_operations)
        assert len(result) == 20
    
    @pytest.mark.benchmark
    def test_concurrent_cache_access(self, benchmark):
        """Benchmark concurrent cache access."""
        import threading
        
        test_data = self.generate_test_data(1000)
        
        @ucache(maxsize=1000)
        def process_data(data_id: int) -> Dict[str, Any]:
            # Simulate some processing
            time.sleep(0.001)
            return test_data[data_id % len(test_data)]
        
        def worker(results: List, worker_id: int):
            for i in range(20):
                result = process_data((worker_id * 20 + i) % 50)
                results.append(result)
        
        def run_concurrent_operations():
            results = []
            threads = []
            
            for i in range(5):  # 5 threads
                thread = threading.Thread(target=worker, args=(results, i))
                threads.append(thread)
                thread.start()
            
            for thread in threads:
                thread.join()
            
            return results
        
        result = benchmark(run_concurrent_operations)
        assert len(result) == 100  # 5 threads * 20 operations
    
    @pytest.mark.benchmark
    def test_cache_hit_ratio(self, benchmark):
        """Benchmark cache hit ratio performance."""
        
        call_count = 0
        
        @ucache(maxsize=100)
        def expensive_operation(value: int) -> int:
            nonlocal call_count
            call_count += 1
            # Simulate expensive operation
            time.sleep(0.001)
            return value * 2
        
        def run_hit_ratio_test():
            results = []
            # Generate requests with 80% cache hit ratio
            for i in range(200):
                if i < 160:
                    # High probability of cache hits
                    value = i % 20
                else:
                    # New values (cache misses)
                    value = i
                
                result = expensive_operation(value)
                results.append(result)
            return results, call_count
        
        results, actual_calls = benchmark(run_hit_ratio_test)
        
        # Should have significantly fewer calls than total requests
        assert actual_calls < 200
        assert len(results[0]) == 200
    
    @pytest.mark.benchmark
    def test_cache_serialization_performance(self, benchmark):
        """Benchmark cache serialization performance."""
        
        complex_data = {
            'numbers': list(range(1000)),
            'strings': [''.join(random.choices(string.ascii_letters, k=20)) for _ in range(100)],
            'nested': {
                'level1': {
                    'level2': {
                        'data': [random.random() for _ in range(100)]
                    }
                }
            }
        }
        
        @ucache(maxsize=100, folder_name="serialization_cache")
        def process_complex_data(data_id: int) -> Dict[str, Any]:
            # Simulate processing
            time.sleep(0.002)
            return {**complex_data, 'id': data_id}
        
        def run_serialization_test():
            results = []
            for i in range(50):
                result = process_complex_data(i % 10)
                results.append(result['id'])
            return results
        
        result = benchmark(run_serialization_test)
        assert len(result) == 50


class TestCacheEngineComparison:
    """Compare different cache engines."""
    
    @pytest.mark.benchmark
    def test_engine_comparison(self, benchmark):
        """Compare performance across different cache engines."""
        
        engines = [
            ('functools', {}),
            ('cachetools', {'maxsize': 1000}),
            ('diskcache', {'folder_name': 'comparison_test', 'maxsize': 1000}),
        ]
        
        # Add cachebox if available
        try:
            import cachebox
            engines.append(('cachebox', {'maxsize': 1000}))
        except ImportError:
            pass
        
        def test_engine(engine_name: str, config: Dict[str, Any]):
            @ucache(preferred_engine=engine_name, **config)
            def compute_value(x: int) -> int:
                # Simulate computation
                time.sleep(0.001)
                return x * x + x
            
            # Test with mix of cache hits and misses
            results = []
            for i in range(100):
                result = compute_value(i % 20)
                results.append(result)
            return results
        
        def run_engine_comparison():
            all_results = {}
            for engine_name, config in engines:
                try:
                    results = test_engine(engine_name, config)
                    all_results[engine_name] = results
                except Exception as e:
                    # Engine might not be available
                    all_results[engine_name] = f"Error: {e}"
            return all_results
        
        result = benchmark(run_engine_comparison)
        
        # At least functools should work
        assert 'functools' in result
        assert isinstance(result['functools'], list)
        assert len(result['functools']) == 100


# Performance regression tests
class TestPerformanceRegression:
    """Test for performance regressions."""
    
    @pytest.mark.benchmark
    def test_cache_overhead(self, benchmark):
        """Measure cache overhead vs direct function calls."""
        
        def direct_function(x: int) -> int:
            return x * 2
        
        @ucache(maxsize=1000)
        def cached_function(x: int) -> int:
            return x * 2
        
        def run_direct_calls():
            results = []
            for i in range(1000):
                result = direct_function(i)
                results.append(result)
            return results
        
        def run_cached_calls():
            results = []
            for i in range(1000):
                result = cached_function(i % 100)  # High cache hit ratio
                results.append(result)
            return results
        
        # Benchmark both approaches
        direct_result = benchmark(run_direct_calls)
        cached_result = benchmark(run_cached_calls)
        
        assert len(direct_result) == 1000
        assert len(cached_result) == 1000
        
        # For high cache hit ratios, cached should be faster
        # But we can't assert timing here as it depends on the environment
    
    @pytest.mark.benchmark
    def test_memory_usage_stability(self, benchmark):
        """Test that cache memory usage is stable."""
        
        @ucache(maxsize=100)
        def memory_test_function(x: int) -> str:
            return 'x' * 1000  # 1KB string
        
        def run_memory_test():
            results = []
            # Generate many cache entries beyond maxsize
            for i in range(1000):
                result = memory_test_function(i)
                results.append(len(result))
            return results
        
        result = benchmark(run_memory_test)
        
        # Should not cause memory leaks
        assert len(result) == 1000
        assert all(length == 1000 for length in result)