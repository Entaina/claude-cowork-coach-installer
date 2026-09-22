"""Integrity checks for the Markdown package; not an app integration test."""
from pathlib import Path
import hashlib
import json
import re
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "AIOS/skills"
BASELINE = json.loads((ROOT / "tests/baseline-2.0.0.json").read_text())


def frontmatter(path):
    text = path.read_text()
    assert text.startswith("---\n"), f"Missing frontmatter: {path}"
    return yaml.safe_load(text.split("---", 2)[1])


class PackageIntegrity(unittest.TestCase):
    def test_skill_metadata(self):
        paths = list(SKILLS.glob("*/SKILL.md"))
        self.assertTrue(paths)
        for path in paths:
            with self.subTest(skill=path.parent.name):
                data = frontmatter(path)
                self.assertEqual(data["name"], path.parent.name)
                self.assertRegex(data["name"], r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
                self.assertLessEqual(len(data["name"]), 64)
                self.assertIsInstance(data["description"], str)
                self.assertTrue(data["description"].strip())
                self.assertLessEqual(len(data["description"]), 1024)
                self.assertIsInstance(data.get("metadata", {}), dict)

    def test_system_skills_resolve(self):
        for path in (ROOT / "AIOS/systems").glob("*.md"):
            for name in frontmatter(path).get("skills", "").split(","):
                name = name.strip()
                if name:
                    with self.subTest(system=path.name, skill=name):
                        self.assertTrue((SKILLS / name / "SKILL.md").is_file())

    def test_skill_map_covers_canonical_skills(self):
        content = (ROOT / "AIOS/mapa-skills.md").read_text()
        for path in SKILLS.glob("*/SKILL.md"):
            with self.subTest(skill=path.parent.name):
                self.assertIn(path.parent.name, content)

    def test_explicit_aios_file_references_resolve(self):
        paths = list((ROOT / "AIOS").rglob("*.md"))
        paths += [ROOT / name for name in ("AGENTS.md", "ME.md", "INSTALL.md")]
        count = 0
        for path in paths:
            for reference in re.findall(r"`(AIOS/[^`\n]+\.md)`", path.read_text()):
                if any(marker in reference for marker in ("{", "<", "*", "…")):
                    continue  # Template paths are intentionally not concrete files.
                count += 1
                with self.subTest(file=path.relative_to(ROOT), target=reference):
                    self.assertTrue((ROOT / reference).is_file(), reference)
        self.assertGreater(count, 0)

    def test_version_has_changelog_and_migration(self):
        version = re.search(r"`(\d+\.\d+\.\d+)`", (ROOT / "AIOS/VERSION.md").read_text())[1]
        changelog = (ROOT / "CHANGELOG.md").read_text()
        self.assertEqual(version, re.search(r"^## \[([^]]+)\]", changelog, re.M)[1])
        self.assertTrue((ROOT / "migrations" / f"{version}.md").is_file())

    def test_migration_originals_are_pristine(self):
        directory = ROOT / "migrations/2.1.0/originals"
        actual = {path.relative_to(directory).as_posix() for path in directory.rglob("*") if path.is_file()}
        self.assertEqual(actual, set(BASELINE["originals"]))
        for relative, digest in BASELINE["originals"].items():
            with self.subTest(file=relative):
                self.assertEqual(hashlib.sha256((directory / relative).read_bytes()).hexdigest(), digest)

    def test_previous_migrations_remain_unchanged(self):
        for relative, digest in BASELINE["historical_migrations"].items():
            with self.subTest(file=relative):
                self.assertEqual(hashlib.sha256((ROOT / relative).read_bytes()).hexdigest(), digest)


if __name__ == "__main__":
    unittest.main()
