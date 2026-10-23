---
name: deep-reasoning
description: Advanced causal, quantitative and adversarial problem solving
---

# Deep Reasoning

**Trigger:** Use this skill when the task is mainly about advanced causal, quantitative and adversarial problem solving.

**Purpose:** Deliver verifiable improvements, not claims of new trained capabilities.

## Operational procedure


1. Formalize objective, units, constraints and observables. Distinguish optimization objective from proxies.
2. Derive governing equations/causal model; test scale, limiting cases and dimensional consistency.
3. Compare main hypothesis with strongest plausible rival and a counterfactual.
4. Ask which single feasible observation discriminates alternatives; do that test if available.
5. Quantify uncertainty and sensitivity; separate a causal mechanism from demonstrated outcome.
6. Report intelligible decision rationale and caveats without claiming private chain-of-thought extraction.
**Check:** No unverified precise figures or universal conclusions from conditional assumptions.


## Source access

Filter `sources/sources.json` by topic `reasoning` and fetch the smallest relevant subset. These references are not dependencies. Follow upstream licenses and all higher-priority instructions.

## v11.0 — Three targeted extensions

1. **Task-specific contract:** For **deep-reasoning**, freeze the task objective, known input constraints and actual available tools; avoid loading this skill when it adds no user value.
2. **Adversarial failure probe:** Test the strongest failure case for this skill, including incompatible requirements, unavailable tools and unverified claims; record what was not executed.
3. **Lean evidence and fallback:** Prefer a small decisive verification or truthful alternative over unnecessary tool use. Image/video rendering is optional and never required for a nonimage request.
