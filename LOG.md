---
this_file: LOG.md
---

# Changelog

All notable changes to the `twat_cache` project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), 
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

As you develop, run 

```
uv venv; source .venv/bin/activate; uv pip install -e .[all,dev,test]; hatch run lint:fix; hatch test
```

to ensure that the code is linted and tested. This will inform your next steps. 

## [1.8.1] - 2025-02-18

### Added
- Added comprehensive type stubs for all cache engines
- Added detailed rationale section in README.md comparing different caching libraries
- Added extensive code examples for each caching strategy

### Changed
- Updated documentation with detailed type hints and protocols
- Improved error messages in cache engines
- Enhanced configuration validation

### Fixed
- Fixed type hints in async cache implementations
- Fixed decorator type hints for better IDE support
- Fixed linter errors in multiple files

### Issues
- Still missing type stubs for external dependencies
- Some linter warnings in test files need addressing
- Need to improve async test coverage

### Next Steps
1. Fix remaining linter issues:
   - Add missing type stubs for external dependencies
   - Address warnings in test files
   - Improve type safety in async code

2. Enhance test coverage:
   - Add more async test cases
   - Add stress tests for race conditions
   - Add integration tests for all backends

3. Improve documentation:
   - Add migration guide
   - Add performance comparison guide
   - Add troubleshooting section

## [1.8.0] - 2025-02-17

### Added
- Completed core features:
  - Memory-based caching (mcache)
  - Disk-based caching (bcache)
  - File-based caching (fcache)
  - Async-capable caching (via ucache)
  - Universal caching (ucache)
- Implemented all cache engines:
  - FunctoolsCacheEngine (base memory cache)
  - CacheToolsEngine (flexible memory cache)
  - DiskCacheEngine (SQL-based disk cache)
  - JoblibEngine (file-based cache)
  - KleptoEngine (flexible cache)
  - AioCacheEngine (async cache)
- Added comprehensive features:
  - TTL support for all caches
  - Multiple eviction policies (LRU, LFU, FIFO, RR)
  - Secure file permissions for disk caches
  - Compression support for file caches
  - Race condition handling
  - Proper error handling and logging
- Added proper type hints and protocols
- Added comprehensive test suite
- Updated documentation with examples

### Changed
- Reorganized backend priorities for each decorator:
  - mcache: cachebox > cachetools > functools
  - bcache: diskcache > klepto SQL > mcache
  - fcache: joblib > klepto file > mcache
  - ucache: auto-selects best backend
- Enhanced test coverage with backend-specific tests
- Improved error handling and logging
- Updated configuration system to use Pydantic

### Fixed
- Fixed CacheConfig initialization issues
- Fixed cache stats tracking
- Fixed maxsize enforcement
- Fixed race conditions in multi-threaded scenarios
- Fixed file permissions for disk caches
- Fixed type hints and protocols

### Issues
- Missing type stubs for some dependencies:
  - aiocache
  - diskcache
  - joblib
  - klepto
- Some linter warnings in test files
- Need more async test coverage
- Need more stress tests for race conditions

### Next Steps
1. Type System:
   - Add missing type stubs for dependencies
   - Fix remaining linter warnings
   - Add more type safety

2. Testing:
   - Add more async tests
   - Add stress tests for race conditions
   - Add performance benchmarks
   - Add integration tests

3. Documentation:
   - Add API reference
   - Add performance guide
   - Add migration guide
   - Add troubleshooting guide

4. Performance:
   - Add caching statistics
   - Add cache warming
   - Add cache prefetching
   - Add cache compression options

5. Security:
   - Add encryption support
   - Add access control
   - Add audit logging
   - Add cache poisoning protection

## [1.7.9] - 2025-02-16

### Changed

* Updated TODO.md with clearer structure and priorities
* Reorganized Phase 2 tasks to focus on critical issues first
* Added more detailed subtasks for each component

### Fixed

* Fixed Pydantic field validators in CacheConfig
* Updated model_config settings
* Improved error messages

### Issues

* Critical: CacheEngine import failing in test_engines.py
* CacheConfig initialization still broken (TypeError: CacheConfig() takes no arguments)
* Cache stats tracking not working
* Cache maxsize enforcement not working
* Multiple linting issues identified:
  - Magic numbers in comparisons
  - Boolean argument type issues
  - Module naming conflicts with stdlib
  - Unused arguments in lambda functions
  - Complex function (clear_cache)

