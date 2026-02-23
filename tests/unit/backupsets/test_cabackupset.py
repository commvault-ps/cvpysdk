"""Tests for cvpysdk/backupsets/cabackupset.py (CloudAppsBackupset)."""

from unittest.mock import MagicMock

import pytest

from cvpysdk.backupset import Backupset
from cvpysdk.backupsets.cabackupset import CloudAppsBackupset


@pytest.mark.unit
class TestCloudAppsBackupsetInheritance:
    def test_inherits_backupset(self):
        assert issubclass(CloudAppsBackupset, Backupset)

    def test_has_new_method(self):
        assert hasattr(CloudAppsBackupset, "__new__")


@pytest.mark.unit
class TestCloudAppsBackupsetNew:
    def test_returns_salesforce_for_instance_type_3(self):
        from cvpysdk.backupsets.cloudapps.salesforce_backupset import (
            SalesforceBackupset,
        )

        instance_object = MagicMock()
        instance_object._properties = {"cloudAppsInstance": {"instanceType": 3}}

        result = CloudAppsBackupset.__new__(CloudAppsBackupset, instance_object, "test_bs")
        assert isinstance(result, SalesforceBackupset)

    def test_returns_base_class_for_unknown_instance_type(self):
        instance_object = MagicMock()
        instance_object._properties = {"cloudAppsInstance": {"instanceType": 999}}

        result = CloudAppsBackupset.__new__(CloudAppsBackupset, instance_object, "test_bs")
        assert type(result) is CloudAppsBackupset

    def test_returns_base_class_for_instance_type_1(self):
        instance_object = MagicMock()
        instance_object._properties = {"cloudAppsInstance": {"instanceType": 1}}

        result = CloudAppsBackupset.__new__(CloudAppsBackupset, instance_object, "test_bs")
        assert type(result) is CloudAppsBackupset
