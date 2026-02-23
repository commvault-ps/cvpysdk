from unittest.mock import patch

import pytest

from cvpysdk.activateapps.entity_manager import (
    ActivateEntities,
    Tags,
)
from cvpysdk.exception import SDKException


@pytest.mark.unit
class TestActivateEntities:
    """Tests for the ActivateEntities class."""

    def _make_entities(self, mock_commcell, entities=None):
        with patch.object(
            ActivateEntities,
            "_get_all_activate_entities",
            return_value=entities or {},
        ):
            return ActivateEntities(mock_commcell)

    def test_has_entity_true(self, mock_commcell):
        entities = {
            "test_entity": {
                "entity_id": 1,
                "entity_key": "key1",
            }
        }
        ae = self._make_entities(mock_commcell, entities=entities)
        assert ae.has_entity("test_entity") is True

    def test_has_entity_non_string_raises(self, mock_commcell):
        ae = self._make_entities(mock_commcell)
        with pytest.raises(SDKException):
            ae.has_entity(123)

    def test_get_nonexistent_raises(self, mock_commcell):
        ae = self._make_entities(mock_commcell)
        with pytest.raises(SDKException):
            ae.get("nonexistent")

    def test_refresh_calls_get(self, mock_commcell):
        with patch.object(
            ActivateEntities,
            "_get_all_activate_entities",
            return_value={},
        ) as mock_get:
            ae = ActivateEntities(mock_commcell)
            ae.refresh()
        assert mock_get.call_count == 2


@pytest.mark.unit
class TestTags:
    """Tests for the Tags class."""

    def _make_tags(self, mock_commcell, tag_sets=None):
        with patch.object(Tags, "_get_all_tag_sets", return_value=tag_sets or {}):
            return Tags(mock_commcell)

    def test_has_tag_set_true(self, mock_commcell):
        tag_sets = {"testset": {"container_id": 1}}
        t = self._make_tags(mock_commcell, tag_sets=tag_sets)
        assert t.has_tag_set("testset") is True

    def test_has_tag_set_non_string_raises(self, mock_commcell):
        t = self._make_tags(mock_commcell)
        with pytest.raises(SDKException):
            t.has_tag_set(123)

    def test_get_nonexistent_raises(self, mock_commcell):
        t = self._make_tags(mock_commcell)
        with pytest.raises(SDKException):
            t.get("nonexistent")

    def test_refresh_calls_get(self, mock_commcell):
        with patch.object(Tags, "_get_all_tag_sets", return_value={}) as mock_get:
            t = Tags(mock_commcell)
            t.refresh()
        assert mock_get.call_count == 2
