"""Tests for cvpysdk/backupsets/_virtual_server/vmware.py."""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.backupsets._virtual_server.vmware import (
    VMwareBackupset,
    _BLRReplicationPair,
    _get_blr_pair_details,
)
from cvpysdk.backupsets.vsbackupset import VSBackupset
from cvpysdk.exception import SDKException


@pytest.mark.unit
class TestVMwareBackupsetInheritance:
    def test_inherits_vsbackupset(self):
        assert issubclass(VMwareBackupset, VSBackupset)

    def test_has_refresh_method(self):
        assert hasattr(VMwareBackupset, "refresh")

    def test_has_get_blr_replication_pair(self):
        assert hasattr(VMwareBackupset, "get_blr_replication_pair")


@pytest.mark.unit
class TestGetBlrPairDetails:
    def test_returns_dict_on_success(self):
        commcell = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "summary": {"totalPairs": 2},
            "siteInfo": [
                {"sourceName": "VM1", "id": 1},
                {"sourceName": "VM2", "id": 2},
            ],
        }
        commcell._cvpysdk_object.make_request.return_value = (
            True,
            mock_response,
        )

        result = _get_blr_pair_details(commcell)
        assert "VM1" in result
        assert "VM2" in result
        assert result["VM1"]["id"] == 1

    def test_returns_none_on_zero_pairs(self):
        commcell = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "summary": {"totalPairs": 0},
            "siteInfo": [],
        }
        commcell._cvpysdk_object.make_request.return_value = (
            True,
            mock_response,
        )
        result = _get_blr_pair_details(commcell)
        assert result is None

    def test_raises_on_key_error(self):
        commcell = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        commcell._cvpysdk_object.make_request.return_value = (
            True,
            mock_response,
        )
        with pytest.raises(SDKException):
            _get_blr_pair_details(commcell)


@pytest.mark.unit
class TestVMwareBackupsetGetBlrPair:
    def _make_instance(self):
        inst = object.__new__(VMwareBackupset)
        inst._commcell_object = MagicMock()
        inst._blr_pair_details = {"VM1": {"sourceName": "VM1", "id": 1, "status": 4}}
        return inst

    def test_get_blr_pair_returns_pair_object(self):
        inst = self._make_instance()
        pair = inst.get_blr_replication_pair("VM1")
        assert isinstance(pair, _BLRReplicationPair)

    def test_get_blr_pair_raises_for_unknown_vm(self):
        inst = self._make_instance()
        with pytest.raises(SDKException):
            inst.get_blr_replication_pair("UnknownVM")


@pytest.mark.unit
class TestBLRReplicationPair:
    def _make_pair(self):
        commcell = MagicMock()
        details = {
            "sourceName": "VM1",
            "sourceGuid": "guid-1",
            "id": 100,
            "status": 4,
            "tailClientId": 5,
        }
        return _BLRReplicationPair(commcell, "VM1", details)

    def test_status_enum(self):
        assert _BLRReplicationPair.Status.replicating.value == 4
        assert _BLRReplicationPair.Status.stop.value == 6
        assert _BLRReplicationPair.Status.suspend.value == 5

    def test_stop_updates_status(self):
        pair = self._make_pair()
        mock_response = MagicMock()
        mock_response.json.return_value = {"errorCode": 0}
        pair._commcell._cvpysdk_object.make_request.return_value = (
            True,
            mock_response,
        )
        with patch(
            "cvpysdk.backupsets._virtual_server.vmware._get_blr_pair_details",
            return_value={"VM1": {"status": 6}},
        ):
            pair.stop()
        assert pair._details["status"] == 6

    def test_suspend_updates_status(self):
        pair = self._make_pair()
        mock_response = MagicMock()
        mock_response.json.return_value = {"errorCode": 0}
        pair._commcell._cvpysdk_object.make_request.return_value = (
            True,
            mock_response,
        )
        with patch(
            "cvpysdk.backupsets._virtual_server.vmware._get_blr_pair_details",
            return_value={"VM1": {"status": 5}},
        ):
            pair.suspend()
        assert pair._details["status"] == 5

    def test_resync_updates_status(self):
        pair = self._make_pair()
        mock_response = MagicMock()
        mock_response.json.return_value = {"errorCode": 0}
        pair._commcell._cvpysdk_object.make_request.return_value = (
            True,
            mock_response,
        )
        with patch(
            "cvpysdk.backupsets._virtual_server.vmware._get_blr_pair_details",
            return_value={"VM1": {"status": 3}},
        ):
            pair.resync()
        assert pair._details["status"] == 3

    def test_get_vm_boot_info(self):
        pair = self._make_pair()
        info = pair._get_vm_boot_info("TestVM", 3600, "esx_host", "vm_network")
        assert info["vmUUId"] == "guid-1"
        assert info["vmName"] == "VM1"
        assert info["newVmName"] == "TestVM"
        assert info["lifeTimeInSec"] == 3600
        assert info["blrPairId"] == 100

    def test_get_admin_options(self):
        pair = self._make_pair()
        opts = pair._get_admin_options(operation_type=1)
        assert opts["blockOperation"]["operations"]["dstProxyClientId"] == 5
        assert opts["blockOperation"]["operations"]["opType"] == 1

    def test_resume_calls_start(self):
        pair = self._make_pair()
        pair.start = MagicMock()
        pair.resume()
        pair.start.assert_called_once()
