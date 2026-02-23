"""Unit tests for cvpysdk.recovery_targets module."""

from unittest.mock import patch

import pytest

from cvpysdk.exception import SDKException
from cvpysdk.recovery_targets import RecoveryTarget, RecoveryTargets


@pytest.mark.unit
class TestRecoveryTargets:
    """Tests for the RecoveryTargets collection class."""

    def _make_targets(self, mock_commcell, mock_response):
        resp = mock_response(
            json_data={
                "recoveryTargets": [
                    {
                        "name": "Target1",
                        "id": 1,
                        "applicationType": "LIVE_MOUNT",
                    },
                    {
                        "name": "Target2",
                        "id": 2,
                        "applicationType": "CLEAN_ROOM",
                    },
                ]
            }
        )
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        return RecoveryTargets(mock_commcell)

    def test_init_populates_targets(self, mock_commcell, mock_response):
        targets = self._make_targets(mock_commcell, mock_response)
        assert "target1" in targets.all_targets
        # CLEAN_ROOM should be excluded
        assert "target2" not in targets.all_targets

    def test_has_recovery_target_true(self, mock_commcell, mock_response):
        targets = self._make_targets(mock_commcell, mock_response)
        assert targets.has_recovery_target("Target1") is True

    def test_has_recovery_target_false(self, mock_commcell, mock_response):
        targets = self._make_targets(mock_commcell, mock_response)
        assert targets.has_recovery_target("missing") is False

    def test_get_returns_recovery_target_object(self, mock_commcell, mock_response):
        targets = self._make_targets(mock_commcell, mock_response)
        with patch.object(RecoveryTarget, "__init__", return_value=None):
            result = targets.get("Target1")
            assert isinstance(result, RecoveryTarget)

    def test_get_raises_on_missing(self, mock_commcell, mock_response):
        targets = self._make_targets(mock_commcell, mock_response)
        with pytest.raises(SDKException):
            targets.get("nonexistent")

    def test_str_contains_target_names(self, mock_commcell, mock_response):
        targets = self._make_targets(mock_commcell, mock_response)
        result = str(targets)
        assert "target1" in result

    def test_init_raises_on_empty_response(self, mock_commcell, mock_response):
        resp = mock_response(json_data={})
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        with pytest.raises(SDKException):
            RecoveryTargets(mock_commcell)
