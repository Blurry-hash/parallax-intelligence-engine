---
name: property-based-testing-lab
description: Property-based test design; use for exploring broad input spaces and edge cases
---

# Property-based test design

**Trigger:** Exploring broad input spaces and edge cases.

**Goal:** Make a concrete, reviewable improvement without inventing new model capabilities.

## Operational procedure

1. Establish the workload, correctness contract, resource budget, accessible tooling and protected requirements.
2. Derive invariant properties from public contracts, not the implementation.
3. Generate boundary, degenerate, structured and malformed inputs with fixed seeds for reproduction.
4. Shrink counterexamples; convert every confirmed failure into a deterministic regression.
5. Record measured results, counterexamples and rollback steps; compare with baseline and avoid introducing unnecessary dependencies.

**Check:** Each property has an oracle and reproducible failing input when violated.

## Source access

Relevant upstream reference: https://github.com/HypothesisWorks/hypothesis. Consult current documentation and its license before adopting code. A repository link is a pointer, not installed software or proof of a performance claim. Do not run untrusted scripts automatically.

## Fallback and limits

If no executor is available, provide an executable test plan or patch and label it NOT EXECUTED. Never pretend to have measured speed, quality, security or correctness without running the relevant checks.
