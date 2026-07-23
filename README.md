# JSIP

JSIP is a document-driven project workflow for coding agents. It carries one initiative through explicit brainstorming, planning, and test-first implementation stages while preserving the user's approved intent.

## Why JSIP

Long-running agent work can gradually replace the original goal with assumptions from recent conversation or implementation details. JSIP creates durable source-of-truth documents to prevent drift where it matters:

- Approved intent lives in `spec.md`, not chat memory.
- Observable acceptance criteria have stable IDs that every plan must trace.
- Plans pin an exact specification revision.
- State pins both approved revisions and records the current task.
- Dated approvals, decisions, deviations, and verification evidence explain how the initiative evolved.
- Strict stage gates stop implementation before unapproved divergence.

Dates provide chronology and help future readers reconstruct context. Stable filenames and explicit revisions provide the actual consistency guarantees without breaking references.

## Workflow

| Skill | Purpose | Output |
| --- | --- | --- |
| `jsip:brainstorm` | Clarify intent, compare approaches, and approve a design | `spec.md` and initial `state.md` |
| `jsip:plan` | Derive vertical, test-first tasks from the approved spec | `plan.md` and updated `state.md` |
| `jsip:implement` | Execute approved tasks with RED-GREEN-REFACTOR and persisted evidence | Code, tests, completed plan, and final state |

Each stage must be explicitly invoked. JSIP never automatically advances to the next stage and never creates a git commit unless separately requested.

## Initiative Documents

Each feature, fix, or milestone has one dated directory:

```text
docs/jsip/initiatives/YYYY-MM-DD-<slug>/
├── spec.md
├── plan.md
└── state.md
```

Read `state.md` first when resuming work. It identifies the approved revisions, current position, blockers, evidence, and next action. See `references/artifact-protocol.md` for the full contract.

Validate an initiative before stage transitions and after revision changes:

```bash
python3 /path/to/jsip/scripts/validate_initiative.py \
  docs/jsip/initiatives/2026-07-23-example
```

## Installation

Restart the relevant application after installation or updates so it reloads plugin configuration.

### Codex

```bash
codex plugin marketplace add /path/to/jsip
codex plugin add jsip@jsip-dev
```

Codex exposes the skills through the `jsip` plugin namespace. Invoke the stage explicitly, for example `jsip:brainstorm`.

### Claude Code

```bash
claude plugin marketplace add /path/to/jsip --scope user
claude plugin install jsip@jsip-dev --scope user
```

Invoke `/jsip:brainstorm`, `/jsip:plan`, or `/jsip:implement`.

### OpenCode

Add the local adapter to the global `plugin` array in `~/.config/opencode/opencode.json`:

```json
{
  "plugin": [
    "file:///absolute/path/to/jsip/.opencode/plugins/jsip.js"
  ]
}
```

The adapter registers the shared skills and exact `/jsip:brainstorm`, `/jsip:plan`, and `/jsip:implement` aliases. OpenCode's native skill names cannot contain colons, so the aliases load the corresponding valid underlying skill without duplicating workflow content.

## Development

Run all repository tests:

```bash
python3 -m unittest discover -s tests -v
npm test
```

Validate each skill and the Codex and Claude manifests before release. The repository is licensed under MIT.
