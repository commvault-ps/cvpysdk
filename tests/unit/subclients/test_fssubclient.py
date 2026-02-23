"""Unit tests for cvpysdk/subclients/fssubclient.py"""

import pytest

from cvpysdk.subclient import Subclient
from cvpysdk.subclients.fssubclient import FileSystemSubclient


@pytest.mark.unit
class TestFileSystemSubclient:
    """Tests for the FileSystemSubclient class."""

    def test_inherits_subclient(self):
        """FileSystemSubclient should inherit from Subclient."""
        assert issubclass(FileSystemSubclient, Subclient)

    def test_has_key_methods(self):
        """FileSystemSubclient should have expected methods."""
        assert hasattr(FileSystemSubclient, "restore_in_place")
        assert hasattr(FileSystemSubclient, "restore_out_of_place")
        assert hasattr(FileSystemSubclient, "backup")
        assert hasattr(FileSystemSubclient, "find_all_versions")
        assert hasattr(FileSystemSubclient, "run_backup_copy")
        assert hasattr(FileSystemSubclient, "enable_content_indexing")
        assert hasattr(FileSystemSubclient, "disable_content_indexing")
        assert hasattr(FileSystemSubclient, "preview_backedup_file")

    def test_has_key_properties(self):
        """FileSystemSubclient should have expected properties."""
        assert hasattr(FileSystemSubclient, "content")
        assert hasattr(FileSystemSubclient, "filter_content")
        assert hasattr(FileSystemSubclient, "exception_content")
        assert hasattr(FileSystemSubclient, "scan_type")
        assert hasattr(FileSystemSubclient, "trueup_option")
        assert hasattr(FileSystemSubclient, "backup_retention")
        assert hasattr(FileSystemSubclient, "backup_retention_days")
        assert hasattr(FileSystemSubclient, "block_level_backup_option")

    def test_has_ibmi_properties(self):
        """FileSystemSubclient should have IBM i specific properties."""
        assert hasattr(FileSystemSubclient, "generate_signature_on_ibmi")
        assert hasattr(FileSystemSubclient, "backup_using_multiple_drives")
        assert hasattr(FileSystemSubclient, "pending_record_changes")
        assert hasattr(FileSystemSubclient, "other_pending_changes")
        assert hasattr(FileSystemSubclient, "object_level_backup")

    def test_has_archiver_properties(self):
        """FileSystemSubclient should have archiver properties."""
        assert hasattr(FileSystemSubclient, "archiver_retention")
        assert hasattr(FileSystemSubclient, "archiver_retention_days")
        assert hasattr(FileSystemSubclient, "disk_cleanup")
        assert hasattr(FileSystemSubclient, "disk_cleanup_rules")
        assert hasattr(FileSystemSubclient, "backup_only_archiving_candidate")
        assert hasattr(FileSystemSubclient, "file_version")

    def test_has_system_state_and_onetouch(self):
        """FileSystemSubclient should have system state and one-touch options."""
        assert hasattr(FileSystemSubclient, "system_state_option")
        assert hasattr(FileSystemSubclient, "onetouch_option")
        assert hasattr(FileSystemSubclient, "onetouch_server")
        assert hasattr(FileSystemSubclient, "onetouch_server_directory")

    def test_has_network_share_properties(self):
        """FileSystemSubclient should have network share and impersonation props."""
        assert hasattr(FileSystemSubclient, "network_share_auto_mount")
        assert hasattr(FileSystemSubclient, "impersonate_user")
        assert hasattr(FileSystemSubclient, "plan")
