import pytest

from cvpysdk.policies.schedule_options import (
    AuxCopyOptions,
    BackupOptions,
    ScheduleOptions,
)


@pytest.mark.unit
class TestScheduleOptions:
    """Tests for the ScheduleOptions factory class."""

    def test_new_creates_backup_options(self):
        result = ScheduleOptions("backupOpts")
        assert isinstance(result, BackupOptions)

    def test_new_creates_auxcopy_options(self):
        result = ScheduleOptions("auxcopyJobOption")
        assert isinstance(result, AuxCopyOptions)

    def test_policy_to_options_map(self):
        assert "Data Protection" in ScheduleOptions.policy_to_options_map
        assert "Auxiliary Copy" in ScheduleOptions.policy_to_options_map
        assert ScheduleOptions.policy_to_options_map["Data Protection"] == "backupOpts"
        assert ScheduleOptions.policy_to_options_map["Auxiliary Copy"] == "auxcopyJobOption"


@pytest.mark.unit
class TestBackupOptions:
    """Tests for the BackupOptions class."""

    def test_options_json_defaults(self):
        bo = BackupOptions("backupOpts")
        result = bo.options_json()
        assert "backupOpts" in result
        assert result["backupOpts"]["backupLevel"] == "Incremental"
        assert result["backupOpts"]["incLevel"] == 1

    def test_options_json_with_new_options(self):
        bo = BackupOptions("backupOpts")
        result = bo.options_json({"backupLevel": "Full"})
        assert result["backupOpts"]["backupLevel"] == "Full"

    def test_options_json_with_current_options(self):
        bo = BackupOptions("backupOpts", current_options={"backupLevel": "Full"})
        result = bo.options_json({"incLevel": 2})
        assert result["backupOpts"]["backupLevel"] == "Full"
        assert result["backupOpts"]["incLevel"] == 2

    def test_options_json_merges_current_and_new(self):
        bo = BackupOptions(
            "backupOpts",
            current_options={"backupLevel": "Incremental", "incLevel": 1},
        )
        result = bo.options_json({"backupLevel": "Differential"})
        assert result["backupOpts"]["backupLevel"] == "Differential"
        assert result["backupOpts"]["incLevel"] == 1

    def test_options_json_no_options_no_current(self):
        bo = BackupOptions("backupOpts")
        result = bo.options_json()
        assert result["backupOpts"]["runIncrementalBackup"] is False


@pytest.mark.unit
class TestAuxCopyOptions:
    """Tests for the AuxCopyOptions class."""

    def test_options_json_defaults(self):
        aco = AuxCopyOptions("auxcopyJobOption")
        result = aco.options_json()
        assert "backupOpts" in result
        assert "mediaOpt" in result["backupOpts"]
        auxcopy = result["backupOpts"]["mediaOpt"]["auxcopyJobOption"]
        assert auxcopy["maxNumberOfStreams"] == 0
        assert auxcopy["useMaximumStreams"] is True
        assert auxcopy["allCopies"] is True
        assert auxcopy["totalJobsToProcess"] == 1000

    def test_options_json_with_new_options(self):
        aco = AuxCopyOptions("auxcopyJobOption")
        result = aco.options_json({"maxNumberOfStreams": 5})
        auxcopy = result["backupOpts"]["mediaOpt"]["auxcopyJobOption"]
        assert auxcopy["maxNumberOfStreams"] == 5

    def test_options_json_with_current_options(self):
        aco = AuxCopyOptions(
            "auxcopyJobOption",
            current_options={"maxNumberOfStreams": 3, "allCopies": False},
        )
        result = aco.options_json({"allCopies": True})
        auxcopy = result["backupOpts"]["mediaOpt"]["auxcopyJobOption"]
        assert auxcopy["maxNumberOfStreams"] == 3
        assert auxcopy["allCopies"] is True

    def test_options_json_empty_new_uses_defaults(self):
        aco = AuxCopyOptions("auxcopyJobOption")
        result = aco.options_json({})
        auxcopy = result["backupOpts"]["mediaOpt"]["auxcopyJobOption"]
        assert auxcopy["useScallableResourceManagement"] is True
