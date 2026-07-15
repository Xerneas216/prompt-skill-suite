import hashlib
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


LEGACY_MANIFEST_NAME = ".prompt-skill-suite-manifest.json"
PROCRAFT_MANIFEST_NAME = ".procraft-manifest.json"
KNOWN_LEGACY_MANIFEST = ROOT / "tools" / "legacy-v0.1.0-manifest.json"
INTERNAL_SKILLS = [
    "defining-prompt-contracts",
    "prompting-general-tasks",
    "prompting-tool-agents",
    "prompting-software-engineering",
    "reviewing-prompt-packages",
    "evaluating-prompt-packages",
]


def write_skill(root, name, body):
    skill = root / name
    (skill / "agents").mkdir(parents=True)
    (skill / "SKILL.md").write_text(body, encoding="utf-8")
    (skill / "agents" / "openai.yaml").write_text("interface: {}\n", encoding="utf-8")


def file_hashes(root, skill_names):
    files = {}
    for skill_name in skill_names:
        for path in sorted((root / skill_name).rglob("*")):
            if path.is_file():
                relative = (Path(skill_name) / path.relative_to(root / skill_name)).as_posix()
                files[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    return files


def write_suite(root, entry_name, marker):
    names = [entry_name, *INTERNAL_SKILLS]
    for name in names:
        write_skill(root, name, f"{marker}:{name}")
    return names


def write_legacy_install(target):
    skill_names = write_suite(target, "building-prompt-packages", "legacy-v0.1.0")
    manifest = {
        "manifest_version": "1.0",
        "source": "known-v0.1.0-release",
        "skills": skill_names,
        "files": file_hashes(target, skill_names),
    }
    (target / LEGACY_MANIFEST_NAME).write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def tree_snapshot(root):
    return {
        "directories": sorted(path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_dir()),
        "files": {
            path.relative_to(root).as_posix(): path.read_bytes()
            for path in sorted(root.rglob("*"))
            if path.is_file()
        },
    }


class InstallSkillsTests(unittest.TestCase):
    def test_v0_1_0_release_hashes_are_committed_as_the_trust_anchor(self):
        if not KNOWN_LEGACY_MANIFEST.is_file():
            self.fail("tools/legacy-v0.1.0-manifest.json must be committed")
        manifest = json.loads(KNOWN_LEGACY_MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual("v0.1.0", manifest.get("release"))
        self.assertEqual(
            ["building-prompt-packages", *INTERNAL_SKILLS],
            manifest.get("skills"),
        )
        hashes = manifest.get("files", {})
        self.assertTrue(hashes)
        self.assertIn("building-prompt-packages/SKILL.md", hashes)
        for relative, digest in hashes.items():
            with self.subTest(relative=relative):
                self.assertRegex(digest, r"\A[0-9a-f]{64}\Z")

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
            self.assertEqual("clean_install", result.get("mode"))
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
            self.assertEqual("clean_install", result.get("mode"))
            self.assertTrue((target / PROCRAFT_MANIFEST_NAME).is_file())
            self.assertFalse((target / LEGACY_MANIFEST_NAME).exists())

    def _install_with_known_legacy(self, source, target, legacy_manifest, dry_run=False):
        try:
            return install_skills(
                source,
                target,
                dry_run=dry_run,
                known_legacy_manifests=[legacy_manifest],
            )
        except TypeError as exc:
            self.fail(f"installer must support trusted legacy manifests without breaking its existing API: {exc}")

    def test_matching_known_legacy_install_migrates_atomically(self):
        with tempfile.TemporaryDirectory() as source_dir, tempfile.TemporaryDirectory() as target_dir:
            source = Path(source_dir)
            target = Path(target_dir)
            new_skills = write_suite(source, "procraft", "v0.2.0")
            legacy_manifest = write_legacy_install(target)

            dry_run = self._install_with_known_legacy(
                source, target, legacy_manifest, dry_run=True
            )
            self.assertEqual("legacy_migration", dry_run["mode"])
            self.assertTrue((target / "building-prompt-packages").is_dir())
            self.assertFalse((target / "procraft").exists())

            result = self._install_with_known_legacy(source, target, legacy_manifest)

            self.assertEqual("legacy_migration", result["mode"])
            self.assertEqual(new_skills, result["skills"])
            self.assertFalse((target / "building-prompt-packages").exists())
            self.assertFalse((target / LEGACY_MANIFEST_NAME).exists())
            self.assertTrue((target / PROCRAFT_MANIFEST_NAME).is_file())
            for skill_name in new_skills:
                self.assertEqual(
                    f"v0.2.0:{skill_name}",
                    (target / skill_name / "SKILL.md").read_text(encoding="utf-8"),
                )

    def test_changed_legacy_install_is_rejected_without_any_write(self):
        mutations = {
            "modified": lambda target: (target / "defining-prompt-contracts" / "SKILL.md").write_text(
                "user modification", encoding="utf-8"
            ),
            "extra": lambda target: (target / "defining-prompt-contracts" / "extra.txt").write_text(
                "external", encoding="utf-8"
            ),
            "missing": lambda target: (target / "defining-prompt-contracts" / "SKILL.md").unlink(),
        }
        for case, mutate in mutations.items():
            with self.subTest(case=case), tempfile.TemporaryDirectory() as source_dir, tempfile.TemporaryDirectory() as target_dir:
                source = Path(source_dir)
                target = Path(target_dir)
                write_suite(source, "procraft", "v0.2.0")
                legacy_manifest = write_legacy_install(target)
                mutate(target)
                before = tree_snapshot(target)

                with self.assertRaises(InstallerError):
                    self._install_with_known_legacy(source, target, legacy_manifest)

                self.assertEqual(before, tree_snapshot(target))

    def test_migration_publish_failure_restores_the_complete_legacy_install(self):
        with tempfile.TemporaryDirectory() as source_dir, tempfile.TemporaryDirectory() as target_dir:
            source = Path(source_dir)
            target = Path(target_dir)
            write_suite(source, "procraft", "v0.2.0")
            legacy_manifest = write_legacy_install(target)
            before = tree_snapshot(target)

            with patch("install_skills.os.link", side_effect=OSError("simulated manifest publish failure")):
                with self.assertRaises(OSError):
                    self._install_with_known_legacy(source, target, legacy_manifest)

            self.assertEqual(before, tree_snapshot(target))

    def test_migration_race_preserves_foreign_content_and_restores_legacy(self):
        with tempfile.TemporaryDirectory() as source_dir, tempfile.TemporaryDirectory() as target_dir:
            source = Path(source_dir)
            target = Path(target_dir).resolve()
            write_suite(source, "procraft", "v0.2.0")
            legacy_manifest = write_legacy_install(target)
            original_rename = os.rename

            def race_on_procraft_publish(staged, destination):
                destination = Path(destination)
                if destination == target / "procraft":
                    destination.mkdir(parents=True)
                    (destination / "foreign.txt").write_text("foreign", encoding="utf-8")
                    raise FileExistsError("simulated concurrent ProCraft install")
                return original_rename(staged, destination)

            with patch("install_skills.os.rename", side_effect=race_on_procraft_publish):
                with self.assertRaises((InstallerError, FileExistsError)):
                    self._install_with_known_legacy(source, target, legacy_manifest)

            self.assertEqual(
                "foreign", (target / "procraft" / "foreign.txt").read_text(encoding="utf-8")
            )
            self.assertTrue((target / "building-prompt-packages" / "SKILL.md").is_file())
            self.assertTrue((target / LEGACY_MANIFEST_NAME).is_file())
            self.assertFalse((target / PROCRAFT_MANIFEST_NAME).exists())

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
