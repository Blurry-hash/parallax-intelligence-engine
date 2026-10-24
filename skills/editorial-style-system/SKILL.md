---
name: editorial-style-system
description: Create consistent AI-assisted video edits from reusable editorial references
---

# Create consistent AI-assisted video edits from reusable editorial references

## Operational procedure

1. Identify a playable-video versus editable-project deliverable, target platform, duration, aspect, FPS, audience and reference footage. Inspect available editing runtimes before promising After Effects, Remotion, FFmpeg, Blender or a generative model.
2. Analyse owned reference edits into explicit observations: cut rhythm, opening hook, beat hierarchy, typography scale, caption cadence, motion easing, transitions, sound accents, color and safe areas. Separate measured timing from aesthetic interpretation.
3. Maintain a dedicated project directory with STYLE.md (visual rules), TASTE-MODEL.md (accepted/rejected examples and reasons), EDIT-LAWS.md (hard constraints), MOTION-PLAYBOOK.md (named animation recipes), asset manifest, licensed fonts/branding, footage and versioned timelines. These filenames are a useful local convention, not magic integration instructions.
4. Convert the brief into shot/beat IDs with exact in/out frames, required assets, narration, captions and transitions. Prefer reusable parameterized scenes over duplicating code; render one representative difficult 5–10 second segment before a full encode.
5. Make precise editing requests: shot ID, current behavior, desired change, protected audio/timing/identity and acceptance check. Correct one causal failure at a time. Freeze approved sections and rerender affected spans only when the backend supports it.
6. Compare candidate to reference on legibility, timing, narrative clarity, pacing and brand consistency; compare technical output via video_qc. Repeated assets support consistency but should not flatten narrative variation. Preserve project sources and export settings alongside the playable file.
7. Automate deterministic operations such as trim, caption placement, titles, compositing and encode only after rules are explicit. Neural footage generation and natural-language editing require actual installed/connected providers and separate evaluation.

**Check:** Rendered media matches duration/FPS and captions do not overlap or clip. A new scene must obey the same documented typographic and motion rules without copying all prior scene code.

**Provenance:** Inspired in part by the user-uploaded Download (2).mp4. Only sampled visual frames/subtitles were reviewed; the complete narration and automation/income claims were not independently verified.

## Source access

https://www.remotion.dev/docs/ ; https://ffmpeg.org/ffmpeg-filters.html ; https://ae-scripting.docsforadobe.dev/ (community scripting reference; verify against installed Adobe version).
