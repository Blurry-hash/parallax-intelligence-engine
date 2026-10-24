---
name: runtime-memory-analysis
description: Allocation and memory footprint engineering; use for investigating oom, gc pressure and memory leaks
---

# Allocation and memory footprint engineering

**Trigger:** Investigating OOM, GC pressure and memory leaks.

## Operational procedure

1. Profile allocations and resident memory with representative input sizes.
2. Find retention roots, duplicated buffers and copy paths; stream or reuse safely.
3. Measure peak memory and correctness under repeated load and long sessions.

**Check:** Lower measured peak without leaks, premature frees or output changes.

## Source access

Relevant upstream reference: https://github.com/bloomberg/memray. Consult current documentation and its license before adopting code. A repository link is a pointer, not installed software or proof of a performance claim. Do not run untrusted scripts automatically.
