---
name: prompting-general-tasks
description: Use only in an active ProCraft workflow when a ready contract needs general-task prompt rules for question answering, research, analysis, writing, rewriting, summarization, extraction, or classification.
---

# Prompting General Tasks

## Core principle

Shape the output with a positive contract: say what the answer must contain and preserve before saying what may be trimmed. Do not trade factual integrity or material caveats for style, brevity, or persuasion.

**REQUIRED SUB-SKILL:** Use `defining-prompt-contracts` first. Continue only with a ready contract.

Read [references/general-task-patterns.md](references/general-task-patterns.md), selecting only the pattern that matches the contract. If the workflow uses retrieval or tools, also use `prompting-tool-agents` for routing and evidence acquisition.

## Workflow

1. Select the task pattern: grounded answer, research synthesis, analysis, drafting, rewriting, summarization, extraction, or classification.
2. Convert the contract into concise System, Developer, and User responsibilities. State each rule once.
3. Define preservation priority before optimization. For transformations, preserve the requested artifact, facts, genre, structure, and material qualifiers before improving clarity or tone.
4. Define evidence behavior: supported facts, inference labels, conflicts, and missing-evidence language.
5. Set response length by naming required content and lower-value detail to omit. If the length limit cannot contain all required fields, return to the contract as blocked rather than silently dropping content.
6. Add examples only when they encode a product requirement or repair a measured failure.
7. Produce task-specific evaluation cases, including missing data and adversarial inputs.

## Required contribution

Return:

- `general_task_pattern`;
- concise prompt rules for the selected pattern;
- a User Prompt template with trusted context separated from untrusted content;
- response-format requirements;
- preservation and grounding checks;
- representative evaluation cases.

Do not add tools, permissions, business thresholds, facts, or API parameters that are absent from the ready contract.

## Completion check

Verify that persuasion did not add claims, brevity did not remove required facts or caveats, missing evidence was not converted into a factual negative, and every evaluation assertion is observable.
