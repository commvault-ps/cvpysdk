"""Unit tests for cvpysdk.datacube.sedstype module."""

import pytest

from cvpysdk.datacube.sedstype import SEDS_TYPE_DICT


@pytest.mark.unit
class TestSedsTypeDict:
    """Tests for SEDS_TYPE_DICT."""

    def test_dict_is_not_empty(self):
        assert len(SEDS_TYPE_DICT) > 0

    def test_known_entries(self):
        assert SEDS_TYPE_DICT[0] == "NONE"
        assert SEDS_TYPE_DICT[1] == "jdbc"
        assert SEDS_TYPE_DICT[5] == "file"
        assert SEDS_TYPE_DICT[8] == "salesforce"
        assert SEDS_TYPE_DICT[21] == "fsindex"
        assert SEDS_TYPE_DICT[43] == "asset"

    def test_all_values_are_strings(self):
        for key, value in SEDS_TYPE_DICT.items():
            assert isinstance(value, str), f"Key {key} has non-string value: {value}"

    def test_all_keys_are_ints(self):
        for key in SEDS_TYPE_DICT:
            assert isinstance(key, int), f"Key {key} is not int"

    def test_contiguous_keys_from_zero(self):
        """Keys should go from 0 to max without gaps."""
        max_key = max(SEDS_TYPE_DICT.keys())
        assert max_key == 43
        for i in range(max_key + 1):
            assert i in SEDS_TYPE_DICT, f"Key {i} is missing from SEDS_TYPE_DICT"
