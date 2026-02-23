"""Unit tests for cvpysdk/subclients/lotusnotes/lndocsubclient.py module."""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.subclients.lotusnotes.lndocsubclient import LNDocSubclient
from cvpysdk.subclients.lotusnotes.lnsubclient import LNSubclient


@pytest.mark.unit
class TestLNDocSubclientInheritance:
    """Tests for LNDocSubclient class hierarchy."""

    def test_inherits_lnsubclient(self):
        assert issubclass(LNDocSubclient, LNSubclient)

    def test_class_exists_and_importable(self):
        from cvpysdk.subclients.lotusnotes import lndocsubclient

        assert hasattr(lndocsubclient, "LNDocSubclient")


@pytest.mark.unit
class TestLNDocSubclientRestoreMethods:
    """Tests for LNDocSubclient restore methods."""

    def test_has_restore_in_place_method(self):
        assert hasattr(LNDocSubclient, "restore_in_place")

    def test_has_restore_out_of_place_method(self):
        assert hasattr(LNDocSubclient, "restore_out_of_place")

    def test_restore_in_place_delegates_to_parent(self):
        with patch.object(LNDocSubclient, "__init__", lambda self, *a, **k: None):
            sub = object.__new__(LNDocSubclient)
        sub._subClientEntity = {"subclientId": 1}
        sub._backupset_object = MagicMock()
        sub._backupset_object._instance_object = MagicMock()
        sub._filter_paths = MagicMock(return_value=["/db1"])
        sub._restore_json = MagicMock(return_value={"taskInfo": {}})
        sub._process_restore_response = MagicMock(return_value="job_obj")

        result = sub.restore_in_place(["/db1"])
        assert result == "job_obj"

    def test_restore_out_of_place_delegates_to_parent(self):
        with patch.object(LNDocSubclient, "__init__", lambda self, *a, **k: None):
            sub = object.__new__(LNDocSubclient)
        sub._subClientEntity = {"subclientId": 1}
        sub._backupset_object = MagicMock()
        sub._instance_object = MagicMock()
        sub._backupset_object._instance_object = MagicMock()
        sub._commcell_object = MagicMock()
        sub._commcell_object.clients = MagicMock()
        sub._filter_paths = MagicMock(return_value=["/db1"])
        sub._restore_json = MagicMock(return_value={"taskInfo": {}})
        sub._process_restore_response = MagicMock(return_value="job_obj")

        client_mock = MagicMock()
        client_mock.client_name = "test_client"
        client_mock.client_id = "1"

        result = sub.restore_out_of_place(
            client=client_mock,
            destination_path="/dest",
            paths=["/db1"],
        )
        assert result == "job_obj"
