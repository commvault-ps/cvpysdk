"""Unit tests for cvpysdk.license module."""

import pytest

from cvpysdk.exception import SDKException
from cvpysdk.license import LicenseDetails


@pytest.mark.unit
class TestLicenseDetails:
    """Tests for the LicenseDetails class."""

    def _make_license(self, mock_commcell, mock_response):
        resp = mock_response(
            json_data={
                "commcellId": 12345,
                "csHostNameOrAddress": "testcs.example.com",
                "licenseIpAddress": "10.0.0.1",
                "oemName": "Commvault",
                "regCode": "REG-CODE-123",
                "serialNo": "SN-456",
                "licenseMode": "Evaluation",
                "expiryDate": "2026-12-31",
            }
        )
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        return LicenseDetails(mock_commcell)

    def test_init(self, mock_commcell, mock_response):
        ld = self._make_license(mock_commcell, mock_response)
        assert ld.commcell_id == 12345

    def test_commcell_id_hex(self, mock_commcell, mock_response):
        ld = self._make_license(mock_commcell, mock_response)
        assert ld.commcell_id_hex == hex(12345).split("x")[1].upper()

    def test_commcell_id_hex_negative_one(self, mock_commcell, mock_response):
        ld = self._make_license(mock_commcell, mock_response)
        ld._commcell_id = -1
        assert ld.commcell_id_hex == "FFFFF"

    def test_cs_hostname(self, mock_commcell, mock_response):
        ld = self._make_license(mock_commcell, mock_response)
        assert ld.cs_hostname == "testcs.example.com"

    def test_license_ipaddress(self, mock_commcell, mock_response):
        ld = self._make_license(mock_commcell, mock_response)
        assert ld.license_ipaddress == "10.0.0.1"

    def test_oem_name(self, mock_commcell, mock_response):
        ld = self._make_license(mock_commcell, mock_response)
        assert ld.oem_name == "Commvault"

    def test_license_mode(self, mock_commcell, mock_response):
        ld = self._make_license(mock_commcell, mock_response)
        assert ld.license_mode == "Evaluation"

    def test_registration_code(self, mock_commcell, mock_response):
        ld = self._make_license(mock_commcell, mock_response)
        assert ld.registration_code == "REG-CODE-123"

    def test_serial_number(self, mock_commcell, mock_response):
        ld = self._make_license(mock_commcell, mock_response)
        assert ld.serial_number == "SN-456"

    def test_expiry_date(self, mock_commcell, mock_response):
        ld = self._make_license(mock_commcell, mock_response)
        assert ld.expiry_date == "2026-12-31"

    def test_init_raises_on_empty_response(self, mock_commcell, mock_response):
        resp = mock_response(json_data={})
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        with pytest.raises(SDKException):
            LicenseDetails(mock_commcell)

    def test_init_raises_on_api_failure(self, mock_commcell, mock_response):
        resp = mock_response(status_code=500, text="Server Error")
        mock_commcell._cvpysdk_object.make_request.return_value = (False, resp)
        with pytest.raises(SDKException):
            LicenseDetails(mock_commcell)
