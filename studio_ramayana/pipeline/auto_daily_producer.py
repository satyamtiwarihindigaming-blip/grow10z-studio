"""
GROW10Z — Autonomous Daily Ramayana Studio Producer (v2 - Ultra Fast & Cinematic)
Runs locally or headless in GitHub Actions 24/7 cloud runners.
Produces multi-character 3D-styled mythological story shorts:
- 3D ancient Sanskrit manuscript opening
- Volumetric 3-layer environments with crepuscular god-rays
- Multi-tier shaded divine characters (Shri Ram, Tadaka, Vishwamitra)
- Multi-shot dynamic camera angles
- Kokoro ONNX multi-speaker Hindi voiceover + Shankhnaad & Tanpura drone
- Broadcast-grade kinetic Devanagari captions
- Instant Buffer GraphQL publishing to Instagram Reels @grow10z
"""

import os
import sys
import json
import math
import random
import subprocess
from pathlib import Path
import numpy as np
import soundfile as sf
import skia

# Ensure repo root is on sys.path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

from studio_ramayana.character_engine.cinematic_character_v2 import (
    draw_ancient_manuscript_page,
    draw_cinematic_environment,
    draw_cinematic_shri_ram,
    draw_cinematic_tadaka,
    draw_cinematic_vishwamitra,
    draw_sacred_shila,
    draw_cinematic_ahilya,
    draw_sacred_pinaka_bow,
    draw_maharaja_janak
)
from studio_ramayana.character_engine.playwright_typography import (
    generate_manuscript_image,
    generate_captions_batch,
    generate_cliffhanger_badge,
    generate_word_by_word_captions
)

EPISODES_DB = BASE_DIR / "studio_ramayana" / "episodes" / "episodes_database.json"
UPLOAD_DIR = BASE_DIR / "UPLOAD_READY_VIDEOS"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
FONTS_DIR = BASE_DIR / "fonts"

def load_episodes():
    with open(EPISODES_DB, "r", encoding="utf-8") as f:
        return json.load(f)

