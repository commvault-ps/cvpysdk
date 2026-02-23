"""Unit tests for cvpysdk.tags module."""

import pytest

from cvpysdk.exception import SDKException
from cvpysdk.tags import Tag, Tags


@pytest.mark.unit
class TestTags:
    """Tests for the Tags collection class."""

    def _make_tags(self, mock_commcell, mock_response):
        resp = mock_response(
            json_data={
                "tagSetInfo": {"id": 100},
                "tags": [
                    {"name": "TestTag", "id": 1},
                    {"name": "OtherTag", "id": 2},
                ],
            }
        )
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        return Tags(mock_commcell)

    def test_init_populates_tags(self, mock_commcell, mock_response):
        tags = self._make_tags(mock_commcell, mock_response)
        assert "testtag" in tags.all_tags
        assert "othertag" in tags.all_tags

    def test_has_tag_true(self, mock_commcell, mock_response):
        tags = self._make_tags(mock_commcell, mock_response)
        assert tags.has_tag("TestTag") is True

    def test_has_tag_false(self, mock_commcell, mock_response):
        tags = self._make_tags(mock_commcell, mock_response)
        assert tags.has_tag("missing") is False

    def test_has_tag_raises_on_non_string(self, mock_commcell, mock_response):
        tags = self._make_tags(mock_commcell, mock_response)
        with pytest.raises(SDKException):
            tags.has_tag(123)

    def test_get_returns_tag_object(self, mock_commcell, mock_response):
        tags = self._make_tags(mock_commcell, mock_response)
        result = tags.get("TestTag")
        assert isinstance(result, Tag)
        assert result.tag_name == "testtag"
        assert result.tag_id == "1"

    def test_get_raises_on_missing(self, mock_commcell, mock_response):
        tags = self._make_tags(mock_commcell, mock_response)
        with pytest.raises(SDKException):
            tags.get("nonexistent")

    def test_refresh(self, mock_commcell, mock_response):
        tags = self._make_tags(mock_commcell, mock_response)
        resp2 = mock_response(
            json_data={
                "tagSetInfo": {"id": 100},
                "tags": [
                    {"name": "NewTag", "id": 3},
                ],
            }
        )
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp2)
        tags.refresh()
        assert "newtag" in tags.all_tags
        assert "testtag" not in tags.all_tags

    def test_default_tagset_id_set(self, mock_commcell, mock_response):
        tags = self._make_tags(mock_commcell, mock_response)
        assert tags.DEFAULT_TAGSET_ID == 100


@pytest.mark.unit
class TestTag:
    """Tests for the Tag entity class."""

    def test_init_with_id(self, mock_commcell):
        tag = Tag(mock_commcell, "mytag", tag_id=42)
        assert tag.tag_name == "mytag"
        assert tag.tag_id == "42"

    def test_tag_name_property(self, mock_commcell):
        tag = Tag(mock_commcell, "anothertag", tag_id=5)
        assert tag.tag_name == "anothertag"

    def test_tag_id_property(self, mock_commcell):
        tag = Tag(mock_commcell, "testtag", tag_id=99)
        assert tag.tag_id == "99"
