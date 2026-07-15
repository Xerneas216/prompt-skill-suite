# Prompt Skill Suite Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the approved seven-skill prompt package suite.

**Architecture:** PromptPackage v1 JSON is the single source of truth and produces derived Markdown. Each skill is developed with TDD; verified source is copied for installation only after integration checks pass.

**Tech Stack:** Skill Markdown, Python, JSON, JSON Schema, and `jsonschema>=4.23,<5`.

## Global constraints

- Implement exactly the seven skills named in the approved design.
- Keep PromptPackage v1 JSON authoritative and render Markdown from it.
- Use a separate TDD cycle for every skill.
- Verify source before copy-based installation.

## Implementation sequence

- [ ] **1. Contract:** Implement `defining-prompt-contracts` with focused tests.
- [ ] **2. General:** Implement `prompting-general-tasks` with focused tests against the contract.
- [ ] **3. Agent:** Implement `prompting-tool-agents` with focused tests against the contract.
- [ ] **4. Software:** Implement `prompting-software-engineering` with focused tests against the contract.
- [ ] **5. Review:** Implement `reviewing-prompt-packages` with focused tests.
- [ ] **6. Evaluation:** Implement `evaluating-prompt-packages` with focused tests and evaluation cases.
- [ ] **7. Controller:** Implement `building-prompt-packages` with focused tests across the preceding skills.
- [ ] **8. Integration and installation:** Verify the complete source suite, then copy the verified source to the installation destination and smoke-test the copy.
