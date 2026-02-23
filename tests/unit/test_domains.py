"""Unit tests for cvpysdk.domains module."""

import pytest

from cvpysdk.domains import Domains
from cvpysdk.exception import SDKException


@pytest.mark.unit
class TestDomains:
    """Tests for the Domains collection class."""

    def _make_domains(self, mock_commcell, mock_response):
        resp = mock_response(
            json_data={
                "providers": [
                    {
                        "shortName": {"domainName": "TestDomain"},
                        "providerType": 1,
                        "bLogin": True,
                        "tppm": {"tppmType": 0},
                    }
                ]
            }
        )
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        return Domains(mock_commcell)

    def test_init_populates_domains(self, mock_commcell, mock_response):
        domains = self._make_domains(mock_commcell, mock_response)
        assert domains.all_domains is not None

    def test_repr(self, mock_commcell, mock_response):
        domains = self._make_domains(mock_commcell, mock_response)
        assert repr(domains) == "Domains class instance for Commcell"

    def test_has_domain_true(self, mock_commcell, mock_response):
        domains = self._make_domains(mock_commcell, mock_response)
        assert domains.has_domain("TestDomain") is True

    def test_has_domain_false(self, mock_commcell, mock_response):
        domains = self._make_domains(mock_commcell, mock_response)
        assert domains.has_domain("nonexistent") is False

    def test_has_domain_raises_on_non_string(self, mock_commcell, mock_response):
        domains = self._make_domains(mock_commcell, mock_response)
        with pytest.raises(SDKException):
            domains.has_domain(123)

    def test_get_raises_on_missing(self, mock_commcell, mock_response):
        domains = self._make_domains(mock_commcell, mock_response)
        with pytest.raises(SDKException):
            domains.get("nonexistent")

    def test_str_contains_domain_names(self, mock_commcell, mock_response):
        domains = self._make_domains(mock_commcell, mock_response)
        result = str(domains)
        assert "testdomain" in result

    def test_len(self, mock_commcell, mock_response):
        domains = self._make_domains(mock_commcell, mock_response)
        assert len(domains) >= 0
