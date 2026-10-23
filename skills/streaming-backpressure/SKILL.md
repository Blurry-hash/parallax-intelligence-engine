---
name: streaming-backpressure
description: Streaming throughput and cancellation; use for high-volume async data or media pipelines
---

# Streaming throughput and cancellation

**Trigger:** High-volume async data or media pipelines.

**Goal:** Make a concrete, reviewable improvement without inventing new model capabilities.

## Operational procedure

1. Establish the workload, correctness contract, resource budget, accessible tooling and protected requirements.
2. Model producer and consumer rates, queue bounds, latency budget and cancellation semantics.
3. Use bounded buffers, flow control and explicit timeout policies, not infinite retries.
4. Test slow consumer, partial reads, disconnect, overload and shutdown.
5. Record measured results, counterexamples and rollback steps; compare with baseline and avoid introducing unnecessary dependencies.

**Check:** Bounded resource growth with correct cancellation and no silent data loss.

## Source access

Relevant upstream reference: https://github.com/encode/uvicorn. Consult current documentation and its license before adopting code. A repository link is a pointer, not installed software or proof of a performance claim. Do not run untrusted scripts automatically.

## Fallback and limits

If no executor is available, provide an executable test plan or patch and label it NOT EXECUTED. Never pretend to have measured speed, quality, security or correctness without running the relevant checks.

## v11.0 — Three targeted extensions

1. **Task-specific contract:** For **streaming-backpressure**, freeze the task objective, known input constraints and actual available tools; avoid loading this skill when it adds no user value.
2. **Adversarial failure probe:** Test the strongest failure case for this skill, including incompatible requirements, unavailable tools and unverified claims; record what was not executed.
3. **Lean evidence and fallback:** Prefer a small decisive verification or truthful alternative over unnecessary tool use. Image/video rendering is optional and never required for a nonimage request.
