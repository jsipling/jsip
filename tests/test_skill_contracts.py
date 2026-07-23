import re
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


class SkillContractTests(unittest.TestCase):
    def skill(self, name):
        path = ROOT / "skills" / name / "SKILL.md"
        self.assertTrue(path.is_file(), f"missing {path.relative_to(ROOT)}")
        return path.read_text(encoding="utf-8")

    def test_all_skills_are_explicit_and_do_not_commit(self):
        for name in ("brainstorm", "plan", "implement"):
            with self.subTest(skill=name):
                content = self.skill(name)
                self.assertRegex(content, rf"(?m)^name: {name}$")
                self.assertIn("explicitly invokes", content)
                self.assertIn("Never create a git commit", content)

                metadata = ROOT / "skills" / name / "agents" / "openai.yaml"
                self.assertTrue(metadata.is_file())
                self.assertIn(
                    "allow_implicit_invocation: false",
                    metadata.read_text(encoding="utf-8"),
                )

    def test_brainstorm_owns_specification_without_implementing(self):
        content = self.skill("brainstorm")

        for phrase in (
            "docs/jsip/initiatives/YYYY-MM-DD-<slug>/",
            "spec.md",
            "state.md",
            "Intent and Drift Guardrails",
            "Do not write implementation code",
            "Stop after approval",
        ):
            self.assertIn(phrase, content)

    def test_plan_requires_an_approved_spec_and_traces_acceptance_criteria(self):
        content = self.skill("plan")

        for phrase in (
            "approved `spec.md`",
            "pinned spec revision",
            "acceptance criterion",
            "test-first",
            "Do not modify production code",
            "Stop after approval",
        ):
            self.assertIn(phrase, content)

    def test_document_skills_resolve_bundled_resources_from_skill_base(self):
        for name in ("brainstorm", "plan"):
            with self.subTest(skill=name):
                self.assertIn(
                    "Resolve bundled paths from this skill's base directory",
                    self.skill(name),
                )

    def test_implement_validates_inputs_and_stops_on_drift(self):
        content = self.skill("implement")

        for phrase in (
            "validate_initiative.py",
            "RED",
            "GREEN",
            "Stop before deviating",
            "Decision and Deviation Log",
            "Verification Evidence",
            "Do not revise approved intent",
        ):
            self.assertIn(phrase, content)

    def test_implement_resolves_protocol_from_installed_plugin_root(self):
        content = self.skill("implement")

        for phrase in (
            "installed JSIP plugin root",
            "`<jsip-plugin-root>/references/artifact-protocol.md`",
            "Never resolve bundled paths from the current working directory",
        ):
            self.assertIn(phrase, content)

    def test_skill_frontmatter_has_only_name_and_description(self):
        for name in ("brainstorm", "plan", "implement"):
            with self.subTest(skill=name):
                content = self.skill(name)
                match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
                self.assertIsNotNone(match)
                keys = {
                    line.split(":", 1)[0]
                    for line in match.group(1).splitlines()
                    if ":" in line
                }
                self.assertEqual(keys, {"name", "description"})


if __name__ == "__main__":
    unittest.main()
