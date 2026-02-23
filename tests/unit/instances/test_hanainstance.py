"""Unit tests for cvpysdk/instances/hanainstance.py"""

import pytest

from cvpysdk.instance import Instance


@pytest.mark.unit
class TestSAPHANAInstance:
    """Tests for the SAPHANAInstance class."""

    def test_inherits_instance(self):
        """Test that SAPHANAInstance is a subclass of Instance."""
        from cvpysdk.instances.hanainstance import SAPHANAInstance

        assert issubclass(SAPHANAInstance, Instance)

    def test_sps_version_property(self):
        """Test sps_version returns the correct version."""
        from cvpysdk.instances.hanainstance import SAPHANAInstance

        inst = object.__new__(SAPHANAInstance)
        inst._properties = {"saphanaInstance": {"spsVersion": "SPS04"}}
        assert inst.sps_version == "SPS04"

    def test_instance_number_property(self):
        """Test instance_number returns the correct instance number."""
        from cvpysdk.instances.hanainstance import SAPHANAInstance

        inst = object.__new__(SAPHANAInstance)
        inst._properties = {"saphanaInstance": {"dbInstanceNumber": "00"}}
        assert inst.instance_number == "00"

    def test_sql_location_directory(self):
        """Test sql_location_directory property."""
        from cvpysdk.instances.hanainstance import SAPHANAInstance

        inst = object.__new__(SAPHANAInstance)
        inst._properties = {"saphanaInstance": {"hdbsqlLocationDirectory": "/usr/sap/hdbsql"}}
        assert inst.sql_location_directory == "/usr/sap/hdbsql"

    def test_instance_db_username(self):
        """Test instance_db_username property."""
        from cvpysdk.instances.hanainstance import SAPHANAInstance

        inst = object.__new__(SAPHANAInstance)
        inst._properties = {"saphanaInstance": {"dbUser": {"userName": "SYSTEM"}}}
        assert inst.instance_db_username == "SYSTEM"

    def test_hdb_user_storekey(self):
        """Test hdb_user_storekey property."""
        from cvpysdk.instances.hanainstance import SAPHANAInstance

        inst = object.__new__(SAPHANAInstance)
        inst._properties = {"saphanaInstance": {"hdbuserstorekey": "mykey"}}
        assert inst.hdb_user_storekey == "mykey"

    def test_restore_raises_for_non_string_instance(self):
        """Test restore raises SDKException when instance is not string or Instance."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.hanainstance import SAPHANAInstance

        inst = object.__new__(SAPHANAInstance)

        with pytest.raises(SDKException):
            inst.restore("client", 12345)
