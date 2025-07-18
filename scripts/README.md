# Scripts Directory

This directory contains build, release, and development scripts for the twat-cache project.

## Scripts Overview

### Core Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `build.py` | Build and test management | `python3 scripts/build.py <command>` |
| `release.py` | Release automation | `python3 scripts/release.py <command>` |
| `version.py` | Version management | `python3 scripts/version.py <command>` |
| `setup-dev.sh` | Development environment setup | `./scripts/setup-dev.sh` |

### Quick Start

```bash
# Set up development environment
./scripts/setup-dev.sh

# Run tests
python3 scripts/build.py test

# Build package
python3 scripts/build.py build

# Create a release
python3 scripts/release.py release patch
```

## Script Details

### build.py

Build and test management script with the following commands:

- `clean` - Clean build artifacts
- `format` - Format code using Ruff
- `lint` - Run linting checks
- `test` - Run tests
- `coverage` - Run tests with coverage
- `build` - Build package
- `install-dev` - Install in development mode
- `benchmark` - Run benchmark tests
- `check` - Run full check sequence

### release.py

Release automation script with the following commands:

- `release <bump_type>` - Create a new release (patch/minor/major)
- `check` - Run pre-release checks
- `--dry-run` - Show what would be done without making changes
- `--test-pypi` - Publish to Test PyPI instead of PyPI

### version.py

Version management script with the following commands:

- `current` - Show current version
- `next <bump_type>` - Calculate next version
- `tag <version>` - Create version tag
- `push <version>` - Push version tag to remote
- `list` - List all version tags

### setup-dev.sh

Development environment setup script that:
- Checks Python version compatibility
- Installs build tools and dependencies
- Sets up pre-commit hooks
- Runs initial tests
- Provides setup verification

## Usage Examples

### Development Workflow

```bash
# Initial setup
./scripts/setup-dev.sh

# Make changes, then
python3 scripts/build.py format
python3 scripts/build.py test
python3 scripts/build.py lint

# Before committing
python3 scripts/build.py check
```

### Release Workflow

```bash
# Check current version
python3 scripts/version.py current

# See what next version would be
python3 scripts/version.py next patch

# Dry run release
python3 scripts/release.py release patch --dry-run

# Actually release
python3 scripts/release.py release patch
```

### Version Management

```bash
# List all version tags
python3 scripts/version.py list

# Create specific version tag
python3 scripts/version.py tag 1.2.3

# Push tag to remote
python3 scripts/version.py push 1.2.3
```

## Integration with Make

All scripts can be called via Make for convenience:

```bash
make help           # Show all commands
make test           # Run tests
make lint           # Run linting
make format         # Format code
make build          # Build package
make release-check  # Run all checks
make release        # Create patch release
make version        # Show current version
```

## Environment Requirements

- Python 3.10+
- Git
- Standard build tools (pip, setuptools, wheel)
- Optional: make, pre-commit

## Error Handling

All scripts include proper error handling and will:
- Exit with non-zero code on failure
- Provide meaningful error messages
- Check prerequisites before running
- Validate input parameters

## Customization

Scripts can be customized by:
- Modifying the Python scripts directly
- Setting environment variables
- Updating the `pyproject.toml` configuration
- Adding custom Make targets

## Troubleshooting

### Common Issues

1. **Permission denied**: Make scripts executable with `chmod +x scripts/*.py`
2. **Python not found**: Ensure Python 3.10+ is in PATH
3. **Git not found**: Install git and ensure it's in PATH
4. **Module not found**: Run `pip install -e .[dev,test,all]`

### Debug Mode

Enable debug output:
```bash
export TWAT_CACHE_DEBUG=1
python3 scripts/build.py test
```

## Contributing

When adding new scripts:
1. Follow the existing naming convention
2. Include proper error handling
3. Add documentation
4. Update this README
5. Test on multiple platforms

## License

Scripts are part of the twat-cache project and follow the same MIT license.