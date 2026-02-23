"""Unit tests for cvpysdk/instances/splunkinstance.py"""

from unittest.mock import patch

import pytest

from cvpysdk.instance import Instance


@pytest.mark.unit
class TestSplunkInstance:
    """Tests for the SplunkInstance class."""

    def test_inherits_bigdataapps_instance(self):
        """Test that SplunkInstance is a subclass of BigDataAppsInstance."""
        from cvpysdk.instances.bigdataappsinstance import BigDataAppsInstance
        from cvpysdk.instances.splunkinstance import SplunkInstance

        assert issubclass(SplunkInstance, BigDataAppsInstance)

    def test_inherits_instance(self):
        """Test that SplunkInstance is transitively a subclass of Instance."""
        from cvpysdk.instances.splunkinstance import SplunkInstance

        assert issubclass(SplunkInstance, Instance)

    def test_has_restore_json_method(self):
        """Test that SplunkInstance has _restore_json method."""
        from cvpysdk.instances.splunkinstance import SplunkInstance

        assert callable(getattr(SplunkInstance, "_restore_json", None))

    def _make_base_json(self):
        """Helper to create a base restore JSON structure."""
        return {
            "taskInfo": {
                "subTasks": [
                    {
                        "options": {
                            "restoreOptions": {
                                "browseOption": {"backupset": {}},
                                "commonOptions": {},
                                "destination": {
                                    "destClient": {},
                                    "destinationInstance": {},
                                },
                            }
                        }
                    }
                ]
            }
        }

    def _make_instance(self):
        """Helper to create a SplunkInstance with mocked internals."""
        from cvpysdk.instances.splunkinstance import SplunkInstance

        inst = object.__new__(SplunkInstance)
        inst._properties = {
            "instance": {
                "clientId": 1,
                "applicationId": 64,
                "instanceId": 10,
                "instanceName": "splunk_inst",
            }
        }
        inst._instance = inst._properties["instance"]
        inst._restore_association = None
        return inst

    def test_restore_json_inplace_sets_out_of_place_false(self):
        """Test _restore_json sets outofPlaceRestore=False when no destination_entity."""
        inst = self._make_instance()
        base_json = self._make_base_json()

        with patch(
            "cvpysdk.instances.bigdataappsinstance.BigDataAppsInstance._restore_json",
            return_value=base_json,
        ):
            result = inst._restore_json(paths=["/data"])
            dist_opts = result["taskInfo"]["subTasks"][0]["options"]["restoreOptions"][
                "distributedAppsRestoreOptions"
            ]
            assert dist_opts["distributedRestore"] is True
            assert dist_opts["splunkRestoreOptions"]["outofPlaceRestore"] is False

    def test_restore_json_out_of_place_sets_flag_true(self):
        """Test _restore_json sets outofPlaceRestore=True when destination_entity given."""
        inst = self._make_instance()
        base_json = self._make_base_json()

        dest_entity = {
            "clientId": 2,
            "clientName": "dest_client",
            "instanceName": "dest_inst",
            "appName": "Big Data Apps",
            "instanceId": 20,
            "applicationId": 64,
        }

        with patch(
            "cvpysdk.instances.bigdataappsinstance.BigDataAppsInstance._restore_json",
            return_value=base_json,
        ):
            result = inst._restore_json(paths=["/data"], destination_entity=dest_entity)
            dist_opts = result["taskInfo"]["subTasks"][0]["options"]["restoreOptions"][
                "distributedAppsRestoreOptions"
            ]
            assert dist_opts["splunkRestoreOptions"]["outofPlaceRestore"] is True

    def test_restore_json_sets_unconditional_overwrite(self):
        """Test _restore_json sets unconditionalOverwrite to True."""
        inst = self._make_instance()
        base_json = self._make_base_json()

        with patch(
            "cvpysdk.instances.bigdataappsinstance.BigDataAppsInstance._restore_json",
            return_value=base_json,
        ):
            result = inst._restore_json(paths=["/data"])
            common_opts = result["taskInfo"]["subTasks"][0]["options"]["restoreOptions"][
                "commonOptions"
            ]
            assert common_opts["unconditionalOverwrite"] is True
            assert common_opts["skip"] is False

    def test_restore_json_sets_qr_option(self):
        """Test _restore_json sets qrOption with correct application id."""
        inst = self._make_instance()
        base_json = self._make_base_json()

        with patch(
            "cvpysdk.instances.bigdataappsinstance.BigDataAppsInstance._restore_json",
            return_value=base_json,
        ):
            result = inst._restore_json(paths=["/data"])
            qr_opt = result["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["qrOption"]
            assert qr_opt["destAppTypeId"] == 64
