import pytest

from cvpysdk.activateapps.constants import (
    ActivateEntityConstants,
    ClassifierConstants,
    ComplianceConstants,
    EdiscoveryConstants,
    InventoryConstants,
    PlanConstants,
    RequestConstants,
    TagConstants,
    TargetApps,
    TrainingStatus,
)


@pytest.mark.unit
class TestTargetApps:
    """Tests for the TargetApps enum."""

    def test_sdg_value(self):
        assert TargetApps.SDG.value == 2

    def test_fso_value(self):
        assert TargetApps.FSO.value == 1

    def test_case_mgr_value(self):
        assert TargetApps.CASE_MGR.value == 4

    def test_fs_value(self):
        assert TargetApps.FS.value == 8

    def test_ra_value(self):
        assert TargetApps.RA.value == 128


@pytest.mark.unit
class TestTrainingStatus:
    """Tests for the TrainingStatus enum."""

    def test_not_applicable(self):
        assert TrainingStatus.NOT_APPLICABLE.value == 0

    def test_completed(self):
        assert TrainingStatus.COMPLETED.value == 4

    def test_failed(self):
        assert TrainingStatus.FAILED.value == 3

    def test_not_usable(self):
        assert TrainingStatus.NOT_USABLE.value == 6


@pytest.mark.unit
class TestRequestConstants:
    """Tests for the RequestConstants class."""

    def test_request_status_enum(self):
        assert RequestConstants.RequestStatus.TaskCreated.value == 1
        assert RequestConstants.RequestStatus.ReviewCompleted.value == 4
        assert RequestConstants.RequestStatus.Failed.value == 12

    def test_request_type_enum(self):
        assert RequestConstants.RequestType.EXPORT.value == "EXPORT"
        assert RequestConstants.RequestType.DELETE.value == "DELETE"

    def test_field_constants(self):
        assert RequestConstants.FIELD_DOC_COUNT == "TotalDocuments"
        assert RequestConstants.FIELD_REVIEWED == "ReviewedDocuments"

    def test_search_query_selection_set_is_set(self):
        assert isinstance(RequestConstants.SEARCH_QUERY_SELECTION_SET, set)
        assert "contentid" in RequestConstants.SEARCH_QUERY_SELECTION_SET


@pytest.mark.unit
class TestEdiscoveryConstants:
    """Tests for the EdiscoveryConstants class."""

    def test_crawl_type_enum(self):
        assert EdiscoveryConstants.CrawlType.LIVE.value == 1
        assert EdiscoveryConstants.CrawlType.BACKUP.value == 2

    def test_source_type_enum(self):
        assert EdiscoveryConstants.SourceType.SOURCE.value == 1
        assert EdiscoveryConstants.SourceType.BACKUP.value == 2

    def test_review_actions_enum(self):
        assert EdiscoveryConstants.ReviewActions.DELETE.value == 1
        assert EdiscoveryConstants.ReviewActions.MOVE.value == 4
        assert EdiscoveryConstants.ReviewActions.TAG.value == 98

    def test_client_type_enum(self):
        assert EdiscoveryConstants.ClientType.FILE_SYSTEM.value == 5
        assert EdiscoveryConstants.ClientType.EXCHANGE.value == 17

    def test_data_source_types(self):
        assert EdiscoveryConstants.DATA_SOURCE_TYPES[5] == "file"
        assert EdiscoveryConstants.DATA_SOURCE_TYPES[17] == "exchange"

    def test_review_action_fso_supported(self):
        assert 1 in EdiscoveryConstants.REVIEW_ACTION_FSO_SUPPORTED
        assert 4 in EdiscoveryConstants.REVIEW_ACTION_FSO_SUPPORTED

    def test_exchange_constants(self):
        assert EdiscoveryConstants.EXCHANGE_AGENT == "exchange mailbox"
        assert EdiscoveryConstants.EXCHANGE_BACKUPSET == "user mailbox"


