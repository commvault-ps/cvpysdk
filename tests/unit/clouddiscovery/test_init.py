"""Unit tests for cvpysdk.clouddiscovery.__init__ module."""

import pytest


@pytest.mark.unit
class TestCloudDiscoveryInit:
    """Tests for the clouddiscovery package __init__."""

    def test_import_clouddiscovery_package(self):
        """Test that the clouddiscovery package is importable."""
        import cvpysdk.clouddiscovery

        assert hasattr(cvpysdk.clouddiscovery, "__author__")

    def test_author_attribute(self):
        """Test __author__ is set correctly."""
        from cvpysdk.clouddiscovery import __author__

        assert __author__ == "Commvault Systems Inc."
