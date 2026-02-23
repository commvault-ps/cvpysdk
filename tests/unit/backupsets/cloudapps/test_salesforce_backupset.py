"""Tests for cvpysdk/backupsets/cloudapps/salesforce_backupset.py."""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.backupsets.cabackupset import CloudAppsBackupset
from cvpysdk.backupsets.cloudapps.salesforce_backupset import (
    SalesforceBackupset,
)


@pytest.mark.unit
class TestSalesforceBackupsetInheritance:
    def test_inherits_cloud_apps_backupset(self):
        assert issubclass(SalesforceBackupset, CloudAppsBackupset)

    def test_has_download_cache_path_property(self):
        assert isinstance(SalesforceBackupset.__dict__.get("download_cache_path"), property)

    def test_has_mutual_auth_path_property(self):
        assert isinstance(SalesforceBackupset.__dict__.get("mutual_auth_path"), property)

    def test_has_salesforce_user_name_property(self):
        assert isinstance(SalesforceBackupset.__dict__.get("salesforce_user_name"), property)

    def test_has_is_sync_db_enabled_property(self):
        assert isinstance(SalesforceBackupset.__dict__.get("is_sync_db_enabled"), property)

    def test_has_sync_db_type_property(self):
        assert isinstance(SalesforceBackupset.__dict__.get("sync_db_type"), property)


@pytest.mark.unit
class TestSalesforceBackupsetPropertyGetters:
    def _make_instance(self):
        inst = object.__new__(SalesforceBackupset)
        inst._download_cache_path = "/cache/path"
        inst._mutual_auth_path = "/mutual/auth"
        inst._user_name = "sf_user@example.com"
        inst._sync_db_enabled = True
        inst._sync_db_type = 1
        inst._sync_db_host = "db.example.com"
        inst._sync_db_instance = "inst1"
        inst._sync_db_name = "syncdb"
        inst._sync_db_port = 5432
        inst._sync_db_user_name = "db_user"
        return inst

    def test_download_cache_path(self):
        inst = self._make_instance()
        assert inst.download_cache_path == "/cache/path"

    def test_mutual_auth_path(self):
        inst = self._make_instance()
        assert inst.mutual_auth_path == "/mutual/auth"

    def test_salesforce_user_name(self):
        inst = self._make_instance()
        assert inst.salesforce_user_name == "sf_user@example.com"

    def test_is_sync_db_enabled(self):
        inst = self._make_instance()
        assert inst.is_sync_db_enabled is True

    def test_sync_db_type(self):
        inst = self._make_instance()
        assert inst.sync_db_type == 1

    def test_sync_db_host(self):
        inst = self._make_instance()
        assert inst.sync_db_host == "db.example.com"

    def test_sync_db_instance(self):
        inst = self._make_instance()
        assert inst.sync_db_instance == "inst1"

    def test_sync_db_name(self):
        inst = self._make_instance()
        assert inst.sync_db_name == "syncdb"

    def test_sync_db_port(self):
        inst = self._make_instance()
        assert inst.sync_db_port == 5432

    def test_sync_db_user_name(self):
        inst = self._make_instance()
        assert inst.sync_db_user_name == "db_user"


@pytest.mark.unit
class TestSalesforceBackupsetGetProperties:
    def _make_instance(self):
        inst = object.__new__(SalesforceBackupset)
        inst._download_cache_path = None
        inst._mutual_auth_path = None
        inst._user_name = None
        inst._api_token = None
        inst._sync_db_enabled = None
        inst._sync_db_type = None
        inst._sync_db_host = None
        inst._sync_db_instance = None
        inst._sync_db_name = None
        inst._sync_db_port = None
        inst._sync_db_user_name = None
        inst._sync_db_user_password = None
        return inst

    def test_get_backupset_properties_with_full_sf_data(self):
        inst = self._make_instance()
        inst._properties = {
            "cloudAppsBackupset": {
                "salesforceBackupSet": {
                    "downloadCachePath": "/cache",
                    "mutualAuthPath": "/auth",
                    "userPassword": {"userName": "user@sf.com"},
                    "syncDatabase": {
                        "dbEnabled": True,
                        "dbType": 2,
                        "dbHost": "host1",
                        "dbInstance": "inst1",
                        "dbName": "mydb",
                        "dbPort": 3306,
                        "dbUserPassword": {
                            "userName": "dbuser",
                            "password": "dbpass",
                        },
                    },
                }
            }
        }

        # Call _get_backupset_properties with parent mocked
        with patch.object(CloudAppsBackupset, "_get_backupset_properties"):
            inst._get_backupset_properties()

        assert inst._download_cache_path == "/cache"
        assert inst._mutual_auth_path == "/auth"
        assert inst._user_name == "user@sf.com"
        assert inst._sync_db_enabled is True
        assert inst._sync_db_type == 2
        assert inst._sync_db_host == "host1"
        assert inst._sync_db_name == "mydb"
        assert inst._sync_db_port == 3306
        assert inst._sync_db_user_name == "dbuser"

    def test_get_backupset_properties_without_cloud_apps(self):
        inst = self._make_instance()
        inst._properties = {}

        with patch.object(CloudAppsBackupset, "_get_backupset_properties"):
            inst._get_backupset_properties()

        assert inst._download_cache_path is None
        assert inst._sync_db_enabled is None


@pytest.mark.unit
class TestSalesforceBackupsetPrepareBrowseJson:
    def _make_instance(self):
        inst = object.__new__(SalesforceBackupset)
        return inst

    def test_prepare_browse_json_adds_view_name_list(self):
        inst = self._make_instance()
        options = {"_browse_view_name_list": ["TBLVIEW", "FILEVIEW"]}

        with patch.object(
            CloudAppsBackupset,
            "_prepare_browse_json",
            return_value={"advOptions": {}},
        ):
            result = inst._prepare_browse_json(options)
            assert result["advOptions"]["browseViewNameList"] == [
                "TBLVIEW",
                "FILEVIEW",
            ]


@pytest.mark.unit
class TestSalesforceBackupsetMutualAuthSetter:
    def _make_instance(self):
        inst = object.__new__(SalesforceBackupset)
        inst._mutual_auth_path = "/old/path"
        inst._sync_db_enabled = False
        inst._properties = {
            "cloudAppsBackupset": {
                "salesforceBackupSet": {
                    "mutualAuthPath": "/old/path",
                }
            }
        }
        inst.update_properties = MagicMock()
        return inst

    def test_mutual_auth_path_setter_updates_when_different(self):
        inst = self._make_instance()
        inst.mutual_auth_path = "/new/path"
        assert (
            inst._properties["cloudAppsBackupset"]["salesforceBackupSet"]["mutualAuthPath"]
            == "/new/path"
        )
        inst.update_properties.assert_called_once()

    def test_mutual_auth_path_setter_no_op_when_same(self):
        inst = self._make_instance()
        inst.mutual_auth_path = "/old/path"
        inst.update_properties.assert_not_called()
