"""Unit tests for cvpysdk/subclients/exchange/constants.py module."""

import pytest

from cvpysdk.subclients.exchange.constants import (
    ExchangeConstants,
    JobOptionIntegers,
    JobOptionKeys,
    JobOptionValues,
)


@pytest.mark.unit
class TestExchangeConstants:
    """Tests for the ExchangeConstants class."""

    def test_search_processing_info_has_required_keys(self):
        info = ExchangeConstants.SEAARCH_PROCESSING_INFO
        assert "resultOffset" in info
        assert "pageSize" in info
        assert "sortParams" in info

    def test_search_processing_info_default_page_size(self):
        assert ExchangeConstants.SEAARCH_PROCESSING_INFO["pageSize"] == 100

    def test_advanced_search_group_has_email_filter(self):
        group = ExchangeConstants.ADVANCED_SEARCH_GROUP
        assert "emailFilter" in group
        assert "commonFilter" in group
        assert "galaxyFilter" in group

    def test_find_mailbox_request_data_structure(self):
        data = ExchangeConstants.FIND_MAILBOX_REQUEST_DATA
        assert data["mode"] == 4
        assert "advSearchGrp" in data
        assert "searchProcessingInfo" in data
        assert "facetRequests" in data

    def test_find_mbx_query_default_params_keys(self):
        params = ExchangeConstants.FIND_MBX_QUERY_DEFAULT_PARAMS
        assert "RESPONSE_FIELD_LIST" in params
        assert "SHOW_EMAILS_ONLY" in params
        assert "SUPPORT_SOLR_ONLY" in params
        assert params["SHOW_EMAILS_ONLY"] == "true"

    def test_find_mbx_default_facet_is_set(self):
        facet = ExchangeConstants.FIND_MBX_DEFAULT_FACET
        assert isinstance(facet, set)
        assert "MODIFIEDTIME" in facet
        assert "SIZEINKB" in facet
        assert "FOLDER_PATH" in facet

    def test_search_in_restore_payload_structure(self):
        payload = ExchangeConstants.SEARCH_IN_RESTORE_PAYLOAD
        assert payload["mode"] == 4
        assert "advSearchGrp" in payload
        assert "searchProcessingInfo" in payload
        proc = payload["searchProcessingInfo"]
        assert proc["pageSize"] == 15


@pytest.mark.unit
class TestJobOptionKeys:
    """Tests for the JobOptionKeys enum."""

    def test_enum_members_exist(self):
        assert JobOptionKeys.RESTORE_DESTINATION.value == "Restore destination"
        assert JobOptionKeys.DESTINATION.value == "Destination"
        assert JobOptionKeys.IF_MESSAGE_EXISTS.value == "If the message exists"

    def test_exchange_restore_choice(self):
        assert JobOptionKeys.EXCHANGE_RESTORE_CHOICE.value == "exchangeRestoreChoice"


@pytest.mark.unit
class TestJobOptionValues:
    """Tests for the JobOptionValues enum."""

    def test_enum_members_exist(self):
        assert JobOptionValues.SKIP.value == "Skip"
        assert JobOptionValues.DISABLED.value == "Disabled"
        assert JobOptionValues.ENABLED.value == "Enabled"
        assert JobOptionValues.EXCHANGE.value == "Exchange"

    def test_original_location_value(self):
        assert JobOptionValues.ORIGINAL_LOCATION.value == "Original Location"


@pytest.mark.unit
class TestJobOptionIntegers:
    """Tests for the JobOptionIntegers enum."""

    def test_enum_members_exist(self):
        assert JobOptionIntegers.EXCHANGE_RESTORE_CHOICE.value == 1
        assert JobOptionIntegers.EXCHANGE_RESTORE_DRIVE.value == 1
        assert JobOptionIntegers.RECOVER_STUBS.value == 0
        assert JobOptionIntegers.STUB_REPORTING.value == 1
        assert JobOptionIntegers.UPDATE_RECALL_LINK.value == 2
