"""Unit tests for cvpysdk.subclients.virtualserver.oracle_cloud module."""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.subclients.virtualserver.oracle_cloud import (
    OracleCloudVirtualServerSubclient,
)
from cvpysdk.subclients.vssubclient import VirtualServerSubclient


@pytest.mark.unit
class TestOracleCloudVirtualServerSubclient:
    """Tests for the OracleCloudVirtualServerSubclient class."""

    def test_inherits_from_virtual_server_subclient(self):
        """Test that OracleCloudVirtualServerSubclient inherits VirtualServerSubclient."""
        assert issubclass(OracleCloudVirtualServerSubclient, VirtualServerSubclient)

    def test_class_exists_and_importable(self):
        """Test that the class can be imported correctly."""
        from cvpysdk.subclients.virtualserver import oracle_cloud

        assert hasattr(oracle_cloud, "OracleCloudVirtualServerSubclient")

    def test_has_restore_methods(self):
        """Test that the class defines the full_vm_restore_out_of_place method."""
        assert hasattr(OracleCloudVirtualServerSubclient, "full_vm_restore_out_of_place")

    def test_full_vm_restore_out_of_place_calls_process_restore(self):
        """Test that full_vm_restore_out_of_place calls _process_restore_response."""
        with patch.object(
            VirtualServerSubclient, "__new__", lambda cls, *a, **k: object.__new__(cls)
        ):
            with patch.object(OracleCloudVirtualServerSubclient, "__init__", return_value=None):
                obj = OracleCloudVirtualServerSubclient(MagicMock(), "test_sub")
        obj._set_restore_inputs = MagicMock()
        obj._set_vm_to_restore = MagicMock(return_value=["vm1"])
        obj._prepare_fullvm_restore_json = MagicMock(return_value={"taskInfo": {}})
        obj._process_restore_response = MagicMock(return_value="job_obj")

        result = obj.full_vm_restore_out_of_place(vm_to_restore=["vm1"])
        assert result == "job_obj"
        obj._process_restore_response.assert_called_once()

    def test_no_custom_init_defined(self):
        """Test that OracleCloudVirtualServerSubclient does not define __init__."""
        assert "__init__" not in OracleCloudVirtualServerSubclient.__dict__
