"""Unit tests for cvpysdk.drorchestration.dr_orchestration_job_phase module."""

import pytest

from cvpysdk.drorchestration.dr_orchestration_job_phase import DRJobPhases, DRJobPhaseToText


@pytest.mark.unit
class TestDRJobPhases:
    """Tests for DRJobPhases enum."""

    def test_script_execution(self):
        assert DRJobPhases.SCRIPT_EXECUTION.value == 0

    def test_power_on(self):
        assert DRJobPhases.POWER_ON.value == 1

    def test_replication(self):
        assert DRJobPhases.REPLICATION.value == 7

    def test_finalize(self):
        assert DRJobPhases.FINALIZE.value == 26

    def test_restore_vm(self):
        assert DRJobPhases.RESTORE_VM.value == 51

    def test_vm_level(self):
        assert DRJobPhases.VM_LEVEL.value == 54

    def test_enum_is_unique(self):
        """All values should be unique."""
        values = [member.value for member in DRJobPhases]
        assert len(values) == len(set(values))

    def test_lookup_by_value(self):
        assert DRJobPhases(0) == DRJobPhases.SCRIPT_EXECUTION
        assert DRJobPhases(1) == DRJobPhases.POWER_ON


@pytest.mark.unit
class TestDRJobPhaseToText:
    """Tests for DRJobPhaseToText enum."""

    def test_script_execution_text(self):
        assert DRJobPhaseToText.SCRIPT_EXECUTION.value == "Script Execution"

    def test_power_on_text(self):
        assert DRJobPhaseToText.POWER_ON.value == "Power On"

    def test_replication_text(self):
        assert DRJobPhaseToText.REPLICATION.value == "Replication"

    def test_restore_vm_text(self):
        assert DRJobPhaseToText.RESTORE_VM.value == "Restore VM"

    def test_all_phases_have_text(self):
        """Every phase in DRJobPhases should have a matching DRJobPhaseToText entry."""
        for phase in DRJobPhases:
            assert hasattr(DRJobPhaseToText, phase.name), (
                f"DRJobPhaseToText missing entry for {phase.name}"
            )

    def test_all_text_values_are_strings(self):
        for member in DRJobPhaseToText:
            assert isinstance(member.value, str)
