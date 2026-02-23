"""Unit tests for cvpysdk/instances/virtualserver/azure.py"""

import pytest

from cvpysdk.instances.vsinstance import VirtualServerInstance


@pytest.mark.unit
class TestAzureInstance:
    """Tests for the AzureInstance class."""

    def test_inherits_virtual_server_instance(self):
        """Test that AzureInstance is a subclass of VirtualServerInstance."""
        from cvpysdk.instances.virtualserver.azure import AzureInstance

        assert issubclass(AzureInstance, VirtualServerInstance)

    def test_server_name_property(self):
        """Test server_name returns the server name list."""
        from cvpysdk.instances.virtualserver.azure import AzureInstance

        inst = object.__new__(AzureInstance)
        inst._server_name = ["azure_proxy"]
        assert inst.server_name == ["azure_proxy"]

    def test_server_host_name_property(self):
        """Test server_host_name returns same as server_name."""
        from cvpysdk.instances.virtualserver.azure import AzureInstance

        inst = object.__new__(AzureInstance)
        inst._server_name = ["azure_proxy"]
        assert inst.server_host_name == ["azure_proxy"]

    def test_get_instance_properties_json_structure(self):
        """Test _get_instance_properties_json returns correct structure."""
        from cvpysdk.instances.virtualserver.azure import AzureInstance

        inst = object.__new__(AzureInstance)
        inst._instance = {"clientName": "azure_client"}
        inst._instanceActivityControl = {"enableBackup": True}
        inst._virtualserverinstance = {
            "vsInstanceType": 5,
            "associatedClients": {"memberServers": []},
        }
        result = inst._get_instance_properties_json()
        assert result["instanceProperties"]["isDeleted"] is False
        assert result["instanceProperties"]["virtualServerInstance"]["vsInstanceType"] == 5
