# twat-cache Repository File Catalog
<!-- this_file: REVIEW/FILES-cla.md -->

## Repository Structure Overview

```
.
├── .cursor/                          # Cursor IDE configuration
├── .github/                          # GitHub Actions and workflows
├── .specstory/                       # Project history and development logs
├── REVIEW/                           # Repository analysis and improvement plans
├── docs/                             # Project documentation
├── examples/                         # Usage examples
├── scripts/                          # Build and development scripts
├── src/                              # Main source code
├── src_docs/                         # Documentation source files
├── tests/                            # Test suite
└── [config files]                   # Various configuration files
```

## Root Directory Files

### Core Project Files
- **README.md** - Main project documentation with installation, usage examples, and technical details. Comprehensive overview of the twat-cache library with code examples for all major decorators (mcache, bcache, fcache, acache, ucache).

- **pyproject.toml** - Python project configuration defining build system, dependencies, development tools, and packaging metadata. Uses Hatchling build backend with comprehensive tool configurations for Ruff, MyPy, pytest, and coverage.

- **LICENSE** - Project license file (MIT License based on pyproject.toml).

- **mkdocs.yml** - MkDocs documentation site configuration for generating documentation website.

- **uv.lock** - UV package manager lockfile ensuring reproducible dependency installations.

### Development and Planning Files
- **PLAN.md** - Comprehensive development roadmap with 6 phases of improvements including documentation infrastructure, code quality, testing, features, community building, and quality assurance.

- **TODO.md** - Detailed task list with 170+ specific actionable items organized by category (documentation, type hints, testing, etc.). Mix of completed legacy tasks and pending improvements.

- **WORK.md** - Current work progress and immediate next steps tracking.

- **CHANGELOG.md** - Project change history and release notes.

- **NEXT.md** - Future feature and improvement ideas.

- **WORKFLOW_SETUP.md** - Development workflow and setup instructions.

### Legacy and Cleanup Files
- **CLEANUP.txt** - Notes on files and features to clean up or remove.

- **PROMPT.txt** - Development prompts and guidelines.

- **REPO_CONTENT.txt** - Repository content analysis.

- **REFACTOR_FILELIST.txt** - List of files needing refactoring.

- **VERSION.txt** - Version information file.

- **cleanup.py** - Python script for automated cleanup tasks.

### Configuration Files
- **.gitignore** - Git ignore patterns for Python projects, build artifacts, and IDE files.

- **.pre-commit-config.yaml** - Pre-commit hooks configuration for code quality enforcement.

## .cursor/ Directory
IDE-specific configuration files for Cursor editor:
- **rules/0project.mdc** - Project-specific rules and guidelines
- **rules/cleanup.mdc** - Cleanup guidelines
- **rules/filetree.mdc** - File tree organization rules
- **rules/quality.mdc** - Code quality standards

## .github/ Directory
GitHub Actions CI/CD configuration:
- **workflows/ci.yml** - Continuous integration pipeline for testing and quality checks
- **workflows/push.yml** - Pipeline triggered on pushes
- **workflows/release.yml** - Automated release and publishing pipeline

## .specstory/ Directory
Development history and decision logs:
- **history/.what-is-this.md** - Explanation of the specstory concept
- **history/[multiple dated files].md** - Chronological development logs with timestamps
- Various analysis and planning documents tracking the evolution of the project

## docs/ Directory
Project documentation:
- **BUILD_AND_RELEASE.md** - Build system and release process documentation
- **context_management.md** - Cache context management documentation

## examples/ Directory
Usage examples:
- **backend_selection.py** - Example demonstrating backend selection and configuration

## scripts/ Directory
Development and build automation:
- **README.md** - Scripts documentation
- **build.py** - Main build script for testing, linting, formatting, and packaging
- **release.py** - Release management and versioning script
- **setup-dev.sh** - Development environment setup script
- **version.py** - Version management utilities

## src/ Directory - Main Source Code

### src/twat_cache/ - Core Library
- **__init__.py** - Public API exports including decorators (ucache, acache), cache management functions, context managers, and exception classes. Main entry point defining what users can import.

- **__main__.py** - CLI entry point and utility functions for the package.

- **cache.py** - Global cache registry and management. Functions for registering caches, clearing caches, retrieving statistics, and managing cache lifecycles.

- **config.py** - Configuration management using Pydantic models. Defines CacheConfig class with validation for cache parameters like maxsize, TTL, policies, etc.

- **context.py** - Context managers for explicit cache control. Provides CacheContext class and engine_context function for managing cache engines within specific code blocks.

