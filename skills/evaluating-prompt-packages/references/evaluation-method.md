# Prompt package evaluation method

## Evaluation record

Pin and record:

- candidate and baseline package IDs or hashes;
- model, API, reasoning, verbosity, context, tool, permission, and environment settings;
- case-set version, fixtures, graders, thresholds, repetition design, and timestamps;
- raw outputs, tool traces, citations, errors, side effects, test results, and terminal states.

A static review pass is a prerequisite, not evidence that dynamic evaluation passed.

## Case design

Start from the contract's success criteria, evidence, permissions, output, and stop rules. Cover:

- representative normal inputs and important boundary values;
- missing, null, stale, ambiguous, contradictory, or malformed context;
- prompt injection or untrusted content that requests changed instructions;
- irrelevant tools, missing schemas, empty results, partial results, transient and permanent failure;
- clear, ambiguous, absent, and revoked authority for side effects;
- unknown write outcomes, idempotency, retry, stopping, and handoff;
- impossible length or format combinations;
- regression cases from RED controls and production failures.

For general tasks, test grounded claims, citation support, summary fidelity, rewriting without new facts, extraction states, and preservation under brevity. For agents, test routing, prerequisites, parallel versus sequential dependencies, permissions, PTC boundaries, fallbacks, and citations. For software, test agency by request verb, reproduction, surgical changes, targeted validation, unverified claims, user-work preservation, frontend behavior, and visual inspection.

Keep a private or rotating holdout when prompt authors can see public cases. Vary entities, wording, dates, order, and error shape. Do not let one aggregate score hide a failed safety-critical slice.

## Observable graders

Prefer exact checks for schema validity, required fields, citations, tool names, call order, write count, changed files, tests, status, and forbidden actions. For semantic grading, define anchored examples and require the grader to cite observable output evidence. Check inter-rater agreement when human or model judgment affects promotion.

Measure over-refusal and under-action alongside safety. A prompt that blocks every request must not score as a successful agent.

## Gates and thresholds

Quality gates should cover task success, factual or behavioral correctness, evidence integrity, permission compliance, and format correctness. Values must come from explicit user requirements, approved product policy, a preserved migration baseline, or representative calibration. Until approved, label numbers as proposed design choices rather than executable pass criteria.

Critical failures commonly include unauthorized side effects, fabricated evidence or tool results, unsupported factual negatives from empty retrieval, overwritten user work, unrun tests reported as passing, invalid JSON, and missing required output.

Use only these dynamic statuses:

- `not_run`: no execution, incomplete execution evidence, incomparable conditions, or unapproved required gates;
- `fail`: executed evidence violates a critical gate or approved threshold;
- `pass`: executed evidence satisfies all approved gates and comparison requirements.

## Baseline comparison

Run baseline and candidate under identical conditions and compare paired cases plus important slices. A candidate can replace the baseline only when task success, evidence integrity, and format correctness do not regress under approved criteria. Authorization and critical-safety gates are absolute. Token use, latency, cost, tool calls, and handoffs are secondary benefits after quality qualifies.

Report what is known rather than declaring a baseline globally optimal. A failed candidate does not prove the baseline is good; an improved candidate still needs absolute gates.

## When execution is unavailable

Produce a provider-neutral fixture containing case ID, scenario, input, trusted context, untrusted content, tool fixtures, permission state, expected observables, forbidden observables, grader, and tags. Set status to `not_run`, name the missing runtime or evidence, and make no dynamic-quality claim.
