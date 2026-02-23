from unittest.mock import patch

import pytest

from cvpysdk.activateapps.ediscovery_utils import EdiscoveryClients
from cvpysdk.activateapps.file_storage_optimization import (
    FsoServerGroups,
    FsoServers,
)
from cvpysdk.exception import SDKException


@pytest.mark.unit
class TestFsoServers:
    """Tests for the FsoServers collection class."""

    def _make_fso_servers(self, mock_commcell, servers=None):
        with patch.object(
            FsoServers, "_get_all_fso_servers", return_value=servers or {}
        ), patch.object(EdiscoveryClients, "__init__", return_value=None):
            return FsoServers(mock_commcell)

    def test_has_server_true(self, mock_commcell):
        servers = {"testserver": {"client_id": 1}}
        s = self._make_fso_servers(mock_commcell, servers=servers)
        assert s.has_server("testserver") is True

    def test_has_server_non_string_raises(self, mock_commcell):
        s = self._make_fso_servers(mock_commcell)
        with pytest.raises(SDKException):
            s.has_server(123)

    def test_get_nonexistent_raises(self, mock_commcell):
        s = self._make_fso_servers(mock_commcell)
        with pytest.raises(SDKException):
            s.get("nonexistent")

    def test_refresh_calls_get(self, mock_commcell):
        with patch.object(
            FsoServers, "_get_all_fso_servers", return_value={}
        ) as mock_get, patch.object(EdiscoveryClients, "__init__", return_value=None):
            s = FsoServers(mock_commcell)
            s.refresh()
        assert mock_get.call_count == 2


@pytest.mark.unit
class TestFsoServerGroups:
    """Tests for the FsoServerGroups collection class."""

    def _make_fso_server_groups(self, mock_commcell, groups=None):
        with patch.object(
            FsoServerGroups, "_get_all_fso_server_groups", return_value=groups or {}
        ), patch.object(EdiscoveryClients, "__init__", return_value=None):
            return FsoServerGroups(mock_commcell)

    def test_has_group_true(self, mock_commcell):
        groups = {"testgroup": {"server_group_id": 1}}
        sg = self._make_fso_server_groups(mock_commcell, groups=groups)
        assert sg.has("testgroup") is True

    def test_has_group_non_string_raises(self, mock_commcell):
        sg = self._make_fso_server_groups(mock_commcell)
        with pytest.raises(SDKException):
            sg.has(123)

    def test_get_nonexistent_raises(self, mock_commcell):
        sg = self._make_fso_server_groups(mock_commcell)
        with pytest.raises(SDKException):
            sg.get("nonexistent")

    def test_refresh_calls_get(self, mock_commcell):
        with patch.object(
            FsoServerGroups, "_get_all_fso_server_groups", return_value={}
        ) as mock_get, patch.object(EdiscoveryClients, "__init__", return_value=None):
            sg = FsoServerGroups(mock_commcell)
            sg.refresh()
        assert mock_get.call_count == 2
