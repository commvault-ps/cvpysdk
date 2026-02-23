"""Unit tests for cvpysdk/instances/sybaseinstance.py"""

import pytest

from cvpysdk.instances.dbinstance import DatabaseInstance


@pytest.mark.unit
class TestSybaseInstance:
    """Tests for the SybaseInstance class."""

    def test_inherits_database_instance(self):
        """Test that SybaseInstance is a subclass of DatabaseInstance."""
        from cvpysdk.instances.sybaseinstance import SybaseInstance

        assert issubclass(SybaseInstance, DatabaseInstance)

    def test_restore_common_options_json_raises_for_non_dict(self):
        """Test _restore_common_options_json raises SDKException for non-dict input."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.sybaseinstance import SybaseInstance

        inst = object.__new__(SybaseInstance)
        with pytest.raises(SDKException):
            inst._restore_common_options_json("not_a_dict")

    def test_restore_common_options_json_sets_values(self):
        """Test _restore_common_options_json sets correct values from dict."""
        from cvpysdk.instances.sybaseinstance import SybaseInstance

        inst = object.__new__(SybaseInstance)
        inst._restore_common_options_json(
            {
                "index_free_restore": True,
                "restore_to_disk": False,
                "sybase_create_device": True,
            }
        )
        assert inst._commonoption_restore_json["indexFreeRestore"] is True
        assert inst._commonoption_restore_json["restoreToDisk"] is False
        assert inst._commonoption_restore_json["sybaseCreateDevices"] is True

    def test_restore_destination_json_raises_for_non_dict(self):
        """Test _restore_destination_json raises SDKException for non-dict input."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.sybaseinstance import SybaseInstance

        inst = object.__new__(SybaseInstance)
        with pytest.raises(SDKException):
            inst._restore_destination_json(42)

    def test_restore_destination_json_sets_values(self):
        """Test _restore_destination_json populates destination restore JSON."""
        from cvpysdk.instances.sybaseinstance import SybaseInstance

        inst = object.__new__(SybaseInstance)
        inst._restore_destination_json(
            {
                "destination_client": "client1",
                "destination_instance_name": "inst1",
                "destination_path": "/restore/path",
            }
        )
        dest = inst._destination_restore_json
        assert dest["destinationInstance"]["clientName"] == "client1"
        assert dest["destinationInstance"]["instanceName"] == "inst1"
        assert dest["destinationInstance"]["appName"] == "Sybase"
        assert dest["destClient"]["clientName"] == "client1"
        assert dest["destPath"] == ["/restore/path"]

    def test_restore_sybase_option_json_raises_for_non_dict(self):
        """Test _restore_sybase_option_json raises SDKException for non-dict."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.sybaseinstance import SybaseInstance

        inst = object.__new__(SybaseInstance)
        with pytest.raises(SDKException):
            inst._restore_sybase_option_json([1, 2, 3])

    def test_sybase_properties_non_hadr(self):
        """Test property accessors for non-HADR instance."""
        from cvpysdk.instances.sybaseinstance import SybaseInstance

        inst = object.__new__(SybaseInstance)
        inst._is_hadr = False
        inst._properties = {
            "sybaseInstance": {
                "sybaseHome": "/opt/sybase",
                "enableAutoDiscovery": True,
                "localAdministrator": {"userName": "admin"},
                "saUser": {"userName": "sa"},
                "backupServer": "BS_SYB",
                "sybaseOCS": "/opt/sybase/OCS",
                "sybaseASE": "/opt/sybase/ASE",
                "sybaseBlockSize": 4096,
                "configFile": "/opt/sybase/sybase.cfg",
                "sharedMemoryDirectory": "/opt/sybase/shared",
            },
            "instance": {"instanceName": "SYBASE_INST"},
            "version": "16.0",
        }
        assert inst.sybase_home == "/opt/sybase"
        assert inst.sybase_instance_name == "SYBASE_INST"
        assert inst.is_discovery_enabled is True
        assert inst.localadmin_user == "admin"
        assert inst.sa_user == "sa"
        assert inst.version == "16.0"
        assert inst.backup_server == "BS_SYB"
        assert inst.sybase_ocs == "/opt/sybase/OCS"
        assert inst.sybase_ase == "/opt/sybase/ASE"
        assert inst.sybase_blocksize == 4096
        assert inst.sybase_configfile == "/opt/sybase/sybase.cfg"
        assert inst.sybase_sharedmemory_directory == "/opt/sybase/shared"

    def test_get_single_database_json_basic(self):
        """Test _get_single_database_json returns correct structure."""
        from cvpysdk.instances.sybaseinstance import SybaseInstance

        inst = object.__new__(SybaseInstance)
        result = inst._get_single_database_json("testdb")
        assert result["databaseId"]["name"] == "testdb"
        assert result["associatedSubClientId"] == 0
        assert "0:0:testdb:0" in result["databaseChain"]

    def test_restore_database_raises_when_no_database_list(self):
        """Test restore_database raises SDKException when database_list is None."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.sybaseinstance import SybaseInstance

        inst = object.__new__(SybaseInstance)
        inst._properties = {"instance": {"clientName": "client1"}}
        inst._instance_name = "inst1"
        with pytest.raises(SDKException):
            inst.restore_database(database_list=None)

    def test_restore_to_disk_raises_for_non_list(self):
        """Test restore_to_disk raises SDKException when backup_job_ids is not list."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.sybaseinstance import SybaseInstance

        inst = object.__new__(SybaseInstance)
        with pytest.raises(SDKException):
            inst.restore_to_disk("client1", "/path", "not_a_list", "user", "pass")
