---
name: sfx-design
description: Design and mix synthesized sound effects, ambience and music for story shorts. Use when planning a cue sheet or building the audio mix.
---
# SFX & music design

## Cue sheet (one row per event)
`time | event | sound (function) | level dB | pan | note` — build it from the storyboard; no event without a sound, no sound without an event.

## Library (all code-made: `reference_code/sfx_library.py`)
heartbeat · breath/gasp/gulp · bus_rumble (loop bed) · wind · crickets (night ambience) · door_hiss · clink (tiffin/metal) · phone_buzz · riser · impact · whoosh · tick. Extend by adding functions; document parameters in the docstring.

## Layering rules
- Every important event = 2–3 layers (e.g. door = hiss + thud + latch tick).
- Ambience bed always on (−32…−26 dB): bus_rumble + wind + crickets; change it when location changes.
- Tension build: heartbeat starts 72 bpm → 110 bpm over the last 12 s; **riser 2.5 s** into the cliffhanger; then **hard cut to silence 0.4 s**, then one low `impact`.
- Hits −14…−10 dB; voice always dominates. Duck music/ambience 6 dB under voice (attack 30 ms, release 300 ms).
- Pan moving things (bus passing) L→R with equal-power law.
- Avoid constant loops: randomize timing ±10% and pitch ±3%.

## Music
Drone on D + soft pad; accents from the free **GeneralUser GS** soundfont via `tinysoundfont` (GM programs: 104 sitar, 111 shehnai, 89 warm pad). D Phrygian-dominant (D Eb F# G A Bb C). No copyrighted tracks. Music off at reveals; returns after the cliffhanger as a single sustained note.

## Deliver
`out/epNN/audio/{cue_sheet.csv, voice.wav, sfx.wav, music.wav, mix.wav}` and the loudness report.
