import hashlib
import inspect
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from install_skills import InstallerError, install_skills  # noqa: E402


PROCRAFT_MANIFEST_NAME = ".procraft-manifest.json"
PROCRAFT_SKILLS = ["procraft"]
SKILL_NAME = PROCRAFT_SKILLS[0]
MANIFEST_FIELDS = {
    "manifest_version",
    "distribution",
    "package_version",
    "source",
    "mode",
    "skills",
    "files",
}


def write_skill(root, name, body):
    skill = root / name
    (skill / "agents").mkdir(parents=True)
    (skill / "SKILL.md").write_text(body, encoding="utf-8")
    (skill / "agents" / "openai.yaml").write_text("interface: {}\n", encoding="utf-8")


class InstallSkillsTests(unittest.TestCase):
    def test_installer_source_has_no_retired_migration_surface(self):
        source = (ROOT / "tools" / "install_skills.py").read_text(encoding="utf-8")
        retired_markers = (
            "legacy" + "_migration",
            "legacy-" + "v0." + "1.0",
            ".prompt" + "-skill-suite-manifest.json",
        )

        for marker in retired_markers:
            with self.subTest(marker=marker):
                self.assertNotIn(marker, source)

    def test_root_cli_dry_run_does_not_write(self):
        with tempfile.TemporaryDirectory() as source_dir, tempfile.TemporaryDirectory() as target_dir:
            source = Path(source_dir)
            target = Path(target_dir)
            write_skill(source, SKILL_NAME, SKILL_NAME)
            completed = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "install_skills.py"),
                    "--source",
                    str(source),
                    "--target",
                    str(target),
                    "--source-ref",
                    "local-test",
                    "--dry-run",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(0, completed.returncode, completed.stderr)
            self.assertEqual([], list(target.iterdir()))
            manifest = json.loads(completed.stdout)
            self.assertEqual("local-test", manifest["source"]["ref"])

    def test_dry_run_does_not_write(self):
        with tempfile.TemporaryDirectory() as source_dir, tempfile.TemporaryDirectory() as target_dir:
            source = Path(source_dir)
            target = Path(target_dir)
            write_skill(source, SKILL_NAME, SKILL_NAME)
            result = install_skills(source, target, dry_run=True)
            self.assertEqual("clean_install", result["mode"])
            self.assertEqual(PROCRAFT_SKILLS, result["skills"])
            self.assertEqual([], list(target.iterdir()))

    def test_canonical_distribution_contains_only_procraft(self):
        with tempfile.TemporaryDirectory() as source_dir, tempfile.TemporaryDirectory() as target_dir:
            source = Path(source_dir)
            target = Path(target_dir)
            for name in reversed(PROCRAFT_SKILLS):
                write_skill(source, name, name)

            result = install_skills(source, target, dry_run=True)

            self.assertEqual(PROCRAFT_SKILLS, result["skills"])

    def test_manifest_v2_has_exact_distribution_metadata(self):
        self.assertIn("source_ref", inspect.signature(install_skills).parameters)
        with tempfile.TemporaryDirectory() as source_dir, tempfile.TemporaryDirectory() as target_dir:
            source = Path(source_dir)
            target = Path(target_dir)
            write_skill(source, "procraft", "procraft")

            result = install_skills(source, target, dry_run=True, source_ref="v0.3.0")

            self.assertEqual(MANIFEST_FIELDS, set(result))
            self.assertEqual("2.0", result["manifest_version"])
            self.assertEqual("procraft", result["distribution"])
            self.assertEqual("0.3.0", result["package_version"])
            self.assertEqual(
                {
                    "repository": "https://github.com/Xerneas216/ProCraft",
                    "ref": "v0.3.0",
                },
                result["source"],
            )
            self.assertEqual("clean_install", result["mode"])
            self.assertEqual(["procraft"], result["skills"])

    def test_noncanonical_skill_set_is_rejected(self):
        with tempfile.TemporaryDirectory() as source_dir, tempfile.TemporaryDirectory() as target_dir:
            source = Path(source_dir)
            target = Path(target_dir)
            write_skill(source, "other", "other")

            with self.assertRaisesRegex(InstallerError, "exactly.*procraft"):
                install_skills(source, target)

    def test_empty_source_ref_is_rejected(self):
        with tempfile.TemporaryDirectory() as source_dir, tempfile.TemporaryDirectory() as target_dir:
            source = Path(source_dir)
            target = Path(target_dir)
            write_skill(source, SKILL_NAME, SKILL_NAME)

            with self.assertRaisesRegex(InstallerError, "non-empty.*tag or commit"):
                install_skills(source, target, source_ref="  ")

    def test_missing_metadata_is_rejected(self):
        with tempfile.TemporaryDirectory() as source_dir, tempfile.TemporaryDirectory() as target_dir:
            source = Path(source_dir)
            target = Path(target_dir)
            skill = source / SKILL_NAME
            skill.mkdir()
            (skill / "SKILL.md").write_text(SKILL_NAME, encoding="utf-8")

            with self.assertRaisesRegex(InstallerError, "Missing agents/openai.yaml"):
                install_skills(source, target)

    def test_name_conflict_is_rejected_before_copy(self):
        with tempfile.TemporaryDirectory() as source_dir, tempfile.TemporaryDirectory() as target_dir:
            source = Path(source_dir)
            target = Path(target_dir)
            write_skill(source, SKILL_NAME, "new")
            write_skill(target, SKILL_NAME, "existing")

            with self.assertRaises(InstallerError):
                install_skills(source, target)

            self.assertEqual("existing", (target / SKILL_NAME / "SKILL.md").read_text(encoding="utf-8"))

    def test_existing_manifest_is_rejected_before_copy(self):
        with tempfile.TemporaryDirectory() as source_dir, tempfile.TemporaryDirectory() as target_dir:
            source = Path(source_dir)
            target = Path(target_dir)
            write_skill(source, SKILL_NAME, SKILL_NAME)
            (target / PROCRAFT_MANIFEST_NAME).write_text("{}\n", encoding="utf-8")

            with self.assertRaisesRegex(InstallerError, "existing manifest"):
                install_skills(source, target)

            self.assertFalse((target / SKILL_NAME).exists())

    def test_copy_and_manifest_hashes_match(self):
        with tempfile.TemporaryDirectory() as source_dir, tempfile.TemporaryDirectory() as target_dir:
            source = Path(source_dir)
            target = Path(target_dir)
            write_skill(source, SKILL_NAME, SKILL_NAME)

            result = install_skills(source, target)

            copied = target / SKILL_NAME / "SKILL.md"
            expected = hashlib.sha256(copied.read_bytes()).hexdigest()
            self.assertEqual(expected, result["files"][f"{SKILL_NAME}/SKILL.md"])
            self.assertEqual("clean_install", result["mode"])
            self.assertTrue((target / PROCRAFT_MANIFEST_NAME).is_file())

    def test_copy_failure_cleans_partial_destination(self):
        with tempfile.TemporaryDirectory() as source_dir, tempfile.TemporaryDirectory() as target_dir:
            source = Path(source_dir)
            target = Path(target_dir)
            write_skill(source, SKILL_NAME, SKILL_NAME)

            def partial_copy(_source, destination):
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_text("partial", encoding="utf-8")
                raise OSError("simulated copy failure")

            with patch("install_skills.shutil.copy2", side_effect=partial_copy):
                with self.assertRaises(OSError):
                    install_skills(source, target)

            self.assertEqual([], list(target.iterdir()))

    def test_manifest_publish_failure_cleans_skills_and_staging(self):
        with tempfile.TemporaryDirectory() as source_dir, tempfile.TemporaryDirectory() as target_dir:
            source = Path(source_dir)
            target = Path(target_dir)
            write_skill(source, SKILL_NAME, SKILL_NAME)

            with patch("install_skills.os.link", side_effect=OSError("simulated publish failure")):
                with self.assertRaises(OSError):
                    install_skills(source, target)

            self.assertEqual([], list(target.iterdir()))

    def test_publish_race_does_not_delete_foreign_directory(self):
        with tempfile.TemporaryDirectory() as source_dir, tempfile.TemporaryDirectory() as target_dir:
            source = Path(source_dir)
            target = Path(target_dir)
            write_skill(source, SKILL_NAME, SKILL_NAME)

            def race_publish(_source, destination):
                destination.mkdir(parents=True)
                (destination / "foreign.txt").write_text("foreign", encoding="utf-8")
                raise FileExistsError("simulated concurrent install")

            with patch("install_skills.os.rename", side_effect=race_publish):
                with self.assertRaises(FileExistsError):
                    install_skills(source, target)

            self.assertEqual(
                "foreign",
                (target / SKILL_NAME / "foreign.txt").read_text(encoding="utf-8"),
            )

    def test_cleanup_failure_reports_published_install(self):
        with tempfile.TemporaryDirectory() as source_dir, tempfile.TemporaryDirectory() as target_dir:
            source = Path(source_dir)
            target = Path(target_dir)
            write_skill(source, SKILL_NAME, SKILL_NAME)

            with patch(
                "install_skills._cleanup_staging_root",
                side_effect=OSError("simulated cleanup failure"),
            ) as cleanup:
                with self.assertRaisesRegex(
                    InstallerError,
                    "published and verified.*staging cleanup failed",
                ):
                    install_skills(source, target)

            cleanup.assert_called_once()
            self.assertTrue((target / SKILL_NAME).is_dir())
            self.assertTrue((target / PROCRAFT_MANIFEST_NAME).is_file())
            stages = [path for path in target.iterdir() if path.name.startswith(".procraft-stage-")]
            self.assertEqual(1, len(stages))

    def test_unlisted_cache_files_are_not_copied(self):
        with tempfile.TemporaryDirectory() as source_dir, tempfile.TemporaryDirectory() as target_dir:
            source = Path(source_dir)
            target = Path(target_dir)
            write_skill(source, SKILL_NAME, SKILL_NAME)
            cache = source / SKILL_NAME / "__pycache__"
            cache.mkdir()
            (cache / "module.pyc").write_bytes(b"cache")

            result = install_skills(source, target)

            self.assertNotIn(f"{SKILL_NAME}/__pycache__/module.pyc", result["files"])
            self.assertFalse((target / SKILL_NAME / "__pycache__").exists())


if __name__ == "__main__":
    unittest.main()
