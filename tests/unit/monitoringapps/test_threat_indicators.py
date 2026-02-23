"""Unit tests for cvpysdk.monitoringapps.threat_indicators module."""

from unittest.mock import MagicMock

import pytest

from cvpysdk.exception import SDKException
from cvpysdk.monitoringapps.threat_indicators import AnomalyType, TAServer, TAServers


@pytest.mark.unit
class TestAnomalyType:
    """Tests for the AnomalyType enum."""

    def test_anomaly_type_values(self):
        """Test AnomalyType enum has expected members and values."""
        assert AnomalyType.FILE_ACTIVITY.value == 16
        assert AnomalyType.FILE_TYPE.value == 32
        assert AnomalyType.THREAT_ANALYSIS.value == 64
        assert AnomalyType.FILE_DATA.value == 128
        assert AnomalyType.EXTENSION_BASED.value == 512
        assert AnomalyType.DATA_WRITTEN.value == 4096


@pytest.mark.unit
class TestTAServers:
    """Tests for the TAServers class."""

    def _make_taservers(self, mock_commcell, mock_response):
        """Helper to create a TAServers instance with mocked API calls."""
        # Mock the three API calls in refresh()
        indicators_resp = mock_response(
            json_data={"anomalyClients": [{"client": {"displayName": "server1", "clientId": 1}}]}
        )
        clients_resp = mock_response(json_data={"fileServers": 1, "vms": 2, "laptops": 0})
        vm_resp = mock_response(json_data={"monitoredVMs": 5})

        mock_commcell._cvpysdk_object.make_request.side_effect = [
            (True, indicators_resp),
            (True, clients_resp),
            (True, vm_resp),
        ]
        return TAServers(mock_commcell)

    def test_init(self, mock_commcell, mock_response):
        """Test constructor initializes and calls refresh."""
        servers = self._make_taservers(mock_commcell, mock_response)
        assert "server1" in servers._servers
        assert servers._total_clients is not None
        assert servers._monitored_vms is not None

    def test_has_existing_server(self, mock_commcell, mock_response):
        """Test has returns True for existing server."""
        servers = self._make_taservers(mock_commcell, mock_response)
        assert servers.has("server1") is True

    def test_has_nonexistent_server(self, mock_commcell, mock_response):
        """Test has returns False for non-existing server."""
        servers = self._make_taservers(mock_commcell, mock_response)
        assert servers.has("nonexistent") is False

    def test_get_existing_server(self, mock_commcell, mock_response):
        """Test get returns TAServer for existing server."""
        servers = self._make_taservers(mock_commcell, mock_response)

        # Mock the TAServer init dependencies
        mock_client = MagicMock()
        mock_client.client_id = 1
        mock_commcell.clients.get.return_value = mock_client

        # Mock the refresh calls in TAServer.__init__
        anomaly_resp = mock_response(json_data={"clientInfo": [{"anomalyRecordList": []}]})
        stats_resp = mock_response(
            json_data={
                "anomalyClients": [
                    {
                        "client": {"displayName": "server1"},
                        "infectedFilesCount": 0,
                        "fingerPrintFilesCount": 0,
                        "createCount": 0,
                        "deleteCount": 0,
                        "modCount": 0,
                        "renameCount": 0,
                        "dataSourceId": 0,
                    }
                ]
            }
        )
        mock_commcell._cvpysdk_object.make_request.side_effect = [
            (True, anomaly_resp),
            (True, stats_resp),
        ]

        result = servers.get("server1")
        assert isinstance(result, TAServer)

    def test_get_nonexistent_raises(self, mock_commcell, mock_response):
        """Test get raises SDKException for non-existing server."""
        servers = self._make_taservers(mock_commcell, mock_response)
        with pytest.raises(SDKException):
            servers.get("nonexistent")

    def test_get_invalid_type_raises(self, mock_commcell, mock_response):
        """Test get raises SDKException for non-string input."""
        servers = self._make_taservers(mock_commcell, mock_response)
        with pytest.raises(SDKException):
            servers.get(123)

    def test_run_scan_invalid_server_name_type(self, mock_commcell, mock_response):
        """Test run_scan raises for non-string server_name."""
        servers = self._make_taservers(mock_commcell, mock_response)
        with pytest.raises(SDKException):
            servers.run_scan(123, [AnomalyType.FILE_ACTIVITY])

    def test_run_scan_invalid_anomaly_types(self, mock_commcell, mock_response):
        """Test run_scan raises for non-list anomaly_types."""
        servers = self._make_taservers(mock_commcell, mock_response)
        with pytest.raises(SDKException):
            servers.run_scan("server1", "not_a_list")

    def test_clients_count_property(self, mock_commcell, mock_response):
        """Test clients_count returns cached value."""
        servers = self._make_taservers(mock_commcell, mock_response)
        assert servers.clients_count is not None

    def test_monitored_vms_property(self, mock_commcell, mock_response):
        """Test monitored_vms returns cached value."""
        servers = self._make_taservers(mock_commcell, mock_response)
        assert servers.monitored_vms is not None


