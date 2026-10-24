---
name: code-synthesis-evaluation
description: Reliable automated code generation; use for evaluating ai-generated code beyond passing examples
---

# Reliable automated code generation

**Trigger:** Evaluating AI-generated code beyond passing examples.

## Operational procedure

1. Use specification/acceptance criteria and hidden tests independent of generation context.
2. Check compilation, security, data loss, resource leaks, performance and deterministic reproducibility.
3. Compare original baseline and candidate under equal tools, budgets, dependencies and seeds.

**Check:** Clear pass/fail artifacts, no assumed correctness based on plausibility.

## Source access

Relevant upstream reference: https://github.com/princeton-nlp/SWE-bench. Consult current documentation and its license before adopting code. A repository link is a pointer, not installed software or proof of a performance claim. Do not run untrusted scripts automatically.
