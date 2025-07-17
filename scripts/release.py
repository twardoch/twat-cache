#!/usr/bin/env python3
"""
Release script for twat-cache project.
Handles version bumping, tagging, and releasing to PyPI.
"""
# this_file: scripts/release.py

import subprocess
import sys
import os
from pathlib import Path
from typing import Optional

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Import our version utilities
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
from version import get_current_version, get_next_version, create_tag, push_tag
from build import full_check, clean, build


def run_cmd(cmd: str, cwd: Optional[Path] = None, check: bool = True) -> subprocess.CompletedProcess:
    """Run a shell command and return the result."""
    if cwd is None:
        cwd = PROJECT_ROOT
    
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, check=check)
    return result


def check_git_status():
    """Check if git working directory is clean."""
    print("🔍 Checking git status...")
    result = run_cmd("git status --porcelain", check=False)
    
    if result.stdout.strip():
        print("❌ Git working directory is not clean. Please commit or stash changes.")
        print("Uncommitted changes:")
        print(result.stdout)
        return False
    
    print("✅ Git working directory is clean")
    return True


def check_main_branch():
    """Check if we're on the main branch."""
    print("🔍 Checking current branch...")
    result = run_cmd("git branch --show-current", check=False)
    current_branch = result.stdout.strip()
    
    if current_branch != "main":
        print(f"❌ Currently on branch '{current_branch}'. Please switch to 'main' branch for releases.")
        return False
    
    print("✅ On main branch")
    return True


def pull_latest():
    """Pull latest changes from remote."""
    print("📥 Pulling latest changes...")
    try:
        run_cmd("git pull origin main")
        print("✅ Successfully pulled latest changes")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to pull latest changes")
        return False


def publish_to_pypi(test: bool = False):
    """Publish package to PyPI."""
    target = "Test PyPI" if test else "PyPI"
    print(f"📤 Publishing to {target}...")
    
    # Install/upgrade twine if needed
    run_cmd("pip install --upgrade twine")
    
    if test:
        # Publish to Test PyPI
        run_cmd("python -m twine upload --repository testpypi dist/*")
    else:
        # Publish to PyPI
        run_cmd("python -m twine upload dist/*")
    
    print(f"✅ Successfully published to {target}")


def create_github_release(version: str, changelog: str = None):
    """Create a GitHub release."""
    print("🚀 Creating GitHub release...")
    
    # Check if gh CLI is available
    try:
        run_cmd("gh --version", check=False)
    except:
        print("⚠️  GitHub CLI not found. Skipping GitHub release creation.")
        print("   You can manually create a release at: https://github.com/twardoch/twat/releases")
        return
    
    tag = f"v{version}"
    title = f"Release {version}"
    
    if changelog:
        notes = changelog
    else:
        notes = f"Release version {version}"
    
    try:
        # Create release
        run_cmd(f'gh release create {tag} --title "{title}" --notes "{notes}" ./dist/*')
        print("✅ GitHub release created successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to create GitHub release")
        print("   You can manually create a release at: https://github.com/twardoch/twat/releases")


def release(bump_type: str = "patch", dry_run: bool = False, test_pypi: bool = False):
    """Main release workflow."""
    print(f"🚀 Starting release process (bump: {bump_type})")
    
    if dry_run:
        print("🔍 DRY RUN MODE - No actual changes will be made")
    
    # Pre-release checks
    if not check_git_status():
        sys.exit(1)
    
    if not check_main_branch():
        sys.exit(1)
    
    if not pull_latest():
        sys.exit(1)
    
    # Determine next version
    current_version = get_current_version()
    if current_version:
        next_version = get_next_version(current_version, bump_type)
        print(f"📈 Version bump: {current_version} → {next_version}")
    else:
        next_version = "0.1.0"
        print(f"📈 Initial version: {next_version}")
    
    if dry_run:
        print(f"🔍 Would create tag: v{next_version}")
        return
    
    # Run full check
    print("🧪 Running full check sequence...")
    full_check()
    
    # Create and push tag
    if not create_tag(next_version):
        sys.exit(1)
    
    if not push_tag(next_version):
        sys.exit(1)
    
    # Publish to PyPI
    if test_pypi:
        publish_to_pypi(test=True)
    else:
        publish_to_pypi(test=False)
    
    # Create GitHub release
    create_github_release(next_version)
    
    print(f"\n{'='*50}")
    print(f"🎉 Release {next_version} completed successfully!")
    print(f"{'='*50}")
    print(f"📦 Package published to {'Test PyPI' if test_pypi else 'PyPI'}")
    print(f"🏷️  Tag: v{next_version}")
    print(f"📱 GitHub release created")


def main():
    """Main CLI interface."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Release script for twat-cache")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Release command
    release_parser = subparsers.add_parser('release', help='Create a new release')
    release_parser.add_argument('bump_type', choices=['major', 'minor', 'patch'], 
                               default='patch', nargs='?', help='Type of version bump')
    release_parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')
    release_parser.add_argument('--test-pypi', action='store_true', help='Publish to Test PyPI instead of PyPI')
    
    # Pre-release checks
    subparsers.add_parser('check', help='Run pre-release checks')
    
    args = parser.parse_args()
    
    if args.command == 'release':
        release(args.bump_type, args.dry_run, args.test_pypi)
    elif args.command == 'check':
        if check_git_status() and check_main_branch() and pull_latest():
            print("✅ All pre-release checks passed")
        else:
            sys.exit(1)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()