---
name: building-prompt-packages
description: Use when a user asks to create, improve, package, review, or evaluate a high-quality prompt for a general, tool-agent, software-engineering, or mixed task.
---

# Building Prompt Packages

## Core principle

This is the suite's user-facing entry. Convert a natural-language request into one canonical PromptPackage v1 JSON object, then derive every human-readable artifact from that validated source. Do not maintain JSON and Markdown independently.

Read [references/prompt-package-v1.md](references/prompt-package-v1.md).

## Workflow

1. Use `defining-prompt-contracts`. Preserve explicit values and ask at most one smallest blocking question. If the contract is blocked, return the conflict and question; do not fabricate a ready package.
2. Route the ready contract:
   - general -> `prompting-general-tasks`;
   - agent or any tool use -> `prompting-tool-agents`;
   - software -> `prompting-software-engineering`;
   - hybrid -> every applicable specialist, without duplicating rules.
3. Select model settings in this order: explicit user values; `gpt-5.6` for new quality-first work; `gpt-5.6-terra` as a cost-balanced candidate; `gpt-5.6-luna` as a high-throughput candidate. Use `medium` reasoning effort as a new-task baseline. For migration, preserve the current setting and evaluate one level lower. Use `high`, `xhigh`, `max`, or Pro only when evaluations show benefit. Let `text.verbosity` set request-wide detail; prompt for task-specific structure and preservation.
4. Assemble only the schema fields that apply. Include `tool_policy` exactly when tools are used. Add PTC only for a bounded deterministic reduction. Omit persistent reasoning context for single-turn work and omit empty optional sections.
5. Use `reviewing-prompt-packages`. Apply at most two minimal repair rounds while protecting explicit values; stop on unresolved static defects.
6. Write or hold canonical JSON first. Run `scripts/validate_package.py`. A failed package is not deliverable.
7. Run `scripts/render_package.py` only on valid JSON. Never hand-edit the derived Markdown.
8. Use `evaluating-prompt-packages` for provider-neutral cases and baseline comparison. If execution is unavailable, record `not_run`; never claim dynamic validation.

## Delivery

Default to conversation delivery with two layers:

1. concise routing, settings, verification status, and residual-risk summary;
2. canonical `prompt-package.json` content plus deterministically rendered `prompt-package.md` content.

Write files only when the user requests file delivery. For file delivery, validate JSON before rendering Markdown and report both paths.

## Completion check

Verify the contract is ready, applicable specialists participated, explicit settings survived, conditional fields are correct, static review passed, JSON validates, Markdown came from that JSON, evaluation status matches actual execution, and no file was written without request.
