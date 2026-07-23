---
jsip_version: 1
initiative: {{initiative}}
artifact: plan
status: draft
revision: 1
spec_revision: {{approved_spec_revision}}
created: {{date}}
---
# {{title}} Implementation Plan

## Goal
{{one sentence tied to approved intent}}

## Spec Traceability
- AC-1: Task 1

## Tasks

### Task 1: {{vertical slice}}

- [ ] Objective and acceptance criteria: {{objective}}; AC-1
- [ ] Files: {{exact create, modify, and test paths}}
- [ ] RED: {{test change, exact command, and expected missing-behavior failure}}
- [ ] GREEN: {{smallest production change}}
- [ ] REFACTOR: {{justified cleanup or none}}
- [ ] Verification: {{focused and broader commands with expected outcomes}}
- [ ] Evidence: Record commands and outcomes in `state.md`.

## Verification
- {{full tests, lint, formatting, and build commands appropriate to the repository}}
