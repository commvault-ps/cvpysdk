from unittest.mock import patch

import pytest

from cvpysdk.drorchestration.replication_groups import (
    ReplicationGroup,
    ReplicationGroups,
)


@pytest.mark.unit
class TestReplicationGroups:
    def test_repr(self, mock_commcell):
        with patch.object(ReplicationGroups, "_get_replication_groups", return_value={}):
            groups = ReplicationGroups(mock_commcell)
        assert "testcs" in repr(groups)

    def test_has_replication_group_true(self, mock_commcell):
        with patch.object(
            ReplicationGroups,
            "_get_replication_groups",
            return_value={"testgroup": {"id": 1}},
        ):
            groups = ReplicationGroups(mock_commcell)
        assert groups.has_replication_group("testgroup")

    def test_replication_groups_property(self, mock_commcell):
        sample = {"group1": {"id": 1}}
        with patch.object(ReplicationGroups, "_get_replication_groups", return_value=sample):
            groups = ReplicationGroups(mock_commcell)
        assert groups.replication_groups == sample

    def test_refresh(self, mock_commcell):
        with patch.object(ReplicationGroups, "_get_replication_groups", return_value={}):
            groups = ReplicationGroups(mock_commcell)
        with patch.object(
            ReplicationGroups,
            "_get_replication_groups",
            return_value={"new": {"id": 2}},
        ):
            groups.refresh()
        assert "new" in groups.replication_groups


@pytest.mark.unit
class TestReplicationGroup:
    def test_class_exists(self):
        assert ReplicationGroup is not None
