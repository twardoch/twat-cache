"""Utility functions for twat_cache."""

# this_file: src/twat_cache/utils.py

import json
from typing import Any, Callable
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

class DataclassJSONEncoder(json.JSONEncoder):
    """JSON encoder that handles dataclasses."""
    def default(self, o):
        if hasattr(o, '__dataclass_fields__'):  # Check for dataclass
            return o.__dict__
        try:
            return super().default(o)
        except TypeError:
            return str(o)  # Fallback to string representation


def make_key(*args: Any, **kwargs: Any, serializer: Callable[[Any], str] | None = None) -> str:
    """
    Create a cache key from function arguments.

    Handles unhashable types by converting them to JSON strings.  Uses a
    custom serializer if provided.
    """
    if serializer:
        return serializer((args, kwargs))

    # Use the custom encoder to handle dataclasses
    return json.dumps((args, kwargs), sort_keys=True, cls=DataclassJSONEncoder)