### Next Steps

1. Fix Critical Engine Issues:
   - Fix CacheEngine import in base.py
   - Fix test_engines.py import error
   - Fix CacheConfig initialization
   - Address linting issues

2. Fix Cache Engine Core:
   - Implement proper stats tracking
   - Fix maxsize enforcement
   - Add proper cache key generation
   - Add proper error handling

3. Improve Test Coverage:
   - Fix failing tests
   - Add engine-specific tests
   - Add performance benchmarks

4. Documentation:
   - Add configuration guide
   - Add backend selection guide
   - Add performance optimization guide

# Development Log

## 2024-02-16

### Dependency Management
- [x] Made optional backend imports more robust in engines/__init__.py
- [x] Fixed type annotations for __all__ exports
- [x] Added proper error handling for missing dependencies

### Test Improvements
- [x] Created test_constants.py to eliminate magic numbers
- [x] Updated test_cache.py to use constants
- [x] Updated test_decorators.py to use constants
- [x] Updated test_engines.py to use constants
- [x] Updated test_config.py to use constants
- [x] Improved test organization and documentation
- [x] Added more descriptive test names and docstrings
- [x] Simplified test cases to focus on core functionality
- [x] Removed redundant test cases

### Code Quality
- [x] Fixed linter errors in engines/__init__.py
- [x] Fixed boolean parameter issues in config.py
- [x] Fixed boolean parameter issues in decorators.py
- [x] Improved type annotations
- [x] Added proper file headers with this_file magic records
- [x] Cleaned up imports
- [x] Made boolean parameters keyword-only
- [x] Standardized parameter naming and types
- [x] Refactored ucache decorator for reduced complexity
- [x] Added proper type definitions for decorators
- [x] Fixed type annotation issues in decorators.py

## TODO

### Critical Issues
1. Fix remaining linter errors:
   - [x] Boolean parameter issues in function definitions
   - [ ] Unused imports in various files
   - [x] Function complexity issues
   - [x] Type annotation issues in decorators.py

2. Test Suite:
   - [x] Update test_cache.py to use constants
   - [x] Update test_decorators.py to use constants
   - [x] Update test_engines.py to use constants
   - [x] Update test_config.py to use constants
   - [ ] Fix test dependencies
   - [ ] Add proper fallback testing
   - [ ] Improve async testing

3. Documentation:
   - [ ] Update README with installation instructions
   - [ ] Add troubleshooting guide
   - [ ] Document fallback behavior

### Next Steps
1. Add proper fallback tests:
   - [ ] Test backend selection logic
   - [ ] Test fallback behavior with missing dependencies
   - [ ] Test async fallback behavior
   - [ ] Test disk cache fallback

2. Improve async support:
   - [x] Fix async type hints
   - [ ] Add proper async tests
   - [ ] Improve async fallback behavior
   - [ ] Document async usage

3. Clean up imports:
   - [ ] Remove unused imports
   - [ ] Organize imports consistently
   - [ ] Fix import cycles
   - [ ] Document import requirements

## Implementation Notes

### Type System Improvements
1. Added Protocol classes for cache decorators:
   - CacheDecorator for sync functions
   - AsyncCacheDecorator for async functions
2. Added type aliases for decorator functions:
   - SyncDecorator for sync cache decorators
   - AsyncDecorator for async cache decorators
3. Fixed type hints in decorator functions:
   - Proper handling of async functions
   - Better type safety for decorator returns
   - Fixed unbound type variables

### Code Improvements
1. Made all boolean parameters keyword-only to prevent confusion
2. Standardized type hints using Optional instead of union syntax
3. Added proper parameter documentation
4. Improved function signatures for better type safety
5. Added validation for configuration parameters
6. Split ucache decorator into smaller functions:
   - _get_available_backends
   - _select_best_backend
   - _create_engine

### Test Refactoring
1. Removed redundant test cases that were testing the same functionality
2. Simplified test assertions to use constants
3. Improved test organization and naming
4. Added better docstrings and comments
5. Standardized test structure across all test files
6. Added proper error handling for missing dependencies

### Dependency Management
1. Made backend imports optional with proper error handling
2. Added availability flags for each backend
3. Improved __all__ exports to handle missing backends
4. Fixed type annotations for module exports

### Code Quality
1. Added proper file headers
2. Fixed import organization
3. Improved type hints
4. Removed unused code
5. Standardized code formatting
6. Made boolean parameters safer with keyword-only arguments
7. Reduced function complexity through better organization

