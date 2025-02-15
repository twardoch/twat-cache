---
this_file: LOG.md
---

# Changelog

All notable changes to the `twat-cache` project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.7.5] - 2025-02-15

### Fixed

- Fixed README.md formatting

## [1.7.3] - 2025-02-15

### Changed

- Minor documentation updates
- Internal code improvements

## [1.7.0] - 2025-02-13

### Added

- Added pyupgrade to development dependencies
- Added new fix command in pyproject.toml for automated code fixes
- Enhanced test environment with specific pytest dependencies
  - Added pytest-xdist for parallel test execution
  - Added pytest-benchmark for performance testing

### Changed

- Reorganized imports in core module
- Updated gitignore to exclude _private directory

### Fixed

- Fixed import statement in __init__.py
- Improved development tooling configuration

## [1.6.2] - 2025-02-06

### Fixed

- Bug fixes and stability improvements

## [1.6.1] - 2025-02-06

### Changed

- Minor updates and improvements

## [1.6.0] - 2025-02-06

### Added

- Initial GitHub repository setup
- Comprehensive project structure
- Basic caching functionality
- Multiple backend support (memory, SQL, joblib)
- Automatic cache directory management
- Type hints and modern Python features

## [1.1.0] - 2025-02-03

### Added

- Early development version
- Core caching functionality

## [1.0.0] - 2025-02-03

### Added

- Initial release
- Basic memory caching implementation

[1.7.5]: https://github.com/twardoch/twat-cache/compare/v1.7.3...v1.7.5
[1.7.3]: https://github.com/twardoch/twat-cache/compare/v1.7.0...v1.7.3
[1.7.0]: https://github.com/twardoch/twat-cache/compare/v1.6.2...v1.7.0
[1.6.2]: https://github.com/twardoch/twat-cache/compare/v1.6.1...v1.6.2
[1.6.1]: https://github.com/twardoch/twat-cache/compare/v1.6.0...v1.6.1
[1.6.0]: https://github.com/twardoch/twat-cache/compare/v1.1.0...v1.6.0
[1.1.0]: https://github.com/twardoch/twat-cache/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/twardoch/twat-cache/releases/tag/v1.0.0 
