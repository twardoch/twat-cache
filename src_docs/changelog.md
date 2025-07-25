---
# this_file: src_docs/changelog.md
title: Changelog - TWAT-Cache
description: Version history and release notes for TWAT-Cache
---

# Changelog

All notable changes to TWAT-Cache will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive MkDocs documentation with Material theme
- Expanded test coverage across all modules
- Type hints throughout the codebase
- Plugin system architecture for custom cache engines
- Performance benchmarking suite

### Changed
- Improved error messages with actionable solutions
- Enhanced logging with structured output
- Refactored engine selection logic for better performance

### Fixed
- Context manager compatibility with async functions
- Memory leak in long-running cache instances
- Edge cases in TTL expiration handling

## [1.0.0] - 2024-07-01

### Added
- Initial release of TWAT-Cache
- Universal cache decorator (`@ucache`)
- Async cache decorator (`@acache`) 
- Multiple cache engine support:
  - FuncTools (built-in Python LRU cache)
  - CacheTools (advanced in-memory caching)
  - CacheBox (high-performance Rust backend)
  - DiskCache (persistent SQLite storage)
  - Joblib (optimized for large objects)
  - AioCache (async caching)
  - Klepto (scientific computing)
- Configuration system with Pydantic
- Context managers for dynamic configuration
- Comprehensive test suite
- Full type hints and mypy support

### Security
- Input validation for all cache keys
- Safe serialization of cache entries

---

## Version Guidelines

### Version Numbering

We use Semantic Versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality (backwards compatible)
- **PATCH**: Bug fixes (backwards compatible)

### Release Schedule

- **Patch releases**: As needed for bug fixes
- **Minor releases**: Monthly with new features
- **Major releases**: Annually or for breaking changes

[Unreleased]: https://github.com/twat-framework/twat-cache/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/twat-framework/twat-cache/releases/tag/v1.0.0