@pytest.mark.unit
class TestInventoryConstants:
    """Tests for the InventoryConstants class."""

    def test_crawl_job_states(self):
        assert InventoryConstants.CRAWL_JOB_COMPLETE_STATE == 4
        assert InventoryConstants.CRAWL_JOB_COMPLETE_ERROR_STATE == 13
        assert isinstance(InventoryConstants.CRAWL_JOB_FAILED_STATE, list)

    def test_asset_type_enum(self):
        assert InventoryConstants.AssetType.IDENTITY_SERVER.value == 61
        assert InventoryConstants.AssetType.FILE_SERVER.value == 132

    def test_field_property_constants(self):
        assert InventoryConstants.FIELD_PROPERTY_NAME == "name"
        assert InventoryConstants.FIELD_PROPERTY_DNSHOST == "hostName"
        assert InventoryConstants.FIELD_PROPERTY_IP == "ipAddress"


@pytest.mark.unit
class TestPlanConstants:
    """Tests for the PlanConstants class."""

    def test_indexing_constants(self):
        assert PlanConstants.INDEXING_ONLY_METADATA == 1
        assert PlanConstants.INDEXING_METADATA_AND_CONTENT == 2

    def test_default_doc_sizes(self):
        assert PlanConstants.DEFAULT_MIN_DOC_SIZE == 0
        assert PlanConstants.DEFAULT_MAX_DOC_SIZE == 50

    def test_search_type_enum(self):
        assert PlanConstants.RAPlanSearchType.SEARCH_TYPE_ONLY_METADATA.value == "METADATA"

    def test_plan_app_type_enum(self):
        assert PlanConstants.RAPlanAppType.CLASSIFIED.value == 2
        assert PlanConstants.RAPlanAppType.UNIFIED.value == 6


@pytest.mark.unit
class TestClassifierConstants:
    """Tests for the ClassifierConstants class."""

    def test_create_request_json_structure(self):
        req = ClassifierConstants.CREATE_REQUEST_JSON
        assert "entityName" in req
        assert "entityType" in req
        assert req["entityType"] == 4
        assert "classifierDetails" in req["entityXML"]


@pytest.mark.unit
class TestActivateEntityConstants:
    """Tests for the ActivateEntityConstants class."""

    def test_request_json_structure(self):
        req = ActivateEntityConstants.REQUEST_JSON
        assert "regularExpression" in req
        assert "entityName" in req
        assert "entityXML" in req
        assert req["entityXML"]["isSystemDefinedEntity"] is False


@pytest.mark.unit
class TestTagConstants:
    """Tests for the TagConstants class."""

    def test_tag_set_add_request_json(self):
        req = TagConstants.TAG_SET_ADD_REQUEST_JSON
        assert req["entityType"] == 9504
        assert req["operationType"] == 1

    def test_tag_set_modify_request_json(self):
        req = TagConstants.TAG_SET_MODIFY_REQUEST_JSON
        assert req["operationType"] == 3

    def test_tag_set_delete_request_json(self):
        req = TagConstants.TAG_SET_DELETE_REQUEST_JSON
        assert req["entityType"] == 9504


@pytest.mark.unit
class TestComplianceConstants:
    """Tests for the ComplianceConstants class."""

    def test_app_types_enum(self):
        assert ComplianceConstants.AppTypes.EXCHANGE.value == "EXCHANGE"
        assert ComplianceConstants.AppTypes.FILE_SYSTEM.value == "FILE_SYSTEM"
        assert ComplianceConstants.AppTypes.TEAMS.value == "TEAMS"

    def test_export_types_enum(self):
        assert ComplianceConstants.ExportTypes.CAB.value == "CAB"
        assert ComplianceConstants.ExportTypes.PST.value == "PST"

    def test_permissions(self):
        assert "View" in ComplianceConstants.PERMISSIONS
        assert "Delete" in ComplianceConstants.PERMISSIONS
        assert "Add" in ComplianceConstants.PERMISSIONS
        assert "Download" in ComplianceConstants.PERMISSIONS

    def test_compliance_search_json_structure(self):
        req = ComplianceConstants.COMPLIANCE_SEARCH_JSON
        assert "mode" in req
        assert "advSearchGrp" in req
        assert req["mode"] == 2
