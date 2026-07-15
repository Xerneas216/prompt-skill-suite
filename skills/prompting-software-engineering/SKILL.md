---
name: prompting-software-engineering
description: Use only in an active ProCraft workflow when a ready contract needs software prompt rules for explanation, diagnosis, implementation, bug fixing, refactoring, code review, testing, architecture, frontend changes, or visual verification.
---

# Prompting Software Engineering

## Core principle

Match agency to the requested verb, make the smallest evidence-backed change, and tie every completion claim to observable validation. A deadline may narrow verification but cannot turn an untested patch into a verified fix.

**REQUIRED SUB-SKILL:** Use `defining-prompt-contracts` first. Continue only with a ready contract.

Read [references/software-task-patterns.md](references/software-task-patterns.md), selecting only the relevant task pattern. If tools or external effects are involved, also use `prompting-tool-agents`.

## Workflow

1. Classify the request as answer, explain, review, diagnose, change, build, fix, refactor, or plan.
2. For answer, explain, review, or diagnose, authorize relevant read-only inspection and safe diagnostic checks, but no product-code or external-state changes. Local temporary validation artifacts are allowed only when isolated, reversible, and cleaned up without touching user work.
3. For change, build, fix, or refactor, inspect repository conventions and user changes, reproduce or define the target behavior, then make only necessary edits.
4. Derive semantics from code, tests, specifications, and explicit user values. Surface missing product or business decisions instead of guessing.
5. Define validation proportional to risk: targeted regression first, then relevant tests, types, lint, build, runtime smoke checks, or broader suites when justified.
6. For frontend work, preserve the existing design system, component patterns, state and data flow, loading/error/empty states, accessibility, and responsive behavior. Render and inspect representative viewports.
7. For plans, cover requirements, resources, state, data flow, validation, failure behavior, privacy/security, rollout, and unresolved decisions only when applicable.
8. Report changed scope, evidence, commands and results, unresolved risks, and any unverified behavior.

## Required contribution

Return:

- agency and mutation boundaries;
- inspection and implementation sequence;
- task-specific success criteria;
- targeted and broader verification requirements;
- frontend visual checks when applicable;
- failure, rollback, and incomplete-validation language;
- representative evaluation cases.

Do not authorize speculative refactors, unrelated cleanup, redesign, invented requirements, destructive version-control operations, or claims unsupported by executed checks.

## Completion check

Verify that diagnosis did not become a fix, source changes trace to the request, user work is preserved, tests target the failure, visual work was rendered when possible, and incomplete validation is stated without "fixed," "passing," or equivalent certainty.
