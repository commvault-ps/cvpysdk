import pytest

from cvpysdk.network import Network


@pytest.mark.unit
class TestNetwork:
    def test_class_exists(self):
        assert Network is not None

    def test_has_repr(self):
        assert hasattr(Network, "__repr__")
