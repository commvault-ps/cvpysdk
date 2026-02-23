"""Unit tests for cvpysdk.subclients.virtualserver.__init__ module."""

import pytest


@pytest.mark.unit
class TestVirtualServerSubclientsInit:
    """Tests for the virtualserver subclients __init__ package."""

    def test_package_importable(self):
        """Test that the virtualserver subclients package can be imported."""
        from cvpysdk.subclients import virtualserver

        assert virtualserver is not None

    def test_has_author_attribute(self):
        """Test that the package has an __author__ attribute."""
        from cvpysdk.subclients import virtualserver

        assert hasattr(virtualserver, "__author__")
        assert virtualserver.__author__ == "Commvault Systems Inc."

    def test_submodules_importable(self):
        """Test that key submodules are importable from the package."""
        from cvpysdk.subclients.virtualserver import amazon_web_services, hyperv, vmware

        assert vmware is not None
        assert amazon_web_services is not None
        assert hyperv is not None
