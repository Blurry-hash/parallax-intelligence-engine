---
name: paired-regression-gates
description: Use separate development/holdout scenarios and hard regression gates before promoting an experimental improvement.
---

# Paired Regression Gates

## Operational procedure

1. Specify paired, objective case scores on a common 0–1 scale; freeze at least one genuinely held-out case before candidate tuning.
2. Run `tools/quality_gate.py cases.json`, which requires no critical regressions, no holdout regressions and a user-defined mean gain.
3. Treat fixtures as fixtures: `provenance=fixture` can never claim observed performance. Validate real trial collection externally; do not cherry-pick or repeatedly tune to holdout.
4. Measure latency, cost, confidence intervals, error classes and human utility independently when relevant. This gate alone does not establish significance or authorize rollout.

**Check:** Construct cases where the mean improves but a critical or holdout case regresses. They must not pass.

## Source access

https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.permutation_test.html (paired permutation tests) and https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html (confidence intervals).

## Fallback and limits

No model-weight updates, background execution, paid inference or external API calls occur merely by loading this skill.
