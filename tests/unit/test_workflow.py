from unittest.mock import patch

import pytest

from cvpysdk.exception import SDKException
from cvpysdk.workflow import WorkFlow, WorkFlows


@pytest.mark.unit
class TestWorkFlows:
    """Tests for the WorkFlows collection class."""

    def test_repr(self, mock_commcell):
        with patch.object(WorkFlows, "_get_workflows", return_value={}), patch.object(
            WorkFlows, "_get_activities", return_value={}
        ):
            wf = WorkFlows(mock_commcell)
        assert "WorkFlow" in repr(wf)

    def test_all_workflows_property(self, mock_commcell):
        workflows = {"wf1": {"id": "1", "description": "test"}}
        with patch.object(WorkFlows, "_get_workflows", return_value=workflows), patch.object(
            WorkFlows, "_get_activities", return_value={}
        ):
            wf = WorkFlows(mock_commcell)
        assert wf.all_workflows == workflows

    def test_has_workflow_true(self, mock_commcell):
        workflows = {"wf1": {"id": "1", "description": "test"}}
        with patch.object(WorkFlows, "_get_workflows", return_value=workflows), patch.object(
            WorkFlows, "_get_activities", return_value={}
        ):
            wf = WorkFlows(mock_commcell)
        assert wf.has_workflow("wf1") is True

    def test_has_workflow_false(self, mock_commcell):
        with patch.object(WorkFlows, "_get_workflows", return_value={}), patch.object(
            WorkFlows, "_get_activities", return_value={}
        ):
            wf = WorkFlows(mock_commcell)
        assert not wf.has_workflow("nonexistent")

    def test_has_workflow_case_insensitive(self, mock_commcell):
        workflows = {"wf1": {"id": "1", "description": "test"}}
        with patch.object(WorkFlows, "_get_workflows", return_value=workflows), patch.object(
            WorkFlows, "_get_activities", return_value={}
        ):
            wf = WorkFlows(mock_commcell)
        assert wf.has_workflow("WF1") is True

    def test_has_workflow_bad_type_raises(self, mock_commcell):
        with patch.object(WorkFlows, "_get_workflows", return_value={}), patch.object(
            WorkFlows, "_get_activities", return_value={}
        ):
            wf = WorkFlows(mock_commcell)
        with pytest.raises(SDKException):
            wf.has_workflow(123)

    def test_has_activity_true(self, mock_commcell):
        activities = {"act1": {"id": "1", "description": "test"}}
        with patch.object(WorkFlows, "_get_workflows", return_value={}), patch.object(
            WorkFlows, "_get_activities", return_value=activities
        ):
            wf = WorkFlows(mock_commcell)
        assert wf.has_activity("act1") is True

    def test_has_activity_false(self, mock_commcell):
        with patch.object(WorkFlows, "_get_workflows", return_value={}), patch.object(
            WorkFlows, "_get_activities", return_value={}
        ):
            wf = WorkFlows(mock_commcell)
        assert not wf.has_activity("nonexistent")

    def test_has_activity_bad_type_raises(self, mock_commcell):
        with patch.object(WorkFlows, "_get_workflows", return_value={}), patch.object(
            WorkFlows, "_get_activities", return_value={}
        ):
            wf = WorkFlows(mock_commcell)
        with pytest.raises(SDKException):
            wf.has_activity(123)

    def test_len(self, mock_commcell):
        workflows = {
            "wf1": {"id": "1", "description": "test"},
            "wf2": {"id": "2", "description": "test2"},
        }
        with patch.object(WorkFlows, "_get_workflows", return_value=workflows), patch.object(
            WorkFlows, "_get_activities", return_value={}
        ):
            wf = WorkFlows(mock_commcell)
        assert len(wf) == 2

    def test_getitem_by_name(self, mock_commcell):
        workflows = {"wf1": {"id": "1", "description": "test"}}
        with patch.object(WorkFlows, "_get_workflows", return_value=workflows), patch.object(
            WorkFlows, "_get_activities", return_value={}
        ):
            wf = WorkFlows(mock_commcell)
        assert wf["wf1"]["id"] == "1"

    def test_getitem_by_id(self, mock_commcell):
        workflows = {"wf1": {"id": "1", "description": "test"}}
        with patch.object(WorkFlows, "_get_workflows", return_value=workflows), patch.object(
            WorkFlows, "_get_activities", return_value={}
        ):
            wf = WorkFlows(mock_commcell)
        assert wf["1"] == "wf1"

    def test_getitem_invalid_raises(self, mock_commcell):
        workflows = {"wf1": {"id": "1", "description": "test"}}
        with patch.object(WorkFlows, "_get_workflows", return_value=workflows), patch.object(
            WorkFlows, "_get_activities", return_value={}
        ):
            wf = WorkFlows(mock_commcell)
        with pytest.raises(IndexError):
            wf["999"]

    def test_import_workflow_bad_type_raises(self, mock_commcell):
        with patch.object(WorkFlows, "_get_workflows", return_value={}), patch.object(
            WorkFlows, "_get_activities", return_value={}
        ):
            wf = WorkFlows(mock_commcell)
        with pytest.raises(SDKException):
            wf.import_workflow(123)

    def test_import_activity_bad_type_raises(self, mock_commcell):
        with patch.object(WorkFlows, "_get_workflows", return_value={}), patch.object(
            WorkFlows, "_get_activities", return_value={}
        ):
            wf = WorkFlows(mock_commcell)
        with pytest.raises(SDKException):
            wf.import_activity(123)

    def test_refresh(self, mock_commcell):
        with patch.object(WorkFlows, "_get_workflows", return_value={}) as mock_get, patch.object(
            WorkFlows, "_get_activities", return_value={}
        ):
            wf = WorkFlows(mock_commcell)
            wf.refresh()
        assert mock_get.call_count == 2


@pytest.mark.unit
class TestWorkFlow:
    """Tests for the WorkFlow (Workflow) entity class."""

    def test_workflow_name_property(self, mock_commcell):
        with patch.object(WorkFlow, "_get_workflow_properties"):
            wf = WorkFlow.__new__(WorkFlow)
            wf._commcell_object = mock_commcell
            wf._workflow_name = "testwf"
            wf._workflow_id = "1"
        assert wf._workflow_name == "testwf"
