"""Unit tests for cvpysdk/instances/db2instance.py"""

import pytest

from cvpysdk.instance import Instance


@pytest.mark.unit
class TestDB2Instance:
    """Tests for the DB2Instance class."""

    def test_inherits_instance(self):
        """Test that DB2Instance is a subclass of Instance."""
        from cvpysdk.instances.db2instance import DB2Instance

        assert issubclass(DB2Instance, Instance)

    def test_version_property(self):
        """Test version property returns db2 version."""
        from cvpysdk.instances.db2instance import DB2Instance

        inst = object.__new__(DB2Instance)
        inst._properties = {"version": "11.5"}
        assert inst.version == "11.5"

    def test_version_property_empty(self):
        """Test version property returns empty string when not set."""
        from cvpysdk.instances.db2instance import DB2Instance

        inst = object.__new__(DB2Instance)
        inst._properties = {}
        assert inst.version == ""

    def test_home_directory_property(self):
        """Test home_directory property returns db2 home."""
        from cvpysdk.instances.db2instance import DB2Instance

        inst = object.__new__(DB2Instance)
        inst._properties = {"db2Instance": {"homeDirectory": "/home/db2inst1"}}
        assert inst.home_directory == "/home/db2inst1"

    def test_user_name_property(self):
        """Test user_name property returns db2 user."""
        from cvpysdk.instances.db2instance import DB2Instance

        inst = object.__new__(DB2Instance)
        inst._properties = {"db2Instance": {"userAccount": {"userName": "db2admin"}}}
        assert inst.user_name == "db2admin"

    def test_data_backup_storage_policy(self):
        """Test data_backup_storage_policy property."""
        from cvpysdk.instances.db2instance import DB2Instance

        inst = object.__new__(DB2Instance)
        inst._properties = {
            "db2Instance": {
                "DB2StorageDevice": {"dataBackupStoragePolicy": {"storagePolicyName": "sp1"}}
            }
        }
        assert inst.data_backup_storage_policy == "sp1"

    def test_log_backup_storage_policy(self):
        """Test log_backup_storage_policy property."""
        from cvpysdk.instances.db2instance import DB2Instance

        inst = object.__new__(DB2Instance)
        inst._properties = {
            "db2Instance": {
                "DB2StorageDevice": {"logBackupStoragePolicy": {"storagePolicyName": "log_sp1"}}
            }
        }
        assert inst.log_backup_storage_policy == "log_sp1"

    def test_restore_destination_json_raises_on_non_dict(self):
        """Test _restore_destination_json raises SDKException for non-dict input."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.db2instance import DB2Instance

        inst = object.__new__(DB2Instance)
        with pytest.raises(SDKException):
            inst._restore_destination_json("not_a_dict")

    def test_db2_restore_options_json_raises_on_non_dict(self):
        """Test _db2_restore_options_json raises SDKException for non-dict input."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.db2instance import DB2Instance

        inst = object.__new__(DB2Instance)
        with pytest.raises(SDKException):
            inst._db2_restore_options_json("not_a_dict")
