"""Unit tests for cvpysdk.drorchestration.drjob module."""

from unittest.mock import patch

import pytest

from cvpysdk.drorchestration.drjob import DRJob


@pytest.mark.unit
class TestDRJob:
    """Tests for the DRJob class."""

    def _create_drjob(self, mock_commcell, mock_response):
        """Create a DRJob object by patching Job.__init__."""
        mock_commcell.commserv_version = 31

        resp = mock_response(
            json_data={
                "job": [
                    {
                        "jobId": 100,
                        "replicationId": 1,
                        "phase": [
                            {
                                "phase": 1,
                                "status": 0,
                                "startTime": {"time": 1000},
                                "endTime": {"time": 2000},
                                "entity": {"clientName": "vm1"},
                                "phaseInfo": {
                                    "job": [
                                        {
                                            "jobid": 101,
                                            "failure": {"errorMessage": ""},
                                        }
                                    ]
                                },
                            }
                        ],
                        "client": {"clientId": 0, "clientName": "vm1"},
                    }
                ]
            }
        )
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)

        with patch("cvpysdk.drorchestration.drjob.Job.__init__", return_value=None):
            drjob = DRJob(mock_commcell, 100)
            drjob._commcell_object = mock_commcell
            drjob._job_id = 100

        drjob._replication_job_stats = [
            {
                "jobId": 100,
                "replicationId": 1,
                "phase": [
                    {
                        "phase": 1,
                        "status": 0,
                        "startTime": {"time": 1000},
                        "endTime": {"time": 2000},
                        "entity": {"clientName": "vm1"},
                        "phaseInfo": {
                            "job": [
                                {
                                    "jobid": 101,
                                    "failure": {"errorMessage": ""},
                                }
                            ]
                        },
                    }
                ],
                "client": {"clientId": 0, "clientName": "vm1"},
            }
        ]
        return drjob

    def test_get_phases(self, mock_commcell, mock_response):
        drjob = self._create_drjob(mock_commcell, mock_response)
        phases = drjob.get_phases()
        assert "vm1" in phases
        assert len(phases["vm1"]) == 1
        assert phases["vm1"][0]["phase_status"] == 0

    def test_get_phases_empty(self, mock_commcell, mock_response):
        drjob = self._create_drjob(mock_commcell, mock_response)
        drjob._replication_job_stats = None
        phases = drjob.get_phases()
        assert phases == {}

    def test_get_phases_machine_name(self, mock_commcell, mock_response):
        drjob = self._create_drjob(mock_commcell, mock_response)
        phases = drjob.get_phases()
        assert phases["vm1"][0]["machine_name"] == "vm1"

    def test_service_url_version_gt_30(self, mock_commcell, mock_response):
        """Test that correct service URL is used for version > 30."""
        mock_commcell.commserv_version = 31
        with patch("cvpysdk.drorchestration.drjob.Job.__init__", return_value=None):
            drjob = DRJob(mock_commcell, 100)
        expected_url = mock_commcell._services["DRORCHESTRATION_JOB_STATS"] % 100
        assert drjob._REPLICATION_STATS == expected_url
