"""Unit tests for cvpysdk/instances/virtualserver/google_cloud_platform.py"""

import pytest

from cvpysdk.instances.vsinstance import VirtualServerInstance


@pytest.mark.unit
class TestGoogleCloudInstance:
    """Tests for the GoogleCloudInstance class."""

    def test_inherits_virtual_server_instance(self):
        """Test that GoogleCloudInstance is a subclass of VirtualServerInstance."""
        from cvpysdk.instances.virtualserver.google_cloud_platform import GoogleCloudInstance

        assert issubclass(GoogleCloudInstance, VirtualServerInstance)

    def test_server_name_property(self):
        """Test server_name returns the server name list."""
        from cvpysdk.instances.virtualserver.google_cloud_platform import GoogleCloudInstance

        inst = object.__new__(GoogleCloudInstance)
        inst._server_name = ["gcp_proxy"]
        assert inst.server_name == ["gcp_proxy"]

    def test_server_host_name_property(self):
        """Test server_host_name returns same as server_name."""
        from cvpysdk.instances.virtualserver.google_cloud_platform import GoogleCloudInstance

        inst = object.__new__(GoogleCloudInstance)
        inst._server_name = ["gcp_proxy"]
        assert inst.server_host_name == ["gcp_proxy"]

    def test_get_instance_properties_json_structure(self):
        """Test _get_instance_properties_json returns correct structure."""
        from cvpysdk.instances.virtualserver.google_cloud_platform import GoogleCloudInstance

        inst = object.__new__(GoogleCloudInstance)
        inst._instance = {"clientName": "gcp_client"}
        inst._instanceActivityControl = {"enableBackup": True}
        inst._virtualserverinstance = {
            "vsInstanceType": 16,
            "associatedClients": {"memberServers": []},
            "vmwareVendor": {},
        }
        result = inst._get_instance_properties_json()
        assert result["instanceProperties"]["virtualServerInstance"]["vsInstanceType"] == 16
