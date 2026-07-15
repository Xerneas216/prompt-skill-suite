---
name: evaluating-prompt-packages
description: Use when an in-progress PromptPackage needs representative cases, an executable provider-neutral fixture, repeated runtime tests, baseline comparison, promotion criteria, or an honest not-run result.
---

# Evaluating Prompt Packages

## Core principle

Evaluate observable behavior, not how polished the prompt sounds. A candidate may replace a baseline only when task success, evidence integrity, and format correctness are non-inferior; efficiency matters only after those quality gates hold.

Read [references/evaluation-method.md](references/evaluation-method.md). Require a passing static review before executing dynamic evaluation.

## Workflow

1. Identify the exact candidate, baseline, model profile, tool contracts, permissions, package hashes, and intended input scope.
2. Derive assertions from the ready contract. Do not invent rubric weights, thresholds, non-inferiority margins, or run counts; mark unapproved values as evaluation-design candidates.
3. Build representative cases for normal success, missing or ambiguous data, conflicts, adversarial instructions, tool failures, permission edges, stopping, and prior observed failures.
4. Use the same model settings, fixtures, inputs, and grading rules for baseline and candidate. Randomize order and blind subjective review when feasible.
5. Prefer deterministic evidence: schema validation, tool traces, citations, tests, changed files, side-effect logs, and terminal states. Use rubric graders only for behavior that cannot be checked directly.
6. Repeat nondeterministic cases according to an approved or measured design; preserve raw outputs and report variance and worst slices.
7. Assign only `not_run`, `pass`, or `fail`. Use `not_run` when execution or required evidence is unavailable. Use `fail` when an executed candidate violates a gate or approved threshold. Use `pass` only when execution evidence satisfies every approved gate.
8. Compare paired results by task and slice. Reject any candidate with a critical permission, evidence, format, or unsupported-claim regression even if it is faster or cheaper.
9. Record residual risks and scope. Do not generalize beyond the evaluated model, package version, fixtures, cases, and settings.

## Required contribution

Return:

- provider-neutral cases, inputs, fixtures, expected observables, and graders;
- baseline and candidate identities;
- approved gates plus unresolved design choices;
- per-case and aggregate results when run;
- `status`: `not_run`, `pass`, or `fail`, with evidence;
- promotion decision, quality comparison, secondary efficiency metrics, and residual risk.

If no runtime is available, generate executable fixtures and return `not_run`; never infer dynamic success from static quality, author claims, or prompt inspection.

## Completion check

Verify that cases cover every contract risk, graders cannot reward over-refusal, baseline and candidate conditions match, raw evidence is traceable, efficiency never compensates for quality loss, and status matches what actually ran.
