"""Unit tests for cvpysdk/instances/lotusnotes/lndocinstance.py"""

from unittest.mock import MagicMock, PropertyMock, patch

import pytest

from cvpysdk.instances.lotusnotes.lninstance import LNInstance


@pytest.mark.unit
class TestLNDOCInstance:
    """Tests for the LNDOCInstance class."""

    def test_inherits_lninstance(self):
        """Test that LNDOCInstance is a subclass of LNInstance."""
        from cvpysdk.instances.lotusnotes.lndocinstance import LNDOCInstance

        assert issubclass(LNDOCInstance, LNInstance)

    def test_restore_common_options_json_raises_for_non_dict(self):
        """Test _restore_common_options_json raises SDKException for non-dict."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.lotusnotes.lndocinstance import LNDOCInstance

        inst = object.__new__(LNDOCInstance)
        with pytest.raises(SDKException):
            inst._restore_common_options_json("not_a_dict")

    def test_restore_common_options_json_sets_values(self):
        """Test _restore_common_options_json sets expected keys."""
        from cvpysdk.instances.lotusnotes.lndocinstance import LNDOCInstance

        inst = object.__new__(LNDOCInstance)
        value = {
            "common_options_dict": {
                "overwriteDBLinks": True,
                "overwriteDesignDoc": True,
                "overwriteDataDoc": False,
                "dbLinksOnly": False,
            }
        }
        inst._restore_common_options_json(value)
        result = inst._commonoption_restore_json
        assert result["overwriteDBLinks"] is True
        assert result["overwriteDesignDoc"] is True
        assert result["overwriteDataDoc"] is False
        assert result["dbLinksOnly"] is False

    def test_restore_common_options_json_defaults(self):
        """Test _restore_common_options_json uses defaults for missing keys."""
        from cvpysdk.instances.lotusnotes.lndocinstance import LNDOCInstance

        inst = object.__new__(LNDOCInstance)
        value = {"common_options_dict": {}}
        inst._restore_common_options_json(value)
        result = inst._commonoption_restore_json
        assert result["overwriteDBLinks"] is False
        assert result["overwriteDesignDoc"] is False
        assert result["overwriteDataDoc"] is False
        assert result["dbLinksOnly"] is False
        assert result["onePassRestore"] is False

    def test_restore_in_place_delegates_to_super(self):
        """Test restore_in_place delegates to parent class."""
        from cvpysdk.instances.lotusnotes.lndocinstance import LNDOCInstance

        inst = object.__new__(LNDOCInstance)
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
