---
name: cache-invalidation-design
description: Cache correctness and coherence; use for avoiding stale responses, stampedes and accidental cross-user cache sharing
---

# Cache correctness and coherence

**Trigger:** Avoiding stale responses, stampedes and accidental cross-user cache sharing.

**Goal:** Make a concrete, reviewable improvement without inventing new model capabilities.

## Operational procedure

1. Establish the workload, correctness contract, resource budget, accessible tooling and protected requirements.
2. Define cache keys including auth scope, locale, version and invalidation triggers.
3. Choose TTL, write-through or event invalidation and add stampede protection as justified.
4. Exercise races, stale writes, revocation and deployment-version transitions.
5. Record measured results, counterexamples and rollback steps; compare with baseline and avoid introducing unnecessary dependencies.

**Check:** No unauthorized cross-scope hits and stale bounds satisfy the contract.

## Source access

Relevant upstream reference: https://github.com/redis/redis. Consult current documentation and its license before adopting code. A repository link is a pointer, not installed software or proof of a performance claim. Do not run untrusted scripts automatically.

## Fallback and limits

If no executor is available, provide an executable test plan or patch and label it NOT EXECUTED. Never pretend to have measured speed, quality, security or correctness without running the relevant checks.
