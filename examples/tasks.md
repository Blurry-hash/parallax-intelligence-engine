# Example tasks / invocation

## 1. Production bug fix
Task: "Diagnose this Express auth redirect regression and implement the smallest tested fix."
Load `coding-engineering`, `security-reliability`. Check failing route/tests, repair, run tests, report commits/results.

## 2. Latency improvement
Task: "Reduce p95 server response latency by 30% without sacrificing accuracy."
Load `performance-speed`, `coding-engineering`. Capture baseline, profile, compare changes under equal traffic, monitor error rate.

## 3. ESP32 device and app integration
Task: "Design a BLE ESP32 gateway with low power consumption."
Load `hardware-physical`, `networking-digital`. Check region rules, SoC constraints, electrical limits, firmware, BLE throughput and power budget.

## 4. Photographic edit
Task: "Make this photograph look like an authentic 1980s snapshot, but preserve all subjects' identities."
Load `image-generation`. Define protected attributes, period optics and printing artifacts; inspect resulting reference drift.

## 5. Deep model research
Task: "Compare benchmarkable reasoning techniques from GPT-OSS, Open R1 and Qwen3."
Load `deep-reasoning`, `knowledge-distillation`, `scientific-research`. Avoid equating model cards with independent measured results.

## Deep + wide research
“Compare several independent approaches to this unusual engineering failure. Search diverse GitHub/academic/vendor sources, trace key assumptions back to primary evidence, challenge the leading hypothesis and stop when more searching would not change the decision.”

## Fast and human
“Answer as a natural expert in two short paragraphs, without robotic framing. Use the smallest needed verification step and avoid excessive internal branching. Add humor only if clearly appropriate.”

## Render a real video without a generative video model

Prompt: “Create a 1080×1920 animated explainer MP4 from this scene manifest. Use FFmpeg if available, preserve timestamps, and verify the result with ffprobe.”

Example:

```bash
python3 tools/render_video.py examples/video-storyboard.json --out /tmp/aiontrix-demo.mp4
ffprobe -v error -show_entries format=duration -show_entries stream=codec_name,width,height,r_frame_rate -of json /tmp/aiontrix-demo.mp4
```

The output is procedural motion graphics, **not** a neural cinematic video generation result. Higher-end scenes require their respective rendering engine, model or assets.
