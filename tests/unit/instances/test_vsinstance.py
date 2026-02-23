"""Unit tests for cvpysdk/instances/vsinstance.py"""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.instance import Instance


@pytest.mark.unit
class TestVirtualServerInstance:
    """Tests for the VirtualServerInstance class."""

    def test_inherits_instance(self):
        """Test that VirtualServerInstance is a subclass of Instance."""
        from cvpysdk.instances.vsinstance import VirtualServerInstance

        assert issubclass(VirtualServerInstance, Instance)

    def test_get_instance_properties_sets_vs_attrs(self):
        """Test _get_instance_properties sets virtual server attributes."""
        from cvpysdk.instances.vsinstance import VirtualServerInstance

        inst = object.__new__(VirtualServerInstance)
        inst._properties = {
            "virtualServerInstance": {
                "vsInstanceType": 1,
                "associatedClients": {"memberServers": []},
            }
        }
        with patch.object(Instance, "_get_instance_properties"):
            inst._get_instance_properties()
        assert inst._vsinstancetype == 1
        assert inst._asscociatedclients == {"memberServers": []}

    def test_get_instance_properties_no_vs_data(self):
        """Test _get_instance_properties when no virtualServerInstance key."""
        from cvpysdk.instances.vsinstance import VirtualServerInstance

        inst = object.__new__(VirtualServerInstance)
        inst._properties = {}
        with patch.object(Instance, "_get_instance_properties"):
            inst._get_instance_properties()
        assert inst._vsinstancetype is None
        assert inst._asscociatedclients is None

    def test_associated_clients_property(self):
        """Test associated_clients returns list of client names."""
        from cvpysdk.instances.vsinstance import VirtualServerInstance

        inst = object.__new__(VirtualServerInstance)
        inst._asscociatedclients = {
            "memberServers": [
                {"client": {"clientName": "proxy1"}},
                {"client": {"clientName": "proxy2"}},
            ]
        }
        result = inst.associated_clients
        assert result == ["proxy1", "proxy2"]

    def test_associated_clients_with_client_groups(self):
        """Test associated_clients returns client group names."""
        from cvpysdk.instances.vsinstance import VirtualServerInstance

        inst = object.__new__(VirtualServerInstance)
        inst._asscociatedclients = {
            "memberServers": [
                {"client": {"clientGroupName": "group1"}},
            ]
        }
        result = inst.associated_clients
        assert result == ["group1"]

    def test_server_name_property(self):
        """Test server_name returns the pseudoclient name."""
        from cvpysdk.instances.vsinstance import VirtualServerInstance

        inst = object.__new__(VirtualServerInstance)
        mock_client = MagicMock()
        mock_client.client_name = "vs_pseudo_client"
        inst._agent_object = MagicMock()
        inst._agent_object._client_object = mock_client
        assert inst.server_name == "vs_pseudo_client"
