"""Unit tests for cvpysdk/instances/virtualserver/azure_resource_manager.py"""

import pytest

from cvpysdk.instances.vsinstance import VirtualServerInstance


@pytest.mark.unit
class TestAzureRMInstance:
    """Tests for the AzureRMInstance class."""

    def test_inherits_virtual_server_instance(self):
        """Test that AzureRMInstance is a subclass of VirtualServerInstance."""
        from cvpysdk.instances.virtualserver.azure_resource_manager import AzureRMInstance

        assert issubclass(AzureRMInstance, VirtualServerInstance)

    def test_server_name_property(self):
        """Test server_name returns the server name list."""
        from cvpysdk.instances.virtualserver.azure_resource_manager import AzureRMInstance

        inst = object.__new__(AzureRMInstance)
        inst._server_name = ["arm_proxy"]
        assert inst.server_name == ["arm_proxy"]

    def test_server_host_name_property(self):
        """Test server_host_name returns same as server_name."""
        from cvpysdk.instances.virtualserver.azure_resource_manager import AzureRMInstance

        inst = object.__new__(AzureRMInstance)
        inst._server_name = ["arm_proxy"]
        assert inst.server_host_name == ["arm_proxy"]

    def test_get_instance_properties_json_structure(self):
        """Test _get_instance_properties_json returns correct structure."""
        from cvpysdk.instances.virtualserver.azure_resource_manager import AzureRMInstance

        inst = object.__new__(AzureRMInstance)
        inst._instance = {"clientName": "arm_client"}
        inst._instanceActivityControl = {"enableBackup": True}
        inst._virtualserverinstance = {
            "vsInstanceType": 7,
            "associatedClients": {"memberServers": []},
        }
        result = inst._get_instance_properties_json()
        assert result["instanceProperties"]["virtualServerInstance"]["vsInstanceType"] == 7
