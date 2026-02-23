"""Tests for cvpysdk/backupsets/adbackupset.py (ADBackupset)."""

from unittest.mock import MagicMock

import pytest

from cvpysdk.backupset import Backupset
from cvpysdk.backupsets.adbackupset import ADBackupset
from cvpysdk.exception import SDKException


@pytest.mark.unit
class TestADBackupsetInheritance:
    def test_inherits_backupset(self):
        assert issubclass(ADBackupset, Backupset)

    def test_has_check_subclient_method(self):
        assert hasattr(ADBackupset, "check_subclient")


@pytest.mark.unit
class TestADBackupsetCheckSubclient:
    def _make_instance(self):
        return object.__new__(ADBackupset)

    def test_returns_existing_subclient_without_delete(self):
        inst = self._make_instance()
        mock_backupset = MagicMock()
        mock_subclient = MagicMock()
        mock_backupset.subclients.has_subclient.return_value = True
        mock_backupset.subclients.get.return_value = mock_subclient

        result = inst.check_subclient(mock_backupset, "test_sc", deleteexist=False)
        assert result == mock_subclient
        mock_backupset.delete.assert_not_called()

    def test_deletes_existing_subclient_when_deleteexist_true(self):
        inst = self._make_instance()
        mock_backupset = MagicMock()
        mock_subclient = MagicMock()
        mock_backupset.subclients.has_subclient.return_value = True
        mock_backupset.subclients.get.return_value = mock_subclient

        inst.check_subclient(mock_backupset, "test_sc", deleteexist=True)
        mock_backupset.delete.assert_called_once_with("test_sc")

    def test_creates_new_subclient_with_storage_policy(self):
        inst = self._make_instance()
        mock_backupset = MagicMock()
        mock_backupset.subclients.has_subclient.return_value = False
        new_sc = MagicMock()
        mock_backupset.subclients.get.return_value = new_sc

        inst.check_subclient(
            mock_backupset,
            "new_sc",
            storagepolicy="pol1",
            subclientcontent=["OU=test,DC=domain"],
        )
        mock_backupset.subclients.add.assert_called_once_with("new_sc", "pol1")

    def test_raises_when_no_storage_policy_for_new_subclient(self):
        inst = self._make_instance()
        mock_backupset = MagicMock()
        mock_backupset.subclients.has_subclient.return_value = False

        with pytest.raises(SDKException):
            inst.check_subclient(mock_backupset, "new_sc")

    def test_sets_content_on_new_subclient(self):
        inst = self._make_instance()
        mock_backupset = MagicMock()
        mock_backupset.subclients.has_subclient.return_value = False
        new_sc = MagicMock()
        mock_backupset.subclients.get.return_value = new_sc

        content_entries = ["OU=Users,DC=test", "OU=Groups,DC=test"]
        inst.check_subclient(
            mock_backupset,
            "new_sc",
            storagepolicy="pol1",
            subclientcontent=content_entries,
        )
        new_sc._set_subclient_properties.assert_called_once()
        call_args = new_sc._set_subclient_properties.call_args
        assert call_args[0][0] == "content"
        content_list = call_args[0][1]
        assert len(content_list) == 2
        assert content_list[0]["path"] == ",OU=Users,DC=test"
        assert content_list[1]["path"] == ",OU=Groups,DC=test"
