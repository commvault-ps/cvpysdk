"""Unit tests for cvpysdk/cvpysdk.py module."""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.cvpysdk import CVPySDK
from cvpysdk.exception import SDKException


@pytest.mark.unit
class TestCVPySDKInit:
    """Tests for CVPySDK constructor."""

    def test_init_stores_commcell_object(self):
        commcell = MagicMock()
        sdk = CVPySDK(commcell)
        assert sdk._commcell_object is commcell

    def test_init_default_verify_ssl(self):
        commcell = MagicMock()
        sdk = CVPySDK(commcell)
        assert sdk._verify_ssl is True

    def test_init_disable_ssl(self):
        commcell = MagicMock()
        with patch("cvpysdk.cvpysdk.urllib3.disable_warnings"):
            sdk = CVPySDK(commcell, verify_ssl=False)
        assert sdk._verify_ssl is False

    def test_init_certificate_path(self):
        commcell = MagicMock()
        sdk = CVPySDK(commcell, certificate_path="/path/to/cert")
        assert sdk._certificate_path == "/path/to/cert"


@pytest.mark.unit
class TestCVPySDKIsValidService:
    """Tests for _is_valid_service method."""

    def test_valid_service_returns_true(self):
        commcell = MagicMock()
        commcell._web_service = "https://example.com/api/"
        sdk = CVPySDK(commcell)

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.ok = True

        with patch.object(sdk, "_request", return_value=mock_resp):
            assert sdk._is_valid_service() is True

    def test_invalid_service_returns_false(self):
        commcell = MagicMock()
        commcell._web_service = "https://example.com/api/"
        sdk = CVPySDK(commcell)

        mock_resp = MagicMock()
        mock_resp.status_code = 404
        mock_resp.ok = False

        with patch.object(sdk, "_request", return_value=mock_resp):
            assert sdk._is_valid_service() is False


@pytest.mark.unit
class TestCVPySDKLogin:
    """Tests for _login method."""

    def test_login_success_returns_token(self):
        commcell = MagicMock()
        commcell._password = "encoded_password"
        commcell.is_service_commcell = False
        commcell._user = "admin"
        commcell.device_id = "test-device"
        commcell._services = {"LOGIN": "https://example.com/api/Login"}

        sdk = CVPySDK(commcell)

        mock_resp = MagicMock()
        mock_resp.json.return_value = {"userName": "admin", "token": "test-token"}

        with patch.object(sdk, "make_request", return_value=(True, mock_resp)):
            token = sdk._login()
        assert token == "test-token"

    def test_login_dict_password_raises(self):
        commcell = MagicMock()
        commcell._password = {"Authtoken": "some-token"}
        commcell.is_service_commcell = False

        sdk = CVPySDK(commcell)

        with pytest.raises(SDKException):
            sdk._login()

    def test_login_failed_response_raises(self):
        commcell = MagicMock()
        commcell._password = "encoded_password"
        commcell.is_service_commcell = False
        commcell._user = "admin"
        commcell.device_id = "test-device"
        commcell._services = {"LOGIN": "https://example.com/api/Login"}
        commcell._update_response_ = MagicMock(return_value="error msg")

        sdk = CVPySDK(commcell)

        mock_resp = MagicMock()
        mock_resp.text = "error"

        with patch.object(sdk, "make_request", return_value=(False, mock_resp)):
            with pytest.raises(SDKException):
                sdk._login()

    def test_login_empty_response_raises(self):
        commcell = MagicMock()
        commcell._password = "encoded_password"
        commcell.is_service_commcell = False
        commcell._user = "admin"
        commcell.device_id = "test-device"
        commcell._services = {"LOGIN": "https://example.com/api/Login"}

        sdk = CVPySDK(commcell)

        mock_resp = MagicMock()
        mock_resp.json.return_value = {}

        with patch.object(sdk, "make_request", return_value=(True, mock_resp)):
            with pytest.raises(SDKException):
                sdk._login()

    def test_login_error_message_raises(self):
        commcell = MagicMock()
        commcell._password = "encoded_password"
        commcell.is_service_commcell = False
        commcell._user = "admin"
        commcell.device_id = "test-device"
        commcell._services = {"LOGIN": "https://example.com/api/Login"}

        sdk = CVPySDK(commcell)

        mock_resp = MagicMock()
        mock_resp.json.return_value = {
            "errList": [{"errLogMessage": "Invalid credentials"}],
            "isAccountLocked": False,
        }

        with patch.object(sdk, "make_request", return_value=(True, mock_resp)):
            with pytest.raises(SDKException):
                sdk._login()


