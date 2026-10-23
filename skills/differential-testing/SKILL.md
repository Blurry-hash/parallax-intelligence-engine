---
name: differential-testing
description: Cross-implementation oracle testing; use for comparing multiple parsers, compilers, serializers or numerical implementations
---

# Cross-implementation oracle testing

**Trigger:** Comparing multiple parsers, compilers, serializers or numerical implementations.

**Goal:** Make a concrete, reviewable improvement without inventing new model capabilities.

## Operational procedure

1. Establish the workload, correctness contract, resource budget, accessible tooling and protected requirements.
2. Identify independent trusted oracles and normalize output semantics first.
3. Feed identical inputs to at least two implementations; record disagreements, undefined behavior and tolerances.
4. Bisect divergent cases and investigate which implementation is wrong instead of majority voting.
5. Record measured results, counterexamples and rollback steps; compare with baseline and avoid introducing unnecessary dependencies.

**Check:** Differences logged with minimized inputs, versions and provenance.

## Source access

Relevant upstream reference: https://github.com/google/oss-fuzz. Consult current documentation and its license before adopting code. A repository link is a pointer, not installed software or proof of a performance claim. Do not run untrusted scripts automatically.

## Fallback and limits

If no executor is available, provide an executable test plan or patch and label it NOT EXECUTED. Never pretend to have measured speed, quality, security or correctness without running the relevant checks.