@pytest.mark.unit
class TestTAServer:
    """Tests for the TAServer class."""

    def _make_taserver(self, mock_commcell, mock_response):
        """Helper to create a TAServer instance."""
        mock_client = MagicMock()
        mock_client.client_id = 1
        mock_commcell.clients.get.return_value = mock_client

        anomaly_resp = mock_response(
            json_data={"clientInfo": [{"anomalyRecordList": [{"file": "test.txt"}]}]}
        )
        stats_resp = mock_response(
            json_data={
                "anomalyClients": [
                    {
                        "client": {"displayName": "server1"},
                        "infectedFilesCount": 5,
                        "fingerPrintFilesCount": 3,
                        "createCount": 10,
                        "deleteCount": 20,
                        "modCount": 30,
                        "renameCount": 2,
                        "dataSourceId": 42,
                    }
                ]
            }
        )
        mock_commcell._cvpysdk_object.make_request.side_effect = [
            (True, anomaly_resp),
            (True, stats_resp),
        ]
        return TAServer(mock_commcell, "server1")

    def test_init(self, mock_commcell, mock_response):
        """Test TAServer constructor initializes correctly."""
        server = self._make_taserver(mock_commcell, mock_response)
        assert server._server_name == "server1"
        assert server._server_id == 1

    def test_anomaly_records_property(self, mock_commcell, mock_response):
        """Test anomaly_records returns list of records."""
        server = self._make_taserver(mock_commcell, mock_response)
        assert server.anomaly_records == [{"file": "test.txt"}]

    def test_anomaly_stats_property(self, mock_commcell, mock_response):
        """Test anomaly_stats returns file type stats."""
        server = self._make_taserver(mock_commcell, mock_response)
        stats = server.anomaly_stats
        assert stats["createCount"] == 10
        assert stats["deleteCount"] == 20

    def test_threat_anomaly_stats_property(self, mock_commcell, mock_response):
        """Test threat_anomaly_stats returns threat stats."""
        server = self._make_taserver(mock_commcell, mock_response)
        threat_stats = server.threat_anomaly_stats
        assert threat_stats["infectedFilesCount"] == 5
        assert threat_stats["fingerPrintFilesCount"] == 3

    def test_datasource_id_property(self, mock_commcell, mock_response):
        """Test datasource_id returns correct value."""
        server = self._make_taserver(mock_commcell, mock_response)
        assert server.datasource_id == 42

    def test_anomaly_file_count(self, mock_commcell, mock_response):
        """Test anomaly_file_count sums all counts."""
        server = self._make_taserver(mock_commcell, mock_response)
        # anomaly_stats: 10+20+30+2 = 62
        # threat_stats: 5+3 = 8
        # total = 70
        assert server.anomaly_file_count == 70

    def test_clear_anomaly_invalid_type_raises(self, mock_commcell, mock_response):
        """Test clear_anomaly raises for non-list input."""
        server = self._make_taserver(mock_commcell, mock_response)
        with pytest.raises(SDKException):
            server.clear_anomaly("not_a_list")
