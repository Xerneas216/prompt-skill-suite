# defining-prompt-contracts baseline

Date: 2026-07-15
Target skill absent: yes

## Samples

1. Refund workflow with missing schemas and thresholds: the response handled evidence and approvals well, but invented extensive logical tool inputs and returns. It also proposed `temperature: 0.1` and `top_p: 1` with an “omit if unsupported” caveat instead of verifying or omitting them.
2. Research prompt with contradictory rules: the response resolved “must answer” as allowing an evidence-insufficient terminal response. It still proposed `temperature: 0` conditionally without verifying API support.
3. GPT-5.4 migration with explicit `reasoning.effort=high`: the response correctly preserved `high`, separated model and prompt changes, and refused to claim production readiness without historical evaluation.
4. Risk-threshold scenario: not run because the platform rejected creation of another fresh agent with `agent thread limit reached`.
5. Diagnose-versus-fix authorization scenario: not run for the same platform limit.

## Observed failures addressed

- Inventing tool schemas when the integration contract is missing.
- Suggesting unverified model/API parameters conditionally.
- Treating a detailed candidate as production-ready despite missing decisions.

Dynamic five-sample acceptance status: `not_run` because only three fresh contexts were available. No five-sample quality claim may be made.

## GREEN and REFACTOR

The skill correctly returned `contract_status: blocked`, refused to invent thresholds or permissions, omitted speculative parameters, and reduced the forbidden-question request to a safe read-only audit contract. It initially mislabeled the order-risk task as `software`; the skill was refactored with explicit scenario classification criteria. Further fresh-context verification remains `not_run` because the thread limit persisted.
