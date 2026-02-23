"""Unit tests for cvpysdk.datacube.__init__ module."""

import pytest

import cvpysdk.datacube


@pytest.mark.unit
class TestDatacubeInit:
    """Tests for the datacube package initialization."""

    def test_module_has_author(self):
        """Verify that the module defines __author__."""
        assert hasattr(cvpysdk.datacube, "__author__")
        assert cvpysdk.datacube.__author__ == "Commvault Systems Inc."

    def test_module_is_importable(self):
        """Verify the datacube package can be imported."""
        assert cvpysdk.datacube is not None
