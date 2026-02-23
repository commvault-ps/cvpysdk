"""Unit tests for cvpysdk/__init__.py module."""

import pytest

import cvpysdk


@pytest.mark.unit
class TestInit:
    """Tests for the cvpysdk package-level attributes."""

    def test_version_is_string(self):
        assert isinstance(cvpysdk.__version__, str)

    def test_version_format(self):
        parts = cvpysdk.__version__.split(".")
        assert len(parts) >= 2
        for part in parts:
            assert part.isdigit()

    def test_author_is_string(self):
        assert isinstance(cvpysdk.__author__, str)

    def test_author_not_empty(self):
        assert len(cvpysdk.__author__) > 0
