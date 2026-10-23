---
name: performance-speed
description: Reduce total latency and expense without reducing quality
---

# Performance Speed

**Trigger:** Use this skill when the task is mainly about reduce total latency and expense without reducing quality.

**Purpose:** Deliver verifiable improvements, not claims of new trained capabilities.

## Operational procedure


1. Choose optimization target: task-completion time, p50/p95 latency, inference tokens/s, build times, throughput, cost or energy.
2. Measure baseline including tool calls/network wait, queueing and cold starts; identify critical path.
3. Improve algorithm/architecture first; batch independent operations, cache immutable results, reuse context and avoid repetitive searches.
4. Route by task difficulty; cheap deterministic tools for arithmetic/validation, stronger model only for hard decisions.
5. For hosted/open-weight inference: test vLLM/SGLang features only if relevant and supported; benchmark output correctness after quantization/batching.
6. Limit concurrency to avoid overload; use retries with bounded exponential backoff and circuit-breaker/fallback rules.
7. Repeat measurements under identical workload; report median, p95, error rate, cost and any quality regression.
**Check:** Demonstrated end-to-end gain rather than speculative 'infinite speed'.


## Source access

Filter `sources/sources.json` by topic `speed` and fetch the smallest relevant subset. These references are not dependencies. Follow upstream licenses and all higher-priority instructions.

## v11.0 — Three targeted extensions

1. **Task-specific contract:** For **performance-speed**, freeze the task objective, known input constraints and actual available tools; avoid loading this skill when it adds no user value.
2. **Adversarial failure probe:** Test the strongest failure case for this skill, including incompatible requirements, unavailable tools and unverified claims; record what was not executed.
3. **Lean evidence and fallback:** Prefer a small decisive verification or truthful alternative over unnecessary tool use. Image/video rendering is optional and never required for a nonimage request.
