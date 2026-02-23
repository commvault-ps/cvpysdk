"""Unit tests for cvpysdk/policy.py module."""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.policy import Policies


@pytest.mark.unit
class TestPoliciesInit:
    """Tests for the Policies class."""

    def test_repr(self, mock_commcell):
        policies = Policies(mock_commcell)
        assert "Policies" in repr(policies)

    def test_stores_commcell(self, mock_commcell):
        policies = Policies(mock_commcell)
        assert policies._commcell_object is mock_commcell

    def test_refresh_resets_lazy_attrs(self, mock_commcell):
        policies = Policies(mock_commcell)
        # After init, refresh is called, so lazy attrs should be None
        assert policies._configuration_policies is None
        assert policies._storage_policies is None
        assert policies._schedule_policies is None


@pytest.mark.unit
class TestPoliciesLazyProperties:
    """Tests for lazy property loading on Policies."""

    def test_configuration_policies_lazy(self, mock_commcell):
        policies = Policies(mock_commcell)
        with patch("cvpysdk.policy.ConfigurationPolicies") as MockConfigPolicies:
            MockConfigPolicies.return_value = MagicMock()
            result = policies.configuration_policies
            MockConfigPolicies.assert_called_once_with(mock_commcell)
            assert result is not None

    def test_storage_policies_lazy(self, mock_commcell):
        policies = Policies(mock_commcell)
        with patch("cvpysdk.policy.StoragePolicies") as MockSP:
            MockSP.return_value = MagicMock()
            result = policies.storage_policies
            MockSP.assert_called_once_with(mock_commcell)
            assert result is not None

    def test_schedule_policies_lazy(self, mock_commcell):
        policies = Policies(mock_commcell)
        with patch("cvpysdk.policy.SchedulePolicies") as MockSchedP:
            MockSchedP.return_value = MagicMock()
            result = policies.schedule_policies
            MockSchedP.assert_called_once_with(mock_commcell)
            assert result is not None

    def test_configuration_policies_cached(self, mock_commcell):
        policies = Policies(mock_commcell)
        with patch("cvpysdk.policy.ConfigurationPolicies") as MockConfigPolicies:
            mock_instance = MagicMock()
            MockConfigPolicies.return_value = mock_instance
            result1 = policies.configuration_policies
            result2 = policies.configuration_policies
            MockConfigPolicies.assert_called_once()
            assert result1 is result2

    def test_refresh_clears_cache(self, mock_commcell):
        policies = Policies(mock_commcell)
        with patch("cvpysdk.policy.ConfigurationPolicies") as MockConfigPolicies:
            MockConfigPolicies.return_value = MagicMock()
            _ = policies.configuration_policies
            policies.refresh()
            assert policies._configuration_policies is None
