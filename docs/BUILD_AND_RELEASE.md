# Build and Release Guide

This document describes the build and release process for `twat-cache`.

## Overview

The project uses git-tag-based semantic versioning with automated CI/CD for multiplatform testing, building, and releasing to PyPI.

## Prerequisites

### Local Development

1. **Python 3.10+** - The project supports Python 3.10, 3.11, and 3.12
2. **Git** - For version control and tag management
3. **Make** (optional) - For convenient command shortcuts

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/twardoch/twat.git
cd twat

# Run the setup script
./scripts/setup-dev.sh

# Or manually install dependencies
pip install -e .[dev,test,all]
```

## Build System

The project uses:
- **Hatch** - Primary build backend and environment management
- **hatch-vcs** - Git-based versioning
- **Build** - PEP 517 compatible build tool
- **Ruff** - Linting and formatting
- **MyPy** - Type checking
- **Pytest** - Testing framework

## Local Development Workflow

### Quick Commands

```bash
# Using Make (recommended)
make help           # Show all available commands
make test           # Run tests
make lint           # Run linting
make format         # Format code
make build          # Build package
make release-check  # Run all pre-release checks

# Using scripts directly
python3 scripts/build.py test
python3 scripts/build.py lint
python3 scripts/build.py format
python3 scripts/build.py build
python3 scripts/build.py check
```

### Development Cycle

1. **Make changes** to the code
2. **Format code**: `make format`
3. **Run tests**: `make test`
4. **Check linting**: `make lint`
5. **Build package**: `make build`
6. **Run full check**: `make release-check`

## Version Management

### Git Tag-Based Versioning

The project uses git tags for versioning:
- Tags follow the pattern `v<major>.<minor>.<patch>` (e.g., `v1.2.3`)
- Version is automatically extracted from git tags using `hatch-vcs`
- Development versions use git commit hash

### Version Commands

```bash
# Check current version
make version
python3 scripts/version.py current

# Get next version
python3 scripts/version.py next patch
python3 scripts/version.py next minor
python3 scripts/version.py next major

# List all version tags
make version-list
python3 scripts/version.py list
```

## Release Process

### Automated Release (Recommended)

1. **Ensure clean working directory**:
   ```bash
   git status  # Should be clean
   git checkout main
   git pull origin main
   ```

2. **Run pre-release checks**:
   ```bash
   make release-check
   ```

3. **Create and push release**:
   ```bash
   # Patch release (1.2.3 -> 1.2.4)
   make release
   
   # Minor release (1.2.3 -> 1.3.0)
   make release-minor
   
   # Major release (1.2.3 -> 2.0.0)
   make release-major
   ```

The release script will:
- Run all tests and checks
- Determine the next version number
- Create and push a git tag
- Trigger GitHub Actions for building and publishing

### Manual Release

If you need more control:

```bash
# 1. Determine next version
NEXT_VERSION=$(python3 scripts/version.py next patch)

# 2. Run pre-release checks
make release-check

# 3. Create and push tag
python3 scripts/version.py tag $NEXT_VERSION
git push origin v$NEXT_VERSION

# GitHub Actions will handle the rest
```

### Dry Run

To see what would happen without making changes:

```bash
make release-dry-run
python3 scripts/release.py release patch --dry-run
```

## CI/CD Pipeline

### GitHub Actions Workflows

#### 1. CI Workflow (`.github/workflows/ci.yml`)

Triggers on:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`

Jobs:
- **Test**: Runs on Ubuntu, Windows, macOS with Python 3.10, 3.11, 3.12
- **Security**: Runs security scans with `safety` and `bandit`
- **Build**: Builds package and uploads artifacts

#### 2. Release Workflow (`.github/workflows/release.yml`)

Triggers on:
- Git tags matching `v*` pattern

Jobs:
- **Test**: Multi-platform testing (Ubuntu, Windows, macOS)
- **Build**: Creates source distribution and wheel
- **Publish**: Publishes to PyPI
- **Release**: Creates GitHub release with artifacts

### Multiplatform Support

The project is tested on:
- **Operating Systems**: Ubuntu, Windows, macOS
- **Python Versions**: 3.10, 3.11, 3.12
- **Architectures**: x64 (primary), arm64 (via GitHub's runners)

## Package Distribution

### PyPI Publication

Packages are automatically published to PyPI when tags are pushed:
- **Source distribution** (`.tar.gz`)
- **Universal wheel** (`.whl`)

### GitHub Releases

Each release includes:
- Source code archives
- Distribution files
- Automatically generated release notes
- Full changelog

## Quality Assurance

### Pre-Release Checks

The release process includes:
1. **Code formatting** (Ruff)
2. **Linting** (Ruff with multiple rule sets)
3. **Type checking** (MyPy)
4. **Unit tests** (Pytest)
5. **Integration tests**
6. **Benchmark tests**
7. **Security scanning** (Safety, Bandit)
8. **Build verification**

### Test Coverage

- **Unit tests** for all core functionality
- **Integration tests** for real-world scenarios
- **Benchmark tests** for performance regression detection
- **Platform-specific tests** for compatibility

## Security

### Supply Chain Security

- **Dependency scanning** with Safety
- **Code security scanning** with Bandit
- **Automated security updates** for dependencies
- **Signed releases** (planned)

### Secrets Management

Required secrets for CI/CD:
- `PYPI_TOKEN` - PyPI API token for publishing
- `GITHUB_TOKEN` - Automatically provided by GitHub

## Troubleshooting

### Common Issues

1. **Version not updating**:
   - Ensure git tags are pushed: `git push origin --tags`
   - Check tag format: should be `v1.2.3`

2. **Build fails**:
   - Run `make release-check` locally first
   - Check Python version compatibility
   - Verify all dependencies are installed

3. **Tests fail on CI**:
   - Check platform-specific issues
   - Verify environment variables
   - Check for race conditions in tests

4. **Release fails**:
   - Check PyPI token validity
   - Verify package name availability
   - Check GitHub permissions

### Debug Commands

```bash
# Debug version information
make debug-version

# Debug build process
make debug-build

# Check environment
make env-info

# Run specific test
python3 -m pytest tests/test_specific.py -v
```

## Advanced Usage

### Custom Build Configuration

To customize the build process, modify:
- `pyproject.toml` - Project metadata and build configuration
- `scripts/build.py` - Build script logic
- `scripts/release.py` - Release script logic

### Environment Variables

- `TWAT_CACHE_DEBUG` - Enable debug logging
- `TWAT_CACHE_CONFIG` - Custom configuration file path
- `GITHUB_TOKEN` - GitHub API token for releases

### Hatch Environments

The project defines several Hatch environments:

```bash
# Run tests in isolated environment
hatch env run test:test

# Run linting in isolated environment
hatch env run lint:all

# List all environments
hatch env show
```

## Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run `make release-check`
5. Submit a pull request

### Release Schedule

- **Patch releases**: Bug fixes, minor improvements
- **Minor releases**: New features, backward-compatible changes
- **Major releases**: Breaking changes, major new features

### Versioning Policy

We follow [Semantic Versioning](https://semver.org/):
- `MAJOR.MINOR.PATCH`
- Pre-release versions: `MAJOR.MINOR.PATCH-dev.N`
- Development versions: `MAJOR.MINOR.PATCH.dev.N+commit.hash`

## References

- [Hatch Documentation](https://hatch.pypa.io/)
- [PEP 517 - A build-system independent format for source trees](https://peps.python.org/pep-0517/)
- [PEP 621 - Storing project metadata in pyproject.toml](https://peps.python.org/pep-0621/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [PyPI Publishing Guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/)