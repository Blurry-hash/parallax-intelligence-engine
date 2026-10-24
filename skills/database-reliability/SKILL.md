---
name: database-reliability
description: Improve SQL schemas and transactional integrity with realistic plans and query benchmarks.
---
# Database Reliability


## Source access

https://www.postgresql.org/docs/current/transaction-iso.html (isolation anomalies) and https://www.postgresql.org/docs/current/wal.html (write-ahead logging). DuckDB query speed does not establish transactional guarantees.

## Operational procedure
1. Map data access patterns, ownership, sensitive fields and transactional invariants.
2. Inspect DDL, indexes, cardinality and representative EXPLAIN query plans.
3. Test isolation, unique constraints, migrations, rollbacks and concurrency races.
4. Compare indexed/unindexed query performance using fixed representative samples.
5. Plan backups, restore rehearsal and staged migration verification.
6. Detect PII exposure and least-privilege roles before production changes.

## Failure handling
No live DB access: explain queries and produce safe migration plan; never claim EXPLAIN results.

## Verification criteria
Correct constraints, reversible migrations, no measured query regressions.

**Check:** Report what was actually measured, executed or reviewed. Declare failed, unrun and blocked checks clearly. Protect private repositories and data; obtain approval for consequential external writes.
