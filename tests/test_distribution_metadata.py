import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DistributionMetadataTests(unittest.TestCase):
    def test_runtime_and_development_dependencies_are_pinned(self):
        runtime = (ROOT / "requirements.txt").read_text(encoding="utf-8").splitlines()
        development = (ROOT / "requirements-dev.txt").read_text(encoding="utf-8").splitlines()

        self.assertEqual(["jsonschema==4.23.0"], runtime)
        self.assertEqual(["-r requirements.txt", "PyYAML==6.0.2"], development)

    def test_repository_text_formats_are_forced_to_lf(self):
        path = ROOT / ".gitattributes"
        self.assertTrue(path.is_file())
        attributes = path.read_text(encoding="utf-8").splitlines()
        for pattern in (
            ".gitattributes",
            "*.md",
            "*.yaml",
            "*.yml",
            "*.json",
            "*.py",
            "*.txt",
            "*.sha256",
        ):
            with self.subTest(pattern=pattern):
                self.assertIn(f"{pattern} text eol=lf", attributes)

    def test_distributed_skill_text_is_physically_lf_only(self):
        skill_root = ROOT / "skills" / "procraft"
        text_suffixes = {".md", ".yaml", ".yml", ".json", ".py", ".txt"}
        for path in sorted(skill_root.rglob("*")):
            if path.is_file() and path.suffix in text_suffixes:
                with self.subTest(path=path.relative_to(ROOT).as_posix()):
                    self.assertNotIn(b"\r", path.read_bytes())

    def test_ci_covers_supported_platforms_and_python_versions(self):
        workflow = ROOT / ".github" / "workflows" / "ci.yml"
        self.assertTrue(workflow.is_file())
        content = workflow.read_text(encoding="utf-8")
        for value in (
            "ubuntu-latest",
            "windows-latest",
            '"3.8"',
            '"3.12"',
            "pip install -r requirements-dev.txt",
            "python -m unittest discover -s tests -v",
            "python tools/build_release.py",
        ):
            with self.subTest(value=value):
                self.assertIn(value, content)

    def test_ci_rebuilds_outside_dist_and_checks_the_committed_checksum(self):
        workflow = ROOT / ".github" / "workflows" / "ci.yml"
        content = workflow.read_text(encoding="utf-8")
        for value in (
            "python tools/build_release.py --output-dir build-release",
            "build-release/procraft-v0.3.0.zip",
            "dist/procraft-v0.3.0.zip.sha256",
            "hashlib.sha256",
            "if actual != expected",
        ):
            with self.subTest(value=value):
                self.assertIn(value, content)
        self.assertNotIn("- run: python tools/build_release.py\n", content)
        self.assertIn("push:\n    branches: [main]", content)


if __name__ == "__main__":
    unittest.main()
