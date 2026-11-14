---
name: shot-camera-motion
description: Shot list, camera moves, transitions and motion rules for suspense shorts. Use when creating storyboards/shotlist.json and animating cameras.
---
# Shots & camera

- Shot length 2–4 s; at least 6 shots per episode; vary scale (wide → medium → close-up → insert).
- Moves: slow **push-in** on reveals (1.00→1.08 over 4 s, ease-in-out); **parallax** layer speeds 0.1 / 0.3 / 1.0; handheld shake for panic (±3 px @ 12 Hz, 0.8 s); light flicker (±8% @ 6–9 Hz) on unstable lights; fog drift 5–10 px/s.
- Transitions: hard cut on SFX hit; whip pan with whoosh for travel; flash-cut only once per episode (for the reveal).
- Composition: rule of thirds, leave look-room, keep the story prop (tiffin) as the brightest point in frame.
- Cliffhanger: final hold 1.2 s on the wrong/empty/unanswerable image + riser→silence→impact.
- `shotlist.json` fields: `id, start, end, scene, camera, characters, action, sfx[], caption, note`.
