import pytest

from cvpysdk.clients.onedrive_client import OneDriveClient


@pytest.mark.unit
class TestOneDriveClient:
    def test_class_exists(self):
        assert OneDriveClient is not None

    def test_has_repr(self):
        assert hasattr(OneDriveClient, "__repr__")