## Next Focus Areas
1. Add comprehensive fallback tests
2. Improve async support
3. Clean up imports
4. Update documentation

## [1.7.8] - 2025-02-16

### Changed

* Reorganized TODO.md with clearer structure and priorities
* Added Phase 3 for advanced features
* Updated test results analysis

### Fixed

* Fixed Pydantic field validators in CacheConfig
* Updated field validator decorators to use @classmethod
* Fixed model_config settings

### Issues

* CacheConfig initialization still broken (TypeError: CacheConfig() takes no arguments)
* Cache stats tracking not working (hits/misses not being counted)
* Cache maxsize enforcement not working (cache growing beyond limit)
* Cache clearing behavior inconsistent
* Field validation in CacheConfig needs fixing

### Next Steps

1. Fix CacheConfig initialization:
   - Update Pydantic model to properly accept constructor arguments
   - Fix field validation and property access
   - Add proper error messages
   - Update model_config for proper initialization

2. Fix cache engine issues:
   - Fix stats tracking in FunctoolsCacheEngine
   - Fix maxsize enforcement
   - Fix cache key generation
   - Fix cache clearing behavior

3. Fix failing tests:
   - Fix CacheConfig initialization tests
   - Fix cache stats tracking tests
   - Fix maxsize enforcement tests
   - Fix cache clearing tests

## [1.7.7] - 2025-02-16

### Changed

* Reorganized TODO.md to better reflect current priorities
* Updated CacheConfig implementation to use proper Pydantic fields
* Fixed linting issues in configuration system

### Fixed

* Removed leading underscores from CacheConfig field names
* Fixed field validation in CacheConfig
* Fixed property access in CacheConfig

### Issues

* CacheConfig initialization is broken (TypeError: CacheConfig() takes no arguments)
* Cache stats tracking is not working (hits/misses not being counted)
* Cache maxsize enforcement is not working (cache growing beyond limit)
* Cache clearing behavior is inconsistent
* Field validation in CacheConfig needs fixing

### Next Steps

1. Fix CacheConfig initialization:
   - Implement proper Pydantic model initialization
   - Fix field validation
   - Add proper error messages

2. Fix cache engine issues:
   - Fix stats tracking in FunctoolsCacheEngine
   - Fix maxsize enforcement
   - Fix cache key generation
   - Fix cache clearing behavior

3. Improve test coverage:
   - Add missing engine-specific tests
   - Add benchmark tests
   - Add stress tests
   - Add integration tests

## [1.7.6] - 2025-02-16

### Changed

* Reorganized TODO.md to better track progress
* Updated test suite with comprehensive engine tests
* Improved error handling in cache engines

### Fixed

* Renamed `lru.py` to `functools.py` for clarity
* Removed redundant SQL and Redis implementations
* Added proper type hints and docstrings

## [1.7.5] - 2025-02-15

### Fixed

* Fixed README.md formatting

## [1.7.3] - 2025-02-15

### Changed

* Minor documentation updates
* Internal code improvements

## [1.7.0] - 2025-02-13

### Added

* Added pyupgrade to development dependencies
* Added new fix command in pyproject.toml for automated code fixes
* Enhanced test environment with specific pytest dependencies
  + Added pytest-xdist for parallel test execution
  + Added pytest-benchmark for performance testing

### Changed

* Reorganized imports in core module
* Updated gitignore to exclude _private directory

### Fixed

* Fixed import statement in __init__.py
* Improved development tooling configuration

## [1.6.2] - 2025-02-06

### Fixed

* Bug fixes and stability improvements

## [1.6.1] - 2025-02-06

### Changed

* Minor updates and improvements

## [1.6.0] - 2025-02-06

### Added

* Initial GitHub repository setup
* Comprehensive project structure
* Basic caching functionality
* Multiple backend support (memory, SQL, joblib)
* Automatic cache directory management
* Type hints and modern Python features

## [1.1.0] - 2025-02-03

### Added

* Early development version
* Core caching functionality

## [1.0.0] - 2025-02-03

### Added

* Initial release
* Basic memory caching implementation

