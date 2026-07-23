---
name: brainstorm
description: Use ONLY when the user explicitly invokes jsip:brainstorm to turn one initiative idea into a dated, approved JSIP specification before planning or implementation.
---

# JSIP Brainstorm

Turn an idea into an approved specification whose recorded intent can anchor every later decision. The documents are durable handoff context, not a retrospective summary.

## Non-Negotiable Boundaries

- Do not write implementation code, create implementation scaffolding, or make behavior changes.
- Do not create `plan.md`; that belongs to `jsip:plan`.
- Ask one question at a time and wait for the answer.
- Never create a git commit unless the user separately and explicitly requests one.
- Stop after approval. Do not automatically invoke or perform the planning stage.
- Resolve bundled paths from this skill's base directory supplied by the harness, never from the target repository.

## Workflow

1. Inspect the repository's relevant code, documentation, instructions, and current behavior before proposing a design.
2. Determine whether the user is continuing an existing JSIP initiative or starting one. If ambiguous, ask.
3. For a new initiative, create `docs/jsip/initiatives/YYYY-MM-DD-<slug>/` using the current date and a concise lowercase slug.
4. Initialize draft `spec.md` and `state.md` from `<skill-base>/assets/`. Reuse an existing draft rather than creating a competing initiative.
5. Read `<skill-base>/../../references/artifact-protocol.md` and maintain its metadata and revision rules.
6. Clarify purpose, users, current behavior, desired behavior, constraints, non-goals, success criteria, and risks one question at a time.
7. Present two or three viable approaches with tradeoffs and a recommendation. Record the selected approach and why alternatives were rejected.
8. Present the proposed design in reviewable sections. Revise until the user explicitly approves the complete specification.
9. Run the initiative validator and correct structural errors before requesting final approval:

   ```bash
   python3 "<jsip-plugin-root>/scripts/validate_initiative.py" "docs/jsip/initiatives/<initiative>"
   ```

10. On explicit approval, set `spec.md` to `status: approved`, set `approved_at`, and increment its revision if an earlier approved revision changed.
11. Pin that spec revision in `state.md`, record the dated approval in `Decision and Deviation Log`, and set the next action to explicit invocation of `jsip:plan`.
12. Validate again, report the artifact paths and approved revision, then stop.

## Specification Quality Gate

Do not approve a specification until it contains concrete content for every required section:

- **Intent:** Why this initiative exists and the user outcome it must preserve.
- **Goals and Non-Goals:** Explicit scope boundaries.
- **Constraints:** Technical, product, operational, and compatibility limits.
- **Design:** Components, interfaces, data flow, failure handling, and testing implications at appropriate depth.
- **Acceptance Criteria:** Observable, uniquely numbered requirements such as `AC-1`.
- **Intent and Drift Guardrails:** Decisions, invariants, prohibited shortcuts, and conditions that require renewed approval. State that this section exists to prevent implementation drift from approved intent.

Remove ambiguity, placeholders, unresolved contradictions, and unbounded scope before approval. If an open question affects behavior or architecture, resolve it with the user rather than guessing.

## Existing Approved Specifications

Never silently revise approved intent. If invoked to change an approved specification:

1. Explain the proposed change and affected acceptance criteria.
2. Obtain explicit approval for the revision.
3. Increment `spec.md` revision and update `approved_at`.
4. Mark any existing `plan.md` as `stale`.
5. Update `state.md` pins and append a dated reason to `Decision and Deviation Log`.

The stable filenames and dated initiative directory preserve references and chronology while revisions expose changed intent.
