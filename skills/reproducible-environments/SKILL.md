---
name: reproducible-environments
description: Hermetic toolchains and build provenance; use for making developer, ci and deployment results consistent
---

# Hermetic toolchains and build provenance

**Trigger:** Making developer, CI and deployment results consistent.

## Operational procedure

1. Pin runtime/toolchain and dependencies; declare required system tools.
2. Use deterministic artifacts, checksums and isolated build steps; avoid hidden network installs.
3. Rebuild from clean checkout and compare manifest, tests and output hashes.

**Check:** Recreated build behaves identically within documented nondeterminism.

## Source access

Relevant upstream reference: https://github.com/reproducible-builds/reproducible-website. Consult current documentation and its license before adopting code. A repository link is a pointer, not installed software or proof of a performance claim. Do not run untrusted scripts automatically.
