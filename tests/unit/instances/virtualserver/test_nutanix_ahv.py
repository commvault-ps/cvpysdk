"""Unit tests for cvpysdk/instances/virtualserver/nutanix_ahv.py"""

import pytest

from cvpysdk.instances.vsinstance import VirtualServerInstance


@pytest.mark.unit
class TestNutanixInstance:
    """Tests for the nutanixinstance class."""

    def test_inherits_virtual_server_instance(self):
        """Test that nutanixinstance is a subclass of VirtualServerInstance."""
        from cvpysdk.instances.virtualserver.nutanix_ahv import nutanixinstance

        assert issubclass(nutanixinstance, VirtualServerInstance)

    def test_server_host_name_property(self):
        """Test server_host_name returns the server name list."""
        from cvpysdk.instances.virtualserver.nutanix_ahv import nutanixinstance

        inst = object.__new__(nutanixinstance)
        inst._server_name = ["nutanix_proxy"]
        assert inst.server_host_name == ["nutanix_proxy"]

    def test_nutanix_cluster_property(self):
        """Test nutanix_cluster returns the cluster name."""
        from cvpysdk.instances.virtualserver.nutanix_ahv import nutanixinstance

        inst = object.__new__(nutanixinstance)
        inst._nutanix_cluster = "prism.example.com"
        assert inst.nutanix_cluster == "prism.example.com"

    def test_username_property(self):
        """Test username returns the cluster username."""
        from cvpysdk.instances.virtualserver.nutanix_ahv import nutanixinstance

        inst = object.__new__(nutanixinstance)
        inst._username = "admin"
        assert inst.username == "admin"

    def test_get_instance_properties_json_structure(self):
        """Test _get_instance_properties_json returns correct structure."""
        from cvpysdk.instances.virtualserver.nutanix_ahv import nutanixinstance

        inst = object.__new__(nutanixinstance)
        inst._instance = {"clientName": "nutanix_client"}
        inst._instanceActivityControl = {"enableBackup": True}
        inst._virtualserverinstance = {
            "vsInstanceType": 601,
            "associatedClients": {"memberServers": []},
        }
        result = inst._get_instance_properties_json()
        assert result["instanceProperties"]["virtualServerInstance"]["vsInstanceType"] == 601
