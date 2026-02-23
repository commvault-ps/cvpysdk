"""Unit tests for cvpysdk.subclients.virtualserver.fusioncompute module."""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.subclients.virtualserver.fusioncompute import (
    FusionComputeVirtualServerSubclient,
)
from cvpysdk.subclients.vssubclient import VirtualServerSubclient


@pytest.mark.unit
class TestFusionComputeVirtualServerSubclient:
    """Tests for the FusionComputeVirtualServerSubclient class."""

    def test_inherits_from_virtual_server_subclient(self):
        """Test FusionComputeVirtualServerSubclient inherits VirtualServerSubclient."""
        assert issubclass(FusionComputeVirtualServerSubclient, VirtualServerSubclient)

    def test_class_exists_and_importable(self):
        """Test that the class can be imported correctly."""
        from cvpysdk.subclients.virtualserver import fusioncompute

        assert hasattr(fusioncompute, "FusionComputeVirtualServerSubclient")

    def test_has_restore_methods(self):
        """Test that the class defines expected restore methods."""
        assert hasattr(FusionComputeVirtualServerSubclient, "full_vm_restore_in_place")
        assert hasattr(FusionComputeVirtualServerSubclient, "full_vm_restore_out_of_place")

    def test_init_sets_disk_extension_and_options(self):
        """Test that __init__ sets diskExtension and _disk_option correctly."""
        with patch.object(
            VirtualServerSubclient, "__new__", lambda cls, *a, **k: object.__new__(cls)
        ):
            with patch.object(VirtualServerSubclient, "__init__", return_value=None):
                obj = FusionComputeVirtualServerSubclient(MagicMock(), "test_sub", "123")

        assert obj.diskExtension == ["none"]
        assert obj._disk_option == {
            "original": 0,
            "thicklazyzero": 1,
            "thin": 2,
            "common": 3,
        }

    def test_full_vm_restore_in_place_calls_process_restore(self):
        """Test that full_vm_restore_in_place calls _process_restore_response."""
        with patch.object(
            VirtualServerSubclient, "__new__", lambda cls, *a, **k: object.__new__(cls)
        ):
            with patch.object(FusionComputeVirtualServerSubclient, "__init__", return_value=None):
                obj = FusionComputeVirtualServerSubclient(MagicMock(), "test_sub")
        obj._set_restore_inputs = MagicMock()
        obj._set_vm_to_restore = MagicMock(return_value=["vm1"])
        obj._prepare_fullvm_restore_json = MagicMock(return_value={"taskInfo": {}})
        obj._process_restore_response = MagicMock(return_value="job_obj")

        result = obj.full_vm_restore_in_place(vm_to_restore="vm1")
        assert result == "job_obj"
        obj._process_restore_response.assert_called_once()
