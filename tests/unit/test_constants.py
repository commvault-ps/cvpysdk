"""Unit tests for cvpysdk/constants.py module."""

import pytest

from cvpysdk.constants import (
    ENTITY_TYPE_MAP,
    TIMEZONES,
    AppIDAName,
    AppIDAType,
    ApplicationGroup,
    HypervisorType,
    InstanceBackupType,
    OSType,
    SQLDefines,
    VSAFailOverStatus,
    VSALiveSyncStatus,
    VSAObjects,
    VsInstanceType,
)


@pytest.mark.unit
class TestTimezones:
    """Tests for TIMEZONES dictionary."""

    def test_timezones_is_dict(self):
        assert isinstance(TIMEZONES, dict)

    def test_timezones_not_empty(self):
        assert len(TIMEZONES) > 0

    def test_well_known_timezone_exists(self):
        assert "America/New_York" in TIMEZONES
        assert "Europe/London" in TIMEZONES
        assert "Asia/Kolkata" in TIMEZONES
        assert "UTC" in TIMEZONES

    def test_timezone_values_are_strings(self):
        for key, value in TIMEZONES.items():
            assert isinstance(key, str)
            assert isinstance(value, str)


@pytest.mark.unit
class TestEntityTypeMap:
    """Tests for ENTITY_TYPE_MAP dictionary."""

    def test_entity_type_map_is_dict(self):
        assert isinstance(ENTITY_TYPE_MAP, dict)

    def test_known_entity_types(self):
        assert ENTITY_TYPE_MAP[1] == "file server"
        assert ENTITY_TYPE_MAP[3] == "hypervisor"
        assert ENTITY_TYPE_MAP[33] == "plan"

    def test_keys_are_integers(self):
        for key in ENTITY_TYPE_MAP:
            assert isinstance(key, int)


@pytest.mark.unit
class TestHypervisorType:
    """Tests for HypervisorType enum."""

    def test_vmware_value(self):
        assert HypervisorType.VIRTUAL_CENTER.value == "VMware"

    def test_azure_value(self):
        assert HypervisorType.AZURE.value == "Azure"

    def test_aws_value(self):
        assert HypervisorType.AMAZON_AWS.value == "Amazon Web Services"

    def test_google_cloud_value(self):
        assert HypervisorType.GOOGLE_CLOUD.value == "Google Cloud Platform"

    def test_enum_membership(self):
        assert HypervisorType("VMware") == HypervisorType.VIRTUAL_CENTER


@pytest.mark.unit
class TestAppIDAType:
    """Tests for AppIDAType enum."""

    def test_windows_fs_value(self):
        assert AppIDAType.WINDOWS_FILE_SYSTEM.value == 33

    def test_linux_fs_value(self):
        assert AppIDAType.LINUX_FILE_SYSTEM.value == 29

    def test_virtual_server_value(self):
        assert AppIDAType.VIRTUAL_SERVER.value == 106


@pytest.mark.unit
class TestAppIDAName:
    """Tests for AppIDAName enum."""

    def test_file_system_name(self):
        assert AppIDAName.FILE_SYSTEM.value == "File System"

    def test_virtual_server_name(self):
        assert AppIDAName.VIRTUAL_SERVER.value == "Virtual Server"


@pytest.mark.unit
class TestInstanceBackupType:
    """Tests for InstanceBackupType enum."""

    def test_full_value(self):
        assert InstanceBackupType.FULL.value == "full"

    def test_incremental_value(self):
        assert InstanceBackupType.INCREMENTAL.value == "incremental"

    def test_cumulative_matches_incremental(self):
        assert InstanceBackupType.CUMULATIVE.value == "incremental"


@pytest.mark.unit
class TestSQLDefines:
    """Tests for SQLDefines class."""

    def test_database_restore_constant(self):
        assert SQLDefines.DATABASE_RESTORE == "DATABASE_RESTORE"

    def test_state_recover_constant(self):
        assert SQLDefines.STATE_RECOVER == "STATE_RECOVER"


@pytest.mark.unit
class TestVSAEnums:
    """Tests for VSA-related enums."""

    def test_vsa_objects_server(self):
        assert VSAObjects.SERVER.value == 1

    def test_vsa_objects_vm(self):
        assert VSAObjects.VM.value == 9

    def test_vsa_live_sync_in_sync(self):
        assert VSALiveSyncStatus.IN_SYNC.value == 1

    def test_vsa_failover_complete(self):
        assert VSAFailOverStatus.FAILOVER_COMPLETE.value == 1


@pytest.mark.unit
class TestApplicationGroup:
    """Tests for ApplicationGroup enum."""

    def test_windows_exists(self):
        assert ApplicationGroup.WINDOWS is not None

    def test_unix_exists(self):
        assert ApplicationGroup.UNIX is not None


@pytest.mark.unit
class TestVsInstanceType:
    """Tests for VsInstanceType class."""

    def test_vmware_type(self):
        assert VsInstanceType.VSINSTANCE_TYPE[101] == "vmware"

    def test_hyperv_type(self):
        assert VsInstanceType.VSINSTANCE_TYPE[102] == "hyperv"

    def test_aws_type(self):
        assert VsInstanceType.VSINSTANCE_TYPE[301] == "amazon_web_services"


@pytest.mark.unit
class TestOSType:
    """Tests for OSType enum."""

    def test_windows_value(self):
        assert OSType.WINDOWS.value == 1

    def test_unix_value(self):
        assert OSType.UNIX.value == 2
