from unittest.mock import patch

import pytest

from cvpysdk.content_analyzer import ContentAnalyzers
from cvpysdk.exception import SDKException


@pytest.mark.unit
class TestContentAnalyzers:
    """Tests for the ContentAnalyzers collection class."""

    def test_init(self, mock_commcell):
        ca_data = {"ca1": {"caUrl": "http://url1", "clientName": "ca1", "clientId": 1}}
        with patch.object(ContentAnalyzers, "_get_all_content_analyzers", return_value=ca_data):
            ca = ContentAnalyzers(mock_commcell)
        assert ca._content_analyzers == ca_data

    def test_has_client_true(self, mock_commcell):
        ca_data = {"ca1": {"caUrl": "http://url1", "clientName": "ca1", "clientId": 1}}
        with patch.object(ContentAnalyzers, "_get_all_content_analyzers", return_value=ca_data):
            ca = ContentAnalyzers(mock_commcell)
        assert ca.has_client("ca1") is True

    def test_has_client_bad_type_raises(self, mock_commcell):
        with patch.object(ContentAnalyzers, "_get_all_content_analyzers", return_value={}):
            ca = ContentAnalyzers(mock_commcell)
        with pytest.raises(SDKException):
            ca.has_client(123)

    def test_get_bad_type_raises(self, mock_commcell):
        with patch.object(ContentAnalyzers, "_get_all_content_analyzers", return_value={}):
            ca = ContentAnalyzers(mock_commcell)
        with pytest.raises(SDKException):
            ca.get(123)

    def test_get_nonexistent_raises(self, mock_commcell):
        with patch.object(ContentAnalyzers, "_get_all_content_analyzers", return_value={}):
            ca = ContentAnalyzers(mock_commcell)
        with pytest.raises(SDKException):
            ca.get("nonexistent")

    def test_get_properties(self, mock_commcell):
        ca_data = {"ca1": {"caUrl": "http://url1", "clientName": "ca1", "clientId": 1}}
        with patch.object(ContentAnalyzers, "_get_all_content_analyzers", return_value=ca_data):
            ca = ContentAnalyzers(mock_commcell)
        result = ca.get_properties("ca1")
        assert result["caUrl"] == "http://url1"

    def test_get_cloud_from_collections(self):
        collections = {
            "contentAnalyzerList": [
                {"caUrl": "http://url1", "clientName": "ca1", "clientId": 1},
                {"caUrl": "http://url2", "clientName": "ca2", "clientId": 2},
            ]
        }
        result = ContentAnalyzers._get_cloud_from_collections(collections)
        assert "ca1" in result
        assert "ca2" in result
        assert result["ca1"]["clientId"] == 1

    def test_refresh(self, mock_commcell):
        with patch.object(
            ContentAnalyzers, "_get_all_content_analyzers", return_value={}
        ) as mock_get:
            ca = ContentAnalyzers(mock_commcell)
            ca.refresh()
        assert mock_get.call_count == 2
