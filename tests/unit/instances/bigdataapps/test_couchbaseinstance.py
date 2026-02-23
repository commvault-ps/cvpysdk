"""Unit tests for cvpysdk/instances/bigdataapps/couchbaseinstance.py"""

from unittest.mock import MagicMock

import pytest

from cvpysdk.instances.bigdataappsinstance import BigDataAppsInstance


@pytest.mark.unit
class TestCouchbaseInstance:
    """Tests for the CouchbaseInstance class."""

    def test_inherits_bigdataapps_instance(self):
        """Test that CouchbaseInstance is a subclass of BigDataAppsInstance."""
        from cvpysdk.instances.bigdataapps.couchbaseinstance import CouchbaseInstance

        assert issubclass(CouchbaseInstance, BigDataAppsInstance)

    def test_restore_raises_for_non_dict(self):
        """Test restore raises SDKException when options is not a dict."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.bigdataapps.couchbaseinstance import CouchbaseInstance

        inst = object.__new__(CouchbaseInstance)
        with pytest.raises(SDKException):
            inst.restore("not_a_dict")

    def test_restore_builds_distributed_json(self):
        """Test restore builds distributedAppsRestoreOptions correctly."""
        from cvpysdk.instances.bigdataapps.couchbaseinstance import CouchbaseInstance

        inst = object.__new__(CouchbaseInstance)
        inst._commcell_object = MagicMock()

        mock_client = MagicMock()
        mock_client.client_id = "100"
        mock_client.client_name = "node1"
        inst._commcell_object.clients.get.return_value = mock_client

        mock_json = {
            "taskInfo": {
                "associations": [{"subclientId": 0, "backupsetName": ""}],
                "subTasks": [{"options": {"restoreOptions": {}}}],
            }
        }
        inst._restore_json = MagicMock(return_value=mock_json)
        inst._process_restore_response = MagicMock(return_value="job_obj")

        restore_options = {
            "subclient_id": 5,
            "backupset_name": "bs1",
            "restore_items": ["bucket1"],
            "client_type": 17,
            "accessnodes": ["node1"],
        }

        result = inst.restore(restore_options)
        assert result == "job_obj"

        dist_opts = mock_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"][
            "distributedAppsRestoreOptions"
        ]
        assert dist_opts["distributedRestore"] is True
        assert dist_opts["isMultiNodeRestore"] is True
