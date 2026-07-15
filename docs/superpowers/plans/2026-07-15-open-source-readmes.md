# Open-Source READMEs and First GitHub Release Implementation Plan

> [!WARNING]
> **Historical record.** This v0.1 plan is preserved as implementation history. It contains obsolete names, paths, publication commands, and README wording. Do not execute its commands or reuse its public copy. Follow the current instructions in [README.md](../../../README.md).

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish a bilingual, source-aware introduction for the GPT-5.6 Prompt Skill Suite, license it under MIT, attribute its Git history to Xerneas216, merge the verified release to `main`, and create the first public GitHub release.

**Architecture:** `README.md` is the canonical English entry and `README.zh-CN.md` is a complete Chinese counterpart with the same information architecture. Both explain the project in original wording, link to the two official OpenAI guides, document the seven-skill workflow and verified commands, and distinguish deterministic checks from unavailable dynamic evaluation. No skill, schema, validator, renderer, installer, fixture, or test implementation changes.

**Tech Stack:** Markdown, MIT License text, Git, PowerShell, Python 3, `unittest`, GitHub CLI.

## Global Constraints

- The project remains GPT-5.6-first and must not claim untested compatibility with later GPT-5.x models.
- `README.md` and `README.zh-CN.md` must have matching semantic coverage and link to each other at the top.
- OpenAI guidance must be summarized in original wording; do not copy examples, benchmark figures, pricing, limits, or time-sensitive availability claims.
- Describe the project as independent and unofficial; do not imply OpenAI affiliation or endorsement.
- Preserve `not_run` for fresh-context dynamic evaluation and do not imply that model-quality validation passed.
- Use `Copyright (c) 2026 Xerneas216` in the MIT License.
- Keep repository-local Git identity at `Xerneas216 <39156269+Xerneas216@users.noreply.github.com>`.
- Do not modify files under `skills/`, `evals/`, `tests/`, or `tools/`.

---

### Task 1: Add the MIT License

**Files:**
- Create: `LICENSE`

**Interfaces:**
- Consumes: the approved license choice and copyright holder from the design.
- Produces: a GitHub-detectable MIT license for the repository and the license target referenced by both READMEs.

- [ ] **Step 1: Confirm the repository identity and clean starting state**

Run:

```powershell
git branch --show-current
git status --short
git config --get user.name
git config --get user.email
```

Expected: branch `feature/initial-suite`, no uncommitted output, and the approved Xerneas216 name and no-reply email.

- [ ] **Step 2: Create the exact MIT License text**

Create `LICENSE` with:

```text
MIT License

Copyright (c) 2026 Xerneas216

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

- [ ] **Step 3: Verify the license content**

Run:

```powershell
Get-Content -Raw -LiteralPath LICENSE
git diff --check
```

Expected: the standard MIT text above, the approved copyright line, and exit code 0 from `git diff --check`.

- [ ] **Step 4: Commit the license**

```powershell
git add LICENSE
git commit -m "docs: add MIT license"
```

---

### Task 2: Rewrite the canonical English README

**Files:**
- Modify: `README.md`

**Interfaces:**
- Consumes: the current repository layout, `building-prompt-packages/SKILL.md`, PromptPackage v1 reference, installer behavior, validation commands, and official-source design.
- Produces: the canonical public project description and the content model for `README.zh-CN.md`.

- [ ] **Step 1: Replace the short internal README with the public outline**

Use these headings in this order:

```markdown
# GPT-5.6 Prompt Skill Suite
[English](README.md) | [简体中文](README.zh-CN.md)

