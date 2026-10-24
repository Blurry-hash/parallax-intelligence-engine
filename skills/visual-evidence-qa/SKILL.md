---
name: visual-evidence-qa
description: Optional visual quality review
---

# Optional visual quality review

## Operational procedure

1. Select relevant checks for anatomy, lighting, occlusion, text legibility, edge halo, reference drift and export format.
2. Only examine real input/output if the user requested image generation/editing; do not turn an explanation task into image rendering.
3. Record observed defects and suggest the smallest localized correction; label unavailable checks as unperformed.

4. Keep reference and output side by side at matched crop/scale. Inspect focal subject, anatomy, text, reflections, shadow direction and protected details separately.

**Check:** A thumbnail can hide malformed fingers or text; inspect native resolution and state unviewed regions rather than declaring overall fidelity.

## Source access

Start from the primary tool/reference named in this procedure and `sources/sources.json`; verify the version relevant to this task before relying on an integration.
