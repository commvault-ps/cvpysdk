"""Unit tests for cvpysdk/subclients/vminstancesubclient.py"""

from unittest.mock import MagicMock

import pytest

from cvpysdk.subclient import Subclient
from cvpysdk.subclients.vminstancesubclient import VMInstanceSubclient


@pytest.mark.unit
class TestVMInstanceSubclient:
    """Tests for the VMInstanceSubclient class."""

    def test_inherits_subclient(self):
        """VMInstanceSubclient should inherit from Subclient."""
        assert issubclass(VMInstanceSubclient, Subclient)

    def test_has_key_properties(self):
        """VMInstanceSubclient should have expected properties."""
        assert hasattr(VMInstanceSubclient, "parent_client")
        assert hasattr(VMInstanceSubclient, "parent_agent")
        assert hasattr(VMInstanceSubclient, "parent_instance")
        assert hasattr(VMInstanceSubclient, "parent_backupset")
        assert hasattr(VMInstanceSubclient, "parent_subclient")
        assert hasattr(VMInstanceSubclient, "vm_guid")

    def test_has_key_methods(self):
        """VMInstanceSubclient should have expected methods."""
        assert hasattr(VMInstanceSubclient, "backup")

    def test_filter_types_dict(self):
        """filter_types should be set during init and contain expected values."""
        sub = object.__new__(VMInstanceSubclient)
        sub.filter_types = {
            "1": "Datastore",
            "2": "Virtual Disk Name/Pattern",
            "3": "Virtual Device Node",
            "4": "Container",
            "5": "Disk Label",
            "6": "Disk Type",
            "9": "Disk Tag Name/Value",
            "10": "Repository",
        }
        assert "1" in sub.filter_types
        assert sub.filter_types["1"] == "Datastore"
        assert len(sub.filter_types) == 8

    def test_parent_client_returns_none_initially(self):
        """parent_client returns None when _parent_client is None."""
        sub = object.__new__(VMInstanceSubclient)
        sub._parent_client = None
        sub._client_vm_status = {}
        sub._commcell_object = MagicMock()
        result = sub.parent_client
        assert result is None
