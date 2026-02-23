"""Unit tests for cvpysdk.subclients.virtualserver.azure_stack module."""

import pytest

from cvpysdk.subclients.virtualserver.azure_stack import AzureStackSubclient
from cvpysdk.subclients.vssubclient import VirtualServerSubclient


@pytest.mark.unit
class TestAzureStackSubclient:
    """Tests for the AzureStackSubclient class."""

    def test_inherits_from_virtual_server_subclient(self):
        """Test that AzureStackSubclient is a subclass of VirtualServerSubclient."""
        assert issubclass(AzureStackSubclient, VirtualServerSubclient)

    def test_has_restore_methods(self):
        """Test that the class defines expected restore methods."""
        assert hasattr(AzureStackSubclient, "full_vm_restore_out_of_place")
        assert hasattr(AzureStackSubclient, "full_vm_restore_in_place")

    def test_class_importable(self):
        """Test that the class is importable from the module."""
        from cvpysdk.subclients.virtualserver import azure_stack

        assert hasattr(azure_stack, "AzureStackSubclient")
