"""Unit tests for cvpysdk.subclients.virtualserver.kubernetes module."""

import pytest

from cvpysdk.subclient import Subclients
from cvpysdk.subclients.virtualserver.kubernetes import (
    ApplicationGroups,
    KubernetesVirtualServerSubclient,
)
from cvpysdk.subclients.vssubclient import VirtualServerSubclient


@pytest.mark.unit
class TestKubernetesVirtualServerSubclient:
    """Tests for the KubernetesVirtualServerSubclient class."""

    def test_inherits_from_virtual_server_subclient(self):
        """Test correct inheritance chain."""
        assert issubclass(KubernetesVirtualServerSubclient, VirtualServerSubclient)

    def test_has_restore_methods(self):
        """Test that the class defines expected restore methods."""
        assert hasattr(KubernetesVirtualServerSubclient, "full_app_restore_out_of_place")
        assert hasattr(KubernetesVirtualServerSubclient, "full_app_restore_in_place")
        assert hasattr(KubernetesVirtualServerSubclient, "disk_restore")
        assert hasattr(KubernetesVirtualServerSubclient, "guest_file_restore")
        assert hasattr(KubernetesVirtualServerSubclient, "guest_files_browse")

    def test_has_namespace_restore_methods(self):
        """Test that namespace-level restore methods are defined."""
        assert hasattr(KubernetesVirtualServerSubclient, "namespace_restore_out_of_place")
        assert hasattr(KubernetesVirtualServerSubclient, "namespace_restore_in_place")

    def test_has_enable_intelli_snap(self):
        """Test that enable_intelli_snap method exists."""
        assert hasattr(KubernetesVirtualServerSubclient, "enable_intelli_snap")

    def test_has_prepare_json_methods(self):
        """Test that internal JSON preparation methods exist."""
        assert hasattr(KubernetesVirtualServerSubclient, "_prepare_kubernetes_restore_json")
        assert hasattr(
            KubernetesVirtualServerSubclient,
            "_prepare_kubernetes_inplace_restore_json",
        )
        assert hasattr(KubernetesVirtualServerSubclient, "_json_restore_volumeRstOption")


@pytest.mark.unit
class TestApplicationGroups:
    """Tests for the ApplicationGroups class."""

    def test_inherits_from_subclients(self):
        """Test that ApplicationGroups inherits from Subclients."""
        assert issubclass(ApplicationGroups, Subclients)

    def test_has_browse_method(self):
        """Test that browse method is defined."""
        assert hasattr(ApplicationGroups, "browse")

    def test_has_create_application_group_method(self):
        """Test that create_application_group method is defined."""
        assert hasattr(ApplicationGroups, "create_application_group")

    def test_has_get_children_node_method(self):
        """Test that get_children_node method is defined."""
        assert hasattr(ApplicationGroups, "get_children_node")
