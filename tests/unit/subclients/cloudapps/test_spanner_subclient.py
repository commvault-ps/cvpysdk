"""Unit tests for cvpysdk/subclients/cloudapps/spanner_subclient.py"""

from unittest.mock import MagicMock

import pytest

from cvpysdk.subclients.casubclient import CloudAppsSubclient
from cvpysdk.subclients.cloudapps.spanner_subclient import GoogleSpannerSubclient


@pytest.mark.unit
class TestGoogleSpannerSubclient:
    """Tests for the GoogleSpannerSubclient class."""

    def test_inherits_cloud_apps_subclient(self):
        """GoogleSpannerSubclient should inherit from CloudAppsSubclient."""
        assert issubclass(GoogleSpannerSubclient, CloudAppsSubclient)

    def test_has_content_property(self):
        """GoogleSpannerSubclient should have content property."""
        assert hasattr(GoogleSpannerSubclient, "content")

    def test_content_property_returns_database_names(self):
        """content property should return list of database names."""
        sub = object.__new__(GoogleSpannerSubclient)
        sub._spanner_content = ["db1", "db2", "db3"]
        result = sub.content
        assert result == ["db1", "db2", "db3"]

    def test_content_setter_calls_set_subclient_properties(self):
        """content setter should call _set_subclient_properties."""
        sub = object.__new__(GoogleSpannerSubclient)
        sub._set_subclient_properties = MagicMock()
        sub.content = ["new_db"]
        sub._set_subclient_properties.assert_called_once()
        call_args = sub._set_subclient_properties.call_args
        assert call_args[0][0] == "_content"
        content_list = call_args[0][1]
        assert len(content_list) == 1
        assert (
            content_list[0]["cloudAppsSubClientProp"]["cloudSpannerSubclient"]["backupObject"][
                "dbName"
            ]
            == "new_db"
        )

    def test_has_get_subclient_properties(self):
        """GoogleSpannerSubclient should have _get_subclient_properties."""
        assert hasattr(GoogleSpannerSubclient, "_get_subclient_properties")
