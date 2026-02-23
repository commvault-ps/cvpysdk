"""Unit tests for cvpysdk/instances/lotusnotes/lndbinstance.py"""

from unittest.mock import MagicMock, PropertyMock, patch

import pytest

from cvpysdk.instances.lotusnotes.lninstance import LNInstance


@pytest.mark.unit
class TestLNDBInstanceLotusNotes:
    """Tests for the LNDBInstance class in lotusnotes subpackage."""

    def test_inherits_lninstance(self):
        """Test that LNDBInstance is a subclass of LNInstance."""
        from cvpysdk.instances.lotusnotes.lndbinstance import LNDBInstance

        assert issubclass(LNDBInstance, LNInstance)

    def test_restore_common_options_json_raises_for_non_dict(self):
        """Test _restore_common_options_json raises SDKException for non-dict."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.lotusnotes.lndbinstance import LNDBInstance

        inst = object.__new__(LNDBInstance)
        with pytest.raises(SDKException):
            inst._restore_common_options_json("not_a_dict")

    def test_restore_common_options_json_sets_values(self):
        """Test _restore_common_options_json sets values from dict."""
        from cvpysdk.instances.lotusnotes.lndbinstance import LNDBInstance

        inst = object.__new__(LNDBInstance)
        value = {
            "common_options_dict": {
                "doNotReplayTransactLogs": True,
                "recoverWait": True,
                "recoverZap": False,
            }
        }
        inst._restore_common_options_json(value)
        assert inst._commonoption_restore_json["doNotReplayTransactLogs"] is True
        assert inst._commonoption_restore_json["recoverWait"] is True
        assert inst._commonoption_restore_json["recoverZap"] is False

    def test_restore_common_options_json_disaster_recovery(self):
        """Test _restore_common_options_json adds disaster recovery keys."""
        from cvpysdk.instances.lotusnotes.lndbinstance import LNDBInstance

        inst = object.__new__(LNDBInstance)
        value = {
            "common_options_dict": {
                "disasterRecovery": True,
                "skipErrorsAndContinue": True,
            }
        }
        inst._restore_common_options_json(value)
        assert inst._commonoption_restore_json["disasterRecovery"] is True
        assert inst._commonoption_restore_json["skipErrorsAndContinue"] is True

    def test_restore_in_place_delegates_to_super(self):
        """Test restore_in_place delegates to parent class."""
        from cvpysdk.instances.lotusnotes.lndbinstance import LNDBInstance

        inst = object.__new__(LNDBInstance)
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
            result = inst.restore_in_place(
                paths=["/path"],
                common_options_dict={"recoverWait": False},
                lndb_restore_options={"disableReplication": False},
            )
        assert result == "job"
