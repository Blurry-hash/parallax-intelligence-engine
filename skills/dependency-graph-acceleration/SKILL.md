---
name: dependency-graph-acceleration
description: Dependency and impact graph engineering; use for finding safe parallelizable build/test tasks
---

# Dependency and impact graph engineering

**Trigger:** Finding safe parallelizable build/test tasks.

**Goal:** Make a concrete, reviewable improvement without inventing new model capabilities.

## Operational procedure

1. Establish the workload, correctness contract, resource budget, accessible tooling and protected requirements.
2. Model work items and dependencies as a DAG; validate missing references and detect cycles.
3. Compute critical path, independent frontiers, estimated wall time and expensive bottlenecks.
4. Parallelize only independent, non-conflicting work; keep mutable shared resources serialized.
5. Record measured results, counterexamples and rollback steps; compare with baseline and avoid introducing unnecessary dependencies.

**Check:** Dependency-valid schedule and measured completion-time improvement.

## Source access

Relevant upstream reference: https://github.com/google/or-tools. Consult current documentation and its license before adopting code. A repository link is a pointer, not installed software or proof of a performance claim. Do not run untrusted scripts automatically.

## Fallback and limits

If no executor is available, provide an executable test plan or patch and label it NOT EXECUTED. Never pretend to have measured speed, quality, security or correctness without running the relevant checks.
