---
name: mutation-testing-strategy
description: Test-suite mutation resistance; use for checking whether tests would detect real implementation bugs
---

# Test-suite mutation resistance

**Trigger:** Checking whether tests would detect real implementation bugs.

**Goal:** Make a concrete, reviewable improvement without inventing new model capabilities.

## Operational procedure

1. Establish the workload, correctness contract, resource budget, accessible tooling and protected requirements.
2. Select representative mutations that change branches, operators and error handling.
3. Run tests against isolated candidate mutations and record which survive.
4. Investigate surviving realistic mutations; never optimize solely for mutation score.
5. Record measured results, counterexamples and rollback steps; compare with baseline and avoid introducing unnecessary dependencies.

**Check:** Critical behavior is caught by at least one meaningful test per risk.

## Source access

Relevant upstream reference: https://github.com/mutmut/mutmut. Consult current documentation and its license before adopting code. A repository link is a pointer, not installed software or proof of a performance claim. Do not run untrusted scripts automatically.

## Fallback and limits

If no executor is available, provide an executable test plan or patch and label it NOT EXECUTED. Never pretend to have measured speed, quality, security or correctness without running the relevant checks.

## v11.0 — Three targeted extensions

1. **Task-specific contract:** For **mutation-testing-strategy**, freeze the task objective, known input constraints and actual available tools; avoid loading this skill when it adds no user value.
2. **Adversarial failure probe:** Test the strongest failure case for this skill, including incompatible requirements, unavailable tools and unverified claims; record what was not executed.
3. **Lean evidence and fallback:** Prefer a small decisive verification or truthful alternative over unnecessary tool use. Image/video rendering is optional and never required for a nonimage request.
