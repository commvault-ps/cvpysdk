"""Unit tests for cvpysdk/subclients/cloudapps/salesforce_subclient.py"""

import pytest

from cvpysdk.subclients.casubclient import CloudAppsSubclient
from cvpysdk.subclients.cloudapps.salesforce_subclient import SalesforceSubclient


@pytest.mark.unit
class TestSalesforceSubclient:
    """Tests for the SalesforceSubclient class."""

    def test_inherits_cloud_apps_subclient(self):
        """SalesforceSubclient should inherit from CloudAppsSubclient."""
        assert issubclass(SalesforceSubclient, CloudAppsSubclient)

    def test_has_key_properties(self):
        """SalesforceSubclient should have expected properties."""
        assert hasattr(SalesforceSubclient, "objects")
        assert hasattr(SalesforceSubclient, "files")
        assert hasattr(SalesforceSubclient, "metadata")

    def test_has_enable_disable_methods(self):
        """SalesforceSubclient should have enable/disable methods."""
        assert hasattr(SalesforceSubclient, "enable_files")
        assert hasattr(SalesforceSubclient, "disable_files")
        assert hasattr(SalesforceSubclient, "enable_metadata")
        assert hasattr(SalesforceSubclient, "disable_metadata")

    def test_has_restore_methods(self):
        """SalesforceSubclient should have restore methods."""
        assert hasattr(SalesforceSubclient, "restore_to_file_system")
        assert hasattr(SalesforceSubclient, "restore_to_database")
        assert hasattr(SalesforceSubclient, "restore_to_salesforce_from_database")
        assert hasattr(SalesforceSubclient, "restore_to_salesforce_from_media")

    def test_has_metadata_restore(self):
        """SalesforceSubclient should have metadata_restore_to_salesforce method."""
        assert hasattr(SalesforceSubclient, "metadata_restore_to_salesforce")
