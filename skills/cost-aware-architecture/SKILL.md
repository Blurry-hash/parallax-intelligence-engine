---
name: cost-aware-architecture
description: Compute and token cost engineering; use for balancing quality, throughput and spend
---

# Compute and token cost engineering

**Trigger:** Balancing quality, throughput and spend.

**Goal:** Make a concrete, reviewable improvement without inventing new model capabilities.

## Operational procedure

1. Establish the workload, correctness contract, resource budget, accessible tooling and protected requirements.
2. Price each step with measured requests, tokens, tool calls and external services.
3. Compare batching, caching, small-model delegation and failure/retry cost.
4. Enforce budget caps and never make paid calls without authorization.
5. Record measured results, counterexamples and rollback steps; compare with baseline and avoid introducing unnecessary dependencies.

**Check:** Lower cost per verified outcome, not merely fewer generated tokens.

## Source access

Relevant upstream reference: https://github.com/BerriAI/litellm. Consult current documentation and its license before adopting code. A repository link is a pointer, not installed software or proof of a performance claim. Do not run untrusted scripts automatically.

## Fallback and limits

If no executor is available, provide an executable test plan or patch and label it NOT EXECUTED. Never pretend to have measured speed, quality, security or correctness without running the relevant checks.

## v11.0 — Three targeted extensions

1. **Task-specific contract:** For **cost-aware-architecture**, freeze the task objective, known input constraints and actual available tools; avoid loading this skill when it adds no user value.
2. **Adversarial failure probe:** Test the strongest failure case for this skill, including incompatible requirements, unavailable tools and unverified claims; record what was not executed.
3. **Lean evidence and fallback:** Prefer a small decisive verification or truthful alternative over unnecessary tool use. Image/video rendering is optional and never required for a nonimage request.
