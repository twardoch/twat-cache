"""
Integration tests for twat-cache.
These tests verify end-to-end functionality and real-world usage scenarios.
"""
# this_file: tests/test_integration.py

import pytest
import asyncio
import tempfile
import shutil
import time
import threading
from pathlib import Path
from typing import Dict, List, Any, Optional

from twat_cache import ucache, acache
from twat_cache.context import CacheContext
from twat_cache.cache import clear_cache, get_stats
from twat_cache.config import create_cache_config


class TestRealWorldScenarios:
    """Test real-world usage scenarios."""
    
    def test_web_api_simulation(self):
        """Simulate web API response caching."""
        
        # Simulate API call latency
        api_calls = 0
        
        @ucache(ttl=60, maxsize=100)
        def fetch_user_data(user_id: int) -> Dict[str, Any]:
            nonlocal api_calls
            api_calls += 1
            # Simulate API call delay
            time.sleep(0.01)
            return {
                'id': user_id,
                'name': f'User {user_id}',
                'email': f'user{user_id}@example.com',
                'created_at': time.time()
            }
        
        # Simulate multiple requests for same users
        users = [1, 2, 3, 1, 2, 4, 1, 3, 5, 2]
        results = []
        
        for user_id in users:
            result = fetch_user_data(user_id)
            results.append(result)
        
        # Should have made only 5 API calls (unique users)
        assert api_calls == 5
        assert len(results) == 10
        
        # Verify cached data consistency
        user_1_results = [r for r in results if r['id'] == 1]
        assert len(user_1_results) == 3
        assert all(r['created_at'] == user_1_results[0]['created_at'] for r in user_1_results)
    
    def test_database_query_caching(self):
        """Simulate database query result caching."""
        
        query_count = 0
        
        @ucache(folder_name="db_cache", ttl=300)
        def execute_query(query: str, params: tuple = ()) -> List[Dict[str, Any]]:
            nonlocal query_count
            query_count += 1
            # Simulate database query delay
            time.sleep(0.02)
            
            # Simulate different query results
            if "users" in query:
                return [{'id': i, 'name': f'User {i}'} for i in range(len(params) or 10)]
            elif "orders" in query:
                return [{'id': i, 'total': i * 100} for i in range(len(params) or 5)]
            else:
                return []
        
        # Multiple queries with some repetition
        queries = [
            ("SELECT * FROM users WHERE active = ?", (True,)),
            ("SELECT * FROM orders WHERE user_id = ?", (1,)),
            ("SELECT * FROM users WHERE active = ?", (True,)),  # Duplicate
            ("SELECT * FROM orders WHERE user_id = ?", (2,)),
            ("SELECT * FROM users WHERE active = ?", (True,)),  # Duplicate
        ]
        
        results = []
        for query, params in queries:
            result = execute_query(query, params)
            results.append(result)
        
        # Should have made only 3 unique queries
        assert query_count == 3
        assert len(results) == 5
    
    def test_file_processing_pipeline(self):
        """Test file processing with caching."""
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create test files
            test_files = []
            for i in range(5):
                file_path = temp_path / f"test_file_{i}.txt"
                file_path.write_text(f"Content of file {i}\n" * 100)
                test_files.append(file_path)
            
            processing_count = 0
            
            @ucache(folder_name="file_cache", maxsize=10)
            def process_file(file_path: Path) -> Dict[str, Any]:
                nonlocal processing_count
                processing_count += 1
                
                # Simulate file processing delay
                time.sleep(0.01)
                
                content = file_path.read_text()
                return {
                    'path': str(file_path),
                    'lines': len(content.splitlines()),
                    'chars': len(content),
                    'processed_at': time.time()
                }
            
            # Process files multiple times
            results = []
            for _ in range(3):  # 3 iterations
                for file_path in test_files:
                    result = process_file(file_path)
                    results.append(result)
            
            # Should have processed each file only once
            assert processing_count == 5
            assert len(results) == 15  # 3 iterations * 5 files
    
    @pytest.mark.asyncio
    async def test_async_web_scraping(self):
        """Test async web scraping with caching."""
        
        scrape_count = 0
        
        @acache(ttl=60, maxsize=50)
        async def scrape_page(url: str) -> Dict[str, Any]:
            nonlocal scrape_count
            scrape_count += 1
            
            # Simulate HTTP request delay
            await asyncio.sleep(0.01)
            
            return {
                'url': url,
                'title': f'Title for {url}',
                'content_length': len(url) * 100,
                'scraped_at': time.time()
            }
        
        # Simulate concurrent scraping with some URL repetition
        urls = [
            'https://example.com',
            'https://example.org',
            'https://example.net',
            'https://example.com',  # Duplicate
            'https://example.org',  # Duplicate
        ]
        
        # Process URLs concurrently
        tasks = [scrape_page(url) for url in urls]
        results = await asyncio.gather(*tasks)
        
        # Should have scraped only unique URLs
        assert scrape_count == 3
        assert len(results) == 5
    
    def test_machine_learning_model_caching(self):
        """Test ML model prediction caching."""
        
        model_calls = 0
        
        @ucache(folder_name="ml_cache", maxsize=1000)
        def predict(features: tuple) -> Dict[str, Any]:
            nonlocal model_calls
            model_calls += 1
            
            # Simulate model inference delay
            time.sleep(0.005)
            
            # Simple mock prediction
            score = sum(features) / len(features)
            return {
                'features': features,
                'prediction': score > 0.5,
                'confidence': abs(score - 0.5) * 2,
                'model_version': '1.0.0'
            }
        
        # Simulate batch prediction with some duplicate feature sets
        feature_sets = [
            (0.1, 0.2, 0.3),
            (0.8, 0.9, 0.7),
            (0.1, 0.2, 0.3),  # Duplicate
            (0.5, 0.6, 0.4),
            (0.8, 0.9, 0.7),  # Duplicate
            (0.2, 0.3, 0.1),
        ]
        
        predictions = []
        for features in feature_sets:
            prediction = predict(features)
            predictions.append(prediction)
        
        # Should have made only 4 unique predictions
        assert model_calls == 4
        assert len(predictions) == 6
    
    def test_concurrent_cache_access(self):
        """Test concurrent access to cache from multiple threads."""
        
        computation_count = 0
        lock = threading.Lock()
        
        @ucache(maxsize=100)
        def expensive_computation(value: int) -> int:
            nonlocal computation_count
            with lock:
                computation_count += 1
            
            # Simulate computation delay
            time.sleep(0.01)
            return value * value
        
        def worker(results: List[int], worker_id: int):
            """Worker function for threading test."""
            for i in range(20):
                # Use overlapping values to test cache hits
                value = (worker_id * 10 + i) % 30
                result = expensive_computation(value)
                results.append(result)
        
        # Run multiple threads concurrently
        threads = []
        results = []
        
        for i in range(5):
            thread = threading.Thread(target=worker, args=(results, i))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # Should have fewer computations than total requests due to caching
        assert computation_count <= 30  # Max unique values
        assert len(results) == 100  # 5 threads * 20 operations
    
    def test_cache_persistence(self):
        """Test cache persistence across different cache instances."""
        
        with tempfile.TemporaryDirectory() as temp_dir:
            cache_folder = Path(temp_dir) / "persistence_test"
            
            # First cache instance
            computation_count_1 = 0
            
            @ucache(folder_name=str(cache_folder), maxsize=100)
            def compute_value_1(x: int) -> int:
                nonlocal computation_count_1
                computation_count_1 += 1
                time.sleep(0.01)
                return x * x
            
            # Compute some values
            values_1 = [compute_value_1(i) for i in range(10)]
            assert computation_count_1 == 10
            
            # Clear in-memory cache but keep disk cache
            clear_cache()
            
            # Second cache instance (should reuse disk cache)
            computation_count_2 = 0
            
            @ucache(folder_name=str(cache_folder), maxsize=100)
            def compute_value_2(x: int) -> int:
                nonlocal computation_count_2
                computation_count_2 += 1
                time.sleep(0.01)
                return x * x
            
            # Compute same values (should hit disk cache)
            values_2 = [compute_value_2(i) for i in range(10)]
            
            # Should not have recomputed (disk cache hit)
            assert computation_count_2 == 0
            assert values_1 == values_2
    
    def test_ttl_expiration(self):
        """Test TTL expiration functionality."""
        
        computation_count = 0
        
        @ucache(ttl=0.1, maxsize=100)  # 100ms TTL
        def time_sensitive_computation(x: int) -> Dict[str, Any]:
            nonlocal computation_count
            computation_count += 1
            return {
                'value': x * 2,
                'computed_at': time.time()
            }
        
        # First computation
        result1 = time_sensitive_computation(5)
        assert computation_count == 1
        
        # Second computation (should hit cache)
        result2 = time_sensitive_computation(5)
        assert computation_count == 1
        assert result1['computed_at'] == result2['computed_at']
        
        # Wait for TTL expiration
        time.sleep(0.15)
        
        # Third computation (should recompute due to TTL)
        result3 = time_sensitive_computation(5)
        assert computation_count == 2
        assert result3['computed_at'] > result1['computed_at']
    
    def test_cache_statistics(self):
        """Test cache statistics functionality."""
        
        @ucache(maxsize=100)
        def test_function(x: int) -> int:
            return x * 2
        
        # Clear existing statistics
        clear_cache()
        
        # Generate cache hits and misses
        for i in range(10):
            test_function(i)  # Cache misses
        
        for i in range(5):
            test_function(i)  # Cache hits
        
        # Get statistics
        stats = get_stats()
        
        # Should have some statistics
        assert len(stats) > 0
        
        # Check that we have hit/miss information
        total_hits = sum(stat.get('hits', 0) for stat in stats.values())
        total_misses = sum(stat.get('misses', 0) for stat in stats.values())
        
        assert total_hits >= 5  # At least 5 hits
        assert total_misses >= 10  # At least 10 misses


