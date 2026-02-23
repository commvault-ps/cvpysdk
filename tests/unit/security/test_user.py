import pytest

from cvpysdk.security.user import User, Users


@pytest.mark.unit
class TestUsers:
    def test_class_exists(self):
        assert Users is not None

    def test_has_repr(self):
        assert hasattr(Users, "__repr__")

    def test_has_has_user(self):
        assert callable(getattr(Users, "has_user", None))


@pytest.mark.unit
class TestUser:
    def test_class_exists(self):
        assert User is not None

    def test_has_repr(self):
        assert hasattr(User, "__repr__")
