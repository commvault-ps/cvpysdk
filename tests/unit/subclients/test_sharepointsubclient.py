"""Unit tests for cvpysdk/subclients/sharepointsubclient.py"""

import pytest

from cvpysdk.subclient import Subclient
from cvpysdk.subclients.sharepointsubclient import (
    SharepointSubclient,
    SharepointSuperSubclient,
    SharepointV1Subclient,
)


@pytest.mark.unit
class TestSharepointSuperSubclient:
    """Tests for the SharepointSuperSubclient class."""

    def test_inherits_subclient(self):
        """SharepointSuperSubclient should inherit from Subclient."""
        assert issubclass(SharepointSuperSubclient, Subclient)


@pytest.mark.unit
class TestSharepointSubclient:
    """Tests for the SharepointSubclient class."""

    def test_inherits_sharepoint_super_subclient(self):
        """SharepointSubclient should inherit from SharepointSuperSubclient."""
        assert issubclass(SharepointSubclient, SharepointSuperSubclient)

    def test_has_key_methods(self):
        """SharepointSubclient should have expected methods."""
        assert hasattr(SharepointSubclient, "content")
        assert hasattr(SharepointSubclient, "restore")
        assert hasattr(SharepointSubclient, "run_manual_discovery")
        assert hasattr(SharepointSubclient, "browse_for_content")
        assert hasattr(SharepointSubclient, "process_index_retention_rules")

    def test_has_restore_methods(self):
        """SharepointSubclient should have restore methods."""
        assert hasattr(SharepointSubclient, "restore_in_place")
        assert hasattr(SharepointSubclient, "out_of_place_restore")
        assert hasattr(SharepointSubclient, "disk_restore")


@pytest.mark.unit
class TestSharepointV1Subclient:
    """Tests for the SharepointV1Subclient class."""

    def test_inherits_sharepoint_super_subclient(self):
        """SharepointV1Subclient should inherit from SharepointSuperSubclient."""
        assert issubclass(SharepointV1Subclient, SharepointSuperSubclient)

    def test_has_content_property(self):
        """SharepointV1Subclient should have content property."""
        assert hasattr(SharepointV1Subclient, "content")
