from unittest.mock import patch

import pytest

from cvpysdk.exception import SDKException
from cvpysdk.policies.schedule_policies import (
    OperationType,
    SchedulePolicies,
    SchedulePolicy,
)


@pytest.mark.unit
class TestOperationType:
    """Tests for the OperationType constants."""

    def test_include(self):
        assert OperationType.INCLUDE == "include"

    def test_delete(self):
        assert OperationType.DELETE == "deleted"


@pytest.mark.unit
class TestSchedulePolicies:
    """Tests for the SchedulePolicies collection class."""

    def _make_policies(self, mock_commcell, policies=None):
        with patch.object(SchedulePolicies, "_get_policies", return_value=policies or {}):
            return SchedulePolicies(mock_commcell)

    def test_repr(self, mock_commcell):
        sp = self._make_policies(mock_commcell)
        assert "SchedulePolicies" in repr(sp)

    def test_str(self, mock_commcell):
        sp = self._make_policies(mock_commcell, policies={"pol1": "1"})
        result = str(sp)
        assert "pol1" in result

    def test_all_schedule_policies_property(self, mock_commcell):
        policies = {"pol1": "1", "pol2": "2"}
        sp = self._make_policies(mock_commcell, policies=policies)
        assert sp.all_schedule_policies == policies

    def test_has_policy_true(self, mock_commcell):
        sp = self._make_policies(mock_commcell, policies={"testpol": "1"})
        assert sp.has_policy("testpol") is True

    def test_has_policy_case_insensitive(self, mock_commcell):
        sp = self._make_policies(mock_commcell, policies={"testpol": "1"})
        assert sp.has_policy("TestPol") is True

    def test_has_policy_non_string_raises(self, mock_commcell):
        sp = self._make_policies(mock_commcell)
        with pytest.raises(SDKException):
            sp.has_policy(123)

    def test_get_non_string_raises(self, mock_commcell):
        sp = self._make_policies(mock_commcell)
        with pytest.raises(SDKException):
            sp.get(123)

    def test_get_nonexistent_raises(self, mock_commcell):
        sp = self._make_policies(mock_commcell)
        with pytest.raises(SDKException):
            sp.get("nonexistent")

    def test_get_returns_schedule_policy(self, mock_commcell):
        sp = self._make_policies(mock_commcell, policies={"testpol": "1"})
        with patch.object(SchedulePolicy, "__init__", return_value=None):
            result = sp.get("testpol")
        assert isinstance(result, SchedulePolicy)

    def test_delete_non_string_raises(self, mock_commcell):
        sp = self._make_policies(mock_commcell)
        with pytest.raises(SDKException):
            sp.delete(123)

    def test_delete_nonexistent_raises(self, mock_commcell):
        sp = self._make_policies(mock_commcell)
        with pytest.raises(SDKException):
            sp.delete("nonexistent")

    def test_add_non_list_schedules_raises(self, mock_commcell):
        sp = self._make_policies(mock_commcell)
        with pytest.raises(SDKException):
            sp.add("test", "Data Protection", [], "not_a_list")

    def test_refresh_calls_get_policies(self, mock_commcell):
        with patch.object(SchedulePolicies, "_get_policies", return_value={}) as mock_get:
            sp = SchedulePolicies(mock_commcell)
            sp.refresh()
        assert mock_get.call_count == 2

    def test_subtasks_json_data_protection(self):
        result = SchedulePolicies.subtasks_json("Data Protection")
        assert result["subTaskType"] == 2
        assert result["operationType"] == 2

    def test_subtasks_json_auxiliary_copy(self):
        result = SchedulePolicies.subtasks_json("Auxiliary Copy")
        assert result["subTaskType"] == 1
        assert result["operationType"] == 4003

    def test_policy_types_mapping(self):
        assert SchedulePolicies.policy_types["Data Protection"] == 0
        assert SchedulePolicies.policy_types["Auxiliary Copy"] == 1


@pytest.mark.unit
class TestSchedulePolicy:
    """Tests for the SchedulePolicy entity class."""

    def test_get_schedule_no_args_raises(self, mock_commcell):
        with patch.object(SchedulePolicy, "_get_schedule_policy_properties"):
            sp = SchedulePolicy(mock_commcell, "test_pol", "1")
        with pytest.raises(SDKException):
            sp.get_schedule()

    def test_get_schedule_non_string_name_raises(self, mock_commcell):
        with patch.object(SchedulePolicy, "_get_schedule_policy_properties"):
            sp = SchedulePolicy(mock_commcell, "test_pol", "1")
        with pytest.raises(SDKException):
            sp.get_schedule(schedule_name=123)

    def test_get_schedule_non_int_id_raises(self, mock_commcell):
        with patch.object(SchedulePolicy, "_get_schedule_policy_properties"):
            sp = SchedulePolicy(mock_commcell, "test_pol", "1")
        with pytest.raises(SDKException):
            sp.get_schedule(schedule_id="abc")

    def test_get_option_found(self):
        option_dict = {"level1": {"level2": {"target": "value"}}}
        result = SchedulePolicy.get_option(option_dict, "target")
        assert result == "value"

    def test_get_option_not_found(self):
        option_dict = {"level1": {"level2": {"other": "value"}}}
        result = SchedulePolicy.get_option(option_dict, "target")
        assert result is None

    def test_get_option_direct_key(self):
        option_dict = {"target": "value"}
        result = SchedulePolicy.get_option(option_dict, "target")
        assert result == "value"

    def test_get_option_non_dict(self):
        result = SchedulePolicy.get_option("not_a_dict", "target")
        assert result is None

    def test_all_schedules_property(self, mock_commcell):
        with patch.object(SchedulePolicy, "_get_schedule_policy_properties"):
            sp = SchedulePolicy(mock_commcell, "test_pol", "1")
        assert sp.all_schedules == []
