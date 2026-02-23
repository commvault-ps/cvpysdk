"""Unit tests for cvpysdk.drorchestration.drorchestrationoperations module."""

import pytest

from cvpysdk.drorchestration.drorchestrationoperations import DROrchestrationOperations


@pytest.mark.unit
class TestDROrchestrationOperations:
    """Tests for the DROrchestrationOperations class."""

    def _create_ops(self, mock_commcell):
        mock_commcell.commserv_version = 31
        ops = DROrchestrationOperations(mock_commcell)
        return ops

    def test_init(self, mock_commcell):
        ops = self._create_ops(mock_commcell)
        assert ops._commcell_object is mock_commcell
        assert ops._dr_orchestration_option is None

    def test_repr(self, mock_commcell):
        ops = self._create_ops(mock_commcell)
        assert repr(ops) == "DROrchestrationOperations instance for Commcell"

    def test_dr_orchestration_options_getter_setter(self, mock_commcell):
        ops = self._create_ops(mock_commcell)
        assert ops.dr_orchestration_options is None
        opts = {"failoverGroupId": 10, "failoverGroupName": "fg1"}
        ops.dr_orchestration_options = opts
        assert ops.dr_orchestration_options is opts

    def test_dr_group_id(self, mock_commcell):
        ops = self._create_ops(mock_commcell)
        ops.dr_orchestration_options = {"failoverGroupId": 42}
        assert ops.dr_group_id == 42

    def test_dr_group_id_default(self, mock_commcell):
        ops = self._create_ops(mock_commcell)
        ops.dr_orchestration_options = {}
        assert ops.dr_group_id == 0

    def test_json_task(self, mock_commcell):
        ops = self._create_ops(mock_commcell)
        task = ops._json_task
        assert task["taskType"] == 1
        assert task["ownerId"] == 1
        assert task["initiatedFrom"] == 2

    def test_json_dr_orchestration_subtasks(self, mock_commcell):
        ops = self._create_ops(mock_commcell)
        subtask = ops._json_dr_orchestration_subtasks
        assert subtask["subTaskType"] == 1
        assert subtask["operationType"] == 4046

    def test_json_dr_orchestration_from_monitor(self, mock_commcell):
        ops = self._create_ops(mock_commcell)
        ops.dr_orchestration_options = {
            "DROrchestrationType": "7",
            "initiatedfromMonitor": True,
            "replicationIds": [1, 2],
        }
        result = ops._json_dr_orchestration
        assert result["operationType"] == 7
        assert result["initiatedfromMonitor"] is True
        assert "replicationInfo" in result

    def test_json_dr_orchestration_from_failover_group(self, mock_commcell):
        ops = self._create_ops(mock_commcell)
        ops.dr_orchestration_options = {
            "DROrchestrationType": "1",
            "initiatedfromMonitor": False,
            "failoverGroupId": 10,
            "failoverGroupName": "fg1",
        }
        result = ops._json_dr_orchestration
        assert result["operationType"] == 1
        assert "vApp" in result
        assert result["vApp"]["vAppId"] == 10

    def test_call_dr_orchestration_task_success(self, mock_commcell, mock_response):
        ops = self._create_ops(mock_commcell)
        ops.dr_orchestration_options = {
            "DROrchestrationType": "7",
            "failoverGroupId": 10,
        }
        resp = mock_response(json_data={"taskId": 50, "jobIds": [100]})
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        result = ops._call_dr_orchestration_task({"taskInfo": {}})
        assert result == (100, 50)

    def test_call_reverse_replication_task_success(self, mock_commcell, mock_response):
        ops = self._create_ops(mock_commcell)
        ops.dr_orchestration_options = {
            "DROrchestrationType": "9",
            "failoverGroupId": 10,
        }
        resp = mock_response(json_data={"taskId": 60})
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        result = ops._call_reverse_replication_task({"drOrchestrationOption": {}})
        assert result == 60

    def test_get_operation_string(self, mock_commcell):
        ops = self._create_ops(mock_commcell)
        assert ops._get_dr_orchestration_operation_string(1) == "Planned Failover"
        assert ops._get_dr_orchestration_operation_string(2) == "Failback"
        assert ops._get_dr_orchestration_operation_string(3) == "UnPlanned Failover"
        assert ops._get_dr_orchestration_operation_string(4) == "Revert Failover"
        assert ops._get_dr_orchestration_operation_string(6) == "Undo Failover"
        assert ops._get_dr_orchestration_operation_string(7) == "TestBoot"
        assert ops._get_dr_orchestration_operation_string(8) == "Point in Time Failover"
        assert ops._get_dr_orchestration_operation_string(9) == "Reverse Replication"
        assert ops._get_dr_orchestration_operation_string(99) == ""

    def test_dr_orchestration_job_phase(self, mock_commcell):
        ops = self._create_ops(mock_commcell)
        from cvpysdk.drorchestration.dr_orchestration_job_phase import DRJobPhases

        assert ops.dr_orchestration_job_phase is DRJobPhases
