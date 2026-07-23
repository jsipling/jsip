#!/usr/bin/env python3
"""Validate a JSIP initiative's documents and pinned revisions."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


INITIATIVE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*$")
HEADING_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
ACCEPTANCE_CRITERION_RE = re.compile(r"\bAC-\d+\b")

REQUIRED_HEADINGS = {
    "spec.md": (
        "Intent",
        "Goals",
        "Non-Goals",
        "Constraints",
        "Design",
        "Acceptance Criteria",
        "Intent and Drift Guardrails",
    ),
    "plan.md": ("Goal", "Spec Traceability", "Tasks", "Verification"),
    "state.md": (
        "Current Position",
        "Approved Inputs",
        "Decision and Deviation Log",
        "Verification Evidence",
        "Blockers",
        "Next Action",
    ),
}


@dataclass(frozen=True)
class Document:
    name: str
    metadata: dict[str, str]
    body: str


def parse_document(path: Path, errors: list[str]) -> Document | None:
    if not path.is_file():
        errors.append(f"missing required document `{path.name}`")
        return None

    content = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", content, re.DOTALL)
    if not match:
        errors.append(f"{path.name} must start with YAML frontmatter")
        return None

    metadata: dict[str, str] = {}
    for line_number, line in enumerate(match.group(1).splitlines(), start=2):
        if not line.strip():
            continue
        key, separator, value = line.partition(":")
        if not separator or not key.strip() or not value.strip():
            errors.append(f"{path.name}:{line_number} has invalid scalar frontmatter")
            continue
        metadata[key.strip()] = value.strip().strip("\"'")

    return Document(path.name, metadata, match.group(2))


def require_metadata(document: Document, keys: tuple[str, ...], errors: list[str]) -> None:
    for key in keys:
        if not document.metadata.get(key):
            errors.append(f"{document.name} is missing frontmatter field `{key}`")


def integer_metadata(document: Document, key: str, errors: list[str]) -> int | None:
    value = document.metadata.get(key)
    if value is None:
        return None
    try:
        parsed = int(value)
    except ValueError:
        errors.append(f"{document.name} field `{key}` must be a positive integer")
        return None
    if parsed < 1:
        errors.append(f"{document.name} field `{key}` must be a positive integer")
        return None
    return parsed


def validate_headings(document: Document, errors: list[str]) -> None:
    headings = set(HEADING_RE.findall(document.body))
    for heading in REQUIRED_HEADINGS[document.name]:
        if heading not in headings:
            errors.append(f"{document.name} is missing heading `{heading}`")


def section_body(document: Document, heading: str) -> str:
    match = re.search(
        rf"^##\s+{re.escape(heading)}\s*$\n(.*?)(?=^##\s+|\Z)",
        document.body,
        re.MULTILINE | re.DOTALL,
    )
    return match.group(1) if match else ""


def validate_document_identity(
    document: Document, initiative: str, artifact: str, errors: list[str]
) -> None:
    require_metadata(document, ("jsip_version", "initiative", "artifact"), errors)
    if document.metadata.get("jsip_version") != "1":
        errors.append(f"{document.name} field `jsip_version` must be `1`")
    if document.metadata.get("initiative") != initiative:
        errors.append(f"{document.name} initiative does not match directory `{initiative}`")
    if document.metadata.get("artifact") != artifact:
        errors.append(f"{document.name} field `artifact` must be `{artifact}`")
    validate_headings(document, errors)


def validate_initiative(path: Path | str) -> list[str]:
    initiative_path = Path(path).resolve()
    errors: list[str] = []
    initiative = initiative_path.name

    if not initiative_path.is_dir():
        return [f"initiative directory does not exist: {initiative_path}"]
    if not INITIATIVE_RE.fullmatch(initiative):
        errors.append("initiative directory must use `YYYY-MM-DD-lowercase-slug` format")

    spec = parse_document(initiative_path / "spec.md", errors)
    state = parse_document(initiative_path / "state.md", errors)
    plan_path = initiative_path / "plan.md"
    plan = parse_document(plan_path, errors) if plan_path.exists() else None

    if spec:
        validate_document_identity(spec, initiative, "spec", errors)
        require_metadata(spec, ("status", "revision", "created"), errors)
        if spec.metadata.get("status") not in {"draft", "approved", "superseded"}:
            errors.append("spec.md field `status` must be draft, approved, or superseded")
        if spec.metadata.get("status") == "approved" and not spec.metadata.get("approved_at"):
            errors.append("approved spec.md requires `approved_at`")

    if state:
        validate_document_identity(state, initiative, "state", errors)
        require_metadata(state, ("phase", "status", "spec_revision", "updated"), errors)
        if state.metadata.get("phase") not in {"brainstorm", "plan", "implement", "complete"}:
            errors.append("state.md field `phase` must be brainstorm, plan, implement, or complete")
        if state.metadata.get("status") not in {
            "active",
            "awaiting-approval",
            "blocked",
            "completed",
        }:
            errors.append(
                "state.md field `status` must be active, awaiting-approval, blocked, or completed"
            )

    phase = state.metadata.get("phase") if state else None
    if phase in {"plan", "implement", "complete"} and plan is None:
        errors.append(f"{phase} phase requires plan.md")

    if plan:
        validate_document_identity(plan, initiative, "plan", errors)
        require_metadata(
            plan, ("status", "revision", "spec_revision", "created"), errors
        )
        if plan.metadata.get("status") not in {"draft", "approved", "stale", "completed"}:
            errors.append("plan.md field `status` must be draft, approved, stale, or completed")
        if plan.metadata.get("status") == "approved" and not plan.metadata.get("approved_at"):
            errors.append("approved plan.md requires `approved_at`")

    spec_revision = integer_metadata(spec, "revision", errors) if spec else None
    state_spec_revision = integer_metadata(state, "spec_revision", errors) if state else None
    if spec_revision and state_spec_revision and spec_revision != state_spec_revision:
        errors.append(
            f"state.md pins spec revision {state_spec_revision} but spec.md is revision {spec_revision}"
        )

    if plan:
        plan_revision = integer_metadata(plan, "revision", errors)
        plan_spec_revision = integer_metadata(plan, "spec_revision", errors)
        if spec_revision and plan_spec_revision and spec_revision != plan_spec_revision:
            errors.append(
                f"plan.md pins spec revision {plan_spec_revision} but spec.md is revision {spec_revision}"
            )
        if state:
            require_metadata(state, ("plan_revision",), errors)
            state_plan_revision = integer_metadata(state, "plan_revision", errors)
            if plan_revision and state_plan_revision and plan_revision != state_plan_revision:
                errors.append(
                    f"state.md pins plan revision {state_plan_revision} but plan.md is revision {plan_revision}"
                )

        if spec:
            criteria = set(ACCEPTANCE_CRITERION_RE.findall(spec.body))
            traceability = section_body(plan, "Spec Traceability")
            planned = set(ACCEPTANCE_CRITERION_RE.findall(traceability))
            for criterion in sorted(criteria - planned):
                errors.append(f"plan.md does not trace acceptance criterion {criterion}")

    if phase == "implement":
        if spec and spec.metadata.get("status") != "approved":
            errors.append("implement phase requires an approved spec")
        if plan and plan.metadata.get("status") != "approved":
            errors.append("implement phase requires an approved plan")

    if phase == "complete":
        if state and state.metadata.get("status") != "completed":
            errors.append("complete phase requires state status completed")
        if plan and plan.metadata.get("status") != "completed":
            errors.append("complete phase requires plan status completed")

    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("initiative", help="Path to docs/jsip/initiatives/YYYY-MM-DD-slug")
    args = parser.parse_args()
    errors = validate_initiative(args.initiative)
    if errors:
        print("JSIP initiative validation failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print(f"JSIP initiative validation passed: {Path(args.initiative).resolve()}")


if __name__ == "__main__":
    main()
