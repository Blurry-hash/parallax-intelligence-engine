---
name: differential-testing
description: Cross-implementation oracle testing; use for comparing multiple parsers, compilers, serializers or numerical implementations
---

# Cross-implementation oracle testing

**Trigger:** Comparing multiple parsers, compilers, serializers or numerical implementations.

## Operational procedure

1. Identify independent trusted oracles and normalize output semantics first.
2. Feed identical inputs to at least two implementations; record disagreements, undefined behavior and tolerances.
3. Bisect divergent cases and investigate which implementation is wrong instead of majority voting.

**Check:** Differences logged with minimized inputs, versions and provenance.

## Source access

Relevant upstream reference: https://github.com/google/oss-fuzz. Consult current documentation and its license before adopting code. A repository link is a pointer, not installed software or proof of a performance claim. Do not run untrusted scripts automatically.
