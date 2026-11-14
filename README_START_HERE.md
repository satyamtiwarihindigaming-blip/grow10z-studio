# Antigravity pack — "आख़िरी बस" Hindi 2D story shorts (code-made videos)

## 1) Install karna hai (sab free)
| Cheez | Kaise |
|---|---|
| Google Antigravity | antigravity.google se download (plan/limits khud check karo) |
| Python 3.12, ffmpeg, Git | Windows: `.\setup_windows.ps1` (winget). Mac/Linux: `sh setup_mac_linux.sh` |
| pip packages | `requirements.txt` (kokoro-onnx, soundfile, numpy, scipy, pillow, skia-python, pymunk, pedalboard, imageio-ffmpeg) + `tinysoundfont` (`--no-deps`) |
| Hindi voice model (GitHub) | Kokoro `kokoro-v1.0.onnx` + `voices-v1.0.bin` (setup script khud download karta hai) |
| Soundfont music (GitHub) | GeneralUser GS `.sf2` (setup script download karta hai) |
| libraqm (Hindi text shaping) | Linux: `apt install libraqm0`; check: `python check_env.py` |
| Optional | Blender (3D shots), Playwright+Chromium (agar Pillow raqm False ho) |

## 2) Antigravity me chalana
1. Is folder ko **workspace** ki tarah kholo. `.agents/` (aur `.agent/`, dono rakhe hain taaki jo bhi version ho wo skills utha le) me AGENTS.md aur 9 skills hain.
2. `MASTER_PROMPT.md` ka poora text agent chat me paste karo.
3. Har gate (G1–G5) pe agent rukega. Tum "ok" ya correction bhejo.

## 3) GitHub se aur free skills (agent ko bol sakte ho)
- `https://github.com/anthropics/skills` — skills ka public repo (skill-creator, canvas-design, algorithmic-art, slack-gif-creator, webapp-testing, ...). `git clone --depth 1` karke jo chahiye wo folder `.agents/skills/` me copy karo. **Har skill ki LICENSE alag ho sakti hai — copy karne se pehle check karo.**
- `https://github.com/remotion-dev/skills` — Remotion (React se video) ka skill. Optional alternative route; Remotion ki licence shartein khud check karo.
- Apni skills banane ke liye `skill-creator` skill use karo.

## 4) Seedhi baatein
- Is pack me **9 skills mere likhe hain**, specific is story project ke liye. Tumhari "Guruji Motors 200 skill studio" ki skills maine isme nahi daali: wo ek jaise template hain aur Guruji Motors ke naam se bandhi hain. Chaho to alag se kuch dalwa lo.
- Antigravity ka agent kya kar paayega ye uske plan/limits aur tumhare PC pe nirbhar hai; yahan maine jo kuch test kiya wo mere sandbox me chala (check_env, SFX library, voice FX, voice comparison, style frame). Windows pe chalaya nahi.
- Voice standard Hindi AI voice hai (Shekhawati/lehja nahi). Hindi text khud proofread karna.
- Output quality tab hi aayegi jab har gate pe tum dekhoge/sunoge.

## 5) Files
`MASTER_PROMPT.md` · `.agents/` · `project/` (story bible, ep01 script/storyboard/shotlist, assets: style frame + voice sample) · `reference_code/` (SFX synth, voice FX, skia style frame, music mix, character engine reference) · `check_env.py` · setup scripts · `fonts/`.
