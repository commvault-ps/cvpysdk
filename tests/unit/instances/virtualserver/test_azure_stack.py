"""Unit tests for cvpysdk/instances/virtualserver/azure_stack.py"""

import pytest

from cvpysdk.instances.vsinstance import VirtualServerInstance


@pytest.mark.unit
class TestAzureStackInstance:
    """Tests for the AzureStackInstance class."""

    def test_inherits_virtual_server_instance(self):
        """Test that AzureStackInstance is a subclass of VirtualServerInstance."""
        from cvpysdk.instances.virtualserver.azure_stack import AzureStackInstance

        assert issubclass(AzureStackInstance, VirtualServerInstance)

    def test_server_host_name_property(self):
        """Test server_host_name returns the server name list."""
        from cvpysdk.instances.virtualserver.azure_stack import AzureStackInstance

        inst = object.__new__(AzureStackInstance)
        inst._server_name = ["stack_proxy"]
        assert inst.server_host_name == ["stack_proxy"]

    def test_subscriptionid_property(self):
        """Test subscriptionid returns the subscription ID."""
        from cvpysdk.instances.virtualserver.azure_stack import AzureStackInstance

        inst = object.__new__(AzureStackInstance)
        inst._subscriptionid = "sub-12345"
        assert inst.subscriptionid == "sub-12345"

    def test_applicationid_property(self):
        """Test applicationid returns the application ID."""
        from cvpysdk.instances.virtualserver.azure_stack import AzureStackInstance

        inst = object.__new__(AzureStackInstance)
        inst._applicationid = "app-67890"
        assert inst.applicationid == "app-67890"

    def test_get_instance_properties_json_structure(self):
        """Test _get_instance_properties_json returns correct structure."""
        from cvpysdk.instances.virtualserver.azure_stack import AzureStackInstance

        inst = object.__new__(AzureStackInstance)
        inst._instance = {"clientName": "stack_client"}
        inst._instanceActivityControl = {"enableBackup": True}
        inst._virtualserverinstance = {
            "vsInstanceType": 403,
            "associatedClients": {"memberServers": []},
        }
        result = inst._get_instance_properties_json()
        assert result["instanceProperties"]["virtualServerInstance"]["vsInstanceType"] == 403
