"""Unit tests for cvpysdk/subclients/casubclient.py"""

from unittest.mock import MagicMock

import pytest

from cvpysdk.subclient import Subclient
from cvpysdk.subclients.casubclient import CloudAppsSubclient


@pytest.mark.unit
class TestCloudAppsSubclient:
    """Tests for the CloudAppsSubclient class."""

    def test_inherits_subclient(self):
        """CloudAppsSubclient should inherit from Subclient."""
        assert issubclass(CloudAppsSubclient, Subclient)

    def test_has_new_method(self):
        """CloudAppsSubclient should override __new__."""
        assert hasattr(CloudAppsSubclient, "__new__")

    def test_new_returns_google_subclient_for_type_1(self):
        """__new__ should return GoogleSubclient for instance type 1 (Gmail)."""
        from cvpysdk.subclients.cloudapps.google_subclient import GoogleSubclient

        backupset_obj = MagicMock()
        backupset_obj._instance_object._properties = {"cloudAppsInstance": {"instanceType": 1}}
        result = CloudAppsSubclient.__new__(CloudAppsSubclient, backupset_obj, "test")
        assert isinstance(result, GoogleSubclient)

    def test_new_returns_salesforce_subclient_for_type_3(self):
        """__new__ should return SalesforceSubclient for instance type 3."""
        from cvpysdk.subclients.cloudapps.salesforce_subclient import (
            SalesforceSubclient,
        )

        backupset_obj = MagicMock()
        backupset_obj._instance_object._properties = {"cloudAppsInstance": {"instanceType": 3}}
        result = CloudAppsSubclient.__new__(CloudAppsSubclient, backupset_obj, "test")
        assert isinstance(result, SalesforceSubclient)

    def test_new_returns_cloud_storage_for_type_5(self):
        """__new__ should return CloudStorageSubclient for instance type 5 (S3)."""
        from cvpysdk.subclients.cloudapps.cloud_storage_subclient import (
            CloudStorageSubclient,
        )

        backupset_obj = MagicMock()
        backupset_obj._instance_object._properties = {"cloudAppsInstance": {"instanceType": 5}}
        result = CloudAppsSubclient.__new__(CloudAppsSubclient, backupset_obj, "test")
        assert isinstance(result, CloudStorageSubclient)

    def test_new_returns_onedrive_for_type_7(self):
        """__new__ should return OneDriveSubclient for instance type 7."""
        from cvpysdk.subclients.cloudapps.onedrive_subclient import OneDriveSubclient

        backupset_obj = MagicMock()
        backupset_obj._instance_object._properties = {"cloudAppsInstance": {"instanceType": 7}}
        result = CloudAppsSubclient.__new__(CloudAppsSubclient, backupset_obj, "test")
        assert isinstance(result, OneDriveSubclient)

    def test_new_returns_teams_for_type_36(self):
        """__new__ should return TeamsSubclient for instance type 36."""
        from cvpysdk.subclients.cloudapps.teams_subclient import TeamsSubclient

        backupset_obj = MagicMock()
        backupset_obj._instance_object._properties = {"cloudAppsInstance": {"instanceType": 36}}
        result = CloudAppsSubclient.__new__(CloudAppsSubclient, backupset_obj, "test")
        assert isinstance(result, TeamsSubclient)

    def test_new_raises_for_unknown_instance_type(self):
        """__new__ should raise SDKException for unsupported instance types."""
        from cvpysdk.exception import SDKException

        backupset_obj = MagicMock()
        backupset_obj._instance_object._properties = {"cloudAppsInstance": {"instanceType": 999}}
        with pytest.raises(SDKException):
            CloudAppsSubclient.__new__(CloudAppsSubclient, backupset_obj, "test")

    def test_new_returns_dynamics365_for_type_35(self):
        """__new__ should return MSDynamics365Subclient for instance type 35."""
        from cvpysdk.subclients.cloudapps.dynamics365_subclient import (
            MSDynamics365Subclient,
        )

        backupset_obj = MagicMock()
        backupset_obj._instance_object._properties = {"cloudAppsInstance": {"instanceType": 35}}
        result = CloudAppsSubclient.__new__(CloudAppsSubclient, backupset_obj, "test")
        assert isinstance(result, MSDynamics365Subclient)
