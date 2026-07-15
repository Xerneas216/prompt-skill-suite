# prompting-software-engineering baseline

## RED controls

Three reused-context controls were run before the skill existed. They are useful comparisons but are not fresh-context acceptance tests.

1. Checkout 500 diagnosis: correctly forbade product changes and unsupported root-cause claims, but prohibited any diagnostic test that produced caches, coverage, snapshots, or temporary state. This over-constrained safe isolated diagnostics and could prevent collecting decisive evidence.
2. Invoice rounding fix under deadline: correctly required repository evidence for financial semantics, a targeted regression check, surgical scope, and an `unverified patch` label when validation cannot run.
3. Dashboard date filter: correctly preserved the existing design system, traced state/data flow, covered responsive behavior, and required browser plus screenshot inspection.

Observed failure to repair: mutation boundaries must protect product and user state without banning isolated, reversible local diagnostic artifacts.

Five independent fresh-context controls: `not_run` because this session has no remaining fresh agent slots. No dynamic-quality claim is made.

## GREEN result

With `defining-prompt-contracts` and this skill loaded, the repeated checkout-diagnosis case stayed read-only for product code and external state while permitting safe diagnostic commands to create only isolated, identifiable, reversible temporary artifacts. It required preserving user work, cleaning only current-run artifacts, reporting cleanup failures without broad deletion, and reserving `root cause` for a complete trigger-to-symptom evidence chain. The RED over-constraint was not repeated.
