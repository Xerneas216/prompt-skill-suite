#!/usr/bin/env python3
"""Install verified ProCraft skills with conflict detection and safe migration."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any


MANIFEST_NAME = ".procraft-manifest.json"
LEGACY_MANIFEST_NAME = ".prompt-skill-suite-manifest.json"
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
KNOWN_LEGACY_MANIFEST_PATH = Path(__file__).with_name("legacy-v0.1.0-manifest.json")


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
        # ProCraft v0.2 uses an entry-first public ordering; v0.1 used alphabetical discovery.
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


def _tree_fingerprint(root: Path, skill_names: list[str]) -> dict[str, tuple[int, int, int, int, int]]:
    fingerprint: dict[str, tuple[int, int, int, int, int]] = {}
    for skill_name in skill_names:
        skill_root = root / skill_name
        for path in [skill_root, *sorted(skill_root.rglob("*"))]:
            stat = path.stat()
            relative = path.relative_to(root).as_posix()
            fingerprint[relative] = (
                stat.st_dev,
                stat.st_ino,
                stat.st_mode,
                stat.st_size,
                stat.st_mtime_ns,
            )
    return fingerprint


def _validate_manifest_shape(manifest: Any, label: str) -> tuple[list[str], dict[str, str]]:
    if not isinstance(manifest, dict):
        raise InstallerError(f"{label} must contain a JSON object")
    skills = manifest.get("skills")
    files = manifest.get("files")
    if (
        not isinstance(skills, list)
        or not skills
        or any(not isinstance(name, str) or not name or Path(name).name != name for name in skills)
        or len(skills) != len(set(skills))
    ):
        raise InstallerError(f"{label} has an invalid skills list")
    if not isinstance(files, dict) or not files:
        raise InstallerError(f"{label} has an invalid files map")
    for relative, digest in files.items():
        if not isinstance(relative, str) or not isinstance(digest, str):
            raise InstallerError(f"{label} has a non-string file entry")
        path = PurePosixPath(relative)
        if (
            path.is_absolute()
            or not path.parts
            or path.parts[0] not in skills
            or any(part in {"", ".", ".."} for part in path.parts)
            or len(digest) != 64
            or any(character not in "0123456789abcdef" for character in digest)
        ):
            raise InstallerError(f"{label} has an invalid file entry: {relative}")
    return skills, files


def _load_known_legacy_manifests() -> list[dict[str, Any]]:
    """Load committed trust anchors; callers cannot supply migration trust."""
    try:
        manifest = json.loads(KNOWN_LEGACY_MANIFEST_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise InstallerError(f"Cannot load legacy trust anchor: {KNOWN_LEGACY_MANIFEST_PATH}") from exc
    _validate_manifest_shape(manifest, "Legacy trust anchor")
    return [manifest]


def _read_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise InstallerError(f"Cannot read {label}: {path}") from exc
    if not isinstance(value, dict):
        raise InstallerError(f"{label} must contain a JSON object")
    return value


def _trusted_legacy_state(target: Path, legacy_manifest_path: Path) -> dict[str, Any]:
    installed = _read_json(legacy_manifest_path, "legacy manifest")
    installed_skills, installed_files = _validate_manifest_shape(installed, "Legacy manifest")
    trusted: dict[str, Any] | None = None
    for candidate in _load_known_legacy_manifests():
        candidate_skills, candidate_files = _validate_manifest_shape(candidate, "Legacy trust anchor")
        if installed_skills == candidate_skills and installed_files == candidate_files:
            trusted = candidate
            break
    if trusted is None:
        raise InstallerError("Legacy manifest does not match a committed trust anchor")
    if not _tree_matches_manifest(target, installed_skills, installed_files):
        raise InstallerError("Legacy skill files are missing, modified, or contain untracked content")
    return {
        "skills": installed_skills,
        "files": installed_files,
        "manifest_bytes": legacy_manifest_path.read_bytes(),
        "manifest_identity": _identity(legacy_manifest_path),
        "tree_fingerprint": _tree_fingerprint(target, installed_skills),
    }


def _legacy_state_is_current(target: Path, legacy_manifest_path: Path, state: dict[str, Any]) -> bool:
    try:
        return (
            legacy_manifest_path.read_bytes() == state["manifest_bytes"]
            and _identity(legacy_manifest_path) == state["manifest_identity"]
            and _tree_fingerprint(target, state["skills"]) == state["tree_fingerprint"]
            and _tree_matches_manifest(target, state["skills"], state["files"])
        )
    except OSError:
        return False


def _write_manifest(path: Path, manifest: dict[str, Any]) -> None:
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


def _restore_legacy_backup(
    target: Path,
    backup_root: Path,
    legacy_skill_names: list[str],
    legacy_manifest_path: Path,
) -> list[str]:
    errors: list[str] = []
    for skill_name in legacy_skill_names:
        backup = backup_root / skill_name
        if not backup.exists():
            continue
        destination = target / skill_name
        if destination.exists():
            errors.append(f"cannot restore {skill_name}: destination appeared")
            continue
        try:
            os.rename(backup, destination)
        except OSError as exc:
            errors.append(f"cannot restore {skill_name}: {exc}")
    backup_manifest = backup_root / LEGACY_MANIFEST_NAME
    if backup_manifest.exists():
        if legacy_manifest_path.exists():
            errors.append("cannot restore legacy manifest: destination appeared")
        else:
            try:
                os.rename(backup_manifest, legacy_manifest_path)
            except OSError as exc:
                errors.append(f"cannot restore legacy manifest: {exc}")
    return errors


def install_skills(source: Path, target: Path, dry_run: bool = False) -> dict[str, Any]:
    """Install discovered skills or migrate an exact trusted v0.1.0 installation."""
    source = source.resolve()
    target = target.resolve()
    skills = _skill_dirs(source)
    skill_names = [skill.name for skill in skills]
    source_files = _source_files(skills)
    expected_hashes = {relative: _sha256(path) for relative, path in source_files}
    manifest_path = target / MANIFEST_NAME
    legacy_manifest_path = target / LEGACY_MANIFEST_NAME
    legacy_state: dict[str, Any] | None = None

    if manifest_path.exists():
        raise InstallerError(f"Refusing to overwrite existing manifest: {manifest_path}")
    if legacy_manifest_path.exists():
        if skill_names != PROCRAFT_SKILLS:
            raise InstallerError("Legacy migration requires the complete seven-skill ProCraft source suite")
        legacy_state = _trusted_legacy_state(target, legacy_manifest_path)
        allowed_conflicts = set(legacy_state["skills"])
        conflicts = [name for name in skill_names if (target / name).exists() and name not in allowed_conflicts]
        if conflicts:
            raise InstallerError("Refusing to overwrite existing skills: " + ", ".join(conflicts))
        mode = "legacy_migration"
    else:
        conflicts = [name for name in skill_names if (target / name).exists()]
        if conflicts:
            raise InstallerError("Refusing to overwrite existing skills: " + ", ".join(conflicts))
        mode = "clean_install"

    manifest = {
        "manifest_version": "1.0",
        "mode": mode,
        "source": str(source),
        "skills": skill_names,
        "files": expected_hashes,
    }
    if dry_run:
        return manifest

    target.mkdir(parents=True, exist_ok=True)
    staging_root = Path(tempfile.mkdtemp(dir=target, prefix=STAGING_PREFIX))
    staged_new_root = staging_root / "new"
    staged_new_root.mkdir()
    staged_manifest = staged_new_root / MANIFEST_NAME
    backup_root = staging_root / "backup"
    published: list[tuple[Path, tuple[int, int]]] = []
    manifest_identity: tuple[int, int] | None = None
    manifest_bytes = b""
    keep_stage = False
    migration_started = False

    try:
        for relative, source_path in source_files:
            staged_path = staged_new_root / Path(relative)
            staged_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, staged_path)
        if not _tree_matches_manifest(staged_new_root, skill_names, expected_hashes):
            raise InstallerError("Staged file set or hash does not match the source manifest")
        _write_manifest(staged_manifest, manifest)
        manifest_identity = _identity(staged_manifest)
        manifest_bytes = staged_manifest.read_bytes()

        if mode == "legacy_migration":
            assert legacy_state is not None
            if manifest_path.exists() or (target / "procraft").exists():
                raise InstallerError("Installation target changed during staging")
            if not _legacy_state_is_current(target, legacy_manifest_path, legacy_state):
                raise InstallerError("Legacy installation changed during staging")

            backup_root.mkdir()
            migration_started = True
            for legacy_skill_name in legacy_state["skills"]:
                os.rename(target / legacy_skill_name, backup_root / legacy_skill_name)
            os.rename(legacy_manifest_path, backup_root / LEGACY_MANIFEST_NAME)
        else:
            concurrent_conflicts = [name for name in skill_names if (target / name).exists()]
            if concurrent_conflicts or manifest_path.exists() or legacy_manifest_path.exists():
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
        if mode == "legacy_migration" and (
            legacy_manifest_path.exists() or (target / "building-prompt-packages").exists()
        ):
            raise InstallerError("Legacy entry or manifest remains after migration")
    except Exception as exc:
        rollback_errors: list[str] = []
        if manifest_identity is not None:
            try:
                _remove_matching_manifest(manifest_path, manifest_identity, manifest_bytes)
            except OSError as rollback_exc:
                rollback_errors.append(f"cannot remove new manifest: {rollback_exc}")
        rollback_errors.extend(_remove_matching_skills(target, published, expected_hashes))
        if migration_started and legacy_state is not None:
            rollback_errors.extend(
                _restore_legacy_backup(target, backup_root, legacy_state["skills"], legacy_manifest_path)
            )
            if not rollback_errors and not _legacy_state_is_current(target, legacy_manifest_path, legacy_state):
                rollback_errors.append("restored legacy installation failed verification")
        if rollback_errors:
            keep_stage = True
            raise InstallerError(
                f"Installation failed and rollback was incomplete: {'; '.join(rollback_errors)}"
            ) from exc
        raise
    finally:
        if not keep_stage and staging_root.exists():
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
