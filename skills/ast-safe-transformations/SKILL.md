---
name: ast-safe-transformations
description: Syntax-aware source transformations; use for refactoring many source files without brittle text replacement
---

# Syntax-aware source transformations

**Trigger:** Refactoring many source files without brittle text replacement.

**Goal:** Make a concrete, reviewable improvement without inventing new model capabilities.

## Operational procedure

1. Establish the workload, correctness contract, resource budget, accessible tooling and protected requirements.
2. Parse into an AST or concrete syntax tree and record symbol scopes and formatting requirements.
3. Limit edits to matched nodes, preserve comments via CST if necessary, and emit a reversible diff.
4. Run parser, typecheck and focused regression tests; compare public function signatures.
5. Record measured results, counterexamples and rollback steps; compare with baseline and avoid introducing unnecessary dependencies.

**Check:** Unrelated nodes unchanged and syntax valid under targeted fixtures.

## Source access

Relevant upstream reference: https://github.com/Instagram/LibCST. Consult current documentation and its license before adopting code. A repository link is a pointer, not installed software or proof of a performance claim. Do not run untrusted scripts automatically.

## Fallback and limits

If no executor is available, provide an executable test plan or patch and label it NOT EXECUTED. Never pretend to have measured speed, quality, security or correctness without running the relevant checks.

## v11.0 — Three targeted extensions

1. **Task-specific contract:** For **ast-safe-transformations**, freeze the task objective, known input constraints and actual available tools; avoid loading this skill when it adds no user value.
2. **Adversarial failure probe:** Test the strongest failure case for this skill, including incompatible requirements, unavailable tools and unverified claims; record what was not executed.
3. **Lean evidence and fallback:** Prefer a small decisive verification or truthful alternative over unnecessary tool use. Image/video rendering is optional and never required for a nonimage request.