[1.7.9]: https://github.com/twardoch/twat-cache/compare/v1.7.8...v1.7.9
[1.7.8]: https://github.com/twardoch/twat-cache/compare/v1.7.7...v1.7.8
[1.7.7]: https://github.com/twardoch/twat-cache/compare/v1.7.6...v1.7.7
[1.7.6]: https://github.com/twardoch/twat-cache/compare/v1.7.5...v1.7.6
[1.7.5]: https://github.com/twardoch/twat-cache/compare/v1.7.3...v1.7.5
[1.7.3]: https://github.com/twardoch/twat-cache/compare/v1.7.0...v1.7.3
[1.7.0]: https://github.com/twardoch/twat-cache/compare/v1.6.2...v1.7.0
[1.6.2]: https://github.com/twardoch/twat-cache/compare/v1.6.1...v1.6.2
[1.6.1]: https://github.com/twardoch/twat-cache/compare/v1.6.0...v1.6.1
[1.6.0]: https://github.com/twardoch/twat-cache/compare/v1.1.0...v1.6.0
[1.1.0]: https://github.com/twardoch/twat-cache/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/twardoch/twat-cache/releases/tag/v1.0.0

# Development Log

### Completed

* Updated TODO.md with clearer structure and priorities
* Fixed Pydantic field validators
* Updated model_config settings
* Identified critical import issue in test_engines.py

### In Progress

* Fixing CacheEngine import issue
* Fixing CacheConfig initialization
* Addressing linting issues
* Improving test coverage

### Next Steps

1. Fix Critical Issues:
   - Fix CacheEngine import
   - Fix CacheConfig initialization
   - Fix test failures
   - Address linting issues

2. Improve Core Functionality:
   - Fix stats tracking
   - Fix maxsize enforcement
   - Improve cache key generation
   - Add proper error handling

3. Enhance Testing:
   - Fix failing tests
   - Add comprehensive test suite
   - Add performance benchmarks

# Critical Considerations

1. Engine System:
   - CacheEngine must be properly exported from base.py
   - All engines must properly implement the base interface
   - Stats tracking must be consistent across all engines

2. Configuration System:
   - CacheConfig must properly initialize with constructor arguments
   - Field validation must be robust and informative
   - Cache directory management must be reliable

3. Testing System:
   - All engines must be properly tested
   - Performance benchmarks must be comprehensive
   - Error handling must be thoroughly tested

## [1.7.8]: https://github.com/twardoch/twat-cache/compare/v1.7.7...v1.7.8
## [1.7.7]: https://github.com/twardoch/twat-cache/compare/v1.7.6...v1.7.7
## [1.7.6]: https://github.com/twardoch/twat-cache/compare/v1.7.5...v1.7.6
## [1.7.5]: https://github.com/twardoch/twat-cache/compare/v1.7.3...v1.7.5
## [1.7.3]: https://github.com/twardoch/twat-cache/compare/v1.7.0...v1.7.3
## [1.7.0]: https://github.com/twardoch/twat-cache/compare/v1.6.2...v1.7.0
## [1.6.2]: https://github.com/twardoch/twat-cache/compare/v1.6.1...v1.6.2
## [1.6.1]: https://github.com/twardoch/twat-cache/compare/v1.6.0...v1.6.1
## [1.6.0]: https://github.com/twardoch/twat-cache/compare/v1.1.0...v1.6.0
## [1.1.0]: https://github.com/twardoch/twat-cache/compare/v1.0.0...v1.1.0
## [1.0.0]: https://github.com/twardoch/twat-cache/releases/tag/v1.0.0

# Development Log

### Completed

* Fixed Pydantic field validators in CacheConfig:
  - Updated validators to use @classmethod decorator
  - Fixed model_config settings
  - Improved error messages
* Reorganized TODO.md:
  - Added clearer structure
  - Prioritized critical fixes
  - Added Phase 3 for advanced features
* Updated test suite:
  - Added more comprehensive test cases
  - Identified failing tests
  - Added test categories

### In Progress

* Fixing CacheConfig initialization issues:
  - Working on proper Pydantic model setup
  - Fixing field validation and property access
  - Adding proper error messages
* Fixing cache engine issues:
  - Implementing proper stats tracking
  - Fixing maxsize enforcement
  - Improving cache key generation
  - Fixing cache clearing behavior

### Next Steps

1. Fix Critical Issues:
   - Fix CacheConfig initialization
   - Fix cache stats tracking
   - Fix maxsize enforcement
   - Fix cache clearing behavior

2. Enhance Test Coverage:
   - Fix failing tests
   - Add missing engine-specific tests
   - Add performance tests

3. Improve Documentation:
   - Update configuration guide
   - Add troubleshooting guide
   - Add performance tips
   - Add examples

