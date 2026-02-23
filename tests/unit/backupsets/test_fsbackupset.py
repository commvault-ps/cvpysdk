"""Tests for cvpysdk/backupsets/fsbackupset.py (FSBackupset)."""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.backupset import Backupset
from cvpysdk.backupsets.fsbackupset import FSBackupset
from cvpysdk.exception import SDKException


@pytest.mark.unit
class TestFSBackupsetInheritance:
    def test_inherits_backupset(self):
        assert issubclass(FSBackupset, Backupset)

    def test_has_restore_in_place(self):
        assert hasattr(FSBackupset, "restore_in_place")

    def test_has_restore_out_of_place(self):
        assert hasattr(FSBackupset, "restore_out_of_place")

    def test_has_find_all_versions(self):
        assert hasattr(FSBackupset, "find_all_versions")

    def test_has_index_server_property(self):
        assert isinstance(FSBackupset.__dict__.get("index_server"), property)

    def test_has_index_pruning_type_property(self):
        assert isinstance(FSBackupset.__dict__.get("index_pruning_type"), property)


@pytest.mark.unit
class TestFSBackupsetRestoreInPlace:
    def _make_instance(self):
        inst = object.__new__(FSBackupset)
        inst._instance_object = MagicMock()
        inst._backupset_association = {"backupsetId": 1}
        inst._client_object = MagicMock()
        return inst

    def test_restore_in_place_delegates_to_instance(self):
        inst = self._make_instance()
        paths = ["/data/file1.txt"]
        inst.restore_in_place(paths)
        inst._instance_object._restore_in_place.assert_called_once()

    def test_restore_in_place_sets_association(self):
        inst = self._make_instance()
        inst.restore_in_place(["/data"])
        assert inst._instance_object._restore_association == inst._backupset_association

    def test_restore_in_place_with_fs_options_multistream(self):
        inst = self._make_instance()
        inst._client_object.agents.all_agents = {"file system": 33}
        fs_options = {"no_of_streams": 2}

        inst.restore_in_place(["/data"], fs_options=fs_options)
        assert fs_options["destination_appTypeId"] == 33


@pytest.mark.unit
class TestFSBackupsetRestoreOutOfPlace:
    def _make_instance(self):
        inst = object.__new__(FSBackupset)
        inst._instance_object = MagicMock()
        inst._backupset_association = {"backupsetId": 1}
        inst._commcell_object = MagicMock()
        return inst

    def test_raises_for_invalid_client_type(self):
        inst = self._make_instance()
        with pytest.raises(SDKException):
            inst.restore_out_of_place(
                client=123,
                destination_path="/dest",
                paths=["/data"],
            )

    @patch("cvpysdk.backupsets.fsbackupset.Client")
    def test_accepts_string_client_name(self, mock_client_cls):
        inst = self._make_instance()
        mock_client_inst = MagicMock()
        mock_client_cls.return_value = mock_client_inst

        inst.restore_out_of_place(
            client="test_client",
            destination_path="/dest",
            paths=["/data"],
        )
        mock_client_cls.assert_called_once_with(inst._commcell_object, "test_client")
        inst._instance_object._restore_out_of_place.assert_called_once()


@pytest.mark.unit
class TestFSBackupsetFindAllVersions:
    def _make_instance(self):
        inst = object.__new__(FSBackupset)
        inst._do_browse = MagicMock(return_value=(["path1"], {"path1": {}}))
        return inst

    def test_find_all_versions_sets_operation(self):
        inst = self._make_instance()
        inst.find_all_versions(path="c:\\hello")
        call_args = inst._do_browse.call_args[0][0]
        assert call_args["operation"] == "all_versions"

    def test_find_all_versions_with_dict_arg(self):
        inst = self._make_instance()
        inst.find_all_versions({"path": "c:\\hello", "show_deleted": True})
        call_args = inst._do_browse.call_args[0][0]
        assert call_args["operation"] == "all_versions"
        assert call_args["show_deleted"] is True


@pytest.mark.unit
class TestFSBackupsetIndexProperties:
    def _make_instance(self):
        inst = object.__new__(FSBackupset)
        inst._properties = {
            "indexSettings": {
                "indexPruningType": 1,
                "indexRetDays": 30,
                "indexRetCycles": 5,
            }
        }
        inst._process_update_reponse = MagicMock()
        inst._commcell_object = MagicMock()
        return inst

    def test_index_pruning_type_getter(self):
        inst = self._make_instance()
        assert inst.index_pruning_type == 1

    def test_index_pruning_days_retention_getter(self):
        inst = self._make_instance()
        assert inst.index_pruning_days_retention == 30

    def test_index_pruning_cycles_retention_getter(self):
        inst = self._make_instance()
        assert inst.index_pruning_cycles_retention == 5

    def test_index_pruning_type_setter_cycles(self):
        inst = self._make_instance()
        inst.index_pruning_type = "cycles_based"
        inst._process_update_reponse.assert_called_once()
        call_json = inst._process_update_reponse.call_args[0][0]
        assert call_json["backupsetProperties"]["indexSettings"]["indexPruningType"] == 1

    def test_index_pruning_type_setter_days(self):
        inst = self._make_instance()
        inst.index_pruning_type = "days_based"
        call_json = inst._process_update_reponse.call_args[0][0]
        assert call_json["backupsetProperties"]["indexSettings"]["indexPruningType"] == 2

    def test_index_pruning_type_setter_invalid_raises(self):
        inst = self._make_instance()
        with pytest.raises(SDKException):
            inst.index_pruning_type = "invalid_value"

    def test_index_pruning_days_setter_valid(self):
        inst = self._make_instance()
        inst.index_pruning_days_retention = 10
        inst._process_update_reponse.assert_called_once()

    def test_index_pruning_days_setter_too_low_raises(self):
        inst = self._make_instance()
        with pytest.raises(SDKException):
            inst.index_pruning_days_retention = 1

    def test_index_pruning_cycles_setter_valid(self):
        inst = self._make_instance()
        inst.index_pruning_cycles_retention = 3
        inst._process_update_reponse.assert_called_once()

    def test_index_pruning_cycles_setter_too_low_raises(self):
        inst = self._make_instance()
        with pytest.raises(SDKException):
            inst.index_pruning_cycles_retention = 0
