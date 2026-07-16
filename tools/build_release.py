#!/usr/bin/env python3
"""Build the deterministic ProCraft release archive and checksum."""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

from install_skills import install_skills


ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.3.0"
SOURCE_REF = f"v{VERSION}"
ARCHIVE_NAME = f"procraft-v{VERSION}.zip"
CHECKSUM_NAME = f"{ARCHIVE_NAME}.sha256"
FIXED_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
FILE_MODE = 0o100644 << 16


def _zip_info(name: str) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, FIXED_TIMESTAMP)
    info.compress_type = zipfile.ZIP_STORED
    info.create_system = 3
    info.external_attr = FILE_MODE
    return info


def _manifest_bytes(output_dir: Path) -> bytes:
    manifest = install_skills(
        source=ROOT / "skills",
        target=output_dir,
        dry_run=True,
        source_ref=SOURCE_REF,
    )
    return (json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def build_release(output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    archive_path = output_dir / ARCHIVE_NAME
    checksum_path = output_dir / CHECKSUM_NAME
    manifest_bytes = _manifest_bytes(output_dir)
    skill_root = ROOT / "skills" / "procraft"
    source_files = sorted(
        [
            path
            for path in skill_root.rglob("*")
            if path.is_file() and path.suffix != ".pyc" and "__pycache__" not in path.parts
        ],
        key=lambda path: path.relative_to(skill_root).as_posix(),
    )

    with zipfile.ZipFile(archive_path, mode="w") as archive:
        archive.writestr(_zip_info(".procraft-manifest.json"), manifest_bytes)
        for path in source_files:
            name = f"procraft/{path.relative_to(skill_root).as_posix()}"
            archive.writestr(_zip_info(name), path.read_bytes())

    digest = hashlib.sha256(archive_path.read_bytes()).hexdigest()
    with checksum_path.open("w", encoding="ascii", newline="\n") as checksum_file:
        checksum_file.write(f"{digest}  {ARCHIVE_NAME}\n")
    return archive_path, checksum_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    archive_path, checksum_path = build_release(args.output_dir)
    print(archive_path)
    print(checksum_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
