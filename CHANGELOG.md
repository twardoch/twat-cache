# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- (Nothing yet)

### Changed
- Refactored `CacheEngineManager` (`src/twat_cache/engines/manager.py`):
    - Now instantiates and returns cache engine instances via `create_engine_instance` method based on `CacheConfig`.
    - `get_engine_manager()` now returns a singleton instance.
    - Selection logic prioritizes `config.preferred_engine` and defaults to "functools".
    - Renamed `get_engine` to `get_engine_class`.
    - Renamed `get_available_engines` to `list_available_engines`.
- Simplified decorators in `src/twat_cache/decorators.py`:
    - `ucache` now uses `CacheEngineManager` and accepts configuration parameters directly.
    - `acache` now strictly uses `AioCacheEngine` (via `CacheEngineManager`) or raises `EngineNotAvailableError`.
- Updated `src/twat_cache/__init__.py` for new decorator structure and removed old exports.

###Removed
- `src/twat_cache/backend_selector.py` and `src/twat_cache/hybrid_cache.py` modules and their functionalities.
- Decorators `mcache`, `bcache`, `fcache` from `src/twat_cache/decorators.py`.
- Internal helper functions (`_get_available_backends`, `_select_best_backend`, `_create_engine`) from `decorators.py`.
- Global `HAS_*` constants for backend availability from `decorators.py`.
- Imports and `__all__` entries related to `backend_selector`, `hybrid_cache`, `mcache`, `bcache`, `fcache` from `src/twat_cache/__init__.py`.
- Deleted redundant `src/twat_cache/engines/functools.py` (keeping `functools_engine.py`).
- Removed the concrete `CacheEngine` class from `src/twat_cache/engines/base.py` as it was redundant.
- **Redis Support:**
    - Deleted `src/twat_cache/engines/redis.py`.
    - Removed Redis engine registration from `CacheEngineManager`.
    - Removed Redis-specific fields from `CacheConfig`.
    - Deleted `tests/test_redis_cache.py`.

### Fixed
- Standardized TTL handling in `DiskCacheEngine` to reliably use `diskcache` library's own `expire` mechanism, simplifying internal logic.
- Commented out failing assertion in `test_safe_key_serializer` in `tests/test_exceptions.py` as per user feedback.
- Corrected `get()` and `set()` methods in `FunctoolsCacheEngine` to use its internal dict-based cache logic instead of incorrectly attempting to call LRU-cache specific methods.
- Updated `context.py` (`engine_context`, `CacheContext`, `get_or_create_engine`) to use the new `CacheEngineManager.create_engine_instance()` method, resolving `AttributeError` for `select_engine` and `get_engine`.
- Made `AioCacheEngine` backend selection more robust by ensuring conditional imports of `RedisCache` and `MemcachedCache` are correctly guarded and fallback to `SimpleMemoryCache` is properly structured.
- Ensured `CacheToolsEngine` and `CacheBoxEngine` only pass `ttl` argument to underlying cache constructors if the specific cache type supports it, preventing TypeErrors.
