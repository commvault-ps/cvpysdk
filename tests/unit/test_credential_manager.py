"""Unit tests for cvpysdk.credential_manager module."""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.credential_manager import Credential, Credentials
from cvpysdk.exception import SDKException


@pytest.mark.unit
class TestCredentials:
    """Tests for the Credentials collection class."""

    def _make_credentials(self, mock_commcell, mock_response):
        resp = mock_response(
            json_data={
                "credentialRecordInfo": [
                    {
                        "credentialRecord": {
                            "credentialId": 1,
                            "credentialName": "TestCred",
                        }
                    },
                    {
                        "credentialRecord": {
                            "credentialId": 2,
                            "credentialName": "OtherCred",
                        }
                    },
                ]
            }
        )
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        return Credentials(mock_commcell)

    def test_init_populates_credentials(self, mock_commcell, mock_response):
        creds = self._make_credentials(mock_commcell, mock_response)
        assert "testcred" in creds.all_credentials
        assert "othercred" in creds.all_credentials

    def test_repr(self, mock_commcell, mock_response):
        creds = self._make_credentials(mock_commcell, mock_response)
        assert repr(creds) == "Credentials class instance for Commcell"

    def test_str_contains_credential_names(self, mock_commcell, mock_response):
        creds = self._make_credentials(mock_commcell, mock_response)
        result = str(creds)
        assert "testcred" in result

    def test_has_credential_returns_true(self, mock_commcell, mock_response):
        creds = self._make_credentials(mock_commcell, mock_response)
        assert creds.has_credential("TestCred") is True

    def test_has_credential_returns_false(self, mock_commcell, mock_response):
        creds = self._make_credentials(mock_commcell, mock_response)
        assert creds.has_credential("nonexistent") is False

    def test_get_returns_credential_object(self, mock_commcell, mock_response):
        creds = self._make_credentials(mock_commcell, mock_response)
        # Patch Credential init to avoid API call
        with patch.object(Credential, "__init__", return_value=None):
            result = creds.get("TestCred")
            assert isinstance(result, Credential)

    def test_get_raises_on_missing(self, mock_commcell, mock_response):
        creds = self._make_credentials(mock_commcell, mock_response)
        with pytest.raises(SDKException):
            creds.get("nonexistent")

    def test_refresh_re_fetches(self, mock_commcell, mock_response):
        creds = self._make_credentials(mock_commcell, mock_response)
        # Simulate new credential on refresh
        resp2 = mock_response(
            json_data={
                "credentialRecordInfo": [
                    {
                        "credentialRecord": {
                            "credentialId": 3,
                            "credentialName": "NewCred",
                        }
                    }
                ]
            }
        )
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp2)
        creds.refresh()
        assert "newcred" in creds.all_credentials
        assert "testcred" not in creds.all_credentials

    def test_get_credentials_api_failure(self, mock_commcell, mock_response):
        resp = mock_response(status_code=500, text="Server Error")
        mock_commcell._cvpysdk_object.make_request.return_value = (False, resp)
        mock_commcell._update_response_ = MagicMock(return_value="Server Error")
        with pytest.raises(SDKException):
            Credentials(mock_commcell)


@pytest.mark.unit
class TestCredential:
    """Tests for the Credential entity class."""

    def test_credential_name(self, mock_commcell):
        with patch.object(Credential, "_get_credential_properties"):
            cred = Credential(mock_commcell, "TestCred", credential_id=42)
        assert cred.credential_name == "testcred"

    def test_credential_id(self, mock_commcell):
        with patch.object(Credential, "_get_credential_properties"):
            cred = Credential(mock_commcell, "TestCred", credential_id=42)
        assert cred.credential_id == 42
