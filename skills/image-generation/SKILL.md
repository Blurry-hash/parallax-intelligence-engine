---
name: image-generation
description: Grounded image prompting and high-fidelity edits
---

# Image Generation

**Trigger:** Use this skill when the task is mainly about grounded image prompting and high-fidelity edits.

**Purpose:** Deliver verifiable improvements, not claims of new trained capabilities.

## Operational procedure


1. Classify: new generation, targeted edit, stylization or compositing.
2. Assign roles to references: identity, pose, composition, aesthetic and materials. Resolve conflicts explicitly.
3. Define LOCKED (face, distinctive marks, proportions, background areas), EDITABLE and FLEXIBLE properties.
4. Describe camera and scene geometry, lens perspective, lighting direction/quality, physically plausible textures and natural imperfection.
5. For historical images use era-consistent cameras, environments, color science, optics and print artifacts rather than generic filters.
6. Use localized edits and reassert invariants; inspect resulting anatomy, hands, text, light consistency and drift.
7. Acknowledge that generative edits cannot guarantee pixel-identical preservation; use deterministic compositing for hard locks when possible.
**Check:** Focal request fulfilled; no unrequested identity or geometry change.


## Source access

Filter `sources/sources.json` by topic `image` and fetch the smallest relevant subset. These references are not dependencies. Follow upstream licenses and all higher-priority instructions.
