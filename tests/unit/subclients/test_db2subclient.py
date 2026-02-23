"""Unit tests for cvpysdk/subclients/db2subclient.py"""

import pytest

from cvpysdk.subclient import Subclient
from cvpysdk.subclients.db2subclient import DB2Subclient


@pytest.mark.unit
class TestDB2Subclient:
    """Tests for the DB2Subclient class."""

    def test_inherits_subclient(self):
        """DB2Subclient should inherit from Subclient."""
        assert issubclass(DB2Subclient, Subclient)

    def test_has_key_methods(self):
        """DB2Subclient should have expected methods and properties."""
        assert hasattr(DB2Subclient, "db2_use_dedupe_device")
        assert hasattr(DB2Subclient, "db2_delete_log_files_after")
        assert hasattr(DB2Subclient, "db2_backup_log_files")
        assert hasattr(DB2Subclient, "is_backup_data_enabled")
        assert hasattr(DB2Subclient, "enable_backupdata")
        assert hasattr(DB2Subclient, "disable_backupdata")
        assert hasattr(DB2Subclient, "enable_table_level")
        assert hasattr(DB2Subclient, "enable_acs_backup")
        assert hasattr(DB2Subclient, "db2_backup")

    def test_db2_use_dedupe_device_property(self):
        """db2_use_dedupe_device should read from properties."""
        subclient = object.__new__(DB2Subclient)
        subclient._properties = {"db2SubclientProp": {"db2UseDedupeDevice": True}}
        assert subclient.db2_use_dedupe_device is True

    def test_db2_delete_log_files_after_property(self):
        """db2_delete_log_files_after should read from subclient properties."""
        subclient = object.__new__(DB2Subclient)
        subclient._subclient_properties = {"db2SubclientProp": {"db2DeleteLogFilesAfter": False}}
        assert subclient.db2_delete_log_files_after is False

    def test_db2_backup_log_files_property(self):
        """db2_backup_log_files should read from subclient properties."""
        subclient = object.__new__(DB2Subclient)
        subclient._subclient_properties = {"db2SubclientProp": {"db2BackupLogFiles": True}}
        assert subclient.db2_backup_log_files is True

    def test_is_backup_data_enabled_defaults_true(self):
        """is_backup_data_enabled should default to True when key is absent."""
        subclient = object.__new__(DB2Subclient)
        subclient._subclient_properties = {"db2SubclientProp": {}}
        assert subclient.is_backup_data_enabled is True

    def test_backup_mode_online_property(self):
        """backup_mode_online should return backup mode value."""
        subclient = object.__new__(DB2Subclient)
        subclient._subclient_properties = {"db2SubclientProp": {"db2BackupMode": 1}}
        assert subclient.backup_mode_online == 1

    def test_db2_backup_raises_for_invalid_level(self):
        """db2_backup should raise SDKException for invalid backup level."""
        from cvpysdk.exception import SDKException

        subclient = object.__new__(DB2Subclient)
        with pytest.raises(SDKException):
            subclient.db2_backup(backup_level="invalid")

    def test_db2_backup_raises_for_backup_copy_with_non_full(self):
        """db2_backup should raise SDKException for backup copy with non-full level."""
        from cvpysdk.exception import SDKException

        subclient = object.__new__(DB2Subclient)
        with pytest.raises(SDKException):
            subclient.db2_backup(
                backup_level="incremental",
                create_backup_copy_immediately=True,
            )
