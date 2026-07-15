# GPT-5.6 Prompt Skill Suite

Seven Codex skills for turning a natural-language request into a reviewed, schema-valid, and evaluable PromptPackage v1. `building-prompt-packages` is the user-facing entry; the other six skills are internal contract, scenario, review, and evaluation modules.

PromptPackage JSON is canonical. Markdown is generated only from JSON that passes both JSON Schema and semantic validation.

## Project layout

- `skills/`: exactly seven source skills.
- `skills/building-prompt-packages/references/prompt-package.schema.json`: normative PromptPackage v1 schema.
- `skills/building-prompt-packages/scripts/validate_package.py`: schema and semantic validator.
- `skills/building-prompt-packages/scripts/render_package.py`: deterministic JSON-to-Markdown renderer.
- `evals/fixtures/representative-cases.json`: provider-neutral evaluation cases.
- `evals/results/`: recorded RED/GREEN comparisons; unavailable fresh-context runs are marked `not_run`.
- `install_skills.py`: copy installer with dry-run, conflict detection, and SHA-256 manifest.

## Verify

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Validate a package:

```powershell
.\.venv\Scripts\python.exe skills\building-prompt-packages\scripts\validate_package.py prompt-package.json
```

Render a validated package:

```powershell
.\.venv\Scripts\python.exe skills\building-prompt-packages\scripts\render_package.py prompt-package.json --output prompt-package.md
```

## Install

Preview without writing:

```powershell
.\.venv\Scripts\python.exe install_skills.py --dry-run
```

Install into the default Codex skills directory:

```powershell
.\.venv\Scripts\python.exe install_skills.py
```

The installer refuses every same-name skill conflict before publishing anything. It copies only manifest-listed files into a unique staging directory, verifies the complete staged set, rechecks conflicts, publishes without overwrite, verifies the installed set, and then atomically publishes `.prompt-skill-suite-manifest.json`. Failure cleanup never removes a concurrently created target.

## Verification scope

Deterministic tests validate the schema, semantic references, rendering, fixture shape, installation conflicts, and source-to-copy hashes. Dynamic fresh-context evaluation is a separate gate: when no runtime is available, the package must say `not_run` and must not claim quality validation.
