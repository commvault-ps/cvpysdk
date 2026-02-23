"""Unit tests for cvpysdk.internetoptions module."""

import pytest

from cvpysdk.exception import SDKException
from cvpysdk.internetoptions import InternetOptions


@pytest.mark.unit
class TestInternetOptions:
    """Tests for the InternetOptions class."""

    def _make_internet_options(self, mock_commcell, mock_response):
        resp = mock_response(
            json_data={
                "config": {
                    "internetGateway": {"clientName": "gateway1"},
                    "httpProxy": {"enabled": False},
                }
            }
        )
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        return InternetOptions(mock_commcell)

    def test_init_fetches_config(self, mock_commcell, mock_response):
        io = self._make_internet_options(mock_commcell, mock_response)
        assert io._config is not None

    def test_repr(self, mock_commcell, mock_response):
        io = self._make_internet_options(mock_commcell, mock_response)
        assert "InternetOption" in repr(io)

    def test_init_raises_on_empty_response(self, mock_commcell, mock_response):
        resp = mock_response(json_data={})
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        with pytest.raises(SDKException):
            InternetOptions(mock_commcell)

    def test_init_raises_on_api_failure(self, mock_commcell, mock_response):
        resp = mock_response(status_code=500, text="Server Error")
        mock_commcell._cvpysdk_object.make_request.return_value = (False, resp)
        with pytest.raises(SDKException):
            InternetOptions(mock_commcell)

    def test_refresh_re_fetches(self, mock_commcell, mock_response):
        io = self._make_internet_options(mock_commcell, mock_response)
        resp2 = mock_response(
            json_data={
                "config": {
                    "internetGateway": {"clientName": "gateway2"},
                    "httpProxy": {"enabled": True},
                }
            }
        )
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp2)
        io.refresh()
        assert io._config["httpProxy"]["enabled"] is True
