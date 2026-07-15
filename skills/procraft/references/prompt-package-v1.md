# PromptPackage v1 orchestration reference

## Canonical flow

`request -> prompt contract -> scenario modules -> candidate JSON -> semantic review -> JSON validation -> Markdown rendering -> dynamic evaluation -> delivery`

JSON is authoritative. `prompt-package.md` is a deterministic projection created by `scripts/render_package.py` after `scripts/validate_package.py` succeeds. A blocked contract, failed static review, or invalid JSON stops delivery.

## Required top-level fields

The schema in [prompt-package.schema.json](prompt-package.schema.json) is normative. Its required top-level fields are:

- `version`;
- `request`: original goal, scenario, audience, language, explicit values, tool use, interaction mode, and delivery;
- `assumptions`: explicit non-direction-changing assumptions;
- `model_profile`: model, Responses API, verbosity, reasoning effort, and applicable mode or context;
- `prompt_contract`: role, personality, collaboration, goal, success criteria, constraints, evidence, permissions, output, and stop rules;
- `messages`: System, Developer, User template, and variables;
- `response_format`: text structure or JSON Schema;
- `verification`: static review, dynamic evaluation, baseline comparison, repair count, and residual risks;
- `provenance`: official sources, generation time, schema version, and participating modules.

`tool_policy` is required when `request.uses_tools` is true and prohibited otherwise. PTC and long-task configuration are optional nested sections and must be omitted when inapplicable. A single-turn package must not request `all_turns` reasoning context.

`request.explicit_values` maps JSON Pointer paths to the exact user-provided values, for example `"/model_profile/model": "gpt-5.6"` or `"/request/delivery": "conversation"`. It may be empty when the user supplied no explicit setting. Every pointer must resolve and equal its canonical target, so the same mechanism protects model, language, length, delivery, permissions, and other explicit values without a hard-coded field list.

Each tool entry carries its actual input and output JSON Schema, human-readable returns and errors, runtime limits, citation capability, and side-effect class. Write or destructive tools also declare idempotency and status-recovery capability. A stable `contract_ref` may identify the runtime contract, but it does not replace the executable schemas in the package.

## Module routing

Always include the controller, contract, reviewer, and evaluator in provenance. Add:

- `prompting-general-tasks` for general work;
- `prompting-tool-agents` for agent work or any tool use;
- `prompting-software-engineering` for software work;
- at least two applicable specialists for a hybrid package.

Each responsibility belongs to one authoritative layer. The controller composes contributions; it does not paste every specialist rule into every message.

## Model profile decisions

Explicit values win. For an unspecified new quality-first task, use `gpt-5.6` and `medium` reasoning effort as evaluation baselines, not universal optima. Suggest `gpt-5.6-terra` for cost balance and `gpt-5.6-luna` for high throughput only as candidates. Preserve migration settings and compare one level lower. Adopt high-effort or Pro settings only after representative evaluation demonstrates a quality benefit.

Use `text_verbosity` for request-wide detail. Keep task-specific length, structure, required content, and compression priority in the contract and messages. Verify parameters against the target API; omit unsupported or speculative settings.

## Validation semantics

Beyond JSON Schema, the validator checks normalized duplicates, identical message layers, explicit-value overrides, scenario-module coverage, single-turn reasoning context, embedded JSON Schema validity, unique tools and route steps, dangling tool and dependency references, dependency cycles, PTC tool references, and approval presence for write-capable tools.

Dynamic and baseline statuses are exactly `not_run`, `pass`, or `fail`. A `pass` or `fail` requires evidence. Static review status is `pass` or `fail`; a failure requires findings. Automatic repair rounds cannot exceed two.

## Delivery behavior

For conversation delivery, present a compact decision layer followed by the canonical JSON and its rendered Markdown. For requested file delivery, write JSON first, validate it, render Markdown, and return both paths. Do not create files merely because file artifacts are supported.

## Official sources

- https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6
- https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.6
