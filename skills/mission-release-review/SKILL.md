---
name: mission-release-review
description: Compose plan, independent software auditors, artifact digests, task traces and evaluation into a fail-closed release recommendation.
---

# Mission Release Review

## Operational procedure

1. Run `tools/mission_review.py examples/planning-v10.3.json` as a default blocked case: without independent artifacts, task evidence and observed holdout metrics it must block.
2. For real work, provide task evidence, benchmarks and a digest manifest. Verify the origin and independence of those materials manually or through separately authenticated systems.
3. Treat the aggregate as an advisory review, never an automatic GitHub publish or a source of account permissions.
4. Keep the last green revision available for rollback and record any blocker in `docs/CONTINUITY.md`.

**Check:** Deliberately omit evidence and corrupt manifest data; review must return BLOCKED.

## Source access

Official reference design: https://developers.google.com/optimization/scheduling/job_shop (resource scheduling), https://developers.openai.com/api/docs/guides/agents/guardrails-approvals (gated agent actions), https://github.com/openai/openai-agents-python (optional authorized multi-model runtime). These are documentation links, not installed providers or execution capabilities.

## Fallback and limits

No model-weight updates, background execution, paid inference or external API calls occur merely by loading this skill.

## v11.0 — Three targeted extensions

1. **Task-specific contract:** For **mission-release-review**, freeze the task objective, known input constraints and actual available tools; avoid loading this skill when it adds no user value.
2. **Adversarial failure probe:** Test the strongest failure case for this skill, including incompatible requirements, unavailable tools and unverified claims; record what was not executed.
3. **Lean evidence and fallback:** Prefer a small decisive verification or truthful alternative over unnecessary tool use. Image/video rendering is optional and never required for a nonimage request.
