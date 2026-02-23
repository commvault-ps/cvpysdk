"""Unit tests for cvpysdk/instances/cainstance.py"""

from unittest.mock import MagicMock

import pytest

from cvpysdk.instance import Instance


@pytest.mark.unit
class TestCloudAppsInstance:
    """Tests for the CloudAppsInstance class."""

    def test_inherits_instance(self):
        """Test that CloudAppsInstance is a subclass of Instance."""
        from cvpysdk.instances.cainstance import CloudAppsInstance

        assert issubclass(CloudAppsInstance, Instance)

    def test_new_returns_google_for_type_1(self):
        """Test __new__ returns GoogleInstance for instance type 1."""
        from cvpysdk.instances.cainstance import CloudAppsInstance
        from cvpysdk.instances.cloudapps.google_instance import GoogleInstance

        agent_object = MagicMock()
        response = MagicMock()
        response.json.return_value = {
            "instanceProperties": [{"cloudAppsInstance": {"instanceType": 1}}]
        }
        agent_object._commcell_object.request.return_value = response

        obj = CloudAppsInstance.__new__(CloudAppsInstance, agent_object, "test", 10)
        assert isinstance(obj, GoogleInstance)

    def test_new_returns_salesforce_for_type_3(self):
        """Test __new__ returns SalesforceInstance for instance type 3."""
        from cvpysdk.instances.cainstance import CloudAppsInstance
        from cvpysdk.instances.cloudapps.salesforce_instance import SalesforceInstance

        agent_object = MagicMock()
        response = MagicMock()
        response.json.return_value = {
            "instanceProperties": [{"cloudAppsInstance": {"instanceType": 3}}]
        }
        agent_object._commcell_object.request.return_value = response

        obj = CloudAppsInstance.__new__(CloudAppsInstance, agent_object, "test", 11)
        assert isinstance(obj, SalesforceInstance)

    def test_new_returns_cloud_storage_for_type_5(self):
        """Test __new__ returns CloudStorageInstance for instance type 5 (S3)."""
        from cvpysdk.instances.cainstance import CloudAppsInstance
        from cvpysdk.instances.cloudapps.cloud_storage_instance import CloudStorageInstance

        agent_object = MagicMock()
        response = MagicMock()
        response.json.return_value = {
            "instanceProperties": [{"cloudAppsInstance": {"instanceType": 5}}]
        }
        agent_object._commcell_object.request.return_value = response

        obj = CloudAppsInstance.__new__(CloudAppsInstance, agent_object, "test", 12)
        assert isinstance(obj, CloudStorageInstance)

    def test_new_returns_onedrive_for_type_7(self):
        """Test __new__ returns OneDriveInstance for instance type 7."""
        from cvpysdk.instances.cainstance import CloudAppsInstance
        from cvpysdk.instances.cloudapps.onedrive_instance import OneDriveInstance

        agent_object = MagicMock()
        response = MagicMock()
        response.json.return_value = {
            "instanceProperties": [{"cloudAppsInstance": {"instanceType": 7}}]
        }
        agent_object._commcell_object.request.return_value = response

        obj = CloudAppsInstance.__new__(CloudAppsInstance, agent_object, "test", 13)
        assert isinstance(obj, OneDriveInstance)

    def test_new_returns_teams_for_type_36(self):
        """Test __new__ returns TeamsInstance for instance type 36."""
        from cvpysdk.instances.cainstance import CloudAppsInstance
        from cvpysdk.instances.cloudapps.teams_instance import TeamsInstance

        agent_object = MagicMock()
        response = MagicMock()
        response.json.return_value = {
            "instanceProperties": [{"cloudAppsInstance": {"instanceType": 36}}]
        }
        agent_object._commcell_object.request.return_value = response

        obj = CloudAppsInstance.__new__(CloudAppsInstance, agent_object, "test", 14)
        assert isinstance(obj, TeamsInstance)

    def test_new_raises_on_bad_response(self):
        """Test __new__ raises SDKException on empty response."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.cainstance import CloudAppsInstance

        agent_object = MagicMock()
        response = MagicMock()
        response.json.return_value = {}
        agent_object._commcell_object.request.return_value = response

        with pytest.raises(SDKException):
            CloudAppsInstance.__new__(CloudAppsInstance, agent_object, "test", 15)
