"""Unit tests for cvpysdk.subclients.virtualserver.xen module."""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.subclients.virtualserver.xen import Xen
from cvpysdk.subclients.vssubclient import VirtualServerSubclient


@pytest.mark.unit
class TestXen:
    """Tests for the Xen class."""

    def test_inherits_from_virtual_server_subclient(self):
        """Test that Xen is a subclass of VirtualServerSubclient."""
        assert issubclass(Xen, VirtualServerSubclient)

    def test_class_exists_and_importable(self):
        """Test that the class can be imported correctly."""
        from cvpysdk.subclients.virtualserver import xen

        assert hasattr(xen, "Xen")

    def test_has_restore_methods(self):
        """Test that the class defines expected restore methods."""
        assert hasattr(Xen, "full_vm_restore_in_place")
        assert hasattr(Xen, "full_vm_restore_out_of_place")

    def test_init_sets_disk_extension(self):
        """Test that __init__ sets diskExtension correctly."""
        with patch.object(
            VirtualServerSubclient, "__new__", lambda cls, *a, **k: object.__new__(cls)
        ):
            with patch.object(VirtualServerSubclient, "__init__", return_value=None):
                obj = Xen(MagicMock(), "test_sub", "123")

        assert obj.diskExtension == ["none"]

    def test_full_vm_restore_in_place_calls_process_restore(self):
        """Test that full_vm_restore_in_place calls _process_restore_response."""
        with patch.object(
            VirtualServerSubclient, "__new__", lambda cls, *a, **k: object.__new__(cls)
        ):
            with patch.object(Xen, "__init__", return_value=None):
                obj = Xen(MagicMock(), "test_sub")
        obj._set_restore_inputs = MagicMock()
        obj._set_vm_to_restore = MagicMock(return_value=["vm1"])
        obj._prepare_fullvm_restore_json = MagicMock(return_value={"taskInfo": {}})
        obj._process_restore_response = MagicMock(return_value="job_obj")

        result = obj.full_vm_restore_in_place(vm_to_restore="vm1")
        assert result == "job_obj"
        obj._process_restore_response.assert_called_once()
