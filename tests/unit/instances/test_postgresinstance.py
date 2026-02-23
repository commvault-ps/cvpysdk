"""Unit tests for cvpysdk/instances/postgresinstance.py"""

import pytest

from cvpysdk.instance import Instance


@pytest.mark.unit
class TestPostgreSQLInstance:
    """Tests for the PostgreSQLInstance class."""

    def test_inherits_instance(self):
        """Test that PostgreSQLInstance is a subclass of Instance."""
        from cvpysdk.instances.postgresinstance import PostgreSQLInstance

        assert issubclass(PostgreSQLInstance, Instance)

    def test_postgres_bin_directory_returns_value(self):
        """Test postgres_bin_directory property returns the binary directory."""
        from cvpysdk.instances.postgresinstance import PostgreSQLInstance

        inst = object.__new__(PostgreSQLInstance)
        inst._properties = {
            "postGreSQLInstance": {"BinaryDirectory": "/usr/lib/postgresql/14/bin"}
        }
        assert inst.postgres_bin_directory == "/usr/lib/postgresql/14/bin"

    def test_postgres_bin_directory_raises_when_empty(self):
        """Test postgres_bin_directory raises SDKException when empty."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.postgresinstance import PostgreSQLInstance

        inst = object.__new__(PostgreSQLInstance)
        inst._properties = {"postGreSQLInstance": {"BinaryDirectory": ""}}
        with pytest.raises(SDKException):
            _ = inst.postgres_bin_directory

    def test_postgres_lib_directory_returns_value(self):
        """Test postgres_lib_directory property returns the lib directory."""
        from cvpysdk.instances.postgresinstance import PostgreSQLInstance

        inst = object.__new__(PostgreSQLInstance)
        inst._properties = {"postGreSQLInstance": {"LibDirectory": "/usr/lib/postgresql/14/lib"}}
        assert inst.postgres_lib_directory == "/usr/lib/postgresql/14/lib"

    def test_log_storage_policy_returns_value(self):
        """Test log_storage_policy returns the storage policy name."""
        from cvpysdk.instances.postgresinstance import PostgreSQLInstance

        inst = object.__new__(PostgreSQLInstance)
        inst._properties = {
            "postGreSQLInstance": {"logStoragePolicy": {"storagePolicyName": "my_sp"}}
        }
        assert inst.log_storage_policy == "my_sp"

    def test_log_storage_policy_returns_none_when_missing(self):
        """Test log_storage_policy returns None when not set."""
        from cvpysdk.instances.postgresinstance import PostgreSQLInstance

        inst = object.__new__(PostgreSQLInstance)
        inst._properties = {"postGreSQLInstance": {}}
        assert inst.log_storage_policy is None

    def test_log_storage_policy_setter_raises_for_non_string(self):
        """Test log_storage_policy setter raises SDKException for non-string."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.postgresinstance import PostgreSQLInstance

        inst = object.__new__(PostgreSQLInstance)
        inst._properties = {"postGreSQLInstance": {}}
        with pytest.raises(SDKException):
            inst.log_storage_policy = 123

    def test_archive_delete_returns_false_by_default(self):
        """Test archive_delete returns False when not set."""
        from cvpysdk.instances.postgresinstance import PostgreSQLInstance

        inst = object.__new__(PostgreSQLInstance)
        inst._properties = {"postGreSQLInstance": {}}
        assert inst.archive_delete is False

    def test_archive_delete_returns_true_when_enabled(self):
        """Test archive_delete returns True when enabled."""
        from cvpysdk.instances.postgresinstance import PostgreSQLInstance

        inst = object.__new__(PostgreSQLInstance)
        inst._properties = {"postGreSQLInstance": {"ArchiveDelete": True}}
        assert inst.archive_delete is True

    def test_archive_delete_setter_raises_for_non_bool(self):
        """Test archive_delete setter raises SDKException for non-bool."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.postgresinstance import PostgreSQLInstance

        inst = object.__new__(PostgreSQLInstance)
        inst._properties = {"postGreSQLInstance": {}}
        with pytest.raises(SDKException):
            inst.archive_delete = "yes"

    def test_ssl_properties(self):
        """Test SSL-related properties return correct values."""
        from cvpysdk.instances.postgresinstance import PostgreSQLInstance

        inst = object.__new__(PostgreSQLInstance)
        inst._properties = {
            "postGreSQLInstance": {
                "sslOpt": {
                    "sslEnabled": True,
                    "sslCa": "/path/ca.pem",
                    "sslKey": "/path/key.pem",
                    "sslCert": "/path/cert.pem",
                }
            }
        }
        assert inst.postgres_ssl_status is True
        assert inst.postgres_ssl_ca_file == "/path/ca.pem"
        assert inst.postgres_ssl_key_file == "/path/key.pem"
        assert inst.postgres_ssl_cert_file == "/path/cert.pem"

    def test_change_sa_password_raises_for_non_string(self):
        """Test change_sa_password raises SDKException for non-string input."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.postgresinstance import PostgreSQLInstance

        inst = object.__new__(PostgreSQLInstance)
        with pytest.raises(SDKException):
            inst.change_sa_password(12345)

    def test_restore_in_place_raises_for_non_list_path(self):
        """Test restore_in_place raises SDKException for non-list path."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.postgresinstance import PostgreSQLInstance

        inst = object.__new__(PostgreSQLInstance)
        with pytest.raises(SDKException):
            inst.restore_in_place(
                path="not_a_list",
                dest_client_name="client1",
                dest_instance_name="inst1",
                backupset_name="bs1",
                backupset_flag=True,
            )

    def test_restore_in_place_raises_for_empty_path(self):
        """Test restore_in_place raises SDKException for empty path list."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.postgresinstance import PostgreSQLInstance

        inst = object.__new__(PostgreSQLInstance)
        with pytest.raises(SDKException):
            inst.restore_in_place(
                path=[],
                dest_client_name="client1",
                dest_instance_name="inst1",
                backupset_name="bs1",
                backupset_flag=True,
            )

    def test_standby_properties_when_disabled(self):
        """Test standby properties return None when standby is not enabled."""
        from cvpysdk.instances.postgresinstance import PostgreSQLInstance

        inst = object.__new__(PostgreSQLInstance)
        inst._properties = {"postGreSQLInstance": {}}
        assert inst.standby_instance_name is None
        assert inst.standby_instance_id is None
        assert inst.is_standby_enabled is False

    def test_use_master_for_log_backup_default(self):
        """Test use_master_for_log_backup returns False by default."""
        from cvpysdk.instances.postgresinstance import PostgreSQLInstance

        inst = object.__new__(PostgreSQLInstance)
        inst._properties = {"postGreSQLInstance": {}}
        assert inst.use_master_for_log_backup is False

    def test_use_master_for_data_backup_default(self):
        """Test use_master_for_data_backup returns False by default."""
        from cvpysdk.instances.postgresinstance import PostgreSQLInstance

        inst = object.__new__(PostgreSQLInstance)
        inst._properties = {"postGreSQLInstance": {}}
        assert inst.use_master_for_data_backup is False

    def test_restore_postgres_option_json_raises_for_non_dict(self):
        """Test _restore_postgres_option_json raises SDKException for non-dict."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.postgresinstance import PostgreSQLInstance

        inst = object.__new__(PostgreSQLInstance)
        with pytest.raises(SDKException):
            inst._restore_postgres_option_json("not_a_dict")

    def test_restore_postgres_option_json_basic(self):
        """Test _restore_postgres_option_json sets correct basic options."""
        from cvpysdk.instances.postgresinstance import PostgreSQLInstance

        inst = object.__new__(PostgreSQLInstance)
        inst._restore_postgres_option_json({"backupset_flag": True})
        assert inst.postgres_restore_json["restoreToSameServer"] is False
        assert inst.postgres_restore_json["fsBackupSetRestore"] is True
        assert inst.postgres_restore_json["tableLevelRestore"] is False
