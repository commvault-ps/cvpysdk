from unittest.mock import patch

import pytest

from cvpysdk.drorchestration.replication_pairs import ReplicationPair, ReplicationPairs


@pytest.mark.unit
class TestReplicationPairs:
    def test_repr(self, mock_commcell):
        with patch.object(ReplicationPairs, "_get_replication_pairs", return_value={}):
            pairs = ReplicationPairs(mock_commcell)
        assert isinstance(repr(pairs), str)

    def test_replication_pairs_property_empty(self, mock_commcell):
        with patch.object(ReplicationPairs, "_get_replication_pairs", return_value={}):
            pairs = ReplicationPairs(mock_commcell)
        assert pairs.replication_pairs == {}

    def test_has_refresh(self, mock_commcell):
        with patch.object(ReplicationPairs, "_get_replication_pairs", return_value={}):
            pairs = ReplicationPairs(mock_commcell)
        assert callable(getattr(pairs, "refresh", None))


@pytest.mark.unit
class TestReplicationPair:
    def test_class_exists(self):
        assert ReplicationPair is not None
