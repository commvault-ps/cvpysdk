"""Unit tests for cvpysdk.subclients.virtualserver.hyperv module."""

from enum import Enum

import pytest

from cvpysdk.subclients.virtualserver.hyperv import HyperVVirtualServerSubclient
from cvpysdk.subclients.vssubclient import VirtualServerSubclient


@pytest.mark.unit
class TestHyperVVirtualServerSubclient:
    """Tests for the HyperVVirtualServerSubclient class."""

    def test_inherits_from_virtual_server_subclient(self):
        """Test that HyperVVirtualServerSubclient is a subclass of VirtualServerSubclient."""
        assert issubclass(HyperVVirtualServerSubclient, VirtualServerSubclient)

    def test_has_restore_methods(self):
        """Test that the class defines expected restore methods."""
        assert hasattr(HyperVVirtualServerSubclient, "full_vm_restore_in_place")
        assert hasattr(HyperVVirtualServerSubclient, "full_vm_restore_out_of_place")
        assert hasattr(HyperVVirtualServerSubclient, "disk_restore")

    def test_has_conversion_methods(self):
        """Test that the class defines VM conversion methods."""
        assert hasattr(HyperVVirtualServerSubclient, "full_vm_conversion_vmware")
        assert hasattr(HyperVVirtualServerSubclient, "full_vm_conversion_azurerm")

    def test_disk_pattern_enum(self):
        """Test that disk_pattern enum is defined with correct values."""
        dp = HyperVVirtualServerSubclient.disk_pattern
        assert issubclass(dp, Enum)
        assert dp.name.value == "name"
        assert dp.datastore.value == "DestinationPath"
        assert dp.new_name.value == "new_name"

    def test_get_guest_os_method_exists(self):
        """Test that _get_guest_os method exists."""
        assert hasattr(HyperVVirtualServerSubclient, "_get_guest_os")
