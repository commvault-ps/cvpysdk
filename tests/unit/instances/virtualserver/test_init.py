"""Unit tests for cvpysdk/instances/virtualserver/__init__.py"""

import pytest


@pytest.mark.unit
class TestVirtualServerInit:
    """Tests for the virtualserver package init module."""

    def test_module_importable(self):
        """Test that the virtualserver package can be imported."""
        import cvpysdk.instances.virtualserver

        assert cvpysdk.instances.virtualserver is not None

    def test_has_author(self):
        """Test that __author__ is set."""
        import cvpysdk.instances.virtualserver

        assert hasattr(cvpysdk.instances.virtualserver, "__author__")

    def test_author_value(self):
        """Test __author__ is Commvault Systems Inc."""
        import cvpysdk.instances.virtualserver

        assert cvpysdk.instances.virtualserver.__author__ == "Commvault Systems Inc."
