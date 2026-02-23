"""Unit tests for cvpysdk/commcell.py module."""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.commcell import Commcell


@pytest.mark.unit
class TestCommcellContextManager:
    """Tests for Commcell __enter__/__exit__."""

    def test_enter_returns_self(self):
        with patch.object(Commcell, "__init__", lambda x, *a, **kw: None):
            cc = Commcell.__new__(Commcell)
            assert cc.__enter__() is cc

    def test_exit_calls_logout(self):
        with patch.object(Commcell, "__init__", lambda x, *a, **kw: None):
            cc = Commcell.__new__(Commcell)
            cc._cvpysdk_object = MagicMock()
            cc._cvpysdk_object._logout.return_value = "logged out"
            with patch.object(cc, "_remove_attribs_"):
                cc.__exit__(None, None, None)
            cc._cvpysdk_object._logout.assert_called_once()


@pytest.mark.unit
class TestCommcellUpdateResponse:
    """Tests for _update_response_ method."""

    def test_extracts_title(self):
        with patch.object(Commcell, "__init__", lambda x, *a, **kw: None):
            cc = Commcell.__new__(Commcell)
            result = cc._update_response_("<html><title>Error Page</title></html>")
            assert result == "Error Page"

    def test_returns_original_without_title(self):
        with patch.object(Commcell, "__init__", lambda x, *a, **kw: None):
            cc = Commcell.__new__(Commcell)
            result = cc._update_response_("plain text response")
            assert result == "plain text response"


@pytest.mark.unit
class TestCommcellLazyProperties:
    """Tests for lazy property loading on Commcell."""

    def _make_commcell(self):
        """Helper to create a Commcell with init bypassed."""
        with patch.object(Commcell, "__init__", lambda x, *a, **kw: None):
            cc = Commcell.__new__(Commcell)
            cc._commcell_object = cc
            cc._cvpysdk_object = MagicMock()
            cc._services = MagicMock()
            cc._headers = {"Authtoken": "fake-token"}
            cc._update_response_ = MagicMock()
            return cc

    def test_clients_lazy_init(self):
        cc = self._make_commcell()
        cc._clients = None
        with patch("cvpysdk.commcell.Clients") as MockClients:
            MockClients.return_value = MagicMock()
            result = cc.clients
            MockClients.assert_called_once_with(cc)
            assert result is not None

    def test_plans_lazy_init(self):
        cc = self._make_commcell()
        cc._plans = None
        with patch("cvpysdk.commcell.Plans") as MockPlans:
            MockPlans.return_value = MagicMock()
            result = cc.plans
            MockPlans.assert_called_once_with(cc)
            assert result is not None

    def test_organizations_lazy_init(self):
        cc = self._make_commcell()
        cc._organizations = None
        with patch("cvpysdk.commcell.Organizations") as MockOrgs:
            MockOrgs.return_value = MagicMock()
            result = cc.organizations
            MockOrgs.assert_called_once_with(cc)
            assert result is not None

    def test_client_groups_lazy_init(self):
        cc = self._make_commcell()
        cc._client_groups = None
        with patch("cvpysdk.commcell.ClientGroups") as MockCG:
            MockCG.return_value = MagicMock()
            result = cc.client_groups
            MockCG.assert_called_once_with(cc)
            assert result is not None

    def test_job_controller_lazy_init(self):
        cc = self._make_commcell()
        cc._job_controller = None
        with patch("cvpysdk.commcell.JobController") as MockJC:
            MockJC.return_value = MagicMock()
            result = cc.job_controller
            MockJC.assert_called_once_with(cc)
            assert result is not None

    def test_system_lazy_init(self):
        cc = self._make_commcell()
        cc._system = None
        with patch("cvpysdk.commcell.System") as MockSystem:
            MockSystem.return_value = MagicMock()
            result = cc.system
            MockSystem.assert_called_once_with(cc)
            assert result is not None

    def test_activate_lazy_init(self):
        cc = self._make_commcell()
        cc._activate = None
        with patch("cvpysdk.commcell.Activate") as MockActivate:
            MockActivate.return_value = MagicMock()
            result = cc.activate
            MockActivate.assert_called_once_with(cc)
            assert result is not None

    def test_policies_lazy_init(self):
        cc = self._make_commcell()
        cc._policies = None
        with patch("cvpysdk.commcell.Policies") as MockPolicies:
            MockPolicies.return_value = MagicMock()
            result = cc.policies
            MockPolicies.assert_called_once_with(cc)
            assert result is not None


@pytest.mark.unit
class TestCommcellServiceUrlConstruction:
    """Tests for service URL construction logic."""

    def test_get_services_returns_dict(self):
        from cvpysdk.services import get_services

        services = get_services("https://example.com/api/")
        assert isinstance(services, dict)
        assert "LOGIN" in services
        assert "LOGOUT" in services

    def test_services_contain_base_url(self):
        from cvpysdk.services import get_services

        base = "https://example.com/api/"
        services = get_services(base)
        assert services["LOGIN"].startswith(base) or base.rstrip("/") in services["LOGIN"]
