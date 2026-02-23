from unittest.mock import patch

import pytest

from cvpysdk.alert import Alert, Alerts
from cvpysdk.exception import SDKException


@pytest.mark.unit
class TestAlerts:
    """Tests for the Alerts collection class."""

    def test_repr(self, mock_commcell):
        with patch.object(Alerts, "_get_alerts", return_value={}):
            alerts = Alerts(mock_commcell)
        assert "Alerts" in repr(alerts)

    def test_all_alerts_property(self, mock_commcell):
        alert_data = {"test_alert": {"id": "1", "description": "desc", "category": "cat"}}
        with patch.object(Alerts, "_get_alerts", return_value=alert_data):
            alerts = Alerts(mock_commcell)
        assert alerts.all_alerts == alert_data

    def test_has_alert_true(self, mock_commcell):
        alert_data = {"test_alert": {"id": "1", "description": "desc", "category": "cat"}}
        with patch.object(Alerts, "_get_alerts", return_value=alert_data):
            alerts = Alerts(mock_commcell)
        assert alerts.has_alert("test_alert") is True

    def test_has_alert_case_insensitive(self, mock_commcell):
        alert_data = {"test_alert": {"id": "1", "description": "desc", "category": "cat"}}
        with patch.object(Alerts, "_get_alerts", return_value=alert_data):
            alerts = Alerts(mock_commcell)
        assert alerts.has_alert("TEST_ALERT") is True

    def test_has_alert_bad_type_raises(self, mock_commcell):
        with patch.object(Alerts, "_get_alerts", return_value={}):
            alerts = Alerts(mock_commcell)
        with pytest.raises(SDKException):
            alerts.has_alert(123)

    def test_get_returns_alert_object(self, mock_commcell):
        alert_data = {"test_alert": {"id": "1", "description": "desc", "category": "cat"}}
        with patch.object(Alerts, "_get_alerts", return_value=alert_data):
            alerts = Alerts(mock_commcell)
        with patch.object(Alert, "__init__", return_value=None):
            result = alerts.get("test_alert")
        assert isinstance(result, Alert)

    def test_get_bad_type_raises(self, mock_commcell):
        with patch.object(Alerts, "_get_alerts", return_value={}):
            alerts = Alerts(mock_commcell)
        with pytest.raises(SDKException):
            alerts.get(123)

    def test_get_nonexistent_raises(self, mock_commcell):
        with patch.object(Alerts, "_get_alerts", return_value={}):
            alerts = Alerts(mock_commcell)
        with pytest.raises(SDKException):
            alerts.get("nonexistent")

    def test_len(self, mock_commcell):
        alert_data = {
            "alert1": {"id": "1", "description": "d1", "category": "c1"},
            "alert2": {"id": "2", "description": "d2", "category": "c2"},
        }
        with patch.object(Alerts, "_get_alerts", return_value=alert_data):
            alerts = Alerts(mock_commcell)
        assert len(alerts) == 2

    def test_getitem_by_name(self, mock_commcell):
        alert_data = {"alert1": {"id": "1", "description": "d1", "category": "c1"}}
        with patch.object(Alerts, "_get_alerts", return_value=alert_data):
            alerts = Alerts(mock_commcell)
        result = alerts["alert1"]
        assert result["id"] == "1"

    def test_getitem_by_id(self, mock_commcell):
        alert_data = {"alert1": {"id": "1", "description": "d1", "category": "c1"}}
        with patch.object(Alerts, "_get_alerts", return_value=alert_data):
            alerts = Alerts(mock_commcell)
        result = alerts["1"]
        assert result == "alert1"

    def test_getitem_invalid_raises(self, mock_commcell):
        alert_data = {"alert1": {"id": "1", "description": "d1", "category": "c1"}}
        with patch.object(Alerts, "_get_alerts", return_value=alert_data):
            alerts = Alerts(mock_commcell)
        with pytest.raises(IndexError):
            alerts["999"]

    def test_delete_bad_type_raises(self, mock_commcell):
        with patch.object(Alerts, "_get_alerts", return_value={}):
            alerts = Alerts(mock_commcell)
        with pytest.raises(SDKException):
            alerts.delete(123)

    def test_delete_nonexistent_raises(self, mock_commcell):
        with patch.object(Alerts, "_get_alerts", return_value={}):
            alerts = Alerts(mock_commcell)
        with pytest.raises(SDKException):
            alerts.delete("nonexistent")

    def test_console_alerts_bad_type_raises(self, mock_commcell):
        with patch.object(Alerts, "_get_alerts", return_value={}):
            alerts = Alerts(mock_commcell)
        with pytest.raises(SDKException):
            alerts.console_alerts(page_number="1", page_count=1)

    def test_console_alert_bad_type_raises(self, mock_commcell):
        with patch.object(Alerts, "_get_alerts", return_value={}):
            alerts = Alerts(mock_commcell)
        with pytest.raises(SDKException):
            alerts.console_alert("not_an_int")

    def test_create_alert_bad_type_raises(self, mock_commcell):
        with patch.object(Alerts, "_get_alerts", return_value={}):
            alerts = Alerts(mock_commcell)
        with pytest.raises(SDKException):
            alerts.create_alert("not_a_dict")

    def test_get_entities_bad_type_raises(self, mock_commcell):
        with patch.object(Alerts, "_get_alerts", return_value={}):
            alerts = Alerts(mock_commcell)
        with pytest.raises(SDKException):
            alerts._get_entities("not_a_dict")

    def test_refresh(self, mock_commcell):
        with patch.object(Alerts, "_get_alerts", return_value={}) as mock_get:
            alerts = Alerts(mock_commcell)
            alerts.refresh()
        assert mock_get.call_count == 2

    def test_str_representation(self, mock_commcell):
        alert_data = {"alert1": {"id": "1", "description": "desc1", "category": "cat1"}}
        with patch.object(Alerts, "_get_alerts", return_value=alert_data):
            alerts = Alerts(mock_commcell)
        result = str(alerts)
        assert "alert1" in result


@pytest.mark.unit
class TestAlert:
    """Tests for the Alert entity class."""

    def _make_alert(self, mock_commcell, name="test_alert", alert_id="1", category="cat"):
        """Helper to create Alert with mocked internals."""
        with patch.object(Alerts, "_get_alerts", return_value={}), patch.object(
            Alert, "_get_alert_properties"
        ):
            alert = Alert(mock_commcell, name, alert_id=alert_id, alert_category=category)
        return alert

    def test_repr(self, mock_commcell):
        alert = self._make_alert(mock_commcell)
        assert "test_alert" in repr(alert)

    def test_alert_id_property(self, mock_commcell):
        alert = self._make_alert(mock_commcell)
        assert alert.alert_id == "1"

    def test_alert_name_property(self, mock_commcell):
        alert = self._make_alert(mock_commcell)
        assert alert.alert_name == "test_alert"
