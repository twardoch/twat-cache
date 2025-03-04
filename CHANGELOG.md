---
this_file: CHANGELOG.md
---

# Changelog

All notable changes to the `twat_cache` package will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
