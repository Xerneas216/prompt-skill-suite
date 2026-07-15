import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from install_skills import InstallerError, install_skills  # noqa: E402


def write_skill(root, name, body):
    skill = root / name
    (skill / "agents").mkdir(parents=True)
    (skill / "SKILL.md").write_text(body, encoding="utf-8")
    (skill / "agents" / "openai.yaml").write_text("interface: {}\n", encoding="utf-8")


class InstallSkillsTests(unittest.TestCase):
    def test_root_cli_dry_run_does_not_write(self):
        with tempfile.TemporaryDirectory() as source_dir, tempfile.TemporaryDirectory() as target_dir:
            source = Path(source_dir)
            target = Path(target_dir)
            write_skill(source, "one", "one")
            completed = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "install_skills.py"),
                    "--source",
                    str(source),
                    "--target",
                    str(target),
                    "--dry-run",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(0, completed.returncode, completed.stderr)
            self.assertEqual([], list(target.iterdir()))

    def test_dry_run_does_not_write(self):
        with tempfile.TemporaryDirectory() as source_dir, tempfile.TemporaryDirectory() as target_dir:
            source = Path(source_dir)
            target = Path(target_dir)
            write_skill(source, "one", "one")
            result = install_skills(source, target, dry_run=True)
            self.assertEqual(["one"], result["skills"])
            self.assertEqual([], list(target.iterdir()))

    def test_default_refuses_name_conflict_before_copy(self):
        with tempfile.TemporaryDirectory() as source_dir, tempfile.TemporaryDirectory() as target_dir:
            source = Path(source_dir)
            target = Path(target_dir)
            write_skill(source, "one", "new")
            write_skill(source, "two", "two")
            write_skill(target, "one", "existing")
            with self.assertRaises(InstallerError):
                install_skills(source, target)
            self.assertFalse((target / "two").exists())

    def test_copy_and_manifest_hashes_match(self):
        with tempfile.TemporaryDirectory() as source_dir, tempfile.TemporaryDirectory() as target_dir:
            source = Path(source_dir)
            target = Path(target_dir)
            write_skill(source, "one", "one")
            result = install_skills(source, target)
            copied = target / "one" / "SKILL.md"
            expected = hashlib.sha256(copied.read_bytes()).hexdigest()
            self.assertEqual(expected, result["files"]["one/SKILL.md"])
            self.assertTrue((target / ".prompt-skill-suite-manifest.json").is_file())

    def test_copytree_failure_cleans_partial_destination(self):
        with tempfile.TemporaryDirectory() as source_dir, tempfile.TemporaryDirectory() as target_dir:
            source = Path(source_dir)
            target = Path(target_dir)
            write_skill(source, "one", "one")

            def partial_copy(_source, destination):
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_text("partial", encoding="utf-8")
                raise OSError("simulated copy failure")

            with patch("install_skills.shutil.copy2", side_effect=partial_copy):
                with self.assertRaises(OSError):
                    install_skills(source, target)
            self.assertEqual([], list(target.iterdir()))

    def test_manifest_replace_failure_cleans_skills_and_temp_manifest(self):
        with tempfile.TemporaryDirectory() as source_dir, tempfile.TemporaryDirectory() as target_dir:
            source = Path(source_dir)
            target = Path(target_dir)
            write_skill(source, "one", "one")
            with patch("install_skills.os.link", side_effect=OSError("simulated manifest publish failure")):
                with self.assertRaises(OSError):
                    install_skills(source, target)
            self.assertEqual([], list(target.iterdir()))

    def test_publish_race_does_not_delete_foreign_directory(self):
        with tempfile.TemporaryDirectory() as source_dir, tempfile.TemporaryDirectory() as target_dir:
            source = Path(source_dir)
            target = Path(target_dir)
            write_skill(source, "one", "one")

            def race_publish(_source, destination):
                destination.mkdir(parents=True)
                (destination / "foreign.txt").write_text("foreign", encoding="utf-8")
                raise FileExistsError("simulated concurrent install")

            with patch("install_skills.os.rename", side_effect=race_publish):
                with self.assertRaises(FileExistsError):
                    install_skills(source, target)
            self.assertEqual("foreign", (target / "one" / "foreign.txt").read_text(encoding="utf-8"))

    def test_unlisted_cache_files_are_not_copied(self):
        with tempfile.TemporaryDirectory() as source_dir, tempfile.TemporaryDirectory() as target_dir:
            source = Path(source_dir)
            target = Path(target_dir)
            write_skill(source, "one", "one")
            cache = source / "one" / "__pycache__"
            cache.mkdir()
            (cache / "module.pyc").write_bytes(b"cache")
            result = install_skills(source, target)
            self.assertNotIn("one/__pycache__/module.pyc", result["files"])
            self.assertFalse((target / "one" / "__pycache__").exists())


if __name__ == "__main__":
    unittest.main()
