---
name: audio-realtime-streaming
description: Low latency speech/audio streaming; use for interactive tts, asr and duplex conversations
---

# Low latency speech/audio streaming

**Trigger:** Interactive TTS, ASR and duplex conversations.

**Goal:** Make a concrete, reviewable improvement without inventing new model capabilities.

## Operational procedure

1. Establish the workload, correctness contract, resource budget, accessible tooling and protected requirements.
2. Budget capture, VAD, chunking, transport jitter and synthesis latency separately.
3. Use timestamps, buffer bounds, resampling contracts and graceful interruption.
4. Test silence, interruptions, out-of-order packets and device changes.
5. Record measured results, counterexamples and rollback steps; compare with baseline and avoid introducing unnecessary dependencies.

**Check:** No runaway buffering and end-to-end timing measured.

## Source access

Relevant upstream reference: https://github.com/pion/webrtc. Consult current documentation and its license before adopting code. A repository link is a pointer, not installed software or proof of a performance claim. Do not run untrusted scripts automatically.

## Fallback and limits

If no executor is available, provide an executable test plan or patch and label it NOT EXECUTED. Never pretend to have measured speed, quality, security or correctness without running the relevant checks.

## v11.0 — Three targeted extensions

1. **Task-specific contract:** For **audio-realtime-streaming**, freeze voice consent, waveform quality and acoustic constraints; avoid loading this skill when it adds no user value.
2. **Adversarial failure probe:** Test the strongest failure case for this skill, including incompatible requirements, unavailable tools and unverified claims; record what was not executed.
3. **Lean evidence and fallback:** Prefer a small decisive verification or truthful alternative over unnecessary tool use. Image/video rendering is optional and never required for a nonimage request.
