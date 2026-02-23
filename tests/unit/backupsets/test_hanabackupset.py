"""Tests for cvpysdk/backupsets/hanabackupset.py (HANABackupset)."""

import pytest

from cvpysdk.backupset import Backupset
from cvpysdk.backupsets.hanabackupset import HANABackupset


@pytest.mark.unit
class TestHANABackupsetInheritance:
    def test_inherits_backupset(self):
        assert issubclass(HANABackupset, Backupset)

    def test_has_restore_method(self):
        assert hasattr(HANABackupset, "restore")
