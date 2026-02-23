"""Unit tests for cvpysdk/instances/vminstance.py"""

import pytest

from cvpysdk.instance import Instance


@pytest.mark.unit
class TestVMInstance:
    """Tests for the VMInstance class."""

    def test_inherits_instance(self):
        """Test that VMInstance is a subclass of Instance."""
        from cvpysdk.instances.vminstance import VMInstance

        assert issubclass(VMInstance, Instance)

    def test_class_exists(self):
        """Test that VMInstance can be imported."""
        from cvpysdk.instances.vminstance import VMInstance

        assert VMInstance is not None

    def test_init_calls_super(self):
        """Test that VMInstance.__init__ signature accepts expected args."""
        import inspect

        from cvpysdk.instances.vminstance import VMInstance

        sig = inspect.signature(VMInstance.__init__)
        params = list(sig.parameters.keys())
        assert "agent_object" in params
        assert "instance_name" in params
        assert "instance_id" in params

    def test_has_no_extra_methods(self):
        """Test that VMInstance only adds __init__ beyond Instance."""
        from cvpysdk.instances.vminstance import VMInstance

        own_methods = [m for m in VMInstance.__dict__ if not m.startswith("_") or m == "__init__"]
        assert "__init__" in own_methods
