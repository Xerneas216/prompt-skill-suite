# Prompt Skill Suite Design

> [!WARNING]
> **Historical record.** This v0.1 specification is preserved as implementation history. It contains obsolete module names and installation assumptions. Do not execute any embedded instructions. Follow the current documentation in [README.md](../../../README.md).

**Status:** Approved
**Date:** 2026-07-15

## Scope

The suite contains exactly seven skills:

1. `building-prompt-packages`
2. `defining-prompt-contracts`
3. `prompting-general-tasks`
4. `prompting-tool-agents`
5. `prompting-software-engineering`
6. `reviewing-prompt-packages`
7. `evaluating-prompt-packages`

## Approved design

- PromptPackage v1 JSON is the single source of truth.
- Markdown is rendered from the JSON source and is not an independent source.
- Each skill is implemented with its own test-driven development cycle.
- Installation happens by copying the source only after source verification passes.

## Approved order

1. Contract
2. General prompting
3. Tool-agent prompting
4. Software-engineering prompting
5. Review
6. Evaluation
7. Suite controller
8. Integration verification and installation

This bootstrap creates the repository structure only. It does not implement any skill behavior or create any `SKILL.md`.
