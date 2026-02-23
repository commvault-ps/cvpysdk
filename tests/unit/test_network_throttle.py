"""Unit tests for cvpysdk.network_throttle module."""

from unittest.mock import MagicMock

import pytest

from cvpysdk.network_throttle import NetworkThrottle


@pytest.mark.unit
class TestNetworkThrottle:
    """Tests for the NetworkThrottle class."""

    def _make_throttle(self, mock_commcell):
        """Create a NetworkThrottle instance backed by a mock Client."""
        throttle = NetworkThrottle.__new__(NetworkThrottle)
        throttle._class_object = MagicMock()
        throttle._commcell_object = mock_commcell
        throttle.flag = ""
        throttle.is_client = True
        throttle.is_client_group = None
        throttle._client_object = MagicMock()
        throttle._enable_network_throttling = True
        throttle._share_bandwidth = True
        throttle._throttle_schedules = []
        throttle._remote_client_groups = []
        throttle._remote_clients = [
            {"clientName": "client1"},
            {"clientName": "client2"},
        ]
        return throttle

    def test_enable_network_throttle_getter(self, mock_commcell):
        throttle = self._make_throttle(mock_commcell)
        assert throttle.enable_network_throttle is True

    def test_share_bandwidth_getter(self, mock_commcell):
        throttle = self._make_throttle(mock_commcell)
        assert throttle.share_bandwidth is True

    def test_remote_clients_getter(self, mock_commcell):
        throttle = self._make_throttle(mock_commcell)
        assert throttle.remote_clients == ["client1", "client2"]

    def test_remote_client_groups_getter(self, mock_commcell):
        throttle = self._make_throttle(mock_commcell)
        assert throttle.remote_client_groups == []

    def test_throttle_schedules_getter(self, mock_commcell):
        throttle = self._make_throttle(mock_commcell)
        assert throttle.throttle_schedules == []
