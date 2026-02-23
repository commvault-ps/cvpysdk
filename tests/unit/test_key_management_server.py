"""Unit tests for cvpysdk.key_management_server module."""

import pytest

from cvpysdk.exception import SDKException
from cvpysdk.key_management_server import (
    KeyManagementServer,
    KeyManagementServers,
)


@pytest.mark.unit
class TestKeyManagementServers:
    """Tests for the KeyManagementServers collection class."""

    def _make_kms_collection(self, mock_commcell, mock_response):
        resp = mock_response(
            json_data={
                "keyProviders": [
                    {
                        "keyProviderType": 3,
                        "provider": {
                            "keyProviderName": "TestKMS",
                            "keyProviderId": 10,
                        },
                    }
                ]
            }
        )
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        return KeyManagementServers(mock_commcell)

    def test_init_populates_kms_dict(self, mock_commcell, mock_response):
        kms = self._make_kms_collection(mock_commcell, mock_response)
        assert "testkms" in kms.get_all_kms()

    def test_repr(self, mock_commcell, mock_response):
        kms = self._make_kms_collection(mock_commcell, mock_response)
        assert repr(kms) == "KeyManagementServers class instance for Commcell"

    def test_has_kms_true(self, mock_commcell, mock_response):
        kms = self._make_kms_collection(mock_commcell, mock_response)
        assert kms.has_kms("TestKMS") is True

    def test_has_kms_false(self, mock_commcell, mock_response):
        kms = self._make_kms_collection(mock_commcell, mock_response)
        assert kms.has_kms("NoKMS") is False

    def test_has_kms_raises_on_non_string(self, mock_commcell, mock_response):
        kms = self._make_kms_collection(mock_commcell, mock_response)
        with pytest.raises(SDKException):
            kms.has_kms(123)

    def test_get_returns_kms_object(self, mock_commcell, mock_response):
        kms = self._make_kms_collection(mock_commcell, mock_response)
        result = kms.get("TestKMS")
        assert isinstance(result, KeyManagementServer)
        assert result.name == "testkms"
        assert result.id == 10

    def test_get_raises_on_missing(self, mock_commcell, mock_response):
        kms = self._make_kms_collection(mock_commcell, mock_response)
        with pytest.raises(SDKException):
            kms.get("nonexistent")

    def test_validate_input_str(self):
        # Should not raise for valid string
        KeyManagementServers._validate_input("hello", str)
        with pytest.raises(SDKException):
            KeyManagementServers._validate_input(123, str)

    def test_validate_input_int(self):
        # Should accept int-convertible values
        KeyManagementServers._validate_input(42, int)
        KeyManagementServers._validate_input("42", int)
        with pytest.raises(SDKException):
            KeyManagementServers._validate_input("abc", int)

    def test_empty_response_returns_empty_dict(self, mock_commcell, mock_response):
        resp = mock_response(json_data={})
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        kms = KeyManagementServers(mock_commcell)
        assert kms.get_all_kms() == {}


@pytest.mark.unit
class TestKeyManagementServer:
    """Tests for the KeyManagementServer entity class."""

    def test_init(self, mock_commcell):
        kms = KeyManagementServer(mock_commcell, "mykms", 5, 3)
        assert kms.name == "mykms"
        assert kms.id == 5
        assert kms.type_id == 3
        assert kms.type_name == "KEY_PROVIDER_AWS_KMS"

    def test_repr(self, mock_commcell):
        kms = KeyManagementServer(mock_commcell, "mykms", 5, 3)
        assert "mykms" in repr(kms)

    def test_get_name_from_type_unknown(self, mock_commcell):
        with pytest.raises(SDKException):
            KeyManagementServer(mock_commcell, "mykms", 5, 999)

    def test_init_validates_name_type(self, mock_commcell):
        with pytest.raises(SDKException):
            KeyManagementServer(mock_commcell, 123, 5, 3)
