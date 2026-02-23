"""Unit tests for cvpysdk.reports.report module."""

import pytest

from cvpysdk.reports.report import BackupJobSummary, FormatType, Report


@pytest.mark.unit
class TestFormatType:
    """Tests for the FormatType enum."""

    def test_format_type_members(self):
        """Test FormatType has expected members."""
        assert FormatType.HTML.value == 1
        assert FormatType.PDF.value == 6
        assert FormatType.TEXT.value == 2
        assert FormatType.XML.value == 12

    def test_format_type_names(self):
        """Test FormatType member names."""
        names = [f.name for f in FormatType]
        assert "HTML" in names
        assert "PDF" in names
        assert "TEXT" in names
        assert "XML" in names


@pytest.mark.unit
class TestReport:
    """Tests for the Report class."""

    def test_init(self, mock_commcell):
        """Test constructor initializes attributes."""
        report = Report(mock_commcell)
        assert report._commcell is mock_commcell
        assert report._request_json == {}
        assert report._report_extension == "HTML"
        assert report._backup_job_summary_report is None

    def test_backup_job_summary_property(self, mock_commcell):
        """Test backup_job_summary returns BackupJobSummary instance."""
        mock_commcell.commcell_username = "admin"
        report = Report(mock_commcell)
        summary = report.backup_job_summary
        assert isinstance(summary, BackupJobSummary)
        # Second access returns same instance
        assert report.backup_job_summary is summary

    def test_set_report_custom_name(self, mock_commcell):
        """Test set_report_custom_name appends extension."""
        report = Report(mock_commcell)
        report._request_json = {
            "taskInfo": {
                "subTasks": [
                    {
                        "options": {
                            "adminOpts": {"reportOption": {"commonOpt": {"reportCustomName": ""}}}
                        }
                    }
                ]
            }
        }
        report.set_report_custom_name("my_report")
        custom_name = report._request_json["taskInfo"]["subTasks"][0]["options"]["adminOpts"][
            "reportOption"
        ]["commonOpt"]["reportCustomName"]
        assert custom_name == "my_report.HTML"

    def test_run_report_success(self, mock_commcell, mock_response):
        """Test run_report returns job ID on success."""
        report = Report(mock_commcell)
        resp = mock_response(json_data={"jobIds": ["99"]})
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        result = report.run_report()
        assert result == "99"


@pytest.mark.unit
class TestBackupJobSummary:
    """Tests for the BackupJobSummary class."""

    def test_init(self, mock_commcell):
        """Test constructor builds request JSON."""
        mock_commcell.commcell_username = "admin"
        summary = BackupJobSummary(mock_commcell)
        assert "taskInfo" in summary._request_json
        task_info = summary._request_json["taskInfo"]
        assert task_info["task"]["ownerName"] == "admin"

    def test_select_protected_objects(self, mock_commcell):
        """Test select_protected_objects sets the right flag."""
        mock_commcell.commcell_username = "admin"
        summary = BackupJobSummary(mock_commcell)
        summary.select_protected_objects()
        flag = summary._request_json["taskInfo"]["subTasks"][0]["options"]["adminOpts"][
            "reportOption"
        ]["jobSummaryReport"]["rptSelections"]["protectedObjects"]
        assert flag is True

    def test_set_last_hours(self, mock_commcell):
        """Test set_last_hours sets time range."""
        mock_commcell.commcell_username = "admin"
        summary = BackupJobSummary(mock_commcell)
        summary.set_last_hours(48)
        time_range = summary._request_json["taskInfo"]["subTasks"][0]["options"]["adminOpts"][
            "reportOption"
        ]["timeRangeOption"]
        assert time_range["type"] == 13
        assert time_range["toTimeValue"] == "48"

    def test_set_last_days(self, mock_commcell):
        """Test set_last_days sets time range."""
        mock_commcell.commcell_username = "admin"
        summary = BackupJobSummary(mock_commcell)
        summary.set_last_days(7)
        time_range = summary._request_json["taskInfo"]["subTasks"][0]["options"]["adminOpts"][
            "reportOption"
        ]["timeRangeOption"]
        assert time_range["type"] == 11
        assert time_range["toTimeValue"] == "7"

    def test_select_computers(self, mock_commcell):
        """Test select_computers sets clients and groups."""
        mock_commcell.commcell_username = "admin"
        summary = BackupJobSummary(mock_commcell)
        summary.select_computers(clients=["client1", "client2"], client_groups=["group1"])
        computer_sel = summary._request_json["taskInfo"]["subTasks"][0]["options"]["adminOpts"][
            "reportOption"
        ]["computerSelectionList"]
        assert computer_sel["includeAll"] is False
        assert len(computer_sel["clientList"]) == 2
        assert len(computer_sel["clientGroupList"]) == 1
