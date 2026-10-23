---
name: runtime-memory-analysis
description: Allocation and memory footprint engineering; use for investigating oom, gc pressure and memory leaks
---

# Allocation and memory footprint engineering

**Trigger:** Investigating OOM, GC pressure and memory leaks.

**Goal:** Make a concrete, reviewable improvement without inventing new model capabilities.

## Operational procedure

1. Establish the workload, correctness contract, resource budget, accessible tooling and protected requirements.
2. Profile allocations and resident memory with representative input sizes.
3. Find retention roots, duplicated buffers and copy paths; stream or reuse safely.
4. Measure peak memory and correctness under repeated load and long sessions.
5. Record measured results, counterexamples and rollback steps; compare with baseline and avoid introducing unnecessary dependencies.

**Check:** Lower measured peak without leaks, premature frees or output changes.

## Source access

Relevant upstream reference: https://github.com/bloomberg/memray. Consult current documentation and its license before adopting code. A repository link is a pointer, not installed software or proof of a performance claim. Do not run untrusted scripts automatically.

## Fallback and limits

If no executor is available, provide an executable test plan or patch and label it NOT EXECUTED. Never pretend to have measured speed, quality, security or correctness without running the relevant checks.

## v11.0 — Three targeted extensions

1. **Task-specific contract:** For **runtime-memory-analysis**, freeze the task objective, known input constraints and actual available tools; avoid loading this skill when it adds no user value.
2. **Adversarial failure probe:** Test the strongest failure case for this skill, including incompatible requirements, unavailable tools and unverified claims; record what was not executed.
3. **Lean evidence and fallback:** Prefer a small decisive verification or truthful alternative over unnecessary tool use. Image/video rendering is optional and never required for a nonimage request.
