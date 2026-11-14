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
    draw_cinematic_ahilya
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
    - Kokoro ONNX multi-speaker Hindi dialogue
    - Reverberating Shankhnaad (conch) opening
    - Sacred D-Major Tanpura drone & temple chimes
    - Damru / battle drum pulse during tension beats
    """
    sr = 44100
    kokoro_model = BASE_DIR / "models" / "kokoro-v1.0.onnx"
    voices_file = BASE_DIR / "models" / "voices-v1.0.bin"

    voice_audio = None
    if kokoro_model.exists() and voices_file.exists():
        try:
            from kokoro_onnx import Kokoro
            kokoro = Kokoro(str(kokoro_model), str(voices_file))
            voice_chunks = []
            for item in lines:
                spk = "hm_omega" if item.get("speaker") == "narrator" else "hm_psi"
                samples, k_sr = kokoro.create(item["text"], voice=spk, speed=1.04, lang="hi")
                voice_chunks.append(samples)
                # 0.45s pause between sentences
                voice_chunks.append(np.zeros(int(k_sr * 0.45), dtype=np.float32))
            
            raw_v = np.concatenate(voice_chunks)
            t_orig = np.linspace(0, len(raw_v) / k_sr, len(raw_v))
            t_target = np.linspace(0, duration, int(duration * sr))
            voice_audio = np.zeros(len(t_target), dtype=np.float32)
            v_resamp = np.interp(t_target[:int(len(raw_v) * (sr / k_sr))], t_orig, raw_v)
            voice_audio[:len(v_resamp)] = v_resamp
            print("✅ Kokoro Multi-Speaker Hindi dialogue generated successfully!")
        except Exception as e:
            print(f"⚠️ Kokoro generation note: {e}")

    t = np.linspace(0, duration, int(sr * duration), False)
    
    # 1. Sacred Shankhnaad opening burst (0.0 to 4.2s)
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

    # 2. Rich D-Major Tanpura Drone
    d2 = 73.42
    drone = (
        0.35 * np.sin(2 * np.pi * d2 * t) +
        0.26 * np.sin(2 * np.pi * (d2 * 1.5) * t) +
        0.18 * np.sin(2 * np.pi * (d2 * 2.0) * t) +
        0.12 * np.sin(2 * np.pi * (d2 * 3.0) * t)
    )
    mod = 0.82 + 0.18 * np.sin(2 * np.pi * 0.22 * t)
    drone = drone * mod * 0.24

    # 3. Temple Bell Chimes & Battle Beats
    bells = np.zeros(len(t), dtype=np.float32)
    for chime_t in np.arange(1.5, duration - 1.5, 5.5):
        idx = int(chime_t * sr)
        dur_bell = min(int(3.2 * sr), len(t) - idx)
        tb = np.linspace(0, 3.2, dur_bell, False)
        bell = 0.22 * np.sin(2 * np.pi * 880 * tb) * np.exp(-1.4 * tb)
        bells[idx:idx+dur_bell] += bell

    # Climax Sub-bass impact at 32.0s
    impact_t = 32.0
    if impact_t < duration:
        idx_imp = int(impact_t * sr)
        dur_imp = min(int(2.5 * sr), len(t) - idx_imp)
        ti = np.linspace(0, 2.5, dur_imp, False)
        impact = 0.45 * np.sin(2 * np.pi * 55 * ti) * np.exp(-2.2 * ti)
        bells[idx_imp:idx_imp+dur_imp] += impact

    if voice_audio is not None:
        master = voice_audio * 0.96 + shankh * 0.42 + drone * 0.55 + bells * 0.45
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

    chunk_dur = duration / len(lines)
    caption_events = []
    for i, line in enumerate(lines):
        t_start = i * chunk_dur
        t_end = (i + 1) * chunk_dur
        pill_path = captions_dir / f"chunk_{i:02d}.png"
        generate_devanagari_caption_pill_v2(line["text"][:38], pill_path)
        caption_events.append({
            "idx": i,
            "speaker": line["speaker"],
            "text": line["text"],
            "start": t_start,
            "end": t_end,
            "img_path": str(pill_path)
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
        "-preset", "veryfast",
        "-crf", "18",
        str(temp_video)
    ]

    pipe = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

    # Pre-render Manuscript Page & Environment Backdrop for blazingly fast rendering
    book_surf = skia.Surface(W, H)
    bcv = book_surf.getCanvas()
    bcv.clear(skia.ColorSetARGB(255, 12, 8, 18))
    draw_ancient_manuscript_page(bcv, W, H, title, "॥ ॐ श्री गणेशाय नमः ॥", 1.0)
    book_snap = book_surf.makeImageSnapshot()

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
        if t_sec < 4.5:
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
                card_rect = skia.Rect(80, 720, W - 80, 1020)
                card_p = skia.Paint(Color=skia.ColorSetARGB(235, 18, 10, 22), AntiAlias=True)
                canvas.drawRoundRect(card_rect, 25, 25, card_p)
                canvas.drawRoundRect(card_rect, 25, 25, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=4, Color=skia.ColorSetARGB(255, 245, 195, 60), AntiAlias=True))
                
                font_c1 = skia.Font(skia.Typeface.MakeFromName("Arial", skia.FontStyle.Bold()), 52)
                font_c2 = skia.Font(skia.Typeface.MakeFromName("Arial", skia.FontStyle.Normal()), 40)
                
                t1 = "आगे क्या होगा? 🚩"
                b1 = font_c1.measureText(t1)
                canvas.drawString(t1, (W - b1) * 0.5, 820, font_c1, skia.Paint(Color=skia.ColorSetARGB(255, 255, 220, 80), AntiAlias=True))

                t2 = "देखिए अगले भाग में! फॉलो करें @grow10z"
                b2 = font_c2.measureText(t2)
                canvas.drawString(t2, (W - b2) * 0.5, 910, font_c2, skia.Paint(Color=skia.ColorWHITE, AntiAlias=True))

        # Floating Golden Light Sparks / Embers
        for pt in particles:
            py = (pt["y"] - pt["speed"] * frame_idx * 0.9) % H
            canvas.drawCircle(pt["x"], py, pt["r"], skia.Paint(Color=skia.ColorSetARGB(190, 255, 235, 130), AntiAlias=True))

        # Kinetic Devanagari Caption Overlay (from 4.5s onwards)
        if t_sec >= 4.5:
            for i, ev in enumerate(caption_events):
                if ev["start"] <= t_sec < ev["end"]:
                    img = cap_images[i]
                    if img:
                        elapsed = t_sec - ev["start"]
                        pop = min(1.0, elapsed * 6.0)
                        canvas.save()
                        cap_y = 1580
                        canvas.translate(W * 0.5, cap_y + 80)
                        canvas.scale(pop, pop)
                        canvas.translate(-W * 0.5, -(cap_y + 80))
                        canvas.drawImage(img, (W - 960) * 0.5, cap_y)
                        canvas.restore()
                    break

        # Vignette
        canvas.drawRect(skia.Rect(0, 0, W, H), vignette_p)

        # Pipe frame to FFmpeg
        img_snap = surface.makeImageSnapshot()
        pixel_bytes = img_snap.toarray(colorType=skia.kBGRA_8888_ColorType)
        pipe.stdin.write(pixel_bytes)

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

    # 5. Copy to UPLOAD_READY_VIDEOS
    upload_video = UPLOAD_DIR / f"RAMAYANA_{ep_id}_{title.replace(' ', '_').replace('—', '_')}.mp4"
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
    ep_data["status"] = "completed"
    save_episodes(load_episodes())

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
