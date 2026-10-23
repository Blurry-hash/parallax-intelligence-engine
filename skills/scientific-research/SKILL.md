---
name: scientific-research
description: Evidence synthesis and experimentally testable claims
---

# Scientific Research

**Trigger:** Use this skill when the task is mainly about evidence synthesis and experimentally testable claims.

**Purpose:** Deliver verifiable improvements, not claims of new trained capabilities.

## Operational procedure


1. Translate question into precise variables, outcomes and competing hypotheses.
2. Search official documents and primary experiments; assess design, confounders, sample sizes and external validity.
3. Distinguish observation from mechanism, animal from human outcomes, and effect size from significance.
4. Seek null and contradictory results, replication and measurement artifacts.
5. Quantify uncertainty where supported; propose minimal falsifying test or prototype.
6. Label established / probable / speculative / unknown and avoid fictional citations.
**Check:** Main conclusion robust to strongest alternative explanation.


## Source access

Filter `sources/sources.json` by topic `reasoning` and fetch the smallest relevant subset. These references are not dependencies. Follow upstream licenses and all higher-priority instructions.

## v11.0 — Three targeted extensions

1. **Task-specific contract:** For **scientific-research**, freeze the task objective, known input constraints and actual available tools; avoid loading this skill when it adds no user value.
2. **Adversarial failure probe:** Test the strongest failure case for this skill, including incompatible requirements, unavailable tools and unverified claims; record what was not executed.
3. **Lean evidence and fallback:** Prefer a small decisive verification or truthful alternative over unnecessary tool use. Image/video rendering is optional and never required for a nonimage request.
