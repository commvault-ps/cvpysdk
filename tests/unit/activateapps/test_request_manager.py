from unittest.mock import patch

import pytest

from cvpysdk.activateapps.request_manager import Requests
from cvpysdk.exception import SDKException


@pytest.mark.unit
class TestRequests:
    """Tests for the Requests collection class."""

    def _make_requests(self, mock_commcell, requests_data=None):
        with patch.object(Requests, "_get_all_requests", return_value=requests_data or {}):
            return Requests(mock_commcell)

    def test_has_request_true(self, mock_commcell):
        reqs = {"testreq": {"request_id": 1}}
        r = self._make_requests(mock_commcell, requests_data=reqs)
        assert r.has_request("testreq") is True

    def test_has_request_non_string_raises(self, mock_commcell):
        r = self._make_requests(mock_commcell)
        with pytest.raises(SDKException):
            r.has_request(123)

    def test_get_nonexistent_raises(self, mock_commcell):
        r = self._make_requests(mock_commcell)
        with pytest.raises(SDKException):
            r.get("nonexistent")

    def test_refresh_calls_get(self, mock_commcell):
        with patch.object(Requests, "_get_all_requests", return_value={}) as mock_get:
            r = Requests(mock_commcell)
            r.refresh()
        assert mock_get.call_count == 2

    def test_delete_nonexistent_raises(self, mock_commcell):
        r = self._make_requests(mock_commcell)
        with pytest.raises(SDKException):
            r.delete("nonexistent")