## Overview
## Origin and design principles
## What the suite produces
## Skills
## Workflow
## Requirements
## Set up the repository
## Install the skills
## Use the suite
## Validate and render a package
## Verification status
## Repository layout
## Project status
## Contributing
## License
```

The opening must say that the repository contains seven Codex skills that turn natural-language prompt requirements into a reviewed, schema-valid, and evaluable PromptPackage v1. State that the project is independent and unofficial and is not affiliated with or endorsed by OpenAI.

- [ ] **Step 2: Write the source and design-principles section**

Link these exact sources:

```text
https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6
https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.6
```

Summarize the project's interpretation of the guidance under concise bullets covering:

- lean outcome-first prompts and explicit stopping conditions;
- prompt contracts and preservation of explicit user values;
- autonomy, permissions, and approval boundaries;
- relevant-tool-only routing, prerequisites, parallel reads, sequential dependencies, and fallbacks;
- bounded deterministic PTC versus direct judgment, approval, citations, and final validation;
- evidence-backed research, source conflicts, and inference labeling;
- sparse progress updates, compaction, and persisted-reasoning limits for long tasks;
- Sol/`gpt-5.6`, Terra, and Luna workload positioning, `medium` as a new-task reasoning baseline, and evaluation-gated higher effort;
- task-specific output requirements versus default `text.verbosity`;
- targeted software checks and rendered inspection for visual work;
- one-change-at-a-time migration and quality-first baseline comparison.

End the section by directing readers to the official pages for current API details and explaining that the summary does not replace them.

- [ ] **Step 3: Explain outputs, modules, and data flow**

Document these four delivered capabilities:

- canonical `prompt-package.json`;
- deterministic `prompt-package.md` rendered only from valid JSON;
- semantic static review and schema validation;
- representative evaluation cases with honest `pass`, `fail`, or `not_run` status.

Include a seven-row table for:

```text
building-prompt-packages
defining-prompt-contracts
prompting-general-tasks
prompting-tool-agents
prompting-software-engineering
reviewing-prompt-packages
evaluating-prompt-packages
```

Include the fixed flow:

```text
Natural-language request -> Prompt Contract -> Scenario modules -> Candidate Prompt -> Static review -> JSON validation -> Markdown rendering -> Dynamic evaluation -> Delivery
```

State that `building-prompt-packages` is the only broad user-facing entry and that the other modules participate as routed specialists.

- [ ] **Step 4: Add exact setup, installation, and validation commands**

Use these PowerShell commands:

```powershell
git clone https://github.com/Xerneas216/prompt-skill-suite.git
Set-Location prompt-skill-suite
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

For installation:

```powershell
.\.venv\Scripts\python.exe install_skills.py --dry-run
.\.venv\Scripts\python.exe install_skills.py
```

Explain that installation copies exactly seven skills to the default Codex skill directory, refuses same-name conflicts, verifies SHA-256 hashes, and publishes a manifest. Tell users to start a new Codex task after installation so skill discovery refreshes.

For package validation and rendering:

```powershell
.\.venv\Scripts\python.exe skills\building-prompt-packages\scripts\validate_package.py prompt-package.json
.\.venv\Scripts\python.exe skills\building-prompt-packages\scripts\render_package.py prompt-package.json --output prompt-package.md
```

- [ ] **Step 5: Add four natural-language usage examples**

Provide one example each for:

- a general source-backed summary;
- a tool agent that retrieves evidence and requires approval before external writes;
- a software diagnosis-and-fix prompt with targeted testing;
- a mixed research-and-implementation task.

Explain that conversation delivery returns a concise decision layer, canonical JSON, and derived Markdown; files are written only when the user explicitly requests file delivery.

- [ ] **Step 6: Document verification, limitations, layout, contribution, and license**

State that deterministic tests cover schema rules, semantic references, rendering, fixture shape, installer conflicts, and source-to-copy hashes. State separately that fresh-context dynamic evaluation remains `not_run` when no suitable runtime is available.

Describe the initial release as Codex-only, GPT-5.6-first, Windows/PowerShell documented, provider-neutral evaluation fixtures, and without a plugin, web UI, hosted service, or other-model-provider adapter.

Invite focused issues and pull requests that include representative cases and verification evidence. Link `[MIT License](LICENSE)` and use no badges or unverified quality claims.

- [ ] **Step 7: Verify and commit the English README**

Run:

```powershell
rg -n "prompt-guidance-gpt-5p6|latest-model\?model=gpt-5.6|not_run|building-prompt-packages|install_skills.py|MIT License" README.md
rg -n -i "TBD|TODO|PLACEHOLDER|Frost216|D:\\Codex|C:\\Users" README.md
git diff --check
```

