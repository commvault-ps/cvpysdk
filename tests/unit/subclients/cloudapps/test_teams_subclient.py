"""Unit tests for cvpysdk/subclients/cloudapps/teams_subclient.py"""

import pytest

from cvpysdk.subclients.casubclient import CloudAppsSubclient
from cvpysdk.subclients.cloudapps.teams_subclient import TeamsSubclient


@pytest.mark.unit
class TestTeamsSubclient:
    """Tests for the TeamsSubclient class."""

    def test_inherits_cloud_apps_subclient(self):
        """TeamsSubclient should inherit from CloudAppsSubclient."""
        assert issubclass(TeamsSubclient, CloudAppsSubclient)

    def test_has_key_methods(self):
        """TeamsSubclient should have expected methods."""
        assert hasattr(TeamsSubclient, "discover")
        assert hasattr(TeamsSubclient, "content")
        assert hasattr(TeamsSubclient, "backup")
        assert hasattr(TeamsSubclient, "out_of_place_restore")
        assert hasattr(TeamsSubclient, "restore_posts_to_html")
        assert hasattr(TeamsSubclient, "get_team")

    def test_has_association_methods(self):
        """TeamsSubclient should have team association methods."""
        assert hasattr(TeamsSubclient, "set_all_users_content")
        assert hasattr(TeamsSubclient, "get_associated_teams")
        assert hasattr(TeamsSubclient, "remove_team_association")
        assert hasattr(TeamsSubclient, "remove_all_users_content")
        assert hasattr(TeamsSubclient, "exclude_teams_from_backup")

    def test_has_restore_methods(self):
        """TeamsSubclient should have various restore methods."""
        assert hasattr(TeamsSubclient, "restore_out_of_place_to_file_location")
        assert hasattr(TeamsSubclient, "restore_files_to_out_of_place")
        assert hasattr(TeamsSubclient, "restore_to_original_location")

    def test_has_stats_and_search_methods(self):
        """TeamsSubclient should have stats and search methods."""
        assert hasattr(TeamsSubclient, "refresh_retention_stats")
        assert hasattr(TeamsSubclient, "refresh_client_level_stats")
        assert hasattr(TeamsSubclient, "do_web_search")
        assert hasattr(TeamsSubclient, "find_teams")

    def test_has_chat_restore_method(self):
        """TeamsSubclient should have run_restore_for_chat_to_onedrive method."""
        assert hasattr(TeamsSubclient, "run_restore_for_chat_to_onedrive")
