"""Unit tests for cvpysdk/plan.py module."""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.exception import SDKException
from cvpysdk.plan import Plan, Plans, PlanTypes


@pytest.mark.unit
class TestPlanTypes:
    """Tests for PlanTypes enum."""

    def test_any_value(self):
        assert PlanTypes.Any.value == 0

    def test_msp_value(self):
        assert PlanTypes.MSP.value == 2

    def test_dc_value(self):
        assert PlanTypes.DC.value == 7


@pytest.mark.unit
class TestPlansInit:
    """Tests for the Plans collection class."""

    def test_repr(self, mock_commcell):
        with patch.object(Plans, "_get_plans", return_value={}):
            plans = Plans(mock_commcell)
        assert "Plans" in repr(plans)

    def test_all_plans_property(self, mock_commcell):
        data = {"test-plan": "1"}
        with patch.object(Plans, "_get_plans", return_value=data):
            plans = Plans(mock_commcell)
        assert plans.all_plans == data

    def test_len(self, mock_commcell):
        data = {"plan1": "1", "plan2": "2"}
        with patch.object(Plans, "_get_plans", return_value=data):
            plans = Plans(mock_commcell)
        assert len(plans) == 2

    def test_len_empty(self, mock_commcell):
        with patch.object(Plans, "_get_plans", return_value={}):
            plans = Plans(mock_commcell)
        assert len(plans) == 0


@pytest.mark.unit
class TestPlansHasPlan:
    """Tests for Plans.has_plan."""

    def test_has_plan_true(self, mock_commcell):
        data = {"test-plan": "1"}
        with patch.object(Plans, "_get_plans", return_value=data):
            plans = Plans(mock_commcell)
        assert plans.has_plan("test-plan") is True

    def test_has_plan_false(self, mock_commcell):
        with patch.object(Plans, "_get_plans", return_value={}):
            plans = Plans(mock_commcell)
        assert not plans.has_plan("nonexistent")

    def test_has_plan_bad_type_raises(self, mock_commcell):
        with patch.object(Plans, "_get_plans", return_value={}):
            plans = Plans(mock_commcell)
        with pytest.raises(SDKException):
            plans.has_plan(123)

    def test_has_plan_case_insensitive(self, mock_commcell):
        data = {"test-plan": "1"}
        with patch.object(Plans, "_get_plans", return_value=data):
            plans = Plans(mock_commcell)
        assert plans.has_plan("Test-Plan") is True


@pytest.mark.unit
class TestPlansGetItem:
    """Tests for Plans.__getitem__."""

    def test_getitem_by_name(self, mock_commcell):
        data = {"test-plan": "1"}
        with patch.object(Plans, "_get_plans", return_value=data):
            plans = Plans(mock_commcell)
        assert plans["test-plan"] == "1"

    def test_getitem_by_id(self, mock_commcell):
        data = {"test-plan": {"id": "1", "name": "test-plan"}}
        with patch.object(Plans, "_get_plans", return_value=data):
            plans = Plans(mock_commcell)
        assert plans["1"] == "test-plan"

    def test_getitem_not_found(self, mock_commcell):
        with patch.object(Plans, "_get_plans", return_value={}):
            plans = Plans(mock_commcell)
        with pytest.raises(IndexError):
            plans["nonexistent"]


@pytest.mark.unit
class TestPlansRefresh:
    """Tests for Plans.refresh."""

    def test_refresh_reloads(self, mock_commcell):
        with patch.object(Plans, "_get_plans", return_value={}) as mock_get:
            plans = Plans(mock_commcell)
            plans.refresh()
            assert mock_get.call_count == 2  # once in init, once in refresh


@pytest.mark.unit
class TestPlanRepr:
    """Tests for Plan __repr__."""

    def test_repr_contains_plan_name(self):
        with patch.object(Plan, "__init__", lambda self, *a, **kw: None):
            plan = Plan.__new__(Plan)
            plan._plan_name = "TestPlan"
            plan._commcell_object = MagicMock()
            plan._commcell_object.commserv_name = "testcs"
            result = repr(plan)
            assert "TestPlan" in result


@pytest.mark.unit
class TestPlanProperties:
    """Tests for Plan property getters."""

    def test_plan_id(self):
        with patch.object(Plan, "__init__", lambda self, *a, **kw: None):
            plan = Plan.__new__(Plan)
            plan._plan_id = "42"
            assert plan.plan_id == "42"

    def test_plan_name(self):
        with patch.object(Plan, "__init__", lambda self, *a, **kw: None):
            plan = Plan.__new__(Plan)
            plan._plan_name = "MyPlan"
            assert plan.plan_name == "MyPlan"
