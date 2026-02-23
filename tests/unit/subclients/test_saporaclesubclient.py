"""Unit tests for cvpysdk/subclients/saporaclesubclient.py"""

import pytest

from cvpysdk.subclient import Subclient
from cvpysdk.subclients.saporaclesubclient import SAPOracleSubclient


@pytest.mark.unit
class TestSAPOracleSubclient:
    """Tests for the SAPOracleSubclient class."""

    def test_inherits_subclient(self):
        """SAPOracleSubclient should inherit from Subclient."""
        assert issubclass(SAPOracleSubclient, Subclient)

    def test_has_key_properties(self):
        """SAPOracleSubclient should have expected properties."""
        assert hasattr(SAPOracleSubclient, "data_sp")
        assert hasattr(SAPOracleSubclient, "sapBackupMode")
        assert hasattr(SAPOracleSubclient, "sapBackupDevice")

    def test_data_sp_returns_policy_name(self):
        """data_sp should return storage policy name."""
        sub = object.__new__(SAPOracleSubclient)
        sub._commonProperties = {
            "storageDevice": {"dataBackupStoragePolicy": {"storagePolicyName": "test_policy"}}
        }
        assert sub.data_sp == "test_policy"

    def test_sap_backup_mode_returns_value(self):
        """sapBackupMode should return sap backup mode value."""
        sub = object.__new__(SAPOracleSubclient)
        sub._sapForOracleSubclientProp = {"sapBackupMode": 0}
        assert sub.sapBackupMode == 0

    def test_sap_backup_device_returns_value(self):
        """sapBackupDevice should return sap backup device value."""
        sub = object.__new__(SAPOracleSubclient)
        sub._sapForOracleSubclientProp = {"sapBackupDevice": 1}
        assert sub.sapBackupDevice == 1

    def test_get_subclient_properties_json_structure(self):
        """_get_subclient_properties_json should return proper dict structure."""
        sub = object.__new__(SAPOracleSubclient)
        sub._subClientEntity = {"subclientId": 1}
        sub._commonProperties = {"prop": "val"}
        sub._sapForOracleSubclientProp = {"sapBackupMode": 0}
        result = sub._get_subclient_properties_json()
        assert "subClientProperties" in result
        props = result["subClientProperties"]
        assert "subClientEntity" in props
        assert "commonProperties" in props
        assert "sapForOracleSubclientProp" in props
