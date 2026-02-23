"""Unit tests for cvpysdk/instances/cloudapps/__init__.py"""

import pytest


@pytest.mark.unit
class TestCloudAppsInit:
    """Tests for the cloudapps __init__ module."""

    def test_module_imports(self):
        """Test that the cloudapps package can be imported."""
        import cvpysdk.instances.cloudapps  # noqa: F401

    def test_author_attribute(self):
        """Test that __author__ is set."""
        import cvpysdk.instances.cloudapps

        assert hasattr(cvpysdk.instances.cloudapps, "__author__")
        assert cvpysdk.instances.cloudapps.__author__ == "Commvault Systems Inc."