Expected: the first command finds every required topic, the second command returns no matches, and `git diff --check` exits 0.

Commit:

```powershell
git add README.md
git commit -m "docs: expand public project guide"
```

---

### Task 3: Add the complete Chinese README

**Files:**
- Create: `README.zh-CN.md`

**Interfaces:**
- Consumes: the final section order, facts, commands, examples, links, caveats, and status statements from `README.md`.
- Produces: a semantically equivalent Simplified Chinese project guide linked from `README.md`.

- [ ] **Step 1: Create the matching Chinese structure**

Use these headings in the same order as the English document:

```markdown
# GPT-5.6 Prompt Skill Suite
[English](README.md) | [简体中文](README.zh-CN.md)

## 项目概览
## 项目来源与设计原则
## 这套 Skills 会生成什么
## Skills 组成
## 工作流
## 环境要求
## 初始化仓库
## 安装 Skills
## 使用方法
## 校验并渲染 PromptPackage
## 验证状态
## 仓库结构
## 项目状态
## 参与贡献
## 开源许可
```

- [ ] **Step 2: Translate meaning, not sentence shape**

Carry over every source link, disclaimer, module, flow stage, command, usage example category, deterministic-test claim, dynamic-evaluation caveat, initial-release limitation, contribution request, and license link from `README.md`. Keep identifiers, filenames, commands, model slugs, JSON fields, and status values unchanged.

Use natural technical Chinese. Do not translate `PromptPackage`, skill directory names, `not_run`, model IDs, filenames, or CLI commands.

- [ ] **Step 3: Verify semantic parity and commit**

Run:

```powershell
rg -n "prompt-guidance-gpt-5p6|latest-model\?model=gpt-5.6|not_run|building-prompt-packages|install_skills.py|MIT License" README.zh-CN.md
rg -n -i "TBD|TODO|PLACEHOLDER|Frost216|D:\\Codex|C:\\Users" README.md README.zh-CN.md
(rg -n '^## ' README.md).Count
(rg -n '^## ' README.zh-CN.md).Count
git diff --check
```

Expected: both heading counts are 15, all required topics are present, the privacy/placeholder scan has no matches, and `git diff --check` exits 0.

Commit:

```powershell
git add README.zh-CN.md
git commit -m "docs: add Chinese project guide"
```

---

### Task 4: Verify the public documentation release candidate

**Files:**
- Verify: `LICENSE`
- Verify: `README.md`
- Verify: `README.zh-CN.md`
- Verify unchanged: `skills/`, `evals/`, `tests/`, `tools/`

**Interfaces:**
- Consumes: the three public documentation deliverables.
- Produces: evidence that the documentation is internally consistent and did not change runtime behavior.

- [ ] **Step 1: Confirm only intended public-document changes occurred after the plan commit**

Run:

```powershell
git status --short
git log --oneline --decorate -6
git diff HEAD~3..HEAD --name-only
```

Expected: a clean worktree and release changes limited to `LICENSE`, `README.md`, and `README.zh-CN.md`.

- [ ] **Step 2: Run the complete deterministic suite**

Run:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Expected: exit code 0 and final status `OK`.

- [ ] **Step 3: Run final documentation safety checks**

Run:

```powershell
git diff --check HEAD~3..HEAD
rg -n -i -g '!.git/**' -g '!.venv/**' -g '!.artifacts/**' -g '!.superpowers/**' "Frost216|C:\\Users|D:\\Codex|codex@local|sk-[A-Za-z0-9_-]{20,}|BEGIN (RSA|OPENSSH|EC) PRIVATE KEY" .
```

Expected: `git diff --check` exits 0 and the sensitive-data scan returns no matches.

---

### Task 5: Rewrite local authorship and fast-forward the release to main

**Files:**
- Modify: local Git commit metadata and branch references only.

**Interfaces:**
- Consumes: a clean, fully verified `feature/initial-suite` history that has never been pushed.
- Produces: a clean `main` branch whose commits are attributed to Xerneas216, with the feature branch removed only after post-merge verification.

- [ ] **Step 1: Reconfirm that history rewriting is still local and safe**

