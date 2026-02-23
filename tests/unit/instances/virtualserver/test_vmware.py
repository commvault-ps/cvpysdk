"""Unit tests for cvpysdk/instances/virtualserver/vmware.py"""

import pytest

from cvpysdk.instances.vsinstance import VirtualServerInstance


@pytest.mark.unit
class TestVMwareInstance:
    """Tests for the VMwareInstance class."""

    def test_inherits_virtual_server_instance(self):
        """Test that VMwareInstance is a subclass of VirtualServerInstance."""
        from cvpysdk.instances.virtualserver.vmware import VMwareInstance

        assert issubclass(VMwareInstance, VirtualServerInstance)

    def test_vendor_id(self):
        """Test that VMwareInstance sets vendor_id to 1."""
        from cvpysdk.instances.virtualserver.vmware import VMwareInstance

        inst = object.__new__(VMwareInstance)
        inst._vendor_id = None
        inst._vmwarvendor = None
        inst._server_name = []
        inst._server_host_name = []
        assert inst._server_name == []

    def test_server_host_name_property(self):
        """Test server_host_name returns the host name list."""
        from cvpysdk.instances.virtualserver.vmware import VMwareInstance

        inst = object.__new__(VMwareInstance)
        inst._server_host_name = ["vcenter.example.com"]
        assert inst.server_host_name == ["vcenter.example.com"]

    def test_server_name_property(self):
        """Test server_name returns the server name list."""
        from cvpysdk.instances.virtualserver.vmware import VMwareInstance

        inst = object.__new__(VMwareInstance)
        inst._server_name = ["vmware_pseudo"]
        assert inst.server_name == ["vmware_pseudo"]

    def test_user_name_property(self):
        """Test _user_name returns username from vmware vendor."""
        from cvpysdk.instances.virtualserver.vmware import VMwareInstance

        inst = object.__new__(VMwareInstance)
        inst._vmwarvendor = {"userName": "admin@vsphere.local"}
        assert inst._user_name == "admin@vsphere.local"
