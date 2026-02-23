"""Unit tests for cvpysdk/subclients/cloudapps/onedrive_subclient.py"""

import pytest

from cvpysdk.subclients.casubclient import CloudAppsSubclient
from cvpysdk.subclients.cloudapps.onedrive_subclient import OneDriveSubclient


@pytest.mark.unit
class TestOneDriveSubclient:
    """Tests for the OneDriveSubclient class."""

    def test_inherits_cloud_apps_subclient(self):
        """OneDriveSubclient should inherit from CloudAppsSubclient."""
        assert issubclass(OneDriveSubclient, CloudAppsSubclient)

    def test_has_key_properties(self):
        """OneDriveSubclient should have expected properties."""
        assert hasattr(OneDriveSubclient, "content")
        assert hasattr(OneDriveSubclient, "groups")

    def test_has_key_methods(self):
        """OneDriveSubclient should have expected methods."""
        assert hasattr(OneDriveSubclient, "discover")
        assert hasattr(OneDriveSubclient, "add_user")
        assert hasattr(OneDriveSubclient, "add_AD_group")
        assert hasattr(OneDriveSubclient, "search_for_user")
        assert hasattr(OneDriveSubclient, "restore_out_of_place")

    def test_has_onedrive_specific_methods(self):
        """OneDriveSubclient should have OneDrive-specific restore and backup methods."""
        assert hasattr(OneDriveSubclient, "add_users_onedrive_for_business_client")
        assert hasattr(OneDriveSubclient, "disk_restore_onedrive_for_business_client")
        assert hasattr(OneDriveSubclient, "out_of_place_restore_onedrive_for_business_client")
        assert hasattr(OneDriveSubclient, "in_place_restore_onedrive_for_business_client")
        assert hasattr(
            OneDriveSubclient,
            "run_user_level_backup_onedrive_for_business_client",
        )

    def test_has_custom_category_methods(self):
        """OneDriveSubclient should have custom category management methods."""
        assert hasattr(OneDriveSubclient, "manage_custom_category")
        assert hasattr(
            OneDriveSubclient,
            "update_custom_categories_association_properties",
        )
