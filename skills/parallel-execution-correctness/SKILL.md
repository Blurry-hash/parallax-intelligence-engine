---
name: parallel-execution-correctness
description: Concurrency and race prevention; use for async workers, threads, actor systems and transaction boundaries
---

# Concurrency and race prevention

**Trigger:** Async workers, threads, actor systems and transaction boundaries.

## Operational procedure

1. Identify shared mutable state and happens-before constraints; isolate writes.
2. Pick safe primitives: bounded queues, locks, immutable messages or transactions.
3. Stress interleavings with deterministic seeds and simulated failures; guard against deadlock.

**Check:** Correctness holds at maximum tested concurrency and cancellation.

## Source access

Relevant upstream reference: https://github.com/python-trio/trio. Consult current documentation and its license before adopting code. A repository link is a pointer, not installed software or proof of a performance claim. Do not run untrusted scripts automatically.
