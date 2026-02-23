"""Unit tests for cvpysdk.subclients.virtualserver.livesync.vmware_live_sync module."""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.subclients.virtualserver.livesync.vmware_live_sync import VMWareLiveSync
from cvpysdk.subclients.virtualserver.livesync.vsa_live_sync import VsaLiveSync


@pytest.mark.unit
class TestVMWareLiveSync:
    """Tests for the VMWareLiveSync class."""

    def test_inherits_from_vsa_live_sync(self):
        """Test that VMWareLiveSync is a subclass of VsaLiveSync."""
        assert issubclass(VMWareLiveSync, VsaLiveSync)

    def test_class_exists_and_importable(self):
        """Test that the class can be imported correctly."""
        from cvpysdk.subclients.virtualserver.livesync import vmware_live_sync

        assert hasattr(vmware_live_sync, "VMWareLiveSync")

    def test_has_configure_live_sync_method(self):
        """Test that configure_live_sync method exists."""
        assert hasattr(VMWareLiveSync, "configure_live_sync")

    def test_configure_live_sync_sets_default_restored_name(self):
        """Test that configure_live_sync defaults restored_vm_name to LiveSync_."""
        with patch.object(VMWareLiveSync, "__new__", return_value=MagicMock(spec=VMWareLiveSync)):
            obj = VMWareLiveSync.__new__(VMWareLiveSync)
        obj._subclient_object = MagicMock()
        obj._subclient_object._set_restore_inputs = MagicMock()
        obj._subclient_object._set_vm_to_restore = MagicMock(return_value=["vm1"])
        obj._configure_live_sync = MagicMock(return_value="schedule_obj")

        result = VMWareLiveSync.configure_live_sync(
            obj,
            schedule_name="sched1",
            vm_to_restore="vm1",
            destination_client="dest",
        )
        assert result == "schedule_obj"
        obj._configure_live_sync.assert_called_once()

    def test_configure_live_sync_passes_correct_arguments(self):
        """Test that configure_live_sync passes schedule_name to _configure_live_sync."""
        with patch.object(VMWareLiveSync, "__new__", return_value=MagicMock(spec=VMWareLiveSync)):
            obj = VMWareLiveSync.__new__(VMWareLiveSync)
        obj._subclient_object = MagicMock()
        obj._subclient_object._set_restore_inputs = MagicMock()
        obj._subclient_object._set_vm_to_restore = MagicMock(return_value=["vm1"])
        obj._configure_live_sync = MagicMock(return_value="schedule_obj")

        VMWareLiveSync.configure_live_sync(
            obj,
            schedule_name="my_schedule",
            vm_to_restore="vm1",
        )
        call_args = obj._configure_live_sync.call_args
        assert call_args[0][0] == "my_schedule"
