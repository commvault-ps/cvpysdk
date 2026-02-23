"""Unit tests for cvpysdk.deployment.uninstall module."""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.deployment.uninstall import UNINSTALL_SELECTED_PACKAGES, Uninstall
from cvpysdk.exception import SDKException


@pytest.mark.unit
class TestUninstall:
    """Tests for the Uninstall class."""

    def _create_uninstall(self, mock_commcell):
        return Uninstall(mock_commcell)

    def test_init(self, mock_commcell):
        u = self._create_uninstall(mock_commcell)
        assert u._commcell_object is mock_commcell

    def test_uninstall_selected_packages_constant(self):
        assert UNINSTALL_SELECTED_PACKAGES == 6

    def test_uninstall_software_invalid_client_name(self, mock_commcell):
        u = self._create_uninstall(mock_commcell)
        with pytest.raises(SDKException):
            u.uninstall_software(client_name=123)

    @patch("cvpysdk.deployment.uninstall.Job")
    def test_uninstall_software_success(self, mock_job, mock_commcell, mock_response):
        u = self._create_uninstall(mock_commcell)
        resp = mock_response(json_data={"jobIds": [600]})
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        mock_job.return_value = MagicMock()
        result = u.uninstall_software(client_name="my_client")
        assert result is not None
        mock_job.assert_called_once()

    @patch("cvpysdk.deployment.uninstall.Job")
    def test_uninstall_software_with_composition(self, mock_job, mock_commcell, mock_response):
        u = self._create_uninstall(mock_commcell)
        resp = mock_response(json_data={"jobIds": [601]})
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        mock_job.return_value = MagicMock()
        composition = [
            {
                "activateClient": True,
                "packageDeliveryOption": 0,
                "components": {
                    "componentInfo": [{"osType": "Windows", "ComponentName": "Index Store"}]
                },
            }
        ]
        result = u.uninstall_software(client_name="my_client", client_composition=composition)
        assert result is not None

    def test_uninstall_software_empty_response(self, mock_commcell, mock_response):
        u = self._create_uninstall(mock_commcell)
        resp = mock_response()
        resp.json.return_value = None
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        with pytest.raises(SDKException):
            u.uninstall_software(client_name="my_client")

    def test_uninstall_software_no_job_ids(self, mock_commcell, mock_response):
        u = self._create_uninstall(mock_commcell)
        resp = mock_response(json_data={"otherKey": "value"})
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        with pytest.raises(SDKException):
            u.uninstall_software(client_name="my_client")

    @patch("cvpysdk.deployment.uninstall.Job")
    def test_uninstall_force_default_true(self, mock_job, mock_commcell, mock_response):
        """Verify default force_uninstall=True is used in request."""
        u = self._create_uninstall(mock_commcell)
        resp = mock_response(json_data={"jobIds": [700]})
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        mock_job.return_value = MagicMock()
        u.uninstall_software(client_name="my_client")
        call_args = mock_commcell._cvpysdk_object.make_request.call_args
        request_json = call_args[0][2]
        force_flag = request_json["taskInfo"]["subTasks"][0]["options"]["adminOpts"][
            "clientInstallOption"
        ]["forceUninstall"]
        assert force_flag is True
