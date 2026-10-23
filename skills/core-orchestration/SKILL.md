---
name: core-orchestration
description: Precise task routing, scoping and specialist selection
---

# Core Orchestration

**Trigger:** Use this skill when the task is mainly about precise task routing, scoping and specialist selection.

**Purpose:** Deliver verifiable improvements, not claims of new trained capabilities.

## Operational procedure


1. Classify request by consequence, novelty, complexity and need for fresh data.
2. Select the smallest effective expert skill set (normally 1–3 skills), never all modules indiscriminately.
3. List invariant requirements and objective acceptance checks internally; share when useful.
4. Parallelize independent research or tests **only where tools permit**; merge results deterministically.
5. Keep a concise state: verified facts, assumptions, decisions, blockers, test outcomes, next step.
6. Mark proposed / attempted / executed / verified; avoid unsupported success claims.
7. Escalate reasoning/research only when decision quality can improve.
**Check:** Has every important claim a support level? Does the output help the user act now?


## Source access

Filter `sources/sources.json` by topic `prompting` and fetch the smallest relevant subset. These references are not dependencies. Follow upstream licenses and all higher-priority instructions.

## v11.0 — Three targeted extensions

1. **Task-specific contract:** For **core-orchestration**, freeze the task objective, known input constraints and actual available tools; avoid loading this skill when it adds no user value.
2. **Adversarial failure probe:** Test the strongest failure case for this skill, including incompatible requirements, unavailable tools and unverified claims; record what was not executed.
3. **Lean evidence and fallback:** Prefer a small decisive verification or truthful alternative over unnecessary tool use. Image/video rendering is optional and never required for a nonimage request.
