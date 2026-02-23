"""Unit tests for cvpysdk/instances/virtualserver/null.py"""

import pytest

from cvpysdk.instances.vsinstance import VirtualServerInstance


@pytest.mark.unit
class TestNullSubclient:
    """Tests for the NullSubclient class."""

    def test_inherits_virtual_server_instance(self):
        """Test that NullSubclient is a subclass of VirtualServerInstance."""
        from cvpysdk.instances.virtualserver.null import NullSubclient

        assert issubclass(NullSubclient, VirtualServerInstance)

    def test_init_raises_sdk_exception(self):
        """Test that NullSubclient.__init__ raises SDKException."""
        from unittest.mock import MagicMock

        from cvpysdk.exception import SDKException
        from cvpysdk.instances.virtualserver.null import NullSubclient

        inst = object.__new__(NullSubclient)
        with pytest.raises(SDKException, match="not yet supported"):
            inst.__init__(MagicMock(), "unsupported_instance", None)

    def test_init_includes_instance_name_in_error(self):
        """Test that the SDKException message includes the instance name."""
        from unittest.mock import MagicMock

        from cvpysdk.exception import SDKException
        from cvpysdk.instances.virtualserver.null import NullSubclient

        inst = object.__new__(NullSubclient)
        with pytest.raises(SDKException, match="my_instance"):
            inst.__init__(MagicMock(), "my_instance", None)
