"""Unit tests for cvpysdk certificate handling.

Note: cvpysdk does not have a separate certificate.py module.
The certificate handling is done within the CVPySDK class in cvpysdk.py.
This file tests certificate-related functionality in the SDK session layer.
"""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.cvpysdk import CVPySDK


@pytest.mark.unit
class TestCertificateHandling:
    """Tests for certificate handling in CVPySDK._request."""

    def test_request_with_certificate_path_https(self):
        commcell = MagicMock()
        commcell._web_service = "https://example.com/api/"
        sdk = CVPySDK(commcell, certificate_path="/path/to/cert")

        with patch("cvpysdk.cvpysdk.requests.request") as mock_req:
            mock_req.return_value = MagicMock()
            sdk._request(method="GET", url="https://example.com/api/test")
            mock_req.assert_called_once_with(
                verify="/path/to/cert", method="GET", url="https://example.com/api/test"
            )

    def test_request_without_certificate_uses_verify_ssl(self):
        commcell = MagicMock()
        commcell._web_service = "https://example.com/api/"
        sdk = CVPySDK(commcell, certificate_path=None, verify_ssl=True)

        with patch("cvpysdk.cvpysdk.requests.request") as mock_req:
            mock_req.return_value = MagicMock()
            sdk._request(method="GET", url="https://example.com/api/test")
            mock_req.assert_called_once_with(
                verify=True, method="GET", url="https://example.com/api/test"
            )

    def test_request_ssl_disabled(self):
        commcell = MagicMock()
        commcell._web_service = "https://example.com/api/"

        with patch("cvpysdk.cvpysdk.urllib3.disable_warnings"):
            sdk = CVPySDK(commcell, verify_ssl=False)

        with patch("cvpysdk.cvpysdk.requests.request") as mock_req:
            mock_req.return_value = MagicMock()
            sdk._request(method="GET", url="https://example.com/api/test")
            mock_req.assert_called_once_with(
                verify=False, method="GET", url="https://example.com/api/test"
            )

    def test_certificate_path_not_used_for_http(self):
        commcell = MagicMock()
        commcell._web_service = "http://example.com/api/"
        sdk = CVPySDK(commcell, certificate_path="/path/to/cert")

        with patch("cvpysdk.cvpysdk.requests.request") as mock_req:
            mock_req.return_value = MagicMock()
            sdk._request(method="GET", url="http://example.com/api/test")
            # When web_service does not start with https, verify_ssl is used instead
            mock_req.assert_called_once_with(
                verify=True, method="GET", url="http://example.com/api/test"
            )

    def test_init_stores_certificate_path(self):
        commcell = MagicMock()
        sdk = CVPySDK(commcell, certificate_path="/certs/ca-bundle.crt")
        assert sdk._certificate_path == "/certs/ca-bundle.crt"

    def test_init_default_certificate_path_is_none(self):
        commcell = MagicMock()
        sdk = CVPySDK(commcell)
        assert sdk._certificate_path is None
