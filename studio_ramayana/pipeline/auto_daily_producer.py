"""
GROW10Z — Autonomous Daily Ramayana Studio Producer
Runs locally or completely headless in GitHub Actions CI/CD.
Finds the next unrendered episode, generates audio, builds kinetic captions,
draws high-detail Skia vector rigs, renders 60fps 1080x1920 video,
and prepares complete publishing packages.
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

from studio_ramayana.character_engine.ramayana_character_rigs import (
    draw_baal_ram,
    draw_maharaja_dasharatha,
    draw_shri_ram_warrior,
    draw_maharishi_vishwamitra,
    draw_tadaka
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

def get_next_episode(episodes):
    for ep in episodes:
        if ep.get("status") != "completed":
            return ep
    return None

def generate_devanagari_caption_pill(text, out_path, font_path=None):
    """Render a kinetic 3-5 word gold/crimson pill badge"""
    WIDTH = 920
    HEIGHT = 160
    surface = skia.Surface(WIDTH, HEIGHT)
    cv = surface.getCanvas()
    cv.clear(skia.ColorTRANSPARENT)

    # Rounded pill badge
    pill_rect = skia.Rect(10, 10, WIDTH - 10, HEIGHT - 10)
    bg_paint = skia.Paint(
        Color=skia.ColorSetARGB(220, 15, 10, 25),
        AntiAlias=True
    )
    cv.drawRoundRect(pill_rect, 35, 35, bg_paint)

    # Gold border
    border_paint = skia.Paint(
        Style=skia.Paint.kStroke_Style,
        StrokeWidth=4,
        Color=skia.ColorSetARGB(240, 245, 195, 65),
        AntiAlias=True
    )
    cv.drawRoundRect(pill_rect, 35, 35, border_paint)

    # Text Font
    font_file = None
    if font_path and os.path.exists(font_path):
        font_file = font_path
    elif (FONTS_DIR / "YatraOne-Regular.ttf").exists():
        font_file = str(FONTS_DIR / "YatraOne-Regular.ttf")
    elif os.path.exists("C:/Windows/Fonts/Nirmala.ttf"):
        font_file = "C:/Windows/Fonts/Nirmala.ttf"

    typeface = skia.Typeface.MakeFromFile(font_file) if font_file else skia.Typeface.MakeFromName("Arial", skia.FontStyle.Bold())
    font = skia.Font(typeface, 48)

    # Text Shadow & Fill
    shadow_paint = skia.Paint(Color=skia.ColorSetARGB(255, 10, 5, 15), AntiAlias=True)
    text_paint = skia.Paint(Color=skia.ColorSetARGB(255, 255, 245, 215), AntiAlias=True)

    # Center text
    blob = skia.TextBlob.MakeFromString(text, font)
    bounds = font.measureText(text)
    tx = (WIDTH - bounds) / 2.0
    ty = 100

    cv.drawString(text, tx + 3, ty + 3, font, shadow_paint)
    cv.drawString(text, tx, ty, font, text_paint)

    img = surface.makeImageSnapshot()
    img.save(str(out_path), skia.kPNG)

def generate_drone_audio(duration, out_wav):
    """Synthesize D-major Tanpura drone + bells audio"""
    sr = 44100
    t = np.linspace(0, duration, int(sr * duration), False)
    # Fundamental D2 (73.4 Hz) + Harmonics
    d2 = 73.42
    drone = (
        0.35 * np.sin(2 * np.pi * d2 * t) +
        0.25 * np.sin(2 * np.pi * (d2 * 1.5) * t) +
        0.18 * np.sin(2 * np.pi * (d2 * 2.0) * t) +
        0.12 * np.sin(2 * np.pi * (d2 * 3.0) * t)
    )
    # Slow gentle amplitude modulation
    mod = 0.8 + 0.2 * np.sin(2 * np.pi * 0.25 * t)
    drone = drone * mod

    # Bell chime every 6 seconds
    for chime_t in np.arange(1.0, duration - 2.0, 6.0):
        idx = int(chime_t * sr)
        dur_bell = min(int(3.0 * sr), len(t) - idx)
        tb = np.linspace(0, 3.0, dur_bell, False)
        bell = 0.25 * np.sin(2 * np.pi * 880 * tb) * np.exp(-1.5 * tb)
        drone[idx:idx+dur_bell] += bell

    # Normalization & write
    drone = np.clip(drone, -0.95, 0.95)
    sf.write(str(out_wav), drone.astype(np.float32), sr)

def render_episode(ep_data):
    ep_id = ep_data["id"]
    title = ep_data["title"]
    print(f"==================================================")
    print(f"🎬 Producing {ep_id}: {title}")
    print(f"==================================================")

    ep_dir = BASE_DIR / "studio_ramayana" / "episodes" / ep_id.lower()
    ep_dir.mkdir(parents=True, exist_ok=True)
    captions_dir = ep_dir / "captions_v2"
    captions_dir.mkdir(parents=True, exist_ok=True)

    # 1. Prepare Script & Timings
    lines = ep_data.get("script_lines", [])
    if not lines:
        # Default dramatic script lines if not provided
        lines = [
            {"speaker": "narrator", "text": f"{ep_id}: {title}"},
            {"speaker": "narrator", "text": "अयोध्या के पावन प्रांगण में जब महर्षि विश्वामित्र पधारे..."},
            {"speaker": "vishwamitra", "text": "राजन! यज्ञ की रक्षा हेतु मुझे राम और लक्ष्मण चाहिए!"},
            {"speaker": "dasharatha", "text": "मुनिवर! मेरे प्राण ले लीजिए, पर मेरे राम को न मांगिए!"},
            {"speaker": "narrator", "text": "किंतु यह तो अधर्म के अंत और मर्यादा की स्थापना का प्रारंभ था।"},
            {"speaker": "narrator", "text": "प्रभु श्रीराम ने अपने धनुष की प्रत्यंचा खींची..."},
            {"speaker": "narrator", "text": "अगले भाग में देखिए: ताड़का वध और महा-पराक्रम!"}
        ]

    # Assign timing chunks
    duration = 40.0
    chunk_dur = duration / len(lines)
    caption_events = []
    for i, line in enumerate(lines):
        t_start = i * chunk_dur
        t_end = (i + 1) * chunk_dur
        pill_path = captions_dir / f"chunk_{i:02d}.png"
        generate_devanagari_caption_pill(line["text"][:38], pill_path)
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

    # 2. Generate Audio
    final_audio_path = ep_dir / "audio_master.wav"
    generate_drone_audio(duration, final_audio_path)

    # 3. Setup Video Pipeline (1080x1920 @ 60fps)
    W, H = 1080, 1920
    fps = 60
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
        "-crf", "19",
        str(temp_video)
    ]

    pipe = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

    # Pre-load caption skia images
    cap_images = []
    for event in caption_events:
        data = skia.Data.MakeFromFileName(event["img_path"])
        cap_images.append(skia.Image.MakeFromEncoded(data) if data else None)

    # Render Frames
    print(f"Rendering {total_frames} frames at {fps} fps...")
    surface = skia.Surface(W, H)
    canvas = surface.getCanvas()

    # Pre-generate floating particles
    np.random.seed(42)
    particles = [{"x": random.randint(50, W-50), "y": random.randint(100, H-100), "speed": random.uniform(1.2, 3.5), "r": random.uniform(3, 8)} for _ in range(35)]

    for frame_idx in range(total_frames):
        t_sec = frame_idx / fps
        canvas.clear(skia.ColorSetARGB(255, 14, 18, 30))

        # Dynamic Mythological Sky Background
        sky_p = skia.Paint(
            Shader=skia.GradientShader.MakeLinear(
                [skia.Point(0, 0), skia.Point(0, H)],
                [skia.ColorSetARGB(255, 25, 15, 45), skia.ColorSetARGB(255, 80, 40, 25), skia.ColorSetARGB(255, 20, 12, 30)],
                [0.0, 0.65, 1.0]
            )
        )
        canvas.drawRect(skia.Rect(0, 0, W, H), sky_p)

        # Temple & Palace Silhouettes
        temple_paint = skia.Paint(Color=skia.ColorSetARGB(180, 30, 20, 40), AntiAlias=True)
        # Spires
        for tx in [180, 540, 900]:
            p = skia.Path()
            p.moveTo(tx - 120, H - 350)
            p.lineTo(tx, H - 750)
            p.lineTo(tx + 120, H - 350)
            p.close()
            canvas.drawPath(p, temple_paint)

        # Character Staging based on script beat
        active_speaker = "narrator"
        for ev in caption_events:
            if ev["start"] <= t_sec < ev["end"]:
                active_speaker = ev["speaker"]
                break

        # Breathing subtle motion
        breath = 1.0 + 0.015 * math.sin(t_sec * 3.5)

        if ep_id == "EP001":
            # Baal Ram & Dasharatha
            draw_baal_ram(canvas, 540, 1020, scale=1.9 * breath, rock_angle=2.5 * math.sin(t_sec * 2.0))
            draw_maharaja_dasharatha(canvas, 230, 1280, scale=1.35)
        elif ep_id == "EP002":
            # Vishwamitra & Shri Ram warrior
            draw_maharishi_vishwamitra(canvas, 320, 1060, scale=1.6 * breath)
            draw_shri_ram_warrior(canvas, 760, 1080, scale=1.55 * breath)
        elif ep_id == "EP003":
            # Shri Ram Warrior facing Tadaka
            draw_shri_ram_warrior(canvas, 320, 1100, scale=1.55 * breath)
            draw_tadaka(canvas, 780, 1020, scale=1.65)
        else:
            # Universal Divine Ram Durbar Staging
            draw_shri_ram_warrior(canvas, 540, 1060, scale=1.75 * breath)

        # Golden Floating Dust Particles
        for pt in particles:
            py = (pt["y"] - pt["speed"] * frame_idx * 0.7) % H
            canvas.drawCircle(pt["x"], py, pt["r"], skia.Paint(Color=skia.ColorSetARGB(180, 255, 230, 120), AntiAlias=True))

        # Kinetic Caption Overlay
        for i, ev in enumerate(caption_events):
            if ev["start"] <= t_sec < ev["end"]:
                img = cap_images[i]
                if img:
                    # Pop-in scaling
                    elapsed = t_sec - ev["start"]
                    scale_c = min(1.0, elapsed * 6.0) if elapsed < 0.18 else 1.0
                    canvas.save()
                    canvas.translate(W / 2.0, H - 380)
                    canvas.scale(scale_c, scale_c)
                    canvas.drawImage(img, -img.width() / 2.0, -img.height() / 2.0)
                    canvas.restore()
                break

        # Header Watermark
        header_p = skia.Paint(Color=skia.ColorSetARGB(220, 255, 215, 0), AntiAlias=True)
        h_font = skia.Font(skia.Typeface.MakeFromName("Arial", skia.FontStyle.Bold()), 38)
        canvas.drawString("GROW10Z • सम्पूर्ण रामायण", 80, 120, h_font, header_p)

        # Pipe frame
        img = surface.makeImageSnapshot()
        pipe.stdin.write(img.tobytes())

        if frame_idx % 300 == 0:
            print(f"Progress: {frame_idx}/{total_frames} frames ({frame_idx/total_frames*100:.1f}%)")

    pipe.stdin.close()
    pipe.wait()

    # Mux Audio
    print("Muxing audio track...")
    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(temp_video),
        "-i", str(final_audio_path),
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(final_video)
    ], check=True)

    # Copy to UPLOAD_READY_VIDEOS
    dest_video = UPLOAD_DIR / f"RAMAYANA_{ep_id}_{title.replace(' ', '_').replace('—', '_')}.mp4"
    if dest_video.exists():
        dest_video.unlink()
    import shutil
    shutil.copy2(str(final_video), str(dest_video))

    # Generate Title Caption file
    postcopy_file = UPLOAD_DIR / f"RAMAYANA_{ep_id}_Title_Caption.txt"
    post_content = f"""# GROW10Z — रामायण: {ep_id}
