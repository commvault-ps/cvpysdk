import pytest

from cvpysdk.security.usergroup import UserGroup, UserGroups


@pytest.mark.unit
class TestUserGroups:
    def test_class_exists(self):
        assert UserGroups is not None

    def test_has_repr(self):
        assert hasattr(UserGroups, "__repr__")

    def test_has_has_user_group(self):
        assert callable(getattr(UserGroups, "has_user_group", None))


@pytest.mark.unit
class TestUserGroup:
    def test_class_exists(self):
        assert UserGroup is not None

    def test_has_repr(self):
        assert hasattr(UserGroup, "__repr__")
