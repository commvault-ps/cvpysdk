"""Unit tests for cvpysdk/subclients/index_server_subclient.py"""

import pytest

from cvpysdk.subclients.bigdataappssubclient import BigDataAppsSubclient
from cvpysdk.subclients.index_server_subclient import IndexServerSubclient


@pytest.mark.unit
class TestIndexServerSubclient:
    """Tests for the IndexServerSubclient class."""

    def test_inherits_bigdataapps_subclient(self):
        """IndexServerSubclient should inherit from BigDataAppsSubclient."""
        assert issubclass(IndexServerSubclient, BigDataAppsSubclient)

    def test_has_key_methods(self):
        """IndexServerSubclient should have expected methods."""
        assert hasattr(IndexServerSubclient, "run_backup")
        assert hasattr(IndexServerSubclient, "configure_backup")
        assert hasattr(IndexServerSubclient, "do_restore_in_place")
        assert hasattr(IndexServerSubclient, "do_restore_out_of_place")
        assert hasattr(IndexServerSubclient, "get_file_details_from_backup")
        assert hasattr(IndexServerSubclient, "_get_path_for_restore")

    def test_run_backup_raises_for_invalid_level(self):
        """run_backup should raise SDKException for non-full backup level."""
        from cvpysdk.exception import SDKException

        subclient = object.__new__(IndexServerSubclient)
        with pytest.raises(SDKException):
            subclient.run_backup(backup_level="incremental")

    def test_do_restore_out_of_place_raises_for_invalid_types(self):
        """do_restore_out_of_place should raise SDKException for non-string args."""
        from cvpysdk.exception import SDKException

        subclient = object.__new__(IndexServerSubclient)
        with pytest.raises(SDKException):
            subclient.do_restore_out_of_place(dest_client=123, dest_path="/path")

    def test_configure_backup_raises_for_invalid_storage_policy(self):
        """configure_backup should raise SDKException for non-string storage policy."""
        from cvpysdk.exception import SDKException

        subclient = object.__new__(IndexServerSubclient)
        with pytest.raises(SDKException):
            subclient.configure_backup(storage_policy=123, role_content=["role1"])

    def test_configure_backup_raises_for_invalid_role_content(self):
        """configure_backup should raise SDKException for non-list role content."""
        from cvpysdk.exception import SDKException

        subclient = object.__new__(IndexServerSubclient)
        with pytest.raises(SDKException):
            subclient.configure_backup(storage_policy="test_policy", role_content="not_a_list")
