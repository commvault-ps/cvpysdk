"""Unit tests for cvpysdk.cleanroom.recovery_groups module."""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.cleanroom.recovery_groups import (
    RecoveryGroup,
    RecoveryGroups,
    RecoveryStatus,
)
from cvpysdk.exception import SDKException


@pytest.mark.unit
class TestRecoveryStatus:
    """Tests for the RecoveryStatus enum."""

    def test_enum_values(self):
        """Test that RecoveryStatus has expected values."""
        assert RecoveryStatus.NO_STATUS.value == 0
        assert RecoveryStatus.NOT_READY.value == 1
        assert RecoveryStatus.READY.value == 2
        assert RecoveryStatus.RECOVERED.value == 3
        assert RecoveryStatus.FAILED.value == 4
        assert RecoveryStatus.RECOVERED_WITH_ERRORS.value == 5
        assert RecoveryStatus.IN_PROGRESS.value == 6
        assert RecoveryStatus.CLEANED_UP.value == 7


@pytest.mark.unit
class TestRecoveryGroups:
    """Tests for the RecoveryGroups collection class."""

    def test_class_exists_and_importable(self):
        """Test that RecoveryGroups can be imported."""
        from cvpysdk.cleanroom import recovery_groups

        assert hasattr(recovery_groups, "RecoveryGroups")

    def test_has_recovery_group_raises_on_non_string(self):
        """Test has_recovery_group raises SDKException for non-string argument."""
        with patch.object(RecoveryGroups, "__init__", lambda self, *a, **k: None):
            obj = RecoveryGroups.__new__(RecoveryGroups)
        obj._recovery_groups = {}
        with pytest.raises(SDKException):
            obj.has_recovery_group(123)

    def test_has_recovery_group_returns_true(self):
        """Test has_recovery_group returns True when group exists."""
        with patch.object(RecoveryGroups, "__init__", lambda self, *a, **k: None):
            obj = RecoveryGroups.__new__(RecoveryGroups)
        obj._recovery_groups = {"group1": "id1"}
        assert obj.has_recovery_group("group1") is True

    def test_has_recovery_group_returns_false(self):
        """Test has_recovery_group returns False when group does not exist."""
        with patch.object(RecoveryGroups, "__init__", lambda self, *a, **k: None):
            obj = RecoveryGroups.__new__(RecoveryGroups)
        obj._recovery_groups = {"group1": "id1"}
        assert obj.has_recovery_group("nonexistent") is False

    def test_get_raises_on_non_string(self):
        """Test get raises SDKException for non-string argument."""
        with patch.object(RecoveryGroups, "__init__", lambda self, *a, **k: None):
            obj = RecoveryGroups.__new__(RecoveryGroups)
        obj._recovery_groups = {}
        with pytest.raises(SDKException):
            obj.get(123)

    def test_get_raises_on_nonexistent_group(self):
        """Test get raises SDKException when group does not exist."""
        with patch.object(RecoveryGroups, "__init__", lambda self, *a, **k: None):
            obj = RecoveryGroups.__new__(RecoveryGroups)
        obj._recovery_groups = {}
        obj._commcell_object = MagicMock()
        with pytest.raises(SDKException):
            obj.get("nonexistent")

    def test_all_groups_property(self):
        """Test all_groups returns the internal dict."""
        with patch.object(RecoveryGroups, "__init__", lambda self, *a, **k: None):
            obj = RecoveryGroups.__new__(RecoveryGroups)
        obj._recovery_groups = {"g1": "1", "g2": "2"}
        assert obj.all_groups == {"g1": "1", "g2": "2"}

    def test_str_representation(self):
        """Test __str__ contains group names."""
        with patch.object(RecoveryGroups, "__init__", lambda self, *a, **k: None):
            obj = RecoveryGroups.__new__(RecoveryGroups)
        obj._recovery_groups = {"group_alpha": "1"}
        result = str(obj)
        assert "group_alpha" in result


@pytest.mark.unit
class TestRecoveryGroup:
    """Tests for the RecoveryGroup entity class."""

    def test_class_exists_and_importable(self):
        """Test that RecoveryGroup can be imported."""
        from cvpysdk.cleanroom import recovery_groups

        assert hasattr(recovery_groups, "RecoveryGroup")

    def test_id_property(self):
        """Test that the id property returns integer id."""
        with patch.object(RecoveryGroup, "__init__", lambda self, *a, **k: None):
            obj = RecoveryGroup.__new__(RecoveryGroup)
        obj._recovery_group_id = "42"
        assert obj.id == 42

    def test_entities_property(self):
        """Test that entities property returns entities from properties."""
        with patch.object(RecoveryGroup, "__init__", lambda self, *a, **k: None):
            obj = RecoveryGroup.__new__(RecoveryGroup)
        obj._properties = {"entities": [{"id": 1}, {"id": 2}]}
        assert len(obj.entities) == 2

    def test_has_expected_methods(self):
        """Test that RecoveryGroup has expected methods."""
        assert hasattr(RecoveryGroup, "recover_all")
        assert hasattr(RecoveryGroup, "refresh")
        assert hasattr(RecoveryGroup, "delete")
        assert hasattr(RecoveryGroup, "_recover_entities")
        assert hasattr(RecoveryGroup, "_get_recovery_group_properties")
