"""Unit tests for cvpysdk/instances/sharepointinstance.py"""

from unittest.mock import MagicMock

import pytest

from cvpysdk.instance import Instance


@pytest.mark.unit
class TestSharepointInstance:
    """Tests for the SharepointInstance class."""

    def test_inherits_instance(self):
        """Test that SharepointInstance is a subclass of Instance."""
        from cvpysdk.instances.sharepointinstance import SharepointInstance

        assert issubclass(SharepointInstance, Instance)

    def test_has_restore_json_method(self):
        """Test that SharepointInstance has _restore_json method."""
        from cvpysdk.instances.sharepointinstance import SharepointInstance

        assert callable(getattr(SharepointInstance, "_restore_json", None))

    def test_has_restore_v1_json_method(self):
        """Test that SharepointInstance has _restore_v1_json method."""
        from cvpysdk.instances.sharepointinstance import SharepointInstance

        assert callable(getattr(SharepointInstance, "_restore_v1_json", None))

    def test_restore_browse_option_json_raises_for_non_dict(self):
        """Test _restore_browse_option_json raises SDKException for non-dict."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.sharepointinstance import SharepointInstance

        inst = object.__new__(SharepointInstance)
        with pytest.raises(SDKException):
            inst._restore_browse_option_json("not_a_dict")

    def test_restore_common_options_json_raises_for_non_dict(self):
        """Test _restore_common_options_json raises SDKException for non-dict."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.sharepointinstance import SharepointInstance

        inst = object.__new__(SharepointInstance)
        with pytest.raises(SDKException):
            inst._restore_common_options_json("not_a_dict")

    def test_restore_common_options_json_sets_overwrite(self):
        """Test _restore_common_options_json correctly sets unconditional_overwrite."""
        from cvpysdk.instances.sharepointinstance import SharepointInstance

        inst = object.__new__(SharepointInstance)
        inst._restore_common_options_json({"unconditional_overwrite": True})
        assert inst._commonoption_restore_json["unconditionalOverwrite"] is True
        assert inst._commonoption_restore_json["skip"] is False

    def test_restore_common_options_json_defaults(self):
        """Test _restore_common_options_json sets correct defaults."""
        from cvpysdk.instances.sharepointinstance import SharepointInstance

        inst = object.__new__(SharepointInstance)
        inst._restore_common_options_json({})
        assert inst._commonoption_restore_json["unconditionalOverwrite"] is False
        assert inst._commonoption_restore_json["skip"] is True
        assert inst._commonoption_restore_json["allVersion"] is True

    def test_restore_destination_json_raises_for_non_dict(self):
        """Test _restore_destination_json raises SDKException for non-dict."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.sharepointinstance import SharepointInstance

        inst = object.__new__(SharepointInstance)
        with pytest.raises(SDKException):
            inst._restore_destination_json("not_a_dict")

    def test_restore_destination_json_sets_values(self):
        """Test _restore_destination_json correctly sets destination values."""
        from cvpysdk.instances.sharepointinstance import SharepointInstance

        inst = object.__new__(SharepointInstance)
        inst._restore_destination_json(
            {
                "in_place": True,
                "client_name": "test_client",
                "client_id": 10,
            }
        )
        assert inst._destination_restore_json["inPlace"] is True
        assert inst._destination_restore_json["destClient"]["clientName"] == "test_client"
        assert inst._destination_restore_json["destClient"]["clientId"] == 10

    def test_restore_browse_option_json_sets_to_time(self):
        """Test _restore_browse_option_json includes toTime when provided."""
        from cvpysdk.instances.sharepointinstance import SharepointInstance

        inst = object.__new__(SharepointInstance)
        inst._commcell_object = MagicMock()
        inst._commcell_object.commcell_id = "2"
        inst._agent_object = MagicMock()
        inst._agent_object._client_object.client_name = "testclient"
        inst._agent_object.agent_name = "SharePoint"
        inst._instance = {"clientId": 1}
        inst._restore_association = {"backupsetId": 5}
        inst._restore_browse_option_json({"to_time": 1234567890})
        assert inst._browse_restore_json["timeRange"]["toTime"] == 1234567890
