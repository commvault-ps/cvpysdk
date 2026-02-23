"""Unit tests for cvpysdk.subclients.virtualserver.vmware module."""

import pytest

from cvpysdk.subclients.virtualserver.vmware import VMWareVirtualServerSubclient
from cvpysdk.subclients.vssubclient import VirtualServerSubclient


@pytest.mark.unit
class TestVMWareVirtualServerSubclient:
    """Tests for the VMWareVirtualServerSubclient class."""

    def test_inherits_from_virtual_server_subclient(self):
        """Test that VMWareVirtualServerSubclient is a subclass of VirtualServerSubclient."""
        assert issubclass(VMWareVirtualServerSubclient, VirtualServerSubclient)

    def test_class_exists_and_importable(self):
        """Test that the class can be imported correctly."""
        from cvpysdk.subclients.virtualserver import vmware

        assert hasattr(vmware, "VMWareVirtualServerSubclient")

    def test_has_restore_methods(self):
        """Test that the class defines expected restore methods."""
        assert hasattr(VMWareVirtualServerSubclient, "full_vm_restore_in_place")
        assert hasattr(VMWareVirtualServerSubclient, "full_vm_restore_out_of_place")
        assert hasattr(VMWareVirtualServerSubclient, "disk_restore")
        assert hasattr(VMWareVirtualServerSubclient, "attach_disk_restore")

    def test_has_conversion_methods(self):
        """Test that the class defines VM conversion methods."""
        assert hasattr(VMWareVirtualServerSubclient, "full_vm_conversion_azurerm")
        assert hasattr(VMWareVirtualServerSubclient, "full_vm_conversion_hyperv")
        assert hasattr(VMWareVirtualServerSubclient, "full_vm_conversion_googlecloud")

    def test_has_blr_method(self):
        """Test that the class defines the BLR replication pair method."""
        assert hasattr(VMWareVirtualServerSubclient, "create_blr_replication_pair")

    def test_add_revert_option_with_revert_true(self):
        """Test add_revert_option sets revert when flag is True."""
        request_json = {
            "taskInfo": {"subTasks": [{"options": {"restoreOptions": {"commonOptions": {}}}}]}
        }
        result = VMWareVirtualServerSubclient.add_revert_option(None, request_json, True)
        common = result["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["commonOptions"]
        assert common["revert"] is True

    def test_add_revert_option_with_revert_false(self):
        """Test add_revert_option does not set revert when flag is False."""
        request_json = {
            "taskInfo": {"subTasks": [{"options": {"restoreOptions": {"commonOptions": {}}}}]}
        }
        result = VMWareVirtualServerSubclient.add_revert_option(None, request_json, False)
        common = result["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["commonOptions"]
        assert "revert" not in common
