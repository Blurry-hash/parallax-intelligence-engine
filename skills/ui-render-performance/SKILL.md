---
name: ui-render-performance
description: UI performance and responsive interaction; use for diagnosing slow interfaces on low-end devices
---

# UI performance and responsive interaction

**Trigger:** Diagnosing slow interfaces on low-end devices.

## Operational procedure

1. Measure interaction-to-next-paint, layout shifts, JS long tasks and network waterfalls.
2. Remove expensive reflows, unnecessary renders and oversized asset transfers.
3. Test low-end/mobile and accessibility, not only desktop Lighthouse scores.

**Check:** Measured interaction improvement without lost semantics or broken keyboard paths.

## Source access

Relevant upstream reference: https://github.com/microsoft/playwright. Consult current documentation and its license before adopting code. A repository link is a pointer, not installed software or proof of a performance claim. Do not run untrusted scripts automatically.