- **decorators.py** - Core caching decorators (mcache, bcache, fcache, acache, ucache). Contains backend selection logic, key generation, and decorator implementation with comprehensive fallback chains.

- **exceptions.py** - Custom exception hierarchy for the library. Defines specific exceptions for different error types (configuration, engine, operation, etc.).

- **logging.py** - Logging configuration using loguru for structured logging throughout the library.

- **paths.py** - Path utilities for cache directory management and file system operations.

- **type_defs.py** - Type definitions, protocols, and typing utilities used throughout the codebase.

- **utils.py** - General utility functions and helpers.

- **py.typed** - PEP 561 marker file indicating type information is available.

### src/twat_cache/engines/ - Cache Backend Implementations
- **__init__.py** - Engine package initialization and exports.

- **base.py** - Abstract base class (BaseCacheEngine) defining the interface all cache engines must implement.

- **manager.py** - CacheEngineManager for discovering, registering, and selecting available cache engines.

- **common.py** - Common utilities and shared functionality for cache engines.

- **functools_engine.py** - Wrapper around Python's built-in functools.lru_cache, always available as fallback.

- **cachetools.py** - Engine using cachetools library for in-memory caching with various eviction policies (LRU, LFU, FIFO).

- **cachebox.py** - High-performance engine using cachebox library (Rust-based) for fast in-memory caching.

- **diskcache.py** - Persistent disk-based caching using diskcache library with SQLite backend.

- **joblib.py** - File-based caching using joblib.Memory, optimized for large objects like NumPy arrays.

- **klepto.py** - Engine using klepto library for diverse storage backends and serialization options.

- **aiocache.py** - Asynchronous caching engine using aiocache library for async/await functions.

- **py.typed** - Type information marker for the engines package.

### src/twat_cache/types/
- **cachebox.pyi** - Type stub file for cachebox library providing type information.

## src_docs/ Directory - Documentation Source
MkDocs documentation source files:
- **index.md** - Documentation homepage
- **getting-started.md** - Quick start guide
- **changelog.md** - Change history
- **faq.md** - Frequently asked questions
- **api/** - API reference documentation
  - **index.md** - API overview
  - **config.md** - Configuration API
  - **decorators.md** - Decorators API
- **user-guide/** - User guides
  - **index.md** - User guide overview
  - **installation.md** - Installation instructions
  - **quickstart.md** - Quick tutorial
  - **decorators.md** - Decorator usage guide
  - **configuration.md** - Configuration guide

## tests/ Directory - Test Suite
Comprehensive test coverage:
- **__init__.py** - Test package initialization
- **conftest.py** - Pytest configuration and shared fixtures
- **test_*.py** - Individual test modules covering:
  - **test_benchmark.py** - Performance benchmarks
  - **test_cache.py** - Cache management functionality
  - **test_config.py** - Configuration validation
  - **test_constants.py** - Constants and enums
  - **test_context.py** - Context manager functionality
  - **test_context_simple.py** - Simplified context tests
  - **test_decorators.py** - Decorator functionality
  - **test_engines.py** - Engine implementations
  - **test_exceptions.py** - Exception handling
  - **test_exceptions_simple.py** - Basic exception tests
  - **test_fallback.py** - Fallback mechanism tests
  - **test_integration.py** - Integration tests
  - **test_twat_cache.py** - Main library tests

## File Quality Assessment

### Well-Structured Files
- **README.md** - Comprehensive, well-organized with clear examples
- **pyproject.toml** - Modern Python packaging with detailed tool configurations
- **PLAN.md** - Detailed 6-phase development roadmap with clear objectives
- **src/twat_cache/decorators.py** - Well-documented with clear decorator implementations
- **src/twat_cache/__init__.py** - Clean public API exports

### Files Needing Attention
- **TODO.md** - Very long with 170+ items, needs prioritization and organization
- **CLEANUP.txt** - Legacy file that should be integrated into TODO.md or removed
- **REFACTOR_FILELIST.txt** - Should be integrated into development workflow
- **.specstory/history/** - Many redundant files that could be archived

### Missing or Incomplete
- **CONTRIBUTING.md** - No explicit contribution guidelines in root
- **SECURITY.md** - No security policy documentation
- **CODE_OF_CONDUCT.md** - No community guidelines
- **src/twat_cache/__version__.py** - Version management file referenced but missing

## Repository Health Summary

**Strengths:**
- Comprehensive documentation structure
- Well-organized source code with clear separation of concerns
- Extensive test coverage across multiple categories
- Modern Python packaging and tooling
- Detailed development planning

**Areas for Improvement:**
- Task management and prioritization
- Community documentation
- Security and contribution guidelines
- Cleanup of legacy development files
- Version management implementation