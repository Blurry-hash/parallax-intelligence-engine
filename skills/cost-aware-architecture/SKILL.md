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
