#!/usr/bin/env python3
"""Render editable, deterministic motion-graphics MP4 from a safe JSON storyboard.

Requires installed FFmpeg with drawtext, libx264 and ffprobe. Does not require a video AI
model or network access. For complex video use Remotion, Blender, Manim or MoviePy.

Example:
  python3 tools/render_video.py examples/video-storyboard.json --out output.mp4
"""
from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

try:
    from video_qc import assess, probe_file
except ModuleNotFoundError:  # importlib-based repository tests
    from tools.video_qc import assess, probe_file

HEX_COLOR = re.compile(r"^#[0-9A-Fa-f]{6}$")


class StoryboardError(ValueError):
    pass


def checked_storyboard(data: object) -> dict:
    if not isinstance(data, dict):
        raise StoryboardError("Storyboard must be a JSON object")
    width, height, fps = data.get("width"), data.get("height"), data.get("fps")
    if type(width) is not int or type(height) is not int or not (128 <= width <= 3840 and 128 <= height <= 3840):
        raise StoryboardError("width and height must be integers in [128, 3840]")
    if width % 2 or height % 2:
        raise StoryboardError("width and height must be even for yuv420p encoding")
    if type(fps) is not int or not 1 <= fps <= 120:
        raise StoryboardError("fps must be an integer in [1, 120]")
    scenes = data.get("scenes")
    if not isinstance(scenes, list) or not 1 <= len(scenes) <= 24:
        raise StoryboardError("scenes must contain 1–24 entries")
    total = 0.0
    for n, scene in enumerate(scenes, 1):
        if not isinstance(scene, dict):
            raise StoryboardError(f"scene {n} must be an object")
        for k in ("title", "subtitle"):
            if not isinstance(scene.get(k, ""), str) or len(scene.get(k, "")) > 500:
                raise StoryboardError(f"scene {n} {k} must be a string <=500 characters")
        try:
            seconds = float(scene.get("seconds"))
        except (TypeError, ValueError):
            raise StoryboardError(f"scene {n} seconds must be a number") from None
        if not math.isfinite(seconds) or not 0.2 <= seconds <= 120:
            raise StoryboardError(f"scene {n} seconds must be finite and between 0.2 and 120")
        if round(seconds * fps) < 1:
            raise StoryboardError(f"scene {n} is shorter than a frame")
        total += seconds
        if not isinstance(scene.get("background"), str) or not HEX_COLOR.fullmatch(scene["background"]):
            raise StoryboardError(f"scene {n} background must be #RRGGBB")
    if total > 300:
        raise StoryboardError("Total video duration must be <= 300 seconds")
    return data


def require_program(name: str) -> str:
    program = shutil.which(name)
    if program is None:
        raise RuntimeError(f"{name} not found on PATH")
    return program


def font_filter_arg(path: str) -> str:
    # Escape FFmpeg filter separators. This function is for paths, never user text.
    return path.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'").replace(",", "\\,").replace("[", "\\[").replace("]", "\\]")


def ffmpeg_command(story: dict, text_dir: Path, output: Path, font: Path | None = None) -> list[str]:
    width, height, fps = story["width"], story["height"], story["fps"]
    cmd = [require_program("ffmpeg"), "-hide_banner", "-loglevel", "error", "-y"]
    filters = []
    for i, scene in enumerate(story["scenes"]):
        duration = round(float(scene["seconds"]) * fps) / fps
        color = scene["background"].replace("#", "0x")
        cmd += ["-f", "lavfi", "-i", f"color=c={color}:s={width}x{height}:r={fps}:d={duration:.6f}"]
        title_file = text_dir / f"title_{i}.txt"
        subtitle_file = text_dir / f"subtitle_{i}.txt"
        title_file.write_text(scene.get("title", ""), encoding="utf-8")
        subtitle_file.write_text(scene.get("subtitle", ""), encoding="utf-8")
        font_str = f"fontfile={font_filter_arg(str(font))}" if font else "font=Sans"
        tf = font_filter_arg(str(title_file))
        sf = font_filter_arg(str(subtitle_file))
        large = min(80, max(18, width // 11))
        small = min(40, max(12, width // 27))
        duration_fade = min(0.30, duration / 4)
        # Animated fade and a subtle horizontal title movement prove this is video, not a still image.
        pipeline = (
            f"[{i}:v]format=yuv420p,"
            f"drawbox=x=0:y=0:w=iw:h=12:color=white@0.2:t=fill,"
            f"drawtext={font_str}:textfile={tf}:expansion=none:fontcolor=white:fontsize={large}:"
            f"x=(w-text_w)/2+6*sin(t*2):y=h*0.40-text_h/2:shadowcolor=black@0.6:shadowx=2:shadowy=2,"
            f"drawtext={font_str}:textfile={sf}:expansion=none:fontcolor=white@0.85:fontsize={small}:"
            f"x=(w-text_w)/2:y=h*0.60-text_h/2,"
            f"fade=t=in:st=0:d={duration_fade:.3f},"
            f"fade=t=out:st={duration-duration_fade:.3f}:d={duration_fade:.3f},"
            f"setpts=PTS-STARTPTS[v{i}]"
        )
        filters.append(pipeline)
    concat = "".join(f"[v{i}]" for i in range(len(story["scenes"])))
    filters.append(f"{concat}concat=n={len(story['scenes'])}:v=1:a=0[outv]")
    cmd += ["-filter_complex", ";".join(filters), "-map", "[outv]", "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-pix_fmt", "yuv420p", "-r", str(fps), "-movflags", "+faststart", str(output)]
    return cmd


def render(input_path: Path, output: Path, font: Path | None = None) -> dict:
    data = checked_storyboard(json.loads(input_path.read_text(encoding="utf-8")))
    require_program("ffprobe")
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    if font is not None and not font.is_file():
        raise FileNotFoundError(f"Specified font not found: {font}")
    with tempfile.TemporaryDirectory(prefix="parallax_video_") as tmp:
        cmd = ffmpeg_command(data, Path(tmp), output, font)
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    metadata = probe_file(output)
    expected_duration = sum(round(float(scene['seconds']) * data['fps']) for scene in data['scenes']) / data['fps']
    qc = assess(metadata, {'width': data['width'], 'height': data['height'],
                          'fps': data['fps'], 'duration_seconds': expected_duration,
                          'duration_tolerance': 1 / data['fps'], 'codec_name': 'h264', 'has_audio': False})
    if qc['status'] != 'pass':
        raise RuntimeError('Output video failed QC: ' + '; '.join(qc['failures']))
    if output.stat().st_size < 1024:
        raise RuntimeError("Output video unexpectedly empty")
    video = next(stream for stream in metadata['streams'] if stream.get('codec_type') == 'video')
    return {"file": str(output), "bytes": output.stat().st_size,
            "duration": qc['observed']['duration_seconds'], "fps": qc['observed']['fps'],
            "video": video, "qc": qc}



def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("storyboard", type=Path, help="Storyboard JSON file")
    parser.add_argument("--out", type=Path, required=True, help="MP4 output path")
    parser.add_argument("--font", type=Path, default=None, help="Optional local TTF/OTF font")
    args = parser.parse_args()
    try:
        print(json.dumps(render(args.storyboard, args.out, args.font), indent=2))
    except (StoryboardError, ValueError, FileNotFoundError, RuntimeError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f"Error: {exc}\n")


if __name__ == "__main__":
    main()
