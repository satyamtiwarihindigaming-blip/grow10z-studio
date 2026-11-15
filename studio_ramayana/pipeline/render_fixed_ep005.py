"""
GROW10Z — Ultra-Cinematic 13-Shot Production Director for EP005 (The Divine Pinaka Bow)
100% Visual Directing Locked to Every Line:
- Shot 1 (0.0s - 2.2s): Fast Ancient Manuscript Opening
- Shot 2 (2.2s - 12.0s): Mithila Darbar & Divine Pinaka Bow Altar Reveal (Line 00 Hook)
- Shot 3 (12.0s - 19.3s): Colossal Pinaka Bow Macro / Golden Altar (Line 01 Pinaka Reveal)
- Shot 4 (19.3s - 25.8s): Mighty Kings Straining against Pedestal with Bronze Armor (Line 02)
- Shot 5 (25.8s - 33.2s): Immovable Pinaka Bow & Shattered King Egos (Line 03)
- Shot 6 (33.2s - 40.4s): Maharaja Janak Weeping in Royal Grief (Line 04)
- Shot 7 (40.4s - 47.8s): Janak's Agonized Heartbroken Lament (Line 05)
- Shot 8 (47.8s - 55.0s): Maharishi Vishwamitra Smiling Serenely (Line 06)
- Shot 9 (55.0s - 64.2s): Shri Ram Divine Stride in 0 dB Silence Vacuum (Line 07)
- Shot 10 (64.2s - 71.0s): Shri Ram Lifting Colossal Bow with One Hand (Line 08)
- Shot 11 (71.0s - 77.7s): Heroic Extreme Profile Close-up — Ram Pulling Bowstring to Ear (Line 09)
- Shot 12 (77.7s - 81.2s): Cosmic Lightning Explosion & Blinding Flash (Line 10 Thunder)
- Shot 13 (81.8s - 83.56s): Void Black Hard Cut + Gold Suspense Cliffhanger Badge
"""

import os
import sys
import json
import math
import random
import time
import subprocess
from pathlib import Path
import numpy as np
import skia

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

from studio_ramayana.character_engine.cinematic_character_v2 import (
    draw_cinematic_environment,
    draw_cinematic_shri_ram,
    draw_cinematic_vishwamitra,
    draw_sacred_pinaka_bow,
    draw_maharaja_janak,
    draw_mighty_kings_struggle,
    draw_ram_extreme_profile_pull,
    draw_cosmic_lightning_burst
)

EP_DIR = BASE_DIR / "studio_ramayana" / "episodes" / "ep005"
TIMELINE_FILE = EP_DIR / "timeline.json"
AUDIO_MASTER_FILE = EP_DIR / "audio_master.wav"

def make_snapshot(draw_fn, W=1080, H=1920):
    surf = skia.Surface(W, H)
    cv = surf.getCanvas()
    draw_fn(cv)
    return surf.makeImageSnapshot()

