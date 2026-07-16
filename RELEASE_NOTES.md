# ProCraft v0.3.0

ProCraft v0.3.0 supersedes v0.2.0. It migrates the distribution from seven Skill directories to one discoverable `procraft` Skill with six bundled internal references.

## Runtime and installation

- Supported development and verification runtimes are Python 3.8 through Python 3.12.
- Python and pinned dependencies run in an external runtime; they are not bundled in the Skill archive.
- Installation remains clean-install only and records a v2 `.procraft-manifest.json` with per-file SHA-256 hashes.

## Release artifact and verification

- `dist/procraft-v0.3.0.zip` contains only the v2 manifest and the installed `procraft` tree.
- `dist/procraft-v0.3.0.zip.sha256` records the archive checksum.
- Deterministic tests validate ZIP membership, timestamps, manifest hashes, and byte-for-byte rebuilds.
- CI covers Windows and Linux on Python 3.8 and Python 3.12.
- The fresh-context v0.3.0 dynamic trigger gate passed: implicit Prompt requests `5/5`, direct-task negatives `5/5`, and explicit `$procraft` `1/1`. Per-case evidence is recorded in `evals/results/procraft-v0.3.0-trigger-run.json`.

These notes are release text for a future GitHub v0.3.0 release. No tag or release is published by this repository change.
