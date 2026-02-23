"""Unit tests for cvpysdk/subclients/cloudapps/__init__.py"""

import pytest

import cvpysdk.subclients.cloudapps as cloudapps_module


@pytest.mark.unit
class TestCloudAppsInit:
    """Tests for the cloudapps __init__ module."""

    def test_author_is_set(self):
        """__author__ should be set to Commvault Systems Inc."""
        assert hasattr(cloudapps_module, "__author__")
        assert cloudapps_module.__author__ == "Commvault Systems Inc."

    def test_module_is_importable(self):
        """The cloudapps module should be importable without errors."""
        assert cloudapps_module is not None

    def test_author_is_string(self):
        """__author__ should be a string."""
        assert isinstance(cloudapps_module.__author__, str)
