"""Unit tests for cvpysdk/instances/virtualserver/oracle_cloud.py"""

import pytest

from cvpysdk.instances.vsinstance import VirtualServerInstance


@pytest.mark.unit
class TestOracleCloudInstance:
    """Tests for the OracleCloudInstance class."""

    def test_inherits_virtual_server_instance(self):
        """Test that OracleCloudInstance is a subclass of VirtualServerInstance."""
        from cvpysdk.instances.virtualserver.oracle_cloud import OracleCloudInstance

        assert issubclass(OracleCloudInstance, VirtualServerInstance)

    def test_server_name_property(self):
        """Test server_name returns the server name list."""
        from cvpysdk.instances.virtualserver.oracle_cloud import OracleCloudInstance

        inst = object.__new__(OracleCloudInstance)
        inst._server_name = ["oc_proxy"]
        assert inst.server_name == ["oc_proxy"]

    def test_server_host_name_property(self):
        """Test server_host_name returns the host name."""
        from cvpysdk.instances.virtualserver.oracle_cloud import OracleCloudInstance

        inst = object.__new__(OracleCloudInstance)
        inst._server_host_name = ["cloud.oracle.com"]
        assert inst.server_host_name == ["cloud.oracle.com"]

    def test_instance_username_property(self):
        """Test instance_username returns the username."""
        from cvpysdk.instances.virtualserver.oracle_cloud import OracleCloudInstance

        inst = object.__new__(OracleCloudInstance)
        inst._username = "oc_admin"
        assert inst.instance_username == "oc_admin"

    def test_get_instance_properties_json_has_xen_server(self):
        """Test _get_instance_properties_json includes xenServer key."""
        from cvpysdk.instances.virtualserver.oracle_cloud import OracleCloudInstance

        inst = object.__new__(OracleCloudInstance)
        inst._instance = {"clientName": "oc_client"}
        inst._instanceActivityControl = {"enableBackup": True}
        inst._virtualserverinstance = {
            "vsInstanceType": 13,
            "associatedClients": {"memberServers": []},
            "vmwareVendor": {},
        }
        result = inst._get_instance_properties_json()
        vs = result["instanceProperties"]["virtualServerInstance"]
        assert "xenServer" in vs
