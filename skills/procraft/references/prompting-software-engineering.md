# Prompting Software Engineering

## Stage instructions

### Core principle

Match agency to the requested verb, make the smallest evidence-backed change, and tie every completion claim to observable validation. A deadline may narrow verification but cannot turn an untested patch into a verified fix.

Apply this stage only after the contract is ready. If tools or external effects are involved, also apply the tool-Agent stage.

### Workflow

1. Classify the request as answer, explain, review, diagnose, change, build, fix, refactor, or plan.
2. For answer, explain, review, or diagnose, authorize relevant read-only inspection and safe diagnostic checks, but no product-code or external-state changes. Local temporary validation artifacts are allowed only when isolated, reversible, and cleaned up without touching user work.
3. For change, build, fix, or refactor, inspect repository conventions and user changes, reproduce or define the target behavior, then make only necessary edits.
4. Derive semantics from code, tests, specifications, and explicit user values. Surface missing product or business decisions instead of guessing.
5. Define validation proportional to risk: targeted regression first, then relevant tests, types, lint, build, runtime smoke checks, or broader suites when justified.
6. For frontend work, preserve the existing design system, component patterns, state and data flow, loading/error/empty states, accessibility, and responsive behavior. Render and inspect representative viewports.
7. For plans, cover requirements, resources, state, data flow, validation, failure behavior, privacy/security, rollout, and unresolved decisions only when applicable.
8. Report changed scope, evidence, commands and results, unresolved risks, and any unverified behavior.

### Required contribution

Return:

- agency and mutation boundaries;
- inspection and implementation sequence;
- task-specific success criteria;
- targeted and broader verification requirements;
- frontend visual checks when applicable;
- failure, rollback, and incomplete-validation language;
- representative evaluation cases.

Do not authorize speculative refactors, unrelated cleanup, redesign, invented requirements, destructive version-control operations, or claims unsupported by executed checks.

### Completion check

Verify that diagnosis did not become a fix, source changes trace to the request, user work is preserved, tests target the failure, visual work was rendered when possible, and incomplete validation is stated without "fixed," "passing," or equivalent certainty.

## Detailed reference

Select only the task pattern below that matches the contract.

## Agency by request type

### Answer, explain, review, diagnose

Inspect relevant files, history, logs, configuration, and existing tests. Safe, reversible diagnostic commands are permitted when relevant. Do not edit product code, configuration, dependencies, committed fixtures, databases, or external systems unless the user separately asks for a change.

Diagnostic tools may create isolated caches, temporary databases, compiled files, or coverage output when the environment makes that safe. Keep them outside user-authored paths when possible, record what was generated, and remove only artifacts created by the current work. Never delete or overwrite pre-existing user files. Treat production data, credentials, and real traffic as separate permission boundaries.

Call something a root cause only when the evidence links trigger, actual code path, failure mechanism, and observed symptom. Otherwise distinguish confirmed findings, likely hypotheses, alternative explanations, and the smallest missing evidence.

### Change, build, fix, refactor

Inspect before editing. Preserve existing style and architecture. Reproduce a bug or define observable target behavior before implementation. Make the smallest change that satisfies the contract and remove only unused elements created by that change. Do not clean up adjacent code merely because it could be improved.

Protect dirty worktrees and unrelated user changes. Never use destructive version-control commands unless explicitly authorized. New dependencies, migrations, generated assets, deployments, and external writes must be justified by the contract and relevant permission rules.

## Verification ladder

Use the smallest checks that can disprove the implementation, then widen according to risk:

1. regression test or deterministic reproduction for the target behavior;
2. nearest affected unit or integration tests;
3. type checking, linting, build, or static analysis relevant to changed files;
4. runtime or browser smoke test;
5. broader suite for cross-cutting or high-risk behavior.

Do not skip the targeted check merely because the deadline is tight. If a check cannot run, give the attempted command, blocker, and remaining uncertainty. Say “unverified patch” or “not validated”; do not say “fixed,” “working,” or “tests pass.”

## Frontend and visual work

- Inspect the existing design system, tokens, components, page hierarchy, states, and supported breakpoints before editing.
- Reuse established components and placement. A feature request is not redesign authorization.
- Trace one authoritative state through inputs, URL or persisted state, cache keys, requests, charts, tables, totals, pagination, and exports as applicable.
- Preserve loading, error, empty, disabled, focus, keyboard, screen-reader, and responsive states.
- Render the implementation and inspect interaction plus representative desktop and narrow viewports. Check overflow, clipping, wrapping, spacing, visual hierarchy, consistency, and unintended redesign.
- Screenshots verify appearance, not data correctness or accessibility; pair them with behavioral checks.

## Architecture and implementation plans

When the deliverable is a plan, define only applicable sections: goal and non-goals, current evidence, requirements, resources, components, state, data flow, interfaces, migration, validation, failure and recovery, observability, privacy/security, rollout, and open decisions. Keep unresolved product choices explicit. Do not disguise assumptions as architecture requirements.

## Review behavior

Prioritize actionable defects by impact and evidence. Reference precise locations. Separate confirmed issues from questions or optional improvements. A clean review means no findings were discovered in the inspected scope, not proof of correctness.
