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

Official reference design: https://developers.google.com/optimization/scheduling/job_shop (resource scheduling), https://developers.openai.com/api/docs/guides/agents/guardrails-approvals (gated agent actions), https://github.com/openai/openai-agents-python (optional authorized multi-model runtime). These are documentation links, not installed providers or execution capabilities.

## Fallback and limits

No model-weight updates, background execution, paid inference or external API calls occur merely by loading this skill.

## v11.0 — Three targeted extensions

1. **Task-specific contract:** For **paired-regression-gates**, freeze the task objective, known input constraints and actual available tools; avoid loading this skill when it adds no user value.
2. **Adversarial failure probe:** Test the strongest failure case for this skill, including incompatible requirements, unavailable tools and unverified claims; record what was not executed.
3. **Lean evidence and fallback:** Prefer a small decisive verification or truthful alternative over unnecessary tool use. Image/video rendering is optional and never required for a nonimage request.
