"""Unit tests for cvpysdk/organization.py module."""

from unittest.mock import patch

import pytest

from cvpysdk.exception import SDKException
from cvpysdk.organization import Organization, Organizations


@pytest.mark.unit
class TestOrganizationsInit:
    """Tests for the Organizations collection class."""

    def test_repr(self, mock_commcell):
        with patch.object(Organizations, "_get_organizations", return_value={}):
            orgs = Organizations(mock_commcell)
        assert "Organizations" in repr(orgs)

    def test_all_organizations_property(self, mock_commcell):
        data = {"test-org": {"id": "1"}}
        with patch.object(Organizations, "_get_organizations", return_value=data):
            orgs = Organizations(mock_commcell)
        assert orgs.all_organizations == data

    def test_len(self, mock_commcell):
        data = {"org1": {"id": "1"}, "org2": {"id": "2"}}
        with patch.object(Organizations, "_get_organizations", return_value=data):
            orgs = Organizations(mock_commcell)
        assert len(orgs) == 2

    def test_len_empty(self, mock_commcell):
        with patch.object(Organizations, "_get_organizations", return_value={}):
            orgs = Organizations(mock_commcell)
        assert len(orgs) == 0


@pytest.mark.unit
class TestOrganizationsHasOrganization:
    """Tests for Organizations.has_organization."""

    def test_has_organization_true(self, mock_commcell):
        data = {"test-org": {"id": "1"}}
        with patch.object(Organizations, "_get_organizations", return_value=data):
            orgs = Organizations(mock_commcell)
        assert orgs.has_organization("test-org") is True

    def test_has_organization_false(self, mock_commcell):
        with patch.object(Organizations, "_get_organizations", return_value={}):
            orgs = Organizations(mock_commcell)
        assert not orgs.has_organization("nonexistent")

    def test_has_organization_bad_type_raises(self, mock_commcell):
        with patch.object(Organizations, "_get_organizations", return_value={}):
            orgs = Organizations(mock_commcell)
        with pytest.raises(SDKException):
            orgs.has_organization(123)

    def test_has_organization_case_insensitive(self, mock_commcell):
        data = {"test-org": {"id": "1"}}
        with patch.object(Organizations, "_get_organizations", return_value=data):
            orgs = Organizations(mock_commcell)
        assert orgs.has_organization("Test-Org") is True


@pytest.mark.unit
class TestOrganizationsGetItem:
    """Tests for Organizations.__getitem__."""

    def test_getitem_by_name(self, mock_commcell):
        data = {"test-org": {"id": "1"}}
        with patch.object(Organizations, "_get_organizations", return_value=data):
            orgs = Organizations(mock_commcell)
        result = orgs["test-org"]
        assert result["id"] == "1"

    def test_getitem_by_id(self, mock_commcell):
        data = {"test-org": {"id": "1"}}
        with patch.object(Organizations, "_get_organizations", return_value=data):
            orgs = Organizations(mock_commcell)
        result = orgs["1"]
        assert result == "test-org"

    def test_getitem_not_found(self, mock_commcell):
        with patch.object(Organizations, "_get_organizations", return_value={}):
            orgs = Organizations(mock_commcell)
        with pytest.raises(IndexError):
            orgs["nonexistent"]


@pytest.mark.unit
class TestOrganizationsRefresh:
    """Tests for Organizations.refresh."""

    def test_refresh_reloads(self, mock_commcell):
        with patch.object(Organizations, "_get_organizations", return_value={}) as mock_get:
            orgs = Organizations(mock_commcell)
            orgs.refresh()
            assert mock_get.call_count == 2


@pytest.mark.unit
class TestOrganizationRepr:
    """Tests for Organization __repr__."""

    def test_repr_contains_org_name(self):
        with patch.object(Organization, "__init__", lambda self, *a, **kw: None):
            org = Organization.__new__(Organization)
            org._organization_name = "TestOrg"
            result = repr(org)
            assert "testorg" in result


@pytest.mark.unit
class TestOrganizationProperties:
    """Tests for Organization property getters."""

    def test_organization_id(self):
        with patch.object(Organization, "__init__", lambda self, *a, **kw: None):
            org = Organization.__new__(Organization)
            org._organization_id = "42"
            assert org.organization_id == "42"

    def test_organization_name(self):
        with patch.object(Organization, "__init__", lambda self, *a, **kw: None):
            org = Organization.__new__(Organization)
            org._organization_name = "MyOrg"
            assert org.organization_name == "myorg"
