---
name: latency-budgeting
description: End-to-end latency budgets; use for reducing perceived slowness across model and tool calls
---

# End-to-end latency budgets

**Trigger:** Reducing perceived slowness across model and tool calls.

## Operational procedure

1. Separate queue, network, retrieval, inference, execution and rendering latency.
2. Allocate per-stage budgets; optimize the critical path instead of irrelevant micro-optimizations.
3. Compare paired p50/p95 and correctness on fixed task sets; count cold starts.

**Check:** No quality regression and measured objective wall-time reduction.

## Source access

Relevant upstream reference: https://github.com/open-telemetry/opentelemetry-python. Consult current documentation and its license before adopting code. A repository link is a pointer, not installed software or proof of a performance claim. Do not run untrusted scripts automatically.
