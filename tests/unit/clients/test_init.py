"""Unit tests for cvpysdk.clients.__init__ module."""

import pytest


@pytest.mark.unit
class TestClientsInit:
    """Tests for the clients package __init__."""

    def test_import_clients_package(self):
        """Test that the clients package is importable."""
        import cvpysdk.clients

        assert hasattr(cvpysdk.clients, "__author__")

    def test_author_attribute(self):
        """Test __author__ is set correctly."""
        from cvpysdk.clients import __author__

        assert __author__ == "Commvault Systems Inc."
