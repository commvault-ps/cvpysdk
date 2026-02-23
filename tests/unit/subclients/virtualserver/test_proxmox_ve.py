"""Unit tests for cvpysdk.subclients.virtualserver.proxmox_ve module."""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.subclients.virtualserver.proxmox_ve import ProxmoxSubclient
from cvpysdk.subclients.vssubclient import VirtualServerSubclient


@pytest.mark.unit
class TestProxmoxSubclient:
    """Tests for the ProxmoxSubclient class."""

    def test_inherits_from_virtual_server_subclient(self):
        """Test that ProxmoxSubclient is a subclass of VirtualServerSubclient."""
        assert issubclass(ProxmoxSubclient, VirtualServerSubclient)

    def test_class_exists_and_importable(self):
        """Test that the class can be imported correctly."""
        from cvpysdk.subclients.virtualserver import proxmox_ve

        assert hasattr(proxmox_ve, "ProxmoxSubclient")

    def test_has_restore_methods(self):
        """Test that the class defines expected restore methods."""
        assert hasattr(ProxmoxSubclient, "full_vm_restore_in_place")
        assert hasattr(ProxmoxSubclient, "full_vm_restore_out_of_place")

    def test_init_sets_disk_extension(self):
        """Test that __init__ sets diskExtension correctly."""
        with patch.object(
            VirtualServerSubclient, "__new__", lambda cls, *a, **k: object.__new__(cls)
        ):
            with patch.object(VirtualServerSubclient, "__init__", return_value=None):
                obj = ProxmoxSubclient(MagicMock(), "test_sub", "123")

        assert obj.diskExtension == [
            "ide",
            "scsi",
            "sata",
            "virtio",
            "qcow2",
            "none",
        ]

    def test_full_vm_restore_in_place_wraps_string_vm_to_list(self):
        """Test that full_vm_restore_in_place wraps a string vm_to_restore into a list."""
        with patch.object(
            VirtualServerSubclient, "__new__", lambda cls, *a, **k: object.__new__(cls)
        ):
            with patch.object(ProxmoxSubclient, "__init__", return_value=None):
                obj = ProxmoxSubclient(MagicMock(), "test_sub")
        obj._set_restore_inputs = MagicMock()
        obj._set_vm_to_restore = MagicMock(return_value=["vm1"])
        obj._prepare_fullvm_restore_json = MagicMock(return_value={"taskInfo": {}})
        obj._process_restore_response = MagicMock(return_value="job_obj")

        obj.full_vm_restore_in_place(
            vm_to_restore="vm1",
            destination_client="dest",
            proxy_client=None,
            overwrite=True,
            power_on=True,
            copy_precedence=0,
        )
        obj._set_vm_to_restore.assert_called_once_with(["vm1"])
