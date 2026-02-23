"""Unit tests for cvpysdk.deployment.deploymentconstants module."""

import pytest

from cvpysdk.deployment.deploymentconstants import (
    DownloadOptions,
    DownloadPackages,
    InstallUpdateOptions,
    OSNameIDMapping,
    UnixDownloadFeatures,
    WindowsDownloadFeatures,
)


@pytest.mark.unit
class TestDownloadOptions:
    """Tests for DownloadOptions enum."""

    def test_latest_servicepack(self):
        assert DownloadOptions.LATEST_SERVICEPACK.value == "latest service pack"

    def test_latest_hotfixes(self):
        assert (
            DownloadOptions.LATEST_HOTFIXES.value
            == "latest hotfixes for the installed service pack"
        )

    def test_servicepack_and_hotfixes(self):
        assert DownloadOptions.SERVICEPACK_AND_HOTFIXES.value == "service pack and hotfixes"

    def test_enum_count(self):
        assert len(DownloadOptions) == 3


@pytest.mark.unit
class TestDownloadPackages:
    """Tests for DownloadPackages enum."""

    def test_windows_64(self):
        assert DownloadPackages.WINDOWS_64.value == "WINDOWS_X64"

    def test_windows_32(self):
        assert DownloadPackages.WINDOWS_32.value == "WINDOWS_X32"

    def test_unix_linux64(self):
        assert DownloadPackages.UNIX_LINUX64.value == "LINUX_X86_64"

    def test_unix_mac(self):
        assert DownloadPackages.UNIX_MAC.value == "MAC_OS"

    def test_all_values_are_strings(self):
        for member in DownloadPackages:
            assert isinstance(member.value, str)


@pytest.mark.unit
class TestUnixDownloadFeatures:
    """Tests for UnixDownloadFeatures enum."""

    def test_file_system(self):
        assert UnixDownloadFeatures.FILE_SYSTEM.value == 1101

    def test_media_agent(self):
        assert UnixDownloadFeatures.MEDIA_AGENT.value == 1301

    def test_oracle(self):
        assert UnixDownloadFeatures.ORACLE.value == 1204

    def test_commserve(self):
        assert UnixDownloadFeatures.COMMSERVE.value == 1020

    def test_all_values_are_ints(self):
        for member in UnixDownloadFeatures:
            assert isinstance(member.value, int)


@pytest.mark.unit
class TestWindowsDownloadFeatures:
    """Tests for WindowsDownloadFeatures enum."""

    def test_file_system(self):
        assert WindowsDownloadFeatures.FILE_SYSTEM.value == 702

    def test_media_agent(self):
        assert WindowsDownloadFeatures.MEDIA_AGENT.value == 51

    def test_commserve(self):
        assert WindowsDownloadFeatures.COMMSERVE.value == 20

    def test_sql_server(self):
        assert WindowsDownloadFeatures.SQLSERVER.value == 353

    def test_all_values_are_ints(self):
        for member in WindowsDownloadFeatures:
            assert isinstance(member.value, int)


@pytest.mark.unit
class TestOSNameIDMapping:
    """Tests for OSNameIDMapping enum."""

    def test_windows_64(self):
        assert OSNameIDMapping.WINDOWS_64.value == 3

    def test_unix_linux64(self):
        assert OSNameIDMapping.UNIX_LINUX64.value == 16

    def test_all_values_are_ints(self):
        for member in OSNameIDMapping:
            assert isinstance(member.value, int)


@pytest.mark.unit
class TestInstallUpdateOptions:
    """Tests for InstallUpdateOptions enum."""

    def test_update_install_cv(self):
        assert InstallUpdateOptions.UPDATE_INSTALL_CV.value == 1

    def test_update_install_sql(self):
        assert InstallUpdateOptions.UPDATE_INSTALL_SQL.value == 2

    def test_hyperscale_os_updates(self):
        assert InstallUpdateOptions.UPDATE_INSTALL_HYPERSCALE_OS_UPDATES.value == 16

    def test_bitwise_combination(self):
        combined = (
            InstallUpdateOptions.UPDATE_INSTALL_CV.value
            | InstallUpdateOptions.UPDATE_INSTALL_SQL.value
        )
        assert combined == 3
