---
name: incremental-build-analysis
description: Incremental compilation and cache validity; use for shortening builds without stale artifacts
---

# Incremental compilation and cache validity

**Trigger:** Shortening builds without stale artifacts.

**Goal:** Make a concrete, reviewable improvement without inventing new model capabilities.

## Operational procedure

1. Establish the workload, correctness contract, resource budget, accessible tooling and protected requirements.
2. Identify deterministic inputs, build outputs and dependency closure.
3. Cache by content and toolchain version; invalidate on changed transitive dependencies.
4. Test cold/warm/changed-input builds and compare output hashes.
5. Record measured results, counterexamples and rollback steps; compare with baseline and avoid introducing unnecessary dependencies.

**Check:** Warm builds faster while clean and incremental outputs are identical.

## Source access

Relevant upstream reference: https://github.com/bazelbuild/bazel. Consult current documentation and its license before adopting code. A repository link is a pointer, not installed software or proof of a performance claim. Do not run untrusted scripts automatically.

## Fallback and limits

If no executor is available, provide an executable test plan or patch and label it NOT EXECUTED. Never pretend to have measured speed, quality, security or correctness without running the relevant checks.
