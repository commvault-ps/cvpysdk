import pytest

from cvpysdk.client import Client, Clients


@pytest.mark.unit
class TestClients:
    def test_class_exists(self):
        assert Clients is not None

    def test_has_repr(self):
        assert hasattr(Clients, "__repr__")

    def test_has_has_client(self):
        assert callable(getattr(Clients, "has_client", None))


@pytest.mark.unit
class TestClient:
    def test_class_exists(self):
        assert Client is not None

    def test_has_repr(self):
        assert hasattr(Client, "__repr__")
