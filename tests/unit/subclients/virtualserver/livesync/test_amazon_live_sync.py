"""Unit tests for cvpysdk.subclients.virtualserver.livesync.amazon_live_sync module."""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.exception import SDKException
from cvpysdk.subclients.virtualserver.livesync.amazon_live_sync import AmazonLiveSync
from cvpysdk.subclients.virtualserver.livesync.vsa_live_sync import VsaLiveSync


@pytest.mark.unit
class TestAmazonLiveSync:
    """Tests for the AmazonLiveSync class."""

    def test_inherits_from_vsa_live_sync(self):
        """Test that AmazonLiveSync is a subclass of VsaLiveSync."""
        assert issubclass(AmazonLiveSync, VsaLiveSync)

    def test_class_exists_and_importable(self):
        """Test that the class can be imported correctly."""
        from cvpysdk.subclients.virtualserver.livesync import amazon_live_sync

        assert hasattr(amazon_live_sync, "AmazonLiveSync")

    def test_has_configure_live_sync_method(self):
        """Test that configure_live_sync method exists."""
        assert hasattr(AmazonLiveSync, "configure_live_sync")

    def test_configure_live_sync_raises_on_non_string_vm(self):
        """Test configure_live_sync raises SDKException for non-string vm_to_restore."""
        with patch.object(AmazonLiveSync, "__new__", return_value=MagicMock(spec=AmazonLiveSync)):
            obj = AmazonLiveSync.__new__(AmazonLiveSync)
        obj._subclient_object = MagicMock()

        with pytest.raises(SDKException):
            AmazonLiveSync.configure_live_sync(obj, vm_to_restore=12345)

    def test_configure_live_sync_sets_default_restored_name(self):
        """Test that configure_live_sync defaults restored_vm_name to LiveSync_."""
        with patch.object(AmazonLiveSync, "__new__", return_value=MagicMock(spec=AmazonLiveSync)):
            obj = AmazonLiveSync.__new__(AmazonLiveSync)
        obj._subclient_object = MagicMock()
        obj._subclient_object._set_restore_inputs = MagicMock()
        obj._subclient_object._set_vm_to_restore = MagicMock(return_value=["vm1"])
        obj._configure_live_sync = MagicMock(return_value="schedule_obj")

        result = AmazonLiveSync.configure_live_sync(
            obj,
            schedule_name="sched1",
            vm_to_restore="vm1",
            destination_client="dest",
        )
        assert result == "schedule_obj"
        # Verify _configure_live_sync was called
        obj._configure_live_sync.assert_called_once()
