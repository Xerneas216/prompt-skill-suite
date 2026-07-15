# GPT-5.6 Prompt Skill Suite

[English](README.md) | [简体中文](README.zh-CN.md)

## Overview

GPT-5.6 Prompt Skill Suite is a collection of seven Codex skills for turning a natural-language prompt requirement into a reviewed, schema-valid, and evaluable **PromptPackage v1**.

The suite does more than draft a prompt. It first defines the task contract, routes the request through the relevant general, tool-agent, or software-engineering specialists, checks the result for semantic defects, validates the canonical JSON, renders a deterministic Markdown view, and records what evaluation was or was not performed.

This is an independent, unofficial open-source project. It is not affiliated with or endorsed by OpenAI.

## Origin and design principles

The project began as an effort to turn the practical guidance in two OpenAI documents into reusable Codex workflows:

- [Prompting guidance for GPT-5.6](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6)
- [GPT-5.6 model guidance](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.6)

The suite interprets that guidance through the following principles:

- **Start with the outcome.** State the user-visible result, constraints, evidence, success criteria, and stopping conditions. Avoid prescribing every reasoning step.
- **Keep prompts lean.** Remove repeated rules, redundant examples, contradictions, and tools unrelated to the task. Keep requirements that materially change behavior.
- **Use an explicit prompt contract.** Separate role, personality, collaboration style, goal, success criteria, constraints, evidence, permissions, output, and stop rules. Preserve every explicit user value.
- **Define autonomy boundaries once.** Let the model perform safe, in-scope local work while requiring approval for external writes, destructive actions, purchases, and material scope expansion.
- **Route tools deliberately.** Expose only relevant tools, resolve prerequisites before acting, parallelize independent reads, sequence dependent calls, and use meaningful fallbacks for empty or partial results.
- **Bound Programmatic Tool Calling.** Use PTC for deterministic reduction such as filtering, joining, ranking, deduplication, aggregation, batching, or repeated validation. Keep approvals, semantic judgment, citations, and final validation under direct model control.
- **Ground research in evidence.** Cite retrieved sources near supported claims, distinguish inference from sourced facts, surface conflicts, and report missing evidence instead of guessing.
- **Manage long work by outcomes.** Use a short preamble and sparse progress updates at major phase changes. Compact at meaningful milestones and avoid carrying stale reasoning into changed objectives.
- **Choose model controls by workload.** The suite uses `gpt-5.6` (the Sol route) as its quality-first baseline, treats `gpt-5.6-terra` as a cost-balanced candidate, and treats `gpt-5.6-luna` as a high-volume candidate. New tasks start evaluation at `medium` reasoning; higher settings are adopted only when representative evaluations show a benefit.
- **Separate default detail from task requirements.** Use `text.verbosity` for request-wide detail and the prompt contract for required structure, length, facts, caveats, and preservation rules.
- **Verify the artifact that matters.** Run targeted checks after software changes, disclose checks that could not run, preserve existing design systems, and render visual work before finalizing it.
- **Migrate through measurement.** Change one prompt, tool, or reasoning variable at a time. Treat lower tokens, latency, cost, or call counts as improvements only after output quality still meets the baseline.

These points are the project's concise interpretation, not a replacement for the official documentation. Consult the linked guides for current API details, limits, pricing, and feature availability.

## What the suite produces

A completed run can deliver:

- `prompt-package.json`: the canonical PromptPackage v1 source of truth.
- `prompt-package.md`: a deterministic human-readable rendering produced only from valid JSON.
- Static verification: semantic review plus JSON Schema and cross-reference validation.
- Evaluation records: representative cases and baseline comparison with honest `pass`, `fail`, or `not_run` status.

Optional sections are emitted only when they apply. For example, `tool_policy` appears only for tool-using requests, PTC configuration appears only for bounded deterministic processing, and persistent reasoning configuration is omitted from single-turn work.

## Skills

| Skill | Responsibility |
|---|---|
| `building-prompt-packages` | The only broad user-facing entry. Routes the request, composes applicable modules, validates the package, renders Markdown, and coordinates delivery. |
| `defining-prompt-contracts` | Converts the request into goals, success criteria, evidence requirements, permissions, output rules, and stopping conditions. |
| `prompting-general-tasks` | Handles research, analysis, writing, rewriting, summarization, extraction, and other general knowledge-work patterns. |
| `prompting-tool-agents` | Defines tool routing, retrieval, citations, approvals, PTC boundaries, long-task state, and fallbacks. |
| `prompting-software-engineering` | Covers diagnosis, implementation, testing, review, frontend work, and visual verification. |
| `reviewing-prompt-packages` | Finds repetition, contradictions, over-constraint, missing fields, irrelevant tools, and unverifiable requirements. |
| `evaluating-prompt-packages` | Creates representative cases, records execution evidence, and compares candidate prompts with a baseline. |

## Workflow

```text
Natural-language request
  -> Prompt Contract
  -> Scenario modules
  -> Candidate Prompt
  -> Static review
  -> JSON validation
  -> Markdown rendering
  -> Dynamic evaluation
  -> Delivery
```

