---
name: type-directed-code-synthesis
description: Type-directed program construction; use for generating reliable strongly typed code from requirements
---

# Type-directed program construction

**Trigger:** Generating reliable strongly typed code from requirements.

**Goal:** Make a concrete, reviewable improvement without inventing new model capabilities.

## Operational procedure

1. Establish the workload, correctness contract, resource budget, accessible tooling and protected requirements.
2. Convert requirements to types, discriminated unions, input/output contracts and explicit error variants.
3. Generate the smallest compiling program, then run typecheck before adding behavior.
4. Test boundary serialization and unsupported states; avoid `any` and implicit casts without a reason.
5. Record measured results, counterexamples and rollback steps; compare with baseline and avoid introducing unnecessary dependencies.

**Check:** All interfaces compile; type-level invalid states cannot pass accepted code.

## Source access

Relevant upstream reference: https://github.com/microsoft/pyright. Consult current documentation and its license before adopting code. A repository link is a pointer, not installed software or proof of a performance claim. Do not run untrusted scripts automatically.

## Fallback and limits

If no executor is available, provide an executable test plan or patch and label it NOT EXECUTED. Never pretend to have measured speed, quality, security or correctness without running the relevant checks.
