---
name: video-generative-workflows
description: Model-aware text-to-video, image-to-video and frame-consistent AI video pipelines
---

# Generative Video Workflows

**Trigger:** Requests for neural text-to-video, image-to-video, character-consistent motion or AI video model automation.

**Purpose:** Choose valid models and outputs, or supply a realistic executable setup without pretending expensive models are preloaded.

## Operational procedure

1. Determine whether the task is T2V, I2V, reference-to-video, video-to-video, character-consistent extension, lip-sync, video enhancement or editing. Establish the reference files and their allowed modifications.
2. Inspect actual provider/model access and permissions. Check official repositories and model cards for availability, checkpoint variant, license, VRAM/RAM/GPU requirements, OS support, inference precision and model-specific guidance.
3. Choose an architecture: ComfyUI graphs for reusable node workflows, HF Diffusers for Python-supported pipelines, or a verified native repository (e.g., LTX-2). Older LTX-Video examples must not be passed off as LTX-2 commands.
4. Protect identity, wardrobe, camera direction and anatomy with explicit keyframes and references where supported; avoid unsupported promises about identical subjects or frames.
5. Start with a short, low-cost clip for feasibility, avoiding quality claims based solely on model-card promotional examples. Test for flicker, frame warping, motion logic, faces, limbs and object permanence.
6. Perform deterministic final finishing with FFmpeg/MoviePy/Remotion for trimming, timing, titles, audio and export. Never confuse a sequence of unrelated still images with coherent model-generated motion.
7. Optimize for target device: choose supported resolution/FPS, batching/chunking, memory strategy and post-processing deliberately, verifying actual decode/encode output and compute cost.
8. If the model cannot be run in the current environment, offer a concrete reproducible external workflow or a code-generated alternative, clearly identifying limitations and authorization/cost requirements.

**Check:** Model access, license, capabilities and runtime were checked; clip is truly generated if claimed; continuity is inspected; post-production verified.

## Source access

Consult ComfyUI, LTX-2, Diffusers and verified first-party model repositories from `sources/sources.json`. Treat third-party custom nodes as untrusted until independently examined.

## V10 model and continuity route

Favor live official model guidance for Lightricks/LTX-2 and current vendor-backed video backends, not copied legacy commands. Qualify license, GPU VRAM, checkpoint, version and real execution permissions, then prototype a short conditioned scene. Validate editability, cross-shot continuity and cost separately from `tools/video_qc.py` output; ffprobe cannot establish physically plausible motion or visual fidelity. If no backend is accessible, provide the executable code-first pipeline as a distinct, lower-fidelity alternative.

## v11.0 — Three targeted extensions

1. **Task-specific contract:** For **video-generative-workflows**, freeze frame continuity, timing and actual media formats; avoid loading this skill when it adds no user value.
2. **Adversarial failure probe:** Test the strongest failure case for this skill, including incompatible requirements, unavailable tools and unverified claims; record what was not executed.
3. **Lean evidence and fallback:** Prefer a small decisive verification or truthful alternative over unnecessary tool use. Image/video rendering is optional and never required for a nonimage request.
