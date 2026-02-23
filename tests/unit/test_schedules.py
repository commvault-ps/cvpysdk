from unittest.mock import patch

import pytest

from cvpysdk.exception import SDKException
from cvpysdk.schedules import OperationType, SchedulePattern, Schedules


@pytest.mark.unit
class TestSchedulePattern:
    """Tests for the SchedulePattern class."""

    def test_init_default(self):
        sp = SchedulePattern()
        assert sp._pattern == {"freq_type": "Init"}

    def test_init_with_pattern(self):
        pattern = {"freq_type": 4, "active_start_time": 3600}
        sp = SchedulePattern(schedule_pattern=pattern)
        assert sp._pattern == pattern

    def test_time_converter_utc_to_epoch(self):
        result = SchedulePattern._time_converter("1/1/1970 00:00", "%m/%d/%Y %H:%M")
        assert result == 0

    def test_time_converter_epoch_to_utc(self):
        result = SchedulePattern._time_converter(0, "%m/%d/%Y %H:%M", utc_to_epoch=False)
        assert result == "01/01/1970 00:00"

    def test_time_converter_bad_format_raises(self):
        with pytest.raises(SDKException):
            SchedulePattern._time_converter("bad_date", "%m/%d/%Y %H:%M")

    def test_create_schedule_pattern_missing_freq_type_raises(self):
        sp = SchedulePattern()
        with pytest.raises(SDKException):
            sp.create_schedule_pattern({})

    def test_create_schedule_pattern_invalid_freq_type_raises(self):
        sp = SchedulePattern()
        with pytest.raises(SDKException):
            sp.create_schedule_pattern({"freq_type": "nonexistent_type"})

    def test_one_time_pattern(self):
        sp = SchedulePattern()
        result = sp.create_schedule_pattern(
            {
                "freq_type": "one_time",
                "active_start_date": "01/01/2025",
                "active_start_time": "09:00",
            }
        )
        assert result["freq_type"] == 1

    def test_daily_pattern(self):
        sp = SchedulePattern()
        result = sp.create_schedule_pattern(
            {"freq_type": "daily", "active_start_time": "09:00", "repeat_days": 2}
        )
        assert result["freq_type"] == 4
        assert result["freq_recurrence_factor"] == 2

    def test_weekly_pattern(self):
        sp = SchedulePattern()
        result = sp.create_schedule_pattern(
            {
                "freq_type": "weekly",
                "active_start_time": "09:00",
                "weekdays": ["Monday", "Wednesday"],
            }
        )
        assert result["freq_type"] == 8

    def test_monthly_pattern(self):
        sp = SchedulePattern()
        result = sp.create_schedule_pattern(
            {"freq_type": "monthly", "active_start_time": "09:00", "on_day": 15}
        )
        assert result["freq_type"] == 16
        assert result["freq_interval"] == 15

    def test_continuous_pattern(self):
        sp = SchedulePattern()
        result = sp.create_schedule_pattern({"freq_type": "continuous", "job_interval": 60})
        assert result["freq_type"] == 4096
        assert result["freq_interval"] == 60

    def test_exception_dates(self):
        result = SchedulePattern.exception_dates([1, 3, 5])
        # 1 << 0 | 1 << 2 | 1 << 4 = 1 + 4 + 16 = 21
        assert result == 21


@pytest.mark.unit
class TestOperationType:
    """Tests for the OperationType class."""

    def test_reports_value(self):
        assert OperationType.REPORTS == "Reports"

    def test_data_aging_value(self):
        assert OperationType.DATA_AGING == "DATA_AGING"


@pytest.mark.unit
class TestSchedules:
    """Tests for the Schedules collection class."""

    def test_init_with_invalid_object_raises(self):
        with pytest.raises(SDKException):
            Schedules("invalid_object")

    def test_init_with_commcell(self, mock_commcell):
        # Need to patch the isinstance check and the _get_schedules method
        from cvpysdk.commcell import Commcell

        with patch("cvpysdk.schedules.isinstance") as mock_isinstance, patch.object(
            Schedules, "_get_schedules", return_value={}
        ):
            mock_isinstance.side_effect = lambda obj, cls: (
                True
                if cls is Commcell and obj is mock_commcell
                else type.__instancecheck__(cls, obj)
            )
            schedules = Schedules(mock_commcell)
            assert schedules.schedules == {}
