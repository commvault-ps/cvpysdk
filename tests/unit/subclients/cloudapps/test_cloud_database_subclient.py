"""Unit tests for cvpysdk/subclients/cloudapps/cloud_database_subclient.py"""

from unittest.mock import MagicMock

import pytest

from cvpysdk.subclients.casubclient import CloudAppsSubclient
from cvpysdk.subclients.cloudapps.cloud_database_subclient import CloudDatabaseSubclient


@pytest.mark.unit
class TestCloudDatabaseSubclient:
    """Tests for the CloudDatabaseSubclient class."""

    def test_inherits_cloud_apps_subclient(self):
        """CloudDatabaseSubclient should inherit from CloudAppsSubclient."""
        assert issubclass(CloudDatabaseSubclient, CloudAppsSubclient)

    def test_has_key_methods(self):
        """CloudDatabaseSubclient should have expected methods."""
        assert hasattr(CloudDatabaseSubclient, "content")
        assert hasattr(CloudDatabaseSubclient, "_set_content")
        assert hasattr(CloudDatabaseSubclient, "browse")
        assert hasattr(CloudDatabaseSubclient, "restore")

    def test_content_property_returns_cloud_db_content(self):
        """content property should return _cloud_db_content dict."""
        sub = object.__new__(CloudDatabaseSubclient)
        sub._cloud_db_content = {"children": [{"name": "db1"}]}
        result = sub.content
        assert result == {"children": [{"name": "db1"}]}

    def test_set_content_updates_cloud_db_content(self):
        """_set_content should update _cloud_db_content with children wrapper."""
        sub = object.__new__(CloudDatabaseSubclient)
        sub._cloud_db_content = {}
        sub._set_subclient_properties = MagicMock()
        content_list = [{"name": "newdb"}]
        sub._set_content(content=content_list)
        assert sub._cloud_db_content == {"children": content_list}
        sub._set_subclient_properties.assert_called_once_with(
            "_cloud_db_content", {"children": content_list}
        )
