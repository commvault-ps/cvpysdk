"""Unit tests for cvpysdk/subclients/bigdataappssubclient.py"""

from unittest.mock import MagicMock

import pytest

from cvpysdk.subclients.bigdataappssubclient import BigDataAppsSubclient
from cvpysdk.subclients.fssubclient import FileSystemSubclient


@pytest.mark.unit
class TestBigDataAppsSubclient:
    """Tests for the BigDataAppsSubclient class."""

    def test_inherits_filesystem_subclient(self):
        """BigDataAppsSubclient should inherit from FileSystemSubclient."""
        assert issubclass(BigDataAppsSubclient, FileSystemSubclient)

    def test_has_key_methods(self):
        """BigDataAppsSubclient should have expected methods."""
        assert hasattr(BigDataAppsSubclient, "set_data_access_nodes")
        assert hasattr(BigDataAppsSubclient, "__new__")

    def test_new_returns_splunk_for_cluster_type_16(self):
        """__new__ should return SplunkSubclient for cluster type 16."""
        from cvpysdk.subclients.splunksubclient import SplunkSubclient

        backupset_obj = MagicMock()
        backupset_obj._instance_object.properties = {
            "distributedClusterInstance": {"clusterType": 16}
        }
        result = BigDataAppsSubclient.__new__(
            BigDataAppsSubclient, backupset_obj, "test_subclient"
        )
        assert isinstance(result, SplunkSubclient)

    def test_new_returns_index_server_for_cluster_type_6(self):
        """__new__ should return IndexServerSubclient for cluster type 6."""
        from cvpysdk.subclients.index_server_subclient import IndexServerSubclient

        backupset_obj = MagicMock()
        backupset_obj._instance_object.properties = {
            "distributedClusterInstance": {"clusterType": 6}
        }
        result = BigDataAppsSubclient.__new__(
            BigDataAppsSubclient, backupset_obj, "test_subclient"
        )
        assert isinstance(result, IndexServerSubclient)

    def test_new_returns_self_for_unknown_cluster_type(self):
        """__new__ should return BigDataAppsSubclient for unknown cluster types."""
        backupset_obj = MagicMock()
        backupset_obj._instance_object.properties = {
            "distributedClusterInstance": {"clusterType": 99}
        }
        result = BigDataAppsSubclient.__new__(
            BigDataAppsSubclient, backupset_obj, "test_subclient"
        )
        assert type(result) is BigDataAppsSubclient

    def test_new_returns_self_when_no_cluster_type(self):
        """__new__ should return BigDataAppsSubclient when no clusterType key."""
        backupset_obj = MagicMock()
        backupset_obj._instance_object.properties = {"distributedClusterInstance": {}}
        result = BigDataAppsSubclient.__new__(
            BigDataAppsSubclient, backupset_obj, "test_subclient"
        )
        assert type(result) is BigDataAppsSubclient
