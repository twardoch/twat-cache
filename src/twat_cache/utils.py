"""Utility functions for twat_cache."""

# this_file: src/twat_cache/utils.py

from pathlib import Path

try:
    import platformdirs

    HAS_PLATFORMDIRS = True
except ImportError:
    HAS_PLATFORMDIRS = False


def get_cache_path(folder_name: str | None = None) -> Path:
    """Get the path for cache storage.

    Uses platform-specific user cache directory if platformdirs is available,
    otherwise falls back to ~/.cache.

    Args:
        folder_name: Optional subdirectory name for the cache

    Returns:
        Path object pointing to the cache directory
    """
    if HAS_PLATFORMDIRS:
        base_path = Path(platformdirs.user_cache_dir("twat_cache"))
    else:
        base_path = Path.home() / ".cache" / "twat_cache"

    if folder_name:
        base_path = base_path / folder_name

    base_path.mkdir(parents=True, exist_ok=True)
    return base_path
