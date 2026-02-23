"""Unit tests for cvpysdk/subclients/hanasubclient.py"""

from unittest.mock import MagicMock

import pytest

from cvpysdk.subclients.dbsubclient import DatabaseSubclient
from cvpysdk.subclients.hanasubclient import SAPHANASubclient


@pytest.mark.unit
class TestSAPHANASubclient:
    """Tests for the SAPHANASubclient class."""

    def test_inherits_database_subclient(self):
        """SAPHANASubclient should inherit from DatabaseSubclient."""
        assert issubclass(SAPHANASubclient, DatabaseSubclient)

    def test_has_key_methods(self):
        """SAPHANASubclient should have expected methods."""
        assert hasattr(SAPHANASubclient, "_backup_request_json")
        assert hasattr(SAPHANASubclient, "_get_subclient_properties")
        assert hasattr(SAPHANASubclient, "content")

    def test_backup_request_json_structure(self):
        """_backup_request_json should include hanaOptions with backupPrefix."""
        subclient = object.__new__(SAPHANASubclient)
        subclient._backup_json = MagicMock(
            return_value={"taskInfo": {"subTasks": [{"options": {"backupOpts": {}}}]}}
        )

        result = subclient._backup_request_json("full", backup_prefix="test_prefix")
        assert (
            result["taskInfo"]["subTasks"][0]["options"]["backupOpts"]["hanaOptions"][
                "backupPrefix"
            ]
            == "test_prefix"
        )

    def test_content_property(self):
        """content property should return stored content."""
        subclient = object.__new__(SAPHANASubclient)
        subclient._content = [{"path": "/test"}]
        assert subclient.content == [{"path": "/test"}]
