# AGENTS.md — "आगे क्या होगा" Hindi 2D story shorts (series 1: "आख़िरी बस")

## Goal
Make one original, family-safe suspense story short per day: Hindi narration, 2D animation drawn by code, designed SFX/music, burned-in captions. 1080x1920, 30fps, 30–45 s, ends on a cliffhanger.

## Hard rules
1. **Free/open-source only.** No paid APIs, no paid assets. Local CPU. Download only from GitHub/PyPI/npm or other legitimate public sources.
2. **Original stories only.** Do not scrape, copy or imitate any specific Instagram/YouTube account or creator. No real people, brands, or real crimes. No gore, self-harm, hate, or sexual content.
3. **Truth over polish.** Never say something works unless you ran it and saw the output. After every render run `ffprobe` and show duration/resolution/audio streams, extract 6 frames into a contact sheet, and show it. If something fails, show the exact error and fix it. Mark unknowns `[NEEDS CONFIRMATION]`.
4. **Approval gates** (stop and ask the human at each; never skip):
   G1 story + facts → G2 Hindi script → G3 storyboard + style frame → G4 animatic (still frames + final audio) → G5 final render.
   Never start a final render before G4 is approved.
5. **Language:** Hindi (Devanagari) is the product language; the human chats in Hinglish. Hindi text must be proofread by the human; flag uncertain words.
6. **Music/SFX:** synthesized or CC0/self-made only; record source+licence for anything downloaded in `project/asset_log.md`.
7. Use the skills in `.agents/skills/` for each department. Read the relevant SKILL.md before doing that kind of work.

## Layout
`project/story_bible.md`, `project/episodes/epNN/{script_hi.txt,storyboard.md,shotlist.json}`, `reference_code/` (working examples: SFX synth, voice FX, skia style frame, music mix, character engine), `models/` (downloaded), `fonts/`, `out/epNN/` (final deliverables).

## Definition of done (per episode)
`out/epNN/epNN_final.mp4` + `epNN_captions.txt` + `epNN_postcopy.md` (title, caption, hashtags, pinned comment) + `epNN_qa.md` (checklist ticked with evidence).
