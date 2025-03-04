---
this_file: CHANGELOG.md
---

# Changelog

All notable changes to the `twat_cache` package will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v2.3.0] - 2025-03-04

### Added
- Improved context management utilities
  - Enhanced error handling in context managers
  - Added support for explicit engine selection in context managers
  - Improved resource cleanup mechanisms
- Enhanced backend selection strategy
  - Refined data type detection for optimal backend selection
  - Added support for hybrid caching with automatic backend switching
  - Improved fallback mechanisms for unavailable backends
- Comprehensive documentation updates
  - Added detailed examples for all cache backends
  - Created documentation for context management
  - Updated installation and usage instructions

### Fixed
- Resolved remaining type compatibility issues across the codebase
- Fixed edge cases in Redis connection handling
- Addressed potential memory leaks in long-running cache instances
- Improved error handling in serialization/deserialization processes

### Changed
- Refactored internal cache key generation for better performance
- Standardized logging format across all cache engines
- Improved test coverage for all components
- Updated dependencies to latest compatible versions

## [v2.2.0] - 2024-09-01

### Added

- Comprehensive test suite for backend selection strategy
  - Tests for data size estimation
  - Tests for type-based backend selection
  - Tests for backend availability
  - Tests for various data types (primitive, containers, NumPy arrays, pandas DataFrames)
- Redis cache engine implementation
  - Full Redis cache engine with serialization, compression, and TTL support
  - Redis-specific configuration options
  - Proper connection handling and error management
  - Registration in the engine manager
- Documentation for cache context management
  - Detailed guide on using context managers
  - Examples for basic and advanced usage patterns
  - Best practices for resource management
  - Error handling recommendations

### Fixed

- Type compatibility issues in context.py with CacheConfig protocol
  - Updated protocol in type_defs.py to use validate_config instead of validate
  - Fixed type casting to avoid type errors
  - Improved type annotations for better static analysis
- Linter errors in engine implementations
  - Fixed import issues with optional dependencies
  - Addressed type compatibility warnings
  - Improved error handling in Redis engine

### Changed

- Expanded test coverage for cache engines
  - Added comprehensive tests for Redis cache engine
  - Tests for initialization, configuration validation, key generation
  - Tests for caching operations and error handling
- Refactored common patterns across engine implementations
  - Standardized engine initialization and validation procedures
  - Created unified interfaces for all cache backends
  - Improved code organization and maintainability

## [v2.1.1] - 2024-08-26

### Added

- New custom exceptions module with proper inheritance hierarchy
  - Base `TwatCacheError` exception class
  - Specialized exceptions for different error categories (configuration, engine, resource, etc.)
  - Improved error messages with context-specific information
- Context management for cache engines
  - `CacheContext` class that provides resource cleanup on exit
  - Safe resource management with proper error handling
  - Support for engine selection based on configuration
- Tests for exceptions and context management modules
  - Simple test suite for exception hierarchy and messages
  - Context management tests with mocking for proper isolation
- Implemented data type-based cache backend selection strategy
  - New `backend_selector` module for automatic backend selection
  - Helper functions for common data types (numpy, pandas, images, json)
  - Smart backend selection based on data characteristics
- Added hybrid caching capabilities
  - `hybrid_cache` decorator for size-based backend selection
  - `smart_cache` decorator for automatic backend selection
- Added example demonstrating the backend selection strategy
- Created CHANGELOG.md for tracking version changes
- Updated TODO.md to reflect completed items and reprioritize tasks

### Fixed

- Fixed error handling in various cache engines
- Improved cleanup logic for better resource management
- Made error messages more consistent across the codebase
- Installation issues with pip install -e . by replacing hatchling with setuptools
- Path handling in CacheContext

### Changed

- Standardized initialization patterns across engine implementations
- Improved shutdown procedures to properly release resources
- Removed setup.py in favor of pyproject.toml for modern Python packaging
- Refactored context manager implementation for better error handling 
