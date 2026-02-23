"""Unit tests for cvpysdk/subclients/cloudapps/azure_cosmosdb_subclient.py"""

from unittest.mock import patch

import pytest

from cvpysdk.subclients.casubclient import CloudAppsSubclient
from cvpysdk.subclients.cloudapps.azure_cosmosdb_subclient import AzureCosmosDBSubclient


@pytest.mark.unit
class TestAzureCosmosDBSubclient:
    """Tests for the AzureCosmosDBSubclient class."""

    def test_inherits_cloud_apps_subclient(self):
        """AzureCosmosDBSubclient should inherit from CloudAppsSubclient."""
        assert issubclass(AzureCosmosDBSubclient, CloudAppsSubclient)

    def test_has_get_subclient_properties(self):
        """AzureCosmosDBSubclient should have _get_subclient_properties method."""
        assert hasattr(AzureCosmosDBSubclient, "_get_subclient_properties")

    def test_get_subclient_properties_calls_super(self):
        """_get_subclient_properties should call parent's _get_subclient_properties."""
        sub = object.__new__(AzureCosmosDBSubclient)
        with patch.object(CloudAppsSubclient, "_get_subclient_properties") as mock_super:
            sub._get_subclient_properties()
            mock_super.assert_called_once()

    def test_class_is_not_abstract(self):
        """AzureCosmosDBSubclient should be instantiable (not abstract)."""
        assert not getattr(AzureCosmosDBSubclient, "__abstractmethods__", set())
