"""Unit tests for cvpysdk/subclients/cloudapps/teams_constants.py"""

import pytest

from cvpysdk.subclients.cloudapps.teams_constants import TeamsConstants


@pytest.mark.unit
class TestTeamsConstants:
    """Tests for the TeamsConstants class."""

    def test_add_discover_type_value(self):
        """ADD_DISCOVER_TYPE should be 12."""
        assert TeamsConstants.ADD_DISCOVER_TYPE == 12

    def test_index_app_type_value(self):
        """INDEX_APP_TYPE should be 200128."""
        assert TeamsConstants.INDEX_APP_TYPE == 200128

    def test_add_subclient_entity_json_has_required_keys(self):
        """ADD_SUBCLIENT_ENTITY_JSON should have expected keys."""
        entity = TeamsConstants.ADD_SUBCLIENT_ENTITY_JSON
        assert "instanceId" in entity
        assert "subclientId" in entity
        assert "clientId" in entity
        assert "applicationId" in entity

    def test_add_team_json_has_required_keys(self):
        """ADD_TEAM_JSON should have expected keys."""
        team = TeamsConstants.ADD_TEAM_JSON
        assert "displayName" in team
        assert "smtpAddress" in team
        assert "associated" in team
        assert "msTeamsInfo" in team
        assert "user" in team

    def test_add_request_json_structure(self):
        """ADD_REQUEST_JSON should have proper structure."""
        req = TeamsConstants.ADD_REQUEST_JSON
        assert "LaunchAutoDiscovery" in req
        assert "cloudAppAssociation" in req
        assoc = req["cloudAppAssociation"]
        assert "cloudAppDiscoverinfo" in assoc
        assert "plan" in assoc

    def test_backup_request_json_structure(self):
        """BACKUP_REQUEST_JSON should have proper structure."""
        req = TeamsConstants.BACKUP_REQUEST_JSON
        assert "processinginstructioninfo" in req
        assert "taskInfo" in req
        task_info = req["taskInfo"]
        assert "associations" in task_info
        assert "task" in task_info
        assert "subTasks" in task_info

    def test_cloud_app_ediscover_type_has_teams(self):
        """ClOUD_APP_EDISCOVER_TYPE should have Teams, Users, and Groups."""
        disc = TeamsConstants.ClOUD_APP_EDISCOVER_TYPE
        assert "Teams" in disc
        assert "Users" in disc
        assert "Groups" in disc
        assert disc["Teams"] == 8

    def test_user_onedrive_restore_json_has_task_info(self):
        """USER_ONEDRIVE_RESTORE_JSON should have taskInfo with proper structure."""
        restore = TeamsConstants.USER_ONEDRIVE_RESTORE_JSON
        assert "taskInfo" in restore
        task_info = restore["taskInfo"]
        assert "associations" in task_info
        assert "task" in task_info
        assert "subTasks" in task_info
        assert len(task_info["subTasks"]) > 0
