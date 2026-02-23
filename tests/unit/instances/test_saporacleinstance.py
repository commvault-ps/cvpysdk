"""Unit tests for cvpysdk/instances/saporacleinstance.py"""

from unittest.mock import MagicMock

import pytest

from cvpysdk.instance import Instance


@pytest.mark.unit
class TestSAPOracleInstance:
    """Tests for the SAPOracleInstance class."""

    def test_inherits_instance(self):
        """Test that SAPOracleInstance is a subclass of Instance."""
        from cvpysdk.instances.saporacleinstance import SAPOracleInstance

        assert issubclass(SAPOracleInstance, Instance)

    def test_oracle_home_property(self):
        """Test oracle_home returns correct value."""
        from cvpysdk.instances.saporacleinstance import SAPOracleInstance

        inst = object.__new__(SAPOracleInstance)
        inst._properties = {"sapOracleInstance": {"oracleHome": "/oracle/SID/19.0.0"}}
        assert inst.oracle_home == "/oracle/SID/19.0.0"

    def test_sapdata_home_property(self):
        """Test sapdata_home returns correct value."""
        from cvpysdk.instances.saporacleinstance import SAPOracleInstance

        inst = object.__new__(SAPOracleInstance)
        inst._properties = {"sapOracleInstance": {"sapDataPath": "/oracle/SID/sapdata"}}
        assert inst.sapdata_home == "/oracle/SID/sapdata"

    def test_sapexepath_property(self):
        """Test sapexepath returns correct value."""
        from cvpysdk.instances.saporacleinstance import SAPOracleInstance

        inst = object.__new__(SAPOracleInstance)
        inst._properties = {"sapOracleInstance": {"sapExeFolder": "/usr/sap/SID/SYS/exe"}}
        assert inst.sapexepath == "/usr/sap/SID/SYS/exe"

    def test_os_user_property(self):
        """Test os_user returns correct value."""
        from cvpysdk.instances.saporacleinstance import SAPOracleInstance

        inst = object.__new__(SAPOracleInstance)
        inst._properties = {"sapOracleInstance": {"oracleUser": {"userName": "orasid"}}}
        assert inst.os_user == "orasid"

    def test_cmd_sp_property(self):
        """Test cmd_sp returns the command line storage policy name."""
        from cvpysdk.instances.saporacleinstance import SAPOracleInstance

        inst = object.__new__(SAPOracleInstance)
        inst._properties = {
            "sapOracleInstance": {
                "oracleStorageDevice": {
                    "commandLineStoragePolicy": {"storagePolicyName": "CmdLineSP"},
                    "logBackupStoragePolicy": {"storagePolicyName": "LogSP"},
                }
            }
        }
        assert inst.cmd_sp == "CmdLineSP"

    def test_log_sp_property(self):
        """Test log_sp returns the log storage policy name."""
        from cvpysdk.instances.saporacleinstance import SAPOracleInstance

        inst = object.__new__(SAPOracleInstance)
        inst._properties = {
            "sapOracleInstance": {
                "oracleStorageDevice": {
                    "logBackupStoragePolicy": {"storagePolicyName": "LogSP"},
                    "commandLineStoragePolicy": {"storagePolicyName": "CmdLineSP"},
                }
            }
        }
        assert inst.log_sp == "LogSP"

    def test_saporacle_db_user_property(self):
        """Test saporacle_db_user returns correct user."""
        from cvpysdk.instances.saporacleinstance import SAPOracleInstance

        inst = object.__new__(SAPOracleInstance)
        inst._properties = {
            "sapOracleInstance": {"sqlConnect": {"userName": "SYS", "domainName": "SID"}}
        }
        assert inst.saporacle_db_user == "SYS"

    def test_saporacle_db_connectstring_property(self):
        """Test saporacle_db_connectstring returns correct value."""
        from cvpysdk.instances.saporacleinstance import SAPOracleInstance

        inst = object.__new__(SAPOracleInstance)
        inst._properties = {
            "sapOracleInstance": {"sqlConnect": {"userName": "SYS", "domainName": "SID"}}
        }
        assert inst.saporacle_db_connectstring == "SID"

    def test_saporacle_blocksize_property(self):
        """Test saporacle_blocksize returns correct value."""
        from cvpysdk.instances.saporacleinstance import SAPOracleInstance

        inst = object.__new__(SAPOracleInstance)
        inst._properties = {"sapOracleInstance": {"blockSize": 65536}}
        assert inst.saporacle_blocksize == 65536

    def test_saporacle_instanceid_property(self):
        """Test saporacle_instanceid returns correct instance id."""
        from cvpysdk.instances.saporacleinstance import SAPOracleInstance

        inst = object.__new__(SAPOracleInstance)
        inst._properties = {"instance": {"instanceId": 42}}
        assert inst.saporacle_instanceid == 42

    def test_restore_in_place_raises_for_invalid_dest_type(self):
        """Test restore_in_place raises SDKException for invalid destination type."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.saporacleinstance import SAPOracleInstance

        inst = object.__new__(SAPOracleInstance)
        inst._agent_object = MagicMock()
        inst._commcell_object = MagicMock()
        with pytest.raises(SDKException):
            inst.restore_in_place(destination_client=12345)
