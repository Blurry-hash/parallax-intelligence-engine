---
name: symbolic-execution-planning
description: Path constraint exploration; use for reasoning about hard-to-reach conditional branches
---

# Path constraint exploration

**Trigger:** Reasoning about hard-to-reach conditional branches.

**Goal:** Make a concrete, reviewable improvement without inventing new model capabilities.

## Operational procedure

1. Establish the workload, correctness contract, resource budget, accessible tooling and protected requirements.
2. Translate important branch guards into logical constraints and list feasible vs impossible paths.
3. Use bounded symbolic execution or small enumeration when available; cap path explosion.
4. Confirm candidate counterexamples against the original executable program.
5. Record measured results, counterexamples and rollback steps; compare with baseline and avoid introducing unnecessary dependencies.

**Check:** At least one targeted boundary/path case reproduced, or explicit infeasibility rationale.

## Source access

Relevant upstream reference: https://github.com/angr/angr. Consult current documentation and its license before adopting code. A repository link is a pointer, not installed software or proof of a performance claim. Do not run untrusted scripts automatically.

## Fallback and limits

If no executor is available, provide an executable test plan or patch and label it NOT EXECUTED. Never pretend to have measured speed, quality, security or correctness without running the relevant checks.

## v11.0 — Three targeted extensions

1. **Task-specific contract:** For **symbolic-execution-planning**, freeze the task objective, known input constraints and actual available tools; avoid loading this skill when it adds no user value.
2. **Adversarial failure probe:** Test the strongest failure case for this skill, including incompatible requirements, unavailable tools and unverified claims; record what was not executed.
3. **Lean evidence and fallback:** Prefer a small decisive verification or truthful alternative over unnecessary tool use. Image/video rendering is optional and never required for a nonimage request.
