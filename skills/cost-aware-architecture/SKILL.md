---
name: cost-aware-architecture
description: Compute and token cost engineering; use for balancing quality, throughput and spend
---

# Compute and token cost engineering

**Trigger:** Balancing quality, throughput and spend.

## Operational procedure

1. Price each step with measured requests, tokens, tool calls and external services.
2. Compare batching, caching, small-model delegation and failure/retry cost.
3. Enforce budget caps and never make paid calls without authorization.

**Check:** Lower cost per verified outcome, not merely fewer generated tokens.

## Source access

Relevant upstream reference: https://github.com/BerriAI/litellm. Consult current documentation and its license before adopting code. A repository link is a pointer, not installed software or proof of a performance claim. Do not run untrusted scripts automatically.
