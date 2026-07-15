# ProCraft 🛠️

[English](README.md) | [简体中文](README.zh-CN.md)

ProCraft turns a rough idea for an AI prompt into instructions you can paste into a model or agent and use. Small requests stay small. Production workflows get the contracts, tool rules, validation, and evaluation records they need.

It is built for Codex and tuned around GPT-5.6. The current project release is `v0.2.0`; the packaged artifact format remains PromptPackage Schema v1.0.

## Where it came from

ProCraft grew out of two OpenAI guides:

- [Prompting guidance for GPT-5.6](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6)
- [GPT-5.6 model guidance](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.6)

The practical idea is simple: make intent, evidence, permissions, and completion criteria visible without scripting every reasoning step.

ProCraft carries these rules into its workflow:

- Describe the result, success criteria, evidence, constraints, and stop rules. Keep every value the user explicitly chose.
- Cut repeated instructions, conflicting rules, irrelevant examples, and tools that the task does not need.
- Give the model room to complete safe work inside scope. Require approval for destructive actions, outside writes, purchases, or a real expansion of scope.
- Retrieve prerequisites before acting. Run unrelated reads in parallel, keep dependent calls in order, and say what happens when a tool returns nothing useful.
- Reserve Programmatic Tool Calling for bounded reduction work such as filtering, joining, ranking, deduplication, aggregation, batching, or repeated validation. Approval handling and semantic judgment stay in the model's direct tool-calling path. Approval itself must come from the user or another authorized party.
- Put citations beside the claims they support. Mark inference as inference, surface source conflicts, and do not fill evidence gaps with guesses.
- Treat reasoning effort and `text.verbosity` as controls to evaluate, not decorations to turn up by default. New work starts at `medium`; higher settings need evidence that they help.
- Verify the artifact the user will actually receive. A software prompt should demand targeted tests, honest disclosure of checks that could not run, and rendered inspection for visual work.
- Change one prompt, tool, or model control at a time during migration. Lower cost or latency matters only after quality still meets the baseline.

ProCraft uses `gpt-5.6` as its quality-first default when the user has not chosen a model. `gpt-5.6-terra` is a cost-balanced candidate and `gpt-5.6-luna` is a throughput candidate. Those are starting points for evaluation, not automatic upgrades.

The linked guides remain the source for current API behavior, limits, pricing, and availability.

## When ProCraft should wake up 🎯

The trigger follows the requested deliverable. ProCraft can start automatically when the user wants a prompt, system instruction, developer or user message, agent rule, tool policy, Structured Output contract, or another reusable instruction for a model.

Ordinary writing, email, research, summarization, coding, and code diagnosis do not trigger ProCraft. Ask for the prompt or model instructions that will perform that work, and it does.

| Request | ProCraft? |
|---|---|
| "Write an email to move Friday's meeting." | No. The deliverable is the email. |
| "Research the current API options." | No. The deliverable is research. |
| "Fix the parser regression." | No. The deliverable is a code change. |
| "Write a prompt that writes an email from a few meeting details." | Yes. The deliverable is a prompt. |
| "Design the system, developer, and user messages for this agent." | Yes. The deliverable is model instructions. |
| "Review this tool policy for approval gaps." | Yes. The deliverable itself is part of a prompt system. |

For an explicit call, start the request with `$procraft`. Codex does not currently use a custom `@ProCraft` Skill syntax.

## Fast or Full

ProCraft picks the smallest useful route unless you choose a mode yourself.

| Mode | Use it when | You get |
|---|---|---|
| Fast mode | The prompt is single-turn, has no tools or side effects, and does not need a baseline evaluation. | A ready-to-use prompt, its required variables, and material assumptions. |
| Full mode | The prompt is for production reuse, layered messages, Structured Outputs, tools or approvals, a long-running agent, repository work, review, evaluation, or model migration. | A validated PromptPackage, rendered Markdown, static review, and an evidence-backed evaluation status. |

If the request is unclear, ProCraft returns a useful Fast mode result and offers the Full mode path. It does not inflate a small prompt into an empty package.

## How the pieces fit

The project has one public gateway and six internal specialists. Most users only need `procraft`; the other modules join when that workflow reaches their stage.