@pytest.mark.unit
class TestCVPySDKMakeRequest:
    """Tests for make_request method."""

    def test_make_request_get(self):
        commcell = MagicMock()
        commcell._headers = {"Authtoken": "fake-token", "Accept": "application/json"}
        sdk = CVPySDK(commcell)

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.ok = True
        mock_resp.json.return_value = {}
        mock_resp.headers = {}

        with patch.object(sdk, "_request", return_value=mock_resp):
            flag, resp = sdk.make_request("GET", "https://example.com/api/test")
        assert flag is True
        assert resp is mock_resp

    def test_make_request_post_with_dict(self):
        commcell = MagicMock()
        commcell._headers = {"Authtoken": "fake-token", "Accept": "application/json"}
        sdk = CVPySDK(commcell)

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.ok = True
        mock_resp.json.return_value = {}
        mock_resp.headers = {}

        with patch.object(sdk, "_request", return_value=mock_resp):
            flag, resp = sdk.make_request("POST", "https://example.com/api/test", {"key": "value"})
        assert flag is True

    def test_make_request_put(self):
        commcell = MagicMock()
        commcell._headers = {"Authtoken": "fake-token", "Accept": "application/json"}
        sdk = CVPySDK(commcell)

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.ok = True
        mock_resp.json.return_value = {}
        mock_resp.headers = {}

        with patch.object(sdk, "_request", return_value=mock_resp):
            flag, resp = sdk.make_request("PUT", "https://example.com/api/test")
        assert flag is True

    def test_make_request_delete(self):
        commcell = MagicMock()
        commcell._headers = {"Authtoken": "fake-token", "Accept": "application/json"}
        sdk = CVPySDK(commcell)

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.ok = True
        mock_resp.json.return_value = {}
        mock_resp.headers = {}

        with patch.object(sdk, "_request", return_value=mock_resp):
            flag, resp = sdk.make_request("DELETE", "https://example.com/api/test")
        assert flag is True

    def test_make_request_unsupported_method_raises(self):
        commcell = MagicMock()
        commcell._headers = {"Authtoken": "fake-token", "Accept": "application/json"}
        sdk = CVPySDK(commcell)

        with pytest.raises(SDKException):
            sdk.make_request("PATCH", "https://example.com/api/test")

    def test_make_request_failure_returns_false(self):
        commcell = MagicMock()
        commcell._headers = {"Authtoken": "fake-token", "Accept": "application/json"}
        sdk = CVPySDK(commcell)

        mock_resp = MagicMock()
        mock_resp.status_code = 500
        mock_resp.ok = False
        mock_resp.json.return_value = {}
        mock_resp.headers = {}

        with patch.object(sdk, "_request", return_value=mock_resp):
            flag, resp = sdk.make_request("GET", "https://example.com/api/test")
        assert flag is False

    def test_make_request_max_attempts_raises(self):
        commcell = MagicMock()
        commcell._headers = {"Authtoken": "fake-token", "Accept": "application/json"}
        sdk = CVPySDK(commcell)

        mock_resp = MagicMock()
        mock_resp.status_code = 401
        mock_resp.ok = False
        mock_resp.json.return_value = {}
        mock_resp.headers = {"Authtoken": "fake-token"}

        with patch.object(sdk, "_request", return_value=mock_resp):
            with pytest.raises(SDKException):
                sdk.make_request("GET", "https://example.com/api/test", attempts=3)


@pytest.mark.unit
class TestCVPySDKLogout:
    """Tests for _logout method."""

    def test_logout_success(self):
        commcell = MagicMock()
        commcell._headers = {"Authtoken": "fake-token"}
        commcell._services = {"LOGOUT": "https://example.com/api/Logout"}
        sdk = CVPySDK(commcell)

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.text = "User logged out"

        with patch.object(sdk, "make_request", return_value=(True, mock_resp)):
            result = sdk._logout()
        assert result == "User logged out"
        assert commcell._headers["Authtoken"] is None

    def test_logout_failure(self):
        commcell = MagicMock()
        commcell._headers = {"Authtoken": "fake-token"}
        commcell._services = {"LOGOUT": "https://example.com/api/Logout"}
        sdk = CVPySDK(commcell)

        with patch.object(sdk, "make_request", return_value=(False, MagicMock())):
            result = sdk._logout()
        assert result == "User already logged out"
