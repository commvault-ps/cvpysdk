from unittest.mock import patch

import pytest

from cvpysdk.exception import SDKException
from cvpysdk.security.security_association import SecurityAssociation


@pytest.mark.unit
class TestSecurityAssociation:
    """Tests for the SecurityAssociation class."""

    def _make_sa(self, mock_commcell):
        with patch.object(SecurityAssociation, "_get_security_roles", return_value={}):
            return SecurityAssociation(mock_commcell, mock_commcell)

    def test_repr(self, mock_commcell):
        sa = self._make_sa(mock_commcell)
        assert "Security" in repr(sa)

    def test_has_role_true(self, mock_commcell):
        with patch.object(
            SecurityAssociation,
            "_get_security_roles",
            return_value={"admin": 1},
        ):
            sa = SecurityAssociation(mock_commcell, mock_commcell)
        assert sa.has_role("admin") is True

    def test_has_role_case_insensitive(self, mock_commcell):
        with patch.object(
            SecurityAssociation,
            "_get_security_roles",
            return_value={"admin": 1},
        ):
            sa = SecurityAssociation(mock_commcell, mock_commcell)
        assert sa.has_role("Admin") is True

    def test_has_role_non_string_raises(self, mock_commcell):
        sa = self._make_sa(mock_commcell)
        with pytest.raises(SDKException):
            sa.has_role(123)

    def test_security_association_json_basic(self):
        entity_dict = {
            "assoc1": {
                "clientName": ["client1"],
                "role": ["role1"],
            }
        }
        result = SecurityAssociation._security_association_json(entity_dict)
        assert len(result) == 1
        assert result[0]["entities"]["entity"][0]["clientName"] == "client1"
        assert result[0]["properties"]["role"]["roleName"] == "role1"

    def test_security_association_json_multiple_entities(self):
        entity_dict = {
            "assoc1": {
                "clientName": ["client1", "client2"],
                "role": ["role1"],
            }
        }
        result = SecurityAssociation._security_association_json(entity_dict)
        assert len(result) == 2

    def test_security_association_json_type_flag(self):
        entity_dict = {
            "assoc1": {
                "_type_": [3],
                "role": ["role1"],
            }
        }
        result = SecurityAssociation._security_association_json(entity_dict)
        assert len(result) == 1
        entity = result[0]["entities"]["entity"][0]
        assert entity["_type_"] == 3
        assert "flags" in entity

    def test_fetch_security_association_empty(self):
        result = SecurityAssociation.fetch_security_association([])
        assert result == {}

    def test_str_representation(self, mock_commcell):
        with patch.object(
            SecurityAssociation,
            "_get_security_roles",
            return_value={"admin": 1, "viewer": 2},
        ):
            sa = SecurityAssociation(mock_commcell, mock_commcell)
        result = str(sa)
        assert "Roles" in result
