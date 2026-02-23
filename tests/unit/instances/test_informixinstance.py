"""Unit tests for cvpysdk/instances/informixinstance.py"""

import pytest

from cvpysdk.instance import Instance


@pytest.mark.unit
class TestInformixInstance:
    """Tests for the InformixInstance class."""

    def test_inherits_instance(self):
        """Test that InformixInstance is a subclass of Instance."""
        from cvpysdk.instances.informixinstance import InformixInstance

        assert issubclass(InformixInstance, Instance)

    def test_informix_directory_property(self):
        """Test informix_directory property."""
        from cvpysdk.instances.informixinstance import InformixInstance

        inst = object.__new__(InformixInstance)
        inst._properties = {"informixInstance": {"informixDir": "/opt/informix"}}
        assert inst.informix_directory == "/opt/informix"

    def test_informix_user_property(self):
        """Test informix_user property."""
        from cvpysdk.instances.informixinstance import InformixInstance

        inst = object.__new__(InformixInstance)
        inst._properties = {"informixInstance": {"informixUser": {"userName": "informix"}}}
        assert inst.informix_user == "informix"

    def test_on_config_file_property(self):
        """Test on_config_file property."""
        from cvpysdk.instances.informixinstance import InformixInstance

        inst = object.__new__(InformixInstance)
        inst._properties = {"informixInstance": {"onConfigFile": "onconfig.testdb"}}
        assert inst.on_config_file == "onconfig.testdb"

    def test_sql_host_file_property(self):
        """Test sql_host_file property."""
        from cvpysdk.instances.informixinstance import InformixInstance

        inst = object.__new__(InformixInstance)
        inst._properties = {"informixInstance": {"sqlHostfile": "/etc/hosts.equiv"}}
        assert inst.sql_host_file == "/etc/hosts.equiv"

    def test_restore_in_place_raises_for_non_list(self):
        """Test restore_in_place raises SDKException if path is not a list."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.informixinstance import InformixInstance

        inst = object.__new__(InformixInstance)
        with pytest.raises(SDKException):
            inst.restore_in_place("not_a_list")

    def test_restore_in_place_raises_for_empty_list(self):
        """Test restore_in_place raises SDKException for empty path list."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.informixinstance import InformixInstance

        inst = object.__new__(InformixInstance)
        with pytest.raises(SDKException):
            inst.restore_in_place([])

    def test_restore_out_of_place_raises_for_non_list(self):
        """Test restore_out_of_place raises SDKException if path is not a list."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.informixinstance import InformixInstance

        inst = object.__new__(InformixInstance)
        with pytest.raises(SDKException):
            inst.restore_out_of_place("not_a_list", "client", "instance")

    def test_restore_informix_option_json_raises_for_non_dict(self):
        """Test _restore_informix_option_json raises SDKException for non-dict."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.informixinstance import InformixInstance

        inst = object.__new__(InformixInstance)
        with pytest.raises(SDKException):
            inst._restore_informix_option_json("not_a_dict")
