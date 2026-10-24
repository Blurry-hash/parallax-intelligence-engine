---
name: mutation-testing-strategy
description: Test-suite mutation resistance; use for checking whether tests would detect real implementation bugs
---

# Test-suite mutation resistance

**Trigger:** Checking whether tests would detect real implementation bugs.

## Operational procedure

1. Select representative mutations that change branches, operators and error handling.
2. Run tests against isolated candidate mutations and record which survive.
3. Investigate surviving realistic mutations; never optimize solely for mutation score.

**Check:** Critical behavior is caught by at least one meaningful test per risk.

## Source access

Relevant upstream reference: https://github.com/mutmut/mutmut. Consult current documentation and its license before adopting code. A repository link is a pointer, not installed software or proof of a performance claim. Do not run untrusted scripts automatically.
