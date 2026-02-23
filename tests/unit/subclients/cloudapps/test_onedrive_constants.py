"""Unit tests for cvpysdk/subclients/cloudapps/onedrive_constants.py"""

import pytest

from cvpysdk.subclients.cloudapps.onedrive_constants import OneDriveConstants


@pytest.mark.unit
class TestOneDriveConstants:
    """Tests for the OneDriveConstants class."""

    def test_index_app_type_value(self):
        """INDEX_APP_TYPE should be 200118."""
        assert OneDriveConstants.INDEX_APP_TYPE == 200118

    def test_instance_value(self):
        """INSTANCE should be 'OneDrive'."""
        assert OneDriveConstants.INSTANCE == "OneDrive"

    def test_index_app_type_is_integer(self):
        """INDEX_APP_TYPE should be an integer."""
        assert isinstance(OneDriveConstants.INDEX_APP_TYPE, int)

    def test_instance_is_string(self):
        """INSTANCE should be a string."""
        assert isinstance(OneDriveConstants.INSTANCE, str)
