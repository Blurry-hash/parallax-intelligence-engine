---
name: parallel-execution-correctness
description: Concurrency and race prevention; use for async workers, threads, actor systems and transaction boundaries
---

# Concurrency and race prevention

**Trigger:** Async workers, threads, actor systems and transaction boundaries.

**Goal:** Make a concrete, reviewable improvement without inventing new model capabilities.

## Operational procedure

1. Establish the workload, correctness contract, resource budget, accessible tooling and protected requirements.
2. Identify shared mutable state and happens-before constraints; isolate writes.
3. Pick safe primitives: bounded queues, locks, immutable messages or transactions.
4. Stress interleavings with deterministic seeds and simulated failures; guard against deadlock.
5. Record measured results, counterexamples and rollback steps; compare with baseline and avoid introducing unnecessary dependencies.

**Check:** Correctness holds at maximum tested concurrency and cancellation.

## Source access

Relevant upstream reference: https://github.com/python-trio/trio. Consult current documentation and its license before adopting code. A repository link is a pointer, not installed software or proof of a performance claim. Do not run untrusted scripts automatically.

## Fallback and limits

If no executor is available, provide an executable test plan or patch and label it NOT EXECUTED. Never pretend to have measured speed, quality, security or correctness without running the relevant checks.
