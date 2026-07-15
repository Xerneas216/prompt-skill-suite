#!/usr/bin/env python3
"""Copy verified skill sources with conflict detection and a SHA-256 manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any


MANIFEST_NAME = ".prompt-skill-suite-manifest.json"


class InstallerError(RuntimeError):
    """Raised when installation cannot proceed without partial or unsafe writes."""


def _skill_dirs(source: Path) -> list[Path]:
    if not source.is_dir():
        raise InstallerError(f"Source directory does not exist: {source}")
    skills = sorted(path for path in source.iterdir() if path.is_dir() and (path / "SKILL.md").is_file())
    if not skills:
        raise InstallerError(f"No skill directories found in: {source}")
    missing_metadata = [path.name for path in skills if not (path / "agents" / "openai.yaml").is_file()]
    if missing_metadata:
        raise InstallerError("Missing agents/openai.yaml: " + ", ".join(missing_metadata))
    return skills


def _source_files(skills: list[Path]) -> list[tuple[str, Path]]:
    files: list[tuple[str, Path]] = []
    for skill in skills:
        for path in sorted(skill.rglob("*")):
            if not path.is_file() or path.suffix == ".pyc" or "__pycache__" in path.parts:
                continue
            relative = Path(skill.name) / path.relative_to(skill)
            files.append((relative.as_posix(), path))
    return files


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _installed_file_set(root: Path, skill_names: list[str]) -> set[str]:
    files: set[str] = set()
    for skill_name in skill_names:
        skill_root = root / skill_name
        if not skill_root.is_dir():
            continue
        for path in skill_root.rglob("*"):
            if path.is_file():
                files.add((Path(skill_name) / path.relative_to(skill_root)).as_posix())
    return files


def _tree_matches_manifest(
    root: Path,
    skill_names: list[str],
    expected_hashes: dict[str, str],
) -> bool:
    if _installed_file_set(root, skill_names) != set(expected_hashes):
        return False
    return all(_sha256(root / Path(relative)) == expected for relative, expected in expected_hashes.items())


def install_skills(source: Path, target: Path, dry_run: bool = False) -> dict[str, Any]:
    """Install all discovered skills, refusing every same-name conflict by default."""
    source = source.resolve()
    target = target.resolve()
    skills = _skill_dirs(source)
    conflicts = [skill.name for skill in skills if (target / skill.name).exists()]
    if conflicts:
        raise InstallerError("Refusing to overwrite existing skills: " + ", ".join(conflicts))

    manifest_path = target / MANIFEST_NAME
    if manifest_path.exists():
        raise InstallerError(f"Refusing to overwrite existing manifest: {manifest_path}")

    source_files = _source_files(skills)
    manifest = {
        "manifest_version": "1.0",
        "source": str(source),
        "skills": [skill.name for skill in skills],
        "files": {relative: _sha256(path) for relative, path in source_files},
    }
    if dry_run:
        return manifest

    target.mkdir(parents=True, exist_ok=True)
    skill_names = [skill.name for skill in skills]
    expected_hashes = manifest["files"]
    staging_root = Path(tempfile.mkdtemp(dir=target, prefix=".prompt-skill-suite-stage-"))
    staged_manifest = staging_root / MANIFEST_NAME
    published: list[tuple[Path, tuple[int, int]]] = []
    try:
        for relative, source_path in source_files:
            staged_path = staging_root / Path(relative)
            staged_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, staged_path)
        if not _tree_matches_manifest(staging_root, skill_names, expected_hashes):
            raise InstallerError("Staged file set or hash does not match the source manifest")

        with staged_manifest.open("x", encoding="utf-8", newline="\n") as handle:
            json.dump(manifest, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())

        concurrent_conflicts = [name for name in skill_names if (target / name).exists()]
        if concurrent_conflicts or manifest_path.exists():
            details = ", ".join(concurrent_conflicts) or str(manifest_path)
            raise InstallerError(f"Installation target changed during staging: {details}")

        for skill_name in skill_names:
            destination = target / skill_name
            staged_skill = staging_root / skill_name
            staged_stat = staged_skill.stat()
            os.rename(staged_skill, destination)
            published.append((destination, (staged_stat.st_dev, staged_stat.st_ino)))

        if not _tree_matches_manifest(target, skill_names, expected_hashes):
            raise InstallerError("Published file set or hash does not match the source manifest")

        os.link(staged_manifest, manifest_path)
    except Exception:
        for destination, identity in reversed(published):
            if not destination.exists():
                continue
            stat = destination.stat()
            skill_name = destination.name
            skill_hashes = {
                relative: expected
                for relative, expected in expected_hashes.items()
                if relative.startswith(f"{skill_name}/")
            }
            if (stat.st_dev, stat.st_ino) == identity and _tree_matches_manifest(
                target, [skill_name], skill_hashes
            ):
                shutil.rmtree(destination, ignore_errors=True)
        raise
    finally:
        if staging_root.exists():
            shutil.rmtree(staging_root, ignore_errors=True)
    return manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path(__file__).resolve().parents[1] / "skills")
    parser.add_argument("--target", type=Path, default=Path.home() / ".codex" / "skills")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    try:
        manifest = install_skills(args.source, args.target, dry_run=args.dry_run)
    except InstallerError as exc:
        print(f"INSTALL ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
