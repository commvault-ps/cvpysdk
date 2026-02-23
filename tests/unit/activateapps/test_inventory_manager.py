from unittest.mock import patch

import pytest

from cvpysdk.activateapps.inventory_manager import Inventories
from cvpysdk.exception import SDKException


@pytest.mark.unit
class TestInventories:
    """Tests for the Inventories collection class."""

    def _make_inventories(self, mock_commcell, inventories=None):
        with patch.object(Inventories, "_get_inventories", return_value=inventories or {}):
            return Inventories(mock_commcell)

    def test_has_inventory_true(self, mock_commcell):
        inv = {"testinv": {"inventory_id": 1}}
        i = self._make_inventories(mock_commcell, inventories=inv)
        assert i.has_inventory("testinv") is True

    def test_has_inventory_non_string_raises(self, mock_commcell):
        i = self._make_inventories(mock_commcell)
        with pytest.raises(SDKException):
            i.has_inventory(123)

    def test_get_nonexistent_raises(self, mock_commcell):
        i = self._make_inventories(mock_commcell)
        with pytest.raises(SDKException):
            i.get("nonexistent")

    def test_refresh_calls_get(self, mock_commcell):
        with patch.object(Inventories, "_get_inventories", return_value={}) as mock_get:
            i = Inventories(mock_commcell)
            i.refresh()
        assert mock_get.call_count == 2

    def test_delete_nonexistent_raises(self, mock_commcell):
        i = self._make_inventories(mock_commcell)
        with pytest.raises(SDKException):
            i.delete("nonexistent")

    def test_delete_non_string_raises(self, mock_commcell):
        i = self._make_inventories(mock_commcell)
        with pytest.raises(SDKException):
            i.delete(123)
