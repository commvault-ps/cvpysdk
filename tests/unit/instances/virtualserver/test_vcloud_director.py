"""Unit tests for cvpysdk/instances/virtualserver/vcloud_director.py"""

import pytest

from cvpysdk.instances.vsinstance import VirtualServerInstance


@pytest.mark.unit
class TestVcloudInstance:
    """Tests for the vcloudInstance class."""

    def test_inherits_virtual_server_instance(self):
        """Test that vcloudInstance is a subclass of VirtualServerInstance."""
        from cvpysdk.instances.virtualserver.vcloud_director import vcloudInstance

        assert issubclass(vcloudInstance, VirtualServerInstance)

    def test_server_name_property(self):
        """Test server_name returns the server name list."""
        from cvpysdk.instances.virtualserver.vcloud_director import vcloudInstance

        inst = object.__new__(vcloudInstance)
        inst._server_name = ["vcloud_pseudo"]
        assert inst.server_name == ["vcloud_pseudo"]

    def test_server_host_name_property(self):
        """Test server_host_name returns the host name list."""
        from cvpysdk.instances.virtualserver.vcloud_director import vcloudInstance

        inst = object.__new__(vcloudInstance)
        inst._server_host_name = ["vcd.example.com"]
        assert inst.server_host_name == ["vcd.example.com"]

    def test_user_name_property(self):
        """Test _user_name returns the username from vcloud vendor."""
        from cvpysdk.instances.virtualserver.vcloud_director import vcloudInstance

        inst = object.__new__(vcloudInstance)
        inst._vcloudvendor = {"userName": "vcd_admin@system"}
        assert inst._user_name == "vcd_admin@system"

    def test_get_instance_properties_json_structure(self):
        """Test _get_instance_properties_json returns correct structure."""
        from cvpysdk.instances.virtualserver.vcloud_director import vcloudInstance

        inst = object.__new__(vcloudInstance)
        inst._instance = {"clientName": "vcd_client"}
        inst._instanceActivityControl = {"enableBackup": True}
        inst._virtualserverinstance = {
            "vsInstanceType": 103,
            "associatedClients": {"memberServers": []},
            "vmwareVendor": {},
        }
        result = inst._get_instance_properties_json()
        assert result["instanceProperties"]["virtualServerInstance"]["vsInstanceType"] == 103
