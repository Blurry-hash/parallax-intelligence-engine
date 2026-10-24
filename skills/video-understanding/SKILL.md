---
name: video-understanding
description: Inspect video, speech and on-screen text with timestamped coverage
---

# Inspect video, speech and on-screen text with timestamped coverage

## Operational procedure

1. Inventory every file or URL, duration, streams, language, user objective and privacy constraints. Probe actual access: a TikTok URL can fail; request the file only when access is blocked. Distinguish video frames, decoded audio, ASR transcript, OCR and metadata as separate modalities.
2. Run `tools/media_ingest.py INPUT --out DIRECTORY --interval 5` for local ffprobe metadata, representative JPEG frames and optional PCM audio. This prepares evidence; it does not itself hear speech, recognize text or understand motion. Do not send private footage to an external provider without authorization.
3. Choose frame sampling by information density: overview contact sheets first, then scene changes, title cards, demonstrations and dense screens at native resolution. Increase temporal sampling around gestures/cuts; one frame cannot establish motion, timing, lip-sync or the absence of a transient event.
4. If native audio listening is genuinely supported, inspect it; otherwise use an actually available ASR engine with timestamps, language and confidence. Keep raw transcript separate from corrections. Mark speaker uncertainty, overlaps and unintelligible spans. Audio extraction is not transcription and a transcript alone is not listening.
5. Read subtitles/on-screen code and OCR when supported. Verify names, units, commands, links and numbers against original frames. Burned-in subtitles may omit speech or be wrong. Never reconstruct missing dialogue as fact.
6. Align observations in a timeline: start/end, visual event, quoted/transcribed words, OCR, modality and uncertainty. Resolve audio/text conflicts using source checks; retain unresolved disagreements. For long clips work in overlapping segments and carry entities/claims forward without inventing unseen content.
7. Produce a faithful summary, ordered procedures, named resources and separable factual claims. Attribute promotional promises to the speaker. Fact-check only when requested or when needed for high-stakes advice; distinguish what the clip says from what is true.
8. Report coverage precisely: sampled frame times, transcript spans, unreviewed gaps and whether sound/movement were examined. Never label a 12-frame contact sheet a full audiovisual review. Preserve concise transferable context in the current chat; long-term storage depends on actual host features.

**Check:** For a subtitled clip with no ASR, summarize visible text while explicitly leaving unheard claims unknown. If the user asks what was said at an unsampled point, inspect that point rather than interpolate.

**Deliverable:** Short summary by default; timestamped evidence table and action extraction for detailed analysis. Reopen source timestamps for pivotal claims.

## Source access

https://ffmpeg.org/ffprobe.html ; https://ffmpeg.org/ffmpeg.html ; https://github.com/openai/whisper . Whisper is an optional ASR implementation, not an installed dependency.
