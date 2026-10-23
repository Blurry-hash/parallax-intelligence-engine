---
name: video-encoding-efficiency
description: Video delivery and perceptual tradeoffs; use for choosing codecs/bitrates for realistic video pipelines
---

# Video delivery and perceptual tradeoffs

**Trigger:** Choosing codecs/bitrates for realistic video pipelines.

**Goal:** Make a concrete, reviewable improvement without inventing new model capabilities.

## Operational procedure

1. Establish the workload, correctness contract, resource budget, accessible tooling and protected requirements.
2. Define resolution, FPS, motion, color depth, quality and compatibility requirements.
3. Profile encode speed, bitrate, decode support and perceptual quality on multiple scene types.
4. Check audio sync, timestamp monotonicity, frame drop and final metadata.
5. Record measured results, counterexamples and rollback steps; compare with baseline and avoid introducing unnecessary dependencies.

**Check:** File plays on target devices with measured size/quality tradeoff.

## Source access

Relevant upstream reference: https://github.com/FFmpeg/FFmpeg. Consult current documentation and its license before adopting code. A repository link is a pointer, not installed software or proof of a performance claim. Do not run untrusted scripts automatically.

## Fallback and limits

If no executor is available, provide an executable test plan or patch and label it NOT EXECUTED. Never pretend to have measured speed, quality, security or correctness without running the relevant checks.
