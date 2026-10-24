---
name: dependency-graph-acceleration
description: Dependency and impact graph engineering; use for finding safe parallelizable build/test tasks
---

# Dependency and impact graph engineering

**Trigger:** Finding safe parallelizable build/test tasks.

## Operational procedure

1. Model work items and dependencies as a DAG; validate missing references and detect cycles.
2. Compute critical path, independent frontiers, estimated wall time and expensive bottlenecks.
3. Parallelize only independent, non-conflicting work; keep mutable shared resources serialized.

**Check:** Dependency-valid schedule and measured completion-time improvement.

## Source access

Relevant upstream reference: https://github.com/google/or-tools. Consult current documentation and its license before adopting code. A repository link is a pointer, not installed software or proof of a performance claim. Do not run untrusted scripts automatically.
