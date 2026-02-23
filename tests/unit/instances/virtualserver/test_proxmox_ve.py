"""Unit tests for cvpysdk/instances/virtualserver/proxmox_ve.py"""

import pytest

from cvpysdk.instances.vsinstance import VirtualServerInstance


@pytest.mark.unit
class TestProxmoxVEInstance:
    """Tests for the ProxmoxVEInstance class."""

    def test_inherits_virtual_server_instance(self):
        """Test that ProxmoxVEInstance is a subclass of VirtualServerInstance."""
        from cvpysdk.instances.virtualserver.proxmox_ve import ProxmoxVEInstance

        assert issubclass(ProxmoxVEInstance, VirtualServerInstance)

    def test_server_name_property(self):
        """Test server_name returns the server name list."""
        from cvpysdk.instances.virtualserver.proxmox_ve import ProxmoxVEInstance

        inst = object.__new__(ProxmoxVEInstance)
        inst._server_name = ["proxmox_client"]
        assert inst.server_name == ["proxmox_client"]

    def test_server_host_name_getter(self):
        """Test server_host_name getter returns the host name."""
        from cvpysdk.instances.virtualserver.proxmox_ve import ProxmoxVEInstance

        inst = object.__new__(ProxmoxVEInstance)
        inst._server_host_name = ["proxmox.example.com"]
        assert inst.server_host_name == ["proxmox.example.com"]

    def test_server_host_name_setter(self):
        """Test server_host_name setter updates the host name."""
        from cvpysdk.instances.virtualserver.proxmox_ve import ProxmoxVEInstance

        inst = object.__new__(ProxmoxVEInstance)
        inst._server_host_name = []
        inst.server_host_name = ["new_host.example.com"]
        assert inst._server_host_name == ["new_host.example.com"]

    def test_get_instance_properties_json_structure(self):
        """Test _get_instance_properties_json returns correct structure."""
        from cvpysdk.instances.virtualserver.proxmox_ve import ProxmoxVEInstance

        inst = object.__new__(ProxmoxVEInstance)
        inst._instance = {"clientName": "proxmox_client"}
        inst._instanceActivityControl = {"enableBackup": True}
        inst._virtualserverinstance = {
            "vsInstanceType": 23,
            "associatedClients": {"memberServers": []},
        }
        result = inst._get_instance_properties_json()
        assert result["instanceProperties"]["virtualServerInstance"]["vsInstanceType"] == 23
        assert "vmwareVendor" not in result["instanceProperties"]["virtualServerInstance"]
