---
name: caption-system
description: Burned-in Hindi (Devanagari) captions - shaping, safe zones, word highlight timing, kinetic hook text. Use for any on-screen text.
---
# Captions

## Rendering Devanagari correctly (critical)
- Check `PIL.features.check("raqm")`. **True** → Pillow `ImageDraw.text(..., font=FreeSansBold)` shapes conjuncts/matras correctly. **False** → use the fallback: render captions as transparent PNGs from HTML with **Playwright + Chromium** (`pip install playwright && playwright install chromium`), font Noto Sans Devanagari / FreeSans.
- Never render Hindi through a basic-text API without shaping (Skia `drawString` does not shape Devanagari). Draw text with Pillow/Chromium and composite.
- Always inspect `out/devanagari_test.png` and one real caption frame before approving.

## Layout (1080×1920)
- Safe zone: keep text out of the top ~250 px and bottom ~380 px (platform UI overlays; confirm on a phone).
- Lower-third caption block around y 1450–1600, max **2 lines**, 3–5 words per chunk, 56–64 px bold, white with dark outline/box (alpha ~175), active word in yellow (255,214,64).
- Hook text (first 2 s): big (150+ px), centered, animated in (scale 0.9→1.0, 0.2 s).

## Timing
Per-word times from `voice_timeline.json`: speech segments (pauses ≥40 ms) → words distributed by character count inside each segment. Re-check on 3 random words by ear/eye. Captions appear 0.1 s before the word, leave 0.15 s after.

## QA
Human proofreads all Devanagari. Run `subtitle-readability` check: contrast ≥ 7:1, no line > 2, no chunk shown < 0.5 s.
