"""Unit tests for cvpysdk/instances/__init__.py"""

import pytest


@pytest.mark.unit
class TestInstancesInit:
    """Tests for the instances __init__ module."""

    def test_module_imports(self):
        """Test that the instances package can be imported."""
        import cvpysdk.instances  # noqa: F401

    def test_author_attribute(self):
        """Test that __author__ is set."""
        import cvpysdk.instances

        assert hasattr(cvpysdk.instances, "__author__")
        assert cvpysdk.instances.__author__ == "Commvault Systems Inc."