| Module | Job inside the workflow |
|---|---|
| `procraft` | Chooses Fast or Full mode, routes the work, checks completion, and delivers the result. |
| `defining-prompt-contracts` | Turns the request into goals, success checks, evidence, permissions, output rules, and stop conditions. |
| `prompting-general-tasks` | Handles research, analysis, writing, rewriting, summary, and extraction prompt patterns. |
| `prompting-tool-agents` | Defines tool routing, retrieval, citations, approvals, PTC boundaries, state, and fallbacks. |
| `prompting-software-engineering` | Covers diagnosis, code changes, tests, review, frontend work, and visual checks. |
| `reviewing-prompt-packages` | Finds contradictions, duplication, missing rules, irrelevant tools, and unverifiable requirements. |
| `evaluating-prompt-packages` | Builds representative cases, records execution evidence, and compares a candidate with its baseline. |

Full mode follows one fixed path:

```text
Request
  -> Prompt contract
  -> Applicable specialists
  -> Candidate PromptPackage JSON
  -> Static review
  -> JSON validation
  -> Deterministic Markdown rendering
  -> Dynamic evaluation or not_run
  -> Delivery
```

`prompt-package.json` is canonical. `prompt-package.md` is rendered from valid JSON in a fixed order, so the two files do not drift apart. Optional fields appear only when the task needs them. A tool-free task, for example, has no empty `tool_policy` block.

## Install it 🚀

The documented commands use Windows PowerShell, Python 3, and Git.

```powershell
git clone https://github.com/Xerneas216/ProCraft.git
Set-Location ProCraft
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Preview the installation:

```powershell
.\.venv\Scripts\python.exe install_skills.py --dry-run
```

Then install into `%USERPROFILE%\.codex\skills`:

```powershell
.\.venv\Scripts\python.exe install_skills.py
```

A clean install refuses same-name conflicts. If it finds an untouched v0.1.0 installation, the installer can report `legacy_migration` and replace it safely. Migration proceeds only when the old manifest, every expected file, and every SHA-256 hash match the committed v0.1.0 trust anchors exactly. Missing, edited, extra, or concurrently changed content stops the migration before publication. Staging and rollback protect the old copy if publication fails.

The installed state is recorded in `.procraft-manifest.json`. Start a new Codex task after installation so local Skill discovery refreshes.

## Use it

Fast mode can be as short as:

> `$procraft` Create a reusable prompt that turns rough meeting notes into a concise follow-up email. Keep commitments and dates unchanged.

Full mode can carry tool and approval policy:

> `$procraft` Build a production PromptPackage for an agent that retrieves account and policy evidence, explains empty-result fallbacks, and asks for approval before any outside write.

You can also ask for software behavior:

> Create model instructions for diagnosing and fixing a Python regression. Diagnosis must stay read-only. An authorized fix must run targeted tests and disclose checks that could not run.

Fast mode replies with the prompt, variables, and assumptions. Full mode replies with canonical JSON plus Markdown rendered from that JSON. ProCraft writes `prompt-package.json` and `prompt-package.md` to disk only when the user asks for files.

## Validate and render a package

Validate the canonical JSON:

```powershell
.\.venv\Scripts\python.exe skills\procraft\scripts\validate_package.py prompt-package.json
```

Render Markdown after validation succeeds:

```powershell
.\.venv\Scripts\python.exe skills\procraft\scripts\render_package.py prompt-package.json --output prompt-package.md
```

The validator checks the Schema and semantic links: preserved explicit values, scenario coverage, message layers, tool references, dependency cycles, PTC references, approvals, embedded schemas, and evaluation evidence.

## Verification status 🧪

The deterministic suite covers PromptPackage validation, deterministic rendering, provider-neutral evaluation fixtures, trigger contracts, and installer safety including trusted migration and rollback.

Fresh-context dynamic evaluation is a separate gate. Until it is actually executed with evidence, its status remains `not_run`. Passing unit tests does not convert that status into a model-quality claim.

## Repository map

```text
ProCraft/
├── skills/                 # Public gateway and internal specialists
├── evals/                  # Representative cases and evidence records
├── tests/                  # Deterministic unittest suite
├── tools/                  # Verified installer and migration anchors
├── docs/superpowers/       # Historical design and implementation records
├── install_skills.py       # Installation entry point
├── requirements.txt        # Runtime dependency
└── requirements-dev.txt    # Development dependencies
```

The PromptPackage Schema is at `skills/procraft/references/prompt-package.schema.json`. The validator and renderer sit under `skills/procraft/scripts/`.

## Contributing

A useful change starts with an observed failure or missing behavior. Add a representative case, keep the new guidance as small as possible, and include the check that proves the change helps. Model guidance changes should cite current primary documentation and must preserve explicit user choices and evaluation baselines.

## License

[MIT License](LICENSE), Copyright (c) 2026 Xerneas216.
