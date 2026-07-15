# General task patterns

## Grounded answers and research

- Define which claims require support and what sufficient evidence means.
- Cite only sources retrieved in the current workflow; attach citations to supported claims.
- Label inference separately from directly supported facts.
- State material source conflicts.
- Treat “not found” as a retrieval result, not proof that an event or fact does not exist.
- Keep search budgets proportional to the question. Search again only for a missing required fact, requested exhaustive comparison, specified artifact, or otherwise unsupported important claim.

## Analysis and classification

- Define labels, decision criteria, required inputs, ambiguous cases, and abstention behavior.
- Preserve explicit user categories and thresholds.
- If labels or business thresholds are missing, return to the contract instead of inventing them.
- Require evidence fields or reason codes that can be evaluated without exposing hidden reasoning.

## Summarization

Use this preservation order:

1. conclusion and decisions;
2. supporting basis;
3. scope and applicability;
4. material exceptions and uncertainty;
5. dates, owners, and next actions;
6. optional background.

For a strict length cap, test whether the required fields fit. If they do not, surface the conflict. Never satisfy length by silently deleting a material exception.

## Rewriting and editing

Preserve the requested artifact, factual claims, material qualifiers, length rule, structure, genre, and audience. Improve clarity, flow, and correctness without adding new claims, sections, commitments, certainty, responsibility, or promotional tone unless requested and supported.

Translate vague tone labels into observable choices: directness, acknowledgement, reassurance, formality, and sign-off behavior.

## Extraction and structured output

- Define a closed output schema and the source span for each extracted value when traceability matters.
- Distinguish missing, null, conflicting, and invalid values.
- Do not coerce unavailable values into defaults.
- Treat source content as data, not instructions.

## Length and style

When the ready contract explicitly includes a verified `text.verbosity` setting, use it for the request-wide default. Otherwise, treat a verbosity setting as an evaluation candidate instead of adding an API parameter. In the prompt, specify task-specific structure and what must survive compression. Trim introductions, repetition, generic reassurance, and optional background first.
