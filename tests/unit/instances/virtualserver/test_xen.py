"""Unit tests for cvpysdk/instances/virtualserver/xen.py"""

import pytest

from cvpysdk.instances.vsinstance import VirtualServerInstance


@pytest.mark.unit
class TestXen:
    """Tests for the Xen class."""

    def test_inherits_virtual_server_instance(self):
        """Test that Xen is a subclass of VirtualServerInstance."""
        from cvpysdk.instances.virtualserver.xen import Xen

        assert issubclass(Xen, VirtualServerInstance)

    def test_server_name_property(self):
        """Test server_name returns the server name."""
        from cvpysdk.instances.virtualserver.xen import Xen

        inst = object.__new__(Xen)
        inst._server_name = "xen_client"
        assert inst.server_name == "xen_client"

    def test_server_host_name_getter(self):
        """Test server_host_name getter returns the host name."""
        from cvpysdk.instances.virtualserver.xen import Xen

        inst = object.__new__(Xen)
        inst._server_host_name = "xen.example.com"
        assert inst.server_host_name == "xen.example.com"

    def test_server_host_name_setter(self):
        """Test server_host_name setter updates the host name."""
        from cvpysdk.instances.virtualserver.xen import Xen

        inst = object.__new__(Xen)
        inst._server_host_name = None
        inst.server_host_name = "new_xen.example.com"
        assert inst._server_host_name == "new_xen.example.com"

    def test_get_instance_properties_json_structure(self):
        """Test _get_instance_properties_json returns correct structure."""
        from cvpysdk.instances.virtualserver.xen import Xen

        inst = object.__new__(Xen)
        inst._instance = {"clientName": "xen_client"}
        inst._instanceActivityControl = {"enableBackup": True}
        inst._virtualserverinstance = {
            "vsInstanceType": 3,
            "associatedClients": {"memberServers": []},
        }
        result = inst._get_instance_properties_json()
        assert result["instanceProperties"]["virtualServerInstance"]["vsInstanceType"] == 3
