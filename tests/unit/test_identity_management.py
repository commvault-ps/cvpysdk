"""Unit tests for cvpysdk.identity_management module."""

from unittest.mock import patch

import pytest

from cvpysdk.exception import SDKException
from cvpysdk.identity_management import (
    IdentityManagementApp,
    IdentityManagementApps,
    SamlApp,
)


@pytest.mark.unit
class TestIdentityManagementApps:
    """Tests for the IdentityManagementApps collection class."""

    def _make_apps(self, mock_commcell, mock_response):
        resp = mock_response(
            json_data={
                "clientThirdPartyApps": [
                    {
                        "appName": "TestApp",
                        "appKey": "key1",
                        "appType": 2,
                        "appDescription": "desc",
                        "flags": 0,
                        "isEnabled": True,
                    }
                ]
            }
        )
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        return IdentityManagementApps(mock_commcell)

    def test_init_populates_apps(self, mock_commcell, mock_response):
        apps = self._make_apps(mock_commcell, mock_response)
        assert "testapp" in apps.all_apps

    def test_repr(self, mock_commcell, mock_response):
        apps = self._make_apps(mock_commcell, mock_response)
        assert repr(apps) == "IdentityManagementApps class instance for Commcell"

    def test_len(self, mock_commcell, mock_response):
        apps = self._make_apps(mock_commcell, mock_response)
        assert len(apps) == 1

    def test_has_identity_app_true(self, mock_commcell, mock_response):
        apps = self._make_apps(mock_commcell, mock_response)
        assert apps.has_identity_app("testapp") is True

    def test_has_identity_app_false(self, mock_commcell, mock_response):
        apps = self._make_apps(mock_commcell, mock_response)
        assert apps.has_identity_app("missing") is False

    def test_has_identity_app_raises_on_non_string(self, mock_commcell, mock_response):
        apps = self._make_apps(mock_commcell, mock_response)
        with pytest.raises(SDKException):
            apps.has_identity_app(123)

    def test_get_returns_app_object(self, mock_commcell, mock_response):
        apps = self._make_apps(mock_commcell, mock_response)
        with patch.object(IdentityManagementApp, "__init__", return_value=None):
            result = apps.get("TestApp")
            assert isinstance(result, IdentityManagementApp)

    def test_get_raises_on_non_string(self, mock_commcell, mock_response):
        apps = self._make_apps(mock_commcell, mock_response)
        with pytest.raises(SDKException):
            apps.get(123)

    def test_get_raises_on_missing(self, mock_commcell, mock_response):
        apps = self._make_apps(mock_commcell, mock_response)
        with pytest.raises(SDKException):
            apps.get("nonexistent")

    def test_get_saml_raises_on_missing(self, mock_commcell, mock_response):
        apps = self._make_apps(mock_commcell, mock_response)
        with pytest.raises(SDKException):
            apps.get_saml("nonexistent")


@pytest.mark.unit
class TestSamlApp:
    """Tests for the SamlApp class."""

    def test_init_with_properties(self, mock_commcell):
        props = {
            "name": "testsaml",
            "description": "test desc",
            "enabled": True,
            "autoCreateUser": False,
            "createdForCompany": None,
            "appKey": "abc",
        }
        app = SamlApp(mock_commcell, "testsaml", properties=props)
        assert app.saml_app_description == "test desc"
        assert app.is_saml_app_enabled is True
        assert app.is_auto_create_user is False
        assert app.is_company_saml_app is False

    def test_repr(self, mock_commcell):
        props = {"name": "testsaml", "appKey": "abc"}
        app = SamlApp(mock_commcell, "testsaml", properties=props)
        assert "testsaml" in repr(app)
