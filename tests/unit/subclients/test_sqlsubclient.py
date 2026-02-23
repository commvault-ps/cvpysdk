"""Unit tests for cvpysdk/subclients/sqlsubclient.py"""

import pytest

from cvpysdk.subclients.dbsubclient import DatabaseSubclient
from cvpysdk.subclients.sqlsubclient import SQLServerSubclient


@pytest.mark.unit
class TestSQLServerSubclient:
    """Tests for the SQLServerSubclient class."""

    def test_inherits_database_subclient(self):
        """SQLServerSubclient should inherit from DatabaseSubclient."""
        assert issubclass(SQLServerSubclient, DatabaseSubclient)

    def test_has_key_methods(self):
        """SQLServerSubclient should have expected methods."""
        assert hasattr(SQLServerSubclient, "backup")
        assert hasattr(SQLServerSubclient, "update_content")
        assert hasattr(SQLServerSubclient, "content")
        assert hasattr(SQLServerSubclient, "blocklevel_backup_option")

    def test_content_property_returns_database_names(self):
        """content should return list of database names from mssqlDbContent."""
        sub = object.__new__(SQLServerSubclient)
        sub._is_file_group_subclient = False
        sub._subclient_properties = {
            "content": [
                {"mssqlDbContent": {"databaseName": "master"}},
                {"mssqlDbContent": {"databaseName": "tempdb"}},
            ],
            "mssqlSubClientProp": {},
        }
        result = sub.content
        assert result == ["master", "tempdb"]

    def test_content_property_empty_when_no_content(self):
        """content should return empty list when no content key."""
        sub = object.__new__(SQLServerSubclient)
        sub._is_file_group_subclient = False
        sub._subclient_properties = {"mssqlSubClientProp": {}}
        result = sub.content
        assert result == []
