"""Unit tests for cvpysdk.subclients.virtualserver.red_hat_virtualization module."""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.exception import SDKException
from cvpysdk.subclients.virtualserver.red_hat_virtualization import (
    RhevVirtualServerSubclient,
)
from cvpysdk.subclients.vssubclient import VirtualServerSubclient


@pytest.mark.unit
class TestRhevVirtualServerSubclient:
    """Tests for the RhevVirtualServerSubclient class."""

    def test_inherits_from_virtual_server_subclient(self):
        """Test that RhevVirtualServerSubclient is a subclass of VirtualServerSubclient."""
        assert issubclass(RhevVirtualServerSubclient, VirtualServerSubclient)

    def test_class_exists_and_importable(self):
        """Test that the class can be imported correctly."""
        from cvpysdk.subclients.virtualserver import red_hat_virtualization

        assert hasattr(red_hat_virtualization, "RhevVirtualServerSubclient")

    def test_has_restore_methods(self):
        """Test that the class defines expected restore methods."""
        assert hasattr(RhevVirtualServerSubclient, "full_vm_restore_in_place")
        assert hasattr(RhevVirtualServerSubclient, "full_vm_restore_out_of_place")

    def test_init_sets_disk_extension_and_options(self):
        """Test that __init__ sets diskExtension and _disk_option correctly."""
        with patch.object(
            VirtualServerSubclient, "__new__", lambda cls, *a, **k: object.__new__(cls)
        ):
            with patch.object(VirtualServerSubclient, "__init__", return_value=None):
                obj = RhevVirtualServerSubclient(MagicMock(), "test_sub", "123")

        assert obj.diskExtension == ["none"]
        assert obj._disk_option == {
            "Original": 0,
            "Thick Lazy Zero": 1,
            "Thin": 2,
            "Thick Eager Zero": 3,
        }

    def test_full_vm_restore_in_place_raises_on_invalid_vm_type(self):
        """Test that full_vm_restore_in_place raises SDKException for non-string vm."""
        with patch.object(
            VirtualServerSubclient, "__new__", lambda cls, *a, **k: object.__new__(cls)
        ):
            with patch.object(RhevVirtualServerSubclient, "__init__", return_value=None):
                obj = RhevVirtualServerSubclient(MagicMock(), "test_sub")

        with pytest.raises(SDKException):
            obj.full_vm_restore_in_place(vm_to_restore=12345)
