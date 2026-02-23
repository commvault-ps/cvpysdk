"""Unit tests for cvpysdk/instances/cloudapps/cloud_database_instance.py"""

from unittest.mock import MagicMock

import pytest

from cvpysdk.instances.cainstance import CloudAppsInstance


@pytest.mark.unit
class TestCloudDatabaseInstance:
    """Tests for the CloudDatabaseInstance class."""

    def test_inherits_cloud_apps_instance(self):
        """Test that CloudDatabaseInstance is a subclass of CloudAppsInstance."""
        from cvpysdk.instances.cloudapps.cloud_database_instance import CloudDatabaseInstance

        assert issubclass(CloudDatabaseInstance, CloudAppsInstance)

    def test_ca_instance_type_property(self):
        """Test ca_instance_type returns the stored value."""
        from cvpysdk.instances.cloudapps.cloud_database_instance import CloudDatabaseInstance

        inst = object.__new__(CloudDatabaseInstance)
        inst._ca_instance_type = 4
        assert inst.ca_instance_type == 4

    def test_process_browse_response_success(self):
        """Test _process_browse_response returns JSON on success."""
        from cvpysdk.instances.cloudapps.cloud_database_instance import CloudDatabaseInstance

        inst = object.__new__(CloudDatabaseInstance)
        response = MagicMock()
        response.json.return_value = {"snapList": ["snap1"]}

        result = inst._process_browse_response(True, response)
        assert result == {"snapList": ["snap1"]}

    def test_process_browse_response_raises_on_failure(self):
        """Test _process_browse_response raises SDKException on failure."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.cloudapps.cloud_database_instance import CloudDatabaseInstance

        inst = object.__new__(CloudDatabaseInstance)
        with pytest.raises(SDKException):
            inst._process_browse_response(False, "error")
