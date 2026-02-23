"""Unit tests for cvpysdk.subclients.virtualserver.azure module."""

import pytest

from cvpysdk.subclients.virtualserver.azure import AzureSubclient
from cvpysdk.subclients.vssubclient import VirtualServerSubclient


@pytest.mark.unit
class TestAzureSubclient:
    """Tests for the AzureSubclient class."""

    def test_inherits_from_virtual_server_subclient(self):
        """Test that AzureSubclient is a subclass of VirtualServerSubclient."""
        assert issubclass(AzureSubclient, VirtualServerSubclient)

    def test_has_restore_methods(self):
        """Test that the class defines expected restore methods."""
        assert hasattr(AzureSubclient, "full_vm_restore_out_of_place")
        assert hasattr(AzureSubclient, "full_vm_restore_in_place")

    def test_class_importable(self):
        """Test that the class is importable from the module."""
        from cvpysdk.subclients.virtualserver import azure

        assert hasattr(azure, "AzureSubclient")
