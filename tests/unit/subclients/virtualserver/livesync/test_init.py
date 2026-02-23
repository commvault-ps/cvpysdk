"""Unit tests for cvpysdk.subclients.virtualserver.livesync.__init__ module."""

import pytest

from cvpysdk.subclients.virtualserver import livesync


@pytest.mark.unit
class TestLiveSyncInit:
    """Tests for the livesync package __init__ module."""

    def test_package_importable(self):
        """Test that the livesync package can be imported."""
        assert livesync is not None

    def test_has_author(self):
        """Test that the package has __author__ attribute."""
        assert hasattr(livesync, "__author__")

    def test_author_value(self):
        """Test that __author__ is Commvault Systems Inc."""
        assert livesync.__author__ == "Commvault Systems Inc."
