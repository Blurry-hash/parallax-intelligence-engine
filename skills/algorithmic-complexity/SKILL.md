---
name: algorithmic-complexity
description: Algorithm selection and complexity bounds; use for choosing scalable data structures and algorithms
---

# Algorithm selection and complexity bounds

**Trigger:** Choosing scalable data structures and algorithms.

## Operational procedure

1. Measure input cardinality/distribution and choose a complexity target; compare worst-case and amortized bounds.
2. Prototype a baseline and a candidate on adversarial, skewed and representative inputs; include memory, not just runtime.
3. Reject attractive asymptotics if constants, I/O patterns or correctness violate real workloads.

**Check:** Proof sketch + measured scaling with a workload record and counterexample.

## Source access

Relevant upstream reference: https://github.com/TheAlgorithms/Python. Consult current documentation and its license before adopting code. A repository link is a pointer, not installed software or proof of a performance claim. Do not run untrusted scripts automatically.
