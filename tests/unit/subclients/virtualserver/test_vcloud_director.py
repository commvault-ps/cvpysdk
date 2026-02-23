"""Unit tests for cvpysdk.subclients.virtualserver.vcloud_director module."""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.subclients.virtualserver.vcloud_director import (
    VcloudVirtualServerSubclient,
)
from cvpysdk.subclients.vssubclient import VirtualServerSubclient


@pytest.mark.unit
class TestVcloudVirtualServerSubclient:
    """Tests for the VcloudVirtualServerSubclient class."""

    def test_inherits_from_virtual_server_subclient(self):
        """Test that VcloudVirtualServerSubclient is a subclass of VirtualServerSubclient."""
        assert issubclass(VcloudVirtualServerSubclient, VirtualServerSubclient)

    def test_class_exists_and_importable(self):
        """Test that the class can be imported correctly."""
        from cvpysdk.subclients.virtualserver import vcloud_director

        assert hasattr(vcloud_director, "VcloudVirtualServerSubclient")

    def test_init_sets_disk_extension(self):
        """Test that __init__ sets diskExtension correctly."""
        with patch.object(
            VirtualServerSubclient, "__new__", lambda cls, *a, **k: object.__new__(cls)
        ):
            with patch.object(VirtualServerSubclient, "__init__", return_value=None):
                obj = VcloudVirtualServerSubclient(MagicMock(), "test_sub", "123")

        assert obj.diskExtension == [".vmdk"]

    def test_init_sets_disk_option(self):
        """Test that __init__ sets _disk_option correctly."""
        with patch.object(
            VirtualServerSubclient, "__new__", lambda cls, *a, **k: object.__new__(cls)
        ):
            with patch.object(VirtualServerSubclient, "__init__", return_value=None):
                obj = VcloudVirtualServerSubclient(MagicMock(), "test_sub", "123")

        assert obj._disk_option == {
            "Original": 0,
            "Thick Lazy Zero": 1,
            "Thin": 2,
            "Thick Eager Zero": 3,
        }

    def test_init_sets_transport_mode(self):
        """Test that __init__ sets _transport_mode correctly."""
        with patch.object(
            VirtualServerSubclient, "__new__", lambda cls, *a, **k: object.__new__(cls)
        ):
            with patch.object(VirtualServerSubclient, "__init__", return_value=None):
                obj = VcloudVirtualServerSubclient(MagicMock(), "test_sub", "123")

        assert obj._transport_mode == {
            "Auto": 0,
            "SAN": 1,
            "Hot Add": 2,
            "NBD": 5,
            "NBD SSL": 4,
        }
