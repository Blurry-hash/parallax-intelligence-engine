---
name: image-generation
description: Reference-grounded image reasoning, generation, editing and compositing; render only when appropriate
---

# Image Intelligence

**Use this skill for image-specific tasks only.** Do not render an image merely to inspect a README, design source code or write a plan. See visual-intent-contract and visual-evidence-qa for specialist cases.

## Operational procedure

1. Classify the requested deliverable: explanatory text, unchanged image retrieval, newly generated bitmap, targeted generative edit, deterministic layer compositing, vector/code-native design or actual video.
2. Index each provided image by role: edit target, identity, pose, composition, style, materials, lighting or forbidden example. User-provided images may be references rather than edit targets.
3. Define **LOCKED** identity, age, facial features, body proportions, markings, exact text, background, camera framing and any protected pixel regions. Define **EDITABLE** requested changes and **FLEXIBLE** refinements. Resolve conflicts before acting.
4. Model image formation through perspective, focal length impression, illumination direction, contact shadows, reflection, materials, occlusion, anatomy and natural imperfections. For old photographs match era-specific cameras, film and actual environments rather than applying a generic filter.
5. Choose the real supported backend. ComfyUI, ControlNet, SAM2 and IP-Adapter require actual compatible models, checkpoints, compute and licensing. Image generation cannot guarantee pixel-identical locked regions; when pixel locks matter, choose deterministic compositing or explicit masks.
6. For constrained editing, apply one requested change at a time, reiterating invariants to minimize unrelated visual drift. Do not add extra subjects, text or props without authorization.
7. If a real image was produced, inspect the actual result for identity drift, fingers, faces, text, edge halos, alpha, illumination, occlusion and export size. Don't fabricate an image comparison or visual score when no image exists.
8. Limit render attempts. Render only when the user wants an image or a genuine visual uncertainty requires it; avoid automatic multi-renders or generic illustrated documentation.
9. Deliver the actual requested output medium. For missing tools, give reproducible instructions and say which evidence is absent, naturally and without internal status tags.

**Check:** Focal user request fulfilled; protected identity, geometry and unchanged regions respected as far as real backend capabilities permit; no unrequested render.

## Source access

Official OpenAI ImageGen references: https://github.com/openai/codex/blob/main/codex-rs/skills/src/assets/samples/imagegen/references/prompting.md. Other optional references: https://github.com/Comfy-Org/ComfyUI, https://github.com/lllyasviel/ControlNet, https://github.com/facebookresearch/sam2, https://github.com/tencent-ailab/IP-Adapter. Use only checked, compatible code and honor source license.

## v11.0 — Three targeted extensions

1. **Task-specific contract:** Freeze intended output type, reference roles and original locked subject properties; image rendering is not an automatic prerequisite.
2. **Adversarial failure probe:** Inspect reference drift, optical/material inconsistency and added objects; never claim pixel-exact restoration from an uncontrolled generative edit.
3. **Lean evidence and fallback:** If an actual output exists, inspect it. Otherwise provide the minimal verifiable plan, supported backend options and unperformed-check limitations.
