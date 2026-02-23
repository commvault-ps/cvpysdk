import pytest

from cvpysdk.clients.vmclient import VMClient


@pytest.mark.unit
class TestVMClient:
    def test_class_exists(self):
        assert VMClient is not None

    def test_has_repr(self):
        assert hasattr(VMClient, "__repr__")
