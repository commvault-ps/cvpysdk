"""Unit tests for cvpysdk/instances/mysqlinstance.py"""

import pytest

from cvpysdk.instance import Instance


@pytest.mark.unit
class TestMYSQLInstance:
    """Tests for the MYSQLInstance class."""

    def test_inherits_instance(self):
        """Test that MYSQLInstance is a subclass of Instance."""
        from cvpysdk.instances.mysqlinstance import MYSQLInstance

        assert issubclass(MYSQLInstance, Instance)

    def test_port_property(self):
        """Test port property returns MySQL port."""
        from cvpysdk.instances.mysqlinstance import MYSQLInstance

        inst = object.__new__(MYSQLInstance)
        inst._properties = {"mySqlInstance": {"port": "3306"}}
        assert inst.port == "3306"

    def test_config_file_property(self):
        """Test config_file property returns MySQL config file."""
        from cvpysdk.instances.mysqlinstance import MYSQLInstance

        inst = object.__new__(MYSQLInstance)
        inst._properties = {"mySqlInstance": {"ConfigFile": "/etc/my.cnf"}}
        assert inst.config_file == "/etc/my.cnf"

    def test_version_property(self):
        """Test version property returns MySQL version."""
        from cvpysdk.instances.mysqlinstance import MYSQLInstance

        inst = object.__new__(MYSQLInstance)
        inst._properties = {"mySqlInstance": {"version": "8.0.25"}}
        assert inst.version == "8.0.25"

    def test_binary_directory_property(self):
        """Test binary_directory property."""
        from cvpysdk.instances.mysqlinstance import MYSQLInstance

        inst = object.__new__(MYSQLInstance)
        inst._properties = {"mySqlInstance": {"BinaryDirectory": "/usr/bin"}}
        assert inst.binary_directory == "/usr/bin"

    def test_autodiscovery_enabled_property(self):
        """Test autodiscovery_enabled property."""
        from cvpysdk.instances.mysqlinstance import MYSQLInstance

        inst = object.__new__(MYSQLInstance)
        inst._properties = {"mySqlInstance": {"EnableAutoDiscovery": True}}
        assert inst.autodiscovery_enabled is True

    def test_ssl_enabled_property(self):
        """Test ssl_enabled property."""
        from cvpysdk.instances.mysqlinstance import MYSQLInstance

        inst = object.__new__(MYSQLInstance)
        inst._properties = {"mySqlInstance": {"sslEnabled": True}}
        assert inst.ssl_enabled is True

    def test_restore_in_place_raises_for_non_list(self):
        """Test restore_in_place raises SDKException for non-list path."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.mysqlinstance import MYSQLInstance

        inst = object.__new__(MYSQLInstance)
        with pytest.raises(SDKException):
            inst.restore_in_place(path="not_a_list")

    def test_restore_in_place_raises_for_empty_list(self):
        """Test restore_in_place raises SDKException for empty path."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.mysqlinstance import MYSQLInstance

        inst = object.__new__(MYSQLInstance)
        with pytest.raises(SDKException):
            inst.restore_in_place(path=[])

    def test_restore_out_of_place_raises_for_missing_dest_client(self):
        """Test restore_out_of_place raises SDKException when dest_client_name is None."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.mysqlinstance import MYSQLInstance

        inst = object.__new__(MYSQLInstance)
        with pytest.raises(SDKException):
            inst.restore_out_of_place(
                path=["/db1"], dest_client_name=None, dest_instance_name="inst1"
            )

    def test_no_lock_status_setter_raises_for_non_bool(self):
        """Test no_lock_status setter raises SDKException for non-bool input."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.mysqlinstance import MYSQLInstance

        inst = object.__new__(MYSQLInstance)
        with pytest.raises(SDKException):
            inst.no_lock_status = "not_a_bool"
