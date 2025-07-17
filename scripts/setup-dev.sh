#!/bin/bash
# this_file: scripts/setup-dev.sh
# Development environment setup script for twat-cache

set -e

echo "🚀 Setting up twat-cache development environment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [[ ! -f "pyproject.toml" ]]; then
    print_error "pyproject.toml not found. Please run this script from the project root."
    exit 1
fi

# Check Python version
print_status "Checking Python version..."
python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
python_major=$(echo $python_version | cut -d'.' -f1)
python_minor=$(echo $python_version | cut -d'.' -f2)

if [[ $python_major -lt 3 ]] || [[ $python_major -eq 3 && $python_minor -lt 10 ]]; then
    print_error "Python 3.10+ required. Found: $python_version"
    exit 1
else
    print_status "Python $python_version detected ✓"
fi

# Check if git is available
if ! command -v git &> /dev/null; then
    print_error "Git is required but not installed."
    exit 1
fi

# Check if we're in a git repository
if [[ ! -d ".git" ]]; then
    print_error "Not in a git repository. Please run 'git init' first."
    exit 1
fi

# Install/upgrade pip
print_status "Upgrading pip..."
python3 -m pip install --upgrade pip

# Install build tools
print_status "Installing build tools..."
python3 -m pip install build hatch twine

# Install development dependencies
print_status "Installing development dependencies..."
python3 -m pip install -e .[dev,test,all]

# Install pre-commit hooks if available
if command -v pre-commit &> /dev/null; then
    print_status "Setting up pre-commit hooks..."
    pre-commit install
else
    print_warning "pre-commit not found. Install it with: pip install pre-commit"
fi

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p .cache/twat_cache
mkdir -p benchmark

# Run initial tests to verify installation
print_status "Running initial tests..."
if python3 -m pytest tests/test_config.py -v; then
    print_status "Initial tests passed ✓"
else
    print_warning "Some tests failed. Development environment is set up but there may be issues."
fi

# Check code formatting
print_status "Checking code formatting..."
if python3 -m ruff format --check .; then
    print_status "Code formatting is correct ✓"
else
    print_warning "Code formatting needs attention. Run: make format"
fi

# Display summary
echo ""
echo "=========================================="
echo "🎉 Development environment setup complete!"
echo "=========================================="
echo ""
echo "Available commands:"
echo "  make help          - Show all available commands"
echo "  make test          - Run tests"
echo "  make lint          - Run linting"
echo "  make format        - Format code"
echo "  make build         - Build package"
echo "  make release-check - Run pre-release checks"
echo ""
echo "To get started:"
echo "  1. Run 'make test' to verify everything works"
echo "  2. Run 'make lint' to check code quality"
echo "  3. See 'make help' for more commands"
echo ""
echo "Happy coding! 🚀"