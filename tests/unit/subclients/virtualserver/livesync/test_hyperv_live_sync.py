"""Unit tests for cvpysdk.subclients.virtualserver.livesync.hyperv_live_sync module."""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.exception import SDKException
from cvpysdk.subclients.virtualserver.livesync.hyperv_live_sync import HyperVLiveSync
from cvpysdk.subclients.virtualserver.livesync.vsa_live_sync import VsaLiveSync


@pytest.mark.unit
class TestHyperVLiveSync:
    """Tests for the HyperVLiveSync class."""

    def test_inherits_from_vsa_live_sync(self):
        """Test that HyperVLiveSync is a subclass of VsaLiveSync."""
        assert issubclass(HyperVLiveSync, VsaLiveSync)

    def test_class_exists_and_importable(self):
        """Test that the class can be imported correctly."""
        from cvpysdk.subclients.virtualserver.livesync import hyperv_live_sync

        assert hasattr(hyperv_live_sync, "HyperVLiveSync")

    def test_has_configure_live_sync_method(self):
        """Test that configure_live_sync method exists."""
        assert hasattr(HyperVLiveSync, "configure_live_sync")

    def test_configure_live_sync_raises_on_non_string_vm(self):
        """Test configure_live_sync raises SDKException for non-string vm_to_restore."""
        with patch.object(HyperVLiveSync, "__new__", return_value=MagicMock(spec=HyperVLiveSync)):
            obj = HyperVLiveSync.__new__(HyperVLiveSync)
        obj._subclient_object = MagicMock()

        with pytest.raises(SDKException):
            HyperVLiveSync.configure_live_sync(obj, vm_to_restore=12345)

    def test_configure_live_sync_raises_on_non_string_destination_path(self):
        """Test configure_live_sync raises when destination_path is not a string."""
        with patch.object(HyperVLiveSync, "__new__", return_value=MagicMock(spec=HyperVLiveSync)):
            obj = HyperVLiveSync.__new__(HyperVLiveSync)
        obj._subclient_object = MagicMock()
        obj._subclient_object._set_vm_to_restore = MagicMock(return_value=["vm1"])

        with pytest.raises(SDKException):
            HyperVLiveSync.configure_live_sync(
                obj,
                vm_to_restore="vm1",
                destination_path=12345,
                overwrite=True,
                power_on=True,
            )
