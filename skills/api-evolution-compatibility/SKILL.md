---
name: api-evolution-compatibility
description: Backward-compatible API changes; use for versioning apis and schemas without breaking clients
---

# Backward-compatible API changes

**Trigger:** Versioning APIs and schemas without breaking clients.

## Operational procedure

1. Inventory clients, wire formats, error behavior and version negotiation.
2. Apply additive evolution where possible; stage migrations with dual read/write only when justified.
3. Run old-client/new-server and new-client/old-server contract checks.

**Check:** Compatibility matrix covers supported clients and rollback behavior.

## Source access

Relevant upstream reference: https://github.com/oasdiff/oasdiff. Consult current documentation and its license before adopting code. A repository link is a pointer, not installed software or proof of a performance claim. Do not run untrusted scripts automatically.
