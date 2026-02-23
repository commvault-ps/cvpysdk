from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.exception import SDKException
from cvpysdk.index_pools import IndexPool, IndexPools


@pytest.mark.unit
class TestIndexPools:
    """Tests for the IndexPools collection class."""

    def test_repr(self, mock_commcell):
        with patch.object(IndexPools, "_get_all_index_pools"):
            mock_commcell.clients = MagicMock()
            idx = IndexPools(mock_commcell)
        assert "IndexPools" in repr(idx)

    def test_all_index_pools_property(self, mock_commcell):
        with patch.object(IndexPools, "_get_all_index_pools"):
            mock_commcell.clients = MagicMock()
            idx = IndexPools(mock_commcell)
            idx._all_index_pools = {"pool1": 1}
        assert idx.all_index_pools == {"pool1": 1}

    def test_has_pool_true(self, mock_commcell):
        with patch.object(IndexPools, "_get_all_index_pools"):
            mock_commcell.clients = MagicMock()
            idx = IndexPools(mock_commcell)
            idx._all_index_pools = {"pool1": 1}
        assert idx.has_pool("pool1") is True

    def test_has_pool_false(self, mock_commcell):
        with patch.object(IndexPools, "_get_all_index_pools"):
            mock_commcell.clients = MagicMock()
            idx = IndexPools(mock_commcell)
            idx._all_index_pools = {"pool1": 1}
        assert idx.has_pool("nonexistent") is False

    def test_getitem_found(self, mock_commcell):
        with patch.object(IndexPools, "_get_all_index_pools"):
            mock_commcell.clients = MagicMock()
            idx = IndexPools(mock_commcell)
            idx._all_index_pools = {"pool1": 1}
        result = idx["pool1"]
        assert result == {"pool_name": "pool1", "pool_id": 1}

    def test_getitem_not_found_raises(self, mock_commcell):
        with patch.object(IndexPools, "_get_all_index_pools"):
            mock_commcell.clients = MagicMock()
            idx = IndexPools(mock_commcell)
            idx._all_index_pools = {}
        with pytest.raises(SDKException):
            idx["nonexistent"]

    def test_get_bad_type_raises(self, mock_commcell):
        with patch.object(IndexPools, "_get_all_index_pools"):
            mock_commcell.clients = MagicMock()
            idx = IndexPools(mock_commcell)
            idx._all_index_pools = {}
        with pytest.raises(SDKException):
            idx.get(3.14)

    def test_get_not_found_raises(self, mock_commcell):
        with patch.object(IndexPools, "_get_all_index_pools"):
            mock_commcell.clients = MagicMock()
            idx = IndexPools(mock_commcell)
            idx._all_index_pools = {}
        with pytest.raises(SDKException):
            idx.get("nonexistent")

    def test_delete_bad_type_raises(self, mock_commcell):
        with patch.object(IndexPools, "_get_all_index_pools"):
            mock_commcell.clients = MagicMock()
            idx = IndexPools(mock_commcell)
            idx._all_index_pools = {}
        with pytest.raises(SDKException):
            idx.delete(123)

    def test_str_representation(self, mock_commcell):
        with patch.object(IndexPools, "_get_all_index_pools"):
            mock_commcell.clients = MagicMock()
            idx = IndexPools(mock_commcell)
            idx._all_index_pools = {"pool1": 1}
        result = str(idx)
        assert "pool1" in result


@pytest.mark.unit
class TestIndexPool:
    """Tests for the IndexPool entity class."""

    def test_repr(self, mock_commcell):
        with patch.object(IndexPool, "refresh"):
            pool = IndexPool(mock_commcell, "testpool", pool_id=1)
        assert "IndexPool" in repr(pool)
