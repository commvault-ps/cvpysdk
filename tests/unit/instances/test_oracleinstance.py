"""Unit tests for cvpysdk/instances/oracleinstance.py"""

import pytest

from cvpysdk.instances.dbinstance import DatabaseInstance


@pytest.mark.unit
class TestOracleInstance:
    """Tests for the OracleInstance class."""

    def test_inherits_database_instance(self):
        """Test that OracleInstance is a subclass of DatabaseInstance."""
        from cvpysdk.instances.oracleinstance import OracleInstance

        assert issubclass(OracleInstance, DatabaseInstance)

    def test_oracle_home_property(self):
        """Test oracle_home property."""
        from cvpysdk.instances.oracleinstance import OracleInstance

        inst = object.__new__(OracleInstance)
        inst._properties = {"oracleInstance": {"oracleHome": "/u01/app/oracle"}}
        assert inst.oracle_home == "/u01/app/oracle"

    def test_version_property(self):
        """Test version property."""
        from cvpysdk.instances.oracleinstance import OracleInstance

        inst = object.__new__(OracleInstance)
        inst._properties = {"version": "19.0.0.0"}
        assert inst.version == "19.0.0.0"

    def test_os_user_property(self):
        """Test os_user property."""
        from cvpysdk.instances.oracleinstance import OracleInstance

        inst = object.__new__(OracleInstance)
        inst._properties = {"oracleInstance": {"oracleUser": {"userName": "oracle"}}}
        assert inst.os_user == "oracle"

    def test_is_catalog_enabled_property(self):
        """Test is_catalog_enabled property."""
        from cvpysdk.instances.oracleinstance import OracleInstance

        inst = object.__new__(OracleInstance)
        inst._properties = {"oracleInstance": {"useCatalogConnect": True}}
        assert inst.is_catalog_enabled is True

    def test_catalog_user_raises_when_disabled(self):
        """Test catalog_user raises when catalog is disabled."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.oracleinstance import OracleInstance

        inst = object.__new__(OracleInstance)
        inst._properties = {"oracleInstance": {"useCatalogConnect": False}}
        with pytest.raises(SDKException):
            _ = inst.catalog_user

    def test_archive_log_dest_property(self):
        """Test archive_log_dest property."""
        from cvpysdk.instances.oracleinstance import OracleInstance

        inst = object.__new__(OracleInstance)
        inst._properties = {"oracleInstance": {"archiveLogDest": "/u01/archivelog"}}
        assert inst.archive_log_dest == "/u01/archivelog"

    def test_is_autobackup_on_true(self):
        """Test is_autobackup_on returns True when ctrlFileAutoBackup is 1."""
        from cvpysdk.instances.oracleinstance import OracleInstance

        inst = object.__new__(OracleInstance)
        inst._properties = {"oracleInstance": {"ctrlFileAutoBackup": 1}}
        assert inst.is_autobackup_on is True

    def test_is_autobackup_on_false(self):
        """Test is_autobackup_on returns False when ctrlFileAutoBackup is 0."""
        from cvpysdk.instances.oracleinstance import OracleInstance

        inst = object.__new__(OracleInstance)
        inst._properties = {"oracleInstance": {"ctrlFileAutoBackup": 0}}
        assert inst.is_autobackup_on is False

    def test_restore_to_disk_raises_for_non_list(self):
        """Test restore_to_disk raises SDKException for non-list backup_job_ids."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.oracleinstance import OracleInstance

        inst = object.__new__(OracleInstance)
        with pytest.raises(SDKException):
            inst.restore_to_disk("client", "/path", "not_a_list", "user", "pass")

    def test_dbid_property(self):
        """Test dbid property."""
        from cvpysdk.instances.oracleinstance import OracleInstance

        inst = object.__new__(OracleInstance)
        inst._properties = {"oracleInstance": {"DBID": "123456789"}}
        assert inst.dbid == "123456789"

    def test_restore_in_place_raises_for_non_list_path(self):
        """Test restore_in_place raises SDKException for non-list path."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.oracleinstance import OracleInstance

        inst = object.__new__(OracleInstance)
        with pytest.raises(SDKException):
            inst.restore_in_place("pass", "not_a_list", "client", "instance")
