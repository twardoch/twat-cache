"""Path management utilities for twat_cache."""

import inspect
import uuid
from functools import cache
from pathlib import Path

from twat.paths import PathManager


@cache
def get_cache_path(folder_name: str | None = None) -> Path:
    """Get a platform-specific cache directory path.

    Args:
        folder_name: Optional subdirectory name. If None, generates a UUID based on caller.

    Returns:
        Path to the cache directory
    """

    def generate_uuid() -> str:
        """Generate a UUID based on the file of the caller."""
        # Get the stack frame of the caller (2 levels up to skip this function)
        caller_frame = inspect.stack()[2]
        caller_file = caller_frame.filename
        caller_path = Path(caller_file).resolve()
        return str(uuid.uuid5(uuid.NAMESPACE_URL, str(caller_path)))

    # Get base cache directory from central path management
    paths = PathManager.for_package("twat_cache")
    base_cache_dir = paths.cache.package_dir or paths.cache.base_dir

    if folder_name is None:
        folder_name = generate_uuid()

    cache_path = base_cache_dir / folder_name
    cache_path.mkdir(parents=True, exist_ok=True)

    return cache_path
