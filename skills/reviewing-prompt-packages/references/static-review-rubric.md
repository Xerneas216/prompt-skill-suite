# Static review rubric

## Severity and disposition

- **Critical:** unauthorized or destructive action, fabricated evidence or evaluation, invalid canonical package, or a contradiction that can cause severe outcome. Disposition: fail or block.
- **Important:** missing required behavior, impossible contract, dangling tool, unsupported certainty, absent stop rule, or non-executable output. Disposition: fail or block.
- **Minor:** local duplication, avoidable verbosity, unclear wording, or small maintainability issue that does not invalidate delivery.

Use `blocked` when a protected user value conflicts with another required outcome and the reviewer lacks authority to choose. Use `fail` when a known package defect has a safe deterministic repair or when automatic repair rounds are exhausted. Use `pass` only after canonical validation and semantic review find no release blocker; it is not a dynamic-quality claim.

## Completeness checks

Confirm the applicable contract defines:

- a concrete goal and audience;
- observable success criteria and evidence;
- constraints and protected explicit values;
- read, write, external-effect, approval, and escalation permissions;
- output type, schema, length, language, and required content;
- failure, abstention, stop, handoff, and unresolved-state behavior;
- model and API settings as explicit values or evaluation candidates;
- tools, routing, citations, empty-result handling, retries, and PTC boundaries when applicable;
- static review, dynamic evaluation, baseline comparison, residual risk, and provenance.

Omit inapplicable conditional sections rather than accepting empty placeholders.

## Consistency checks

Compare all layers and flag:

- incompatible length, structure, preservation, citation, or language rules;
- `always`, `never`, `all`, `exactly`, `optimal`, or `prove` obligations that conflict or exceed observable evidence;
- “do not assume” paired with implicit or plausible defaults;
- “never ask” paired with “ask when missing”; 
- autonomous action paired with missing authorization;
- response-format schema that cannot represent required states;
- model values that override explicit user settings;
- verification status inconsistent with recorded runs.

Instruction priority resolves which instruction wins at runtime; it does not remove the semantic defect from the package.

## Economy and relevance

Flag exact duplicates and semantic restatements only when consolidation preserves behavior. Do not remove repetition that intentionally appears at a separate enforcement boundary. Remove irrelevant tools, examples, sections, and generic reminders. Keep one authoritative rule per responsibility and reference it rather than paraphrasing it across layers.

## Tool integrity

Every tool named in routing, prerequisites, PTC, fallback, citations, status recovery, or evaluation must resolve to the declared inventory. Verify that the tool contract supports the assumed inputs, outputs, errors, limits, side effects, and citations. A name alone is insufficient. Unknown write outcomes require status or idempotency handling; otherwise stop and hand off.

## Verifiability

Replace vague goals such as “best,” “safe,” or “high quality” with task-specific observables. Universal claims over future inputs are not testable. An evaluation marked `pass` needs run evidence, a named candidate and baseline, cases, metrics, results, and scope. Otherwise use `not_run` or `fail` as appropriate.

## Minimal repair protocol

1. Freeze explicit user values and unaffected valid sections.
2. Link one proposed edit to each confirmed finding.
3. Consolidate duplicates without changing meaning.
4. Resolve deterministic defects such as dangling names or false status.
5. For competing protected requirements, return the exact conflict and smallest decision needed.
6. Re-run schema validation and this rubric.
7. Stop after two automatic repair rounds and report remaining defects.
