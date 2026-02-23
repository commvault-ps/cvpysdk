"""Unit tests for cvpysdk.datacube.handler module."""

from unittest.mock import MagicMock

import pytest

from cvpysdk.datacube.handler import Handler, Handlers
from cvpysdk.exception import SDKException


def _make_datasource_mock(mock_commcell):
    """Create a mock datasource object."""
    datasource = MagicMock()
    datasource._commcell_object = mock_commcell
    datasource.datasource_id = "42"
    datasource.datasource_name = "test_ds"
    return datasource


@pytest.mark.unit
class TestHandlers:
    """Tests for the Handlers collection class."""

    def _create_handlers(self, mock_commcell, mock_response, handler_data=None):
        """Create a Handlers object bypassing __init__."""
        datasource = _make_datasource_mock(mock_commcell)
        handlers = Handlers.__new__(Handlers)
        handlers._datasource_object = datasource
        handlers.commcell_obj = mock_commcell
        handlers._create_handler = mock_commcell._services["CREATE_HANDLER"]
        handlers._get_handler = mock_commcell._services["GET_HANDLERS"] % "42"
        if handler_data is None:
            handler_data = {
                "handler1": {"handlerName": "handler1", "handlerId": 1},
                "handler2": {"handlerName": "handler2", "handlerId": 2},
            }
        handlers._handlers = handler_data
        return handlers

    def test_repr(self, mock_commcell, mock_response):
        h = self._create_handlers(mock_commcell, mock_response)
        assert "test_ds" in repr(h)
        assert "Handlers" in repr(h)

    def test_str(self, mock_commcell, mock_response):
        h = self._create_handlers(mock_commcell, mock_response)
        output = str(h)
        assert "handler1" in output
        assert "handler2" in output

    def test_has_handler_true(self, mock_commcell, mock_response):
        h = self._create_handlers(mock_commcell, mock_response)
        assert h.has_handler("handler1") is True

    def test_has_handler_case_insensitive(self, mock_commcell, mock_response):
        h = self._create_handlers(mock_commcell, mock_response)
        assert h.has_handler("Handler1") is True

    def test_has_handler_false(self, mock_commcell, mock_response):
        h = self._create_handlers(mock_commcell, mock_response)
        assert h.has_handler("nonexistent") is False

    def test_has_handler_invalid_type(self, mock_commcell, mock_response):
        h = self._create_handlers(mock_commcell, mock_response)
        with pytest.raises(SDKException):
            h.has_handler(123)

    def test_get_properties(self, mock_commcell, mock_response):
        h = self._create_handlers(mock_commcell, mock_response)
        props = h.get_properties("handler1")
        assert props["handlerId"] == 1

    def test_get_existing_handler(self, mock_commcell, mock_response):
        h = self._create_handlers(mock_commcell, mock_response)
        result = h.get("handler1")
        assert isinstance(result, Handler)
        assert result.handler_id == 1

    def test_get_nonexistent_handler(self, mock_commcell, mock_response):
        h = self._create_handlers(mock_commcell, mock_response)
        with pytest.raises(SDKException):
            h.get("nonexistent")

    def test_get_invalid_type(self, mock_commcell, mock_response):
        h = self._create_handlers(mock_commcell, mock_response)
        with pytest.raises(SDKException):
            h.get(123)


@pytest.mark.unit
class TestHandler:
    """Tests for the Handler entity class."""

    def _create_handler(self, mock_commcell):
        """Create a Handler object with a known handler_id."""
        datasource = _make_datasource_mock(mock_commcell)
        handler = Handler(datasource, "handler1", handler_id=10)
        return handler

    def test_init_with_id(self, mock_commcell):
        handler = self._create_handler(mock_commcell)
        assert handler.handler_id == 10
        assert handler._handler_name == "handler1"

    def test_handler_id_property(self, mock_commcell):
        handler = self._create_handler(mock_commcell)
        assert handler.handler_id == 10

    def test_get_handler_data_invalid_filter(self, mock_commcell):
        handler = self._create_handler(mock_commcell)
        with pytest.raises(SDKException):
            handler.get_handler_data(handler_filter=123)

    def test_get_handler_data_success(self, mock_commcell, mock_response):
        handler = self._create_handler(mock_commcell)
        resp = mock_response(json_data={"response": {"docs": []}})
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        result = handler.get_handler_data()
        assert result == {"docs": []}

    def test_get_handler_data_api_failure(self, mock_commcell, mock_response):
        handler = self._create_handler(mock_commcell)
        resp = mock_response(status_code=500, text="error")
        mock_commcell._cvpysdk_object.make_request.return_value = (False, resp)
        with pytest.raises(SDKException):
            handler.get_handler_data()
