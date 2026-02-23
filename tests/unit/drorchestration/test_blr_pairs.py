import pytest

from cvpysdk.drorchestration.blr_pairs import BLRPair, BLRPairs, BLRTestFailovers


@pytest.mark.unit
class TestBLRPairs:
    def test_class_exists(self):
        assert BLRPairs is not None

    def test_has_repr(self):
        assert hasattr(BLRPairs, "__repr__")

    def test_has_has_blr_pair(self):
        assert callable(getattr(BLRPairs, "has_blr_pair", None))

    def test_blr_pairs_property_defined(self):
        assert hasattr(BLRPairs, "blr_pairs")


@pytest.mark.unit
class TestBLRPair:
    def test_class_exists(self):
        assert BLRPair is not None

    def test_has_repr(self):
        assert hasattr(BLRPair, "__repr__")


@pytest.mark.unit
class TestBLRTestFailovers:
    def test_class_exists(self):
        assert BLRTestFailovers is not None
