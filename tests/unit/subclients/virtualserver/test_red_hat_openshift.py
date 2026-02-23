"""Unit tests for cvpysdk.subclients.virtualserver.red_hat_openshift module."""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.subclients.virtualserver.red_hat_openshift import OpenshiftSubclient
from cvpysdk.subclients.vssubclient import VirtualServerSubclient


@pytest.mark.unit
class TestOpenshiftSubclient:
    """Tests for the OpenshiftSubclient class."""

    def test_inherits_from_virtual_server_subclient(self):
        """Test that OpenshiftSubclient is a subclass of VirtualServerSubclient."""
        assert issubclass(OpenshiftSubclient, VirtualServerSubclient)

    def test_class_exists_and_importable(self):
        """Test that the class can be imported correctly."""
        from cvpysdk.subclients.virtualserver import red_hat_openshift

        assert hasattr(red_hat_openshift, "OpenshiftSubclient")

    def test_init_calls_parent_init(self):
        """Test that __init__ calls parent class __init__."""
        with patch.object(
            VirtualServerSubclient, "__new__", lambda cls, *a, **k: object.__new__(cls)
        ):
            with patch.object(VirtualServerSubclient, "__init__", return_value=None) as mock_init:
                backupset = MagicMock()
                OpenshiftSubclient(backupset, "test_sub", "123")
                mock_init.assert_called_once_with(backupset, "test_sub", "123")

    def test_no_additional_restore_methods(self):
        """Test that OpenshiftSubclient does not define its own restore methods."""
        assert "full_vm_restore_in_place" not in OpenshiftSubclient.__dict__
        assert "full_vm_restore_out_of_place" not in OpenshiftSubclient.__dict__
