from unittest.mock import patch

import pytest

from cvpysdk.exception import SDKException
from cvpysdk.policies.storage_policies import StoragePolicies, StoragePolicy


@pytest.mark.unit
class TestStoragePolicies:
    """Tests for the StoragePolicies collection class."""

    def _make_policies(self, mock_commcell, policies=None):
        with patch.object(StoragePolicies, "_get_policies", return_value=policies or {}):
            return StoragePolicies(mock_commcell)

    def test_repr(self, mock_commcell):
        sp = self._make_policies(mock_commcell)
        assert "StoragePolicies" in repr(sp)

    def test_str(self, mock_commcell):
        sp = self._make_policies(mock_commcell, policies={"pol1": "1"})
        result = str(sp)
        assert "pol1" in result

    def test_all_storage_policies_property(self, mock_commcell):
        policies = {"pol1": "1", "pol2": "2"}
        sp = self._make_policies(mock_commcell, policies=policies)
        assert sp.all_storage_policies == policies

    def test_has_policy_true(self, mock_commcell):
        sp = self._make_policies(mock_commcell, policies={"testpol": "1"})
        assert sp.has_policy("testpol") is True

    def test_has_policy_case_insensitive(self, mock_commcell):
        sp = self._make_policies(mock_commcell, policies={"testpol": "1"})
        assert sp.has_policy("TestPol") is True

    def test_has_policy_non_string_raises(self, mock_commcell):
        sp = self._make_policies(mock_commcell)
        with pytest.raises(SDKException):
            sp.has_policy(123)

    def test_get_returns_storage_policy(self, mock_commcell):
        sp = self._make_policies(mock_commcell, policies={"testpol": "1"})
        with patch.object(StoragePolicy, "__init__", return_value=None):
            result = sp.get("testpol")
        assert isinstance(result, StoragePolicy)

    def test_get_nonexistent_raises(self, mock_commcell):
        sp = self._make_policies(mock_commcell)
        with pytest.raises(SDKException):
            sp.get("nonexistent")

    def test_get_non_string_raises(self, mock_commcell):
        sp = self._make_policies(mock_commcell)
        with pytest.raises(SDKException):
            sp.get(123)

    def test_refresh_calls_get_policies(self, mock_commcell):
        with patch.object(StoragePolicies, "_get_policies", return_value={}) as mock_get:
            sp = StoragePolicies(mock_commcell)
            sp.refresh()
        assert mock_get.call_count == 2
