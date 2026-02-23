"""Unit tests for cvpysdk/instances/virtualserver/oraclevm.py"""

import pytest

from cvpysdk.instances.vsinstance import VirtualServerInstance


@pytest.mark.unit
class TestOracleVMInstance:
    """Tests for the OracleVMInstance class."""

    def test_inherits_virtual_server_instance(self):
        """Test that OracleVMInstance is a subclass of VirtualServerInstance."""
        from cvpysdk.instances.virtualserver.oraclevm import OracleVMInstance

        assert issubclass(OracleVMInstance, VirtualServerInstance)

    def test_server_name_property(self):
        """Test server_name returns the server name list."""
        from cvpysdk.instances.virtualserver.oraclevm import OracleVMInstance

        inst = object.__new__(OracleVMInstance)
        inst._server_name = ["ovm_pseudo"]
        assert inst.server_name == ["ovm_pseudo"]

    def test_server_host_name_property(self):
        """Test server_host_name returns the host name list."""
        from cvpysdk.instances.virtualserver.oraclevm import OracleVMInstance

        inst = object.__new__(OracleVMInstance)
        inst._server_host_name = ["ovm.example.com"]
        assert inst.server_host_name == ["ovm.example.com"]

    def test_get_instance_properties_json_structure(self):
        """Test _get_instance_properties_json returns correct structure."""
        from cvpysdk.instances.virtualserver.oraclevm import OracleVMInstance

        inst = object.__new__(OracleVMInstance)
        inst._instance = {"clientName": "ovm_client"}
        inst._instanceActivityControl = {"enableBackup": True}
        inst._virtualserverinstance = {
            "vsInstanceType": 10,
            "associatedClients": {"memberServers": []},
        }
        result = inst._get_instance_properties_json()
        assert result["instanceProperties"]["virtualServerInstance"]["vsInstanceType"] == 10
