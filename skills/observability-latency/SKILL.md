---
name: observability-latency
description: Instrument and optimize end-to-end AI task latency safely
---

# Observability & Latency

**Trigger:** Requests to make software, agents or inference materially faster or more reliable.

**Purpose:** Optimize verified end-to-end performance, not speculative tokens-per-second gains.

## Operational procedure

1. Define the user-visible operation, acceptable correctness, workload shape, hardware and budget.
2. Measure the baseline: p50/p95/p99 latency, error rate, task completion rate, throughput, cost and cold-start time where available.
3. Trace the critical path with structured spans for queueing, routing, retrieval, model prefill/generation, tool calls and rendering.
4. Diagnose bottlenecks before tuning. Separate network RTT, DNS, database, CPU, GPU, caching, context size, concurrency and third-party delays.
5. Consider batch sizes, caching, async concurrency, model routing, speculative execution and smaller context only after checking correctness and worst-case reliability.
6. Compare performance with identical workloads and resource limits; include rollbacks and protection against cascading retries and over-parallelization.
7. Avoid storing secrets, personal data, private prompts or unredacted responses in telemetry; implement retention and access control.

**Check:** Repeated measurements demonstrate improvement without unacceptable accuracy, security or cost regressions.

## Source access

Consult topics `observability`, `speed`, `evaluation` and `reliability` in `sources/sources.json`; OpenTelemetry for supported instrumentation patterns.
