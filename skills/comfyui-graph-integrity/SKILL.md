---
name: comfyui-graph-integrity
description: ComfyUI workflow reasoning and safety
---

# ComfyUI workflow reasoning and safety

## Operational procedure

1. Check node inputs/outputs, checkpoint and control compatibility, seeds, scheduler and mask propagation.
2. Treat downloaded graph or custom nodes as untrusted code; review license, origin, models and credentials before running.
3. ComfyUI is an optional backend, not a prerequisite for advice or for unrelated design code.

4. Reject dangling node links, missing checkpoints and incompatible socket types before a short preview; preserve seed and workflow JSON for replay.

**Check:** A workflow referencing a missing checkpoint stays blocked; a valid JSON parse alone cannot prove the graph executes.

## Source access

Start from the primary tool/reference named in this procedure and `sources/sources.json`; verify the version relevant to this task before relying on an integration.
