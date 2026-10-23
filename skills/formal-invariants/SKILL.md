---
name: formal-invariants
description: State machines and invariant-driven design; use for implementing financial, concurrent or stateful logic with correctness constraints
---

# State machines and invariant-driven design

**Trigger:** Implementing financial, concurrent or stateful logic with correctness constraints.

**Goal:** Make a concrete, reviewable improvement without inventing new model capabilities.

## Operational procedure

1. Establish the workload, correctness contract, resource budget, accessible tooling and protected requirements.
2. Specify preconditions, postconditions, invariants and illegal transitions before implementation.
3. Build explicit transition tables and include failure/retry/idempotent paths, not merely happy-path examples.
4. Model-check or enumerate bounded states when small; otherwise write invariant checks and targeted property tests.
5. Record measured results, counterexamples and rollback steps; compare with baseline and avoid introducing unnecessary dependencies.

**Check:** No invalid transitions under bounded cases; undeveloped proof obligations identified.

## Source access

Relevant upstream reference: https://github.com/tlaplus/tlaplus. Consult current documentation and its license before adopting code. A repository link is a pointer, not installed software or proof of a performance claim. Do not run untrusted scripts automatically.

## Fallback and limits

If no executor is available, provide an executable test plan or patch and label it NOT EXECUTED. Never pretend to have measured speed, quality, security or correctness without running the relevant checks.

## v11.0 — Three targeted extensions

1. **Task-specific contract:** For **formal-invariants**, freeze the task objective, known input constraints and actual available tools; avoid loading this skill when it adds no user value.
2. **Adversarial failure probe:** Test the strongest failure case for this skill, including incompatible requirements, unavailable tools and unverified claims; record what was not executed.
3. **Lean evidence and fallback:** Prefer a small decisive verification or truthful alternative over unnecessary tool use. Image/video rendering is optional and never required for a nonimage request.
