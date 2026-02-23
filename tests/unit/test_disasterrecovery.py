"""Unit tests for cvpysdk.disasterrecovery module."""

from unittest.mock import MagicMock

import pytest

from cvpysdk.disasterrecovery import DisasterRecoveryManagement
from cvpysdk.exception import SDKException


@pytest.mark.unit
class TestDisasterRecoveryManagement:
    """Tests for the DisasterRecoveryManagement class."""

    def _make_drm(self, mock_commcell, mock_response):
        resp = mock_response(
            json_data={
                "drBackupProperties": {
                    "numberOfMetadata": 5,
                    "backupMetadataFolder": "/dr/path",
                    "useVss": True,
                    "preScanProcess": "",
                    "postScanProcess": "",
                    "preBackupProcess": "",
                    "postBackupProcess": "",
                    "runPostScanProcess": 0,
                    "runPostBackupProcess": 0,
                    "storagePolicy": {"storagePolicyName": "test-sp"},
                    "drRPOIntervalInMinutes": 60,
                    "wildcardSettings": [],
                    "uploadBackupMetadataToCloud": 0,
                    "uploadBackupMetadataToCloudLib": {},
                }
            }
        )
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        return DisasterRecoveryManagement(mock_commcell)

    def test_init_raises_on_api_failure(self, mock_commcell, mock_response):
        resp = mock_response(status_code=500, text="Server Error")
        mock_commcell._cvpysdk_object.make_request.return_value = (False, resp)
        mock_commcell._update_response_ = MagicMock(return_value="Server Error")
        with pytest.raises(SDKException):
            DisasterRecoveryManagement(mock_commcell)
