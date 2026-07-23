---
name: implement
description: Use ONLY when the user explicitly invokes jsip:implement for an initiative with approved, revision-matched spec.md and plan.md and wants test-first execution with persisted evidence and strict drift controls.
---

# JSIP Implement

Execute the approved plan task by task while continually checking the code against pinned intent. Treat repository documents as the source of truth and chat history as supplemental context only.

## Non-Negotiable Boundaries

- Do not begin without approved, revision-matched `spec.md`, `plan.md`, and `state.md`.
- Do not revise approved intent, acceptance criteria, or plan scope from this skill.
- Stop before deviating from the approved spec or plan, even when the alternative seems minor or better.
- Never create a git commit unless the user separately and explicitly requests one.
- Do not mark work complete without fresh verification evidence.

## Load and Validate

1. Locate the requested `docs/jsip/initiatives/YYYY-MM-DD-<slug>/` directory. Ask if the initiative is ambiguous.
2. Read `state.md` first to recover the current position and next action.
3. Read the complete pinned `spec.md`, especially acceptance criteria and `Intent and Drift Guardrails`.
4. Read the complete pinned `plan.md` and identify the first incomplete task.
5. Resolve the installed JSIP plugin root from this `SKILL.md` location by moving two directories up from its containing `skills/implement/` directory. Read `<jsip-plugin-root>/references/artifact-protocol.md`. Never resolve bundled paths from the current working directory, repository root, or initiative directory.
6. From that same `<jsip-plugin-root>`, run:

   ```bash
   python3 "<jsip-plugin-root>/scripts/validate_initiative.py" "docs/jsip/initiatives/<initiative>"
   ```

7. Stop on any validation error. Do not infer which revision the user intended.
8. Set `state.md` phase to `implement`, status to `active`, and `Next Action` to the first incomplete task. Create a todo for each remaining plan task.

## Execute Each Task

For every task, maintain the plan order unless the plan explicitly permits parallel work:

1. Re-read the task's linked acceptance criteria and applicable drift guardrails.
2. Mark the task in progress in the working todo and `state.md`.
3. **RED:** Write one focused behavioral test before production code. Run the exact focused command and confirm it fails for the expected missing behavior.
4. If RED passes unexpectedly or fails for setup, syntax, or an unrelated reason, correct the test/setup or stop. Do not proceed to production code without the expected RED evidence.
5. **GREEN:** Make the smallest production change that satisfies the failing test.
6. Run the focused test and confirm GREEN.
7. **REFACTOR:** Improve structure only while behavior remains green and only where the plan or changed code justifies it.
8. Run the task's broader verification commands and inspect output for unexpected errors or warnings.
9. Check off the task only after all verification passes.
10. Append concise, dated commands and outcomes under `Verification Evidence`; update `Current Position` and `Next Action` immediately.
11. Re-run `validate_initiative.py` after every state or plan update.

## Drift and Blockers

Stop before deviating when any of these occur:

- Required behavior conflicts with an acceptance criterion or drift guardrail.
- A planned interface, file, dependency, or test strategy is infeasible.
- New scope, architecture, compatibility behavior, or user-visible behavior is needed.
- Verification repeatedly fails for reasons outside the current task.

When blocked, make no speculative fallback. Set `state.md` status to `blocked`, append a dated entry under `Decision and Deviation Log` containing the trigger, affected criteria, proposed change, and evidence, then ask for direction.

Do not revise approved intent from this skill. Direct specification changes back to explicit `jsip:brainstorm`; direct plan-only changes back to explicit `jsip:plan`. Resume implementation only after documents are approved and revision pins validate again.

## Complete the Initiative

After every task is checked:

1. Run all plan-level verification plus the repository's relevant full tests, linters, formatters, and build.
2. Confirm each acceptance criterion has current verification evidence.
3. Confirm the final diff contains no unplanned behavior or unrelated changes.
4. Set `plan.md` to `status: completed` and `state.md` to phase `complete`, status `completed`.
5. Record final commands, outcomes, and the absence of approved deviations under `Verification Evidence`.
6. Run `validate_initiative.py` one final time and report the result without committing.