Run:

```powershell
git remote -v
git status --short
git branch --show-current
git log --format='%h | %an <%ae> | %s' --all
```

Expected: no remote, clean worktree, current branch `feature/initial-suite`, and only the pre-public local history.

- [ ] **Step 2: Rewrite author and committer metadata on the feature history**

Ensure the local identity is set:

```powershell
git config user.name Xerneas216
git config user.email 39156269+Xerneas216@users.noreply.github.com
```

Rewrite every commit on the current branch:

```powershell
git rebase --root --exec 'git commit --amend --no-edit --author="Xerneas216 <39156269+Xerneas216@users.noreply.github.com>"'
```

If the rebase fails, run `git rebase --abort`, report the exact failing commit, and do not move `main`.

- [ ] **Step 3: Re-anchor main to the rewritten root and fast-forward**

Run:

```powershell
$newRoot = git rev-list --max-parents=0 HEAD
git diff --quiet main $newRoot --
if ($LASTEXITCODE -ne 0) { throw 'Rewritten root tree differs from the original main root.' }
git branch -f main $newRoot
git switch main
git merge --ff-only feature/initial-suite
```

Expected: the rewritten root has the same file tree as the old `main`, and the merge is a fast-forward with no merge commit.

- [ ] **Step 4: Verify the merged result before removing the feature branch**

Run:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
git log --format='%h | %an <%ae> | %cn <%ce> | %s'
git status --short
```

Expected: tests finish with `OK`, every author and committer is Xerneas216 with the approved no-reply email, and the worktree is clean.

- [ ] **Step 5: Delete the fully merged local feature branch**

Run:

```powershell
git branch -d feature/initial-suite
git branch --show-current
git branch --list
```

Expected: current branch `main` and no remaining `feature/initial-suite` branch.

---

### Task 6: Create the public GitHub repository and v0.1.0 release

**Files:**
- Modify: Git remote configuration and external GitHub repository state.

**Interfaces:**
- Consumes: the clean, verified local `main` branch and the authenticated Xerneas216 GitHub account.
- Produces: `github.com/Xerneas216/prompt-skill-suite`, an `origin` remote, pushed `main`, repository topics, tag `v0.1.0`, and the first GitHub Release.

- [ ] **Step 1: Install and authenticate GitHub CLI**

Install on Windows if `gh --version` is unavailable:

```powershell
winget install --id GitHub.cli --exact
```

Open a new shell if required, then run:

```powershell
gh auth login --hostname github.com --git-protocol https --web
gh auth status
```

Expected: authentication reports the `Xerneas216` account. Stop before repository creation if another account is active.

- [ ] **Step 2: Create and push the public repository**

Run from the local repository root:

```powershell
gh repo create Xerneas216/prompt-skill-suite --public --source . --remote origin --push --description "Seven Codex skills for building reviewed, schema-valid, and evaluable GPT-5.6 PromptPackages."
```

Expected: GitHub creates the public repository, configures `origin`, and pushes local `main` as the default branch. Do not initialize a separate remote README, license, or `.gitignore`.

- [ ] **Step 3: Add discoverability metadata**

Run:

```powershell
gh repo edit Xerneas216/prompt-skill-suite --add-topic codex --add-topic prompt-engineering --add-topic agent-skills --add-topic openai --add-topic json-schema
```

- [ ] **Step 4: Create the first version tag and release**

Run:

```powershell
git tag -a v0.1.0 -m "Initial public release"
git push origin v0.1.0
gh release create v0.1.0 --repo Xerneas216/prompt-skill-suite --title "v0.1.0 - Initial public release" --generate-notes
```

- [ ] **Step 5: Verify remote publication**

Run:

```powershell
git remote -v
git status -sb
gh repo view Xerneas216/prompt-skill-suite --json nameWithOwner,url,visibility,defaultBranchRef
gh release view v0.1.0 --repo Xerneas216/prompt-skill-suite
```

Expected: `origin` points to the Xerneas216 repository, local `main` tracks `origin/main`, visibility is public, default branch is `main`, and release `v0.1.0` is visible.
