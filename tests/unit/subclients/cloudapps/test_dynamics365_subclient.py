"""Unit tests for cvpysdk/subclients/cloudapps/dynamics365_subclient.py"""

import pytest

from cvpysdk.subclients.cloudapps.dynamics365_subclient import MSDynamics365Subclient
from cvpysdk.subclients.o365apps_subclient import O365AppsSubclient


@pytest.mark.unit
class TestMSDynamics365Subclient:
    """Tests for the MSDynamics365Subclient class."""

    def test_inherits_o365apps_subclient(self):
        """MSDynamics365Subclient should inherit from O365AppsSubclient."""
        assert issubclass(MSDynamics365Subclient, O365AppsSubclient)

    def test_has_key_properties(self):
        """MSDynamics365Subclient should have expected properties."""
        assert hasattr(MSDynamics365Subclient, "discovered_environments")
        assert hasattr(MSDynamics365Subclient, "discovered_tables")
        assert hasattr(MSDynamics365Subclient, "browse_item_type")

    def test_has_restore_methods(self):
        """MSDynamics365Subclient should have restore methods."""
        assert hasattr(MSDynamics365Subclient, "restore_in_place")
        assert hasattr(MSDynamics365Subclient, "restore_out_of_place")
        assert hasattr(MSDynamics365Subclient, "browse")

    def test_has_backup_methods(self):
        """MSDynamics365Subclient should have backup/content methods."""
        assert hasattr(MSDynamics365Subclient, "launch_client_level_full_backup")
        assert hasattr(MSDynamics365Subclient, "_run_backup")
