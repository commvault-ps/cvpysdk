"""Unit tests for cvpysdk.cleanroom.cs_recovery module."""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.cleanroom.cs_recovery import CommServeRecovery


@pytest.mark.unit
class TestCommServeRecoveryClass:
    """Tests for the CommServeRecovery class existence and structure."""

    def test_class_exists_and_importable(self):
        from cvpysdk.cleanroom import cs_recovery

        assert hasattr(cs_recovery, "CommServeRecovery")

    def test_has_expected_methods(self):
        assert hasattr(CommServeRecovery, "start_recovery")
        assert hasattr(CommServeRecovery, "extend_reservation")
        assert hasattr(CommServeRecovery, "get_vm_details")
        assert hasattr(CommServeRecovery, "_get_backupsets")
        assert hasattr(CommServeRecovery, "_get_active_recovery_requests")
        assert hasattr(CommServeRecovery, "_quota_details")

    def test_has_expected_properties(self):
        assert isinstance(CommServeRecovery.is_licensed_commcell, property)
        assert isinstance(CommServeRecovery.backupsets, property)
        assert isinstance(CommServeRecovery.active_recovery_requests, property)
        assert isinstance(CommServeRecovery.recovery_license_details, property)
        assert isinstance(CommServeRecovery.manual_retention_details, property)


@pytest.mark.unit
class TestCommServeRecoveryInit:
    """Tests for CommServeRecovery initialization."""

    def _make_commcell_mock(self):
        commcell = MagicMock()
        commcell._services = {
            "COMMSERVE_RECOVERY": "http://api/csrecovery",
            "GET_COMMSERVE_RECOVERY_LICENSE_DETAILS": "http://api/license/%s",
            "GET_COMMSERVE_RECOVERY_RETENTION_DETAILS": "http://api/retention/%s",
            "GET_BACKUPSET_INFO": "http://api/backupset/%s",
        }
        return commcell

    def test_init_stores_cs_guid(self):
        commcell = self._make_commcell_mock()
        with patch.object(CommServeRecovery, "_quota_details", return_value={"is_licensed": True}):
            with patch.object(CommServeRecovery, "_manual_retention_details", return_value={}):
                obj = CommServeRecovery(commcell, "test-guid-123")
        assert obj.cs_guid == "test-guid-123"

    def test_init_sets_is_licensed(self):
        commcell = self._make_commcell_mock()
        with patch.object(CommServeRecovery, "_quota_details", return_value={"is_licensed": True}):
            with patch.object(CommServeRecovery, "_manual_retention_details", return_value={}):
                obj = CommServeRecovery(commcell, "guid")
        assert obj.is_licensed_commcell is True


@pytest.mark.unit
class TestCommServeRecoveryMethods:
    """Tests for CommServeRecovery methods."""

    def _make_instance(self):
        with patch.object(CommServeRecovery, "__init__", lambda self, *a, **k: None):
            obj = CommServeRecovery.__new__(CommServeRecovery)
        obj._commcell_object = MagicMock()
        obj._cvpysdk_object = MagicMock()
        obj._services = {}
        obj.cs_guid = "test-guid"
        obj._CS_RECOVERY_API = "http://api/csrecovery"
        return obj

    def test_start_recovery_delegates(self):
        obj = self._make_instance()
        with patch.object(CommServeRecovery, "_create_cs_recovery_request", return_value=42):
            result = obj.start_recovery("SET_1")
        assert result == 42

    def test_extend_reservation_delegates(self):
        obj = self._make_instance()
        with patch.object(CommServeRecovery, "_extend_recovery_request", return_value=True):
            result = obj.extend_reservation(42)
        assert result is True

    def test_get_vm_details_delegates(self):
        obj = self._make_instance()
        with patch.object(
            CommServeRecovery, "_get_vm_details", return_value={"url": "http://example.com"}
        ):
            result = obj.get_vm_details(42)
        assert result == {"url": "http://example.com"}
