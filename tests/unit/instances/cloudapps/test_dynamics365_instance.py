"""Unit tests for cvpysdk/instances/cloudapps/dynamics365_instance.py"""

import pytest

from cvpysdk.instances.cainstance import CloudAppsInstance


@pytest.mark.unit
class TestMSDynamics365Instance:
    """Tests for the MSDynamics365Instance class."""

    def test_inherits_cloud_apps_instance(self):
        """Test that MSDynamics365Instance is a subclass of CloudAppsInstance."""
        from cvpysdk.instances.cloudapps.dynamics365_instance import MSDynamics365Instance

        assert issubclass(MSDynamics365Instance, CloudAppsInstance)

    def test_access_node_property(self):
        """Test access_node property returns the stored value."""
        from cvpysdk.instances.cloudapps.dynamics365_instance import MSDynamics365Instance

        inst = object.__new__(MSDynamics365Instance)
        inst._access_node = "test_access_node"
        assert inst.access_node == "test_access_node"

    def test_idx_app_type_property(self):
        """Test idx_app_type returns constant value."""
        from cvpysdk.instances.cloudapps.dynamics365_instance import MSDynamics365Instance

        inst = object.__new__(MSDynamics365Instance)
        assert inst.idx_app_type == 200127

    def test_get_instance_properties_json(self):
        """Test _get_instance_properties_json returns correct format."""
        from cvpysdk.instances.cloudapps.dynamics365_instance import MSDynamics365Instance

        inst = object.__new__(MSDynamics365Instance)
        inst._properties = {"key": "value"}
        result = inst._get_instance_properties_json()
        assert result == {"instanceProperties": {"key": "value"}}
