import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


class PackagingTests(unittest.TestCase):
    def json_file(self, relative_path):
        return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))

    def test_versions_and_names_are_aligned(self):
        codex = self.json_file(".codex-plugin/plugin.json")
        claude = self.json_file(".claude-plugin/plugin.json")
        package = self.json_file("package.json")

        self.assertEqual({codex["name"], claude["name"], package["name"]}, {"jsip"})
        base_versions = {
            manifest["version"].split("+", 1)[0]
            for manifest in (codex, claude, package)
        }
        self.assertEqual(base_versions, {"0.1.0"})
        self.assertTrue((ROOT / package["main"]).is_file())

    def test_marketplaces_publish_the_root_plugin(self):
        codex = self.json_file(".agents/plugins/marketplace.json")
        claude = self.json_file(".claude-plugin/marketplace.json")

        self.assertEqual(codex["name"], "jsip-dev")
        self.assertEqual(codex["plugins"][0]["source"]["path"], ".")
        self.assertEqual(claude["name"], "jsip-dev")
        self.assertEqual(claude["plugins"][0]["source"], "./")

    def test_documentation_explains_drift_prevention_and_platform_usage(self):
        readme_path = ROOT / "README.md"
        self.assertTrue(readme_path.is_file(), "README.md is required")
        readme = readme_path.read_text(encoding="utf-8")

        for phrase in (
            "prevent drift",
            "docs/jsip/initiatives/YYYY-MM-DD-<slug>/",
            "jsip:brainstorm",
            "jsip:plan",
            "jsip:implement",
            "Codex",
            "Claude Code",
            "OpenCode",
        ):
            self.assertIn(phrase, readme)

    def test_generated_placeholders_are_removed(self):
        for path in ROOT.glob("skills/**/SKILL.md"):
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertNotIn("[TODO:", path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
