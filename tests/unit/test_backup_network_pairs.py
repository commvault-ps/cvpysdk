"""Unit tests for cvpysdk.backup_network_pairs module."""

from unittest.mock import MagicMock

import pytest

from cvpysdk.backup_network_pairs import BackupNetworkPairs
from cvpysdk.exception import SDKException


@pytest.mark.unit
class TestBackupNetworkPairs:
    """Tests for the BackupNetworkPairs class."""

    def test_init(self, mock_commcell):
        bnp = BackupNetworkPairs(mock_commcell)
        assert bnp._commcell_object is mock_commcell
        assert bnp.operation_type == ["ADD", "DELETE"]

    def test_repr(self, mock_commcell):
        bnp = BackupNetworkPairs(mock_commcell)
        assert repr(bnp) == "BackupNetworkPairs class instance for Commcell"

    def test_add_backup_interface_pairs_raises_on_non_list(self, mock_commcell):
        bnp = BackupNetworkPairs(mock_commcell)
        with pytest.raises(SDKException):
            bnp.add_backup_interface_pairs("not a list")

    def test_delete_backup_interface_pairs_raises_on_non_list(self, mock_commcell):
        bnp = BackupNetworkPairs(mock_commcell)
        with pytest.raises(SDKException):
            bnp.delete_backup_interface_pairs("not a list")

    def test_get_backup_interface_for_client(self, mock_commcell, mock_response):
        bnp = BackupNetworkPairs(mock_commcell)
        mock_commcell.clients = MagicMock()
        mock_commcell.clients.all_clients = {"testclient": {"id": 1}}
        resp = mock_response(json_data={"ArchPipeLineList": [{"srcip": "10.0.0.1"}]})
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        result = bnp.get_backup_interface_for_client("testclient")
        assert isinstance(result, list)
