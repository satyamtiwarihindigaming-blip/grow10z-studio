---
name: character-style-2d
description: Visual style bible and sprite rig rules for silhouette + rim-light 2D characters and night environments. Use before drawing any character or background.
---
# 2D character & environment style

## Look
Night, low-key, graphic-novel: palette `#060a1e → #1c2a5a` sky, warm window/lantern light `#ffd27a`, accent amber `#ffc45a`, rim light `(255,196,120)` on characters. Characters are **silhouettes with rim light**; faces get detail only in close-ups (white eye highlights). Emotion = posture + light, not cartoon faces.

## Cast (series 1)
- **रोहन**: college student, backpack, hoodie, ~6.5 heads tall, always screen-left of frame when traveling.
- **अम्मा**: bell-shaped shawl silhouette, slightly hunched, glowing tiffin in hand.
- **ड्राइवर**: cap, side profile, lit from dashboard.
Produce a **pose sheet** (idle, startled, reaching, looking out of window, holding tiffin) and a **turnaround** for each before episode 1; keep PNGs in `project/assets/characters/`.

## Rig
Separate sprites: head, torso, upper/lower arm, hand, prop. Draw at **3× supersample** and downscale (Lanczos). Pivot points saved in `rig.json`. Rotation by `Image.rotate(center=pivot)`. Idle breathing ±2 px at 0.25 Hz. Blink 0.12 s every ~3.3 s only when eyes are visible.

## Consistency checklist (run on contact sheet)
Same proportions, same colour values, same light direction, same line weights, props in the same hand across shots. Fail the shot if any differ.

## Environments
Layered: sky+stars · moon · far hills · mist band · midground · road/bus · foreground silhouettes · vignette · grain. Keep foreground trees **out of key action** (check bus windows and character heads stay visible — this was a real bug). Reusable plates in `project/assets/env/`.
