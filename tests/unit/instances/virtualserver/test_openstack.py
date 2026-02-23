"""Unit tests for cvpysdk/instances/virtualserver/openstack.py"""

import pytest

from cvpysdk.instances.vsinstance import VirtualServerInstance


@pytest.mark.unit
class TestOpenStackInstance:
    """Tests for the OpenStackInstance class."""

    def test_inherits_virtual_server_instance(self):
        """Test that OpenStackInstance is a subclass of VirtualServerInstance."""
        from cvpysdk.instances.virtualserver.openstack import OpenStackInstance

        assert issubclass(OpenStackInstance, VirtualServerInstance)

    def test_server_name_property(self):
        """Test server_name returns the server name list."""
        from cvpysdk.instances.virtualserver.openstack import OpenStackInstance

        inst = object.__new__(OpenStackInstance)
        inst._server_name = ["openstack_pseudo"]
        assert inst.server_name == ["openstack_pseudo"]

    def test_server_host_name_property(self):
        """Test server_host_name returns the host name list."""
        from cvpysdk.instances.virtualserver.openstack import OpenStackInstance

        inst = object.__new__(OpenStackInstance)
        inst._server_host_name = ["openstack.example.com"]
        assert inst.server_host_name == ["openstack.example.com"]

    def test_get_instance_properties_json_structure(self):
        """Test _get_instance_properties_json returns correct structure."""
        from cvpysdk.instances.virtualserver.openstack import OpenStackInstance

        inst = object.__new__(OpenStackInstance)
        inst._instance = {"clientName": "os_client"}
        inst._instanceActivityControl = {"enableBackup": True}
        inst._virtualserverinstance = {
            "vsInstanceType": 12,
            "associatedClients": {"memberServers": []},
            "vmwareVendor": {},
        }
        result = inst._get_instance_properties_json()
        assert result["instanceProperties"]["virtualServerInstance"]["vsInstanceType"] == 12
