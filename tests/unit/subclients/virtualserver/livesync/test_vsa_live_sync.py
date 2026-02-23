"""Unit tests for cvpysdk.subclients.virtualserver.livesync.vsa_live_sync module."""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.exception import SDKException
from cvpysdk.subclients.virtualserver.livesync.vsa_live_sync import (
    LiveSyncPairs,
    LiveSyncVMPair,
    VsaLiveSync,
)


@pytest.mark.unit
class TestVsaLiveSync:
    """Tests for the VsaLiveSync class."""

    def test_class_exists_and_importable(self):
        from cvpysdk.subclients.virtualserver.livesync import vsa_live_sync

        assert hasattr(vsa_live_sync, "VsaLiveSync")

    def test_new_raises_for_unsupported_instance(self):
        subclient_obj = MagicMock()
        subclient_obj._instance_object.instance_name = "unsupported_hypervisor"
        with pytest.raises(SDKException, match="not yet supported"):
            VsaLiveSync(subclient_obj)

    def test_live_sync_subtask_json_static_method(self):
        result = VsaLiveSync._live_sync_subtask_json("my_schedule")
        assert result["subTaskType"] == "RESTORE"
        assert result["operationType"] == "SITE_REPLICATION"
        assert result["subTaskName"] == "my_schedule"

    def test_get_raises_on_non_string(self):
        obj = MagicMock(spec=VsaLiveSync)
        obj._live_sync_pairs = {}
        with pytest.raises(SDKException):
            VsaLiveSync.get(obj, 12345)

    def test_has_live_sync_pair_returns_falsy_when_empty(self):
        obj = MagicMock(spec=VsaLiveSync)
        type(obj).live_sync_pairs = property(lambda self: {})
        result = VsaLiveSync.has_live_sync_pair(obj, "nonexistent")
        assert not result

    def test_has_live_sync_pair_returns_true_when_exists(self):
        obj = MagicMock(spec=VsaLiveSync)
        type(obj).live_sync_pairs = property(lambda self: {"mypair": {"id": "1"}})
        result = VsaLiveSync.has_live_sync_pair(obj, "mypair")
        assert result is True


@pytest.mark.unit
class TestLiveSyncPairs:
    """Tests for the LiveSyncPairs class."""

    def test_class_exists_and_importable(self):
        from cvpysdk.subclients.virtualserver.livesync import vsa_live_sync

        assert hasattr(vsa_live_sync, "LiveSyncPairs")

    def test_repr_contains_subclient_name(self):
        with patch.object(LiveSyncPairs, "__init__", lambda self, *a, **k: None):
            obj = LiveSyncPairs.__new__(LiveSyncPairs)
        obj._subclient_name = "test_sc"
        assert "test_sc" in repr(obj)

    def test_live_sync_id_property(self):
        with patch.object(LiveSyncPairs, "__init__", lambda self, *a, **k: None):
            obj = LiveSyncPairs.__new__(LiveSyncPairs)
        obj._live_sync_id = "42"
        assert obj.live_sync_id == "42"

    def test_live_sync_name_property(self):
        with patch.object(LiveSyncPairs, "__init__", lambda self, *a, **k: None):
            obj = LiveSyncPairs.__new__(LiveSyncPairs)
        obj._live_sync_name = "pair1"
        assert obj.live_sync_name == "pair1"

    def test_has_vm_pair_returns_falsy_when_empty(self):
        with patch.object(LiveSyncPairs, "__init__", lambda self, *a, **k: None):
            obj = LiveSyncPairs.__new__(LiveSyncPairs)
        obj._vm_pairs = {}
        assert not obj.has_vm_pair("nonexistent")

    def test_get_raises_on_non_string(self):
        with patch.object(LiveSyncPairs, "__init__", lambda self, *a, **k: None):
            obj = LiveSyncPairs.__new__(LiveSyncPairs)
        obj._vm_pairs = {}
        with pytest.raises(SDKException):
            obj.get(123)


@pytest.mark.unit
class TestLiveSyncVMPair:
    """Tests for the LiveSyncVMPair class."""

    def test_class_exists_and_importable(self):
        from cvpysdk.subclients.virtualserver.livesync import vsa_live_sync

        assert hasattr(vsa_live_sync, "LiveSyncVMPair")

    def test_repr_contains_live_sync_name(self):
        with patch.object(LiveSyncVMPair, "__init__", lambda self, *a, **k: None):
            obj = LiveSyncVMPair.__new__(LiveSyncVMPair)
        mock_pair = MagicMock()
        mock_pair.live_sync_name = "mypair"
        obj.live_sync_pair = mock_pair
        assert "mypair" in repr(obj)

    def test_vm_pair_id_property(self):
        with patch.object(LiveSyncVMPair, "__init__", lambda self, *a, **k: None):
            obj = LiveSyncVMPair.__new__(LiveSyncVMPair)
        obj._vm_pair_id = "99"
        assert obj.vm_pair_id == "99"

    def test_vm_pair_name_property(self):
        with patch.object(LiveSyncVMPair, "__init__", lambda self, *a, **k: None):
            obj = LiveSyncVMPair.__new__(LiveSyncVMPair)
        obj._vm_pair_name = "vm1"
        assert obj.vm_pair_name == "vm1"

    def test_str_contains_source_and_destination(self):
        with patch.object(LiveSyncVMPair, "__init__", lambda self, *a, **k: None):
            obj = LiveSyncVMPair.__new__(LiveSyncVMPair)
        obj._source_vm = "srcVM"
        obj._destination_vm = "dstVM"
        s = str(obj)
        assert "srcVM" in s
        assert "dstVM" in s
