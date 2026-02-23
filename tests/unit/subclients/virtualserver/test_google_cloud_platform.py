"""Unit tests for cvpysdk.subclients.virtualserver.google_cloud_platform module."""

import pytest

from cvpysdk.subclients.virtualserver.google_cloud_platform import (
    GooglecloudVirtualServerSubclient,
)
from cvpysdk.subclients.vssubclient import VirtualServerSubclient


@pytest.mark.unit
class TestGooglecloudVirtualServerSubclient:
    """Tests for the GooglecloudVirtualServerSubclient class."""

    def test_inherits_from_virtual_server_subclient(self):
        """Test correct inheritance chain."""
        assert issubclass(GooglecloudVirtualServerSubclient, VirtualServerSubclient)

    def test_has_restore_methods(self):
        """Test that the class defines expected restore methods."""
        assert hasattr(GooglecloudVirtualServerSubclient, "full_vm_restore_in_place")
        assert hasattr(GooglecloudVirtualServerSubclient, "full_vm_restore_out_of_place")

    def test_class_importable(self):
        """Test that the class is importable from the module."""
        from cvpysdk.subclients.virtualserver import google_cloud_platform

        assert hasattr(google_cloud_platform, "GooglecloudVirtualServerSubclient")
