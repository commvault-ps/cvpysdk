"""Unit tests for cvpysdk/instances/bigdataapps/yugabyteinstance.py"""

from unittest.mock import MagicMock

import pytest

from cvpysdk.instances.bigdataappsinstance import BigDataAppsInstance


@pytest.mark.unit
class TestYugabyteInstance:
    """Tests for the YugabyteInstance class."""

    def test_inherits_bigdataapps_instance(self):
        """Test that YugabyteInstance is a subclass of BigDataAppsInstance."""
        from cvpysdk.instances.bigdataapps.yugabyteinstance import YugabyteInstance

        assert issubclass(YugabyteInstance, BigDataAppsInstance)

    def test_restore_raises_for_non_dict(self):
        """Test restore raises SDKException when options is not a dict."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.bigdataapps.yugabyteinstance import YugabyteInstance

        inst = object.__new__(YugabyteInstance)
        with pytest.raises(SDKException):
            inst.restore("not_a_dict")

    def test_restore_builds_distributed_json(self):
        """Test restore builds yugabyteDBRestoreOptions correctly."""
        from cvpysdk.instances.bigdataapps.yugabyteinstance import YugabyteInstance

        inst = object.__new__(YugabyteInstance)
        inst._commcell_object = MagicMock()

        mock_client = MagicMock()
        mock_client.client_id = "300"
        mock_client.client_name = "yb_node"
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
            "subclient_id": -1,
            "backupset_name": "bs1",
            "sql_fromtable": "t1",
            "cql_fromtable": "t2",
            "sql_totable": "t1_dest",
            "cql_totable": "t2_dest",
            "client_type": 19,
            "accessnodes": ["yb_node"],
            "kms_config": "kms1",
            "kmsconfigUUID": "uuid-1234",
        }

        result = inst.restore(restore_options)
        assert result == "job_obj"

        dist_opts = mock_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"][
            "distributedAppsRestoreOptions"
        ]
        assert dist_opts["distributedRestore"] is True
        assert dist_opts["yugabyteDBRestoreOptions"]["kmsConfigName"] == "kms1"
        assert len(dist_opts["noSQLGenericRestoreOptions"]["tableMap"]) == 2
