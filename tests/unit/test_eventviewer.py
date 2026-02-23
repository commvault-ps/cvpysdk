from unittest.mock import patch

import pytest

from cvpysdk.eventviewer import Event, Events


@pytest.mark.unit
class TestEvents:
    """Tests for the Events collection class."""

    def test_repr(self, mock_commcell):
        with patch.object(Events, "events", return_value={}):
            ev = Events(mock_commcell)
        assert "Events" in repr(ev)

    def test_events_stored(self, mock_commcell):
        events_data = {1: "100", 2: "200"}
        with patch.object(Events, "events", return_value=events_data):
            ev = Events(mock_commcell)
        assert ev._events == events_data

    def test_str_representation(self, mock_commcell):
        events_data = {1: "100"}
        with patch.object(Events, "events", return_value=events_data):
            ev = Events(mock_commcell)
        result = str(ev)
        assert "EventId" in result

    def test_get_returns_event_object(self, mock_commcell):
        with patch.object(Events, "events", return_value={}):
            ev = Events(mock_commcell)
        with patch.object(Event, "__init__", return_value=None):
            result = ev.get("123")
        assert isinstance(result, Event)


@pytest.mark.unit
class TestEvent:
    """Tests for the Event entity class."""

    def test_repr(self, mock_commcell):
        with patch.object(Event, "_get_event_properties"):
            event = Event(mock_commcell, "123")
        assert "123" in repr(event)

    def test_event_code_property(self, mock_commcell):
        with patch.object(Event, "_get_event_properties"):
            event = Event(mock_commcell, "123")
            event._eventcode = "318767861"
        assert event.event_code == "318767861"

    def test_job_id_property(self, mock_commcell):
        with patch.object(Event, "_get_event_properties"):
            event = Event(mock_commcell, "123")
            event._job_id = 456
        assert event.job_id == 456

    def test_is_backup_disabled_true(self, mock_commcell):
        with patch.object(Event, "_get_event_properties"):
            event = Event(mock_commcell, "123")
            event._eventcode = "318767861"
        assert event.is_backup_disabled is True

    def test_is_backup_disabled_false(self, mock_commcell):
        with patch.object(Event, "_get_event_properties"):
            event = Event(mock_commcell, "123")
            event._eventcode = "999999"
        assert event.is_backup_disabled is False

    def test_is_restore_disabled_true(self, mock_commcell):
        with patch.object(Event, "_get_event_properties"):
            event = Event(mock_commcell, "123")
            event._eventcode = "318767864"
        assert event.is_restore_disabled is True

    def test_is_restore_disabled_false(self, mock_commcell):
        with patch.object(Event, "_get_event_properties"):
            event = Event(mock_commcell, "123")
            event._eventcode = "999999"
        assert event.is_restore_disabled is False
