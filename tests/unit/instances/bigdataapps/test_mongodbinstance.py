"""Unit tests for cvpysdk/instances/bigdataapps/mongodbinstance.py"""

from unittest.mock import MagicMock

import pytest

from cvpysdk.instances.bigdataappsinstance import BigDataAppsInstance


@pytest.mark.unit
class TestMongoDBInstance:
    """Tests for the MongoDBInstance class."""

    def test_inherits_bigdataapps_instance(self):
        """Test that MongoDBInstance is a subclass of BigDataAppsInstance."""
        from cvpysdk.instances.bigdataapps.mongodbinstance import MongoDBInstance

        assert issubclass(MongoDBInstance, BigDataAppsInstance)

    def test_restore_raises_for_non_dict(self):
        """Test restore raises SDKException when options is not a dict."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.bigdataapps.mongodbinstance import MongoDBInstance

        inst = object.__new__(MongoDBInstance)
        with pytest.raises(SDKException):
            inst.restore("not_a_dict")

    def test_restore_collection_raises_for_non_dict(self):
        """Test restore_collection raises SDKException when options is not a dict."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.bigdataapps.mongodbinstance import MongoDBInstance

        inst = object.__new__(MongoDBInstance)
        with pytest.raises(SDKException):
            inst.restore_collection("not_a_dict")

    def test_restore_builds_distributed_json(self):
        """Test restore builds mongoDBRestoreOptions correctly."""
        from cvpysdk.instances.bigdataapps.mongodbinstance import MongoDBInstance

        inst = object.__new__(MongoDBInstance)
        inst._commcell_object = MagicMock()

        mock_client = MagicMock()
        mock_client.client_id = "200"
        mock_client.client_name = "mongo_node"
        inst._commcell_object.clients.get.return_value = mock_client

        mock_json = {
            "taskInfo": {
                "associations": [{"subclientId": 0, "backupsetName": "", "_type_": None}],
                "subTasks": [{"options": {"restoreOptions": {}}}],
            }
        }
        inst._restore_json = MagicMock(return_value=mock_json)
        inst._process_restore_response = MagicMock(return_value="job_obj")

        restore_options = {
            "subclient_id": -1,
            "backupset_name": "bs1",
            "_type_": 5,
            "source_shard_name": "rs0",
            "destination_shard_name": "rs0",
            "hostname": "mongo1.example.com",
            "clientName": "mongo_node",
            "desthostName": "mongo1.example.com",
            "destclientName": "mongo_node",
            "destPortNumber": 27017,
            "destDataDir": "/data/db",
            "bkpDataDir": "/backup",
            "backupPortNumber": 27017,
            "restoreDataDir": "/backup",
            "primaryPort": 27017,
        }

        result = inst.restore(restore_options)
        assert result == "job_obj"

    def test_restore_collection_builds_granular_json(self):
        """Test restore_collection builds granular recovery options."""
        from cvpysdk.instances.bigdataapps.mongodbinstance import MongoDBInstance

        inst = object.__new__(MongoDBInstance)
        inst._commcell_object = MagicMock()

        mock_client = MagicMock()
        mock_client.client_id = "200"
        mock_client.client_name = "mongo_node"
        inst._commcell_object.clients.get.return_value = mock_client

        mock_json = {
            "taskInfo": {
                "associations": [{"subclientId": 0, "backupsetName": "", "_type_": None}],
                "subTasks": [{"options": {"restoreOptions": {}}}],
            }
        }
        inst._restore_json = MagicMock(return_value=mock_json)
        inst._process_restore_response = MagicMock(return_value="job_obj")

        restore_options = {
            "subclient_id": 10,
            "backupset_name": "bs1",
            "_type_": 5,
            "source_db_name": "testdb",
            "restore_db_name": "testdb_restored",
            "clientName": "mongo_node",
            "destclientName": "mongo_node",
        }

        result = inst.restore_collection(restore_options)
        assert result == "job_obj"

        dist_opts = mock_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"][
            "distributedAppsRestoreOptions"
        ]
        assert dist_opts["mongoDBRestoreOptions"]["isGranularRecovery"] is True
