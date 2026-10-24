---
name: formal-invariants
description: State machines and invariant-driven design; use for implementing financial, concurrent or stateful logic with correctness constraints
---

# State machines and invariant-driven design

**Trigger:** Implementing financial, concurrent or stateful logic with correctness constraints.

## Operational procedure

1. Specify preconditions, postconditions, invariants and illegal transitions before implementation.
2. Build explicit transition tables and include failure/retry/idempotent paths, not merely happy-path examples.
3. Model-check or enumerate bounded states when small; otherwise write invariant checks and targeted property tests.

**Check:** No invalid transitions under bounded cases; undeveloped proof obligations identified.

## Source access

Relevant upstream reference: https://github.com/tlaplus/tlaplus. Consult current documentation and its license before adopting code. A repository link is a pointer, not installed software or proof of a performance claim. Do not run untrusted scripts automatically.
