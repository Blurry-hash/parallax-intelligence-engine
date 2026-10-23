---
name: code-synthesis-evaluation
description: Reliable automated code generation; use for evaluating ai-generated code beyond passing examples
---

# Reliable automated code generation

**Trigger:** Evaluating AI-generated code beyond passing examples.

**Goal:** Make a concrete, reviewable improvement without inventing new model capabilities.

## Operational procedure

1. Establish the workload, correctness contract, resource budget, accessible tooling and protected requirements.
2. Use specification/acceptance criteria and hidden tests independent of generation context.
3. Check compilation, security, data loss, resource leaks, performance and deterministic reproducibility.
4. Compare original baseline and candidate under equal tools, budgets, dependencies and seeds.
5. Record measured results, counterexamples and rollback steps; compare with baseline and avoid introducing unnecessary dependencies.

**Check:** Clear pass/fail artifacts, no assumed correctness based on plausibility.

## Source access

Relevant upstream reference: https://github.com/princeton-nlp/SWE-bench. Consult current documentation and its license before adopting code. A repository link is a pointer, not installed software or proof of a performance claim. Do not run untrusted scripts automatically.

## Fallback and limits

If no executor is available, provide an executable test plan or patch and label it NOT EXECUTED. Never pretend to have measured speed, quality, security or correctness without running the relevant checks.
