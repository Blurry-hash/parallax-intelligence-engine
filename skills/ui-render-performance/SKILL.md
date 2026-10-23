---
name: ui-render-performance
description: UI performance and responsive interaction; use for diagnosing slow interfaces on low-end devices
---

# UI performance and responsive interaction

**Trigger:** Diagnosing slow interfaces on low-end devices.

**Goal:** Make a concrete, reviewable improvement without inventing new model capabilities.

## Operational procedure

1. Establish the workload, correctness contract, resource budget, accessible tooling and protected requirements.
2. Measure interaction-to-next-paint, layout shifts, JS long tasks and network waterfalls.
3. Remove expensive reflows, unnecessary renders and oversized asset transfers.
4. Test low-end/mobile and accessibility, not only desktop Lighthouse scores.
5. Record measured results, counterexamples and rollback steps; compare with baseline and avoid introducing unnecessary dependencies.

**Check:** Measured interaction improvement without lost semantics or broken keyboard paths.

## Source access

Relevant upstream reference: https://github.com/microsoft/playwright. Consult current documentation and its license before adopting code. A repository link is a pointer, not installed software or proof of a performance claim. Do not run untrusted scripts automatically.

## Fallback and limits

If no executor is available, provide an executable test plan or patch and label it NOT EXECUTED. Never pretend to have measured speed, quality, security or correctness without running the relevant checks.

## v11.0 — Three targeted extensions

1. **Task-specific contract:** For **ui-render-performance**, freeze the task objective, known input constraints and actual available tools; avoid loading this skill when it adds no user value.
2. **Adversarial failure probe:** Test the strongest failure case for this skill, including incompatible requirements, unavailable tools and unverified claims; record what was not executed.
3. **Lean evidence and fallback:** Prefer a small decisive verification or truthful alternative over unnecessary tool use. Image/video rendering is optional and never required for a nonimage request.
