import pytest

from cvpysdk.activateapps.ediscovery_utils import (
    EdiscoveryClientOperations,
    EdiscoveryClients,
    EdiscoveryDataSources,
)


@pytest.mark.unit
class TestEdiscoveryClients:
    def test_class_exists(self):
        assert EdiscoveryClients is not None

    def test_has_repr(self):
        assert hasattr(EdiscoveryClients, "__repr__")


@pytest.mark.unit
class TestEdiscoveryClientOperations:
    def test_class_exists(self):
        assert EdiscoveryClientOperations is not None


@pytest.mark.unit
class TestEdiscoveryDataSources:
    def test_class_exists(self):
        assert EdiscoveryDataSources is not None
