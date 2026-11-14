---
name: frame-render-pipeline
description: Architecture for rendering the 2D animation from code - deterministic render(t), layers, camera, chunked ffmpeg encode, resume, verification. Use when writing or debugging the renderer.
---
# Frame render pipeline

## Architecture
`render(frame) -> RGB image`, deterministic from `t = frame/30`. Layers (back→front): background plates (parallax) · midground · characters · FX/particles · light/glow · grain+vignette · captions · progress/brand. A **camera** object (scale, translate, shake) is applied per layer with easing. Pre-render static plates and sprites once; cache by key.

## Tools
Pillow (compositing, Hindi text) + **skia-python** (gradients, blur, glow, shadows, paths) + numpy. Use skia for scene art, Pillow for text. Convert skia→PIL with `image.convert(alphaType=kUnpremul, colorType=kRGBA_8888).toarray()`. Physics/FX optional: `pymunk`.

## Gotchas learned the hard way
- PIL `ImageDraw` on RGBA **replaces** pixels (no blending) → draw translucent shapes on a separate layer then `alpha_composite`.
- Skia text ≠ Devanagari shaping → use Pillow(raqm)/Chromium.
- `Image.rotate` expands nothing: pad sprite canvases so rotation never clips.
- Long jobs: **render in chunks** (e.g. 350 frames) to `part_N.mp4`, then `ffmpeg -f concat -safe 0 -i list.txt -c copy`; support resume (skip existing parts). On a desktop use `multiprocessing` (one worker per core − 1) over chunks.
- Warm-up: when starting mid-timeline, pre-render ~12 frames so smoothed state (arm angles) is continuous.
- Keep variable names unique when `exec`-ing scripts (loop variables clobber CLI args).

## Encode
Raw RGB → ffmpeg pipe → `libx264 -crf 19 -pix_fmt yuv420p`; mux: `-c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart`.

## Verify (mandatory, show output)
`ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate -show_entries format=duration`; extract frames at 0, 20, 40, 60, 80, 100 % into a contact sheet; list file sizes. Never claim "done" without these.
