"""Tests for cvpysdk/backupsets/__init__.py"""

import pytest

import cvpysdk.backupsets as backupsets_pkg


@pytest.mark.unit
class TestBackupsetsInit:
    def test_module_has_author(self):
        assert hasattr(backupsets_pkg, "__author__")

    def test_author_is_commvault(self):
        assert backupsets_pkg.__author__ == "Commvault Systems Inc."

    def test_module_docstring_exists(self):
        assert backupsets_pkg.__doc__ is not None

    def test_module_is_importable(self):
        from cvpysdk import backupsets  # noqa: F401

        assert backupsets is not None
