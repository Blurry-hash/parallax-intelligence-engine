---
name: visual-control-backend
description: Conditional image tools and workflow compatibility
---

# Conditional image tools and workflow compatibility

## Operational procedure

1. Inspect actual installed backend support for masking, ControlNet, SAM2, IP-Adapter, resolution and transparent alpha.
2. Check checkpoint/control architecture, node types, model licenses and permissions before rendering or loading untrusted custom nodes.
3. Fallback to clear structured prompts or deterministic compositing and label any unrun inference.

4. Check the installed backend and version for actual mask, control-image or conditioning support. Run a small reference-preservation test before the expensive edit.

**Check:** An unsupported control parameter is not silently dropped; stop or use a documented alternative and recheck protected geometry.

## Source access

Start from the primary tool/reference named in this procedure and `sources/sources.json`; verify the version relevant to this task before relying on an integration.
