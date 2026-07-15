#!/usr/bin/env python3
"""Install verified ProCraft skills with conflict detection and rollback."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path


MANIFEST_NAME = ".procraft-manifest.json"
STAGING_PREFIX = ".procraft-stage-"
PROCRAFT_SKILLS = [
    "procraft",
    "defining-prompt-contracts",
    "prompting-general-tasks",
    "prompting-tool-agents",
    "prompting-software-engineering",
    "reviewing-prompt-packages",
    "evaluating-prompt-packages",
]


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
    by_name = {path.name: path for path in skills}
    if set(by_name) == set(PROCRAFT_SKILLS):
        return [by_name[name] for name in PROCRAFT_SKILLS]
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


def _identity(path: Path) -> tuple[int, int]:
    stat = path.stat()
    return stat.st_dev, stat.st_ino


def _installed_file_set(root: Path, skill_names: list[str]) -> set[str]:
    files: set[str] = set()
    for skill_name in skill_names:
        skill_root = root / skill_name
        if not skill_root.is_dir() or skill_root.is_symlink():
            continue
        for path in skill_root.rglob("*"):
            if path.is_symlink():
                files.add(f"!symlink:{(Path(skill_name) / path.relative_to(skill_root)).as_posix()}")
            elif path.is_file():
                files.add((Path(skill_name) / path.relative_to(skill_root)).as_posix())
    return files


def _tree_matches_manifest(
    root: Path,
    skill_names: list[str],
    expected_hashes: dict[str, str],
) -> bool:
    try:
        if _installed_file_set(root, skill_names) != set(expected_hashes):
            return False
        return all(_sha256(root / Path(relative)) == expected for relative, expected in expected_hashes.items())
    except OSError:
        return False


def _write_manifest(path: Path, manifest: dict) -> None:
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(manifest, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())


def _skill_hashes(expected_hashes: dict[str, str], skill_name: str) -> dict[str, str]:
    return {
        relative: expected
        for relative, expected in expected_hashes.items()
        if relative.startswith(f"{skill_name}/")
    }


def _remove_matching_manifest(path: Path, identity: tuple[int, int], expected_bytes: bytes) -> None:
    if path.is_file() and _identity(path) == identity and path.read_bytes() == expected_bytes:
        path.unlink()


def _remove_matching_skills(
    target: Path,
    published: list[tuple[Path, tuple[int, int]]],
    expected_hashes: dict[str, str],
) -> list[str]:
    errors: list[str] = []
    for destination, identity in reversed(published):
        if not destination.exists():
            continue
        hashes = _skill_hashes(expected_hashes, destination.name)
        try:
            matches = _identity(destination) == identity and _tree_matches_manifest(
                target, [destination.name], hashes
            )
        except OSError:
            matches = False
        if not matches:
            errors.append(f"refused to remove changed published skill {destination.name}")
            continue
        shutil.rmtree(destination)
    return errors


def _cleanup_staging_root(staging_root: Path) -> None:
    try:
        shutil.rmtree(staging_root)
    except FileNotFoundError:
        return


def install_skills(source: Path, target: Path, dry_run: bool = False) -> dict:
    """Install a new verified ProCraft suite without overwriting existing skills."""
    source = source.resolve()
    target = target.resolve()
    skills = _skill_dirs(source)
    skill_names = [skill.name for skill in skills]
    source_files = _source_files(skills)
    expected_hashes = {relative: _sha256(path) for relative, path in source_files}
    manifest_path = target / MANIFEST_NAME

    if manifest_path.exists():
        raise InstallerError(f"Refusing to overwrite existing manifest: {manifest_path}")
    conflicts = [name for name in skill_names if (target / name).exists()]
    if conflicts:
        raise InstallerError("Refusing to overwrite existing skills: " + ", ".join(conflicts))

    manifest = {
        "manifest_version": "1.0",
        "mode": "clean_install",
        "source": str(source),
        "skills": skill_names,
        "files": expected_hashes,
    }
    if dry_run:
        return manifest

    target.mkdir(parents=True, exist_ok=True)
    staging_root = Path(tempfile.mkdtemp(dir=target, prefix=STAGING_PREFIX))
    staged_new_root = staging_root / "new"
    staged_manifest = staged_new_root / MANIFEST_NAME
    published: list[tuple[Path, tuple[int, int]]] = []
    manifest_identity: tuple[int, int] | None = None
    manifest_bytes = b""

    try:
        staged_new_root.mkdir()
        for relative, source_path in source_files:
            staged_path = staged_new_root / Path(relative)
            staged_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, staged_path)
        if not _tree_matches_manifest(staged_new_root, skill_names, expected_hashes):
            raise InstallerError("Staged file set or hash does not match the source manifest")
        _write_manifest(staged_manifest, manifest)
        manifest_identity = _identity(staged_manifest)
        manifest_bytes = staged_manifest.read_bytes()

        concurrent_conflicts = [name for name in skill_names if (target / name).exists()]
        if concurrent_conflicts or manifest_path.exists():
            details = ", ".join(concurrent_conflicts) or str(manifest_path)
            raise InstallerError(f"Installation target changed during staging: {details}")

        for skill_name in skill_names:
            destination = target / skill_name
            staged_skill = staged_new_root / skill_name
            staged_identity = _identity(staged_skill)
            os.rename(staged_skill, destination)
            published.append((destination, staged_identity))

        if not _tree_matches_manifest(target, skill_names, expected_hashes):
            raise InstallerError("Published file set or hash does not match the source manifest")
        os.link(staged_manifest, manifest_path)
        if (
            _identity(manifest_path) != manifest_identity
            or manifest_path.read_bytes() != manifest_bytes
            or not _tree_matches_manifest(target, skill_names, expected_hashes)
        ):
            raise InstallerError("Published ProCraft installation failed final verification")
    except Exception as exc:
        rollback_errors: list[str] = []
        if manifest_identity is not None:
            try:
                _remove_matching_manifest(manifest_path, manifest_identity, manifest_bytes)
            except OSError as rollback_exc:
                rollback_errors.append(f"cannot remove new manifest: {rollback_exc}")
        rollback_errors.extend(_remove_matching_skills(target, published, expected_hashes))
        if rollback_errors:
            raise InstallerError(
                f"Installation failed and rollback was incomplete: {'; '.join(rollback_errors)}"
            ) from exc
        try:
            _cleanup_staging_root(staging_root)
        except OSError as cleanup_exc:
            raise InstallerError(
                f"Installation failed; rollback completed, but staging cleanup failed: {cleanup_exc}"
            ) from exc
        raise
    try:
        _cleanup_staging_root(staging_root)
    except OSError as exc:
        raise InstallerError(
            f"Installation was published and verified, but staging cleanup failed: {exc}"
        ) from exc
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
