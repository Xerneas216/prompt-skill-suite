---
name: reviewing-prompt-packages
description: Use when a PromptPackage or prompt draft needs semantic static review for duplication, contradiction, overconstraint, missing requirements, invalid tool references, unsupported claims, or minimal repair before evaluation or delivery.
---

# Reviewing Prompt Packages

## Core principle

Reject false coherence. A shorter prompt is not better when it silently removes an explicit value, material requirement, permission boundary, evidence rule, or stop condition. Repair only what the evidence shows is defective.

Read [references/static-review-rubric.md](references/static-review-rubric.md) and inspect the canonical JSON when a package has both JSON and Markdown.

## Workflow

1. Establish review scope, package version, explicit user values, ready or blocked contract status, participating modules, and available validation evidence.
2. Check completeness: goal, observable success criteria, evidence, permissions, output, failure behavior, stop rules, model settings, and applicable tool policy.
3. Check consistency across system, developer, user template, response format, tool policy, verification, and provenance. Higher-priority instructions do not make a contradiction harmless.
4. Check economy: exact and semantic duplicates, repeated cautions, examples that add no tested behavior, and irrelevant tools or sections.
5. Check executability: impossible combinations, undefined superlatives, universal proof obligations, missing schemas, dangling tool references, fabricated parameters, and unverifiable acceptance criteria.
6. Check safety and epistemics: unsupported certainty, hidden assumptions, absent approvals, empty-result misuse, fake citations, unrun evaluations marked pass, and unknown writes treated as success.
7. Rank findings by release impact and cite exact package locations. Separate confirmed defects from questions and optional improvements.
8. Propose the smallest repair that preserves explicit values and unaffected behavior. If requirements cannot coexist, return `blocked` with the conflict and smallest user decision; do not delete one silently.
9. Re-review after repair. Permit at most two automatic repair rounds; if defects remain, fail delivery with exact unresolved findings.

## Required output

Return:

- `review_status`: `pass`, `fail`, or `blocked`;
- severity-ranked findings with location, evidence, impact, and minimal repair;
- protected explicit values;
- repair round and remaining defects;
- residual risks and unrun checks.

Do not rewrite the whole package, add speculative best practices, change model settings without evidence, or convert an unrun evaluation into a quality claim.

## Completion check

Verify that every failure is actionable, every repair traces to a finding, no explicit value disappeared, tool names resolve, contradictions were not hidden by priority, and `pass` means no release-blocking static defect was found in the reviewed scope.
