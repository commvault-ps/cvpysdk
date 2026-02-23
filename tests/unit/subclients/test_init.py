"""Unit tests for cvpysdk/subclients/__init__.py"""

import pytest


@pytest.mark.unit
class TestSubclientsInit:
    """Tests for the subclients __init__ module."""

    def test_module_importable(self):
        """Verify the subclients package can be imported."""
        import cvpysdk.subclients

        assert hasattr(cvpysdk.subclients, "__author__")

    def test_author_attribute(self):
        """Verify __author__ is set correctly."""
        from cvpysdk.subclients import __author__

        assert __author__ == "Commvault Systems Inc."
