---
name: performance-regression-detection
description: Paired performance guardrails; use for preventing slower releases even when average looks fine
---

# Paired performance guardrails

**Trigger:** Preventing slower releases even when average looks fine.

**Goal:** Make a concrete, reviewable improvement without inventing new model capabilities.

## Operational procedure

1. Establish the workload, correctness contract, resource budget, accessible tooling and protected requirements.
2. Freeze paired task IDs, correctness criteria, baseline latencies and maximum allowable p95 regression.
3. Reject missing tasks, invalid timing or reduced correctness before computing speed gains.
4. Analyze paired deltas and tail latency; use held-out testsets and repeatability.
5. Record measured results, counterexamples and rollback steps; compare with baseline and avoid introducing unnecessary dependencies.

**Check:** Explicit pass/fail report with sample size and caveats.

## Source access

Relevant upstream reference: https://github.com/google/benchmark. Consult current documentation and its license before adopting code. A repository link is a pointer, not installed software or proof of a performance claim. Do not run untrusted scripts automatically.

## Fallback and limits

If no executor is available, provide an executable test plan or patch and label it NOT EXECUTED. Never pretend to have measured speed, quality, security or correctness without running the relevant checks.

## v11.0 — Three targeted extensions

1. **Task-specific contract:** For **performance-regression-detection**, freeze the task objective, known input constraints and actual available tools; avoid loading this skill when it adds no user value.
2. **Adversarial failure probe:** Test the strongest failure case for this skill, including incompatible requirements, unavailable tools and unverified claims; record what was not executed.
3. **Lean evidence and fallback:** Prefer a small decisive verification or truthful alternative over unnecessary tool use. Image/video rendering is optional and never required for a nonimage request.
