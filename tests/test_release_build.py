from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable
BUILD_SCRIPT = ROOT / "tools" / "build_release.py"
ARCHIVE_NAME = "procraft-v0.3.0.zip"
CHECKSUM_NAME = f"{ARCHIVE_NAME}.sha256"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class ReleaseBuildTests(unittest.TestCase):
    def build(self, output_dir: Path) -> tuple[bytes, str]:
        self.assertTrue(BUILD_SCRIPT.is_file(), f"Missing release builder: {BUILD_SCRIPT}")
        subprocess.run(
            [str(PYTHON), str(BUILD_SCRIPT), "--output-dir", str(output_dir)],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        archive = (output_dir / ARCHIVE_NAME).read_bytes()
        checksum = (output_dir / CHECKSUM_NAME).read_text(encoding="ascii")
        return archive, checksum

    def test_build_creates_v030_artifacts_with_exact_members_and_hashes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output_dir = Path(temporary)
            archive_bytes, checksum = self.build(output_dir)

            expected_files = sorted(
                f"procraft/{path.relative_to(ROOT / 'skills' / 'procraft').as_posix()}"
                for path in (ROOT / "skills" / "procraft").rglob("*")
                if path.is_file() and path.suffix != ".pyc" and "__pycache__" not in path.parts
            )
            with zipfile.ZipFile(output_dir / ARCHIVE_NAME) as release:
                self.assertEqual([".procraft-manifest.json", *expected_files], release.namelist())
                for member in release.infolist():
                    self.assertEqual((1980, 1, 1, 0, 0, 0), member.date_time)
                    self.assertNotIn("\\", member.filename)
                manifest = json.loads(release.read(".procraft-manifest.json"))
                self.assertEqual("2.0", manifest["manifest_version"])
                self.assertEqual("0.3.0", manifest["package_version"])
                self.assertEqual("v0.3.0", manifest["source"]["ref"])
                self.assertEqual(["procraft"], manifest["skills"])
                self.assertEqual(
                    manifest["files"],
                    {name: sha256(release.read(name)) for name in expected_files},
                )

        self.assertEqual(f"{sha256(archive_bytes)}  {ARCHIVE_NAME}\n", checksum)

    def test_two_consecutive_builds_are_byte_identical(self) -> None:
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            first_archive, first_checksum = self.build(Path(first))
            second_archive, second_checksum = self.build(Path(second))

        self.assertEqual(first_archive, second_archive)
        self.assertEqual(first_checksum, second_checksum)

    def test_all_members_use_the_portable_stored_method(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output_dir = Path(temporary)
            self.build(output_dir)
            with zipfile.ZipFile(output_dir / ARCHIVE_NAME) as release:
                self.assertEqual(
                    {zipfile.ZIP_STORED},
                    {member.compress_type for member in release.infolist()},
                )

    def test_checksum_writer_is_python_38_compatible(self) -> None:
        source = BUILD_SCRIPT.read_text(encoding="utf-8")
        self.assertNotIn("checksum_path.write_text", source)


if __name__ == "__main__":
    unittest.main()
