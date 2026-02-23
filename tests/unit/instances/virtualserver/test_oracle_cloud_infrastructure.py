"""Unit tests for cvpysdk/instances/virtualserver/oracle_cloud_infrastructure.py"""

import pytest

from cvpysdk.instances.vsinstance import VirtualServerInstance


@pytest.mark.unit
class TestOracleCloudInfrastructureInstance:
    """Tests for the OracleCloudInfrastructureInstance class."""

    def test_inherits_virtual_server_instance(self):
        """Test that OracleCloudInfrastructureInstance is a subclass of VirtualServerInstance."""
        from cvpysdk.instances.virtualserver.oracle_cloud_infrastructure import (
            OracleCloudInfrastructureInstance,
        )

        assert issubclass(OracleCloudInfrastructureInstance, VirtualServerInstance)

    def test_server_name_property(self):
        """Test server_name returns the server name list."""
        from cvpysdk.instances.virtualserver.oracle_cloud_infrastructure import (
            OracleCloudInfrastructureInstance,
        )

        inst = object.__new__(OracleCloudInfrastructureInstance)
        inst._server_name = ["oci_pseudo"]
        assert inst.server_name == ["oci_pseudo"]

    def test_server_host_name_property(self):
        """Test server_host_name returns the host name list."""
        from cvpysdk.instances.virtualserver.oracle_cloud_infrastructure import (
            OracleCloudInfrastructureInstance,
        )

        inst = object.__new__(OracleCloudInfrastructureInstance)
        inst._server_host_name = []
        assert inst.server_host_name == []

    def test_get_instance_properties_json_structure(self):
        """Test _get_instance_properties_json returns correct structure."""
        from cvpysdk.instances.virtualserver.oracle_cloud_infrastructure import (
            OracleCloudInfrastructureInstance,
        )

        inst = object.__new__(OracleCloudInfrastructureInstance)
        inst._instance = {"clientName": "oci_client"}
        inst._instanceActivityControl = {"enableBackup": True}
        inst._virtualserverinstance = {
            "vsInstanceType": 1,
            "associatedClients": {"memberServers": []},
            "vmwareVendor": {},
        }
        result = inst._get_instance_properties_json()
        assert "instanceProperties" in result
