# this_file: Makefile
# Makefile for twat-cache development and release management

.PHONY: help install clean test lint format build release-check release benchmark docs

# Default target
help:
	@echo "twat-cache Development Commands"
	@echo "==============================="
	@echo ""
	@echo "Development:"
	@echo "  install      - Install package in development mode"
	@echo "  clean        - Clean build artifacts and cache"
	@echo "  test         - Run tests"
	@echo "  test-cov     - Run tests with coverage"
	@echo "  lint         - Run linting checks"
	@echo "  format       - Format code"
	@echo "  benchmark    - Run benchmark tests"
	@echo ""
	@echo "Build & Release:"
	@echo "  build        - Build package"
	@echo "  release-check - Run all pre-release checks"
	@echo "  release      - Create a patch release"
	@echo "  release-minor - Create a minor release"
	@echo "  release-major - Create a major release"
	@echo ""
	@echo "Versioning:"
	@echo "  version      - Show current version"
	@echo "  version-next - Show next patch version"
	@echo "  tag          - Create version tag (requires VERSION env var)"
	@echo ""
	@echo "Tools:"
	@echo "  docs         - Generate documentation"
	@echo "  security     - Run security checks"

# Development setup
install:
	pip install -e .[dev,test,all]

# Cleaning
clean:
	python3 scripts/build.py clean

# Testing
test:
	python3 scripts/build.py test

test-cov:
	python3 scripts/build.py coverage

benchmark:
	python3 scripts/build.py benchmark

# Code quality
lint:
	python3 scripts/build.py lint

format:
	python3 scripts/build.py format

# Building
build:
	python3 scripts/build.py build

# Release management
release-check:
	python3 scripts/build.py check

release:
	python3 scripts/release.py release patch

release-minor:
	python3 scripts/release.py release minor

release-major:
	python3 scripts/release.py release major

release-dry-run:
	python3 scripts/release.py release patch --dry-run

# Version management
version:
	python3 scripts/version.py current

version-next:
	python3 scripts/version.py next

version-list:
	python3 scripts/version.py list

tag:
	@if [ -z "$(VERSION)" ]; then \
		echo "Error: VERSION not specified. Use: make tag VERSION=1.2.3"; \
		exit 1; \
	fi
	python3 scripts/version.py tag $(VERSION)

# Documentation
docs:
	@echo "Generating documentation..."
	@echo "README.md contains the main documentation"
	@echo "For API docs, run: python -m pydoc twat_cache"

# Security
security:
	@echo "Running security checks..."
	@command -v safety >/dev/null 2>&1 || pip install safety
	@command -v bandit >/dev/null 2>&1 || pip install bandit
	safety check
	bandit -r src/

# Hatch commands (if available)
hatch-test:
	@command -v hatch >/dev/null 2>&1 || (echo "Hatch not installed" && exit 1)
	hatch env run test:test

hatch-test-cov:
	@command -v hatch >/dev/null 2>&1 || (echo "Hatch not installed" && exit 1)
	hatch env run test:test-cov

hatch-lint:
	@command -v hatch >/dev/null 2>&1 || (echo "Hatch not installed" && exit 1)
	hatch env run lint:all

hatch-build:
	@command -v hatch >/dev/null 2>&1 || (echo "Hatch not installed" && exit 1)
	hatch build

# Development workflow
dev-setup: install
	@echo "Development environment setup complete"
	@echo "Run 'make test' to verify installation"

dev-check: clean format lint test
	@echo "Development checks complete"

# CI simulation
ci-test:
	@echo "Running CI simulation..."
	make clean
	make format
	make lint
	make test
	make build
	@echo "CI simulation complete"

# Quick commands
quick-test:
	python3 -m pytest tests/ -x -v

quick-lint:
	python3 -m ruff check src/

quick-format:
	python3 -m ruff format src/ tests/

# Environment info
env-info:
	@echo "Environment Information:"
	@echo "======================="
	@python3 --version
	@echo "Python path: $(which python3)"
	@echo ""
	@echo "Git info:"
	@git --version
	@echo "Current branch: $(shell git branch --show-current)"
	@echo "Current commit: $(shell git rev-parse --short HEAD)"
	@echo ""
	@echo "Package info:"
	@python3 -c "import twat_cache; print(f'twat-cache version: {twat_cache.__version__ if hasattr(twat_cache, \"__version__\") else \"dev\"}')" 2>/dev/null || echo "twat-cache not installed"

# Debugging
debug-version:
	@echo "Debugging version information..."
	@python3 scripts/version.py current || echo "No version tags found"
	@echo "Git tags:"
	@git tag -l 'v*' --sort=-version:refname | head -10

debug-build:
	@echo "Debugging build process..."
	@python3 -c "import hatchling; print(f'Hatchling version: {hatchling.__version__}')" 2>/dev/null || echo "Hatchling not available"
	@python3 -c "import build; print(f'Build version: {build.__version__}')" 2>/dev/null || echo "Build not available"

# Maintenance
update-deps:
	@echo "Updating dependencies..."
	pip install --upgrade pip
	pip install --upgrade hatch build twine
	pip install --upgrade -e .[dev,test,all]

check-deps:
	@echo "Checking dependencies..."
	pip list | grep -E "(hatch|build|twine|pytest|ruff|mypy)"

# Example usage
example:
	@echo "Example usage:"
	@python3 -c "
from twat_cache import ucache
import time

@ucache(maxsize=100)
def expensive_function(x):
    time.sleep(0.1)
    return x * x

print('First call (slow):', expensive_function(5))
print('Second call (fast):', expensive_function(5))
"