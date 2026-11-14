---
name: voice-direction
description: Direct and process Hindi AI narration - voice choice, pacing, pauses, mood effects (whisper, phone, echo), breaths/gasps, loudness. Use for any voiceover work.
---
# Voice direction

## Engines (free)
- **Kokoro-onnx** (local, Apache-style open model): voices `hm_omega` (male, F0≈129 Hz, chosen narrator), `hm_psi` (≈135 Hz), `hf_alpha` (≈203), `hf_beta` (≈186). Call: `Kokoro(model,voices).create(text,voice=...,speed=0.92,lang="hi")`, 24 kHz.
- Optional extras the agent may evaluate (verify licence/ToS first, label as unofficial if so): Piper `hi_IN` voices (offline), `edge-tts` (online, unofficial endpoint).
- The voice is a standard Hindi AI voice, **not** a regional accent. Never claim otherwise. Disclose AI voice in post copy if the platform asks.

## Direction by text
- Generate **sentence by sentence** and assemble yourself: normal gap 0.25 s, before a reveal 0.8 s, after the cliffhanger question 0.5 s.
- Use `…` and commas for hesitation; `?` for lifted tone. Re-generate any line that mispronounces (ज़/फ़/ड़ words) and note the fix in `project/pronunciation.md`.
- Speed: 0.92 suspense, 1.0 normal, 1.05 panic. Never above 1.1.

## Mood chains (see `reference_code/voice_fx.py`)
`narration` (HPF70, comp, light room) · `tension` (bigger room, wet 0.22) · `phone` (bandpass 320–3400 + light distortion) · `echo` (0.18 s delay) · `whisperize` (magnitude-only STFT + random phase = whisper).

## Reactions (not available from TTS — synthesize or layer)
`breath()`, `gasp()`, `gulp()` from `reference_code/sfx_library.py`. Place 50–150 ms **before** the line they belong to, level −20 to −14 dB relative to voice.

## Levels
Voice peaks −3 dBFS; final mix −14 LUFS ±1 (`ffmpeg -af loudnorm=I=-14:TP=-1.5:LRA=11`, verify with a second pass). Music ≤ −22 dB under voice with 6 dB ducking.

## Deliver
`out/epNN/voice/` per-line WAVs + `voice_timeline.json` (start/end per line, per-segment pauses detected at 2% RMS, ≥40 ms) for captions and lip/mouth sync.
