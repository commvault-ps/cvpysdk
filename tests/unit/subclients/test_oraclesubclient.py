"""Unit tests for cvpysdk/subclients/oraclesubclient.py"""

import pytest

from cvpysdk.subclients.dbsubclient import DatabaseSubclient
from cvpysdk.subclients.oraclesubclient import OracleSubclient


@pytest.mark.unit
class TestOracleSubclient:
    """Tests for the OracleSubclient class."""

    def test_inherits_database_subclient(self):
        """OracleSubclient should inherit from DatabaseSubclient."""
        assert issubclass(OracleSubclient, DatabaseSubclient)

    def test_has_key_properties(self):
        """OracleSubclient should have expected properties."""
        assert hasattr(OracleSubclient, "data")
        assert hasattr(OracleSubclient, "backup_archive_log")
        assert hasattr(OracleSubclient, "archive_delete")
        assert hasattr(OracleSubclient, "data_stream")
        assert hasattr(OracleSubclient, "data_sp")
        assert hasattr(OracleSubclient, "is_snapenabled")
        assert hasattr(OracleSubclient, "is_table_browse_enabled")

    def test_has_key_methods(self):
        """OracleSubclient should have expected methods."""
        assert hasattr(OracleSubclient, "backup")
        assert hasattr(OracleSubclient, "restore")
        assert hasattr(OracleSubclient, "restore_in_place")
        assert hasattr(OracleSubclient, "inline_backupcopy")
        assert hasattr(OracleSubclient, "enable_table_browse")
        assert hasattr(OracleSubclient, "disable_table_browse")
