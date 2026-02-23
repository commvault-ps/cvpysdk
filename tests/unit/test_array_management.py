"""Unit tests for cvpysdk.array_management module."""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.array_management import ArrayManagement
from cvpysdk.exception import SDKException


@pytest.mark.unit
class TestArrayManagement:
    """Tests for the ArrayManagement class."""

    def test_init(self, mock_commcell):
        am = ArrayManagement(mock_commcell)
        assert am._commcell_object is mock_commcell
        assert am._SNAP_OPS is not None
        assert am.storage_arrays is not None

    def test_mount_calls_snap_operation(self, mock_commcell, mock_response):
        am = ArrayManagement(mock_commcell)
        resp = mock_response(json_data={"jobId": 42})
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        with patch("cvpysdk.array_management.Job") as MockJob:
            MockJob.return_value = MagicMock()
            result = am.mount(
                volume_id=[[100]],
                client_name=None,
                mountpath="/mnt/snap",
            )
            assert result is not None

    def test_unmount_calls_snap_operation(self, mock_commcell, mock_response):
        am = ArrayManagement(mock_commcell)
        resp = mock_response(json_data={"jobId": 43})
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        with patch("cvpysdk.array_management.Job") as MockJob:
            MockJob.return_value = MagicMock()
            result = am.unmount(volume_id=[[100]])
            assert result is not None

    def test_delete_calls_snap_operation(self, mock_commcell, mock_response):
        am = ArrayManagement(mock_commcell)
        resp = mock_response(json_data={"jobId": 44})
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        with patch("cvpysdk.array_management.Job") as MockJob:
            MockJob.return_value = MagicMock()
            result = am.delete(volume_id=[[100]])
            assert result is not None

    def test_revert_calls_snap_operation(self, mock_commcell, mock_response):
        am = ArrayManagement(mock_commcell)
        resp = mock_response(json_data={"jobId": 45})
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        with patch("cvpysdk.array_management.Job") as MockJob:
            MockJob.return_value = MagicMock()
            result = am.revert(volume_id=[[100]])
            assert result is not None

    def test_snap_operation_error_response(self, mock_commcell, mock_response):
        am = ArrayManagement(mock_commcell)
        resp = mock_response(json_data={"errorCode": 1, "errorMessage": "Snap failed"})
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        with pytest.raises(SDKException):
            am.mount(volume_id=[[100]], client_name=None, mountpath="/mnt/snap")

    def test_delete_array(self, mock_commcell, mock_response):
        am = ArrayManagement(mock_commcell)
        resp = mock_response(json_data={"errorCode": 0, "errorMessage": "success"})
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        result = am.delete_array("123")
        assert result == "success"
