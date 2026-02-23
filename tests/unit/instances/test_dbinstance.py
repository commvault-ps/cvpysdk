"""Unit tests for cvpysdk/instances/dbinstance.py"""

from unittest.mock import MagicMock

import pytest

from cvpysdk.instance import Instance


@pytest.mark.unit
class TestDatabaseInstance:
    """Tests for the DatabaseInstance class."""

    def test_inherits_instance(self):
        """Test that DatabaseInstance is a subclass of Instance."""
        from cvpysdk.instances.dbinstance import DatabaseInstance

        assert issubclass(DatabaseInstance, Instance)

    def test_get_source_item_app_free(self):
        """Test _get_source_item_app_free returns formatted source items."""
        from cvpysdk.instances.dbinstance import DatabaseInstance

        inst = object.__new__(DatabaseInstance)
        inst._commcell_object = MagicMock()
        inst._commcell_object.commcell_id = 2

        result = inst._get_source_item_app_free([100, 200, 300])
        assert result == ["2:100", "2:200", "2:300"]

    def test_get_source_item_app_free_empty_list(self):
        """Test _get_source_item_app_free with empty job IDs list."""
        from cvpysdk.instances.dbinstance import DatabaseInstance

        inst = object.__new__(DatabaseInstance)
        inst._commcell_object = MagicMock()
        inst._commcell_object.commcell_id = 5

        result = inst._get_source_item_app_free([])
        assert result == []

    def test_get_restore_to_disk_json(self):
        """Test _get_restore_to_disk_json constructs correct JSON."""
        from cvpysdk.instances.dbinstance import DatabaseInstance

        inst = object.__new__(DatabaseInstance)
        inst._commcell_object = MagicMock()
        inst._commcell_object.commcell_id = 2

        mock_json = {
            "taskInfo": {
                "subTasks": [
                    {
                        "options": {
                            "restoreOptions": {
                                "fileOption": {"sourceItem": []},
                                "jobIds": [],
                            }
                        }
                    }
                ]
            }
        }
        inst._restore_json = MagicMock(return_value=mock_json)

        result = inst._get_restore_to_disk_json(
            "dest_client", "/dest/path", [101, 102], "user1", "pass1"
        )

        restore_opts = result["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]
        assert restore_opts["jobIds"] == [101, 102]
        assert restore_opts["fileOption"]["sourceItem"] == ["2:101", "2:102"]
