---
name: procraft
description: Use when the deliverable is explicitly a model or Agent instruction—a Prompt/提示词, 系统指令, system/developer/user message, Agent rule, tool policy, Structured Output contract, or reusable AI workflow specification—and the user asks to create, modify, debug, migrate, review, evaluate, or package it; do not use for ordinary writing, research, programming, code diagnosis, summarization, email, or content generation unless the user asks for the Prompt or instructions that will perform that work.
---

# ProCraft

## Core principle

This is the suite's user-facing gateway. Match only when the deliverable is instructions for a model or Agent, then produce the smallest artifact that satisfies the request. Preserve explicit user values and never claim evaluation that did not run.

Read [references/prompt-package-v1.md](references/prompt-package-v1.md) before producing a PromptPackage.

## Mode selection

Apply this priority:

1. Honor the user's explicit mode choice.
2. Otherwise select Full mode when any Full-mode escalation condition applies.
3. Otherwise select Fast mode. If the request is ambiguous or unclear, default to Fast mode and offer an upgrade to Full mode.

## Fast mode

Use for a simple, single-turn Prompt with no tools, side effects, production reuse, package requirement, or baseline evaluation.

Return only:

- a directly usable Prompt;
- necessary variables and their meanings;
- material assumptions that affect use.

Do not generate an empty PromptPackage, static-review ceremony, or evaluation placeholder. Do not write files unless the user explicitly requests file delivery.

## Full mode

Use when the user requests a PromptPackage or production reuse; separate system, developer, and user layers; Structured Outputs; a tool policy or approval boundary; a long-running Agent; repository work; Prompt review or evaluation; or model/Prompt migration.

1. Build the canonical PromptPackage JSON through `defining-prompt-contracts`, accepting either a complete brief to normalize or an incomplete brief to resolve. Preserve explicit values and ask at most one smallest blocking question.
2. Perform specialist routing: general tasks use `prompting-general-tasks`; Agent or tool tasks use `prompting-tool-agents`; software tasks use `prompting-software-engineering`; mixed tasks use every applicable specialist without duplicate rules.
3. Assemble only applicable schema fields. Use `procraft` in `provenance.participating_modules`; include `tool_policy` only for tool use, PTC only for bounded deterministic reduction, and persistent reasoning context only for multi-turn work.
4. Run `reviewing-prompt-packages` for static review, allowing at most two minimal repair rounds while protecting explicit values.
5. Validate the canonical JSON with `scripts/validate_package.py`. Invalid JSON is not deliverable.
6. Render Markdown from valid JSON with `scripts/render_package.py`; never maintain or hand-edit a parallel Markdown source.
7. Run `evaluating-prompt-packages` for provider-neutral evaluation and baseline comparison. Record `not_run` when execution evidence is unavailable.
8. Deliver both canonical JSON and deterministically rendered Markdown in conversation. Write files only when the user explicitly requests file delivery.

## Completion check

For Fast mode, verify the Prompt is directly usable and every variable and material assumption is visible. For Full mode, verify the contract, specialist participation, conditional fields, static review, validation, rendering, evaluation status, and dual delivery against actual evidence.
