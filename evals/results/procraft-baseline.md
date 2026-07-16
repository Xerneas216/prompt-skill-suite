# ProCraft baseline

## Deterministic status

The deterministic suite covers Fast and Full mode contracts, conservative trigger metadata, PromptPackage Schema v1.0, explicit-value protection, message and tool references, dependency cycles, PTC rules, deterministic Markdown rendering, provider-neutral evaluation fixtures, clean installation, publication races, and rollback.

## v0.2.0 RED evidence

The refreshed Codex registry exposed `procraft` as the public entry and no retired entry. Eleven independent v0.2.0 runs produced:

- Implicit positive requests: `0/5`. The responses preserved the refund approval boundary, but did not provide observable ProCraft Full-mode execution or the canonical JSON plus rendered Markdown delivery.
- Near-boundary ordinary writing: `5/5`. Each run wrote the requested email directly without invoking ProCraft.
- Explicit `$procraft` smoke test: `1/1`. The request was recognized and returned a Fast-mode instruction.

The v0.2.0 RED dynamic trigger status is `fail`. Explicit invocation and the conservative negative boundary work; implicit positive routing still needs improvement.

## v0.3.0 GREEN run

Status: `pass`

On 2026-07-16, the machine-readable cases in `evals/fixtures/trigger-cases.json` ran in independent fork-free contexts after the single-Skill candidate was installed. The model/runtime identity, per-case routing telemetry, observed Skill set, decision, and response summary are recorded in `evals/results/procraft-v0.3.0-trigger-run.json`.

All release gates passed in the same run:

- Implicit positives: `5/5` triggered ProCraft and produced the requested Prompt artifact.
- Direct-task negatives: `5/5` did not trigger ProCraft and performed or correctly began the underlying task directly.
- Explicit `$procraft`: `1/1` triggered ProCraft and returned a Fast-mode Prompt.

The deterministic suite and this dynamic run remain separate evidence. The v0.2.0 RED result above is retained as migration history.
