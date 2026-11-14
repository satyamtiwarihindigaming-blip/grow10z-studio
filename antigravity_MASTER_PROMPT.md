# MASTER PROMPT — Antigravity me paste karo (is folder ko workspace banane ke baad)

Tum meri "AI Film Studio" ke production team ho. Project: Hindi 2D story shorts "आख़िरी बस" (series 1), roz 1 episode, Instagram Reels + YouTube Shorts, sab kuch CODE se banta hai (Python + ffmpeg), sirf free/open-source tools.

**Pehle padho:** `.agents/AGENTS.md`, `project/story_bible.md`, `project/episodes/ep01/*`, aur har kaam ke liye `.agents/skills/*/SKILL.md` (story-hook-tension, voice-direction, sfx-design, caption-system, character-style-2d, frame-render-pipeline, shot-camera-motion, qa-and-publish, blender-3d-optional).

**Phase 0 — Environment audit (abhi karo):**
1. `check_env.py` chalao (pehle `setup_windows.ps1` ya `setup_mac_linux.sh` agar kuch missing ho). Har FAIL ko theek karo ya mujhe exact error dikhao.
2. `reference_code/sfx_library.py`, `voice_fx.py`, `tts_compare_voices.py`, `style_frame_skia.py` chalao aur output files ki list + sizes dikhao. Kya chala, kya nahi — saaf likho.
3. Mujhe ek chhota audit table do: tool | version | status | note. (Blender, Playwright optional hain.)

**Phase 1–3 (har gate pe ruko aur meri approval lo):**
- G1: story bible + 5-episode arc ko review karo; sirf improvements suggest karo, meri story mat badlo.
- G2: Episode 1 ka Hindi script (`script_hi.txt`) — `story-hook-tension` skill ke hisaab se; word count aur timing batao; shabd/uchcharan jo galat ho sakte hain unhe `[NEEDS CONFIRMATION]` mark karo.
- G3: storyboard + shotlist + style frame (character pose sheets: Rohan, Amma, Driver) — `character-style-2d` follow karo.
- G4: animatic: still frames + final audio mix (voice + SFX cue sheet + music) — mujhe sunne/dekhne do.
- G5: sirf approval ke baad final render (`frame-render-pipeline`), phir `qa-and-publish` ki checklist evidence ke saath.

**Kadak niyam:**
- Bina chalaye "ho gaya" mat bolo. Har render ke baad `ffprobe` output + 6-frame contact sheet dikhao.
- Koi paid API, paid asset ya kisi Instagram/YouTube account ki copy nahi. Original kahani, family-safe.
- Hindi text ko main proofread karunga; Devanagari rendering ka screenshot dikhao (`caption-system`).
- Jo cheez pata nahi, `[NEEDS CONFIRMATION]` likho, andaza mat lagao.
- Output sirf `out/epNN/` me; sab files ki list ke saath summary do.

Shuru karo: Phase 0.
