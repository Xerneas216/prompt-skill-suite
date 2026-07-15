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
2. Origin and design sources, linking to the official GPT-5.6 prompt guidance and model guide.
3. What the suite produces: canonical PromptPackage JSON, deterministic Markdown, static review, and evaluation records.
4. The seven skills and their responsibilities.
5. The fixed package-building data flow.
6. Requirements and local setup.
7. Installation, dry-run, and conflict behavior.
8. Usage examples for general, tool-agent, software-engineering, and mixed requests.
9. Package validation and deterministic rendering commands.
10. Verification scope and the meaning of `not_run` for unavailable dynamic evaluation.
11. Repository layout, contributing guidance, project status, and license.

## Content Rules

- Explain concepts in original wording; do not reproduce the OpenAI guides.
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
