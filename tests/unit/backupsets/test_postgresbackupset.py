"""Tests for cvpysdk/backupsets/postgresbackupset.py (PostgresBackupset)."""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.backupset import Backupset
from cvpysdk.backupsets.postgresbackupset import PostgresBackupset
from cvpysdk.exception import SDKException


@pytest.mark.unit
class TestPostgresBackupsetInheritance:
    def test_inherits_backupset(self):
        assert issubclass(PostgresBackupset, Backupset)

    def test_has_configure_live_sync(self):
        assert hasattr(PostgresBackupset, "configure_live_sync")

    def test_has_run_live_sync(self):
        assert hasattr(PostgresBackupset, "run_live_sync")

    def test_has_restore_postgres_server(self):
        assert hasattr(PostgresBackupset, "restore_postgres_server")


@pytest.mark.unit
class TestPostgresBackupsetConfigureLiveSync:
    def _make_instance(self):
        inst = object.__new__(PostgresBackupset)
        inst._cvpysdk_object = MagicMock()
        inst._commcell_object = MagicMock()
        inst._LIVE_SYNC = "https://example.com/livesync"
        inst._update_response_ = MagicMock(return_value="error")
        return inst

    def test_configure_live_sync_success_returns_schedule(self):
        inst = self._make_instance()
        mock_response = MagicMock()
        mock_response.json.return_value = {"taskId": 42}
        inst._cvpysdk_object.make_request.return_value = (True, mock_response)

        with patch("cvpysdk.backupsets.postgresbackupset.Schedules") as mock_schedules_cls:
            mock_sched = MagicMock()
            mock_schedules_cls.return_value.get.return_value = mock_sched
            result = inst.configure_live_sync({"key": "val"})
            assert result == mock_sched

    def test_configure_live_sync_error_code_raises(self):
        inst = self._make_instance()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "errorCode": 1,
            "errorMessage": "some error",
        }
        inst._cvpysdk_object.make_request.return_value = (True, mock_response)

        with pytest.raises(SDKException):
            inst.configure_live_sync({"key": "val"})

    def test_configure_live_sync_empty_response_raises(self):
        inst = self._make_instance()
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        inst._cvpysdk_object.make_request.return_value = (True, mock_response)

        with pytest.raises(SDKException):
            inst.configure_live_sync({"key": "val"})

    def test_configure_live_sync_flag_false_raises(self):
        inst = self._make_instance()
        mock_response = MagicMock()
        mock_response.text = "error text"
        inst._cvpysdk_object.make_request.return_value = (False, mock_response)

        with pytest.raises(SDKException):
            inst.configure_live_sync({"key": "val"})
