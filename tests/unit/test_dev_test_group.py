"""Unit tests for cvpysdk.dev_test_group module."""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.dev_test_group import Dev_Test_Group
from cvpysdk.exception import SDKException


@pytest.mark.unit
class TestDevTestGroup:
    """Tests for the Dev_Test_Group class."""

    def test_init(self, mock_commcell):
        """Test constructor stores commcell references."""
        dtg = Dev_Test_Group(mock_commcell)
        assert dtg._commcell_object is mock_commcell
        assert dtg._cvpysdk_object is mock_commcell._cvpysdk_object
        assert dtg._services is mock_commcell._services
        assert dtg._update_response_ is mock_commcell._update_response_

    def test_json_task_property(self, mock_commcell):
        """Test _json_task returns correct structure."""
        dtg = Dev_Test_Group(mock_commcell)
        task = dtg._json_task
        assert task["initiatedFrom"] == 1
        assert task["taskType"] == 1
        assert task["policyType"] == 0
        assert task["taskFlags"]["disabled"] is False

    def test_json_virtual_subtasks_property(self, mock_commcell):
        """Test _json_virtual_subtasks returns correct structure."""
        dtg = Dev_Test_Group(mock_commcell)
        subtask = dtg._json_virtual_subtasks
        assert subtask["subTaskType"] == 1
        assert subtask["operationType"] == 4038

    def test_json_provision_option_property(self, mock_commcell):
        """Test _json_provision_Option returns correct structure."""
        dtg = Dev_Test_Group(mock_commcell)
        option = dtg._json_provision_Option
        assert option["powerOnVM"] is True
        assert option["useLinkedClone"] is False
        assert option["restoreAsManagedVM"] is False
        assert option["doLinkedCloneFromLocalTemplateCopy"] is False

    def test_process_restore_response_success(self, mock_commcell, mock_response):
        """Test _process_restore_response returns Job on success."""
        dtg = Dev_Test_Group(mock_commcell)
        resp = mock_response(json_data={"jobIds": ["12345"]})
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)

        with patch("cvpysdk.dev_test_group.Job") as mock_job_cls:
            mock_job_cls.return_value = MagicMock()
            dtg._process_restore_response({"fake": "json"})
            mock_job_cls.assert_called_once_with(mock_commcell, "12345")

    def test_process_restore_response_error_code(self, mock_commcell, mock_response):
        """Test _process_restore_response raises on errorCode."""
        dtg = Dev_Test_Group(mock_commcell)
        resp = mock_response(json_data={"errorCode": 1, "errorMessage": "VM error"})
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)

        with pytest.raises(SDKException):
            dtg._process_restore_response({"fake": "json"})

    def test_process_restore_response_empty(self, mock_commcell, mock_response):
        """Test _process_restore_response raises on empty response body."""
        dtg = Dev_Test_Group(mock_commcell)
        resp = mock_response(json_data={})
        resp.json.return_value = {}
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)

        with pytest.raises(SDKException):
            dtg._process_restore_response({"fake": "json"})
