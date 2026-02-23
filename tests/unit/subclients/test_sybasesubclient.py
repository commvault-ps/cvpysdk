"""Unit tests for cvpysdk/subclients/sybasesubclient.py"""

import pytest

from cvpysdk.subclient import Subclient
from cvpysdk.subclients.sybasesubclient import SybaseSubclient


@pytest.mark.unit
class TestSybaseSubclient:
    """Tests for the SybaseSubclient class."""

    def test_inherits_subclient(self):
        """SybaseSubclient should inherit from Subclient."""
        assert issubclass(SybaseSubclient, Subclient)

    def test_has_key_properties(self):
        """SybaseSubclient should have expected properties."""
        assert hasattr(SybaseSubclient, "is_snapenabled")
        assert hasattr(SybaseSubclient, "snap_engine")
        assert hasattr(SybaseSubclient, "snap_proxy")
        assert hasattr(SybaseSubclient, "use_dump_based_backup_copy")
        assert hasattr(SybaseSubclient, "content")

    def test_has_key_methods(self):
        """SybaseSubclient should have expected methods."""
        assert hasattr(SybaseSubclient, "backup")
        assert hasattr(SybaseSubclient, "_get_subclient_properties")

    def test_content_property_returns_database_list(self):
        """content property should return list of database names."""
        sub = object.__new__(SybaseSubclient)
        sub._content = [
            {"sybaseContent": {"databaseName": "sybdb1"}},
            {"sybaseContent": {"databaseName": "sybdb2"}},
        ]
        result = sub.content
        assert result == ["sybdb1", "sybdb2"]

    def test_content_property_returns_empty_list(self):
        """content property should return empty list when content is empty."""
        sub = object.__new__(SybaseSubclient)
        sub._content = []
        result = sub.content
        assert result == []
