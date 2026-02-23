"""Unit tests for cvpysdk/subclients/mysqlsubclient.py"""

import pytest

from cvpysdk.subclient import Subclient
from cvpysdk.subclients.mysqlsubclient import MYSQLSubclient


@pytest.mark.unit
class TestMYSQLSubclient:
    """Tests for the MYSQLSubclient class."""

    def test_inherits_subclient(self):
        """MYSQLSubclient should inherit from Subclient."""
        assert issubclass(MYSQLSubclient, Subclient)

    def test_has_key_methods(self):
        """MYSQLSubclient should have expected methods."""
        assert hasattr(MYSQLSubclient, "backup")
        assert hasattr(MYSQLSubclient, "restore_in_place")
        assert hasattr(MYSQLSubclient, "content")
        assert hasattr(MYSQLSubclient, "is_blocklevel_backup_enabled")
        assert hasattr(MYSQLSubclient, "is_proxy_enabled")
        assert hasattr(MYSQLSubclient, "is_failover_to_production")

    def test_is_blocklevel_backup_enabled(self):
        """is_blocklevel_backup_enabled should return boolean."""
        subclient = object.__new__(MYSQLSubclient)
        subclient._subclient_properties = {"mySqlSubclientProp": {"isUseBlockLevelBackup": True}}
        assert subclient.is_blocklevel_backup_enabled is True

    def test_is_blocklevel_backup_disabled(self):
        """is_blocklevel_backup_enabled should return False when not set."""
        subclient = object.__new__(MYSQLSubclient)
        subclient._subclient_properties = {"mySqlSubclientProp": {}}
        assert subclient.is_blocklevel_backup_enabled is False

    def test_is_proxy_enabled(self):
        """is_proxy_enabled should check proxySettings."""
        subclient = object.__new__(MYSQLSubclient)
        subclient._subclient_properties = {
            "mySqlSubclientProp": {"proxySettings": {"isProxyEnabled": True}}
        }
        assert subclient.is_proxy_enabled is True

    def test_is_failover_to_production(self):
        """is_failover_to_production should return the flag value."""
        subclient = object.__new__(MYSQLSubclient)
        subclient._subclient_properties = {
            "mySqlSubclientProp": {"proxySettings": {"isFailOverToProduction": True}}
        }
        assert subclient.is_failover_to_production is True

    def test_content_property(self):
        """content property should return list of database names."""
        subclient = object.__new__(MYSQLSubclient)
        subclient._content = [
            {"mySQLContent": {"databaseName": "db1"}},
            {"mySQLContent": {"databaseName": "db2"}},
        ]
        assert subclient.content == ["db1", "db2"]

    def test_backup_raises_for_invalid_level(self):
        """backup should raise SDKException for invalid backup level."""
        from cvpysdk.exception import SDKException

        subclient = object.__new__(MYSQLSubclient)
        with pytest.raises(SDKException):
            subclient.backup(backup_level="invalid_level")

    def test_restore_in_place_raises_for_non_list_paths(self):
        """restore_in_place should raise SDKException for non-list paths."""
        from cvpysdk.exception import SDKException

        subclient = object.__new__(MYSQLSubclient)
        with pytest.raises(SDKException):
            subclient.restore_in_place(paths="not_a_list")

    def test_restore_in_place_raises_for_empty_paths(self):
        """restore_in_place should raise SDKException for empty paths."""
        from cvpysdk.exception import SDKException

        subclient = object.__new__(MYSQLSubclient)
        with pytest.raises(SDKException):
            subclient.restore_in_place(paths=[])
