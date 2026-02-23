from unittest.mock import patch

import pytest

from cvpysdk.exception import SDKException
from cvpysdk.monitoring import MonitoringPolicies, MonitoringPolicy


@pytest.mark.unit
class TestMonitoringPolicies:
    """Tests for the MonitoringPolicies collection class."""

    def test_repr(self, mock_commcell):
        with patch.object(
            MonitoringPolicies, "_get_monitoring_policies", return_value={}
        ), patch.object(
            MonitoringPolicies, "_get_analytics_servers", return_value={}
        ), patch.object(MonitoringPolicies, "_get_templates", return_value={}):
            mp = MonitoringPolicies(mock_commcell)
        assert "MonitoringPolicies" in repr(mp)

    def test_all_monitoring_policies_property(self, mock_commcell):
        policies = {"policy1": 1}
        with patch.object(
            MonitoringPolicies, "_get_monitoring_policies", return_value=policies
        ), patch.object(
            MonitoringPolicies, "_get_analytics_servers", return_value={}
        ), patch.object(MonitoringPolicies, "_get_templates", return_value={}):
            mp = MonitoringPolicies(mock_commcell)
        assert mp.all_monitoring_policies == policies

    def test_all_analytics_servers_property(self, mock_commcell):
        servers = {"server1": 1}
        with patch.object(
            MonitoringPolicies, "_get_monitoring_policies", return_value={}
        ), patch.object(
            MonitoringPolicies, "_get_analytics_servers", return_value=servers
        ), patch.object(MonitoringPolicies, "_get_templates", return_value={}):
            mp = MonitoringPolicies(mock_commcell)
        assert mp.all_analytics_servers == servers

    def test_all_templates_property(self, mock_commcell):
        templates = {"template1": {"id": 1, "type": 0}}
        with patch.object(
            MonitoringPolicies, "_get_monitoring_policies", return_value={}
        ), patch.object(
            MonitoringPolicies, "_get_analytics_servers", return_value={}
        ), patch.object(MonitoringPolicies, "_get_templates", return_value=templates):
            mp = MonitoringPolicies(mock_commcell)
        assert mp.all_templates == templates

    def test_has_monitoring_policy_true(self, mock_commcell):
        policies = {"policy1": 1}
        with patch.object(
            MonitoringPolicies, "_get_monitoring_policies", return_value=policies
        ), patch.object(
            MonitoringPolicies, "_get_analytics_servers", return_value={}
        ), patch.object(MonitoringPolicies, "_get_templates", return_value={}):
            mp = MonitoringPolicies(mock_commcell)
        assert mp.has_monitoring_policy("policy1") is True

    def test_has_monitoring_policy_bad_type_raises(self, mock_commcell):
        with patch.object(
            MonitoringPolicies, "_get_monitoring_policies", return_value={}
        ), patch.object(
            MonitoringPolicies, "_get_analytics_servers", return_value={}
        ), patch.object(MonitoringPolicies, "_get_templates", return_value={}):
            mp = MonitoringPolicies(mock_commcell)
        with pytest.raises(SDKException):
            mp.has_monitoring_policy(123)

    def test_has_analytics_server_true(self, mock_commcell):
        servers = {"server1": 1}
        with patch.object(
            MonitoringPolicies, "_get_monitoring_policies", return_value={}
        ), patch.object(
            MonitoringPolicies, "_get_analytics_servers", return_value=servers
        ), patch.object(MonitoringPolicies, "_get_templates", return_value={}):
            mp = MonitoringPolicies(mock_commcell)
        assert mp.has_analytics_server("server1") is True

    def test_has_analytics_server_bad_type_raises(self, mock_commcell):
        with patch.object(
            MonitoringPolicies, "_get_monitoring_policies", return_value={}
        ), patch.object(
            MonitoringPolicies, "_get_analytics_servers", return_value={}
        ), patch.object(MonitoringPolicies, "_get_templates", return_value={}):
            mp = MonitoringPolicies(mock_commcell)
        with pytest.raises(SDKException):
            mp.has_analytics_server(123)

    def test_has_template_true(self, mock_commcell):
        templates = {"tmpl1": {"id": 1, "type": 0}}
        with patch.object(
            MonitoringPolicies, "_get_monitoring_policies", return_value={}
        ), patch.object(
            MonitoringPolicies, "_get_analytics_servers", return_value={}
        ), patch.object(MonitoringPolicies, "_get_templates", return_value=templates):
            mp = MonitoringPolicies(mock_commcell)
        assert mp.has_template("tmpl1") is True

    def test_has_template_bad_type_raises(self, mock_commcell):
        with patch.object(
            MonitoringPolicies, "_get_monitoring_policies", return_value={}
        ), patch.object(
            MonitoringPolicies, "_get_analytics_servers", return_value={}
        ), patch.object(MonitoringPolicies, "_get_templates", return_value={}):
            mp = MonitoringPolicies(mock_commcell)
        with pytest.raises(SDKException):
            mp.has_template(123)

    def test_get_bad_type_raises(self, mock_commcell):
        with patch.object(
            MonitoringPolicies, "_get_monitoring_policies", return_value={}
        ), patch.object(
            MonitoringPolicies, "_get_analytics_servers", return_value={}
        ), patch.object(MonitoringPolicies, "_get_templates", return_value={}):
            mp = MonitoringPolicies(mock_commcell)
        with pytest.raises(SDKException):
            mp.get(123)

    def test_get_nonexistent_raises(self, mock_commcell):
        with patch.object(
            MonitoringPolicies, "_get_monitoring_policies", return_value={}
        ), patch.object(
            MonitoringPolicies, "_get_analytics_servers", return_value={}
        ), patch.object(MonitoringPolicies, "_get_templates", return_value={}):
            mp = MonitoringPolicies(mock_commcell)
        with pytest.raises(SDKException):
            mp.get("nonexistent")

    def test_delete_bad_type_raises(self, mock_commcell):
        with patch.object(
            MonitoringPolicies, "_get_monitoring_policies", return_value={}
        ), patch.object(
            MonitoringPolicies, "_get_analytics_servers", return_value={}
        ), patch.object(MonitoringPolicies, "_get_templates", return_value={}):
            mp = MonitoringPolicies(mock_commcell)
        with pytest.raises(SDKException):
            mp.delete(123)

    def test_str_representation(self, mock_commcell):
        policies = {"policy1": 1}
        with patch.object(
            MonitoringPolicies, "_get_monitoring_policies", return_value=policies
        ), patch.object(
            MonitoringPolicies, "_get_analytics_servers", return_value={}
        ), patch.object(MonitoringPolicies, "_get_templates", return_value={}):
            mp = MonitoringPolicies(mock_commcell)
        result = str(mp)
        assert "policy1" in result


@pytest.mark.unit
class TestMonitoringPolicy:
    """Tests for the MonitoringPolicy entity class."""

    def test_repr(self, mock_commcell):
        policy = MonitoringPolicy(mock_commcell, "test_policy", monitoring_policy_id=1)
        assert "test_policy" in repr(policy)

    def test_monitoring_policy_name_property(self, mock_commcell):
        policy = MonitoringPolicy(mock_commcell, "Test_Policy", monitoring_policy_id=1)
        assert policy.monitoring_policy_name == "test_policy"

    def test_monitoring_policy_id_property(self, mock_commcell):
        policy = MonitoringPolicy(mock_commcell, "test_policy", monitoring_policy_id=42)
        assert policy.monitoring_policy_id == "42"