class TestErrorHandling:
    """Test error handling and edge cases."""
    
    def test_cache_with_exceptions(self):
        """Test cache behavior when function raises exceptions."""
        
        call_count = 0
        
        @ucache(maxsize=100)
        def error_prone_function(x: int) -> int:
            nonlocal call_count
            call_count += 1
            
            if x < 0:
                raise ValueError("Negative value not allowed")
            elif x == 0:
                raise ZeroDivisionError("Division by zero")
            else:
                return x * 2
        
        # Test successful calls
        assert error_prone_function(5) == 10
        assert call_count == 1
        
        # Test cached successful call
        assert error_prone_function(5) == 10
        assert call_count == 1  # Should not increment
        
        # Test exception (should not be cached)
        with pytest.raises(ValueError):
            error_prone_function(-1)
        assert call_count == 2
        
        # Test same exception again (should call function again)
        with pytest.raises(ValueError):
            error_prone_function(-1)
        assert call_count == 3
    
    def test_cache_with_unhashable_arguments(self):
        """Test cache with unhashable arguments."""
        
        call_count = 0
        
        @ucache(maxsize=100)
        def process_data(data: List[int]) -> int:
            nonlocal call_count
            call_count += 1
            return sum(data)
        
        # Test with list (should work with serialization)
        result1 = process_data([1, 2, 3])
        assert result1 == 6
        assert call_count == 1
        
        # Test with same list (should hit cache)
        result2 = process_data([1, 2, 3])
        assert result2 == 6
        assert call_count == 1
        
        # Test with different list
        result3 = process_data([4, 5, 6])
        assert result3 == 15
        assert call_count == 2
    
    def test_cache_context_error_handling(self):
        """Test error handling in cache context."""
        
        with tempfile.TemporaryDirectory() as temp_dir:
            cache_folder = Path(temp_dir) / "error_test"
            
            # Test with valid engine
            with CacheContext(engine_name="functools", maxsize=100) as cache:
                cache.set("key1", "value1")
                assert cache.get("key1") == "value1"
            
            # Test with invalid engine (should fall back or raise appropriate error)
            try:
                with CacheContext(engine_name="nonexistent_engine") as cache:
                    cache.set("key2", "value2")
            except Exception as e:
                # Should raise a meaningful error
                assert "engine" in str(e).lower() or "not found" in str(e).lower()
    
    def test_cache_memory_limits(self):
        """Test cache behavior with memory limits."""
        
        call_count = 0
        
        @ucache(maxsize=5)  # Small cache size
        def create_large_data(x: int) -> List[int]:
            nonlocal call_count
            call_count += 1
            return list(range(x * 100))
        
        # Fill cache beyond capacity
        results = []
        for i in range(10):
            result = create_large_data(i)
            results.append(len(result))
        
        # Should have called function for each unique input
        assert call_count == 10
        
        # Test cache eviction by requesting early items
        early_result = create_large_data(0)
        # This might be a cache miss due to eviction
        assert len(early_result) == 0
    
    @pytest.mark.asyncio
    async def test_async_cache_error_handling(self):
        """Test async cache error handling."""
        
        call_count = 0
        
        @acache(maxsize=100)
        async def async_error_function(x: int) -> int:
            nonlocal call_count
            call_count += 1
            
            if x < 0:
                raise ValueError("Negative value")
            
            await asyncio.sleep(0.001)
            return x * 2
        
        # Test successful call
        result = await async_error_function(5)
        assert result == 10
        assert call_count == 1
        
        # Test cached call
        result = await async_error_function(5)
        assert result == 10
        assert call_count == 1
        
        # Test exception
        with pytest.raises(ValueError):
            await async_error_function(-1)
        assert call_count == 2
        
        # Test same exception again
        with pytest.raises(ValueError):
            await async_error_function(-1)
        assert call_count == 3  # Should not cache exceptions