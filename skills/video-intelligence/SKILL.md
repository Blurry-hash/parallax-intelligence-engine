---
name: video-intelligence
description: Intelligent video creation strategy, multimodal storyboarding, continuity and verification
---

# Video Intelligence

**Trigger:** Any request to plan, create, edit, assess or automate a video.

**Purpose:** Convert user intent into achievable video results across generative, procedural and hybrid workflows without falsely claiming universal model access.

## Operational procedure

1. Identify the deliverable (real MP4/MOV/WebM, GIF, editable timeline, source project, script, storyboard or analysis), target runtime, budget, footage and permissions. Never treat a static image as the requested video.
2. Select a truthful production path: (A) fully procedural, deterministic FFmpeg/Remotion/MoviePy/Manim; (B) 3D scene + camera motion in Blender; (C) generative model only when actually installed, connected and within hardware/licensing limits; (D) hybrid generated footage + deterministic titles/compositing/encoding.
3. Translate concept into a temporal plan: duration, aspect ratio, frame rate, scene beats, composition, text-safe areas, camera movement, cut points, transitions, voice-over/music and constraints. Establish recurring subject, face, clothing, environment and lighting across shots.
4. Separate **LOCKED** identities, references, dialogue, branding and duration from **EDITABLE** transitions and **FLEXIBLE** stylistic choices. Specify expected motion and temporal continuity, not just a list of image prompts.
5. Choose audio/video assets the user owns or has permission to use. Never imply that a diffusion model or proprietary provider is available merely because it appears in a repository.
6. For code-first generation, use `skills/video-code-production/SKILL.md` and run an actual render where tools permit. For diffusion/video models, use `skills/video-generative-workflows/SKILL.md`; resolve model, checkpoint, VRAM, runtime and output parameters.
7. Review representative frames (opening, midpoint, cut boundaries, ending), playback duration, dimensions, frames per second, codec, audio streams, text clipping, legibility, temporal flicker, object/face drift and lip-sync where relevant.
8. Revise the cheapest failed segment rather than blindly rerendering the full video. Keep intermediate timelines/assets reproducible where supported.
9. Deliver the actual artifact if rendered; otherwise clearly label script, plan or unavailable stages. Report the executed commands/tests without claims of generative-video quality that has not been measured.

**Check:** The output is actually moving video when requested; timing and media metadata match the brief; any identity continuity issues are acknowledged; external render costs and licenses are respected.

## Source access

Prioritize official FFmpeg, Remotion, MoviePy, Manim, Blender, ComfyUI and video model repository documentation from `sources/sources.json`. Check model version and platform-specific availability before issuing implementation steps.

## V10 production extension

For exact video tasks, first use `video-shot-grammar` and `video-temporal-consistency` to define narrative beats and protected invariants, then `video-timeline-engineering` and `tools/video_timeline.py` to compile frame-indexed clips and subtitle cues. Use `video-code-production` and `tools/render_video.py` for deterministic motion graphics; use `video-generation-backends` only after model/backend authorization and checkpoint/hardware checks. On final output, apply `video-qc-telemetry` and `tools/video_qc.py`. Avoid asserting that ffprobe detects human identity, storytelling quality or lip-sync: these require actual visual/audio assessment. Track media rights with `video-media-provenance` and cost with `video-render-budget`.
