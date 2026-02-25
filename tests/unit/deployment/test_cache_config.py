"""Unit tests for cvpysdk.deployment.cache_config module."""

from unittest.mock import MagicMock

import pytest

from cvpysdk.deployment.cache_config import CommServeCache, RemoteCache
from cvpysdk.exception import SDKException


@pytest.mark.unit
class TestCommServeCache:
    """Tests for CommServeCache class."""

    def _create_cs_cache(self, mock_commcell):
        cache = CommServeCache(mock_commcell)
        return cache

    def test_init(self, mock_commcell):
        cache = self._create_cs_cache(mock_commcell)
        assert cache.commcell_object is mock_commcell
        assert cache.request_xml is not None
        assert "EVGui_SetUpdateAgentInfoReq" in cache.request_xml

    def test_get_request_xml(self):
        xml = CommServeCache.get_request_xml()
        assert "EVGui_SetUpdateAgentInfoReq" in xml
        assert "uaInfo" in xml
        assert "deletePackageCache" in xml

    def test_get_cs_cache_path_success(self, mock_commcell):
        cache = self._create_cs_cache(mock_commcell)
        mock_commcell.get_gxglobalparam_value.return_value = {
            "error": {"errorCode": 0},
            "commserveSoftwareCache": {"storePatchlocation": "/opt/cache"},
        }
        result = cache.get_cs_cache_path()
        assert result == "/opt/cache"

    def test_get_cs_cache_path_error(self, mock_commcell):
        cache = self._create_cs_cache(mock_commcell)
        mock_commcell.get_gxglobalparam_value.return_value = {
            "error": {"errorCode": 1, "errorMessage": "some error"},
        }
        with pytest.raises(SDKException):
            cache.get_cs_cache_path()

    def test_delete_cache_success(self, mock_commcell):
        cache = self._create_cs_cache(mock_commcell)
        mock_commcell.qoperation_execute.return_value = {"errorCode": 0}
        cache.delete_cache()
        mock_commcell.qoperation_execute.assert_called_once()

    def test_delete_cache_failure(self, mock_commcell):
        cache = self._create_cs_cache(mock_commcell)
        mock_commcell.qoperation_execute.return_value = {
            "errorCode": 1,
            "errorMessage": "error",
        }
        with pytest.raises(SDKException):
            cache.delete_cache()

    def test_commit_cache_success(self, mock_commcell):
        cache = self._create_cs_cache(mock_commcell)
        mock_commcell.qoperation_execute.return_value = {"errorCode": 0}
        cache.commit_cache()
        mock_commcell.qoperation_execute.assert_called_once()

    def test_commit_cache_failure(self, mock_commcell):
        cache = self._create_cs_cache(mock_commcell)
        mock_commcell.qoperation_execute.return_value = {
            "errorCode": 1,
            "errorMessage": "error",
        }
        with pytest.raises(SDKException):
            cache.commit_cache()

    def test_get_remote_cache_clients_success(self, mock_commcell, mock_response):
        cache = self._create_cs_cache(mock_commcell)
        xml_text = (
            "<response>"
            '<client clientName="testcs"/>'
            '<client clientName="rc1"/>'
            '<client clientName="rc2"/>'
            "</response>"
        )
        resp = mock_response(text=xml_text)
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        result = cache.get_remote_cache_clients()
        assert "rc1" in result
        assert "rc2" in result
        assert "testcs" not in result

    def test_get_remote_cache_clients_api_failure(self, mock_commcell, mock_response):
        cache = self._create_cs_cache(mock_commcell)
        resp = mock_response(status_code=500)
        mock_commcell._cvpysdk_object.make_request.return_value = (False, resp)
        with pytest.raises(SDKException):
            cache.get_remote_cache_clients()


@pytest.mark.unit
class TestRemoteCache:
    """Tests for RemoteCache class."""

    def _create_remote_cache(self, mock_commcell):
        """Create a RemoteCache object bypassing __init__ to avoid API call."""
        rc = RemoteCache.__new__(RemoteCache)
        rc.commcell = mock_commcell
        client_obj = MagicMock()
        client_obj.client_name = "rc_client"
        client_obj.client_id = "100"
        rc.client_object = client_obj
        rc.request_xml = CommServeCache.get_request_xml()
        rc._cvpysdk_object = mock_commcell._cvpysdk_object
        rc._services = mock_commcell._services
        return rc

    def test_get_remote_cache_path_found(self, mock_commcell):
        rc = self._create_remote_cache(mock_commcell)
        mock_commcell.qoperation_execute.return_value = {
            "uaInfo": [
                {
                    "client": {"clientName": "rc_client"},
                    "uaCachePath": "/opt/remote_cache",
                },
                {
                    "client": {"clientName": "other_client"},
                    "uaCachePath": "/opt/other_cache",
                },
            ]
        }
        result = rc.get_remote_cache_path()
        assert result == "/opt/remote_cache"

    def test_get_remote_cache_path_not_found(self, mock_commcell):
        rc = self._create_remote_cache(mock_commcell)
        mock_commcell.qoperation_execute.return_value = {
            "uaInfo": [
                {
                    "client": {"clientName": "other_client"},
                    "uaCachePath": "/opt/other_cache",
                }
            ]
        }
        result = rc.get_remote_cache_path()
        assert result is None

    def test_get_remote_cache_path_empty_response(self, mock_commcell):
        rc = self._create_remote_cache(mock_commcell)
        mock_commcell.qoperation_execute.return_value = {}
        with pytest.raises(SDKException):
            rc.get_remote_cache_path()

    def test_delete_remote_cache_contents_success(self, mock_commcell):
        rc = self._create_remote_cache(mock_commcell)
        mock_commcell.qoperation_execute.return_value = {"errorCode": 0}
        rc.delete_remote_cache_contents()
        mock_commcell.qoperation_execute.assert_called_once()

    def test_delete_remote_cache_contents_failure(self, mock_commcell):
        rc = self._create_remote_cache(mock_commcell)
        mock_commcell.qoperation_execute.return_value = {
            "errorCode": 1,
            "errorMessage": "failed",
        }
        with pytest.raises(SDKException):
            rc.delete_remote_cache_contents()

    def test_assoc_entity_no_inputs(self, mock_commcell):
        rc = self._create_remote_cache(mock_commcell)
        with pytest.raises(Exception, match="No clients or client groups"):
            rc.assoc_entity_to_remote_cache()

    def test_configure_packages_to_sync_resolves_enum_values(self, mock_commcell):
        rc = self._create_remote_cache(mock_commcell)
        mock_commcell._qoperation_execscript.return_value = {}

        rc.configure_packages_to_sync(
            win_os=["WINDOWS_64"],
            win_package_list=["FILE_SYSTEM", "MEDIA_AGENT"],
            unix_os=["UNIX_LINUX64"],
            unix_package_list=["FILE_SYSTEM"],
        )

        qscript = mock_commcell._qoperation_execscript.call_args[0][0]
        assert "-si 3 -si 702,51" in qscript
        assert "-si 16 -si 1101" in qscript

    def test_configure_packages_to_sync_rejects_invalid_enum_name(self, mock_commcell):
        rc = self._create_remote_cache(mock_commcell)
        mock_commcell._qoperation_execscript.return_value = {}

        with pytest.raises(SDKException, match="Incorrect input for win_os"):
            rc.configure_packages_to_sync(
                win_os=["WINDOWS_64", "NOT_A_REAL_OS"],
                win_package_list=["FILE_SYSTEM"],
            )
