# evaluating-prompt-packages baseline

## RED controls

Three reused-context controls were run before the skill existed. They are useful comparisons but are not fresh-context acceptance tests.

1. Shorter grounded-research candidate: correctly rejected promotion after citation omissions and an unsupported negative, but invented exact dimension weights and zero-tolerance gates without approved calibration.
2. No runtime available: correctly refused to accept an author's dynamic-pass claim, but returned the non-v1 status `unverified` instead of `not_run`.
3. Mixed general, agent, and software package: designed broad representative cases and quality-first gates, but proposed arbitrary numeric weights and the non-v1 status `measured_not_decided` for an unapproved decision boundary.

Observed failures to repair: evaluation design must not invent executable numeric policy, and verification status must remain exactly `not_run`, `pass`, or `fail`.

Five independent fresh-context controls: `not_run` because this session has no remaining fresh agent slots. No dynamic-quality claim is made.

## GREEN result

With this skill loaded, the repeated no-runtime case returned exactly `status: not_run`, explained that static review and the author's claim are not execution evidence, listed a provider-neutral fixture and traceability artifacts, and set `dynamic_quality_claim_allowed: false`. It introduced no substitute status or invented executable threshold. The RED failures were not repeated.
