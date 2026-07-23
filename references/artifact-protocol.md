# JSIP Artifact Protocol v1

JSIP documents exist to preserve approved intent across sessions, agents, and implementation work. Dates establish chronology; stable paths, explicit revisions, traceability, and approval gates prevent drift.

## Location

Store one initiative at:

```text
docs/jsip/initiatives/YYYY-MM-DD-<slug>/
├── spec.md
├── plan.md
└── state.md
```

Use the creation date in the directory name. Keep filenames stable so later documents and tools can reference them without path churn.

## Shared Metadata

Every document starts with scalar YAML frontmatter:

- `jsip_version: 1`
- `initiative`: Exact initiative directory name.
- `artifact`: `spec`, `plan`, or `state`.

Dates use `YYYY-MM-DD`. Revisions are positive integers. Increment a revision only when an approved artifact changes; drafts may be edited in place before approval.

## Specification

`spec.md` statuses are `draft`, `approved`, and `superseded`. It requires `revision`, `created`, and `approved_at` when approved.

Acceptance criteria use stable IDs (`AC-1`, `AC-2`). `Intent and Drift Guardrails` records invariants, exclusions, and the conditions requiring renewed approval. Never remove an acceptance criterion from an approved revision without recording why.

## Plan

`plan.md` statuses are `draft`, `approved`, `stale`, and `completed`. It requires `revision`, `spec_revision`, `created`, and `approved_at` when approved.

The plan pins one approved spec revision. Every acceptance criterion in that spec must appear under `Spec Traceability` and map to at least one task. A changed approved spec makes the old plan stale until explicitly revised and approved.

## State

`state.md` is the recovery entry point. Read it before the other artifacts.

- `phase`: `brainstorm`, `plan`, `implement`, or `complete`.
- `status`: `active`, `awaiting-approval`, `blocked`, or `completed`.
- `spec_revision`: Current pinned spec revision.
- `plan_revision`: Current pinned plan revision when a plan exists.
- `updated`: Last state update date.

Keep `Decision and Deviation Log` chronological and append-only for approved decisions. Keep `Verification Evidence` concise and reproducible: command, outcome, date, and linked task or criterion.

## Change Control

Approved intent never changes silently. Stop before divergence, record the trigger and proposed change in `state.md`, and obtain explicit user approval in the owning stage. Specification changes belong to `jsip:brainstorm`; plan-only changes belong to `jsip:plan`.

Run `scripts/validate_initiative.py` before every stage transition and after revision changes. Structural validation complements, but does not replace, semantic comparison against approved intent.
