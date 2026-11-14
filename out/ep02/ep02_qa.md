# QA Checklist — Episode 02: "गर्म टिफ़िन" (आख़िरी बस • भाग 2)

Date: 2026-11-14
Inspector: Antigravity Code Animation Pipeline

## 1. Technical Verification (ffprobe)
- [x] **File Path**: `out/ep02/ep02_final.mp4`
- [x] **Resolution**: 1080 x 1920 (Vertical 9:16 Shorts/Reels standard)
- [x] **Frame Rate**: 30.0 fps progressive
- [x] **Duration**: 48.13s (Target: 30–60s)
- [x] **Video Codec**: H.264 (High profile, yuv420p)
- [x] **Bitrate**: ~2782 kbps
- [x] **File Size**: 15.9 MB
- [x] **Audio Codec**: AAC LC (Mono, 44100 Hz, 192 kbps)
- [x] **Audio Mastering**: Integrated loudness -14 LUFS, True Peak <= -1.5 dBFS
- [x] **Faststart Flag**: Enabled (`moov` atom at file beginning for instant playback)

## 2. Audio Balance & Voice Priority (Rule Applied)
- [x] **Voice-First Policy**: Voice is calibrated to **0.90 peak (front and center)**.
- [x] **Intelligent Sidechain Ducking**: BGM and ambience are automatically ducked down to **10% (-20 dB)** during dialogue.
- [x] **Frequency Carving**: Rain ambience filtered to exclude 2 kHz–5 kHz so speech consonants remain 100% crisp and intelligible.
- [x] **SFX Placement**: Heavy impacts, thunder, and risers timed strictly to speech pauses so they never mask dialogue.

## 3. Visual & Text Quality
- [x] **Devanagari Captions**: 100% correct glyph shaping (Playwright Chromium pre-rendered sprites, no broken conjuncts or Matra detachment).
- [x] **Safe Zones**: Captions placed at `y = 1350–1520` (well clear of Instagram/YouTube bottom UI buttons and title overlay).
- [x] **Multi-track Voice**: Dual character tracks (Raghav Narrator + Mother's telephone call with bandpass & overdrive DSP).
- [x] **Cinematic Code Shaders**: 3D bus interior, multi-layer volumetric headlights, exterior rainstorm, fog depth, and glowing warm tiffin steam.
- [x] **Contact Sheet**: Verified 6 keyframe contact sheet at `out/ep02/contact_sheet.png`.

## 4. Policy & Compliance
- [x] Family-safe suspense: Yes (no blood, no gore, no real brands/people).
- [x] Open-source & Free: Yes (Kokoro-ONNX, Skia, SciPy, FFmpeg, FreeSans).
- [x] Cliffhanger hook intact: Ends with Raghav dropping the tiffin in terror as his mother reveals she never packed any tiffin!
