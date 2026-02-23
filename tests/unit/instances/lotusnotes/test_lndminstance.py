"""Unit tests for cvpysdk/instances/lotusnotes/lndminstance.py"""

import pytest

from cvpysdk.instances.lotusnotes.lninstance import LNInstance


@pytest.mark.unit
class TestLNDMInstance:
    """Tests for the LNDMInstance class."""

    def test_inherits_lninstance(self):
        """Test that LNDMInstance is a subclass of LNInstance."""
        from cvpysdk.instances.lotusnotes.lndminstance import LNDMInstance

        assert issubclass(LNDMInstance, LNInstance)

    def test_commonoption_restore_json_raises_for_non_dict(self):
        """Test _commonoption_restore_json raises SDKException for non-dict."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.lotusnotes.lndminstance import LNDMInstance

        inst = object.__new__(LNDMInstance)
        with pytest.raises(SDKException):
            inst._commonoption_restore_json("not_a_dict")

    def test_commonoption_restore_json_sets_values(self):
        """Test _commonoption_restore_json sets expected keys."""
        from cvpysdk.instances.lotusnotes.lndminstance import LNDMInstance

        inst = object.__new__(LNDMInstance)
        value = {
            "common_options_dict": {
                "append": True,
                "skip": False,
                "unconditionalOverwrite": True,
            }
        }
        inst._commonoption_restore_json(value)
        result = inst._commonoption_restore_json
        assert result["append"] is True
        assert result["skip"] is False
        assert result["unconditionalOverwrite"] is True

    def test_commonoption_restore_json_defaults(self):
        """Test _commonoption_restore_json uses defaults for missing keys."""
        from cvpysdk.instances.lotusnotes.lndminstance import LNDMInstance

        inst = object.__new__(LNDMInstance)
        value = {"common_options_dict": {}}
        inst._commonoption_restore_json(value)
        result = inst._commonoption_restore_json
        assert result["append"] is False
        assert result["skip"] is False
        assert result["unconditionalOverwrite"] is True
        assert result["restoreOnlyStubExists"] is False
