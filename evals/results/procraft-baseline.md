# ProCraft baseline

## Deterministic status

The deterministic suite covers Fast and Full mode contracts, conservative trigger metadata, PromptPackage Schema v1.0, explicit-value protection, message and tool references, dependency cycles, PTC rules, deterministic Markdown rendering, provider-neutral evaluation fixtures, clean installation, publication races, and rollback.

## Fresh-context trigger status

The refreshed Codex registry exposed `procraft` as the public entry and no retired entry. Eleven independent runs produced:

- Implicit positive requests: `0/5`. The responses preserved the refund approval boundary, but did not provide observable ProCraft Full-mode execution or the canonical JSON plus rendered Markdown delivery.
- Near-boundary ordinary writing: `5/5`. Each run wrote the requested email directly without invoking ProCraft.
- Explicit `$procraft` smoke test: `1/1`. The request was recognized and returned a Fast-mode instruction.

The dynamic trigger status is `fail`. Explicit invocation and the conservative negative boundary work; implicit positive routing still needs improvement.
