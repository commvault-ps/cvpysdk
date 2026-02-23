"""Unit tests for cvpysdk/instances/virtualserver/fusioncompute.py"""

import pytest

from cvpysdk.instances.vsinstance import VirtualServerInstance


@pytest.mark.unit
class TestFusionComputeInstance:
    """Tests for the FusionComputeInstance class."""

    def test_inherits_virtual_server_instance(self):
        """Test that FusionComputeInstance is a subclass of VirtualServerInstance."""
        from cvpysdk.instances.virtualserver.fusioncompute import FusionComputeInstance

        assert issubclass(FusionComputeInstance, VirtualServerInstance)

    def test_server_name_property(self):
        """Test server_name returns the server name list."""
        from cvpysdk.instances.virtualserver.fusioncompute import FusionComputeInstance

        inst = object.__new__(FusionComputeInstance)
        inst._server_name = ["fc_client"]
        assert inst.server_name == ["fc_client"]

    def test_server_host_name_property(self):
        """Test server_host_name returns the VRM host list."""
        from cvpysdk.instances.virtualserver.fusioncompute import FusionComputeInstance

        inst = object.__new__(FusionComputeInstance)
        inst._server_host_name = ["vrm.example.com"]
        assert inst.server_host_name == ["vrm.example.com"]

    def test_user_name_property(self):
        """Test _user_name returns username from vmware vendor."""
        from cvpysdk.instances.virtualserver.fusioncompute import FusionComputeInstance

        inst = object.__new__(FusionComputeInstance)
        inst._vmwarvendor = {"userName": "fc_admin"}
        assert inst._user_name == "fc_admin"
