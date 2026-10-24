---
name: type-directed-code-synthesis
description: Type-directed program construction; use for generating reliable strongly typed code from requirements
---

# Type-directed program construction

**Trigger:** Generating reliable strongly typed code from requirements.

## Operational procedure

1. Convert requirements to types, discriminated unions, input/output contracts and explicit error variants.
2. Generate the smallest compiling program, then run typecheck before adding behavior.
3. Test boundary serialization and unsupported states; avoid `any` and implicit casts without a reason.

**Check:** All interfaces compile; type-level invalid states cannot pass accepted code.

## Source access

Relevant upstream reference: https://github.com/microsoft/pyright. Consult current documentation and its license before adopting code. A repository link is a pointer, not installed software or proof of a performance claim. Do not run untrusted scripts automatically.
