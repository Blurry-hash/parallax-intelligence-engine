---
name: database-query-planning
description: Index and SQL execution planning; use for optimizing slow database queries
---

# Index and SQL execution planning

**Trigger:** Optimizing slow database queries.

## Operational procedure

1. Collect representative query plans, row estimates, selectivity and index statistics.
2. Compare composite index order, covering indexes, join shape and pagination semantics.
3. Benchmark on realistic data with writes, locks and memory tradeoffs, not only tiny SELECTs.

**Check:** Plan-cost and actual latency improve without regression in write paths.

## Source access

Relevant upstream reference: https://github.com/postgres/postgres. Consult current documentation and its license before adopting code. A repository link is a pointer, not installed software or proof of a performance claim. Do not run untrusted scripts automatically.
