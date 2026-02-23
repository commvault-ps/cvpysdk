"""Unit tests for cvpysdk.monitoringapps.constants module."""

import pytest

from cvpysdk.monitoringapps.constants import (
    FileTypeConstants,
    RequestConstants,
    ThreatConstants,
)


@pytest.mark.unit
class TestThreatConstants:
    """Tests for the ThreatConstants class."""

    def test_infected_count_field(self):
        """Test FIELD_INFECTED_COUNT constant."""
        assert ThreatConstants.FIELD_INFECTED_COUNT == "infectedFilesCount"

    def test_fingerprint_count_field(self):
        """Test FIELD_FINGERPRINT_COUNT constant."""
        assert ThreatConstants.FIELD_FINGERPRINT_COUNT == "fingerPrintFilesCount"

    def test_datasource_id_field(self):
        """Test FIELD_DATASOURCE_ID constant."""
        assert ThreatConstants.FIELD_DATASOURCE_ID == "dataSourceId"


@pytest.mark.unit
class TestFileTypeConstants:
    """Tests for the FileTypeConstants class."""

    def test_delete_count_field(self):
        """Test FIELD_DELETE_COUNT constant."""
        assert FileTypeConstants.FIELD_DELETE_COUNT == "deleteCount"

    def test_rename_count_field(self):
        """Test FIELD_RENAME_COUNT constant."""
        assert FileTypeConstants.FIELD_RENAME_COUNT == "renameCount"

    def test_create_count_field(self):
        """Test FIELD_CREATE_COUNT constant."""
        assert FileTypeConstants.FIELD_CREATE_COUNT == "createCount"

    def test_modified_count_field(self):
        """Test FIELD_MODIFIED_COUNT constant."""
        assert FileTypeConstants.FIELD_MODIFIED_COUNT == "modCount"


@pytest.mark.unit
class TestRequestConstants:
    """Tests for the RequestConstants class."""

    def test_clear_anomaly_json_structure(self):
        """Test CLEAR_ANOMALY_JSON has expected structure."""
        json_data = RequestConstants.CLEAR_ANOMALY_JSON
        assert "clients" in json_data
        assert "anomalyTypes" in json_data
        assert len(json_data["clients"]) == 1
        assert json_data["clients"][0]["_type_"] == "CLIENT_ENTITY"

    def test_run_scan_json_structure(self):
        """Test RUN_SCAN_JSON has expected structure."""
        json_data = RequestConstants.RUN_SCAN_JSON
        assert "client" in json_data
        assert "timeRange" in json_data
        assert "threatAnalysisFlags" in json_data
        assert "indexServer" in json_data
        assert "backupDetails" in json_data