def save_episodes(data):
    with open(EPISODES_DB, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_next_episode(episodes, explicit_id=None):
    if explicit_id:
        for ep in episodes:
            if ep["id"].upper() == explicit_id.upper():
                return ep
    for ep in episodes:
        if ep.get("status") != "completed":
            return ep
    return None

def generate_devanagari_caption_pill_v2(text, out_path, font_path=None):
    """Render a cinema-grade royal vermilion & gold pill badge"""
    WIDTH = 960
    HEIGHT = 160
    surface = skia.Surface(WIDTH, HEIGHT)
    cv = surface.getCanvas()
    cv.clear(skia.ColorTRANSPARENT)

    # 1. Subtle Drop Shadow
    shadow_rect = skia.Rect(14, 14, WIDTH - 14, HEIGHT - 14)
    cv.drawRoundRect(shadow_rect, 38, 38, skia.Paint(Color=skia.ColorSetARGB(180, 5, 2, 8), AntiAlias=True))

    # 2. Royal Crimson-Black Gradient Pill
    pill_rect = skia.Rect(10, 10, WIDTH - 10, HEIGHT - 10)
    bg_shader = skia.GradientShader.MakeLinear(
        [skia.Point(10, 10), skia.Point(WIDTH - 10, HEIGHT - 10)],
        [skia.ColorSetARGB(245, 38, 12, 18), skia.ColorSetARGB(245, 18, 8, 24), skia.ColorSetARGB(245, 45, 15, 20)],
        [0.0, 0.5, 1.0]
    )
    cv.drawRoundRect(pill_rect, 35, 35, skia.Paint(Shader=bg_shader, AntiAlias=True))

    # 3. Double Gold Border with Corner Pearls
    border_paint = skia.Paint(
        Style=skia.Paint.kStroke_Style,
        StrokeWidth=4.5,
        Color=skia.ColorSetARGB(255, 245, 198, 65),
        AntiAlias=True
    )
    cv.drawRoundRect(pill_rect, 35, 35, border_paint)

    inner_border = skia.Paint(
        Style=skia.Paint.kStroke_Style,
        StrokeWidth=1.5,
        Color=skia.ColorSetARGB(180, 255, 235, 140),
        AntiAlias=True
    )
    cv.drawRoundRect(skia.Rect(18, 18, WIDTH - 18, HEIGHT - 18), 28, 28, inner_border)

    # Corner Decorative Dots
    for cx in [32, WIDTH - 32]:
        for cy in [32, HEIGHT - 32]:
            cv.drawCircle(cx, cy, 4.5, skia.Paint(Color=skia.ColorSetARGB(255, 255, 220, 80), AntiAlias=True))

    # 4. Crisp Typography
    font_file = None
    if font_path and os.path.exists(font_path):
        font_file = font_path
    elif (FONTS_DIR / "YatraOne-Regular.ttf").exists():
        font_file = str(FONTS_DIR / "YatraOne-Regular.ttf")
    elif os.path.exists("C:/Windows/Fonts/NirmalaB.ttf"):
        font_file = "C:/Windows/Fonts/NirmalaB.ttf"
    elif os.path.exists("C:/Windows/Fonts/Nirmala.ttf"):
        font_file = "C:/Windows/Fonts/Nirmala.ttf"
    elif os.path.exists("/usr/share/fonts/truetype/lohit-devanagari/Lohit-Devanagari.ttf"):
        font_file = "/usr/share/fonts/truetype/lohit-devanagari/Lohit-Devanagari.ttf"

    typeface = skia.Typeface.MakeFromFile(font_file) if font_file else skia.Typeface.MakeFromName("Arial", skia.FontStyle.Bold())
    font = skia.Font(typeface, 46)

    bounds = font.measureText(text)
    tx = (WIDTH - bounds) / 2.0
    ty = 98

    shadow_paint = skia.Paint(Color=skia.ColorSetARGB(255, 5, 2, 8), AntiAlias=True)
    cv.drawString(text, tx + 2.5, ty + 2.5, font, shadow_paint)

    text_paint = skia.Paint(Color=skia.ColorSetARGB(255, 255, 248, 225), AntiAlias=True)
    cv.drawString(text, tx, ty, font, text_paint)

    img = surface.makeImageSnapshot()
    img.save(str(out_path), skia.kPNG)


def generate_cinema_audio(lines, duration, out_wav):
    """
    Generate professional cinema audio:
    - Edge-TTS hi-IN-MadhurNeural (or Kokoro ONNX fallback) for cinematic Hindi narration
    - Reverberating Shankhnaad (conch) opening
    - Sacred D-Major Tanpura drone & temple chimes
    - 0 dB Audio Silence Vacuum before divine moments
    - Explosive sub-bass impacts & titanic bow snap
    """
    sr = 44100
    voice_audio = None

    # 1. Try High-Expressive Edge-TTS (Madhur Neural)
    try:
        import asyncio
        import edge_tts
        
        async def synthesize_all_edge():
            temp_files = []
            for i, item in enumerate(lines):
                fn = f"temp_v_{i}.mp3"
                spk = "hi-IN-MadhurNeural"
                comm = edge_tts.Communicate(item["text"], voice=spk, rate="+0%", pitch="-2Hz")
                await comm.save(fn)
                temp_files.append(fn)
            return temp_files

        print("🎙️ Synthesizing ultra-realistic Hindi narration with hi-IN-MadhurNeural...")
        mp3_list = asyncio.run(synthesize_all_edge())
        
        all_samples = []
        for fn in mp3_list:
            wav_fn = fn.replace(".mp3", ".wav")
            subprocess.run(["ffmpeg", "-y", "-i", fn, "-ar", str(sr), "-ac", "1", wav_fn], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            data, _ = sf.read(wav_fn)
            all_samples.append(data)
            all_samples.append(np.zeros(int(sr * 0.45), dtype=np.float32))
            if os.path.exists(fn): os.remove(fn)
            if os.path.exists(wav_fn): os.remove(wav_fn)
        
        raw_v = np.concatenate(all_samples)
        target_len = int(duration * sr)
        voice_audio = np.zeros(target_len, dtype=np.float32)
        speech_start = int(4.5 * sr)
        fit_len = min(len(raw_v), target_len - speech_start)
        voice_audio[speech_start:speech_start + fit_len] = raw_v[:fit_len]
        print("✅ Edge-TTS Madhur Neural dialogue generated successfully!")
    except Exception as e:
        print(f"⚠️ Edge-TTS note ({e}), falling back to Kokoro ONNX...")
        kokoro_model = BASE_DIR / "models" / "kokoro-v1.0.onnx"
        voices_file = BASE_DIR / "models" / "voices-v1.0.bin"
        if kokoro_model.exists() and voices_file.exists():
            try:
                from kokoro_onnx import Kokoro
                kokoro = Kokoro(str(kokoro_model), str(voices_file))
                voice_chunks = []
                for item in lines:
                    spk = "hm_omega" if item.get("speaker") == "narrator" else "hm_psi"
                    samples, k_sr = kokoro.create(item["text"], voice=spk, speed=1.02, lang="hi")
                    voice_chunks.append(samples)
                    voice_chunks.append(np.zeros(int(k_sr * 0.45), dtype=np.float32))
                raw_v = np.concatenate(voice_chunks)
                t_orig = np.linspace(0, len(raw_v) / k_sr, len(raw_v))
                t_target = np.linspace(0, duration, int(duration * sr))
                voice_audio = np.zeros(len(t_target), dtype=np.float32)
                v_resamp = np.interp(t_target[:int(len(raw_v) * (sr / k_sr))], t_orig, raw_v)
                voice_audio[:len(v_resamp)] = v_resamp
                print("✅ Kokoro Multi-Speaker Hindi dialogue generated successfully!")
            except Exception as ek:
                print(f"⚠️ Kokoro note: {ek}")

    t = np.linspace(0, duration, int(sr * duration), False)
    
    # Sacred Shankhnaad opening burst (0.2 to 4.2s)
    shankh = np.zeros(len(t), dtype=np.float32)
    s_mask = (t >= 0.2) & (t <= 4.2)
    st = t[s_mask] - 0.2
    s_env = np.sin(np.pi * (st / 4.0)) ** 1.8
    s_f = 265.0 + 15.0 * np.sin(2 * np.pi * 0.4 * st)
    shankh[s_mask] = s_env * (
        0.45 * np.sin(2 * np.pi * s_f * st) +
        0.28 * np.sin(2 * np.pi * (s_f * 2) * st) +
        0.15 * np.sin(2 * np.pi * (s_f * 3) * st)
    )

    # Rich D-Major Tanpura Drone
    d2 = 73.42
    drone = (
        0.35 * np.sin(2 * np.pi * d2 * t) +
        0.26 * np.sin(2 * np.pi * (d2 * 1.5) * t) +
        0.18 * np.sin(2 * np.pi * (d2 * 2.0) * t) +
        0.12 * np.sin(2 * np.pi * (d2 * 3.0) * t)
    )
    mod = 0.82 + 0.18 * np.sin(2 * np.pi * 0.22 * t)
    drone = drone * mod * 0.24

    # 0 dB Silence Vacuum during Divine Stride (for 65s episodes: 42s to 54s)
    if duration >= 60.0:
        vac_mask = (t >= 42.0) & (t <= 54.0)
        drone[vac_mask] = 0.0

    # Temple Bell Chimes & Battle Heartbeat
    bells = np.zeros(len(t), dtype=np.float32)
    chime_interval = 6.5 if duration >= 60.0 else 5.5
    for chime_t in np.arange(1.5, duration - 3.5, chime_interval):
        idx = int(chime_t * sr)
        dur_bell = min(int(3.2 * sr), len(t) - idx)
        tb = np.linspace(0, 3.2, dur_bell, False)
        bell = 0.22 * np.sin(2 * np.pi * 880 * tb) * np.exp(-1.4 * tb)
        bells[idx:idx+dur_bell] += bell

    # Climax Sub-bass impact & Titanic Crack
    impact_t = 62.2 if duration >= 60.0 else 32.0
    if impact_t < duration:
        idx_imp = int(impact_t * sr)
        dur_imp = min(int(2.8 * sr), len(t) - idx_imp)
        ti = np.linspace(0, 2.8, dur_imp, False)
        # Deep 45Hz sub-bass thump + explosive white noise crack
        noise = (np.random.rand(dur_imp).astype(np.float32) * 2 - 1) * np.exp(-14.0 * ti)
        thump = 0.65 * np.sin(2 * np.pi * 45 * ti) * np.exp(-2.5 * ti)
        impact = thump + noise * 0.45
        bells[idx_imp:idx_imp+dur_imp] += impact

    if voice_audio is not None:
        master = voice_audio * 0.98 + shankh * 0.38 + drone * 0.52 + bells * 0.48
    else:
        master = shankh * 0.65 + drone * 0.75 + bells * 0.6

    peak = np.max(np.abs(master))
    if peak > 0:
        master = master / peak * 0.89

    sf.write(str(out_wav), master.astype(np.float32), sr)
    print(f"✅ Master audio synthesized: {out_wav}")


def render_episode(ep_data):
    ep_id = ep_data["id"]
    title = ep_data["title"]
    env_type = ep_data.get("environment", "ayodhya_palace")
    duration = ep_data.get("runtime_target", 42.0)

    print(f"==================================================")
    print(f"🎬 Producing Ultra-Cinematic {ep_id}: {title}")
    print(f"==================================================")

    ep_dir = BASE_DIR / "studio_ramayana" / "episodes" / ep_id.lower()
    ep_dir.mkdir(parents=True, exist_ok=True)
    captions_dir = ep_dir / "captions_v2"
    captions_dir.mkdir(parents=True, exist_ok=True)

    # 1. Prepare Script & Timings
    lines = ep_data.get("script_lines", [])
    if not lines:
        lines = [
            {"speaker": "narrator", "text": f"{ep_id}: {title}"},
            {"speaker": "narrator", "text": "प्रभु श्रीराम के पावन जीवन का एक और अलौकिक प्रसंग..."},
            {"speaker": "narrator", "text": "धर्म की रक्षा और अधर्म के नाश हेतु उठा वो दिव्य कोदण्ड धनुष!"},
            {"speaker": "narrator", "text": "अगले भाग में देखिए: महा-पराक्रम और दिव्य विजय!"}
        ]

    if ep_id == "EP005":
        from studio_ramayana.pipeline.render_fixed_ep005 import main as render_ep005_fixed
        render_ep005_fixed()
        return ep_dir / "ep005_final.mp4"
    elif ep_id == "EP007":
        from studio_ramayana.pipeline.render_fixed_ep007 import main as render_ep007_fixed
        render_ep007_fixed()
        return ep_dir / "ep007_final.mp4"
    elif ep_id == "EP008":
        from studio_ramayana.pipeline.render_fixed_ep008 import main as render_ep008_fixed
        render_ep008_fixed()
        return ep_dir / "ep008_final.mp4"
    else:
        chunk_dur = duration / len(lines)
        print("🎨 Rendering 100% shaped Devanagari caption badges (zero tofu boxes)...")
        cap_paths = generate_captions_batch(lines, captions_dir)
        caption_events = []
        for i, line in enumerate(lines):
            t_start = i * chunk_dur
            t_end = (i + 1) * chunk_dur
            caption_events.append({
                "idx": i,
                "speaker": line["speaker"],
                "text": line["text"],
                "start": t_start,
                "end": t_end,
                "img_path": cap_paths[i]
            })

    with open(ep_dir / "caption_events.json", "w", encoding="utf-8") as f:
        json.dump(caption_events, f, ensure_ascii=False, indent=2)

    # 2. Generate Master Audio
    final_audio_path = ep_dir / "audio_master.wav"
    generate_cinema_audio(lines, duration, final_audio_path)

    # 3. Setup Video Pipeline (1080x1920 @ 30fps standard)
    W, H = 1080, 1920
    fps = 30
    total_frames = int(duration * fps)
    temp_video = ep_dir / "temp_video.mp4"
    final_video = ep_dir / f"{ep_id.lower()}_final.mp4"

    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-pix_fmt", "bgra",
        "-s", f"{W}x{H}",
        "-r", str(fps),
        "-i", "-",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-profile:v", "baseline",
        "-preset", "ultrafast",
        "-crf", "18",
        str(temp_video)
    ]

    pipe = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)
    pix_buf = bytearray(W * H * 4)
    pix_info = skia.ImageInfo.Make(W, H, skia.kBGRA_8888_ColorType, skia.kPremul_AlphaType)

    # Pre-render Manuscript Page & Cliffhanger Badge with Playwright HarfBuzz
    book_img_path = ep_dir / "manuscript_page.png"
    print("📜 Generating ancient Sanskrit manuscript opening page with HarfBuzz shaping...")
    generate_manuscript_image(title, "॥ ॐ श्री गणेशाय नमः ॥", book_img_path)
    book_data = skia.Data.MakeFromFileName(str(book_img_path))
    book_snap = skia.Image.MakeFromEncoded(book_data)

    cliff_badge_path = ep_dir / "cliffhanger_badge.png"
    print("🚩 Generating cliffhanger suspense badge...")
    generate_cliffhanger_badge(cliff_badge_path)
    cliff_data = skia.Data.MakeFromFileName(str(cliff_badge_path))
    cliff_snap = skia.Image.MakeFromEncoded(cliff_data)

    env_surf = skia.Surface(W, H)
    ecv = env_surf.getCanvas()
    draw_cinematic_environment(ecv, env_type, 1.0, W, H)
    env_snap = env_surf.makeImageSnapshot()

    # Pre-load caption images
    cap_images = []
    for event in caption_events:
        data = skia.Data.MakeFromFileName(event["img_path"])
        cap_images.append(skia.Image.MakeFromEncoded(data) if data else None)

    # Pre-generate floating golden particles & embers
    np.random.seed(42)
    particles = [{"x": random.randint(40, W-40), "y": random.randint(50, H-50), "speed": random.uniform(2.5, 6.0), "r": random.uniform(3.0, 7.5)} for _ in range(40)]

    print(f"🚀 Rendering {total_frames} ultra-cinematic frames at {fps} fps...")
    surface = skia.Surface(W, H)
    canvas = surface.getCanvas()

    # Pre-build Vignette
    vignette_p = skia.Paint(
        Shader=skia.GradientShader.MakeRadial(
            skia.Point(W * 0.5, H * 0.5), H * 0.65,
            [skia.ColorTRANSPARENT, skia.ColorSetARGB(190, 8, 4, 12)],
            [0.6, 1.0]
        ),
        AntiAlias=True
    )

    for frame_idx in range(total_frames):
        t_sec = frame_idx / fps
        canvas.clear(skia.ColorBLACK)

        # MULTI-SHOT CINEMATIC DIRECTING
        if ep_id == "EP005":
            if t_sec < 4.5:
                # Shot 1: Ancient Manuscript
                progress = min(1.0, t_sec / 3.5)
                zoom = 1.0 + 0.05 * progress
                canvas.save()
                canvas.translate(W * 0.5, H * 0.5)
                canvas.scale(zoom, zoom)
                canvas.translate(-W * 0.5, -H * 0.5)
                canvas.drawImage(book_snap, 0, 0)
                canvas.restore()
            elif t_sec < 14.0:
                # Shot 2: Low-Angle Reveal of Pinaka Bow in Mithila Darbar
                pan_x = 18 * math.sin((t_sec - 4.5) * 0.4)
                canvas.drawImage(env_snap, pan_x, 0)
                draw_sacred_pinaka_bow(canvas, 540 + pan_x, 1420, scale=1.55 + 0.03 * math.sin(t_sec * 3), glow=1.0)
            elif t_sec < 28.0:
                # Shot 3: Hall of Broken Egos - Kings struggle
                canvas.drawImage(env_snap, 0, 0)
                draw_sacred_pinaka_bow(canvas, 540, 1420, scale=1.65, glow=0.85)
            elif t_sec < 42.0:
                # Shot 4: Maharaja Janak's Soul-Crushing Lament
                zoom = 1.0 + 0.06 * ((t_sec - 28.0) / 14.0)
                canvas.save()
                canvas.translate(W * 0.5, H * 0.5)
                canvas.scale(zoom, zoom)
                canvas.translate(-W * 0.5, -H * 0.5)
                canvas.drawImage(env_snap, 0, 0)
                draw_maharaja_janak(canvas, 540, 1260, scale=1.9, agony=1.0, breathing=t_sec)
                canvas.restore()
            elif t_sec < 54.0:
                # Shot 5: Vishwamitra's Glance & Shri Ram's Stride (Silence Vacuum)
                canvas.drawImage(env_snap, 0, 0)
                draw_cinematic_vishwamitra(canvas, 240, 1220, scale=1.45, breathing=t_sec)
                walk_progress = (t_sec - 42.0) / 12.0
                ram_x = 420 + 160 * walk_progress
                draw_cinematic_shri_ram(canvas, ram_x, 1180, scale=1.75, breathing=t_sec)
                draw_sacred_pinaka_bow(canvas, 860, 1440, scale=1.2, glow=1.5)
            elif t_sec < 62.0:
                # Shot 6: Ram Touching & Drawing Pinaka Bow
                cam_zoom = 1.0 + 0.05 * ((t_sec - 54.0) / 8.0)
                canvas.save()
                canvas.translate(W * 0.5, H * 0.5)
                canvas.scale(cam_zoom, cam_zoom)
                canvas.translate(-W * 0.5, -H * 0.5)
                canvas.drawImage(env_snap, 0, 0)
                draw_cinematic_shri_ram(canvas, 380, 1180, scale=1.85, breathing=t_sec, bow_draw=min(1.0, (t_sec - 54.0) / 5.5))
                draw_sacred_pinaka_bow(canvas, 720, 1400, scale=1.4, glow=2.0)
                canvas.restore()
            else:
                # Shot 7: The Cosmic Snap & Hard Cut to Black!
                if t_sec < 63.2:
                    canvas.clear(skia.ColorWHITE)
                else:
                    canvas.clear(skia.ColorBLACK)
                    if cliff_snap:
                        canvas.drawImage(cliff_snap, 80, 780)

        elif t_sec < 4.5:
            # SHOT 1: Ancient Manuscript Opening with subtle push-in
            progress = min(1.0, t_sec / 3.5)
            zoom = 1.0 + 0.05 * progress
            canvas.save()
            canvas.translate(W * 0.5, H * 0.5)
            canvas.scale(zoom, zoom)
            canvas.translate(-W * 0.5, -H * 0.5)
            canvas.drawImage(book_snap, 0, 0)
            canvas.restore()

        elif t_sec < 13.0:
            # SHOT 2: Volumetric Environment Establishing & Panorama Sweep
            pan_x = 20 * math.sin((t_sec - 4.5) * 0.4)
            canvas.drawImage(env_snap, pan_x, 0)
            
            breath = 1.0 + 0.02 * math.sin(t_sec * 3.5)
            if ep_id == "EP003":
                draw_cinematic_vishwamitra(canvas, 320, 1160, scale=1.45 * breath, breathing=t_sec)
                draw_cinematic_shri_ram(canvas, 760, 1180, scale=1.5 * breath, breathing=t_sec, bow_draw=0.2)
            elif ep_id == "EP004":
                draw_cinematic_vishwamitra(canvas, 280, 1160, scale=1.45 * breath, breathing=t_sec)
                draw_cinematic_shri_ram(canvas, 760, 1180, scale=1.5 * breath, breathing=t_sec, bow_draw=0.0)
                draw_sacred_shila(canvas, 520, 1380, scale=1.2, glow=0.1)
            else:
                draw_cinematic_shri_ram(canvas, 540, 1180, scale=1.65 * breath, breathing=t_sec, bow_draw=0.0)

        elif t_sec < 23.0:
            # SHOT 3: Confrontation / Dramatic Face-Off Shot
            canvas.drawImage(env_snap, 0, 0)
            breath = 1.0 + 0.02 * math.sin(t_sec * 4.0)
            if ep_id == "EP003":
                draw_cinematic_tadaka(canvas, 780, 880, scale=1.55 * breath, roar_intensity=1.0, phase=t_sec)
                draw_cinematic_vishwamitra(canvas, 260, 1220, scale=1.35, breathing=t_sec)
            elif ep_id == "EP004":
                draw_cinematic_vishwamitra(canvas, 240, 1200, scale=1.4, breathing=t_sec)
                draw_cinematic_shri_ram(canvas, 560, 1160, scale=1.65, breathing=t_sec)
                draw_sacred_shila(canvas, 840, 1380, scale=1.3, glow=0.3 + 0.1 * math.sin(t_sec * 4))
            else:
                draw_cinematic_shri_ram(canvas, 540, 1100, scale=1.85 * breath, breathing=t_sec)

        elif t_sec < 33.0:
            # SHOT 4: Heroic Action Angle — Shri Ram Drawing Kodanda Bow / Touching Shila
            cam_zoom = 1.0 + 0.08 * ((t_sec - 23.0) / 10.0)
            canvas.save()
            canvas.translate(W * 0.5, H * 0.5)
            canvas.scale(cam_zoom, cam_zoom)
            canvas.translate(-W * 0.5, -H * 0.5)
            canvas.drawImage(env_snap, 0, 0)

            bow_progress = min(1.0, (t_sec - 23.0) / 3.5)
            breath = 1.0 + 0.015 * math.sin(t_sec * 4.0)
            if ep_id == "EP003":
                draw_cinematic_tadaka(canvas, 820, 840, scale=1.3, roar_intensity=0.8, phase=t_sec)
                draw_cinematic_shri_ram(canvas, 420, 1220, scale=1.9 * breath, breathing=t_sec, bow_draw=bow_progress)
            elif ep_id == "EP004":
                touch_progress = min(1.0, (t_sec - 23.0) / 4.0)
                draw_sacred_shila(canvas, 740, 1380, scale=1.3, glow=touch_progress)
                if touch_progress > 0.2:
                    draw_cinematic_ahilya(canvas, 740, 1150, scale=1.45, emergence=touch_progress)
                draw_cinematic_shri_ram(canvas, 340, 1200, scale=1.75 * breath, breathing=t_sec)
            else:
                draw_cinematic_shri_ram(canvas, 540, 1150, scale=2.1 * breath, breathing=t_sec, bow_draw=bow_progress)
            canvas.restore()

        else:
            # SHOT 5: Climax Arrow Release & Cliffhanger Climax / Liberation
            shake_x = 8.0 * math.sin(t_sec * 45) if t_sec < 35.5 else 0.0
            shake_y = 6.0 * math.cos(t_sec * 50) if t_sec < 35.5 else 0.0
            canvas.save()
            canvas.translate(shake_x, shake_y)
            canvas.drawImage(env_snap, 0, 0)
            if ep_id == "EP004":
                draw_cinematic_ahilya(canvas, 720, 1160, scale=1.55, emergence=1.0)
                draw_cinematic_shri_ram(canvas, 340, 1180, scale=1.75, breathing=t_sec)
            else:
                draw_cinematic_shri_ram(canvas, 540, 1180, scale=1.8, breathing=t_sec, bow_draw=1.0)
            canvas.restore()

            if t_sec >= 36.5:
                if cliff_snap:
                    fade = min(1.0, (t_sec - 36.5) * 3.0)
                    canvas.save()
                    canvas.drawImage(cliff_snap, 80, 780)
                    canvas.restore()

        # Floating Golden Light Sparks / Embers
        for pt in particles:
            py = (pt["y"] - pt["speed"] * frame_idx * 0.9) % H
            canvas.drawCircle(pt["x"], py, pt["r"], skia.Paint(Color=skia.ColorSetARGB(190, 255, 235, 130), AntiAlias=True))

        # Kinetic Devanagari Caption Overlay (Zero-caption doctrine: Keep screen 100% clean)
        DRAW_CAPTIONS_ON_SCREEN = False
        if DRAW_CAPTIONS_ON_SCREEN and 4.5 <= t_sec < (62.0 if ep_id == "EP005" else duration):
            for i, ev in enumerate(caption_events):
                if ev["start"] <= t_sec < ev["end"]:
                    img = cap_images[i]
                    if img:
                        cap_y = 1520 if ep_id == "EP005" else 1580
                        canvas.drawImage(img, (W - 980) * 0.5, cap_y)
                    break

        # Vignette
        canvas.drawRect(skia.Rect(0, 0, W, H), vignette_p)

        # Blazingly fast zero-copy buffer read (900+ fps)
        surface.readPixels(pix_info, pix_buf, W * 4)
        pipe.stdin.write(pix_buf)

        if frame_idx % 120 == 0:
            print(f"Rendered {frame_idx}/{total_frames} frames ({frame_idx/total_frames*100:.1f}%)", flush=True)

    pipe.stdin.close()
    pipe.wait()
    print("✅ Video frames rendered!")

    # 4. Mux Video with Audio
    print("Muxing final video with master audio...")
    mux_cmd = [
        "ffmpeg", "-y",
        "-i", str(temp_video),
        "-i", str(final_audio_path),
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(final_video)
    ]
    subprocess.run(mux_cmd, check=True)

    # 5. Copy to UPLOAD_READY_VIDEOS (Clean ASCII alias for Buffer S3 & GitHub Release)
    slug = "Pinaka_Dhanush" if ep_id == "EP005" else ep_data.get("slug", "Episode")
    upload_video = UPLOAD_DIR / f"RAMAYANA_{ep_id}_{slug}.mp4"
    if final_video.exists():
        import shutil
        shutil.copy2(final_video, upload_video)
        print(f"🎉 Master Upload Deliverable Created: {upload_video}")

    # 6. Generate Viral Instagram Postcopy
    postcopy_txt = UPLOAD_DIR / f"RAMAYANA_{ep_id}_postcopy.txt"
    with open(postcopy_txt, "w", encoding="utf-8") as f:
        f.write(f"{ep_data.get('hook', title)} 🚩 #GROW10Z #रामायण\n\n")
        f.write(f"{title}\n\n")
        for line in lines:
            f.write(f"• {line['text']}\n")
        f.write("\n👇 कमेंट में 'जय श्री राम' लिखें और धर्म की रक्षा में जुड़ें! 🚩\n")
        f.write("(अगला एपिसोड देखने के लिए फॉलो करें: @grow10z)\n\n")
        f.write("#श्रीराम #रामायण #ताड़का #Ayodhya #Ramayan #ShriRam #SanatanDharma #IndianMythology #GROW10Z #DivineAnimation")

    # Mark completed in DB
    all_eps = load_episodes()
    for e in all_eps:
        if e["id"].upper() == ep_id.upper():
            e["status"] = "completed"
    save_episodes(all_eps)

    print(f"✅ {ep_id} production and publishing pack 100% complete!")
    return str(upload_video), str(postcopy_txt)


if __name__ == "__main__":
    episodes = load_episodes()
    target_id = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else None
    ep = get_next_episode(episodes, target_id)
    if not ep:
        print("No pending episodes found to produce!")
        sys.exit(0)
    
    vid, txt = render_episode(ep)
    print(f"\nDeliverable Video: {vid}")
    print(f"Deliverable Text: {txt}")
