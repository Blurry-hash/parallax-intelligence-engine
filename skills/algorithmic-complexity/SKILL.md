---
name: algorithmic-complexity
description: Algorithm selection and complexity bounds; use for choosing scalable data structures and algorithms
---

# Algorithm selection and complexity bounds

**Trigger:** Choosing scalable data structures and algorithms.

**Goal:** Make a concrete, reviewable improvement without inventing new model capabilities.

## Operational procedure

1. Establish the workload, correctness contract, resource budget, accessible tooling and protected requirements.
2. Measure input cardinality/distribution and choose a complexity target; compare worst-case and amortized bounds.
3. Prototype a baseline and a candidate on adversarial, skewed and representative inputs; include memory, not just runtime.
4. Reject attractive asymptotics if constants, I/O patterns or correctness violate real workloads.
5. Record measured results, counterexamples and rollback steps; compare with baseline and avoid introducing unnecessary dependencies.

**Check:** Proof sketch + measured scaling with a workload record and counterexample.

## Source access

Relevant upstream reference: https://github.com/TheAlgorithms/Python. Consult current documentation and its license before adopting code. A repository link is a pointer, not installed software or proof of a performance claim. Do not run untrusted scripts automatically.

## Fallback and limits

If no executor is available, provide an executable test plan or patch and label it NOT EXECUTED. Never pretend to have measured speed, quality, security or correctness without running the relevant checks.
