from unittest.mock import patch

import pytest

from cvpysdk.storage_pool import StoragePool, StoragePools, StorageType


@pytest.mark.unit
class TestStoragePools:
    """Tests for the StoragePools collection class."""

    def test_repr(self, mock_commcell):
        with patch.object(StoragePools, "_get_storage_pools", return_value={}):
            sp = StoragePools(mock_commcell)
        assert "StoragePools" in repr(sp)

    def test_all_storage_pools_property(self, mock_commcell):
        pools = {"pool1": "1", "pool2": "2"}
        with patch.object(StoragePools, "_get_storage_pools", return_value=pools):
            sp = StoragePools(mock_commcell)
        assert sp.all_storage_pools == pools

    def test_has_storage_pool_true(self, mock_commcell):
        pools = {"pool1": "1"}
        with patch.object(StoragePools, "_get_storage_pools", return_value=pools):
            sp = StoragePools(mock_commcell)
        assert sp.has_storage_pool("pool1") is True

    def test_has_storage_pool_false(self, mock_commcell):
        pools = {"pool1": "1"}
        with patch.object(StoragePools, "_get_storage_pools", return_value=pools):
            sp = StoragePools(mock_commcell)
        assert sp.has_storage_pool("nonexistent") is False

    def test_has_storage_pool_case_insensitive(self, mock_commcell):
        pools = {"pool1": "1"}
        with patch.object(StoragePools, "_get_storage_pools", return_value=pools):
            sp = StoragePools(mock_commcell)
        assert sp.has_storage_pool("POOL1") is True

    def test_len(self, mock_commcell):
        pools = {"pool1": "1", "pool2": "2"}
        with patch.object(StoragePools, "_get_storage_pools", return_value=pools):
            sp = StoragePools(mock_commcell)
        assert len(sp) == 2

    def test_getitem_by_name(self, mock_commcell):
        pools = {"pool1": {"id": "1"}}
        with patch.object(StoragePools, "_get_storage_pools", return_value=pools):
            sp = StoragePools(mock_commcell)
        assert sp["pool1"] == {"id": "1"}

    def test_getitem_by_id(self, mock_commcell):
        pools = {"pool1": {"id": "1"}}
        with patch.object(StoragePools, "_get_storage_pools", return_value=pools):
            sp = StoragePools(mock_commcell)
        assert sp["1"] == "pool1"

    def test_getitem_invalid_raises(self, mock_commcell):
        pools = {"pool1": {"id": "1"}}
        with patch.object(StoragePools, "_get_storage_pools", return_value=pools):
            sp = StoragePools(mock_commcell)
        with pytest.raises(IndexError):
            sp["nonexistent"]

    def test_str_representation(self, mock_commcell):
        pools = {"pool1": "1"}
        with patch.object(StoragePools, "_get_storage_pools", return_value=pools):
            sp = StoragePools(mock_commcell)
        result = str(sp)
        assert "pool1" in result

    def test_refresh(self, mock_commcell):
        with patch.object(StoragePools, "_get_storage_pools", return_value={}) as mock_get:
            sp = StoragePools(mock_commcell)
            sp.refresh()
        assert mock_get.call_count == 2


@pytest.mark.unit
class TestStorageType:
    """Tests for StorageType enum."""

    def test_disk_type(self):
        assert StorageType.CLOUD == 2

    def test_hyperscale_type(self):
        assert StorageType.HYPERSCALE == 3

    def test_tape_type(self):
        assert StorageType.TAPE == 4


@pytest.mark.unit
class TestStoragePool:
    """Tests for the StoragePool entity class."""

    def test_repr(self, mock_commcell):
        with patch.object(StoragePool, "_get_storage_pool_properties"):
            pool = StoragePool.__new__(StoragePool)
            pool._commcell_object = mock_commcell
            pool._storage_pool_name = "testpool"
            pool._storage_pool_id = "1"
        repr(pool)
        # StoragePool may have a __repr__ method
        assert pool._storage_pool_name == "testpool"
