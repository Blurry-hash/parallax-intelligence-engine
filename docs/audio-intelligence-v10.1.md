# Audio Intelligence v10.1 — Realism is an evaluated output, not a prompt adjective

## Execution architecture

```text
Intent + speaker rights → capability/license matrix → provider selection
        ↓                                      ↘ no provider → actual recorded speech or runnable specification
Script → pronunciation/SSML where supported → sentence/phrase chunks
        ↓
Authorized synthesis or source recordings → PCM master → acoustic QA
        ↓
SFX/Foley + controlled room tone → mix → loudness/true-peak meter
        ↓
Blind listening + transcription/diarization checks → approved delivery
```

Only actual installed synthesis checkpoints or authorized API connections may generate voices. The included Python audio tool **does not synthesize speech**. Third-party model code is not downloaded or executed automatically. The sound design pipeline can support voiceover, podcasts, spatial stories, games and video post-production.

## Measured vs subjective

- `tools/audio_lab.py`: 16-bit mono/stereo PCM WAV duration, RMS dBFS, sample peak, clip ratio, DC offset, near-silence percentage, peak normalization and edge fades. It does **not** measure LUFS, true peak, fidelity or realism.
- For delivery loudness use FFmpeg `loudnorm` (two-pass if needed), or BS.1770 compliant analyzers, and true-peak measurement. Verify final encode separately.
- For intelligibility, use authorized ASR to calculate WER/CER; for turn-taking use diarization timestamps if available. Inspect accents and proper nouns manually.
- For true realism, perform blinded multiple-listener evaluations on unseen scripts with voice naturalness, timing, prosody, emotional fit, perceived artifact count and fatigue.

## Shortlist and cautions

- [Maintained Coqui TTS](https://github.com/idiap/coqui-ai-TTS): useful multi-model backend; verify each weight license and updated installation compatibility.
- [F5-TTS](https://github.com/SWivid/F5-TTS): excellent research for flow-matching expressive generation. Code MIT, released weights CC-BY-NC; do not assume commercial permission.
- [VibeVoice](https://github.com/microsoft/VibeVoice): ASR and supported realtime paths; original TTS code was removed from the official repo in response to misuse.
- [AudioCraft](https://github.com/facebookresearch/audiocraft), [Stable Audio Tools](https://github.com/Stability-AI/stable-audio-tools): research on generated SFX/music; weights, RAM/GPU and copyrights require inspection.
- [pyannote.audio](https://github.com/pyannote/pyannote-audio): diarization; not speech synthesis.

## Consent and authenticity

Never generate or clone a recognizable real speaker's voice without appropriate permission. Original synthetic voices should not be misrepresented as a real person's recording. Voice embeddings, reference audio, transcripts and personal data must be scoped, access-controlled and removed when no longer needed.

## Offline commands

```bash
python tools/audio_lab.py /path/to/recording.wav
python tools/audio_lab.py /path/to/recording.wav --out /path/to/normalized.wav --peak-dbfs -3
python tools/voice_route.py examples/voice-task.json examples/voice-backends.json
```

The included voice backend registry intentionally starts empty; it is not a phantom service.
