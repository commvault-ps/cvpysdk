"""Unit tests for cvpysdk/subclients/cloudapps/google_constants.py"""

import pytest

from cvpysdk.subclients.cloudapps.google_constants import (
    GDRIVE_DISCOVERY_TYPE,
    GDRIVE_INDEX_APP_TYPE,
    GMAIL_DISCOVERY_TYPE,
    GMAIL_INDEX_APP_TYPE,
)


@pytest.mark.unit
class TestGoogleConstants:
    """Tests for the google_constants module constants."""

    def test_gmail_index_app_type_value(self):
        """GMAIL_INDEX_APP_TYPE should be 200136."""
        assert GMAIL_INDEX_APP_TYPE == 200136

    def test_gdrive_index_app_type_value(self):
        """GDRIVE_INDEX_APP_TYPE should be 200137."""
        assert GDRIVE_INDEX_APP_TYPE == 200137

    def test_gmail_discovery_type_value(self):
        """GMAIL_DISCOVERY_TYPE should be 22."""
        assert GMAIL_DISCOVERY_TYPE == 22

    def test_gdrive_discovery_type_value(self):
        """GDRIVE_DISCOVERY_TYPE should be 24."""
        assert GDRIVE_DISCOVERY_TYPE == 24

    def test_all_constants_are_integers(self):
        """All Google constants should be integers."""
        assert isinstance(GMAIL_INDEX_APP_TYPE, int)
        assert isinstance(GDRIVE_INDEX_APP_TYPE, int)
        assert isinstance(GMAIL_DISCOVERY_TYPE, int)
        assert isinstance(GDRIVE_DISCOVERY_TYPE, int)
