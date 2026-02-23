"""Unit tests for cvpysdk/instances/cloudapps/teams_instance.py"""

from unittest.mock import MagicMock

import pytest

from cvpysdk.instances.cainstance import CloudAppsInstance


@pytest.mark.unit
class TestTeamsInstance:
    """Tests for the TeamsInstance class."""

    def test_inherits_cloud_apps_instance(self):
        """Test that TeamsInstance is a subclass of CloudAppsInstance."""
        from cvpysdk.instances.cloudapps.teams_instance import TeamsInstance

        assert issubclass(TeamsInstance, CloudAppsInstance)

    def test_get_instance_properties_json(self):
        """Test _get_instance_properties_json returns correct format."""
        from cvpysdk.instances.cloudapps.teams_instance import TeamsInstance

        inst = object.__new__(TeamsInstance)
        inst._properties = {"key": "value", "cloudAppsInstance": {"instanceType": 12}}
        result = inst._get_instance_properties_json()
        assert result == {"instanceProperties": inst._properties}

    def test_cloud_apps_restore_json_structure(self):
        """Test _cloud_apps_restore_json returns correct structure."""
        from cvpysdk.instances.cloudapps.teams_instance import TeamsInstance

        inst = object.__new__(TeamsInstance)
        inst._properties = {"cloudAppsInstance": {"instanceType": 12}}
        inst._restore_association = {"subclientId": 100}

        source_team = {
            "displayName": "SourceTeam",
            "user": {"userGUID": "GUID-SRC-123"},
        }
        dest_team = {
            "displayName": "DestTeam",
            "user": {"userGUID": "GUID-DST-456"},
        }
        result = inst._cloud_apps_restore_json(source_team, dest_team)
        assert result["instanceType"] == 12
        opts = result["msTeamsRestoreOptions"]
        assert opts["destLocation"] == "DestTeam"
        assert opts["restoreToTeams"] is True
        assert opts["destinationTeamInfo"]["teamName"] == "DestTeam"
        assert opts["destinationTeamInfo"]["teamId"] == "guid-dst-456"

    def test_cloud_apps_restore_json_selected_items(self):
        """Test _cloud_apps_restore_json includes correct selected items."""
        from cvpysdk.instances.cloudapps.teams_instance import TeamsInstance

        inst = object.__new__(TeamsInstance)
        inst._properties = {"cloudAppsInstance": {"instanceType": 12}}
        inst._restore_association = {"subclientId": 100}

        source_team = {
            "displayName": "SourceTeam",
            "user": {"userGUID": "GUID-SRC-123"},
        }
        dest_team = {
            "displayName": "DestTeam",
            "user": {"userGUID": "GUID-DST-456"},
        }
        result = inst._cloud_apps_restore_json(source_team, dest_team)
        selected = result["msTeamsRestoreOptions"]["selectedItemsToRestsore"][0]
        assert selected["itemId"] == "guid-src-123"
        assert selected["itemType"] == 1
        assert selected["isDirectory"] is True

    def test_update_instance_raises_on_error(self):
        """Test update_instance raises SDKException on error response."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.cloudapps.teams_instance import TeamsInstance

        inst = object.__new__(TeamsInstance)
        inst._services = {"INSTANCE_PROPERTIES": "http://example.com/inst/%s"}
        inst._instance_id = 1

        mock_resp = MagicMock()
        mock_resp.json.return_value = {
            "errorCode": 1,
            "errorMessage": "Update failed",
        }
        inst._cvpysdk_object = MagicMock()
        inst._cvpysdk_object.make_request.return_value = (True, mock_resp)

        with pytest.raises(SDKException):
            inst.update_instance({"prop": "val"})
