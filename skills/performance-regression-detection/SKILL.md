---
name: performance-regression-detection
description: Paired performance guardrails; use for preventing slower releases even when average looks fine
---

# Paired performance guardrails

**Trigger:** Preventing slower releases even when average looks fine.

## Operational procedure

1. Freeze paired task IDs, correctness criteria, baseline latencies and maximum allowable p95 regression.
2. Reject missing tasks, invalid timing or reduced correctness before computing speed gains.
3. Analyze paired deltas and tail latency; use held-out testsets and repeatability.

**Check:** Explicit pass/fail report with sample size and caveats.

## Source access

Relevant upstream reference: https://github.com/google/benchmark. Consult current documentation and its license before adopting code. A repository link is a pointer, not installed software or proof of a performance claim. Do not run untrusted scripts automatically.
