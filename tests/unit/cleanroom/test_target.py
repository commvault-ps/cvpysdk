"""Unit tests for cvpysdk.cleanroom.target module."""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.cleanroom.target import CleanroomTarget, CleanroomTargets
from cvpysdk.exception import SDKException


@pytest.mark.unit
class TestCleanroomTargets:
    """Tests for the CleanroomTargets collection class."""

    def test_class_exists_and_importable(self):
        from cvpysdk.cleanroom import target

        assert hasattr(target, "CleanroomTargets")

    def test_has_cleanroom_target_returns_true(self):
        with patch.object(CleanroomTargets, "__init__", lambda self, *a, **k: None):
            obj = CleanroomTargets.__new__(CleanroomTargets)
        obj._cleanroom_targets = {"target1": "id1"}
        assert obj.has_cleanroom_target("target1") is True

    def test_has_cleanroom_target_returns_false(self):
        with patch.object(CleanroomTargets, "__init__", lambda self, *a, **k: None):
            obj = CleanroomTargets.__new__(CleanroomTargets)
        obj._cleanroom_targets = {"target1": "id1"}
        assert obj.has_cleanroom_target("nonexistent") is False

    def test_get_raises_on_nonexistent_target(self):
        with patch.object(CleanroomTargets, "__init__", lambda self, *a, **k: None):
            obj = CleanroomTargets.__new__(CleanroomTargets)
        obj._cleanroom_targets = {}
        obj._commcell_object = MagicMock()
        with pytest.raises(SDKException):
            obj.get("nonexistent")

    def test_all_targets_property(self):
        with patch.object(CleanroomTargets, "__init__", lambda self, *a, **k: None):
            obj = CleanroomTargets.__new__(CleanroomTargets)
        obj._cleanroom_targets = {"t1": "1", "t2": "2"}
        assert obj.all_targets == {"t1": "1", "t2": "2"}

    def test_str_representation(self):
        with patch.object(CleanroomTargets, "__init__", lambda self, *a, **k: None):
            obj = CleanroomTargets.__new__(CleanroomTargets)
        obj._cleanroom_targets = {"my_target": "1"}
        result = str(obj)
        assert "my_target" in result


@pytest.mark.unit
class TestCleanroomTarget:
    """Tests for the CleanroomTarget entity class."""

    def test_class_exists_and_importable(self):
        from cvpysdk.cleanroom import target

        assert hasattr(target, "CleanroomTarget")

    def test_cleanroom_target_id_property(self):
        with patch.object(CleanroomTarget, "__init__", lambda self, *a, **k: None):
            obj = CleanroomTarget.__new__(CleanroomTarget)
        obj._cleanroom_target_id = "42"
        assert obj.cleanroom_target_id == "42"

    def test_cleanroom_target_name_property(self):
        with patch.object(CleanroomTarget, "__init__", lambda self, *a, **k: None):
            obj = CleanroomTarget.__new__(CleanroomTarget)
        obj._cleanroom_target_name = "my_target"
        assert obj.cleanroom_target_name == "my_target"

    def test_set_policy_type_amazon(self):
        with patch.object(CleanroomTarget, "__init__", lambda self, *a, **k: None):
            obj = CleanroomTarget.__new__(CleanroomTarget)
        obj._policy_type = None
        obj._set_policy_type("AMAZON")
        assert obj._policy_type == 1

    def test_set_policy_type_vmware(self):
        with patch.object(CleanroomTarget, "__init__", lambda self, *a, **k: None):
            obj = CleanroomTarget.__new__(CleanroomTarget)
        obj._policy_type = None
        obj._set_policy_type("VMW_BACKUP_LABTEMPLATE")
        assert obj._policy_type == 13

    def test_set_policy_type_microsoft(self):
        with patch.object(CleanroomTarget, "__init__", lambda self, *a, **k: None):
            obj = CleanroomTarget.__new__(CleanroomTarget)
        obj._policy_type = None
        obj._set_policy_type("MICROSOFT")
        assert obj._policy_type == 2

    def test_set_policy_type_unknown(self):
        with patch.object(CleanroomTarget, "__init__", lambda self, *a, **k: None):
            obj = CleanroomTarget.__new__(CleanroomTarget)
        obj._policy_type = None
        obj._set_policy_type("UNKNOWN_TYPE")
        assert obj._policy_type == -1

    def test_has_delete_method(self):
        assert hasattr(CleanroomTarget, "delete")
        assert hasattr(CleanroomTarget, "refresh")
