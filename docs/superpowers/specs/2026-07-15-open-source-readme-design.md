# Open-Source README Design

## Goal

Prepare the GPT-5.6 Prompt Skill Suite for a public GitHub release with clear, source-aware documentation for both international and Chinese-speaking users.

## Deliverables

- `README.md`: the canonical English project introduction shown by default on GitHub.
- `README.zh-CN.md`: a complete Chinese counterpart with the same structure and meaning.
- `LICENSE`: the standard MIT License with `Copyright (c) 2026 Xerneas216`.

Both README files link to each other at the top. They describe the repository as an independent, unofficial project and do not imply endorsement by OpenAI.

## README Structure

The two README files use the same section order:

1. Project summary and language switch.
2. Origin and design sources, linking to the official GPT-5.6 prompt guidance and model guide and summarizing the guidance applied by this project.
3. What the suite produces: canonical PromptPackage JSON, deterministic Markdown, static review, and evaluation records.
4. The seven skills and their responsibilities.
5. The fixed package-building data flow.
6. Requirements and local setup.
7. Installation, dry-run, and conflict behavior.
8. Usage examples for general, tool-agent, software-engineering, and mixed requests.
9. Package validation and deterministic rendering commands.
10. Verification scope and the meaning of `not_run` for unavailable dynamic evaluation.
11. Repository layout, contributing guidance, project status, and license.

## Source Coverage

Both README files identify these official OpenAI pages as the project's primary design sources:

- GPT-5.6 prompt guidance: https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6
- GPT-5.6 model guidance: https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.6

The source section explains, in original wording, how the suite turns the guidance into reusable skills. It includes a compact summary of these themes:

- **Lean, outcome-first prompts:** define the desired result, important constraints, available evidence, success criteria, and stopping conditions; remove repetition, contradictory rules, redundant examples, and unrelated tools.
- **Prompt contracts:** separate role, personality, collaboration style, goal, success criteria, constraints, permissions, evidence requirements, output shape, and stop rules so each instruction has a clear purpose.
- **Autonomy and approval boundaries:** distinguish safe local work from external writes, destructive operations, costly actions, and scope expansion that require confirmation.
- **Tool routing:** expose only relevant tools, retrieve prerequisites before acting, parallelize independent reads, keep dependent work sequential, and define fallbacks for empty or partial results.
- **Programmatic Tool Calling:** use PTC only for bounded deterministic reduction such as filtering, joining, ranking, deduplication, aggregation, batching, or repeated validation; keep approval, semantic judgment, citations, and final validation in direct model control.
- **Evidence and research:** cite retrieved sources near supported claims, separate inference from sourced facts, surface conflicts, and report missing evidence instead of guessing.
- **Long-running work:** provide a short preamble and sparse outcome-based progress updates, preserve useful state across turns, compact at meaningful milestones, and avoid stale persisted reasoning.
- **Model and output controls:** treat `gpt-5.6`/Sol as the quality-first default, Terra as a cost-balanced option, and Luna as a high-volume option; use `medium` reasoning as a balanced new-task baseline and adopt higher settings only when representative evaluations justify them; use `text.verbosity` for default detail and prompts for task-specific content requirements.
- **Software and visual verification:** distinguish diagnosis from implementation, run targeted validation after changes, disclose unavailable checks, preserve existing design systems, and render visual work before finalizing.
- **Evaluation-driven migration:** change one prompt, tool, or reasoning variable at a time, compare on representative tasks, and count lower tokens, latency, cost, or calls as improvements only after quality remains acceptable.

The README summary is educational context, not a replacement for the official pages. It avoids copying their examples, benchmark figures, pricing, limits, or time-sensitive availability claims. Readers are directed to the official model guide for current API details.

## Content Rules

- Explain concepts in original wording; do not reproduce the OpenAI guides.
- Link each source title directly and label the extracted themes as this project's interpretation of the guidance.
- Preserve the project's GPT-5.6-first scope while noting that later GPT-5.x behavior must be re-evaluated before adoption.
- Distinguish deterministic validation from model-quality evaluation.
- Do not claim that fresh-context dynamic evaluation passed when its recorded status is `not_run`.
- Use copy-pasteable PowerShell commands that match the current repository.
- Keep the English and Chinese documents semantically aligned without forcing line-for-line translation.
- Avoid badges, promotional claims, installation methods, or compatibility promises that are not currently verified.

## Non-Goals

- No package registry publication, hosted service, plugin, web UI, or non-OpenAI provider support.
- No changes to the seven skills, PromptPackage schema, validators, renderer, installer, or tests.
- No generated screenshots or architecture artwork for the initial release.

## Verification

- Check every referenced path and command against the repository.
- Scan both README files for stale local paths, private identifiers, placeholders, and unsupported claims.
- Run the complete deterministic test suite after documentation and license changes.
- Review the English and Chinese headings for matching coverage.
- Confirm Git status is clean after the release-preparation commit.
