---
name: plan
description: Use ONLY when the user explicitly invokes jsip:plan for an initiative with an approved spec.md and wants a concrete, test-first implementation plan linked to that exact specification revision.
---

# JSIP Plan

Derive an executable plan from approved intent. Every task must be traceable to the pinned spec so implementation cannot gradually substitute a different goal.

## Non-Negotiable Boundaries

- Require an approved `spec.md`; do not plan from conversation memory alone.
- Do not modify production code or implement any plan task.
- Do not revise approved specification intent or acceptance criteria.
- Never create a git commit unless the user separately and explicitly requests one.
- Stop after approval. Do not automatically invoke or perform implementation.
- Resolve bundled paths from this skill's base directory supplied by the harness, never from the target repository.

## Workflow

1. Locate the requested initiative under `docs/jsip/initiatives/YYYY-MM-DD-<slug>/`. If several initiatives could match, ask the user to choose.
2. Read `state.md` first, then the complete approved `spec.md`, then any existing `plan.md`.
3. Read `<skill-base>/../../references/artifact-protocol.md` and validate the initiative before planning.
4. Confirm `spec.md` is approved and `state.md` pins its current revision. Stop if either check fails.
5. Inspect the repository thoroughly enough to name exact files, existing interfaces, test conventions, setup commands, and relevant constraints.
6. Design the smallest vertical slices that deliver independently verifiable behavior. Avoid speculative infrastructure.
7. Create or revise draft `plan.md` from `<skill-base>/assets/plan-template.md`. Pin the exact spec revision.
8. Map every acceptance criterion to one or more tasks in `Spec Traceability`. Report any criterion with no task as a blocking plan defect.
9. Present the plan for review, then use the user question tool to ask whether to approve the complete plan or request revisions. Do not use a prose-only approval prompt. Revise as requested and repeat the tool-based approval question until the user explicitly approves the complete plan.
10. On approval, set `plan.md` to `status: approved`, set `approved_at`, and pin its revision in `state.md`.
11. Record the dated approval in `Decision and Deviation Log`, set the next action to explicit invocation of `jsip:implement`, validate, report paths and revisions, then stop.

## Task Contract

Each task must include:

- Objective and linked acceptance criterion IDs.
- Dependencies on earlier tasks, if any.
- Exact files to create, modify, and test.
- A focused test-first RED step with the exact command and expected failure reason.
- The smallest GREEN implementation step.
- A behavior-preserving REFACTOR step only where justified.
- Focused and broader verification commands with expected outcomes.
- Observable completion criteria and `state.md` evidence to record.

Use checkboxes so `jsip:implement` can persist progress. Include enough detail for a fresh agent to continue without relying on prior chat context, but reference approved documents instead of duplicating or paraphrasing intent.

## Drift Checks

Before approval:

1. Compare every task against the pinned spec revision.
2. Confirm every acceptance criterion is traced.
3. Remove tasks that serve no approved goal.
4. Confirm no task weakens an `Intent and Drift Guardrails` invariant.
5. Confirm verification proves user-visible behavior rather than implementation details alone.

If implementation would require a specification change, append a dated proposed change to `state.md`, set status to `blocked`, and stop. Tell the user to explicitly invoke `jsip:brainstorm` to revise intent. Planning must not hide scope or architecture changes as implementation details.
