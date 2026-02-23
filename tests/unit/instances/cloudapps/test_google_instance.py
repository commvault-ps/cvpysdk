"""Unit tests for cvpysdk/instances/cloudapps/google_instance.py"""

import pytest

from cvpysdk.instances.cainstance import CloudAppsInstance


@pytest.mark.unit
class TestGoogleInstance:
    """Tests for the GoogleInstance class."""

    def test_inherits_cloud_apps_instance(self):
        """Test that GoogleInstance is a subclass of CloudAppsInstance."""
        from cvpysdk.instances.cloudapps.google_instance import GoogleInstance

        assert issubclass(GoogleInstance, CloudAppsInstance)

    def test_ca_instance_type_gmail(self):
        """Test ca_instance_type returns GMAIL for type 1."""
        from cvpysdk.instances.cloudapps.google_instance import GoogleInstance

        inst = object.__new__(GoogleInstance)
        inst._ca_instance_type = 1
        assert inst.ca_instance_type == "GMAIL"

    def test_ca_instance_type_gdrive(self):
        """Test ca_instance_type returns GDRIVE for type 2."""
        from cvpysdk.instances.cloudapps.google_instance import GoogleInstance

        inst = object.__new__(GoogleInstance)
        inst._ca_instance_type = 2
        assert inst.ca_instance_type == "GDRIVE"

    def test_ca_instance_type_onedrive(self):
        """Test ca_instance_type returns ONEDRIVE for type 7."""
        from cvpysdk.instances.cloudapps.google_instance import GoogleInstance

        inst = object.__new__(GoogleInstance)
        inst._ca_instance_type = 7
        assert inst.ca_instance_type == "ONEDRIVE"

    def test_properties_return_correct_values(self):
        """Test various property accessors."""
        from cvpysdk.instances.cloudapps.google_instance import GoogleInstance

        inst = object.__new__(GoogleInstance)
        inst._manage_content_automatically = True
        inst._auto_discovery_enabled = True
        inst._auto_discovery_mode = 0
        inst._app_email_id = "app@example.com"
        inst._google_admin_id = "admin@example.com"
        inst._service_account_key_file = "/path/to/key.json"
        inst._app_client_id = "client-id-123"
        inst._client_id = "od-client-id"
        inst._tenant = "tenant-id"
        inst._proxy_client = "proxy_client"

        assert inst.manage_content_automatically is True
        assert inst.auto_discovery_status is True
        assert inst.auto_discovery_mode == 0
        assert inst.app_email_id == "app@example.com"
        assert inst.google_admin_id == "admin@example.com"
        assert inst.key_file_path == "/path/to/key.json"
        assert inst.google_client_id == "client-id-123"
        assert inst.onedrive_client_id == "od-client-id"
        assert inst.onedrive_tenant == "tenant-id"
        assert inst.proxy_client == "proxy_client"

    def test_get_instance_properties_json(self):
        """Test _get_instance_properties_json returns correct format."""
        from cvpysdk.instances.cloudapps.google_instance import GoogleInstance

        inst = object.__new__(GoogleInstance)
        inst._properties = {"key": "value"}
        result = inst._get_instance_properties_json()
        assert result == {"instanceProperties": {"key": "value"}}
