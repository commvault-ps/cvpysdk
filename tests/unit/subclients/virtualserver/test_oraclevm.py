"""Unit tests for cvpysdk.subclients.virtualserver.oraclevm module."""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.exception import SDKException
from cvpysdk.subclients.virtualserver.oraclevm import (
    OracleVMVirtualServerSubclient,
)
from cvpysdk.subclients.vssubclient import VirtualServerSubclient


@pytest.mark.unit
class TestOracleVMVirtualServerSubclient:
    """Tests for the OracleVMVirtualServerSubclient class."""

    def test_inherits_from_virtual_server_subclient(self):
        """Test that OracleVMVirtualServerSubclient is a subclass of VirtualServerSubclient."""
        assert issubclass(OracleVMVirtualServerSubclient, VirtualServerSubclient)

    def test_class_exists_and_importable(self):
        """Test that the class can be imported correctly."""
        from cvpysdk.subclients.virtualserver import oraclevm

        assert hasattr(oraclevm, "OracleVMVirtualServerSubclient")

    def test_has_restore_methods(self):
        """Test that the class defines expected restore methods."""
        assert hasattr(OracleVMVirtualServerSubclient, "full_vm_restore_in_place")
        assert hasattr(OracleVMVirtualServerSubclient, "full_vm_restore_out_of_place")

    def test_init_sets_disk_extension(self):
        """Test that __init__ sets diskExtension correctly."""
        with patch.object(
            VirtualServerSubclient, "__new__", lambda cls, *a, **k: object.__new__(cls)
        ):
            with patch.object(VirtualServerSubclient, "__init__", return_value=None):
                obj = OracleVMVirtualServerSubclient(MagicMock(), "test_sub", "123")

        assert obj.diskExtension == [".img"]

    def test_full_vm_restore_out_of_place_raises_on_invalid_vm_type(self):
        """Test that full_vm_restore_out_of_place raises SDKException for non-string vm."""
        with patch.object(
            VirtualServerSubclient, "__new__", lambda cls, *a, **k: object.__new__(cls)
        ):
            with patch.object(OracleVMVirtualServerSubclient, "__init__", return_value=None):
                obj = OracleVMVirtualServerSubclient(MagicMock(), "test_sub")

        with pytest.raises(SDKException):
            obj.full_vm_restore_out_of_place(vm_to_restore=12345)
