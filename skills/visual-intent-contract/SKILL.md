---
name: visual-intent-contract
description: Image request classification and reference-role planning
---

# Image request classification and reference-role planning

## Operational procedure

1. Identify whether the user asks for explanation, vector/UI code, retrieved image, new bitmap, targeted edit or deterministic compositing. Do not render for nonimage tasks.
2. Assign every actual reference a role: edit target, identity, pose, composition, palette, illumination or negative example. Resolve reference conflicts.
3. Record LOCKED/EDITABLE/FLEXIBLE constraints and the acceptance criteria. If tools cannot produce the medium, provide a truthful specification.

4. Separate LOCKED, EDITABLE and FLEXIBLE attributes with a concrete reference role for each image. Resolve contradictory locks before generation and state output format.

**Check:** A requested background change must not authorize face or body changes. A prompt-only request must not trigger a render.

## Source access

Start from the primary tool/reference named in this procedure and `sources/sources.json`; verify the version relevant to this task before relying on an integration.
