---
name: latency-budgeting
description: End-to-end latency budgets; use for reducing perceived slowness across model and tool calls
---

# End-to-end latency budgets

**Trigger:** Reducing perceived slowness across model and tool calls.

**Goal:** Make a concrete, reviewable improvement without inventing new model capabilities.

## Operational procedure

1. Establish the workload, correctness contract, resource budget, accessible tooling and protected requirements.
2. Separate queue, network, retrieval, inference, execution and rendering latency.
3. Allocate per-stage budgets; optimize the critical path instead of irrelevant micro-optimizations.
4. Compare paired p50/p95 and correctness on fixed task sets; count cold starts.
5. Record measured results, counterexamples and rollback steps; compare with baseline and avoid introducing unnecessary dependencies.

**Check:** No quality regression and measured objective wall-time reduction.

## Source access

Relevant upstream reference: https://github.com/open-telemetry/opentelemetry-python. Consult current documentation and its license before adopting code. A repository link is a pointer, not installed software or proof of a performance claim. Do not run untrusted scripts automatically.

## Fallback and limits

If no executor is available, provide an executable test plan or patch and label it NOT EXECUTED. Never pretend to have measured speed, quality, security or correctness without running the relevant checks.
