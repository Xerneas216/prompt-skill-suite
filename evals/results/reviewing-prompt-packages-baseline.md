# reviewing-prompt-packages baseline

## RED controls

Three reused-context controls were run before the skill existed. They are useful comparisons but are not fresh-context acceptance tests.

1. Contradictory 80-character prompt: found table/list and ask/no-ask conflicts, but repaired by silently deleting the evidence table, five-source requirement, caveat preservation, and raw-quote requirement. It did not return a blocked disposition or protect all explicit values.
2. Tool-agent package: correctly found undeclared CRM/email tools, unauthorized external write, dangling citation, missing stop rules, irrelevant tools, and an unverifiable success standard.
3. Universal safety/accuracy proof with zero tests: correctly failed the package, changed fabricated dynamic `pass` to `not_run`, surfaced contradictory defaults, and replaced universal claims with bounded metrics.

Observed failure to repair: a reviewer can recognize impossible requirements yet produce a superficially clean prompt by silently deleting protected requirements.

Five independent fresh-context controls: `not_run` because this session has no remaining fresh agent slots. No dynamic-quality claim is made.

## GREEN result

With this skill loaded, the repeated contradictory 80-character case returned `review_status: blocked`, identified the table/list, length/content, and ask/no-ask conflicts separately, protected every explicit value, and requested only the two decisions needed to resolve them. It made no automatic rewrite and proposed removing only one exact duplicate after the conflicts are resolved. The RED silent-deletion failure was not repeated.
