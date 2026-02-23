"""Unit tests for cvpysdk/subclients/informixsubclient.py"""

from unittest.mock import MagicMock

import pytest

from cvpysdk.subclient import Subclient
from cvpysdk.subclients.informixsubclient import InformixSubclient


@pytest.mark.unit
class TestInformixSubclient:
    """Tests for the InformixSubclient class."""

    def test_inherits_subclient(self):
        """InformixSubclient should inherit from Subclient."""
        assert issubclass(InformixSubclient, Subclient)

    def test_has_key_methods(self):
        """InformixSubclient should have expected methods."""
        assert hasattr(InformixSubclient, "restore_in_place")
        assert hasattr(InformixSubclient, "_get_subclient_properties")
        assert hasattr(InformixSubclient, "_get_subclient_properties_json")
        assert hasattr(InformixSubclient, "backup_mode")

    def test_get_subclient_properties_json_structure(self):
        """_get_subclient_properties_json should return proper structure."""
        subclient = object.__new__(InformixSubclient)
        subclient._informix_subclient_prop = {"backupMode": "Entire_instance"}
        subclient._subClientEntity = {"subclientId": 1}

        result = subclient._get_subclient_properties_json()
        assert "subClientProperties" in result
        assert "informixSubclientProp" in result["subClientProperties"]
        assert "subClientEntity" in result["subClientProperties"]

    def test_backup_mode_property(self):
        """backup_mode should return the backup mode string."""
        subclient = object.__new__(InformixSubclient)
        subclient._informix_subclient_prop = {"backupMode": "Entire_instance"}
        assert subclient.backup_mode == "Entire_instance"

    def test_backup_mode_property_empty(self):
        """backup_mode should return empty string when not set."""
        subclient = object.__new__(InformixSubclient)
        subclient._informix_subclient_prop = {}
        assert subclient.backup_mode == ""

    def test_restore_in_place_delegates(self):
        """restore_in_place should delegate to instance object."""
        subclient = object.__new__(InformixSubclient)
        subclient._backupset_object = MagicMock()
        subclient._subClientEntity = {"subclientId": 1}
        mock_job = MagicMock()
        subclient._backupset_object._instance_object.restore_in_place.return_value = mock_job

        result = subclient.restore_in_place(
            path=["/test"],
            restore_type="ENTIRE INSTANCE",
        )

        assert result == mock_job
        assert subclient._backupset_object._instance_object._restore_association == {
            "subclientId": 1
        }
