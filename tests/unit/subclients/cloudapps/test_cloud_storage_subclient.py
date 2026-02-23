"""Unit tests for cvpysdk/subclients/cloudapps/cloud_storage_subclient.py"""

from unittest.mock import MagicMock

import pytest

from cvpysdk.subclients.casubclient import CloudAppsSubclient
from cvpysdk.subclients.cloudapps.cloud_storage_subclient import CloudStorageSubclient


@pytest.mark.unit
class TestCloudStorageSubclient:
    """Tests for the CloudStorageSubclient class."""

    def test_inherits_cloud_apps_subclient(self):
        """CloudStorageSubclient should inherit from CloudAppsSubclient."""
        assert issubclass(CloudStorageSubclient, CloudAppsSubclient)

    def test_has_key_methods(self):
        """CloudStorageSubclient should have expected methods."""
        assert hasattr(CloudStorageSubclient, "content")
        assert hasattr(CloudStorageSubclient, "_set_content")
        assert hasattr(CloudStorageSubclient, "restore_in_place")
        assert hasattr(CloudStorageSubclient, "restore_out_of_place")
        assert hasattr(CloudStorageSubclient, "restore_to_fs")

    def test_set_content_creates_path_dicts(self):
        """_set_content should create list of path dicts."""
        sub = object.__new__(CloudStorageSubclient)
        sub._set_subclient_properties = MagicMock()
        sub._set_content(content=["bucket1/path1", "bucket2/path2"])
        call_args = sub._set_subclient_properties.call_args
        assert call_args[0][0] == "_content"
        content_list = call_args[0][1]
        assert len(content_list) == 2
        assert content_list[0] == {"path": "bucket1/path1"}
        assert content_list[1] == {"path": "bucket2/path2"}

    def test_get_subclient_properties_json_structure(self):
        """_get_subclient_properties_json should return proper dict."""
        sub = object.__new__(CloudStorageSubclient)
        sub._proxyClient = {"clientName": "proxy"}
        sub._subClientEntity = {"subclientId": 1}
        sub._commonProperties = {"prop": "val"}
        sub._content = [{"path": "/bucket"}]
        sub._backupset_object = MagicMock()
        sub._backupset_object._instance_object.ca_instance_type = 3
        result = sub._get_subclient_properties_json()
        assert "subClientProperties" in result
        props = result["subClientProperties"]
        assert props["contentOperationType"] == 1
        assert "cloudAppsSubClientProp" in props
