---
name: ast-safe-transformations
description: Syntax-aware source transformations; use for refactoring many source files without brittle text replacement
---

# Syntax-aware source transformations

**Trigger:** Refactoring many source files without brittle text replacement.

## Operational procedure

1. Parse into an AST or concrete syntax tree and record symbol scopes and formatting requirements.
2. Limit edits to matched nodes, preserve comments via CST if necessary, and emit a reversible diff.
3. Run parser, typecheck and focused regression tests; compare public function signatures.

**Check:** Unrelated nodes unchanged and syntax valid under targeted fixtures.

## Source access

Relevant upstream reference: https://github.com/Instagram/LibCST. Consult current documentation and its license before adopting code. A repository link is a pointer, not installed software or proof of a performance claim. Do not run untrusted scripts automatically.
