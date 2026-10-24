---
name: cache-invalidation-design
description: Cache correctness and coherence; use for avoiding stale responses, stampedes and accidental cross-user cache sharing
---

# Cache correctness and coherence

**Trigger:** Avoiding stale responses, stampedes and accidental cross-user cache sharing.

## Operational procedure

1. Define cache keys including auth scope, locale, version and invalidation triggers.
2. Choose TTL, write-through or event invalidation and add stampede protection as justified.
3. Exercise races, stale writes, revocation and deployment-version transitions.

**Check:** No unauthorized cross-scope hits and stale bounds satisfy the contract.

## Source access

Relevant upstream reference: https://github.com/redis/redis. Consult current documentation and its license before adopting code. A repository link is a pointer, not installed software or proof of a performance claim. Do not run untrusted scripts automatically.
