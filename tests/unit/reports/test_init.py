"""Unit tests for cvpysdk.reports.__init__ module."""

import pytest


@pytest.mark.unit
class TestReportsInit:
    """Tests for the reports package __init__."""

    def test_import_reports_package(self):
        """Test that the reports package is importable."""
        import cvpysdk.reports

        assert hasattr(cvpysdk.reports, "__author__")

    def test_author_attribute(self):
        """Test __author__ is set correctly."""
        from cvpysdk.reports import __author__

        assert __author__ == "Commvault Systems Inc."
