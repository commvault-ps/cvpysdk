"""Unit tests for cvpysdk.subclients.virtualserver.livesync.azure_live_sync module."""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.exception import SDKException
from cvpysdk.subclients.virtualserver.livesync.azure_live_sync import AzureLiveSync
from cvpysdk.subclients.virtualserver.livesync.vsa_live_sync import VsaLiveSync


@pytest.mark.unit
class TestAzureLiveSync:
    """Tests for the AzureLiveSync class."""

    def test_inherits_from_vsa_live_sync(self):
        """Test that AzureLiveSync is a subclass of VsaLiveSync."""
        assert issubclass(AzureLiveSync, VsaLiveSync)

    def test_class_exists_and_importable(self):
        """Test that the class can be imported correctly."""
        from cvpysdk.subclients.virtualserver.livesync import azure_live_sync

        assert hasattr(azure_live_sync, "AzureLiveSync")

    def test_has_configure_live_sync_method(self):
        """Test that configure_live_sync method exists."""
        assert hasattr(AzureLiveSync, "configure_live_sync")

    def test_configure_live_sync_raises_on_non_string_vm(self):
        """Test configure_live_sync raises SDKException for non-string vm_to_restore."""
        with patch.object(AzureLiveSync, "__new__", return_value=MagicMock(spec=AzureLiveSync)):
            obj = AzureLiveSync.__new__(AzureLiveSync)
        obj._subclient_object = MagicMock()

        with pytest.raises(SDKException):
            AzureLiveSync.configure_live_sync(obj, vm_to_restore=12345)

    def test_configure_live_sync_raises_on_non_bool_overwrite(self):
        """Test configure_live_sync raises when unconditional_overwrite is not bool."""
        with patch.object(AzureLiveSync, "__new__", return_value=MagicMock(spec=AzureLiveSync)):
            obj = AzureLiveSync.__new__(AzureLiveSync)
        obj._subclient_object = MagicMock()
        obj._subclient_object._set_vm_to_restore = MagicMock(return_value=["vm1"])

        with pytest.raises(SDKException):
            AzureLiveSync.configure_live_sync(
                obj,
                vm_to_restore="vm1",
                unconditional_overwrite="not_bool",
                power_on=True,
            )
