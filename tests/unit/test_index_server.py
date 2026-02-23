from unittest.mock import patch

import pytest

from cvpysdk.exception import SDKException
from cvpysdk.index_server import IndexServers


@pytest.mark.unit
class TestIndexServers:
    """Tests for the IndexServers collection class."""

    def test_repr(self, mock_commcell):
        with patch.object(IndexServers, "_get_index_servers"), patch.object(
            IndexServers, "_get_all_roles"
        ):
            idx = IndexServers(mock_commcell)
        assert "IndexServers" in repr(idx)

    def test_all_index_servers_property(self, mock_commcell):
        with patch.object(IndexServers, "_get_index_servers"), patch.object(
            IndexServers, "_get_all_roles"
        ):
            idx = IndexServers(mock_commcell)
            idx._all_index_servers = {1: {"engineName": "cloud1"}}
        assert idx.all_index_servers == {1: {"engineName": "cloud1"}}

    def test_has_returns_true(self, mock_commcell):
        with patch.object(IndexServers, "_get_index_servers"), patch.object(
            IndexServers, "_get_all_roles"
        ):
            idx = IndexServers(mock_commcell)
            idx._all_index_servers = {1: {"engineName": "cloud1"}}
        assert idx.has("cloud1") is True

    def test_has_returns_false(self, mock_commcell):
        with patch.object(IndexServers, "_get_index_servers"), patch.object(
            IndexServers, "_get_all_roles"
        ):
            idx = IndexServers(mock_commcell)
            idx._all_index_servers = {1: {"engineName": "cloud1"}}
        assert idx.has("nonexistent") is False

    def test_len(self, mock_commcell):
        with patch.object(IndexServers, "_get_index_servers"), patch.object(
            IndexServers, "_get_all_roles"
        ):
            idx = IndexServers(mock_commcell)
            idx._all_index_servers = {1: {"engineName": "a"}, 2: {"engineName": "b"}}
        assert len(idx) == 2

    def test_get_properties_found(self, mock_commcell):
        with patch.object(IndexServers, "_get_index_servers"), patch.object(
            IndexServers, "_get_all_roles"
        ):
            idx = IndexServers(mock_commcell)
            idx._all_index_servers = {1: {"engineName": "cloud1", "cloudID": 1}}
        result = idx.get_properties("cloud1")
        assert result["engineName"] == "cloud1"

    def test_get_properties_not_found_raises(self, mock_commcell):
        with patch.object(IndexServers, "_get_index_servers"), patch.object(
            IndexServers, "_get_all_roles"
        ):
            idx = IndexServers(mock_commcell)
            idx._all_index_servers = {}
        with pytest.raises(SDKException):
            idx.get_properties("nonexistent")

    def test_get_nonexistent_raises(self, mock_commcell):
        with patch.object(IndexServers, "_get_index_servers"), patch.object(
            IndexServers, "_get_all_roles"
        ):
            idx = IndexServers(mock_commcell)
            idx._all_index_servers = {}
        with pytest.raises(SDKException):
            idx.get("nonexistent")
