from unittest.mock import patch

import pytest

from cvpysdk.exception import SDKException
from cvpysdk.virtualmachinepolicies import VirtualMachinePolicies


@pytest.mark.unit
class TestVirtualMachinePolicies:
    """Tests for the VirtualMachinePolicies collection class."""

    def test_repr(self, mock_commcell):
        with patch.object(VirtualMachinePolicies, "_get_vm_policies", return_value={}):
            vmp = VirtualMachinePolicies(mock_commcell)
        assert "VirtualMachinePolicies" in repr(vmp)

    def test_vm_policies_property(self, mock_commcell):
        policies = {"policy1": {"id": "1", "policyType": "4"}}
        with patch.object(VirtualMachinePolicies, "_get_vm_policies", return_value=policies):
            vmp = VirtualMachinePolicies(mock_commcell)
        assert vmp._vm_policies == policies

    def test_has_policy_true(self, mock_commcell):
        policies = {"policy1": {"id": "1", "policyType": "4"}}
        with patch.object(VirtualMachinePolicies, "_get_vm_policies", return_value=policies):
            vmp = VirtualMachinePolicies(mock_commcell)
        assert vmp.has_policy("policy1") is True

    def test_has_policy_case_insensitive(self, mock_commcell):
        policies = {"policy1": {"id": "1", "policyType": "4"}}
        with patch.object(VirtualMachinePolicies, "_get_vm_policies", return_value=policies):
            vmp = VirtualMachinePolicies(mock_commcell)
        assert vmp.has_policy("POLICY1") is True

    def test_str_representation(self, mock_commcell):
        policies = {"policy1": {"id": "1", "policyType": "4"}}
        with patch.object(VirtualMachinePolicies, "_get_vm_policies", return_value=policies):
            vmp = VirtualMachinePolicies(mock_commcell)
        result = str(vmp)
        assert "policy1" in result

    def test_refresh(self, mock_commcell):
        with patch.object(VirtualMachinePolicies, "_get_vm_policies", return_value={}) as mock_get:
            vmp = VirtualMachinePolicies(mock_commcell)
            vmp.refresh()
        assert mock_get.call_count == 2

    def test_get_nonexistent_raises(self, mock_commcell):
        with patch.object(VirtualMachinePolicies, "_get_vm_policies", return_value={}):
            vmp = VirtualMachinePolicies(mock_commcell)
        with pytest.raises(SDKException):
            vmp.get("nonexistent")
