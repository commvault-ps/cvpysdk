"""Unit tests for cvpysdk/instances/lotusnotes/lninstance.py"""

from unittest.mock import MagicMock, PropertyMock, patch

import pytest

from cvpysdk.instance import Instance


@pytest.mark.unit
class TestLNInstance:
    """Tests for the LNInstance class."""

    def test_inherits_instance(self):
        """Test that LNInstance is a subclass of Instance."""
        from cvpysdk.instances.lotusnotes.lninstance import LNInstance

        assert issubclass(LNInstance, Instance)

    def test_restore_in_place_calls_process_restore(self):
        """Test restore_in_place calls _process_restore_response."""
        from cvpysdk.instances.lotusnotes.lninstance import LNInstance

        inst = object.__new__(LNInstance)
        mock_backupset = MagicMock()
        mock_backupset._backupset_association = {"key": "val"}
        mock_backupsets = MagicMock()
        mock_backupsets.all_backupsets = {"bs1": {"id": 1}}
        mock_backupsets.get.return_value = mock_backupset

        mock_json = {"taskInfo": {"subTasks": [{"options": {"restoreOptions": {}}}]}}
        inst._restore_json = MagicMock(return_value=mock_json)
        inst._process_restore_response = MagicMock(return_value="job")

        with patch.object(type(inst), "backupsets", new_callable=PropertyMock) as mock_bs:
            mock_bs.return_value = mock_backupsets
            result = inst.restore_in_place(paths=["/path"])
        assert result == "job"
        inst._process_restore_response.assert_called_once()

    def test_restore_out_of_place_calls_process_restore(self):
        """Test restore_out_of_place calls _process_restore_response."""
        from cvpysdk.instances.lotusnotes.lninstance import LNInstance

        inst = object.__new__(LNInstance)
        mock_backupset = MagicMock()
        mock_backupset._backupset_association = {"key": "val"}
        mock_backupsets = MagicMock()
        mock_backupsets.all_backupsets = {"bs1": {"id": 1}}
        mock_backupsets.get.return_value = mock_backupset

        mock_json = {"taskInfo": {"subTasks": [{"options": {"restoreOptions": {}}}]}}
        inst._restore_json = MagicMock(return_value=mock_json)
        inst._process_restore_response = MagicMock(return_value="job")

        with patch.object(type(inst), "backupsets", new_callable=PropertyMock) as mock_bs:
            mock_bs.return_value = mock_backupsets
            result = inst.restore_out_of_place(
                client="client1", destination_path="/dest", paths=["/path"]
            )
        assert result == "job"
        inst._process_restore_response.assert_called_once()

    def test_restore_in_place_sets_restore_association(self):
        """Test restore_in_place sets _restore_association from backupsets."""
        from cvpysdk.instances.lotusnotes.lninstance import LNInstance

        inst = object.__new__(LNInstance)
        assoc = {"clientName": "c1", "backupsetName": "bs1"}
        mock_backupset = MagicMock()
        mock_backupset._backupset_association = assoc
        mock_backupsets = MagicMock()
        mock_backupsets.all_backupsets = {"bs1": {"id": 1}}
        mock_backupsets.get.return_value = mock_backupset

        inst._restore_json = MagicMock(return_value={})
        inst._process_restore_response = MagicMock(return_value="job")

        with patch.object(type(inst), "backupsets", new_callable=PropertyMock) as mock_bs:
            mock_bs.return_value = mock_backupsets
            inst.restore_in_place(paths=["/path"])
        assert inst._restore_association == assoc