# Critical Considerations

1. Configuration System:
   - CacheConfig must properly initialize with constructor arguments
   - Field validation must work correctly
   - Property access must be reliable
   - Error messages must be helpful

2. Cache Engine Behavior:
   - Stats tracking must be accurate
   - Maxsize enforcement must be reliable
   - Cache clearing must be consistent
   - Key generation must handle all types

3. Test Coverage:
   - All critical functionality must be tested
   - Edge cases must be covered
   - Performance must be verified
   - Error handling must be tested

# Conslidation UI Project Analysis & Plan

## Progress Log

### 2024-03-21
- Updated TODO.md with completed tasks and reorganized remaining work
- Major progress in core functionality:
  - Completed all basic cache engine implementations
  - Fixed cache stats tracking and clearing behavior
  - Improved type hints and configuration system
  - Added comprehensive test coverage for core features
- Next steps prioritized:
  1. Add missing engine-specific tests (eviction, concurrency, etc.)
  2. Implement serialization protocol
  3. Add async test coverage
  4. Create comprehensive documentation

Critical Considerations:
1. Engine-specific Tests:
   - Need stress tests for memory limits and eviction policies
   - Add concurrent access testing with high load
   - Test edge cases like cache corruption and recovery
   - Verify proper cleanup of resources

2. Serialization Protocol:
   - Add support for complex objects and custom types
   - Consider compression for large cached values
   - Implement versioning for cached data format
   - Add validation for serialized data integrity

3. Async Support:
   - Improve error handling for timeouts and connection issues
   - Ensure proper cleanup of async resources
   - Add retry mechanisms for transient failures
   - Test interaction with different event loops

4. Documentation:
   - Add detailed performance characteristics
   - Document tradeoffs between different cache engines
   - Create troubleshooting guide
   - Add migration guide for users of removed implementations

## Recent Changes

### 2024-03-21
- Fixed CacheConfig implementation:
  - Added proper field aliases for configuration parameters
  - Implemented abstract base class methods
  - Added Pydantic model configuration for proper field handling
  - Fixed validation method
- Updated test suite:
  - Fixed failing tests related to CacheConfig instantiation
  - Added tests for field aliases and validation
  - Improved test coverage for configuration handling

### Next Steps
1. Fix remaining test failures:
   - Cache stats tracking
   - List/unhashable type handling
   - Cache clearing behavior
2. Implement missing engine-specific tests:
   - Test cache eviction policies
   - Test concurrent access
   - Test error handling
   - Test serialization/deserialization
   - Test memory limits

### Critical Considerations
1. Engine-specific Tests:
   - Need stress tests for memory limits and eviction policies
   - Add concurrent access testing with high load
   - Test edge cases like cache corruption and recovery
   - Verify proper cleanup of resources

2. Serialization Protocol:
   - Add support for complex objects and custom types
   - Consider compression for large cached values
   - Implement versioning for cached data format
   - Add validation for serialized data integrity

3. Async Support:
   - Improve error handling for timeouts and connection issues
   - Ensure proper cleanup of async resources
   - Add retry mechanisms for transient failures
   - Test interaction with different event loops

4. Documentation:
   - Add detailed performance characteristics
   - Document tradeoffs between different cache engines
   - Create troubleshooting guide
   - Add migration guide for users of removed implementations

### 2024-03-19
#### Current Status
- Ran development setup and tests
- Found critical issues that need immediate attention:
  1. Pydantic field validator errors in CacheConfig
  2. 27 remaining linting issues
  3. Test failures across all test files

#### Critical Issues

1. **Pydantic Integration Issues**
   - Error: `@field_validator` cannot be applied to instance methods
   - Location: `src/twat_cache/config.py`
   - Impact: Breaking all tests due to config initialization failure

2. **Linting Issues**
   - 27 remaining issues including:
     - Magic numbers in comparisons
     - Print statements in production code
     - Boolean positional arguments
     - Module naming conflicts
     - Complex function warnings

#### Next Steps

1. **Immediate Fixes**
   - Fix Pydantic field validator implementation in CacheConfig
   - Address critical linting issues affecting functionality
   - Fix test failures

2. **Short-term Tasks**
   - Complete cache stats tracking implementation
   - Add proper type constraints
   - Implement missing test cases

3. **Documentation Updates**
   - Document configuration system
   - Add validation rules
   - Update type hints documentation

