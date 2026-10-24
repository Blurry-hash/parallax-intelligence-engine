---
name: video-use-transcript-editing
description: Transcript-led coding-agent video editing
---

# Transcript-led coding-agent video editing

## Operational procedure

1. Derive clip timing from real transcript and word timestamps; preserve the original media and distinguish source from render.
2. Plan filler-word trims, cut boundaries, captions and transition sound continuity using actual available editing tools.
3. Adapt only methods from browser-use/video-use; verify its license and dependencies and do not imply source software ran.

4. Map word timestamps to source timebase, keep a reversible edit decision list, preserve breath/room tone and inspect every join after filler removal.

**Check:** An ASR error must not cause an important word to be cut. Compare source and render at the edit boundary and check caption drift near the end.

## Source access

Start from the primary tool/reference named in this procedure and `sources/sources.json`; verify the version relevant to this task before relying on an integration.
