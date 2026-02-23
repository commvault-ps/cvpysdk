"""Unit tests for cvpysdk/subclients/cloudapps/google_subclient.py"""

import pytest

from cvpysdk.subclients.casubclient import CloudAppsSubclient
from cvpysdk.subclients.cloudapps.google_subclient import GoogleSubclient


@pytest.mark.unit
class TestGoogleSubclient:
    """Tests for the GoogleSubclient class."""

    def test_inherits_cloud_apps_subclient(self):
        """GoogleSubclient should inherit from CloudAppsSubclient."""
        assert issubclass(GoogleSubclient, CloudAppsSubclient)

    def test_has_key_properties(self):
        """GoogleSubclient should have expected properties."""
        assert hasattr(GoogleSubclient, "content")
        assert hasattr(GoogleSubclient, "groups")
        assert hasattr(GoogleSubclient, "get_subclient_users")

    def test_has_key_methods(self):
        """GoogleSubclient should have expected methods."""
        assert hasattr(GoogleSubclient, "restore_out_of_place")
        assert hasattr(GoogleSubclient, "discover")
        assert hasattr(GoogleSubclient, "add_AD_group")
        assert hasattr(GoogleSubclient, "add_user")
        assert hasattr(GoogleSubclient, "add_users")
        assert hasattr(GoogleSubclient, "search_for_user")

    def test_has_restore_methods(self):
        """GoogleSubclient should have various restore methods."""
        assert hasattr(GoogleSubclient, "disk_restore")
        assert hasattr(GoogleSubclient, "out_of_place_restore")
        assert hasattr(GoogleSubclient, "in_place_restore")
        assert hasattr(GoogleSubclient, "process_index_retention_rules")
        assert hasattr(GoogleSubclient, "browse_content")
