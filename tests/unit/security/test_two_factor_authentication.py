from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.exception import SDKException
from cvpysdk.security.two_factor_authentication import TwoFactorAuthentication


@pytest.mark.unit
class TestTwoFactorAuthentication:
    """Tests for the TwoFactorAuthentication class."""

    def _make_tfa(self, mock_commcell, org_id=None):
        with patch.object(TwoFactorAuthentication, "_get_tfa_info"):
            return TwoFactorAuthentication(mock_commcell, organization_id=org_id)

    def test_init_default(self, mock_commcell):
        tfa = self._make_tfa(mock_commcell)
        assert tfa._org_id is None

    def test_init_with_org_id_int(self, mock_commcell):
        tfa = self._make_tfa(mock_commcell, org_id=5)
        assert tfa._org_id == 5

    def test_init_with_org_id_str(self, mock_commcell):
        tfa = self._make_tfa(mock_commcell, org_id="5")
        assert tfa._org_id == "5"

    def test_init_with_invalid_org_id_raises(self, mock_commcell):
        with pytest.raises(SDKException):
            with patch.object(TwoFactorAuthentication, "_get_tfa_info"):
                TwoFactorAuthentication(mock_commcell, organization_id=[1, 2])

    def test_is_tfa_enabled_property(self, mock_commcell):
        tfa = self._make_tfa(mock_commcell)
        tfa._tfa_status = True
        assert tfa.is_tfa_enabled is True

    def test_is_tfa_disabled(self, mock_commcell):
        tfa = self._make_tfa(mock_commcell)
        tfa._tfa_status = False
        assert tfa.is_tfa_enabled is False

    def test_tfa_enabled_user_groups_property(self, mock_commcell):
        tfa = self._make_tfa(mock_commcell)
        tfa._tfa_enabled_user_groups = [{"userGroupName": "group1"}]
        assert tfa.tfa_enabled_user_groups == [{"userGroupName": "group1"}]

    def test_refresh_calls_get_info(self, mock_commcell):
        with patch.object(TwoFactorAuthentication, "_get_tfa_info") as mock_get:
            tfa = TwoFactorAuthentication(mock_commcell)
            tfa.refresh()
        assert mock_get.call_count == 2

    def test_process_response_empty_json_raises(self, mock_commcell):
        tfa = self._make_tfa(mock_commcell)
        response = MagicMock()
        response.json.return_value = {}
        with pytest.raises(SDKException):
            tfa._process_response(True, response)

    def test_process_response_error_code_raises(self, mock_commcell):
        tfa = self._make_tfa(mock_commcell)
        response = MagicMock()
        response.json.return_value = {"error": {"errorCode": 1, "errorString": "test error"}}
        with pytest.raises(SDKException):
            tfa._process_response(True, response)
