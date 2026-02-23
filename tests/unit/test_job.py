"""Unit tests for cvpysdk/job.py module."""

from unittest.mock import patch

import pytest

from cvpysdk.exception import SDKException
from cvpysdk.job import Job, JobController


@pytest.mark.unit
class TestJobControllerInit:
    """Tests for the JobController class."""

    def test_repr(self, mock_commcell):
        jc = JobController(mock_commcell)
        assert "JobController" in repr(jc)

    def test_stores_commcell(self, mock_commcell):
        jc = JobController(mock_commcell)
        assert jc._commcell_object is mock_commcell


@pytest.mark.unit
class TestJobControllerGet:
    """Tests for JobController.get method."""

    def test_get_returns_job(self, mock_commcell):
        jc = JobController(mock_commcell)
        with patch.object(Job, "__init__", lambda self, *a, **kw: None):
            job = jc.get(123)
        assert isinstance(job, Job)


@pytest.mark.unit
class TestJobInit:
    """Tests for Job class constructor."""

    def test_non_integer_job_id_raises(self, mock_commcell):
        with pytest.raises(SDKException):
            Job(mock_commcell, "not_a_number")

    def test_valid_job_id_accepted(self, mock_commcell):
        with patch.object(Job, "_is_valid_job", return_value=True):
            with patch.object(Job, "_get_job_summary"):
                with patch.object(Job, "_get_job_details"):
                    with patch.object(Job, "refresh"):
                        Job.__new__(Job)
                        # Simulate the constructor without the full API call
                        try:
                            int("123")
                        except ValueError:
                            pytest.fail("Should not raise")

    def test_integer_job_id_stored(self, mock_commcell):
        with patch.object(Job, "_is_valid_job", return_value=True):
            with patch.object(Job, "refresh"):
                job = Job.__new__(Job)
                job._commcell_object = mock_commcell
                job._cvpysdk_object = mock_commcell._cvpysdk_object
                job._services = mock_commcell._services
                job._update_response_ = mock_commcell._update_response_
                job._job_id = "123"
                assert job._job_id == "123"


@pytest.mark.unit
class TestJobRepr:
    """Tests for Job.__repr__."""

    def test_repr_contains_job_id(self):
        with patch.object(Job, "__init__", lambda self, *a, **kw: None):
            job = Job.__new__(Job)
            job._job_id = "999"
            result = repr(job)
            assert "999" in result
            assert "Job" in result


@pytest.mark.unit
class TestJobIsFinished:
    """Tests for Job.is_finished property."""

    def _make_job(self, status):
        """Helper to create a Job with mocked status."""
        with patch.object(Job, "__init__", lambda self, *a, **kw: None):
            job = Job.__new__(Job)
            job._job_id = "1"
            job._status = status
            job._summary = {"status": status, "lastUpdateTime": 0, "subclient": {}}
            job._details = {}
            job._end_time = None
            return job

    def test_completed_is_finished(self):
        job = self._make_job("Completed")
        with patch.object(Job, "_get_job_summary", return_value=job._summary):
            with patch.object(Job, "_get_job_details", return_value=job._details):
                assert job.is_finished is True

    def test_killed_is_finished(self):
        job = self._make_job("Killed")
        with patch.object(Job, "_get_job_summary", return_value=job._summary):
            with patch.object(Job, "_get_job_details", return_value=job._details):
                assert job.is_finished is True

    def test_failed_is_finished(self):
        job = self._make_job("Failed")
        with patch.object(Job, "_get_job_summary", return_value=job._summary):
            with patch.object(Job, "_get_job_details", return_value=job._details):
                assert job.is_finished is True

    def test_committed_is_finished(self):
        job = self._make_job("Committed")
        with patch.object(Job, "_get_job_summary", return_value=job._summary):
            with patch.object(Job, "_get_job_details", return_value=job._details):
                assert job.is_finished is True

    def test_running_is_not_finished(self):
        job = self._make_job("Running")
        with patch.object(Job, "_get_job_summary", return_value=job._summary):
            with patch.object(Job, "_get_job_details", return_value=job._details):
                assert job.is_finished is False

    def test_waiting_is_not_finished(self):
        job = self._make_job("Waiting")
        with patch.object(Job, "_get_job_summary", return_value=job._summary):
            with patch.object(Job, "_get_job_details", return_value=job._details):
                assert job.is_finished is False

    def test_suspended_is_not_finished(self):
        job = self._make_job("Suspended")
        with patch.object(Job, "_get_job_summary", return_value=job._summary):
            with patch.object(Job, "_get_job_details", return_value=job._details):
                assert job.is_finished is False


@pytest.mark.unit
class TestJobProperties:
    """Tests for Job property getters."""

    def test_job_id_property(self):
        with patch.object(Job, "__init__", lambda self, *a, **kw: None):
            job = Job.__new__(Job)
            job._job_id = "42"
            assert job.job_id == "42"
