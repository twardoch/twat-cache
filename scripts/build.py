#!/usr/bin/env python3
"""
Build script for twat-cache project.
Handles building, testing, and releasing the project.
"""
# this_file: scripts/build.py

import subprocess
import sys
import os
import shutil
from pathlib import Path
from typing import Optional

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent


def run_cmd(cmd: str, cwd: Optional[Path] = None, check: bool = True) -> subprocess.CompletedProcess:
    """Run a shell command and return the result."""
    if cwd is None:
        cwd = PROJECT_ROOT
    
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, check=check)
    return result


def clean():
    """Clean build artifacts."""
    print("🧹 Cleaning build artifacts...")
    
    # Directories to clean
    dirs_to_clean = [
        "build",
        "dist", 
        "*.egg-info",
        ".pytest_cache",
        ".coverage",
        ".mypy_cache",
        "__pycache__",
    ]
    
    for pattern in dirs_to_clean:
        for path in PROJECT_ROOT.glob(pattern):
            if path.is_dir():
                print(f"Removing directory: {path}")
                shutil.rmtree(path)
            elif path.is_file():
                print(f"Removing file: {path}")
                path.unlink()
    
    # Clean Python cache recursively
    for root, dirs, files in os.walk(PROJECT_ROOT):
        for d in dirs:
            if d == "__pycache__":
                cache_path = Path(root) / d
                print(f"Removing cache: {cache_path}")
                shutil.rmtree(cache_path)


def format_code():
    """Format code using ruff."""
    print("🎨 Formatting code...")
    run_cmd("python -m ruff format .")
    run_cmd("python -m ruff check --fix .")


def lint():
    """Run linting checks."""
    print("🔍 Running linting checks...")
    run_cmd("python -m ruff check .")
    run_cmd("python -m mypy --install-types --non-interactive src/twat_cache tests")


def test():
    """Run tests."""
    print("🧪 Running tests...")
    run_cmd("python -m pytest -n auto tests")


def test_coverage():
    """Run tests with coverage."""
    print("📊 Running tests with coverage...")
    run_cmd("python -m pytest -n auto --cov-report=term-missing --cov-config=pyproject.toml --cov=src/twat_cache --cov=tests tests")


def build():
    """Build the package."""
    print("📦 Building package...")
    run_cmd("python -m build")


def install_dev():
    """Install package in development mode."""
    print("🔧 Installing in development mode...")
    run_cmd("pip install -e .[dev,test,all]")


def benchmark():
    """Run benchmarks."""
    print("⚡ Running benchmarks...")
    run_cmd("python -m pytest -v tests/test_benchmark.py --benchmark-only")


def full_check():
    """Run complete check sequence."""
    print("🚀 Running full check sequence...")
    
    steps = [
        ("Clean", clean),
        ("Format", format_code),
        ("Lint", lint),
        ("Test", test),
        ("Coverage", test_coverage),
        ("Build", build),
    ]
    
    for step_name, step_func in steps:
        print(f"\n{'='*50}")
        print(f"Step: {step_name}")
        print(f"{'='*50}")
        
        try:
            step_func()
            print(f"✅ {step_name} completed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ {step_name} failed with exit code {e.returncode}")
            sys.exit(1)
        except Exception as e:
            print(f"❌ {step_name} failed with error: {e}")
            sys.exit(1)
    
    print(f"\n{'='*50}")
    print("🎉 All checks passed! Ready for release.")
    print(f"{'='*50}")


def main():
    """Main CLI interface."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Build script for twat-cache")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add subcommands
    subparsers.add_parser('clean', help='Clean build artifacts')
    subparsers.add_parser('format', help='Format code')
    subparsers.add_parser('lint', help='Run linting checks')
    subparsers.add_parser('test', help='Run tests')
    subparsers.add_parser('coverage', help='Run tests with coverage')
    subparsers.add_parser('build', help='Build package')
    subparsers.add_parser('install-dev', help='Install in development mode')
    subparsers.add_parser('benchmark', help='Run benchmarks')
    subparsers.add_parser('check', help='Run full check sequence')
    
    args = parser.parse_args()
    
    if args.command == 'clean':
        clean()
    elif args.command == 'format':
        format_code()
    elif args.command == 'lint':
        lint()
    elif args.command == 'test':
        test()
    elif args.command == 'coverage':
        test_coverage()
    elif args.command == 'build':
        build()
    elif args.command == 'install-dev':
        install_dev()
    elif args.command == 'benchmark':
        benchmark()
    elif args.command == 'check':
        full_check()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()