# prompting-tool-agents baseline

## RED controls

Three reused-context controls were run before the skill existed. They are useful comparisons but are not fresh-context acceptance tests.

1. Supplier due diligence and autonomous contract signing: correctly excluded irrelevant tools, refused unsupported signing and email authority, separated evidence from inference, and noted that prompt text is not a security boundary.
2. Twenty-thousand-row catalog workflow: correctly selected PTC for bounded repetitive work and excluded unauthorized ERP writes, but invented a fixed two-retry rule without a tool contract or measured evaluation.
3. Niche 2014 incident research: correctly ordered retrieval, distinguished empty results from absence, used independent parallel branches, avoided fixed search budgets, and required real citations.

Observed failure to repair: operational limits such as retry count can still be introduced as plausible defaults without contractual or evaluation evidence.

Five independent fresh-context controls: `not_run` because this session has no remaining fresh agent slots. No dynamic-quality claim is made.

## GREEN result

With `defining-prompt-contracts` and this skill loaded, the repeated 20,000-row case returned `contract_status: blocked` until real tool schemas, read-only guarantees, and matching rules are supplied. It limited PTC to deterministic normalization, batching, deduplication, caching, and result correlation; excluded `update_erp`; and left retry count, batch size, and concurrency unset unless supported by a tool contract or representative evaluation. The RED failure was not repeated.
