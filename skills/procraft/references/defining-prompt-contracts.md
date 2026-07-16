# Defining Prompt Contracts

## Stage instructions

### Core principle

Turn the brief into an explicit contract before writing prompt prose. Preserve user-provided values, expose material gaps, and never invent business rules, permissions, tool schemas, model parameters, or evidence.

### Workflow

1. Extract the intended outcome, audience, supplied evidence, explicit values, constraints, authorized side effects, required output, and completion bar.
2. Classify each gap:
   - **Blocking:** it can change the goal, business decision, safety posture, permission boundary, tool/API contract, evidence standard, or required output.
   - **Non-blocking:** a reversible presentation or implementation choice with a safe default.
3. Ask one smallest blocking question when necessary. If questions are forbidden, return a blocked contract with the missing decision and a safe reduced scope; do not fill the gap.
4. Record non-blocking choices in `assumptions` with their impact.
5. Build the contract using positive, testable fields. Use absolute language only for true invariants.
6. Choose model settings from explicit requirements or measured baselines. Mark unverified recommendations as candidates for evaluation.

Classify `general` for non-tool text or decision work, `agent` when tools or side effects are part of the target, `software` only for software-development work, and `hybrid` only when multiple categories materially apply.

### Required output

Return:

- `contract_status`: `ready` or `blocked`;
- `scenario`: `general`, `agent`, `software`, or `hybrid`;
- `explicit_values` and `assumptions`;
- `blocking_gaps`;
- `model_profile`;
- `prompt_contract` with Role, Personality, Collaboration, Goal, Success criteria, Constraints, Evidence, Permissions, Output, and Stop rules.

Do not draft final System, Developer, or User messages while `contract_status` is `blocked`.

### Completion check

Confirm every required field is testable, every side effect is authorized, explicit values are unchanged, and no unsupported field or fabricated schema has been introduced.

## Detailed reference

Use the guidance below when applying this stage.

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
