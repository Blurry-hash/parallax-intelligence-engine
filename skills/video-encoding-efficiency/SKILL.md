---
name: video-encoding-efficiency
description: Video delivery and perceptual tradeoffs; use for choosing codecs/bitrates for realistic video pipelines
---

# Video delivery and perceptual tradeoffs

**Trigger:** Choosing codecs/bitrates for realistic video pipelines.

## Operational procedure

1. Define resolution, FPS, motion, color depth, quality and compatibility requirements.
2. Profile encode speed, bitrate, decode support and perceptual quality on multiple scene types.
3. Check audio sync, timestamp monotonicity, frame drop and final metadata.

**Check:** File plays on target devices with measured size/quality tradeoff.

## Source access

Relevant upstream reference: https://github.com/FFmpeg/FFmpeg. Consult current documentation and its license before adopting code. A repository link is a pointer, not installed software or proof of a performance claim. Do not run untrusted scripts automatically.
