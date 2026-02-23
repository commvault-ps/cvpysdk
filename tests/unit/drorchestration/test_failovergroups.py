from unittest.mock import patch

import pytest

from cvpysdk.drorchestration.failovergroups import FailoverGroup, FailoverGroups


@pytest.mark.unit
class TestFailoverGroups:
    def test_repr(self, mock_commcell):
        with patch.object(FailoverGroups, "_get_failover_groups", return_value={}):
            groups = FailoverGroups(mock_commcell)
        assert "testcs" in repr(groups)

    def test_has_failover_group_true(self, mock_commcell):
        with patch.object(
            FailoverGroups,
            "_get_failover_groups",
            return_value={"testgroup": {"id": 1}},
        ):
            groups = FailoverGroups(mock_commcell)
        assert groups.has_failover_group("testgroup")

    def test_failover_groups_property(self, mock_commcell):
        sample = {"group1": {"id": 1}}
        with patch.object(FailoverGroups, "_get_failover_groups", return_value=sample):
            groups = FailoverGroups(mock_commcell)
        assert groups.failover_groups == sample

    def test_refresh(self, mock_commcell):
        with patch.object(FailoverGroups, "_get_failover_groups", return_value={}):
            groups = FailoverGroups(mock_commcell)
        with patch.object(
            FailoverGroups,
            "_get_failover_groups",
            return_value={"new": {"id": 2}},
        ):
            groups.refresh()
        assert "new" in groups.failover_groups


@pytest.mark.unit
class TestFailoverGroup:
    def test_class_exists(self):
        assert FailoverGroup is not None

    def test_has_repr(self):
        assert hasattr(FailoverGroup, "__repr__")
