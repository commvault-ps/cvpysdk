"""Unit tests for cvpysdk/instances/cloudapps/azure_cosmosdb_instance.py"""

from unittest.mock import MagicMock

import pytest

from cvpysdk.instances.cainstance import CloudAppsInstance


@pytest.mark.unit
class TestAzureCosmosDBInstance:
    """Tests for the AzureCosmosDBInstance class."""

    def test_inherits_cloud_apps_instance(self):
        """Test that AzureCosmosDBInstance is a subclass of CloudAppsInstance."""
        from cvpysdk.instances.cloudapps.azure_cosmosdb_instance import AzureCosmosDBInstance

        assert issubclass(AzureCosmosDBInstance, CloudAppsInstance)

    def test_restore_raises_for_non_dict(self):
        """Test restore raises SDKException when options is not a dict."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.cloudapps.azure_cosmosdb_instance import AzureCosmosDBInstance

        inst = object.__new__(AzureCosmosDBInstance)
        with pytest.raises(SDKException):
            inst.restore("not_a_dict")

    def test_restore_builds_cloud_app_json(self):
        """Test restore builds cloudAppsRestoreOptions correctly."""
        from cvpysdk.instances.cloudapps.azure_cosmosdb_instance import AzureCosmosDBInstance

        inst = object.__new__(AzureCosmosDBInstance)

        mock_json = {
            "taskInfo": {
                "associations": [{"_type_": None, "cloudInstanceType": None, "backupsetName": ""}],
                "subTasks": [{"options": {"restoreOptions": {}}}],
            }
        }
        inst._restore_json = MagicMock(return_value=mock_json)
        inst._process_restore_response = MagicMock(return_value="job_obj")

        restore_options = {
            "cloudinstancetype": "AZURE_COSMOSDB_CASSANDRA",
            "backupsetname": "default",
            "unconditional_overwrite": True,
            "in_place": True,
            "sourcedatabase": "ks1",
            "destinatinodatabase": "ks1",
            "srcstorageaccount": "acct1",
            "deststorageaccount": "acct1",
        }

        result = inst.restore(restore_options)
        assert result == "job_obj"
