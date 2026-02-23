"""Unit tests for cvpysdk.subclients.virtualserver.amazon_web_services module."""

from enum import Enum

import pytest

from cvpysdk.subclients.virtualserver.amazon_web_services import (
    AmazonVirtualServerSubclient,
)
from cvpysdk.subclients.vssubclient import VirtualServerSubclient


@pytest.mark.unit
class TestAmazonVirtualServerSubclient:
    """Tests for the AmazonVirtualServerSubclient class."""

    def test_inherits_from_virtual_server_subclient(self):
        """Test that AmazonVirtualServerSubclient is a subclass of VirtualServerSubclient."""
        assert issubclass(AmazonVirtualServerSubclient, VirtualServerSubclient)

    def test_has_restore_methods(self):
        """Test that the class defines expected restore methods."""
        assert hasattr(AmazonVirtualServerSubclient, "full_vm_restore_in_place")
        assert hasattr(AmazonVirtualServerSubclient, "full_vm_restore_out_of_place")
        assert hasattr(AmazonVirtualServerSubclient, "attach_disk_restore")

    def test_has_conversion_method(self):
        """Test that the class defines VM conversion methods."""
        assert hasattr(AmazonVirtualServerSubclient, "full_vm_conversion_azurerm")

    def test_disk_pattern_enum(self):
        """Test that disk_pattern enum is defined with correct values."""
        dp = AmazonVirtualServerSubclient.disk_pattern
        assert issubclass(dp, Enum)
        assert dp.name.value == "name"
        assert dp.datastore.value == "availabilityZone"
        assert dp.new_name.value == "newName"
        assert dp.aws_bucket.value == "Datastore"