def main():
    print("==================================================")
    print("🎬 RENDERING 13-SHOT CINEMATIC MASTERPIECE (EP005)")
    print("==================================================")
    t_start_total = time.time()

    with open(TIMELINE_FILE, "r", encoding="utf-8") as f:
        timeline = json.load(f)

    total_duration = timeline[-1]["end"] + 2.4 # 83.56s
    fps = 30
    total_frames = int(total_duration * fps)
    W, H = 1080, 1920

    temp_video = EP_DIR / "temp_video_13shot.mp4"
    final_video = EP_DIR / "ep005_final.mp4"

    # 1. Preload Static Badges & Background
    print("📜 Preloading background, manuscript & badges...")
    book_snap = skia.Image.MakeFromEncoded(skia.Data.MakeFromFileName(str(EP_DIR / "manuscript_page.png")))
    cliff_snap = skia.Image.MakeFromEncoded(skia.Data.MakeFromFileName(str(EP_DIR / "cliffhanger_badge.png")))
    env_snap = make_snapshot(lambda cv: draw_cinematic_environment(cv, "mithila_darbar", 1.0, W, H))

    # Pre-render Vignette
    vig_paint = skia.Paint(
        Shader=skia.GradientShader.MakeRadial(
            skia.Point(W * 0.5, H * 0.5), H * 0.65,
            [skia.ColorTRANSPARENT, skia.ColorSetARGB(190, 8, 4, 12)],
            [0.6, 1.0]
        ),
        AntiAlias=True
    )
    vig_snap = make_snapshot(lambda cv: cv.drawRect(skia.Rect(0, 0, W, H), vig_paint))

    # 2. Pre-render 13 Distinct Cinematic Scene Snapshots
    print("🎨 Pre-rendering 13 distinct cinematic camera angles...")
    # Shot 2: Altar Bow
    bow_altar_snap = make_snapshot(lambda cv: draw_sacred_pinaka_bow(cv, 540, 1420, scale=1.55, glow=1.2))
    # Shot 3: Colossal Bow Close-up
    bow_macro_snap = make_snapshot(lambda cv: draw_sacred_pinaka_bow(cv, 540, 1380, scale=1.85, glow=1.5))
    # Shot 4: Mighty Kings Straining with Bronze Armor
    kings_strain_snap = make_snapshot(lambda cv: [
        draw_sacred_pinaka_bow(cv, 540, 1420, scale=1.50, glow=0.9),
        draw_mighty_kings_struggle(cv, 540, 1320, scale=1.55, strain=1.0)
    ])
    # Shot 5: Immovable Bow with Shockwaves
    bow_immovable_snap = make_snapshot(lambda cv: [
        draw_sacred_pinaka_bow(cv, 540, 1350, scale=1.95, glow=1.8)
    ])
    # Shot 6 & 7: Maharaja Janak Weeping
    janak_weep_snap = make_snapshot(lambda cv: draw_maharaja_janak(cv, 540, 1260, scale=1.9, agony=1.0, breathing=0.0))
    # Shot 8: Maharishi Vishwamitra Divine Smile
    vishwamitra_snap = make_snapshot(lambda cv: draw_cinematic_vishwamitra(cv, 540, 1200, scale=1.75, breathing=0.0))
    # Shot 9: Shri Ram Divine Stride
    ram_stride_snap = make_snapshot(lambda cv: draw_cinematic_shri_ram(cv, 540, 1180, scale=1.75, breathing=0.0, bow_draw=0.0))
    # Shot 10: Shri Ram Lifting Colossal Bow with One Hand
    ram_lift_snap = make_snapshot(lambda cv: [
        draw_cinematic_shri_ram(cv, 400, 1180, scale=1.80, breathing=0.0, bow_draw=0.0),
        draw_sacred_pinaka_bow(cv, 720, 1120, scale=1.50, glow=2.6)
    ])
    # Shot 11: Heroic Extreme Profile Close-up of Shri Ram Pulling Bowstring to Ear
    ram_profile_pull_snap = make_snapshot(lambda cv: draw_ram_extreme_profile_pull(cv, 540, 1020, scale=1.75, pull=1.0, spark=True))
    # Shot 12: Cosmic Lightning Burst
    lightning_burst_snap = make_snapshot(lambda cv: draw_cosmic_lightning_burst(cv, 540, 960, intensity=1.4, seed=77))

    # Floating Golden Embers
    np.random.seed(42)
    particles = [{"x": random.randint(40, W-40), "y": random.randint(50, H-50), "speed": random.uniform(2.5, 6.0), "r": random.uniform(3.0, 7.5)} for _ in range(40)]

    # 3. Setup FFmpeg Pipe
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
        "-threads", "0",
        str(temp_video)
    ]

    pipe = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)
    pix_buf = bytearray(W * H * 4)
    pix_info = skia.ImageInfo.Make(W, H, skia.kBGRA_8888_ColorType, skia.kPremul_AlphaType)

    surface = skia.Surface(W, H)
    canvas = surface.getCanvas()

    # Exact narrative scene timestamps
    t_s1 = timeline[0]["start"]   # 2.20s
    t_s2 = timeline[1]["start"]   # 12.22s
    t_s3 = timeline[2]["start"]   # 19.26s
    t_s4 = timeline[3]["start"]   # 25.84s
    t_s5 = timeline[4]["start"]   # 33.24s
    t_s6 = timeline[5]["start"]   # 40.38s
    t_s7 = timeline[6]["start"]   # 47.83s
    t_s8 = timeline[7]["start"]   # 54.97s
    t_s9 = timeline[8]["start"]   # 64.22s
    t_s10 = timeline[9]["start"]  # 71.04s
    t_s11 = timeline[10]["start"] # 77.73s
    t_s12 = timeline[10]["end"]   # 81.16s
    t_flash = t_s12 + 0.6         # 81.76s

    print(f"🚀 Streaming {total_frames} frames ({total_duration:.2f}s) of 13-shot dynamic action...")

    for frame_idx in range(total_frames):
        t_sec = frame_idx / fps
        canvas.clear(skia.ColorBLACK)

        # -------------------------------------------------------------
        # 13 DISTINCT CAMERA ANGLES & CINEMATIC COMPOSITIONS
        # -------------------------------------------------------------
        if t_sec < t_s1:
            # Shot 1 (0.0s - 2.2s): Ancient Sacred Manuscript Opening
            prog = min(1.0, t_sec / 2.0)
            zoom = 1.0 + 0.04 * prog
            canvas.save()
            canvas.translate(W * 0.5, H * 0.5)
            canvas.scale(zoom, zoom)
            canvas.translate(-W * 0.5, -H * 0.5)
            canvas.drawImage(book_snap, 0, 0)
            canvas.restore()

        elif t_sec < t_s2:
            # Shot 2 (2.2s - 12.2s): Mithila Darbar & Divine Pinaka Bow Altar Reveal (Line 00 Hook)
            # Camera: Slow dramatic pan with glowing golden atmosphere
            pan_x = 22 * math.sin((t_sec - t_s1) * 0.4)
            canvas.drawImage(env_snap, pan_x, 0)
            breath = 1.0 + 0.02 * math.sin(t_sec * 3.5)
            canvas.save()
            canvas.translate(540 + pan_x, 1420)
            canvas.scale(breath, breath)
            canvas.translate(-540, -1420)
            canvas.drawImage(bow_altar_snap, 0, 0)
            canvas.restore()

        elif t_sec < t_s3:
            # Shot 3 (12.2s - 19.3s): Colossal Pinaka Bow Macro / Golden Altar (Line 01 Pinaka Reveal)
            # Camera: Dramatic low-angle push-in on the sacred weapon of Shiva
            zoom = 1.0 + 0.06 * ((t_sec - t_s2) / (t_s3 - t_s2))
            canvas.save()
            canvas.translate(W * 0.5, H * 0.5)
            canvas.scale(zoom, zoom)
            canvas.translate(-W * 0.5, -H * 0.5)
            canvas.drawImage(env_snap, 0, 0)
            canvas.drawImage(bow_macro_snap, 0, 0)
            canvas.restore()

        elif t_sec < t_s4:
            # Shot 4 (19.3s - 25.8s): Mighty Kings Straining with Bronze Armor (Line 02 Kings Arrive)
            # Camera: Intense Dutch angle with heavy bronze armor strain and red anger aura
            shake_x = 3.0 * math.sin(t_sec * 25)
            canvas.save()
            canvas.translate(shake_x, 0)
            canvas.drawImage(env_snap, 0, 0)
            canvas.drawImage(kings_strain_snap, 0, 0)
            canvas.restore()

        elif t_sec < t_s5:
            # Shot 5 (25.8s - 33.2s): Immovable Pinaka Bow & Shattered King Egos (Line 03 Kings Fail)
            # Camera: Extreme upward perspective showing the bow immovable as Mount Kailash
            zoom = 1.0 + 0.05 * ((t_sec - t_s4) / (t_s5 - t_s4))
            canvas.save()
            canvas.translate(W * 0.5, H * 0.5)
            canvas.scale(zoom, zoom)
            canvas.translate(-W * 0.5, -H * 0.5)
            canvas.drawImage(env_snap, 0, 0)
            canvas.drawImage(bow_immovable_snap, 0, 0)
            canvas.restore()

        elif t_sec < t_s6:
            # Shot 6 (33.2s - 40.4s): Maharaja Janak Weeping in Royal Grief (Line 04 Janak Tears)
            # Camera: Royal portrait of Janak, tears glistening in candlelit palace shadows
            zoom = 1.0 + 0.06 * ((t_sec - t_s5) / (t_s6 - t_s5))
            breath = 1.0 + 0.015 * math.sin(t_sec * 3.0)
            canvas.save()
            canvas.translate(W * 0.5, H * 0.5)
            canvas.scale(zoom, zoom)
            canvas.translate(-W * 0.5, -H * 0.5)
            canvas.drawImage(env_snap, 0, 0)
            canvas.save()
            canvas.translate(540, 1260)
            canvas.scale(breath, breath)
            canvas.translate(-540, -1260)
            canvas.drawImage(janak_weep_snap, 0, 0)
            canvas.restore()
            canvas.restore()

        elif t_sec < t_s7:
            # Shot 7 (40.4s - 47.8s): Janak's Agonized Heartbroken Lament (Line 05 Janak Voice)
            # Camera: Deep emotional close-up on Janak raising his despair to the heavens
            zoom = 1.05 + 0.08 * ((t_sec - t_s6) / (t_s7 - t_s6))
            canvas.save()
            canvas.translate(W * 0.5, H * 0.5)
            canvas.scale(zoom, zoom)
            canvas.translate(-W * 0.5, -H * 0.5)
            canvas.drawImage(env_snap, 0, 0)
            canvas.drawImage(janak_weep_snap, 0, 0)
            canvas.restore()

        elif t_sec < t_s8:
            # Shot 8 (47.8s - 55.0s): Maharishi Vishwamitra Divine Serenity (Line 06 Vishwamitra Signal)
            # Camera: Golden aura close-up on Vishwamitra smiling knowingly and gesturing
            zoom = 1.0 + 0.05 * ((t_sec - t_s7) / (t_s8 - t_s7))
            breath = 1.0 + 0.02 * math.sin(t_sec * 3.5)
            canvas.save()
            canvas.translate(W * 0.5, H * 0.5)
            canvas.scale(zoom, zoom)
            canvas.translate(-W * 0.5, -H * 0.5)
            canvas.drawImage(env_snap, 0, 0)
            canvas.save()
            canvas.translate(540, 1200)
            canvas.scale(breath, breath)
            canvas.translate(-540, -1200)
            canvas.drawImage(vishwamitra_snap, 0, 0)
            canvas.restore()
            canvas.restore()

        elif t_sec < t_s9:
            # Shot 9 (55.0s - 64.2s): Shri Ram Divine Stride in 0 dB Silence Vacuum (Line 07 Shri Ram Stride)
            # Camera: Full tracking shot of Shri Ram walking calmly across the hall with golden radiance
            canvas.drawImage(env_snap, 0, 0)
            prog = (t_sec - t_s8) / (t_s9 - t_s8)
            walk_x = -160 + 320 * prog
            canvas.drawImage(ram_stride_snap, walk_x, 0)
            canvas.drawImage(bow_altar_snap, 340, 20)

        elif t_sec < t_s10:
            # Shot 10 (64.2s - 71.0s): Shri Ram Lifting Colossal Bow with One Hand (Line 08 One Hand Lift)
            # Camera: Colossal bow levitating into the air like a dry lotus stem, golden light bursting!
            canvas.drawImage(env_snap, 0, 0)
            lift_pulse = 1.0 + 0.03 * math.sin(t_sec * 4.0)
            canvas.save()
            canvas.translate(W * 0.5, H * 0.5)
            canvas.scale(lift_pulse, lift_pulse)
            canvas.translate(-W * 0.5, -H * 0.5)
            canvas.drawImage(ram_lift_snap, 0, 0)
            canvas.restore()

        elif t_sec < t_s11:
            # Shot 11 (71.0s - 77.7s): Heroic Extreme Profile Close-up of Shri Ram Pulling Bowstring (Line 09)
            # Camera: Extreme macro profile on lotus eyes, kundal, gold bowstring pulled to ear, sparks!
            cam_zoom = 1.0 + 0.08 * ((t_sec - t_s10) / (t_s11 - t_s10))
            canvas.save()
            canvas.translate(W * 0.5, H * 0.5)
            canvas.scale(cam_zoom, cam_zoom)
            canvas.translate(-W * 0.5, -H * 0.5)
            canvas.drawImage(env_snap, 0, 0)
            canvas.drawImage(ram_profile_pull_snap, 0, 0)
            canvas.restore()

        elif t_sec < t_s12:
            # Shot 12 (77.7s - 81.2s): Cosmic Lightning Explosion & Thunder Shockwaves (Line 10 Thunder)
            # Camera: Screen shaking, electric blue-white lightning bolts crackling across hall!
            shake_x = 8.0 * math.sin(t_sec * 60)
            shake_y = 6.0 * math.cos(t_sec * 55)
            canvas.save()
            canvas.translate(shake_x, shake_y)
            canvas.drawImage(env_snap, 0, 0)
            canvas.drawImage(ram_profile_pull_snap, 0, 0)
            canvas.drawImage(lightning_burst_snap, 0, 0)
            canvas.restore()

        elif t_sec < t_flash:
            # Shot 12B (81.2s - 81.76s): Blinding White Cosmic Snap!
            canvas.clear(skia.ColorWHITE)

        else:
            # Shot 13 (81.76s - 83.56s): Void Black Hard Cut + Gold Suspense Cliffhanger Badge
            canvas.clear(skia.ColorBLACK)
            if cliff_snap:
                canvas.drawImage(cliff_snap, 50, 840)

        # Floating Golden Embers (throughout live visual scenes)
        if t_sec < t_s12:
            for pt in particles:
                py = (pt["y"] - pt["speed"] * frame_idx * 0.9) % H
                canvas.drawCircle(pt["x"], py, pt["r"], skia.Paint(Color=skia.ColorSetARGB(190, 255, 235, 130), AntiAlias=True))

        # Vignette overlay
        if t_sec < t_s12:
            canvas.drawImage(vig_snap, 0, 0)

        # Zero-copy write to FFmpeg stdin (100% clean visuals, ZERO CAPTIONS)
        surface.readPixels(pix_info, pix_buf, W * 4)
        pipe.stdin.write(pix_buf)

        if frame_idx % 300 == 0:
            print(f"Rendered {frame_idx}/{total_frames} frames ({frame_idx/total_frames*100:.1f}%)", flush=True)

    pipe.stdin.close()
    pipe.wait()
    t_render_done = time.time()
    print(f"✅ 13-Shot Video rendered in {t_render_done - t_start_total:.1f}s ({total_frames/(t_render_done - t_start_total):.1f} FPS)!")

    # 4. Mux Video with Master Audio
    print("🎬 Muxing 13-shot video with punchy master audio...")
    mux_cmd = [
        "ffmpeg", "-y",
        "-i", str(temp_video),
        "-i", str(AUDIO_MASTER_FILE),
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(final_video)
    ]
    subprocess.run(mux_cmd, check=True)
    print(f"🎉 13-SHOT CINEMATIC VIDEO READY: {final_video}")

    if os.path.exists(temp_video):
        os.remove(temp_video)

if __name__ == "__main__":
    main()
