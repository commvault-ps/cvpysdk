"""Unit tests for cvpysdk.subclients.virtualserver.openstack module."""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.exception import SDKException
from cvpysdk.subclients.virtualserver.openstack import (
    OpenStackVirtualServerSubclient,
)
from cvpysdk.subclients.vssubclient import VirtualServerSubclient


@pytest.mark.unit
class TestOpenStackVirtualServerSubclient:
    """Tests for the OpenStackVirtualServerSubclient class."""

    def test_inherits_from_virtual_server_subclient(self):
        """Test that OpenStackVirtualServerSubclient is a subclass of VirtualServerSubclient."""
        assert issubclass(OpenStackVirtualServerSubclient, VirtualServerSubclient)

    def test_class_exists_and_importable(self):
        """Test that the class can be imported correctly."""
        from cvpysdk.subclients.virtualserver import openstack

        assert hasattr(openstack, "OpenStackVirtualServerSubclient")

    def test_has_restore_methods(self):
        """Test that the class defines expected restore methods."""
        assert hasattr(OpenStackVirtualServerSubclient, "full_vm_restore_in_place")
        assert hasattr(OpenStackVirtualServerSubclient, "full_vm_restore_out_of_place")
        assert hasattr(OpenStackVirtualServerSubclient, "disk_restore")
        assert hasattr(OpenStackVirtualServerSubclient, "attach_disk_restore")

    def test_init_sets_disk_extension(self):
        """Test that __init__ sets diskExtension correctly."""
        with patch.object(
            VirtualServerSubclient, "__new__", lambda cls, *a, **k: object.__new__(cls)
        ):
            with patch.object(VirtualServerSubclient, "__init__", return_value=None):
                obj = OpenStackVirtualServerSubclient(MagicMock(), "test_sub", "123")

        assert obj.diskExtension == ["none"]

    def test_full_vm_restore_in_place_raises_on_invalid_vm_type(self):
        """Test that full_vm_restore_in_place raises SDKException for non-string vm_to_restore."""
        with patch.object(
            VirtualServerSubclient, "__new__", lambda cls, *a, **k: object.__new__(cls)
        ):
            with patch.object(OpenStackVirtualServerSubclient, "__init__", return_value=None):
                obj = OpenStackVirtualServerSubclient(MagicMock(), "test_sub")

        with pytest.raises(SDKException):
            obj.full_vm_restore_in_place(vm_to_restore=12345)
