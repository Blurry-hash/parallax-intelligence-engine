---
name: video-code-production
description: Practical coding, deterministic video rendering and optimization with FFmpeg, MoviePy, Remotion, Manim and Blender
---

# Code-First Video Production

**Trigger:** Create or edit video using code, including environments with no text-to-video foundation model.

**Purpose:** Deliver actual video artifacts from executable instructions instead of merely giving visual prompts.

## Operational procedure

1. Verify available executables, versions, fonts, licenses, assets and codecs (`ffmpeg -version`, `ffprobe -version`, optional `node`, Python packages and Blender). Install nothing without permission if installation changes the user's system.
2. Choose an engine by requirements: FFmpeg for compositing/cutting/encoding; Remotion for typed UI animations, responsive motion graphics and reusable React components; MoviePy v2 for Python edits; Manim for mathematical/educational scenes; Blender Python for procedural 3D/rendering. Do not mix v1 and v2 MoviePy APIs.
3. Describe the entire timeline in a declarative shot/scene manifest with exact durations, frame rate, dimensions, subtitles, audio layers, asset links and rights.
4. Generate editable source code and assets. Execute with explicit arguments (no shell injection), fail fast on missing inputs, use temporary files and make rerenders deterministic where possible.
5. Render a low-resolution/proxy preview before 4K/120fps or costly final encode. Use streaming encode, cache reusable assets and avoid unnecessarily high frame rates. Avoid claiming exact speedups until benchmarked.
6. Test media metadata with ffprobe. Decode representative frames and play or inspect them if tools allow; check audio absence/presence, color, typography, dynamic motion, export readability and output file existence.
7. If only a CPU is available, use code-driven motion graphics, compositing and lightweight animation rather than pretending computationally expensive photorealistic generation will run locally.
8. For subtitles, use a validated timing transcript and correct font fallback. Recheck synchronization following cuts or time-stretch operations.
9. When delivering HTML/CSS/JS timeline code instead of a video file, explicitly state it has **not** been rendered to video yet.

**Check:** Reproducible render produces expected codec, dimensions, duration and actual frame sequence. Dependency and licensing statements are correct for the chosen engine.

## Source access

Refer to official FFmpeg, Remotion, MoviePy, Manim and Blender documentation indexed in `sources/sources.json`; read version-specific examples rather than assuming package API stability.

## V10 runnable interoperability

A declarative `examples/v10-timeline.json` becomes an EDL, SRT and renderer-ready storyboard using `tools/video_timeline.py`; encode with `tools/render_video.py`, then verify file technical metadata with `tools/video_qc.py` against `examples/v10-video-contract.json`. Scene duration is integral frames at the source FPS; codec/sample timing is verified after encoding. Do not use the deterministic renderer for neural character animation claims.
