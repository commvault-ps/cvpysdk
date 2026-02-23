"""Unit tests for cvpysdk/instances/virtualserver/hyperv.py"""

import pytest

from cvpysdk.instances.vsinstance import VirtualServerInstance


@pytest.mark.unit
class TestHyperVInstance:
    """Tests for the HyperVInstance class."""

    def test_inherits_virtual_server_instance(self):
        """Test that HyperVInstance is a subclass of VirtualServerInstance."""
        from cvpysdk.instances.virtualserver.hyperv import HyperVInstance

        assert issubclass(HyperVInstance, VirtualServerInstance)

    def test_server_name_property(self):
        """Test server_name returns the server name list."""
        from cvpysdk.instances.virtualserver.hyperv import HyperVInstance

        inst = object.__new__(HyperVInstance)
        inst._server_name = ["hyperv_host1"]
        assert inst.server_name == ["hyperv_host1"]

    def test_server_host_name_property(self):
        """Test server_host_name returns same as server_name."""
        from cvpysdk.instances.virtualserver.hyperv import HyperVInstance

        inst = object.__new__(HyperVInstance)
        inst._server_name = ["hyperv_host1"]
        assert inst.server_host_name == ["hyperv_host1"]

    def test_get_instance_properties_json_structure(self):
        """Test _get_instance_properties_json returns correct structure."""
        from cvpysdk.instances.virtualserver.hyperv import HyperVInstance

        inst = object.__new__(HyperVInstance)
        inst._instance = {"clientName": "hyperv_client"}
        inst._instanceActivityControl = {"enableBackup": True}
        inst._virtualserverinstance = {
            "vsInstanceType": 2,
            "associatedClients": {"memberServers": []},
        }
        result = inst._get_instance_properties_json()
        assert "instanceProperties" in result
        props = result["instanceProperties"]
        assert props["isDeleted"] is False
        assert props["virtualServerInstance"]["vsInstanceType"] == 2
