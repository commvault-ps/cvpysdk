"""Tests for cvpysdk/backupsets/_virtual_server/__init__.py"""

import pytest

import cvpysdk.backupsets._virtual_server as vs_pkg


@pytest.mark.unit
class TestVirtualServerBackupsetsInit:
    def test_module_has_author(self):
        assert hasattr(vs_pkg, "__author__")

    def test_author_is_commvault(self):
        assert vs_pkg.__author__ == "Commvault Systems Inc."

    def test_module_docstring_exists(self):
        assert vs_pkg.__doc__ is not None

    def test_module_is_importable(self):
        from cvpysdk.backupsets import _virtual_server  # noqa: F401

        assert _virtual_server is not None