`prompt-package.json` is authoritative. `prompt-package.md` is never maintained independently: the renderer reads a package that has already passed validation and produces sections in a fixed order.

## Requirements

- Windows with PowerShell for the documented commands.
- Python 3 with `venv` support.
- Codex with local skills support.
- Git for cloning and contributing.

Runtime validation uses `jsonschema>=4.23,<5`. Development and metadata checks also use `PyYAML>=6,<7`.

## Set up the repository

```powershell
git clone https://github.com/Xerneas216/prompt-skill-suite.git
Set-Location prompt-skill-suite
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

The final command establishes a local deterministic-test baseline before installation or modification.

## Install the skills

Preview the installation without writing anything:

```powershell
.\.venv\Scripts\python.exe install_skills.py --dry-run
```

Install all seven skills into the default Codex skills directory:

```powershell
.\.venv\Scripts\python.exe install_skills.py
```

The default target is `<home>/.codex/skills` (`%USERPROFILE%\.codex\skills` on Windows). The installer:

- discovers exactly the skill directories containing `SKILL.md` and `agents/openai.yaml`;
- refuses all same-name conflicts before publishing files;
- copies only manifest-listed source files through a unique staging directory;
- verifies the complete file set and SHA-256 hashes before and after publication;
- writes `.prompt-skill-suite-manifest.json` only after the installed copy is verified;
- avoids overwriting an existing installation or manifest.

If a conflict is reported, inspect and resolve the existing installation deliberately; the installer will not overwrite it. Start a new Codex task after installation so skill discovery refreshes.

## Use the suite

In a new Codex task, describe the prompt package you want in natural language. `building-prompt-packages` is the entry point and automatically selects the applicable specialists.

General, source-backed work:

> Build a high-quality prompt package for summarizing policy documents. Preserve every factual qualification, cite the supplied sources, and keep the final answer concise without dropping material caveats.

Tool-agent work:

> Build a prompt package for an agent that retrieves account and policy evidence, explains empty-result fallbacks, and asks for approval before any external write.

Software-engineering work:

> Build a prompt package for diagnosing and fixing a Python regression. Diagnosis alone must not modify files; an authorized fix must run targeted tests and disclose anything that could not be verified.

Mixed research and implementation:

> Build a prompt package for researching the current API requirements, citing primary sources, updating the in-scope integration, and validating the changed behavior without expanding the project scope.

Conversation delivery returns two layers:

1. A concise routing, model-settings, verification-status, and residual-risk summary.
2. The canonical JSON content followed by the Markdown rendered from that JSON.

The suite writes `prompt-package.json` and `prompt-package.md` to disk only when the user explicitly requests file delivery.

## Validate and render a package

Validate a candidate package:

```powershell
.\.venv\Scripts\python.exe skills\building-prompt-packages\scripts\validate_package.py prompt-package.json
```

Render Markdown only after validation succeeds:

```powershell
.\.venv\Scripts\python.exe skills\building-prompt-packages\scripts\render_package.py prompt-package.json --output prompt-package.md
```

The validator checks both the JSON Schema and semantic invariants such as explicit-value preservation, scenario-module coverage, message-layer separation, tool references, dependency cycles, PTC references, approval rules, embedded schemas, and evaluation evidence.

## Verification status

The deterministic test suite covers:

- PromptPackage schema and semantic validation;
- tool, dependency, PTC, and module references;
- deterministic Markdown rendering and safe code fences;
- provider-neutral evaluation-fixture structure;
- installer conflicts, staging failures, publication races, exact file sets, and source-to-copy hashes.

Fresh-context dynamic evaluation is a separate quality gate. When a suitable runtime is unavailable, its status remains `not_run`; deterministic tests do not turn that status into a model-quality claim.

## Repository layout

```text
prompt-skill-suite/
├── skills/                 # Seven source skills
├── evals/                  # Representative cases and RED/GREEN records
├── tests/                  # Deterministic unittest suite
├── tools/                  # Installer implementation
├── docs/superpowers/       # Approved design and implementation records
├── install_skills.py       # Root installation entry point
├── requirements.txt        # Runtime dependency
└── requirements-dev.txt    # Development dependencies
```

The normative schema is at `skills/building-prompt-packages/references/prompt-package.schema.json`. The validator and renderer live beside the entry skill under `scripts/`.

## Project status

The initial release is:

- designed for Codex skills;
- GPT-5.6-first, with later GPT-5.x behavior requiring fresh evaluation before adoption;
- documented and verified on Windows with PowerShell;
- equipped with provider-neutral evaluation fixtures but no required OpenAI API key;
- not a plugin, web UI, hosted service, package-registry release, or adapter for other model providers.

## Contributing

Focused issues and pull requests are welcome. Please explain the observed prompt failure or missing behavior, include a representative case, keep guidance minimal, and provide the verification evidence used to justify the change. Changes to model guidance should link to current primary documentation and must not silently overwrite explicit user values or existing evaluation baselines.

## License

Released under the [MIT License](LICENSE). Copyright (c) 2026 Xerneas216.
