---
name: visual-compositing-plan
description: Precise mask and pixel-lock compositing
---

# Precise mask and pixel-lock compositing

## Operational procedure

1. Choose deterministic layering when unchanged source pixels must remain exactly identical.
2. Specify alpha/mask boundary, perspective, light matching, grain, occlusion and output color profile.
3. If no compositing tool exists, provide a step-by-step plan, not an asserted image operation.

4. Record layer order, masks, premultiplied alpha handling, color space, light direction and intended output dimensions. Check hair edges against both light and dark backdrops.

**Check:** Halos, double shadows or inconsistent perspective fail the composite. Pixel-exact locked regions need deterministic replacement, not another generative pass.

## Source access

Start from the primary tool/reference named in this procedure and `sources/sources.json`; verify the version relevant to this task before relying on an integration.
