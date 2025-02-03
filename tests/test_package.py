"""Test suite for twat_cache."""

def test_version():
    """Verify package exposes version."""
    import twat_cache
    assert twat_cache.__version__

def test_plugin():
    """Verify plugin functionality."""
    import twat_cache
    plugin = twat_cache.Plugin()
    plugin.set("test", "value")
    assert plugin.get("test") == "value"
 