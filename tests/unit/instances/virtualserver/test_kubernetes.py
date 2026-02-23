"""Unit tests for cvpysdk/instances/virtualserver/kubernetes.py"""

import pytest

from cvpysdk.instances.vsinstance import VirtualServerInstance


@pytest.mark.unit
class TestKubernetesInstance:
    """Tests for the KubernetesInstance class."""

    def test_inherits_virtual_server_instance(self):
        """Test that KubernetesInstance is a subclass of VirtualServerInstance."""
        from cvpysdk.instances.virtualserver.kubernetes import KubernetesInstance

        assert issubclass(KubernetesInstance, VirtualServerInstance)

    def test_server_name_property(self):
        """Test server_name returns the server name list."""
        from cvpysdk.instances.virtualserver.kubernetes import KubernetesInstance

        inst = object.__new__(KubernetesInstance)
        inst._server_name = ["k8s_pseudo"]
        assert inst.server_name == ["k8s_pseudo"]

    def test_server_host_name_property(self):
        """Test server_host_name returns the host name list."""
        from cvpysdk.instances.virtualserver.kubernetes import KubernetesInstance

        inst = object.__new__(KubernetesInstance)
        inst._server_host_name = ["k8s-api.example.com"]
        assert inst.server_host_name == ["k8s-api.example.com"]

    def test_get_instance_properties_json_structure(self):
        """Test _get_instance_properties_json returns correct structure."""
        from cvpysdk.instances.virtualserver.kubernetes import KubernetesInstance

        inst = object.__new__(KubernetesInstance)
        inst._instance = {"clientName": "k8s_client"}
        inst._instanceActivityControl = {"enableBackup": True}
        inst._virtualserverinstance = {
            "vsInstanceType": 20,
            "associatedClients": {"memberServers": []},
            "vmwareVendor": {},
        }
        result = inst._get_instance_properties_json()
        assert "instanceProperties" in result
