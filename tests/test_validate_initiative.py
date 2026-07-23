import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "validate_initiative.py"
if SCRIPT.exists():
    SPEC = importlib.util.spec_from_file_location("validate_initiative", SCRIPT)
    MODULE = importlib.util.module_from_spec(SPEC)
    sys.modules[SPEC.name] = MODULE
    SPEC.loader.exec_module(MODULE)
else:
    MODULE = None


class ValidateInitiativeTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(MODULE, "initiative validator is not implemented")
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.initiative = Path(self.temp_dir.name) / "2026-07-23-auth-refresh"
        self.initiative.mkdir()

    def write(self, name, content):
        (self.initiative / name).write_text(content, encoding="utf-8")

    def write_valid_documents(self):
        self.write(
            "spec.md",
            """---
jsip_version: 1
initiative: 2026-07-23-auth-refresh
artifact: spec
status: approved
revision: 2
created: 2026-07-23
approved_at: 2026-07-24
---
# Auth Refresh Specification

## Intent
Keep authenticated sessions current without interrupting users.

## Goals
- Refresh expiring sessions.

## Non-Goals
- Replacing the identity provider.

## Constraints
- Preserve the existing token format.

## Design
Refresh through the existing session boundary.

## Acceptance Criteria
- AC-1: Refresh a session before expiry.
- AC-2: Preserve the current session when refresh fails transiently.

## Intent and Drift Guardrails
Implementation must preserve the existing identity provider and token format.
""",
        )
        self.write(
            "plan.md",
            """---
jsip_version: 1
initiative: 2026-07-23-auth-refresh
artifact: plan
status: approved
revision: 3
spec_revision: 2
created: 2026-07-24
approved_at: 2026-07-24
---
# Auth Refresh Implementation Plan

## Goal
Implement the approved refresh design.

## Spec Traceability
- AC-1: Task 1
- AC-2: Task 2

## Tasks
### Task 1: Refresh before expiry
Write a failing test, verify RED, implement minimally, verify GREEN.

### Task 2: Preserve transient failures (AC-2)
Write a failing test, verify RED, implement minimally, verify GREEN.

## Verification
Run the focused tests and full project suite.
""",
        )
        self.write(
            "state.md",
            """---
jsip_version: 1
initiative: 2026-07-23-auth-refresh
artifact: state
phase: implement
status: active
spec_revision: 2
plan_revision: 3
updated: 2026-07-24
---
# Auth Refresh State

## Current Position
Ready for Task 1.

## Approved Inputs
- spec.md revision 2
- plan.md revision 3

## Decision and Deviation Log
- 2026-07-24: Plan approved without deviations.

## Verification Evidence
No implementation evidence yet.

## Blockers
None.

## Next Action
Execute Task 1 test-first.
""",
        )

    def test_accepts_consistent_approved_documents(self):
        self.write_valid_documents()

        self.assertEqual(MODULE.validate_initiative(self.initiative), [])

    def test_rejects_spec_without_drift_guardrails(self):
        self.write_valid_documents()
        spec = (self.initiative / "spec.md").read_text(encoding="utf-8")
        spec = spec.replace("## Intent and Drift Guardrails", "## Notes")
        self.write("spec.md", spec)

        errors = MODULE.validate_initiative(self.initiative)

        self.assertIn("spec.md is missing heading `Intent and Drift Guardrails`", errors)

    def test_rejects_implementation_with_unapproved_spec(self):
        self.write_valid_documents()
        spec = (self.initiative / "spec.md").read_text(encoding="utf-8")
        self.write("spec.md", spec.replace("status: approved", "status: draft", 1))

        errors = MODULE.validate_initiative(self.initiative)

        self.assertIn("implement phase requires an approved spec", errors)

    def test_rejects_revision_drift(self):
        self.write_valid_documents()
        state = (self.initiative / "state.md").read_text(encoding="utf-8")
        self.write("state.md", state.replace("spec_revision: 2", "spec_revision: 1"))

        errors = MODULE.validate_initiative(self.initiative)

        self.assertIn("state.md pins spec revision 1 but spec.md is revision 2", errors)

    def test_rejects_state_without_plan_revision_pin(self):
        self.write_valid_documents()
        state = (self.initiative / "state.md").read_text(encoding="utf-8")
        self.write("state.md", state.replace("plan_revision: 3\n", ""))

        errors = MODULE.validate_initiative(self.initiative)

        self.assertIn("state.md is missing frontmatter field `plan_revision`", errors)

    def test_rejects_unplanned_acceptance_criterion(self):
        self.write_valid_documents()
        plan = (self.initiative / "plan.md").read_text(encoding="utf-8")
        self.write("plan.md", plan.replace("- AC-2: Task 2\n", ""))

        errors = MODULE.validate_initiative(self.initiative)

        self.assertIn("plan.md does not trace acceptance criterion AC-2", errors)

    def test_allows_brainstorm_phase_without_plan(self):
        self.write_valid_documents()
        (self.initiative / "plan.md").unlink()
        state = (self.initiative / "state.md").read_text(encoding="utf-8")
        state = state.replace("phase: implement", "phase: brainstorm")
        state = state.replace("plan_revision: 3\n", "")
        self.write("state.md", state)

        self.assertEqual(MODULE.validate_initiative(self.initiative), [])


if __name__ == "__main__":
    unittest.main()
