---
name: incremental-build-analysis
description: Incremental compilation and cache validity; use for shortening builds without stale artifacts
---

# Incremental compilation and cache validity

**Trigger:** Shortening builds without stale artifacts.

## Operational procedure

1. Identify deterministic inputs, build outputs and dependency closure.
2. Cache by content and toolchain version; invalidate on changed transitive dependencies.
3. Test cold/warm/changed-input builds and compare output hashes.

**Check:** Warm builds faster while clean and incremental outputs are identical.

## Source access

Relevant upstream reference: https://github.com/bazelbuild/bazel. Consult current documentation and its license before adopting code. A repository link is a pointer, not installed software or proof of a performance claim. Do not run untrusted scripts automatically.
