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
        for pattern in ("*.md", "*.yaml", "*.yml", "*.json", "*.py", "*.txt"):
            with self.subTest(pattern=pattern):
                self.assertIn(f"{pattern} text eol=lf", attributes)


if __name__ == "__main__":
    unittest.main()
