---
name: streaming-backpressure
description: Streaming throughput and cancellation; use for high-volume async data or media pipelines
---

# Streaming throughput and cancellation

**Trigger:** High-volume async data or media pipelines.

## Operational procedure

1. Model producer and consumer rates, queue bounds, latency budget and cancellation semantics.
2. Use bounded buffers, flow control and explicit timeout policies, not infinite retries.
3. Test slow consumer, partial reads, disconnect, overload and shutdown.

**Check:** Bounded resource growth with correct cancellation and no silent data loss.

## Source access

Relevant upstream reference: https://github.com/encode/uvicorn. Consult current documentation and its license before adopting code. A repository link is a pointer, not installed software or proof of a performance claim. Do not run untrusted scripts automatically.
