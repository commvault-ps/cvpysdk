"""Unit tests for cvpysdk/subclients/dbsubclient.py"""

import pytest

from cvpysdk.subclient import Subclient
from cvpysdk.subclients.dbsubclient import DatabaseSubclient


@pytest.mark.unit
class TestDatabaseSubclient:
    """Tests for the DatabaseSubclient class."""

    def test_inherits_subclient(self):
        """DatabaseSubclient should inherit from Subclient."""
        assert issubclass(DatabaseSubclient, Subclient)

    def test_has_log_backup_storage_policy(self):
        """DatabaseSubclient should have log_backup_storage_policy property."""
        assert hasattr(DatabaseSubclient, "log_backup_storage_policy")

    def test_log_backup_storage_policy_returns_name(self):
        """log_backup_storage_policy should return storage policy name."""
        subclient = object.__new__(DatabaseSubclient)
        subclient._subclient_properties = {
            "commonProperties": {
                "storageDevice": {"logBackupStoragePolicy": {"storagePolicyName": "test_policy"}}
            }
        }
        assert subclient.log_backup_storage_policy == "test_policy"

    def test_log_backup_storage_policy_returns_none_when_absent(self):
        """log_backup_storage_policy should return None when no log backup policy."""
        subclient = object.__new__(DatabaseSubclient)
        subclient._subclient_properties = {"commonProperties": {"storageDevice": {}}}
        assert subclient.log_backup_storage_policy is None

    def test_log_backup_storage_policy_setter_raises_for_non_string(self):
        """log_backup_storage_policy setter should raise SDKException for non-string."""
        from cvpysdk.exception import SDKException

        subclient = object.__new__(DatabaseSubclient)
        with pytest.raises(SDKException):
            subclient.log_backup_storage_policy = 123
