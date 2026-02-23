"""Unit tests for cvpysdk.subclients.virtualserver.null module."""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.exception import SDKException
from cvpysdk.subclients.virtualserver.null import NullSubclient
from cvpysdk.subclients.vssubclient import VirtualServerSubclient


@pytest.mark.unit
class TestNullSubclient:
    """Tests for the NullSubclient class."""

    def test_inherits_from_virtual_server_subclient(self):
        """Test that NullSubclient is a subclass of VirtualServerSubclient."""
        assert issubclass(NullSubclient, VirtualServerSubclient)

    def test_class_exists_and_importable(self):
        """Test that the class can be imported correctly."""
        from cvpysdk.subclients.virtualserver import null

        assert hasattr(null, "NullSubclient")

    def test_init_raises_sdk_exception(self):
        """Test that creating a NullSubclient raises SDKException."""
        backupset_obj = MagicMock()
        backupset_obj._instance_object.instance_name = "unsupported_instance"

        with patch.object(
            VirtualServerSubclient, "__new__", lambda cls, *a, **k: object.__new__(cls)
        ):
            with pytest.raises(SDKException):
                NullSubclient(backupset_obj, "test_sub", "123")

    def test_init_exception_message_contains_instance_name(self):
        """Test that the exception message references the instance name."""
        backupset_obj = MagicMock()
        backupset_obj._instance_object.instance_name = "MyInstance"

        with patch.object(
            VirtualServerSubclient, "__new__", lambda cls, *a, **k: object.__new__(cls)
        ):
            with pytest.raises(SDKException, match="MyInstance"):
                NullSubclient(backupset_obj, "test_sub", "123")

    def test_init_raises_with_subclient_module(self):
        """Test that SDKException is raised with Subclient module."""
        backupset_obj = MagicMock()
        backupset_obj._instance_object.instance_name = "test"

        with patch.object(
            VirtualServerSubclient, "__new__", lambda cls, *a, **k: object.__new__(cls)
        ):
            with pytest.raises(SDKException) as exc_info:
                NullSubclient(backupset_obj, "test_sub", "123")
            assert "Subclient" in str(exc_info.value)
