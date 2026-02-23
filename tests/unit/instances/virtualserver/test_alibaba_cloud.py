"""Unit tests for cvpysdk/instances/virtualserver/alibaba_cloud.py"""

import pytest

from cvpysdk.instances.vsinstance import VirtualServerInstance


@pytest.mark.unit
class TestAlibabaCloudInstance:
    """Tests for the AlibabaCloudInstance class."""

    def test_inherits_virtual_server_instance(self):
        """Test that AlibabaCloudInstance is a subclass of VirtualServerInstance."""
        from cvpysdk.instances.virtualserver.alibaba_cloud import AlibabaCloudInstance

        assert issubclass(AlibabaCloudInstance, VirtualServerInstance)

    def test_server_name_property(self):
        """Test server_name returns the server name list."""
        from cvpysdk.instances.virtualserver.alibaba_cloud import AlibabaCloudInstance

        inst = object.__new__(AlibabaCloudInstance)
        inst._server_name = ["alibaba_proxy"]
        assert inst.server_name == ["alibaba_proxy"]

    def test_server_host_name_property(self):
        """Test server_host_name returns the host name."""
        from cvpysdk.instances.virtualserver.alibaba_cloud import AlibabaCloudInstance

        inst = object.__new__(AlibabaCloudInstance)
        inst._server_host_name = ["ecs.aliyuncs.com"]
        assert inst.server_host_name == ["ecs.aliyuncs.com"]

    def test_instance_username_property(self):
        """Test instance_username returns the username."""
        from cvpysdk.instances.virtualserver.alibaba_cloud import AlibabaCloudInstance

        inst = object.__new__(AlibabaCloudInstance)
        inst._username = "alibaba_user"
        assert inst.instance_username == "alibaba_user"

    def test_get_instance_properties_json_has_xen_server(self):
        """Test _get_instance_properties_json includes xenServer key."""
        from cvpysdk.instances.virtualserver.alibaba_cloud import AlibabaCloudInstance

        inst = object.__new__(AlibabaCloudInstance)
        inst._instance = {"clientName": "alibaba_client"}
        inst._instanceActivityControl = {"enableBackup": True}
        inst._virtualserverinstance = {
            "vsInstanceType": 18,
            "associatedClients": {"memberServers": []},
            "vmwareVendor": {},
        }
        result = inst._get_instance_properties_json()
        vs = result["instanceProperties"]["virtualServerInstance"]
        assert "xenServer" in vs
