"""Unit tests for cvpysdk/instances/virtualserver/amazon_web_services.py"""

import pytest

from cvpysdk.instances.vsinstance import VirtualServerInstance


@pytest.mark.unit
class TestAmazonInstance:
    """Tests for the AmazonInstance class."""

    def test_inherits_virtual_server_instance(self):
        """Test that AmazonInstance is a subclass of VirtualServerInstance."""
        from cvpysdk.instances.virtualserver.amazon_web_services import AmazonInstance

        assert issubclass(AmazonInstance, VirtualServerInstance)

    def test_server_name_property(self):
        """Test server_name returns the server name list."""
        from cvpysdk.instances.virtualserver.amazon_web_services import AmazonInstance

        inst = object.__new__(AmazonInstance)
        inst._server_name = ["aws_proxy"]
        assert inst.server_name == ["aws_proxy"]

    def test_server_host_name_property(self):
        """Test server_host_name returns same as server_name."""
        from cvpysdk.instances.virtualserver.amazon_web_services import AmazonInstance

        inst = object.__new__(AmazonInstance)
        inst._server_name = ["aws_proxy"]
        assert inst.server_host_name == ["aws_proxy"]

    def test_get_instance_properties_json_structure(self):
        """Test _get_instance_properties_json returns correct structure."""
        from cvpysdk.instances.virtualserver.amazon_web_services import AmazonInstance

        inst = object.__new__(AmazonInstance)
        inst._instance = {"clientName": "aws_client"}
        inst._instanceActivityControl = {"enableBackup": True}
        inst._virtualserverinstance = {
            "vsInstanceType": 4,
            "associatedClients": {"memberServers": []},
            "vmwareVendor": {"virtualCenter": {}},
        }
        result = inst._get_instance_properties_json()
        assert result["instanceProperties"]["virtualServerInstance"]["vsInstanceType"] == 4
