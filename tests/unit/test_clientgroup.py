"""Unit tests for cvpysdk/clientgroup.py module."""

from unittest.mock import patch

import pytest

from cvpysdk.clientgroup import ClientGroup, ClientGroups
from cvpysdk.exception import SDKException


@pytest.mark.unit
class TestClientGroupsInit:
    """Tests for the ClientGroups collection class."""

    def test_repr(self, mock_commcell):
        with patch.object(ClientGroups, "_get_clientgroups", return_value={}):
            cgs = ClientGroups(mock_commcell)
        assert "ClientGroups" in repr(cgs)

    def test_all_clientgroups_property(self, mock_commcell):
        data = {"test-group": "1"}
        with patch.object(ClientGroups, "_get_clientgroups", return_value=data):
            cgs = ClientGroups(mock_commcell)
        assert cgs.all_clientgroups == data

    def test_len(self, mock_commcell):
        data = {"group1": "1", "group2": "2"}
        with patch.object(ClientGroups, "_get_clientgroups", return_value=data):
            cgs = ClientGroups(mock_commcell)
        assert len(cgs) == 2

    def test_len_empty(self, mock_commcell):
        with patch.object(ClientGroups, "_get_clientgroups", return_value={}):
            cgs = ClientGroups(mock_commcell)
        assert len(cgs) == 0


@pytest.mark.unit
class TestClientGroupsHasClientgroup:
    """Tests for ClientGroups.has_clientgroup."""

    def test_has_clientgroup_true(self, mock_commcell):
        data = {"test-group": "1"}
        with patch.object(ClientGroups, "_get_clientgroups", return_value=data):
            cgs = ClientGroups(mock_commcell)
        assert cgs.has_clientgroup("test-group") is True

    def test_has_clientgroup_bad_type_raises(self, mock_commcell):
        with patch.object(ClientGroups, "_get_clientgroups", return_value={}):
            cgs = ClientGroups(mock_commcell)
        with pytest.raises(SDKException):
            cgs.has_clientgroup(123)

    def test_has_clientgroup_case_insensitive(self, mock_commcell):
        data = {"test-group": "1"}
        with patch.object(ClientGroups, "_get_clientgroups", return_value=data):
            cgs = ClientGroups(mock_commcell)
        assert cgs.has_clientgroup("Test-Group") is True


@pytest.mark.unit
class TestClientGroupsGetItem:
    """Tests for ClientGroups.__getitem__."""

    def test_getitem_by_name(self, mock_commcell):
        data = {"test-group": "1"}
        with patch.object(ClientGroups, "_get_clientgroups", return_value=data):
            cgs = ClientGroups(mock_commcell)
        assert cgs["test-group"] == "1"

    def test_getitem_not_found(self, mock_commcell):
        with patch.object(ClientGroups, "_get_clientgroups", return_value={}):
            cgs = ClientGroups(mock_commcell)
        with pytest.raises(IndexError):
            cgs["nonexistent"]


@pytest.mark.unit
class TestClientGroupsRefresh:
    """Tests for ClientGroups.refresh."""

    def test_refresh_reloads(self, mock_commcell):
        with patch.object(ClientGroups, "_get_clientgroups", return_value={}) as mock_get:
            cgs = ClientGroups(mock_commcell)
            cgs.refresh()
            assert mock_get.call_count == 2


@pytest.mark.unit
class TestClientGroupRepr:
    """Tests for ClientGroup __repr__."""

    def test_repr_contains_name(self):
        with patch.object(ClientGroup, "__init__", lambda self, *a, **kw: None):
            cg = ClientGroup.__new__(ClientGroup)
            cg._clientgroup_name = "TestGroup"
            result = repr(cg)
            assert "TestGroup" in result


@pytest.mark.unit
class TestClientGroupProperties:
    """Tests for ClientGroup property getters."""

    def test_clientgroup_id(self):
        with patch.object(ClientGroup, "__init__", lambda self, *a, **kw: None):
            cg = ClientGroup.__new__(ClientGroup)
            cg._clientgroup_id = "42"
            assert cg.clientgroup_id == "42"

    def test_clientgroup_name(self):
        with patch.object(ClientGroup, "__init__", lambda self, *a, **kw: None):
            cg = ClientGroup.__new__(ClientGroup)
            cg._clientgroup_name = "MyGroup"
            assert cg.clientgroup_name == "MyGroup"
