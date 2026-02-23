"""Unit tests for cvpysdk/subclients/nassubclient.py"""

import pytest

from cvpysdk.subclients.fssubclient import FileSystemSubclient
from cvpysdk.subclients.nassubclient import NASSubclient


@pytest.mark.unit
class TestNASSubclient:
    """Tests for the NASSubclient class."""

    def test_inherits_filesystem_subclient(self):
        """NASSubclient should inherit from FileSystemSubclient."""
        assert issubclass(NASSubclient, FileSystemSubclient)

    def test_has_key_methods(self):
        """NASSubclient should have expected methods."""
        assert hasattr(NASSubclient, "backup")
        assert hasattr(NASSubclient, "restore_in_place")
        assert hasattr(NASSubclient, "restore_out_of_place")

    def test_backup_method_signature(self):
        """backup should accept NAS-specific parameters."""
        import inspect

        sig = inspect.signature(NASSubclient.backup)
        param_names = list(sig.parameters.keys())
        assert "snap_name" in param_names
        assert "backup_external_links" in param_names
        assert "backup_offline_data" in param_names
        assert "block_backup" in param_names
        assert "volume_based_backup" in param_names

    def test_restore_in_place_signature(self):
        """restore_in_place should accept NAS-specific options."""
        import inspect

        sig = inspect.signature(NASSubclient.restore_in_place)
        param_names = list(sig.parameters.keys())
        assert "synth_restore" in param_names
        assert "DAR" in param_names
        assert "noRecursive" in param_names