## "{title}"

## Title (YouTube Shorts / Instagram Reels)
{ep_data.get('hook', title)} 🚩 #GROW10Z #रामायण #{ep_id}

## Caption (Description)
{lines[0]['text']}
{lines[1]['text']}
मर्यादा पुरुषोत्तम भगवान श्रीराम की अमर गाथा का अलौकिक प्रसंग।

#श्रीराम #रामायण #अयोध्या #Ramayan #ShriRam #AyodhyaDham #SanatanDharma #IndianMythology #GROW10Z #DivineAnimation

## Pinned Comment
👇 "जय श्री राम" लिखकर प्रभु की लीला का स्वागत करें! 🚩 (अगला भाग जल्द आ रहा है!)

## Source Reference
{ep_data.get('source', 'वाल्मीकि रामायण एवं रामचरितमानस')}
"""
    with open(postcopy_file, "w", encoding="utf-8") as f:
        f.write(post_content)

    # Update database
    ep_data["status"] = "completed"
    ep_data["render_date"] = "automated_daily"
    ep_data["output_file"] = str(dest_video.name)
    save_episodes(load_episodes())

    print(f"🎉 SUCCESS! {ep_id} rendered and delivered to: {dest_video}")
    return dest_video

if __name__ == "__main__":
    episodes = load_episodes()
    target_ep = None
    if len(sys.argv) > 1:
        req_id = sys.argv[1].upper()
        for ep in episodes:
            if ep["id"] == req_id:
                target_ep = ep
                break
    else:
        target_ep = get_next_episode(episodes)

    if not target_ep:
        print("All episodes in database are already completed!")
        sys.exit(0)

    render_episode(target_ep)
