"""Unit tests for cvpysdk/subclients/adsubclient.py"""

import pytest

from cvpysdk.subclient import Subclient
from cvpysdk.subclients.adsubclient import ADSubclient


@pytest.mark.unit
class TestADSubclient:
    """Tests for the ADSubclient class."""

    def test_inherits_subclient(self):
        """ADSubclient should inherit from Subclient."""
        assert issubclass(ADSubclient, Subclient)

    def test_has_key_methods(self):
        """ADSubclient should have expected methods."""
        assert hasattr(ADSubclient, "content")
        assert hasattr(ADSubclient, "cv_contents")
        assert hasattr(ADSubclient, "compare_id")
        assert hasattr(ADSubclient, "trigger_compare_job")
        assert hasattr(ADSubclient, "checkcompare_result_generated")
        assert hasattr(ADSubclient, "generate_compare_report")
        assert hasattr(ADSubclient, "restore_job")

    def test_cv_contents_without_entrypoint(self):
        """cv_contents should convert content to AD format without entrypoint."""
        subclient = object.__new__(ADSubclient)
        contents = ["CN=user1,OU=Users,DC=example,DC=com"]
        result = subclient.cv_contents(contents)
        assert len(result) == 1
        content_entry, short_dn = result[0]
        assert content_entry == "DC=com,DC=example,OU=Users,CN=user1"
        assert short_dn is None

    def test_cv_contents_with_entrypoint(self):
        """cv_contents should convert content with entrypoint stripping."""
        subclient = object.__new__(ADSubclient)
        contents = ["CN=user1,OU=Users,DC=example,DC=com"]
        result = subclient.cv_contents(contents, entrypoint="DC=example,DC=com")
        assert len(result) == 1
        content_entry, short_dn = result[0]
        assert content_entry == "DC=com,DC=example,OU=Users,CN=user1"
        assert short_dn == "DC=com,DC=example,OU=Users,CN=user1".split(",DC=example,DC=com")[0]

    def test_content_property_valid(self):
        """content property should return parsed AD content."""
        subclient = object.__new__(ADSubclient)
        subclient._subclient_properties = {
            "content": [
                {"path": "CN=user1,OU=Users,DC=example"},
            ]
        }
        result = subclient.content
        assert result == ["OU=Users,DC=example"]

    def test_content_property_empty_raises(self):
        """content property should raise SDKException when content is empty."""
        from cvpysdk.exception import SDKException

        subclient = object.__new__(ADSubclient)
        subclient._subclient_properties = {"content": []}
        with pytest.raises(SDKException):
            _ = subclient.content

    def test_content_property_missing_raises(self):
        """content property should raise SDKException when content key is missing."""
        from cvpysdk.exception import SDKException

        subclient = object.__new__(ADSubclient)
        subclient._subclient_properties = {}
        with pytest.raises(SDKException):
            _ = subclient.content
