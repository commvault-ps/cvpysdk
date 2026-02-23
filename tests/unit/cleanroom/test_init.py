"""Unit tests for cvpysdk.cleanroom.__init__ module."""

import pytest

from cvpysdk import cleanroom


@pytest.mark.unit
class TestCleanroomInit:
    """Tests for the cleanroom package __init__ module."""

    def test_package_importable(self):
        """Test that the cleanroom package can be imported."""
        assert cleanroom is not None

    def test_has_author(self):
        """Test that the package has __author__ attribute."""
        assert hasattr(cleanroom, "__author__")

    def test_author_value(self):
        """Test that __author__ is Commvault Systems Inc."""
        assert cleanroom.__author__ == "Commvault Systems Inc."
