"""Unit tests for cvpysdk/instances/sqlinstance.py"""

from unittest.mock import MagicMock

import pytest

from cvpysdk.instance import Instance


@pytest.mark.unit
class TestSQLServerInstance:
    """Tests for the SQLServerInstance class."""

    def test_inherits_instance(self):
        """Test that SQLServerInstance is a subclass of Instance."""
        from cvpysdk.instances.sqlinstance import SQLServerInstance

        assert issubclass(SQLServerInstance, Instance)

    def test_has_key_methods(self):
        """Test that SQLServerInstance has key methods."""
        from cvpysdk.instances.sqlinstance import SQLServerInstance

        assert callable(getattr(SQLServerInstance, "restore", None))
        assert callable(getattr(SQLServerInstance, "browse", None))
        assert callable(getattr(SQLServerInstance, "backup", None))
        assert callable(getattr(SQLServerInstance, "browse_in_time", None))
        assert callable(getattr(SQLServerInstance, "restore_to_destination_server", None))

    def test_restore_raises_for_non_list(self):
        """Test restore raises SDKException for non-list content_to_restore."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.sqlinstance import SQLServerInstance

        inst = object.__new__(SQLServerInstance)
        with pytest.raises(SDKException):
            inst.restore(content_to_restore="not_a_list")

    def test_restore_to_destination_server_raises_for_non_list(self):
        """Test restore_to_destination_server raises SDKException for non-list."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.sqlinstance import SQLServerInstance

        inst = object.__new__(SQLServerInstance)
        with pytest.raises(SDKException):
            inst.restore_to_destination_server(
                content_to_restore="not_a_list",
                destination_server="server1",
            )

    def test_vss_option_calls_set_instance_properties(self):
        """Test vss_option passes correct JSON to _set_instance_properties."""
        from cvpysdk.instances.sqlinstance import SQLServerInstance

        inst = object.__new__(SQLServerInstance)
        inst._set_instance_properties = MagicMock()
        inst.vss_option(True)
        inst._set_instance_properties.assert_called_once_with(
            "_mssql_instance_prop", {"useVss": True}
        )

    def test_vdi_timeout_calls_set_instance_properties(self):
        """Test vdi_timeout passes correct JSON to _set_instance_properties."""
        from cvpysdk.instances.sqlinstance import SQLServerInstance

        inst = object.__new__(SQLServerInstance)
        inst._set_instance_properties = MagicMock()
        inst.vdi_timeout(300)
        inst._set_instance_properties.assert_called_once_with(
            "_mssql_instance_prop", {"vDITimeOut": 300}
        )

    def test_impersonation_local_system(self):
        """Test impersonation with local system account (no credentials)."""
        from cvpysdk.instances.sqlinstance import SQLServerInstance

        inst = object.__new__(SQLServerInstance)
        inst._set_instance_properties = MagicMock()
        inst.impersonation(True)
        args = inst._set_instance_properties.call_args[0]
        assert args[0] == "_mssql_instance_prop"
        assert args[1]["overrideHigherLevelSettings"]["useLocalSystemAccount"] is True

    def test_impersonation_with_credentials(self):
        """Test impersonation with provided credentials."""
        from cvpysdk.instances.sqlinstance import SQLServerInstance

        inst = object.__new__(SQLServerInstance)
        inst._set_instance_properties = MagicMock()
        inst.impersonation(True, credentials="my_cred")
        args = inst._set_instance_properties.call_args[0]
        assert args[1]["MSSQLCredentialinfo"]["credentialName"] == "my_cred"
        assert args[1]["overrideHigherLevelSettings"]["useLocalSystemAccount"] is False

    def test_impersonation_disabled(self):
        """Test impersonation when disabled."""
        from cvpysdk.instances.sqlinstance import SQLServerInstance

        inst = object.__new__(SQLServerInstance)
        inst._set_instance_properties = MagicMock()
        inst.impersonation(False)
        args = inst._set_instance_properties.call_args[0]
        assert args[1]["overrideHigherLevelSettings"]["useLocalSystemAccount"] is False
        assert "MSSQLCredentialinfo" not in args[1]

    def test_create_recovery_point_raises_for_non_string(self):
        """Test create_recovery_point raises SDKException for non-string database_name."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.sqlinstance import SQLServerInstance

        inst = object.__new__(SQLServerInstance)
        with pytest.raises(SDKException):
            inst.create_recovery_point(database_name=123)

    def test_process_restore_response_raises_for_error(self):
        """Test _process_restore_response raises SDKException on error response."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.sqlinstance import SQLServerInstance

        inst = object.__new__(SQLServerInstance)
        inst._commcell_object = MagicMock()
        mock_resp = MagicMock()
        mock_resp.json.return_value = {
            "errorCode": 1,
            "errorMessage": "restore failed",
        }
        inst._commcell_object._cvpysdk_object.make_request.return_value = (
            True,
            mock_resp,
        )
        with pytest.raises(SDKException):
            inst._process_restore_response({"taskInfo": {}})

    def test_process_restore_response_raises_for_empty_response(self):
        """Test _process_restore_response raises SDKException when response is empty."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.sqlinstance import SQLServerInstance

        inst = object.__new__(SQLServerInstance)
        inst._commcell_object = MagicMock()
        mock_resp = MagicMock()
        mock_resp.json.return_value = {}
        inst._commcell_object._cvpysdk_object.make_request.return_value = (
            True,
            mock_resp,
        )
        with pytest.raises(SDKException):
            inst._process_restore_response({"taskInfo": {}})
