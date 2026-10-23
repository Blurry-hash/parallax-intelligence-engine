# Audio Intelligence v10.1

## System architecture

Script + speaker consent → actual backend/license qualification → phonetic/prosody direction → authorized synthesis or recordings → PCM master → mixing → WAV/codec quality checks → blind human listening.

**Bundled:** offline, dependency-free 16-bit PCM WAV audio quality analysis and normalization; consent/availability-aware model routing. **Not bundled:** neural TTS weights, ASR models, voice cloning, microphones, paid APIs or a human listening panel.

### Sound and voice realism checks
- Pronunciation, accent consistency, breaths, rhythm, micro-pauses, semantic focus, articulation, fatigue and long-form identity continuity need actual sampled output and listening. Avoid unnatural random breaths.
- Analyze sample peak, RMS dBFS, clip ratio, DC offset and near-silence through `tools/audio_lab.py`; these are **not** LUFS, true peak or subjective realism.
- For final delivery use suitable BS.1770/EBU R128 meters, check true-peak, room/phase artifacts, playback devices and sample-rate conversions. Check speech ASR/diarization only if genuinely connected.
- Do not imitate an identifiable real voice without appropriate consent; distinguish source-code licenses from pretrained weight rights, e.g. F5-TTS weights CC-BY-NC.

### Research shortlist
- [Maintained Coqui TTS](https://github.com/idiap/coqui-ai-TTS) — multilingual and voice adapters; check individual weights.
- [F5-TTS](https://github.com/SWivid/F5-TTS) — flow-matching research; released weights noncommercial.
- [Microsoft VibeVoice](https://github.com/microsoft/VibeVoice) — ASR/realtime research; the original TTS code was withdrawn.
- [AudioCraft](https://github.com/facebookresearch/audiocraft) and [Stable Audio Tools](https://github.com/Stability-AI/stable-audio-tools) — SFX/music, requiring actual checkpoints and licensed assets.
- [pyannote.audio](https://github.com/pyannote/pyannote-audio) — diarization, not TTS.

Quick use: `python tools/audio_lab.py input.wav` or `python tools/voice_route.py examples/voice-task.json examples/voice-backends.json`. Default providers intentionally empty.