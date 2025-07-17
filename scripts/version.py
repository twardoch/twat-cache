#!/usr/bin/env python3
"""
Version management utilities for twat-cache.
Handles git tag-based semversioning and version operations.
"""
# this_file: scripts/version.py

import subprocess
import sys
import re
from pathlib import Path
from typing import Optional, Tuple


def run_cmd(cmd: str, check: bool = True) -> subprocess.CompletedProcess:
    """Run a shell command and return the result."""
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, check=check)


def get_current_version() -> Optional[str]:
    """Get the current version from git tags."""
    try:
        result = run_cmd("git describe --tags --abbrev=0", check=False)
        if result.returncode == 0:
            tag = result.stdout.strip()
            # Extract version from tag (remove 'v' prefix if present)
            if tag.startswith('v'):
                return tag[1:]
            return tag
    except Exception:
        pass
    return None


def get_next_version(current: str, bump_type: str = "patch") -> str:
    """Calculate the next version based on current version and bump type."""
    # Parse semantic version
    match = re.match(r'^(\d+)\.(\d+)\.(\d+)(?:-(.+))?$', current)
    if not match:
        raise ValueError(f"Invalid version format: {current}")
    
    major, minor, patch = map(int, match.groups()[:3])
    
    if bump_type == "major":
        return f"{major + 1}.0.0"
    elif bump_type == "minor":
        return f"{major}.{minor + 1}.0"
    elif bump_type == "patch":
        return f"{major}.{minor}.{patch + 1}"
    else:
        raise ValueError(f"Invalid bump type: {bump_type}")


def create_tag(version: str, message: str = None) -> bool:
    """Create a new git tag for the given version."""
    tag = f"v{version}"
    
    if message is None:
        message = f"Release version {version}"
    
    try:
        # Create annotated tag
        run_cmd(f'git tag -a {tag} -m "{message}"')
        print(f"Created tag: {tag}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error creating tag: {e}")
        return False


def push_tag(version: str) -> bool:
    """Push a tag to remote repository."""
    tag = f"v{version}"
    
    try:
        run_cmd(f"git push origin {tag}")
        print(f"Pushed tag: {tag}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error pushing tag: {e}")
        return False


def list_tags() -> list:
    """List all version tags."""
    try:
        result = run_cmd("git tag -l 'v*' --sort=-version:refname")
        return [tag.strip() for tag in result.stdout.splitlines() if tag.strip()]
    except Exception:
        return []


def main():
    """Main CLI interface."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Version management for twat-cache")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Current version
    subparsers.add_parser('current', help='Show current version')
    
    # Next version
    next_parser = subparsers.add_parser('next', help='Calculate next version')
    next_parser.add_argument('bump_type', choices=['major', 'minor', 'patch'], 
                            default='patch', nargs='?', help='Type of version bump')
    
    # Create tag
    tag_parser = subparsers.add_parser('tag', help='Create a new version tag')
    tag_parser.add_argument('version', help='Version to tag')
    tag_parser.add_argument('-m', '--message', help='Tag message')
    
    # Push tag
    push_parser = subparsers.add_parser('push', help='Push version tag to remote')
    push_parser.add_argument('version', help='Version to push')
    
    # List tags
    subparsers.add_parser('list', help='List all version tags')
    
    args = parser.parse_args()
    
    if args.command == 'current':
        version = get_current_version()
        if version:
            print(version)
        else:
            print("No version tags found")
            sys.exit(1)
    
    elif args.command == 'next':
        current = get_current_version()
        if not current:
            print("0.1.0")  # Initial version
        else:
            print(get_next_version(current, args.bump_type))
    
    elif args.command == 'tag':
        if create_tag(args.version, args.message):
            sys.exit(0)
        else:
            sys.exit(1)
    
    elif args.command == 'push':
        if push_tag(args.version):
            sys.exit(0)
        else:
            sys.exit(1)
    
    elif args.command == 'list':
        tags = list_tags()
        for tag in tags:
            print(tag)
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()