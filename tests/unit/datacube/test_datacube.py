"""Unit tests for cvpysdk.datacube.datacube module."""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.datacube.datacube import Datacube
from cvpysdk.exception import SDKException


@pytest.mark.unit
class TestDatacube:
    """Tests for the Datacube class."""

    def _create_datacube(self, mock_commcell, mock_response, engines=None):
        """Helper to create a Datacube with mocked API responses."""
        if engines is None:
            engines = [{"clientName": "idx_server1", "cloudID": 1}]
        resp = mock_response(json_data={"listOfCIServer": engines})
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        return Datacube(mock_commcell)

    def test_init_sets_attributes(self, mock_commcell, mock_response):
        dc = self._create_datacube(mock_commcell, mock_response)
        assert dc._commcell_object is mock_commcell
        assert dc._datasources is None

    def test_repr(self, mock_commcell, mock_response):
        dc = self._create_datacube(mock_commcell, mock_response)
        assert "testcs" in repr(dc)
        assert "Datacube" in repr(dc)

    def test_analytics_engines_property(self, mock_commcell, mock_response):
        engines = [{"clientName": "engine1", "cloudID": 10}]
        dc = self._create_datacube(mock_commcell, mock_response, engines=engines)
        assert dc.analytics_engines == engines

    def test_get_analytics_engines_empty(self, mock_commcell, mock_response):
        resp = mock_response(json_data={})
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        dc = Datacube(mock_commcell)
        assert dc.analytics_engines == []

    @patch("cvpysdk.datacube.datacube.Datasources")
    def test_datasources_property_creates_instance(
        self, mock_ds_cls, mock_commcell, mock_response
    ):
        dc = self._create_datacube(mock_commcell, mock_response)
        mock_ds_cls.return_value = MagicMock()
        result = dc.datasources
        assert result is not None
        mock_ds_cls.assert_called_once_with(dc)

    @patch("cvpysdk.datacube.datacube.Datasources")
    def test_datasources_property_cached(self, mock_ds_cls, mock_commcell, mock_response):
        dc = self._create_datacube(mock_commcell, mock_response)
        mock_ds_cls.return_value = MagicMock()
        first = dc.datasources
        second = dc.datasources
        assert first is second
        assert mock_ds_cls.call_count == 1

    def test_get_jdbc_drivers_invalid_type(self, mock_commcell, mock_response):
        dc = self._create_datacube(mock_commcell, mock_response)
        with pytest.raises(SDKException):
            dc.get_jdbc_drivers(123)

    def test_refresh_resets_datasources(self, mock_commcell, mock_response):
        dc = self._create_datacube(mock_commcell, mock_response)
        dc._datasources = MagicMock()
        dc.refresh()
        assert dc._datasources is None

    def test_refresh_engine_re_fetches(self, mock_commcell, mock_response):
        dc = self._create_datacube(mock_commcell, mock_response)
        new_engines = [{"clientName": "engine2", "cloudID": 2}]
        resp2 = mock_response(json_data={"listOfCIServer": new_engines})
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp2)
        dc.refresh_engine()
        assert dc.analytics_engines == new_engines
