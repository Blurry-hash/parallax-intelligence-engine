#!/usr/bin/env python3
"""No-dependency 16-bit PCM WAV quality analysis and reversible peak normalization.

This is SIGNAL PROCESSING, not speech or voice synthesis. RMS dBFS is not LUFS;
peak here is sample peak, not inter-sample true peak. No external network.
"""
from __future__ import annotations
import argparse
import json
import math
import sys
import wave
from array import array
from pathlib import Path

MAX_FRAMES = 20_000_000
MAX_CHANNELS = 2
SUPPORTED_RATES = (8000, 192000)


def _load(path: Path):
    if not path.is_file() or path.stat().st_size > 100_000_000:
        raise ValueError('Missing or oversized WAV file')
    with wave.open(str(path), 'rb') as w:
        channels, rate, width, nframes = w.getnchannels(), w.getframerate(), w.getsampwidth(), w.getnframes()
        if w.getcomptype() != 'NONE' or width != 2 or not (1 <= channels <= MAX_CHANNELS):
            raise ValueError('Only uncompressed mono/stereo 16-bit PCM WAV supported')
        if not (SUPPORTED_RATES[0] <= rate <= SUPPORTED_RATES[1]) or nframes < 1 or nframes > MAX_FRAMES:
            raise ValueError('Invalid frame count or sample rate')
        raw = w.readframes(nframes)
        if len(raw) != nframes * channels * width:
            raise ValueError('Truncated audio data')
    samples = array('h')
    samples.frombytes(raw)
    if sys.byteorder != 'little':
        samples.byteswap()
    return samples, channels, rate


def _db(value: float) -> float | None:
    return round(20 * math.log10(value), 3) if value > 0 else None


def statistics(samples: array, channels: int, rate: int) -> dict:
    length = len(samples)
    if length == 0 or length % channels:
        raise ValueError('Invalid samples')
    total = sum(int(x) ** 2 for x in samples)
    peak = max(abs(int(x)) for x in samples)
    rms = math.sqrt(total / length) / 32768
    dc = sum(int(x) for x in samples) / length / 32768
    # Count near-limit sample values (inter-sample peaks require another analyzer).
    clipping = sum(abs(int(x)) >= 32767 for x in samples)
    near_silent = sum(abs(int(x)) <= 32 for x in samples)
    return {
        'duration_sec': round(length / channels / rate, 5),
        'sample_rate': rate, 'channels': channels, 'format': 'pcm_s16le',
        'sample_peak_dbfs': _db(peak / 32768), 'rms_dbfs': _db(rms),
        'dc_offset': round(dc, 6),
        'clipped_sample_ratio': round(clipping / length, 6),
        'near_silence_sample_ratio': round(near_silent / length, 6),
        'note': 'RMS not LUFS; sample peak not true peak; listening is required for naturalness.',
    }


def analyze(path: Path) -> dict:
    samples, channels, rate = _load(path)
    return statistics(samples, channels, rate)


def normalize(source: Path, target: Path, peak_dbfs: float = -3.0, fade_ms: float = 5.0) -> dict:
    if not (-20 <= peak_dbfs <= -0.1) or not (0 <= fade_ms <= 1000):
        raise ValueError('Unsafe normalization/fade parameters')
    if source.resolve() == target.resolve() or target.exists():
        raise ValueError('Refusing to overwrite source or an existing output')
    samples, channels, rate = _load(source)
    initial = statistics(samples, channels, rate)
    max_sample = max(abs(int(s)) for s in samples)
    if not max_sample:
        raise ValueError('Cannot normalize complete silence')
    desired = 32767 * (10 ** (peak_dbfs / 20))
    gain = desired / max_sample
    frames = len(samples) // channels
    fade_frames = min(int(rate * fade_ms / 1000), frames // 2)
    adjusted = array('h')
    for i, val in enumerate(samples):
        frame = i // channels
        fade = 1.0
        if fade_frames:
            fade = min(1.0, frame / fade_frames, (frames - 1 - frame) / fade_frames)
        out = round(int(val) * gain * max(0.0, fade))
        adjusted.append(max(-32768, min(32767, out)))
    target.parent.mkdir(parents=True, exist_ok=True)
    buffer = array('h', adjusted)
    if sys.byteorder != 'little':
        buffer.byteswap()
    with wave.open(str(target), 'wb') as w:
        w.setnchannels(channels)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(buffer.tobytes())
    return {'before': initial, 'after': statistics(adjusted, channels, rate),
            'gain_db': round(20 * math.log10(gain), 3), 'destination': str(target)}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('input', type=Path)
    p.add_argument('--out', type=Path, help='Optional normalized output WAV')
    p.add_argument('--peak-dbfs', type=float, default=-3.0)
    p.add_argument('--fade-ms', type=float, default=5.0)
    args = p.parse_args()
    result = normalize(args.input, args.out, args.peak_dbfs, args.fade_ms) if args.out else analyze(args.input)
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
