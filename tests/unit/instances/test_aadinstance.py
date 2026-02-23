"""Unit tests for cvpysdk/instances/aadinstance.py"""

from unittest.mock import MagicMock

import pytest

from cvpysdk.instance import Instance


@pytest.mark.unit
class TestAzureAdInstance:
    """Tests for the AzureAdInstance class."""

    def test_inherits_instance(self):
        """Test that AzureAdInstance is a subclass of Instance."""
        from cvpysdk.instances.aadinstance import AzureAdInstance

        assert issubclass(AzureAdInstance, Instance)

    def test_restore_in_place_with_to_time(self):
        """Test _restore_in_place sets timeRange when to_time is provided."""
        from cvpysdk.instances.aadinstance import AzureAdInstance

        inst = object.__new__(AzureAdInstance)
        mock_json = {
            "taskInfo": {
                "subTasks": [
                    {
                        "options": {
                            "restoreOptions": {
                                "browseOption": {
                                    "timeRange": {
                                        "toTime": 0,
                                        "toTimeValue": "some_val",
                                    }
                                },
                                "commonOptions": {"unconditionalOverwrite": False},
                            }
                        }
                    }
                ]
            }
        }
        inst._restore_json = MagicMock(return_value=mock_json)
        inst._process_restore_response = MagicMock(return_value="job_obj")

        kwargs = {
            "to_time": 1234567,
            "fs_options": {"overwrite": True},
            "restore_option": {"azureADOption": {"key": "val"}},
        }
        result = inst._restore_in_place(**kwargs)

        time_range = mock_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"][
            "browseOption"
        ]["timeRange"]
        assert time_range["toTime"] == 1234567
        assert "toTimeValue" not in time_range
        assert result == "job_obj"

    def test_restore_in_place_sets_overwrite(self):
        """Test _restore_in_place sets unconditionalOverwrite from fs_options."""
        from cvpysdk.instances.aadinstance import AzureAdInstance

        inst = object.__new__(AzureAdInstance)
        mock_json = {
            "taskInfo": {
                "subTasks": [
                    {
                        "options": {
                            "restoreOptions": {
                                "browseOption": {"timeRange": {}},
                                "commonOptions": {"unconditionalOverwrite": False},
                            }
                        }
                    }
                ]
            }
        }
        inst._restore_json = MagicMock(return_value=mock_json)
        inst._process_restore_response = MagicMock(return_value="job_obj")

        kwargs = {
            "fs_options": {"overwrite": True},
            "restore_option": {"azureADOption": {"opt": "val"}},
        }
        inst._restore_in_place(**kwargs)

        common_opts = mock_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"][
            "commonOptions"
        ]
        assert common_opts["unconditionalOverwrite"] is True

    def test_restore_in_place_raises_without_azure_option(self):
        """Test _restore_in_place raises SDKException when azureADOption not in restore_option."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.aadinstance import AzureAdInstance

        inst = object.__new__(AzureAdInstance)
        mock_json = {
            "taskInfo": {
                "subTasks": [
                    {
                        "options": {
                            "restoreOptions": {
                                "browseOption": {"timeRange": {}},
                                "commonOptions": {"unconditionalOverwrite": False},
                            }
                        }
                    }
                ]
            }
        }
        inst._restore_json = MagicMock(return_value=mock_json)

        kwargs = {
            "fs_options": {},
            "restore_option": {},
        }

        with pytest.raises(SDKException):
            inst._restore_in_place(**kwargs)

    def test_restore_in_place_sets_azure_ad_option(self):
        """Test _restore_in_place sets azureADOption in restore JSON."""
        from cvpysdk.instances.aadinstance import AzureAdInstance

        inst = object.__new__(AzureAdInstance)
        mock_json = {
            "taskInfo": {
                "subTasks": [
                    {
                        "options": {
                            "restoreOptions": {
                                "browseOption": {"timeRange": {}},
                                "commonOptions": {"unconditionalOverwrite": False},
                            }
                        }
                    }
                ]
            }
        }
        inst._restore_json = MagicMock(return_value=mock_json)
        inst._process_restore_response = MagicMock(return_value="job_obj")

        azure_opt = {"someKey": "someValue"}
        kwargs = {
            "fs_options": {},
            "restore_option": {"azureADOption": azure_opt},
        }
        inst._restore_in_place(**kwargs)

        restore_opts = mock_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]
        assert restore_opts["azureADOption"] == azure_opt
