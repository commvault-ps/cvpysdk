"""Unit tests for cvpysdk/instances/cloudapps/onedrive_instance.py"""

import pytest

from cvpysdk.instances.cainstance import CloudAppsInstance


@pytest.mark.unit
class TestOneDriveInstance:
    """Tests for the OneDriveInstance class."""

    def test_inherits_cloud_apps_instance(self):
        """Test that OneDriveInstance is a subclass of CloudAppsInstance."""
        from cvpysdk.instances.cloudapps.onedrive_instance import OneDriveInstance

        assert issubclass(OneDriveInstance, CloudAppsInstance)

    def test_ca_instance_type_onedrive(self):
        """Test ca_instance_type returns ONEDRIVE for type 7."""
        from cvpysdk.instances.cloudapps.onedrive_instance import OneDriveInstance

        inst = object.__new__(OneDriveInstance)
        inst._ca_instance_type = 7
        assert inst.ca_instance_type == "ONEDRIVE"

    def test_ca_instance_type_other(self):
        """Test ca_instance_type returns raw type for non-7 type."""
        from cvpysdk.instances.cloudapps.onedrive_instance import OneDriveInstance

        inst = object.__new__(OneDriveInstance)
        inst._ca_instance_type = 99
        assert inst.ca_instance_type == 99

    def test_properties_return_correct_values(self):
        """Test various property accessors."""
        from cvpysdk.instances.cloudapps.onedrive_instance import OneDriveInstance

        inst = object.__new__(OneDriveInstance)
        inst._manage_content_automatically = True
        inst._auto_discovery_enabled = False
        inst._auto_discovery_mode = 1
        inst._client_id = "client-123"
        inst._tenant = "tenant-456"
        inst._proxy_client = "proxy1"

        assert inst.manage_content_automatically is True
        assert inst.auto_discovery_status is False
        assert inst.auto_discovery_mode == 1
        assert inst.onedrive_client_id == "client-123"
        assert inst.onedrive_tenant == "tenant-456"
        assert inst.proxy_client == "proxy1"

    def test_modify_connection_settings_raises_for_empty_app_id(self):
        """Test modify_connection_settings raises SDKException for empty app_id."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.cloudapps.onedrive_instance import OneDriveInstance

        inst = object.__new__(OneDriveInstance)
        with pytest.raises(SDKException):
            inst.modify_connection_settings("", "dir_id", "secret")

    def test_modify_connection_settings_raises_for_empty_dir_id(self):
        """Test modify_connection_settings raises SDKException for empty dir_id."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.cloudapps.onedrive_instance import OneDriveInstance

        inst = object.__new__(OneDriveInstance)
        with pytest.raises(SDKException):
            inst.modify_connection_settings("app_id", "", "secret")

    def test_delete_data_from_browse_raises_for_invalid_guid(self):
        """Test delete_data_from_browse raises SDKException for invalid item_guid."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.cloudapps.onedrive_instance import OneDriveInstance

        inst = object.__new__(OneDriveInstance)
        with pytest.raises(SDKException):
            inst.delete_data_from_browse(123)

    def test_get_instance_properties_json(self):
        """Test _get_instance_properties_json returns correct format."""
        from cvpysdk.instances.cloudapps.onedrive_instance import OneDriveInstance

        inst = object.__new__(OneDriveInstance)
        inst._properties = {"key": "value"}
        result = inst._get_instance_properties_json()
        assert result == {"instanceProperties": {"key": "value"}}
