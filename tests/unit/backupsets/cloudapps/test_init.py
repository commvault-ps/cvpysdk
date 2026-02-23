"""Tests for cvpysdk/backupsets/cloudapps/__init__.py"""

import pytest

import cvpysdk.backupsets.cloudapps as cloudapps_pkg


@pytest.mark.unit
class TestCloudAppsBackupsetsInit:
    def test_module_has_author(self):
        assert hasattr(cloudapps_pkg, "__author__")

    def test_author_is_commvault(self):
        assert cloudapps_pkg.__author__ == "Commvault Systems Inc."

    def test_module_docstring_exists(self):
        assert cloudapps_pkg.__doc__ is not None

    def test_module_is_importable(self):
        from cvpysdk.backupsets import cloudapps  # noqa: F401

        assert cloudapps is not None
