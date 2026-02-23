import pytest

from cvpysdk.activateapps.sensitive_data_governance import Project, Projects


@pytest.mark.unit
class TestProjects:
    def test_class_exists(self):
        assert Projects is not None

    def test_has_repr(self):
        assert hasattr(Projects, "__repr__")


@pytest.mark.unit
class TestProject:
    def test_class_exists(self):
        assert Project is not None
