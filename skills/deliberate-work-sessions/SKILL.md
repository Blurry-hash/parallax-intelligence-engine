---
name: deliberate-work-sessions
description: Evidence-based active work sessions with requested wall-time budgets, checkpoints, iterative critique, and honest elapsed-time reporting.
---

# Deliberate work sessions — real elapsed effort, not artificial delay

**Trigger:** The user says e.g. “förbättra detta i 50 minuter”, “spend 1 hour improving this”, “work on it for N minutes” or asks for a long uninterrupted deep review.

## Operational procedure

1. Confirm that a persistent execution environment, clock, tools and work authorization actually exist. Without them, **do not claim an N-minute session**; do the best verified work during the available turn and state the actual duration. Do not imply ChatGPT can remain running after its response.
2. Define the desired outcome and acceptance tests. Record a `requested_minutes` budget and an ordered backlog of **distinct useful tasks** (design, implementation, tests, counterexample search, performance measurement, regression review, documentation). Do not create filler/repeated work just to spend time.
3. When execution is supported, use a monotonic clock and log actual executed operations, input or commit IDs, start/end, outcome and timestamps. Set explicit deadlines and per-step resource limits. Allow cancellation and safe checkpoint/resumption where supported. Separate wall elapsed, substantive execution duration, and unverified/model thinking time.
4. Reassess priorities after each meaningful result. Spend additional time on newly discovered evidence gaps or real regressions rather than rerunning unchanged tasks. Stop when budget expires, no worthwhile work remains, or host/tool limits end the session. A request for a long duration never authorizes unlimited spending, bypassing permissions, or remote execution without approval.
5. Include a factual summary of **actual** elapsed seconds, completed steps, tests, unresolved issues and reasons for early stop. Do not say 50 minutes elapsed unless clocks and logs establish it. Quality is measured via independent tests/holdouts, **not** minutes consumed.

**Check:** A sample run produces an auditable JSON ledger with measured durations, no synthetic sleep, and honest `completed` versus `work_exhausted`/`budget_exhausted`/`failed` states. If executor absent, label the proposed long session NOT EXECUTED.

## Source access

Temporal Python workflows: https://github.com/temporalio/sdk-python — optional platform for durable, resumable *authorized* tasks; it does not grant ChatGPT hidden background execution. Local deterministic reference: `tools/work_budget.py`.

## Fallback and limits

A local script executes only allowlisted repository checks specified in a plan. It is **not** a free-running AI researcher, model improvement service, timer-based magic multiplier, or guaranteed 50-minute cognitive session. Persistent cloud execution requires a separately available supported orchestration runtime and explicit permissions.

## v11.0 — Three targeted extensions

1. **Task-specific contract:** For **deliberate-work-sessions**, freeze the task objective, known input constraints and actual available tools; avoid loading this skill when it adds no user value.
2. **Adversarial failure probe:** Test the strongest failure case for this skill, including incompatible requirements, unavailable tools and unverified claims; record what was not executed.
3. **Lean evidence and fallback:** Prefer a small decisive verification or truthful alternative over unnecessary tool use. Image/video rendering is optional and never required for a nonimage request.
