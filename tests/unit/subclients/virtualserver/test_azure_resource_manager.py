"""Unit tests for cvpysdk.subclients.virtualserver.azure_resource_manager module."""

import pytest

from cvpysdk.subclients.virtualserver.azure_resource_manager import AzureRMSubclient
from cvpysdk.subclients.vssubclient import VirtualServerSubclient


@pytest.mark.unit
class TestAzureRMSubclient:
    """Tests for the AzureRMSubclient class."""

    def test_inherits_from_virtual_server_subclient(self):
        """Test that AzureRMSubclient is a subclass of VirtualServerSubclient."""
        assert issubclass(AzureRMSubclient, VirtualServerSubclient)

    def test_has_restore_methods(self):
        """Test that the class defines expected restore methods."""
        assert hasattr(AzureRMSubclient, "full_vm_restore_out_of_place")
        assert hasattr(AzureRMSubclient, "full_vm_restore_in_place")

    def test_has_conversion_methods(self):
        """Test that the class defines VM conversion methods."""
        assert hasattr(AzureRMSubclient, "full_vm_conversion_azurestack")
        assert hasattr(AzureRMSubclient, "full_vm_conversion_amazon")
        assert hasattr(AzureRMSubclient, "full_vm_conversion_hyperv")
        assert hasattr(AzureRMSubclient, "full_vm_conversion_vmware")

    def test_class_importable(self):
        """Test that the class is importable from the module."""
        from cvpysdk.subclients.virtualserver import azure_resource_manager

        assert hasattr(azure_resource_manager, "AzureRMSubclient")
