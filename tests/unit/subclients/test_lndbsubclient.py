"""Unit tests for cvpysdk/subclients/lndbsubclient.py"""

import pytest

from cvpysdk.subclient import Subclient
from cvpysdk.subclients.lndbsubclient import LNDbSubclient


@pytest.mark.unit
class TestLNDbSubclient:
    """Tests for the LNDbSubclient class."""

    def test_inherits_subclient(self):
        """LNDbSubclient should inherit from Subclient."""
        assert issubclass(LNDbSubclient, Subclient)

    def test_has_key_methods(self):
        """LNDbSubclient should have expected methods."""
        assert hasattr(LNDbSubclient, "restore_in_place")
        assert hasattr(LNDbSubclient, "restore_out_of_place")
        assert hasattr(LNDbSubclient, "backup")
        assert hasattr(LNDbSubclient, "content")

    def test_content_property(self):
        """content property should return stored content."""
        subclient = object.__new__(LNDbSubclient)
        subclient._content = [{"lotusNotesDBContent": {"relativePath": "test.nsf"}}]
        assert subclient.content == [{"lotusNotesDBContent": {"relativePath": "test.nsf"}}]

    def test_get_subclient_properties_json_structure(self):
        """_get_subclient_properties_json should return proper structure."""
        subclient = object.__new__(LNDbSubclient)
        subclient._proxyClient = {"clientName": "proxy"}
        subclient._subClientEntity = {"subclientId": 1}
        subclient._content = []
        subclient._commonProperties = {}

        result = subclient._get_subclient_properties_json()
        assert "subClientProperties" in result
        props = result["subClientProperties"]
        assert "proxyClient" in props
        assert "content" in props
        assert "contentOperationType" in props
        assert props["contentOperationType"] == 1

    def test_restore_in_place_raises_for_invalid_types(self):
        """restore_in_place should raise SDKException for invalid input types."""
        from cvpysdk.exception import SDKException

        subclient = object.__new__(LNDbSubclient)
        with pytest.raises(SDKException):
            subclient.restore_in_place(paths="not_a_list")

    def test_restore_out_of_place_raises_for_invalid_types(self):
        """restore_out_of_place should raise SDKException for invalid types."""
        from cvpysdk.exception import SDKException

        subclient = object.__new__(LNDbSubclient)
        with pytest.raises(SDKException):
            subclient.restore_out_of_place(
                client="client",
                destination_path="/dest",
                paths="not_a_list",
            )
