# GPT-5.6 contract guidance

Sources, checked 2026-07-15:

- https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6
- https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.6

## Contract fields

Define the destination rather than prescribing every step:

| Field | Requirement |
|---|---|
| Role | The model's function and relevant context |
| Personality | Concrete tone choices, not labels such as “friendly” |
| Collaboration | When to ask, assume, act, explain tradeoffs, and verify |
| Goal | User-visible outcome |
| Success criteria | Conditions that must hold before the final answer |
| Constraints | Safety, policy, business, evidence, and side-effect limits |
| Evidence | What needs support, sufficient support, and missing-evidence behavior |
| Permissions | Read, local mutation, external write, destructive, costly, and scope-expanding boundaries |
| Output | Required content, format, length, and values to preserve |
| Stop rules | Retry, fallback, ask, abstain, and completion conditions |

Preserve explicit values. Use decision criteria for implicit values instead of universal defaults, keyword maps, or broad semantic shortcuts. Contradictory invariants are a blocking gap.

## Missing information

Ask only for the smallest fact that materially changes the contract. When the user forbids questions, narrow the capability safely and report the unresolved decision. Missing evidence does not prove a factual “no.” Missing tool schemas do not authorize invented input or return fields.

## Model profile

Use the Responses API for reasoning, tools, and multi-turn workflows.

1. Preserve an explicitly requested model and settings.
2. For a new quality-first GPT-5.6 workload with no contrary constraint, use `gpt-5.6` and `reasoning.effort: medium` as candidates, not measured conclusions.
3. For migrations, keep the existing reasoning effort as the baseline and compare one level lower.
4. Use `low` for latency-sensitive work only when evaluations preserve quality.
5. Use `high`, `xhigh`, `max`, or `reasoning.mode: pro` only when representative evaluations show a meaningful gain.
6. Choose `text.verbosity` from `low`, `medium`, or `high`; put task-specific content priorities in the prompt.
7. Use `reasoning.context: all_turns` only while goals, assumptions, and priorities remain stable; use `current_turn` when earlier reasoning is stale; otherwise prefer `auto` or omit it.

Do not emit speculative parameters with “if supported.” Verify the target API or omit the field and list it as an unresolved integration decision.

## Lean contract

State each rule once. Keep examples only when they encode a product requirement or repair a measured failure. Expose only relevant tools. Conflicting rules cause more instability than missing detail.
