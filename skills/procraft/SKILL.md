---
name: procraft
description: Use when the requested deliverable is an AI or model Prompt, prompt text, or 提示词, including an LLM, Agent, image, video, or audio Prompt, or a system/developer/user message, tool policy, Structured Output contract, or reusable AI workflow specification; do not use for direct execution of writing, research, coding, summarization, email, image generation, or any other underlying task unless the user asks for the Prompt or instructions that will perform it.
---

# ProCraft

## Core principle

This is ProCraft's only user-facing Skill. Match only when the deliverable is instructions for a model or Agent, then produce the smallest artifact that satisfies the request. Preserve explicit user values and never claim evaluation that did not run.

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

1. Read [the contract stage](references/defining-prompt-contracts.md), then build the canonical PromptPackage JSON from either a complete brief to normalize or an incomplete brief to resolve. Preserve explicit values and ask at most one smallest blocking question.
2. Perform specialist routing by reading the applicable merged references directly: general tasks use [the general-task stage](references/prompting-general-tasks.md); Agent or tool tasks use [the tool-Agent stage](references/prompting-tool-agents.md); software tasks use [the software-engineering stage](references/prompting-software-engineering.md); mixed tasks use every applicable stage without duplicate rules.
3. Assemble only applicable schema fields. Use `procraft` in `provenance.participating_modules`; include `tool_policy` only for tool use, PTC only for bounded deterministic reduction, and persistent reasoning context only for multi-turn work.
4. Read and apply [the static review stage](references/reviewing-prompt-packages.md), allowing at most two minimal repair rounds while protecting explicit values.
5. Validate the canonical JSON with `scripts/validate_package.py`. Invalid JSON is not deliverable.
6. Render Markdown from valid JSON with `scripts/render_package.py`; never maintain or hand-edit a parallel Markdown source.
7. Read and apply [the evaluation stage](references/evaluating-prompt-packages.md) for provider-neutral evaluation and baseline comparison. Record `not_run` when execution evidence is unavailable.
8. Deliver both canonical JSON and deterministically rendered Markdown in conversation. Write files only when the user explicitly requests file delivery.

## Completion check

For Fast mode, verify the Prompt is directly usable and every variable and material assumption is visible. For Full mode, verify the contract, specialist participation, conditional fields, static review, validation, rendering, evaluation status, and dual delivery against actual evidence.
