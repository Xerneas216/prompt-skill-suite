---
name: defining-prompt-contracts
description: Use only in an active ProCraft workflow when a complete, incomplete, ambiguous, or conflicting brief must be normalized or checked as a prompt contract before candidate messages are drafted.
---

# Defining Prompt Contracts

## Core principle

Turn the brief into an explicit contract before writing prompt prose. Preserve user-provided values, expose material gaps, and never invent business rules, permissions, tool schemas, model parameters, or evidence.

Read [references/gpt-5p6-contract-guidance.md](references/gpt-5p6-contract-guidance.md) before producing the contract.

## Workflow

1. Extract the intended outcome, audience, supplied evidence, explicit values, constraints, authorized side effects, required output, and completion bar.
2. Classify each gap:
   - **Blocking:** it can change the goal, business decision, safety posture, permission boundary, tool/API contract, evidence standard, or required output.
   - **Non-blocking:** a reversible presentation or implementation choice with a safe default.
3. Ask one smallest blocking question when necessary. If questions are forbidden, return a blocked contract with the missing decision and a safe reduced scope; do not fill the gap.
4. Record non-blocking choices in `assumptions` with their impact.
5. Build the contract using positive, testable fields. Use absolute language only for true invariants.
6. Choose model settings from explicit requirements or measured baselines. Mark unverified recommendations as candidates for evaluation.

Classify `general` for non-tool text or decision work, `agent` when tools or side effects are part of the target, `software` only for software-development work, and `hybrid` only when multiple categories materially apply.

## Required output

Return:

- `contract_status`: `ready` or `blocked`;
- `scenario`: `general`, `agent`, `software`, or `hybrid`;
- `explicit_values` and `assumptions`;
- `blocking_gaps`;
- `model_profile`;
- `prompt_contract` with Role, Personality, Collaboration, Goal, Success criteria, Constraints, Evidence, Permissions, Output, and Stop rules.

Do not draft final System, Developer, or User messages while `contract_status` is `blocked`.

## Completion check

Confirm every required field is testable, every side effect is authorized, explicit values are unchanged, and no unsupported field or fabricated schema has been introduced.
