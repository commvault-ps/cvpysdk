"""Unit tests for cvpysdk/subclients/vssubclient.py"""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.subclient import Subclient
from cvpysdk.subclients.vssubclient import VirtualServerSubclient


@pytest.mark.unit
class TestVirtualServerSubclient:
    """Tests for the VirtualServerSubclient class."""

    def test_inherits_subclient(self):
        """VirtualServerSubclient should inherit from Subclient."""
        assert issubclass(VirtualServerSubclient, Subclient)

    def test_has_new_method(self):
        """VirtualServerSubclient should have __new__ method."""
        assert hasattr(VirtualServerSubclient, "__new__")

    def test_has_key_methods(self):
        """VirtualServerSubclient should have expected methods."""
        assert hasattr(VirtualServerSubclient, "backup")
        assert hasattr(VirtualServerSubclient, "browse")
        assert hasattr(VirtualServerSubclient, "disk_level_browse")
        assert hasattr(VirtualServerSubclient, "guest_files_browse")

    def test_new_dispatches_to_vmware_subclient(self):
        """__new__ should dispatch to VMwareSubclient for VMware instance type."""
        from cvpysdk.constants import VsInstanceType

        backupset_obj = MagicMock()
        backupset_obj._instance_object._vsinstancetype = 1  # VMware

        with patch.dict(VsInstanceType.VSINSTANCE_TYPE, {1: "vmware"}, clear=False):
            result = VirtualServerSubclient.__new__(
                VirtualServerSubclient, backupset_obj, "test_subclient"
            )
            assert isinstance(result, VirtualServerSubclient)
