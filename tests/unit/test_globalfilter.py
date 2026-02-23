"""Unit tests for cvpysdk.globalfilter module."""

from unittest.mock import patch

import pytest

from cvpysdk.exception import SDKException
from cvpysdk.globalfilter import GlobalFilter, GlobalFilters


@pytest.mark.unit
class TestGlobalFilters:
    """Tests for the GlobalFilters class."""

    def test_init(self, mock_commcell):
        gf = GlobalFilters(mock_commcell)
        assert gf._commcell_object is mock_commcell
        assert "WINDOWS" in gf._global_filter_dict
        assert "UNIX" in gf._global_filter_dict
        assert "NAS" in gf._global_filter_dict

    def test_repr(self, mock_commcell):
        gf = GlobalFilters(mock_commcell)
        assert "GlobalFilter" in repr(gf)
        assert "testcs" in repr(gf)

    def test_get_returns_global_filter_object(self, mock_commcell, mock_response):
        gf = GlobalFilters(mock_commcell)
        resp = mock_response(
            json_data={"globalFiltersInfo": {"windowsGlobalFilters": {"filters": []}}}
        )
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        with patch.object(GlobalFilter, "__init__", return_value=None):
            result = gf.get("WINDOWS")
            assert isinstance(result, GlobalFilter)

    def test_get_raises_on_non_string(self, mock_commcell):
        gf = GlobalFilters(mock_commcell)
        with pytest.raises(SDKException):
            gf.get(123)

    def test_get_raises_on_invalid_filter_name(self, mock_commcell):
        gf = GlobalFilters(mock_commcell)
        with pytest.raises(SDKException):
            gf.get("INVALID")


@pytest.mark.unit
class TestGlobalFilter:
    """Tests for the GlobalFilter entity class."""

    def _make_global_filter(self, mock_commcell, mock_response):
        resp = mock_response(
            json_data={
                "globalFiltersInfo": {
                    "windowsGlobalFilters": {
                        "filters": [
                            {"filter": "C:\\Temp"},
                            {"filter": "C:\\Windows\\Temp"},
                        ]
                    }
                }
            }
        )
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        return GlobalFilter(mock_commcell, "WINDOWS", "windowsGlobalFilters")

    def test_init(self, mock_commcell, mock_response):
        gf = self._make_global_filter(mock_commcell, mock_response)
        assert gf._filter_name == "WINDOWS"

    def test_repr(self, mock_commcell, mock_response):
        gf = self._make_global_filter(mock_commcell, mock_response)
        assert "WINDOWS" in repr(gf)

    def test_content(self, mock_commcell, mock_response):
        gf = self._make_global_filter(mock_commcell, mock_response)
        assert isinstance(gf.content, list)
