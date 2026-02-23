"""Unit tests for cvpysdk.monitoringapps.__init__ module."""

import pytest


@pytest.mark.unit
class TestMonitoringAppsInit:
    """Tests for the monitoringapps package __init__."""

    def test_import_monitoringapps_package(self):
        """Test that the monitoringapps package is importable."""
        import cvpysdk.monitoringapps

        assert hasattr(cvpysdk.monitoringapps, "__author__")

    def test_author_attribute(self):
        """Test __author__ is set correctly."""
        from cvpysdk.monitoringapps import __author__

        assert __author__ == "Commvault Systems Inc."
