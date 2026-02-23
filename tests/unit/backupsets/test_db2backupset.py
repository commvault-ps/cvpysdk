"""Tests for cvpysdk/backupsets/db2backupset.py (DB2Backupset)."""

import pytest

from cvpysdk.backupset import Backupset
from cvpysdk.backupsets.db2backupset import DB2Backupset


@pytest.mark.unit
class TestDB2BackupsetInheritance:
    def test_inherits_backupset(self):
        assert issubclass(DB2Backupset, Backupset)

    def test_has_restore_entire_database(self):
        assert hasattr(DB2Backupset, "restore_entire_database")

    def test_has_restore_out_of_place(self):
        assert hasattr(DB2Backupset, "restore_out_of_place")

    def test_has_restore_table_level(self):
        assert hasattr(DB2Backupset, "restore_table_level")

    def test_has_db2_db_status_property(self):
        assert isinstance(DB2Backupset.__dict__.get("db2_db_status"), property)


@pytest.mark.unit
class TestDB2BackupsetProperties:
    def _make_instance(self):
        inst = object.__new__(DB2Backupset)
        return inst

    def test_db2_db_status_returns_status(self):
        inst = self._make_instance()
        inst._properties = {"db2BackupSet": {"dB2DBStatus": "Connected"}}
        assert inst.db2_db_status == "Connected"

    def test_db2_db_status_returns_empty_when_missing(self):
        inst = self._make_instance()
        inst._properties = {}
        assert inst.db2_db_status == ""

    def test_db2_db_status_returns_empty_when_no_inner_key(self):
        inst = self._make_instance()
        inst._properties = {"db2BackupSet": {}}
        assert inst.db2_db_status == ""
