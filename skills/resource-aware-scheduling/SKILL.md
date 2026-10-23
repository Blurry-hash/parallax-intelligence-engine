---
name: resource-aware-scheduling
description: Convert a validated task DAG into resource-limited estimated start/end times without inventing runtime.
---

# Resource Aware Scheduling

## Operational procedure

1. Use `tools/plan_engine.py` for contract validation, then `tools/resource_scheduler.py <plan>` for a deterministic list schedule. Worker slots are exclusive; dependency edges must be complete before dependent starts.
2. Treat user supplied estimated durations as estimates. Compare resource-aware estimated makespan to the task budget, and do not claim global optimality (a constraint solver is required for that).
3. Approval-gated tasks and all downstream dependencies stay blocked until real authorization exists. `--approve` represents a supplied claim, not independently verified permission.
4. For large projects benchmark alternative priority heuristics against representative DAGs and preserve independent counterexamples.

**Check:** Reject worker overlaps, unknown approvals, broken dependencies, and makespan lower than the dependency critical path. Cross-check `check_schedule()` separately.

## Source access

Official reference design: https://developers.google.com/optimization/scheduling/job_shop (resource scheduling), https://developers.openai.com/api/docs/guides/agents/guardrails-approvals (gated agent actions), https://github.com/openai/openai-agents-python (optional authorized multi-model runtime). These are documentation links, not installed providers or execution capabilities.

## Fallback and limits

No model-weight updates, background execution, paid inference or external API calls occur merely by loading this skill.

## v11.0 — Three targeted extensions

1. **Task-specific contract:** For **resource-aware-scheduling**, freeze the task objective, known input constraints and actual available tools; avoid loading this skill when it adds no user value.
2. **Adversarial failure probe:** Test the strongest failure case for this skill, including incompatible requirements, unavailable tools and unverified claims; record what was not executed.
3. **Lean evidence and fallback:** Prefer a small decisive verification or truthful alternative over unnecessary tool use. Image/video rendering is optional and never required for a nonimage request.
