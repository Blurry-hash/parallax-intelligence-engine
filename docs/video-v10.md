# V10 / Video Intelligence production contract

## Pipelines

1. **Code-first:** `video_timeline.py` validates frame-accurate shots and exports a JSON storyboard, EDL and SRT. `render_video.py` renders moving H.264 title scenes with FFmpeg; `video_qc.py` probes the actual output.
2. **Hybrid:** Use user-owned video assets and standard tools (FFmpeg, Remotion, MoviePy, Blender). Confirm rendering libraries are installed and licenses permit the use. Maintain masters and sidecar EDL/SRT; export separately.
3. **Generative:** Select real local/authorized inference backends (e.g., official LTX-2/ComfyUI workflow). Record checkpoint version, runtime, VRAM, seed if relevant, reference images and costs. Do not imply checkpoints ship with PARALLAX.
4. **Review-only:** Read source footage, timestamps and metadata; generate findings with verified observations. No rendering claim if the agent cannot execute.

## Frame and continuity contracts

Frame indexes are half-open `[start_frame, end_frame_exclusive)` and all cuts occur on integral frame boundaries. SRT timestamps are rounded to nearest millisecond from integer frames; the compiler never estimates speech alignment. The optional `locked_state` checker validates declared text fields **only**, not face/scene identity in pixels. Inspect opening, midpoint, closing and cut-adjacent frames. Audio/video lip sync must be checked separately.

## Real verification

`ffprobe` checks codec, FPS, dimensions, duration and audio streams. Missing mandatory metadata fails; missing optional metadata warns. A pass does not establish visually compelling video. For compression benchmarking use a valid reference; VMAF/SSIM measure signal quality, not whether a character's face stayed correct. Captions require accessibility review and actual transcript verification.

## References

- [FFprobe reference](https://ffmpeg.org/ffprobe.html)
- [Remotion](https://github.com/remotion-dev/remotion) — inspect license before commercial usage
- [LTX-2](https://github.com/Lightricks/LTX-2) — generative model, hardware and checkpoints not bundled
- [PySceneDetect](https://github.com/Breakthrough/PySceneDetect) — cut detection where installed
- [Netflix VMAF](https://github.com/Netflix/vmaf) — full-reference measurement
- [OpenTimelineIO](https://github.com/PixarAnimationStudios/OpenTimelineIO) — timeline interchange if installed

## How to test

```bash
python tools/video_timeline.py examples/v10-timeline.json --storyboard-out storyboard.json --srt-out captions.srt --edl-out edl.json
python tools/render_video.py storyboard.json --out output.mp4
python tools/video_qc.py output.mp4 --contract examples/v10-video-contract.json
```
