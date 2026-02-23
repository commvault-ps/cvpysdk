"""Unit tests for cvpysdk.subclients.virtualserver.oracle_cloud_infrastructure module."""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.exception import SDKException
from cvpysdk.subclients.virtualserver.oracle_cloud_infrastructure import (
    OCIVirtualServerSubclient,
)
from cvpysdk.subclients.vssubclient import VirtualServerSubclient


@pytest.mark.unit
class TestOCIVirtualServerSubclient:
    """Tests for the OCIVirtualServerSubclient class."""

    def test_inherits_from_virtual_server_subclient(self):
        """Test that OCIVirtualServerSubclient is a subclass of VirtualServerSubclient."""
        assert issubclass(OCIVirtualServerSubclient, VirtualServerSubclient)

    def test_class_exists_and_importable(self):
        """Test that the class can be imported correctly."""
        from cvpysdk.subclients.virtualserver import oracle_cloud_infrastructure

        assert hasattr(oracle_cloud_infrastructure, "OCIVirtualServerSubclient")

    def test_has_restore_methods(self):
        """Test that the class defines expected restore methods."""
        assert hasattr(OCIVirtualServerSubclient, "full_vm_restore_in_place")
        assert hasattr(OCIVirtualServerSubclient, "full_vm_restore_out_of_place")
        assert hasattr(OCIVirtualServerSubclient, "set_advanced_vm_restore_options")

    def test_init_sets_disk_extension_and_attributes(self):
        """Test that __init__ sets diskExtension and vm_obj/source_vm_details/hvobj."""
        with patch.object(
            VirtualServerSubclient, "__new__", lambda cls, *a, **k: object.__new__(cls)
        ):
            with patch.object(VirtualServerSubclient, "__init__", return_value=None):
                obj = OCIVirtualServerSubclient(MagicMock(), "test_sub", "123")

        assert obj.diskExtension == ["none"]
        assert obj.vm_obj is None
        assert obj.source_vm_details is None
        assert obj.hvobj is None

    def test_full_vm_restore_in_place_raises_on_invalid_types(self):
        """Test that full_vm_restore_in_place raises SDKException for non-bool overwrite."""
        with patch.object(
            VirtualServerSubclient, "__new__", lambda cls, *a, **k: object.__new__(cls)
        ):
            with patch.object(OCIVirtualServerSubclient, "__init__", return_value=None):
                obj = OCIVirtualServerSubclient(MagicMock(), "test_sub")

        with pytest.raises(SDKException):
            obj.full_vm_restore_in_place(
                source_vm_details={"source_ip": "1.2.3.4"},
                overwrite="not_bool",
                power_on=True,
            )
