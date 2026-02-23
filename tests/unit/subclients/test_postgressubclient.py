"""Unit tests for cvpysdk/subclients/postgressubclient.py"""

import pytest

from cvpysdk.subclients.dbsubclient import DatabaseSubclient
from cvpysdk.subclients.postgressubclient import PostgresSubclient


@pytest.mark.unit
class TestPostgresSubclient:
    """Tests for the PostgresSubclient class."""

    def test_inherits_database_subclient(self):
        """PostgresSubclient should inherit from DatabaseSubclient."""
        assert issubclass(PostgresSubclient, DatabaseSubclient)

    def test_has_key_methods(self):
        """PostgresSubclient should have expected methods."""
        assert hasattr(PostgresSubclient, "set_content")
        assert hasattr(PostgresSubclient, "backup")
        assert hasattr(PostgresSubclient, "restore_postgres_server")
        assert hasattr(PostgresSubclient, "collect_object_list")

    def test_has_content_property(self):
        """PostgresSubclient should have content property."""
        assert hasattr(PostgresSubclient, "content")
