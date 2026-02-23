"""Tests for cvpysdk/backupsets/aadbackupset.py (AzureAdBackupset)."""

import pytest

from cvpysdk.backupset import Backupset
from cvpysdk.backupsets.aadbackupset import AzureAdBackupset


@pytest.mark.unit
class TestAzureAdBackupsetInheritance:
    def test_inherits_backupset(self):
        assert issubclass(AzureAdBackupset, Backupset)

    def test_has_browse_method(self):
        assert hasattr(AzureAdBackupset, "browse")

    def test_has_process_browse_response(self):
        assert hasattr(AzureAdBackupset, "_process_browse_response")

    def test_has_get_search_response(self):
        assert hasattr(AzureAdBackupset, "get_search_response")

    def test_has_view_attributes_url_builder(self):
        assert hasattr(AzureAdBackupset, "view_attributes_url_builder")

    def test_has_get_view_attribute_response(self):
        assert hasattr(AzureAdBackupset, "get_view_attribute_response")


@pytest.mark.unit
class TestAzureAdBackupsetBrowseOptionsBuilder:
    def _make_instance(self):
        inst = object.__new__(AzureAdBackupset)
        return inst

    def test_adds_default_filters_when_missing(self):
        inst = self._make_instance()
        options = {}
        result = inst.azuread_browse_options_builder(options)
        assert "filters" in result
        assert len(result["filters"]) == 2

    def test_preserves_existing_filters(self):
        inst = self._make_instance()
        custom_filters = [("76", "abc", "9")]
        options = {"filters": custom_filters}
        result = inst.azuread_browse_options_builder(options)
        assert result["filters"] is custom_filters

    def test_adds_default_operation_when_missing(self):
        inst = self._make_instance()
        options = {}
        result = inst.azuread_browse_options_builder(options)
        assert result["operation"] == "browse"
        assert result["page_size"] == 20
        assert result["skip_node"] == 0

    def test_preserves_existing_operation(self):
        inst = self._make_instance()
        options = {"operation": "search"}
        result = inst.azuread_browse_options_builder(options)
        assert result["operation"] == "search"


@pytest.mark.unit
class TestAzureAdBackupsetDoubleQuery:
    def _make_instance(self):
        inst = object.__new__(AzureAdBackupset)
        return inst

    def test_creates_two_queries(self):
        inst = self._make_instance()
        options = {"page_size": 20, "skip_node": 0, "filters": []}
        request_json = {"paths": ["/some/path"]}
        result = inst.azuread_browse_double_query(options, request_json)
        assert len(result["queries"]) == 2
        assert result["queries"][0]["type"] == "0"
        assert result["queries"][1]["type"] == "1"

    def test_removes_paths_from_request(self):
        inst = self._make_instance()
        options = {"page_size": 10, "skip_node": 0, "filters": []}
        request_json = {"paths": ["/some/path"]}
        result = inst.azuread_browse_double_query(options, request_json)
        assert "paths" not in result

    def test_adds_filters_to_where_clause(self):
        inst = self._make_instance()
        filters = [("76", "someid", "9")]
        options = {"page_size": 20, "skip_node": 0, "filters": filters}
        request_json = {"paths": []}
        result = inst.azuread_browse_double_query(options, request_json)
        assert len(result["queries"][0]["whereClause"]) == 1
        assert result["queries"][0]["whereClause"][0]["criteria"]["field"] == "76"

    def test_filter_with_field_125_removes_connector(self):
        inst = self._make_instance()
        filters = [("125", "USER")]
        options = {"page_size": 20, "skip_node": 0, "filters": filters}
        request_json = {"paths": []}
        result = inst.azuread_browse_double_query(options, request_json)
        clause = result["queries"][0]["whereClause"][0]
        assert "connector" not in clause


@pytest.mark.unit
class TestAzureAdBackupsetMetadata:
    def _make_instance(self):
        inst = object.__new__(AzureAdBackupset)
        return inst

    def test_azuread_get_metadata_success(self):
        inst = self._make_instance()
        result_data = {
            "advancedData": {
                "objectGuid": "guid-123",
                "browseMetaData": {
                    "azureADDataV2": {"someKey": "someVal"},
                },
            }
        }
        metadata = inst.azuread_get_metadata(result_data)
        assert "azureADDataV2" in metadata
        assert metadata["azureADDataV2"]["guid"] == "guid-123"

    def test_azuread_get_metadata_no_advanced_data(self):
        inst = self._make_instance()
        result_data = {}
        metadata = inst.azuread_get_metadata(result_data)
        assert metadata == {}

    def test_azuread_browse_obj_meta(self):
        inst = self._make_instance()
        obj = {
            "commonData": {"displayName": "TestUser", "id": "abc123"},
            "guid": "guid-456",
            "objType": 2,
        }
        name, metainfo = inst.azuread_browse_obj_meta(obj)
        assert name == "TestUser"
        assert metainfo["id"] == "abc123"
        assert metainfo["azureid"] == "abc123".replace("x", "-")
        assert metainfo["guid"] == "guid-456"
        assert metainfo["type"] == 2

    def test_process_result_format(self):
        inst = self._make_instance()
        results = [
            {"commonData": {"id": "abcx123x456"}},
            {"commonData": {"id": "nox"}},
        ]
        processed = inst._process_result_format(results)
        assert processed[0]["azureid"] == "abc-123-456"
        assert processed[1]["azureid"] == "no-"
