"""Unit tests for cvpysdk/instances/lndbinstance.py"""

import pytest

from cvpysdk.instance import Instance


@pytest.mark.unit
class TestLNDBInstance:
    """Tests for the LNDBInstance class."""

    def test_inherits_instance(self):
        """Test that LNDBInstance is a subclass of Instance."""
        from cvpysdk.instances.lndbinstance import LNDBInstance

        assert issubclass(LNDBInstance, Instance)

    def test_restore_common_options_json_raises_for_non_dict(self):
        """Test _restore_common_options_json raises SDKException for non-dict input."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.lndbinstance import LNDBInstance

        inst = object.__new__(LNDBInstance)
        with pytest.raises(SDKException):
            inst._restore_common_options_json("not_a_dict")

    def test_restore_common_options_json_sets_values(self):
        """Test _restore_common_options_json sets values from common_options_dict."""
        from cvpysdk.instances.lndbinstance import LNDBInstance

        inst = object.__new__(LNDBInstance)
        value = {
            "common_options_dict": {
                "doNotReplayTransactLogs": True,
                "recoverWait": True,
                "recoverZap": False,
            }
        }
        inst._restore_common_options_json(value)

        assert inst._commonoption_restore_json["doNotReplayTransactLogs"] is True
        assert inst._commonoption_restore_json["recoverWait"] is True
        assert inst._commonoption_restore_json["recoverZap"] is False

    def test_restore_common_options_json_disaster_recovery(self):
        """Test _restore_common_options_json adds disaster recovery keys."""
        from cvpysdk.instances.lndbinstance import LNDBInstance

        inst = object.__new__(LNDBInstance)
        value = {
            "common_options_dict": {
                "disasterRecovery": True,
                "skipErrorsAndContinue": True,
            }
        }
        inst._restore_common_options_json(value)

        assert inst._commonoption_restore_json["disasterRecovery"] is True
        assert inst._commonoption_restore_json["skipErrorsAndContinue"] is True
