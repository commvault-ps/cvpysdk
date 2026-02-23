import pytest

from cvpysdk.network_topology import NetworkTopologies, NetworkTopology


@pytest.mark.unit
class TestNetworkTopologies:
    def test_class_exists(self):
        assert NetworkTopologies is not None

    def test_has_repr(self):
        assert hasattr(NetworkTopologies, "__repr__")


@pytest.mark.unit
class TestNetworkTopology:
    def test_class_exists(self):
        assert NetworkTopology is not None
