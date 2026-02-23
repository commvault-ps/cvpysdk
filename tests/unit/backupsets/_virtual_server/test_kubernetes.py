"""Tests for cvpysdk/backupsets/_virtual_server/kubernetes.py (KubernetesBackupset)."""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.backupsets._virtual_server.kubernetes import KubernetesBackupset
from cvpysdk.backupsets.vsbackupset import VSBackupset


@pytest.mark.unit
class TestKubernetesBackupsetInheritance:
    def test_inherits_vsbackupset(self):
        assert issubclass(KubernetesBackupset, VSBackupset)

    def test_has_refresh_method(self):
        assert hasattr(KubernetesBackupset, "refresh")

    def test_has_application_groups_property(self):
        assert isinstance(KubernetesBackupset.__dict__.get("application_groups"), property)


@pytest.mark.unit
class TestKubernetesBackupsetApplicationGroups:
    def _make_instance(self):
        inst = object.__new__(KubernetesBackupset)
        inst._application_groups = None
        inst._blr_pair_details = None
        return inst

    @patch("cvpysdk.backupsets._virtual_server.kubernetes.ApplicationGroups")
    def test_application_groups_lazy_init(self, mock_app_groups_cls):
        inst = self._make_instance()
        mock_app_groups = MagicMock()
        mock_app_groups_cls.return_value = mock_app_groups
        result = inst.application_groups
        mock_app_groups_cls.assert_called_once_with(inst)
        assert result == mock_app_groups

    @patch("cvpysdk.backupsets._virtual_server.kubernetes.ApplicationGroups")
    def test_application_groups_caches_result(self, mock_app_groups_cls):
        inst = self._make_instance()
        mock_app_groups = MagicMock()
        mock_app_groups_cls.return_value = mock_app_groups
        _ = inst.application_groups
        _ = inst.application_groups
        mock_app_groups_cls.assert_called_once()

    def test_refresh_resets_application_groups(self):
        inst = self._make_instance()
        inst._application_groups = MagicMock()
        # Mock the super().refresh()
        with patch.object(VSBackupset, "refresh"):
            inst.refresh()
        assert inst._application_groups is None
