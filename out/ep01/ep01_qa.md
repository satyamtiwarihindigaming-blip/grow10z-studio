# Episode 1 QA Checklist & Audit: "आख़िरी बस • भाग 1"

## 1. Technical Deliverable Checklist
- [x] **Format & Codec**: MP4 container, H.264 video (`yuv420p`), AAC audio (`192k`, 44.1 kHz).
- [x] **Resolution & Frame Rate**: 1080×1920 (9:16 vertical video for Reels/Shorts), 30.0 fps progressive.
- [x] **Duration**: 43.01 seconds (strictly within 30–45s suspense short requirement, Shorts ≤ 60s).
- [x] **Audio Master Levels**: Processed via EBU R128 `loudnorm` filter (Integrated loudness = −14.0 LUFS ± 1.0, True Peak ≤ −1.5 dBFS).
- [x] **Captions Safe Zone**: Burned-in Devanagari subtitles rendered in the mobile safe lower third (y: 1530px), avoiding bottom platform overlay UI (~380px) and top handles (~250px).
- [x] **Text Shaping & Spelling**: High-resolution browser-accurate Devanagari text rendered with Chromium (no unshaped conjuncts, correct matras, active word highlighted in gold `#FFD640`).
- [x] **Pacing & Hook**:
  - Hook established within first 3.0s ("रात के ग्यारह बजे… रोहन की आख़िरी बस छूटने ही वाली थी").
  - Escalation 1 at 12s (Amma knows his name without introduction).
  - Escalation 2 at 20s (Glowing tiffin handover with forbidden rule).
  - Climactic turn at 34s (Bus doors open to an empty, non-existent village void).
  - Cliffhanger at 37s ("आगे क्या होगा? कल बताता हूँ। कमेंट में अपना अंदाज़ा लिखो।").
- [x] **Content Safety & Originality**:
  - 100% original script and storyline (no copyright, no real brands, no real people or crimes).
  - Family-safe psychological suspense with zero gore, violence, or explicit material.
- [x] **Free / Open Source Asset Audit**:
  - Synthesis engines: Kokoro ONNX (Apache), Pedalboard (Spotify Open Source), TinySoundFont, FFmpeg.
  - Sound effects: 100% procedurally synthesized in Python with NumPy and SciPy.
  - Fonts: FreeSansBold (GNU FreeFont).

---

## 2. ffprobe Output & Verification
```
[STREAM]
codec_name=h264
width=1080
height=1920
r_frame_rate=30/1
[/STREAM]
[STREAM]
codec_name=aac
sample_rate=44100
channels=1
r_frame_rate=0/0
[/STREAM]
[FORMAT]
duration=43.000000
size=3301562
bit_rate=614244
[/FORMAT]
```
- **Duration**: Exactly 43.00 seconds.
- **Resolution**: 1080×1920 (9:16 vertical).
- **Framerate**: 30.0 fps.
- **Video Bitrate**: ~413 kb/s.
- **Audio Bitrate**: ~192 kb/s AAC @ 44.1 kHz.
- **File Size**: 3.15 MB (ultra-lightweight, high visual fidelity).

---

## 3. Visual Contact Sheet
- **Path**: `out/ep01/contact_sheet.png`
- **Tiled Keyframes**:
  1. Frame 0 (t = 1.0s): Shot 1 — Approaching night bus with headlights + title card "आख़िरी बस • भाग 1"
  2. Frame 1 (t = 8.6s): Shot 2 — Bus cabin interior, warm window lights, Rohan & Amma silhouettes
  3. Frame 2 (t = 17.2s): Shot 2 — Close reaction when Amma calls Rohan's name
  4. Frame 3 (t = 25.8s): Shot 3 — Pulsating glowing brass tiffin handover with amber particles
  5. Frame 4 (t = 34.4s): Shot 4 — Bus doors open, Amma steps into nocturnal mist
  6. Frame 5 (t = 40.0s): Shot 6 — Barren void & kinetic cliffhanger card "आगे क्या होगा? कमेंट में अपना अंदाज़ा लिखो"
