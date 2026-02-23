import pytest

from cvpysdk.security.role import Role, Roles


@pytest.mark.unit
class TestRoles:
    def test_class_exists(self):
        assert Roles is not None

    def test_has_repr(self):
        assert hasattr(Roles, "__repr__")

    def test_has_has_role(self):
        assert callable(getattr(Roles, "has_role", None))


@pytest.mark.unit
class TestRole:
    def test_class_exists(self):
        assert Role is not None

    def test_has_repr(self):
        assert hasattr(Role, "__repr__")
