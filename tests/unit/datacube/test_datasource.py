"""Unit tests for cvpysdk.datacube.datasource module."""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.datacube.datasource import Datasource, Datasources
from cvpysdk.exception import SDKException


def _make_datacube_mock(mock_commcell):
    """Create a mock Datacube object with required attributes."""
    datacube = MagicMock()
    datacube._commcell_object = mock_commcell
    datacube.analytics_engines = [{"clientName": "engine1", "cloudID": 100}]
    datacube._response_not_success = MagicMock(side_effect=SDKException("Response", "101"))
    return datacube


@pytest.mark.unit
class TestDatasources:
    """Tests for the Datasources collection class."""

    def _create_datasources(self, mock_commcell, mock_response, collections=None):
        """Helper to create Datasources with mocked _get_all_datasources."""
        datacube = _make_datacube_mock(mock_commcell)
        if collections is None:
            collections = {
                "ds1": {
                    "data_source_id": 1,
                    "data_source_name": "ds1",
                    "data_source_type": "jdbc",
                }
            }
        resp = mock_response(json_data={"collections": []})
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        ds = Datasources.__new__(Datasources)
        ds._datacube_object = datacube
        ds.commcell_obj = mock_commcell
        ds._all_datasources = mock_commcell._services["GET_ALL_DATASOURCES"]
        ds._create_datasource = mock_commcell._services["CREATE_DATASOURCE"]
        ds._datasources = collections
        return ds

    def test_repr(self, mock_commcell, mock_response):
        ds = self._create_datasources(mock_commcell, mock_response)
        assert repr(ds) == "Datasources class instance for Commcell"

    def test_str_format(self, mock_commcell, mock_response):
        ds = self._create_datasources(mock_commcell, mock_response)
        output = str(ds)
        assert "ds1" in output

    def test_has_datasource_true(self, mock_commcell, mock_response):
        ds = self._create_datasources(mock_commcell, mock_response)
        assert ds.has_datasource("ds1") is True

    def test_has_datasource_false(self, mock_commcell, mock_response):
        ds = self._create_datasources(mock_commcell, mock_response)
        assert ds.has_datasource("nonexistent") is False

    def test_has_datasource_invalid_type(self, mock_commcell, mock_response):
        ds = self._create_datasources(mock_commcell, mock_response)
        with pytest.raises(SDKException):
            ds.has_datasource(123)

    def test_get_existing_datasource(self, mock_commcell, mock_response):
        ds = self._create_datasources(mock_commcell, mock_response)
        with patch(
            "cvpysdk.datacube.datasource.Datasource.__init__", return_value=None
        ) as mock_init:
            ds.get("ds1")
            mock_init.assert_called_once()

    def test_get_nonexistent_datasource(self, mock_commcell, mock_response):
        ds = self._create_datasources(mock_commcell, mock_response)
        with pytest.raises(SDKException):
            ds.get("nonexistent")

    def test_get_invalid_type(self, mock_commcell, mock_response):
        ds = self._create_datasources(mock_commcell, mock_response)
        with pytest.raises(SDKException):
            ds.get(123)

    def test_get_datasource_properties(self, mock_commcell, mock_response):
        ds = self._create_datasources(mock_commcell, mock_response)
        props = ds.get_datasource_properties("ds1")
        assert props["data_source_id"] == 1

    def test_get_datasources_from_collections_static(self):
        collections = [
            {
                "computedCoreName": "core1",
                "cloudId": 10,
                "datasources": [
                    {
                        "datasourceId": 1,
                        "datasourceName": "ds1",
                        "datasourceType": 1,
                        "description": "test",
                        "status": {"totalcount": 100, "state": 1},
                    }
                ],
            }
        ]
        result = Datasources._get_datasources_from_collections(collections)
        assert "ds1" in result
        assert result["ds1"]["data_source_id"] == 1
        assert result["ds1"]["data_source_type"] == "jdbc"
        assert result["ds1"]["computedCoreName"] == "core1"
        assert result["ds1"]["cloudId"] == 10
        assert result["ds1"]["total_count"] == 100

    def test_add_invalid_datasource_name(self, mock_commcell, mock_response):
        ds = self._create_datasources(mock_commcell, mock_response)
        with pytest.raises(SDKException):
            ds.add(123, "engine1", "1", None)

    def test_add_invalid_analytics_engine(self, mock_commcell, mock_response):
        ds = self._create_datasources(mock_commcell, mock_response)
        with pytest.raises(SDKException):
            ds.add("ds_new", 123, "1", None)

    def test_add_invalid_datasource_type(self, mock_commcell, mock_response):
        ds = self._create_datasources(mock_commcell, mock_response)
        with pytest.raises(SDKException):
            ds.add("ds_new", "engine1", 123, None)

    def test_delete_invalid_type(self, mock_commcell, mock_response):
        ds = self._create_datasources(mock_commcell, mock_response)
        with pytest.raises(SDKException):
            ds.delete(123)

    def test_delete_nonexistent(self, mock_commcell, mock_response):
        ds = self._create_datasources(mock_commcell, mock_response)
        with pytest.raises(SDKException):
            ds.delete("nonexistent")

    def test_refresh(self, mock_commcell, mock_response):
        ds = self._create_datasources(mock_commcell, mock_response)
        resp = mock_response(json_data={})
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        ds.refresh()
        assert ds._datasources == {}


@pytest.mark.unit
class TestDatasource:
    """Tests for the Datasource entity class."""

    def _create_datasource(self, mock_commcell):
        """Create a Datasource object bypassing __init__."""
        datasource = Datasource.__new__(Datasource)
        datasource._datacube_object = MagicMock()
        datasource._datacube_object._commcell_object = mock_commcell
        datasource._commcell_object = mock_commcell
        datasource._datasource_name = "test_ds"
        datasource._datasource_id = "42"
        datasource._computed_core_name = "core_test"
        datasource._cloud_id = 10
        datasource._data_source_type = "jdbc"
        datasource._properties = {"data_source_type": "jdbc"}
        datasource._handlers_obj = None
        datasource.handlers = MagicMock()
        return datasource

    def test_repr(self, mock_commcell):
        ds = self._create_datasource(mock_commcell)
        assert repr(ds) == "Datasource class instance for Commcell"

    def test_datasource_id_property(self, mock_commcell):
        ds = self._create_datasource(mock_commcell)
        assert ds.datasource_id == "42"

    def test_datasource_name_property(self, mock_commcell):
        ds = self._create_datasource(mock_commcell)
        assert ds.datasource_name == "test_ds"

    def test_computed_core_name_property(self, mock_commcell):
        ds = self._create_datasource(mock_commcell)
        assert ds.computed_core_name == "core_test"

    def test_index_server_cloud_id_property(self, mock_commcell):
        ds = self._create_datasource(mock_commcell)
        assert ds.index_server_cloud_id == 10

    def test_data_source_type_property(self, mock_commcell):
        ds = self._create_datasource(mock_commcell)
        assert ds.data_source_type == "jdbc"

    def test_properties_property(self, mock_commcell):
        ds = self._create_datasource(mock_commcell)
        assert ds.properties == {"data_source_type": "jdbc"}

    def test_update_datasource_schema_invalid_type(self, mock_commcell):
        ds = self._create_datasource(mock_commcell)
        with pytest.raises(SDKException):
            ds.update_datasource_schema("not_a_list")

    def test_update_datasource_schema_invalid_element(self, mock_commcell):
        ds = self._create_datasource(mock_commcell)
        with pytest.raises(SDKException):
            ds.update_datasource_schema(["not_a_dict"])
