"""Unit tests for cvpysdk.datacube.constants module."""

import pytest

from cvpysdk.datacube.constants import ContentAnalyzerConstants, IndexServerConstants


@pytest.mark.unit
class TestIndexServerConstants:
    """Tests for IndexServerConstants class."""

    def test_ida_name(self):
        assert IndexServerConstants.INDEX_SERVER_IDA_NAME == "Big Data Apps"

    def test_instance_name(self):
        assert IndexServerConstants.INDEX_SERVER_INSTANCE_NAME == "dynamicIndexInstance"

    def test_role_constants(self):
        assert IndexServerConstants.ROLE_DATA_ANALYTICS == "Data Analytics"
        assert IndexServerConstants.ROLE_FILE_SYSTEM_INDEX == "FileSystem Index"
        assert IndexServerConstants.ROLE_EXCHANGE_INDEX == "Exchange Index"
        assert IndexServerConstants.ROLE_ONEDRIVE_INDEX == "OneDrive Index"
        assert IndexServerConstants.ROLE_SYSTEM_DEFAULT == "System Default"

    def test_operation_constants(self):
        assert IndexServerConstants.OPERATION_ADD == 1
        assert IndexServerConstants.OPERATION_DELETE == 2
        assert IndexServerConstants.OPERATION_EDIT == 3

    def test_default_values(self):
        assert IndexServerConstants.DEFAULT_JVM_MAX_MEMORY == "8191"
        assert IndexServerConstants.DEFAULT_SOLR_PORT == "20000"

    def test_solr_meta_info(self):
        assert IndexServerConstants.SOLR_PORT_META_INFO == {
            "name": "PORTNO",
            "value": "20000",
        }
        assert IndexServerConstants.SOLR_JVM_META_INFO == {
            "name": "JVMMAXMEMORY",
            "value": "8191",
        }

    def test_request_json_structure(self):
        rj = IndexServerConstants.REQUEST_JSON
        assert rj["opType"] == 1
        assert rj["type"] == 1
        assert rj["configureNodes"] is True
        assert "solrCloudInfo" in rj
        assert "cloudNodes" in rj

    def test_prune_request_json(self):
        prj = IndexServerConstants.PRUNE_REQUEST_JSON
        assert prj["forceDelete"] is False
        assert prj["datasourceId"] == 0

    def test_update_add_role(self):
        uar = IndexServerConstants.UPDATE_ADD_ROLE
        assert uar["roleName"] == ""
        assert uar["operationType"] == 1


@pytest.mark.unit
class TestContentAnalyzerConstants:
    """Tests for ContentAnalyzerConstants class."""

    def test_operation_constants(self):
        assert ContentAnalyzerConstants.OPERATION_ADD == 1
        assert ContentAnalyzerConstants.OPERATION_DELETE == 2
        assert ContentAnalyzerConstants.OPERATION_EDIT == 3

    def test_request_json_structure(self):
        rj = ContentAnalyzerConstants.REQUEST_JSON
        assert rj["opType"] == 1
        assert rj["type"] == 2
        assert rj["configureNodes"] is True
        assert "cloudNodes" in rj
        assert "cloudInfoEntity" in rj
