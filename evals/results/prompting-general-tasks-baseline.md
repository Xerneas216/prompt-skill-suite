# prompting-general-tasks baseline

Date: 2026-07-15
Target skill absent: yes

Three reused-context samples were run because the platform would not permit additional fresh threads.

## Results

1. Incident-announcement rewrite: preserved facts, qualifiers, structure, genre, and an explicit priority order. No critical failure observed.
2. 120-character regulatory summary: required six fields while also declaring the length limit absolute. It did not surface the possibility that all required content might not fit, creating a silent omission or impossible-contract risk.
3. Company-incident research: correctly treated no search result as non-proof and avoided inventing tool schemas. It proposed a concrete retrieval budget as a candidate despite no workload evidence.

## Failures addressed

- Brevity rules can conflict with required facts and caveats.
- Candidate retrieval budgets can appear more authoritative than their evidence supports.
- Positive preservation priorities need to remain explicit across task types.

Five-fresh-context acceptance status: `not_run` because the thread limit was already exhausted. No five-sample quality claim may be made.

## GREEN

With `defining-prompt-contracts` and this skill loaded, the impossible 120-character summary returned `contract_status: blocked`, declined to draft a final prompt, identified the length-versus-completeness conflict, and proposed measuring the minimum faithful length. No required field was silently removed.
