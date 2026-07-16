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

Status: `not_run`

Run the machine-readable cases in `evals/fixtures/trigger-cases.json` from independent fresh contexts after installing the release artifact. Record the model/runtime identity, clean registry evidence, raw outputs, and per-case trigger decision.

GREEN requires all of these criteria in the same fresh-context run:

- Implicit positives: `5/5` trigger ProCraft and exhibit observable ProCraft behavior.
- Direct-task negatives: `5/5` do not trigger ProCraft and perform the requested underlying task directly.
- Explicit `$procraft`: `1/1` triggers ProCraft.

Do not mark the v0.3.0 run GREEN until those runs and artifacts exist. Deterministic tests and the preserved v0.2.0 result are not substitutes for fresh execution evidence.
