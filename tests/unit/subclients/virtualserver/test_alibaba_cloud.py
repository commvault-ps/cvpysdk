"""Unit tests for cvpysdk.subclients.virtualserver.alibaba_cloud module."""

import pytest

from cvpysdk.subclients.virtualserver.alibaba_cloud import (
    AlibabaCloudVirtualServerSubclient,
)
from cvpysdk.subclients.vssubclient import VirtualServerSubclient


@pytest.mark.unit
class TestAlibabaCloudVirtualServerSubclient:
    """Tests for the AlibabaCloudVirtualServerSubclient class."""

    def test_inherits_from_virtual_server_subclient(self):
        """Test correct inheritance chain."""
        assert issubclass(AlibabaCloudVirtualServerSubclient, VirtualServerSubclient)

    def test_has_restore_method(self):
        """Test that the class defines the out-of-place restore method."""
        assert hasattr(AlibabaCloudVirtualServerSubclient, "full_vm_restore_out_of_place")

    def test_class_importable(self):
        """Test that the class is importable from the module."""
        from cvpysdk.subclients.virtualserver import alibaba_cloud

        assert hasattr(alibaba_cloud, "AlibabaCloudVirtualServerSubclient")
