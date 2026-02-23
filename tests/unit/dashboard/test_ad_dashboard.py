"""Unit tests for cvpysdk.dashboard.ad_dashboard module."""

import pytest

from cvpysdk.dashboard.ad_dashboard import AdDashboard


@pytest.mark.unit
class TestAdDashboard:
    """Tests for the AdDashboard class."""

    def test_init(self, mock_commcell):
        """Test constructor initializes attributes."""
        dashboard = AdDashboard(mock_commcell)
        assert dashboard._commcell_object is mock_commcell
        assert dashboard._cvpysdk_object is mock_commcell._cvpysdk_object
        assert dashboard._services is mock_commcell._services
        assert dashboard.dashboard_response is None
        assert dashboard.apps_response is None

    def test_get_ad_dashboard_details_success(self, mock_commcell, mock_response):
        """Test get_ad_dashboard_details stores response on success."""
        dashboard = AdDashboard(mock_commcell)
        resp = mock_response(json_data={"agentSummary": [{"isConfigured": True}]})
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        dashboard.get_ad_dashboard_details()
        assert dashboard.dashboard_response is not None

    def test_get_ad_apps_details_success(self, mock_commcell, mock_response):
        """Test get_ad_apps_details stores response on success."""
        dashboard = AdDashboard(mock_commcell)
        resp = mock_response(json_data={"totalADClients": 2, "adClients": []})
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        dashboard.get_ad_apps_details()
        assert dashboard.apps_response is not None

    def test_is_configured_property(self, mock_commcell):
        """Test is_configured returns configuration dict."""
        dashboard = AdDashboard(mock_commcell)
        dashboard.dashboard_response = {
            "agentSummary": [
                {"isConfigured": True},
                {"isConfigured": False},
            ]
        }
        dashboard.apps_response = {
            "totalADClients": 2,
            "adClients": [
                {"isConfigured": True, "appTypeId": 41},
                {"isConfigured": True, "appTypeId": 139},
            ],
        }
        result = dashboard.is_configured
        assert result["adconfigure"] is True
        assert result["aadconfigure"] is False
        assert result["apps_adconfigure"] is True
        assert result["apps_aadconfigure"] is True

    def test_domains_and_tenants_property(self, mock_commcell):
        """Test domains_and_tenants returns count data."""
        dashboard = AdDashboard(mock_commcell)
        dashboard.dashboard_response = {
            "solutionSummary": {"slaSummary": {"totalEntities": 5}},
            "agentSummary": [
                {"slaSummary": {"totalEntities": 3}},
                {"slaSummary": {"totalEntities": 2}},
            ],
        }
        dashboard.apps_response = {
            "adClients": [
                {"appTypeId": 41, "slaStatus": "MET_SLA"},
                {"appTypeId": 139, "slaStatus": "MET_SLA"},
            ]
        }
        result = dashboard.domains_and_tenants
        assert result["total_entities"] == 5
        assert result["domain_controllers"] == 3
        assert result["tenants"] == 2
        assert result["apps_domain_controllers"] == 1
        assert result["apps_tenants"] == 1

    def test_backup_health_property(self, mock_commcell):
        """Test backup_health returns health metrics."""
        dashboard = AdDashboard(mock_commcell)
        dashboard.dashboard_response = {
            "solutionSummary": {
                "slaSummary": {
                    "totalEntities": 10,
                    "slaNotMetEntities": 3,
                    "neverBackedupEntities": 1,
                    "slaMetPercentage": 70.0,
                    "slaNotMetProcessedAtleastOncePercentage": 20.0,
                    "neverBackedupPercentage": 10.0,
                }
            }
        }
        dashboard.apps_response = {
            "adClients": [
                {"slaStatus": "MET_SLA", "numberOfItems": 5},
                {"slaStatus": "MISSED_SLA", "numberOfItems": 3},
                {"slaStatus": "MISSED_SLA", "numberOfItems": 0},
            ]
        }
        result = dashboard.backup_health
        assert result["recently_backedup"] == 7
        assert result["recently_not_backedup"] == 2
        assert result["never_backedup"] == 1
        assert result["apps_recently_backedup"] == 1
        assert result["apps_recently_not_backedup"] == 1
        assert result["apps_never_backedup"] == 1
