from unittest.mock import MagicMock

import pytest

from cvpysdk.drorchestration.replicationmonitor import ReplicationMonitor


@pytest.mark.unit
class TestReplicationMonitor:
    def test_class_exists(self):
        assert ReplicationMonitor is not None

    def test_has_key_methods(self):
        assert hasattr(ReplicationMonitor, "testboot")
        assert hasattr(ReplicationMonitor, "planned_failover")
        assert hasattr(ReplicationMonitor, "unplanned_failover")
        assert hasattr(ReplicationMonitor, "failback")
        assert hasattr(ReplicationMonitor, "undo_failover")

    def test_repr(self):
        monitor = MagicMock(spec=ReplicationMonitor)
        monitor.__repr__ = ReplicationMonitor.__repr__
        result = repr(monitor)
        assert isinstance(result, str)
