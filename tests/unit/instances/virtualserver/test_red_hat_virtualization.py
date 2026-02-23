"""Unit tests for cvpysdk/instances/virtualserver/red_hat_virtualization.py"""

import pytest

from cvpysdk.instances.vsinstance import VirtualServerInstance


@pytest.mark.unit
class TestRhevInstance:
    """Tests for the RhevInstance class."""

    def test_inherits_virtual_server_instance(self):
        """Test that RhevInstance is a subclass of VirtualServerInstance."""
        from cvpysdk.instances.virtualserver.red_hat_virtualization import RhevInstance

        assert issubclass(RhevInstance, VirtualServerInstance)

    def test_server_name_property(self):
        """Test server_name returns the server name list."""
        from cvpysdk.instances.virtualserver.red_hat_virtualization import RhevInstance

        inst = object.__new__(RhevInstance)
        inst._server_name = ["rhev_pseudo"]
        assert inst.server_name == ["rhev_pseudo"]

    def test_server_host_name_property(self):
        """Test server_host_name returns the host name list."""
        from cvpysdk.instances.virtualserver.red_hat_virtualization import RhevInstance

        inst = object.__new__(RhevInstance)
        inst._server_host_name = ["rhev.example.com"]
        assert inst.server_host_name == ["rhev.example.com"]

    def test_get_instance_properties_json_structure(self):
        """Test _get_instance_properties_json returns correct structure."""
        from cvpysdk.instances.virtualserver.red_hat_virtualization import RhevInstance

        inst = object.__new__(RhevInstance)
        inst._instance = {"clientName": "rhev_client"}
        inst._instanceActivityControl = {"enableBackup": True}
        inst._virtualserverinstance = {
            "vsInstanceType": 501,
            "associatedClients": {"memberServers": []},
            "vmwareVendor": {},
        }
        result = inst._get_instance_properties_json()
        assert result["instanceProperties"]["virtualServerInstance"]["vsInstanceType"] == 501
