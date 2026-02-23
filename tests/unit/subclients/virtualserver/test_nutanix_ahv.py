"""Unit tests for cvpysdk.subclients.virtualserver.nutanix_ahv module."""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.subclients.virtualserver.nutanix_ahv import nutanixsubclient
from cvpysdk.subclients.vssubclient import VirtualServerSubclient


@pytest.mark.unit
class TestNutanixSubclient:
    """Tests for the nutanixsubclient class."""

    def test_inherits_from_virtual_server_subclient(self):
        assert issubclass(nutanixsubclient, VirtualServerSubclient)

    def test_class_exists_and_importable(self):
        from cvpysdk.subclients.virtualserver import nutanix_ahv

        assert hasattr(nutanix_ahv, "nutanixsubclient")

    def test_has_restore_methods(self):
        assert hasattr(nutanixsubclient, "full_vm_restore_in_place")
        assert hasattr(nutanixsubclient, "full_vm_restore_out_of_place")
        assert hasattr(nutanixsubclient, "full_vm_conversion_vmware")

    def test_init_sets_disk_extension(self):
        with patch.object(
            VirtualServerSubclient, "__new__", lambda cls, *a, **k: object.__new__(cls)
        ):
            with patch.object(VirtualServerSubclient, "__init__", return_value=None):
                obj = nutanixsubclient(MagicMock(), "test_sub", "123")
        assert obj.diskExtension == ["none"]

    def test_full_vm_restore_in_place_calls_process_restore(self):
        with patch.object(
            VirtualServerSubclient, "__new__", lambda cls, *a, **k: object.__new__(cls)
        ):
            with patch.object(nutanixsubclient, "__init__", return_value=None):
                obj = nutanixsubclient(MagicMock(), "test_sub")
        obj._set_restore_inputs = MagicMock()
        obj._set_vm_to_restore = MagicMock(return_value=["vm1"])
        obj._prepare_fullvm_restore_json = MagicMock(return_value={"taskInfo": {}})
        obj._process_restore_response = MagicMock(return_value="job_obj")
        result = obj.full_vm_restore_in_place(vm_to_restore="vm1")
        assert result == "job_obj"
