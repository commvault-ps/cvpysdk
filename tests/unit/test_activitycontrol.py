from unittest.mock import patch

import pytest

from cvpysdk.activitycontrol import ActivityControl
from cvpysdk.exception import SDKException


@pytest.mark.unit
class TestActivityControl:
    """Tests for the ActivityControl class."""

    def test_repr(self, mock_commcell):
        with patch.object(ActivityControl, "_get_activity_control_status"):
            ac = ActivityControl(mock_commcell)
        assert "ActivityControl" in repr(ac)

    def test_init_sets_activity_types(self, mock_commcell):
        with patch.object(ActivityControl, "_get_activity_control_status"):
            ac = ActivityControl(mock_commcell)
        assert "ALL ACTIVITY" in ac._activity_type_dict
        assert "DATA MANAGEMENT" in ac._activity_type_dict
        assert "DATA RECOVERY" in ac._activity_type_dict
        assert "DATA AGING" in ac._activity_type_dict
        assert "AUX COPY" in ac._activity_type_dict
        assert "SCHEDULER" in ac._activity_type_dict

    def test_activity_type_values(self, mock_commcell):
        with patch.object(ActivityControl, "_get_activity_control_status"):
            ac = ActivityControl(mock_commcell)
        assert ac._activity_type_dict["ALL ACTIVITY"] == 128
        assert ac._activity_type_dict["DATA MANAGEMENT"] == 1
        assert ac._activity_type_dict["DATA RECOVERY"] == 2
        assert ac._activity_type_dict["DATA AGING"] == 16

    def test_request_json_structure(self, mock_commcell):
        with patch.object(ActivityControl, "_get_activity_control_status"):
            ac = ActivityControl(mock_commcell)
        result = ac._request_json_("ALL ACTIVITY", 1000000)
        assert "commCellInfo" in result
        assert "commCellActivityControlInfo" in result["commCellInfo"]
        options = result["commCellInfo"]["commCellActivityControlInfo"]["activityControlOptions"][
            0
        ]
        assert options["activityType"] == 128
        assert options["dateTime"]["time"] == 1000000

    def test_is_enabled_finds_activity(self, mock_commcell):
        with patch.object(ActivityControl, "_get_activity_control_status"):
            ac = ActivityControl(mock_commcell)
        ac._activity_control_properties_list = [
            {
                "activityType": 128,
                "enabled": True,
                "reEnableTime": 0,
                "noSchedEnable": False,
                "reenableTimeZone": "UTC",
            }
        ]
        # Patch _get_activity_control_status so it does not overwrite during is_enabled call
        with patch.object(ActivityControl, "_get_activity_control_status"):
            result = ac.is_enabled("ALL ACTIVITY")
        assert result is True

    def test_is_enabled_not_found_raises(self, mock_commcell):
        with patch.object(ActivityControl, "_get_activity_control_status"):
            ac = ActivityControl(mock_commcell)
        ac._activity_control_properties_list = []
        with patch.object(ActivityControl, "_get_activity_control_status"), pytest.raises(
            SDKException
        ):
            ac.is_enabled("ALL ACTIVITY")

    def test_reenable_time_property(self, mock_commcell):
        with patch.object(ActivityControl, "_get_activity_control_status"):
            ac = ActivityControl(mock_commcell)
        ac._reEnableTime = 1234567
        assert ac.reEnableTime == 1234567

    def test_reenable_timezone_property(self, mock_commcell):
        with patch.object(ActivityControl, "_get_activity_control_status"):
            ac = ActivityControl(mock_commcell)
        ac._reenableTimeZone = "UTC"
        assert ac.reEnableTimeZone == "UTC"
