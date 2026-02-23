"""Tests for cvpysdk/backupsets/sharepointbackupset.py (SharepointBackupset)."""

import pytest

from cvpysdk.backupset import Backupset
from cvpysdk.backupsets.sharepointbackupset import SharepointBackupset


@pytest.mark.unit
class TestSharepointBackupsetInheritance:
    def test_inherits_backupset(self):
        assert issubclass(SharepointBackupset, Backupset)

    def test_has_is_sharepoint_online_instance_property(self):
        assert isinstance(
            SharepointBackupset.__dict__.get("is_sharepoint_online_instance"),
            property,
        )

    def test_has_azure_storage_details_property(self):
        assert isinstance(
            SharepointBackupset.__dict__.get("azure_storage_details"),
            property,
        )
