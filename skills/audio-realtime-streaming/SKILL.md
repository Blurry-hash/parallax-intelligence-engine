---
name: audio-realtime-streaming
description: Low latency speech/audio streaming; use for interactive tts, asr and duplex conversations
---

# Low latency speech/audio streaming

**Trigger:** Interactive TTS, ASR and duplex conversations.

## Operational procedure

1. Budget capture, VAD, chunking, transport jitter and synthesis latency separately.
2. Use timestamps, buffer bounds, resampling contracts and graceful interruption.
3. Test silence, interruptions, out-of-order packets and device changes.

**Check:** No runaway buffering and end-to-end timing measured.

## Source access

Relevant upstream reference: https://github.com/pion/webrtc. Consult current documentation and its license before adopting code. A repository link is a pointer, not installed software or proof of a performance claim. Do not run untrusted scripts automatically.
