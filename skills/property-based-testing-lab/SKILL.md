---
name: property-based-testing-lab
description: Property-based test design; use for exploring broad input spaces and edge cases
---

# Property-based test design

**Trigger:** Exploring broad input spaces and edge cases.

## Operational procedure

1. Derive invariant properties from public contracts, not the implementation.
2. Generate boundary, degenerate, structured and malformed inputs with fixed seeds for reproduction.
3. Shrink counterexamples; convert every confirmed failure into a deterministic regression.

**Check:** Each property has an oracle and reproducible failing input when violated.

## Source access

Relevant upstream reference: https://github.com/HypothesisWorks/hypothesis. Consult current documentation and its license before adopting code. A repository link is a pointer, not installed software or proof of a performance claim. Do not run untrusted scripts automatically.
