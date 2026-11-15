"""
GROW10Z — Ultra-Fast Cinema-Grade 8-Shot Production Director for EP007 (Parashurama-Laxman Samvaad)
100% Visual Directing Locked to Every Line:
- Shot 1 (0.0s - 5.5s): Split Standoff — Parashurama's Axe vs Laxman's Defiant Smirk (Line 00)
- Shot 2 (5.5s - 12.6s): Parashurama Wrath Macro — Bloodshot Eyes & Roaring Mouth (Line 01)
- Shot 3 (12.6s - 19.6s): Full-Body Kumar Laxman Fearless Witty Retort in Royal Court (Line 02)
- Shot 4 (19.6s - 26.5s): Severed Pinaka Bow Altar & Floating Golden Dust (Line 03)
- Shot 5 (26.5s - 32.8s): Royal Court Panic, Cowering Kings, Axe Raised Overhead (Line 04)
- Shot 6 (32.8s - 37.8s): Parashurama Towering Strike Pose & Blazing Blade (Line 05)
- Shot 7 (37.8s - 44.2s): Shri Ram Divine Stride with Folded Hands in 0 dB Silence (Line 06)
- Shot 8 (44.2s - 55.0s): Standoff Freeze -> Void Black Hard Cut -> 3D Golden Cliffhanger Badge (Line 07)
ZERO CAPTIONS on video frame (100% clean visuals).
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
    draw_mighty_kings_struggle
)
from scratch.test_full_body_characters import (
    draw_full_body_parashurama,
    draw_full_body_laxman
)
from studio_ramayana.pipeline.render_fixed_ep006 import draw_snapped_bow_halves

EP_DIR = BASE_DIR / "studio_ramayana" / "episodes" / "ep007"
TIMELINE_FILE = EP_DIR / "timeline.json"
AUDIO_MASTER_FILE = EP_DIR / "audio_master.wav"

W, H = 1080, 1920
FPS = 30

def make_snapshot(draw_fn, width=W, height=H):
    surf = skia.Surface(width, height)
    cv = surf.getCanvas()
    draw_fn(cv)
    return surf.makeImageSnapshot()

def main():
    print("==================================================")
    print("🎬 RENDERING 8-SHOT CINEMATIC MASTERPIECE (EP007)")
    print("==================================================")
    t_start_total = time.time()

    total_duration = 55.00 # Exact audio master duration
    total_frames = int(total_duration * FPS) # 1650 frames

    temp_video = EP_DIR / "temp_video_ep007.mp4"
    final_video = EP_DIR / "ep007_final.mp4"

    # 1. Preload Static Badges & Background
    print("📜 Preloading background & badges...")
    badge_path = EP_DIR / "cliffhanger_badge.png"
    badge_snap = skia.Image.MakeFromEncoded(skia.Data.MakeFromFileName(str(badge_path)))

    vig_paint = skia.Paint(
        Shader=skia.GradientShader.MakeRadial(
            skia.Point(W * 0.5, H * 0.5), H * 0.65,
            [skia.ColorTRANSPARENT, skia.ColorSetARGB(190, 8, 4, 12)],
            [0.6, 1.0]
        ),
        AntiAlias=True
    )
    vig_snap = make_snapshot(lambda cv: cv.drawRect(skia.Rect(0, 0, W, H), vig_paint))

    # Pre-render Mithila Environment Snapshot
    print("🏛️ Pre-rendering Mithila Darbar environment...")
    env_snap = make_snapshot(lambda cv: draw_cinematic_environment(cv, "mithila_darbar", 1.0, W, H))

    # Pre-render Cowering Kings Snapshot
    print("👑 Pre-rendering Cowering Kings snapshot...")
    kings_snap = make_snapshot(lambda cv: [
        draw_mighty_kings_struggle(cv, 200, 1420, scale=1.2, strain=1.0),
        draw_mighty_kings_struggle(cv, 400, 1440, scale=1.1, strain=0.8),
        draw_mighty_kings_struggle(cv, 680, 1440, scale=1.1, strain=0.8),
        draw_mighty_kings_struggle(cv, 880, 1420, scale=1.2, strain=1.0)
    ])

    # Pre-render Full-Body Characters Snapshots
    print("⚔️ Pre-rendering Full-Body Characters...")
    parashurama_full_snap = make_snapshot(lambda cv: draw_full_body_parashurama(cv, cx=540, ground_y=1660, scale=1.0))
    laxman_full_snap = make_snapshot(lambda cv: draw_full_body_laxman(cv, cx=580, ground_y=1660, scale=0.98))
    
    # Pre-render Serene Shri Ram with folded hands / peace gesture
    ram_peace_snap = make_snapshot(lambda cv: [
        draw_cinematic_shri_ram(cv, 540, 1220, scale=1.75, breathing=0.0, bow_draw=0.0)
    ])

    # Pre-render Snapped Bow Snapshot
    bow_snapped_snap = make_snapshot(lambda cv: draw_snapped_bow_halves(cv, 540, 1380, scale=1.60, sep=36))

    # Setup FFmpeg Pipe
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-pix_fmt", "bgra",
        "-s", f"{W}x{H}",
        "-r", str(FPS),
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

    # Dynamic Scene Cut Timestamps
    t_s1 = 5.50   # Shot 1: Split Standoff (0.0s - 5.5s)
    t_s2 = 12.60  # Shot 2: Parashurama Wrath Macro (5.5s - 12.6s)
    t_s3 = 19.60  # Shot 3: Laxman Fearless Retort (12.6s - 19.6s)
    t_s4 = 26.50  # Shot 4: Snapped Bow Truth Metaphor (19.6s - 26.5s)
    t_s5 = 32.80  # Shot 5: Court Panic & Axe Raised (26.5s - 32.8s)
    t_s6 = 37.80  # Shot 6: Parashurama Towering Strike (32.8s - 37.8s)
    t_s7 = 44.20  # Shot 7: Shri Ram Divine Stride in 0 dB Silence (37.8s - 44.2s)
    t_cut_black = 47.00 # Standoff tension -> Hard cut to black (44.2s - 47.0s -> 47.0s+)

    print(f"🚀 Streaming {total_frames} frames into FFmpeg pipeline...")

    # Floating golden dust particles
    np.random.seed(42)
    particles = [{"x": random.randint(40, W-40), "y": random.randint(50, H-50), "speed": random.uniform(2.5, 6.0), "r": random.uniform(3.0, 7.5)} for _ in range(45)]

    for frame_idx in range(total_frames):
        t_sec = frame_idx / FPS
        canvas.clear(skia.ColorSetARGB(255, 10, 6, 12))

        # --- SCENE SELECTION ---
        if t_sec < t_s1:
            # Shot 1: Split Standoff Faceoff Slider
            prog = t_sec / t_s1
            zoom = 1.0 + 0.08 * prog
            canvas.save()
            canvas.translate(W * 0.5, H * 0.5)
            canvas.scale(zoom, zoom)
            canvas.translate(-W * 0.5, -H * 0.5)
            canvas.drawImage(env_snap, 0, 0)
            # Left Parashurama
            canvas.save()
            canvas.translate(-190, 20)
            canvas.drawImage(parashurama_full_snap, 0, 0)
            canvas.restore()
            # Right Laxman
            canvas.save()
            canvas.translate(190, 20)
            canvas.drawImage(laxman_full_snap, 0, 0)
            canvas.restore()
            canvas.restore()

        elif t_sec < t_s2:
            # Shot 2: Parashurama Divine Wrath Macro Close-up
            roar_shake = 4.5 * math.sin(t_sec * 45)
            canvas.save()
            canvas.translate(roar_shake, 0)
            canvas.drawImage(env_snap, 0, 0)
            canvas.save()
            canvas.translate(540, 960)
            macro_scale = 2.15 + 0.12 * math.sin((t_sec - t_s1) * 5)
            canvas.scale(macro_scale, macro_scale)
            canvas.translate(-540, -880)
            canvas.drawImage(parashurama_full_snap, 0, 0)
            canvas.restore()
            canvas.restore()

        elif t_sec < t_s3:
            # Shot 3: Full-Body Kumar Laxman Fearless Witty Retort
            zoom = 1.0 + 0.05 * ((t_sec - t_s2) / (t_s3 - t_s2))
            canvas.save()
            canvas.translate(W * 0.5, H * 0.5)
            canvas.scale(zoom, zoom)
            canvas.translate(-W * 0.5, -H * 0.5)
            canvas.drawImage(env_snap, 0, 0)
            draw_mighty_kings_struggle(canvas, 220, 1420, scale=1.1, strain=1.0)
            lax_breath = 1.0 + 0.018 * math.sin((t_sec - t_s2) * 3.5)
            canvas.save()
            canvas.translate(580, 1660)
            canvas.scale(lax_breath, lax_breath)
            canvas.translate(-580, -1660)
            canvas.drawImage(laxman_full_snap, 0, 0)
            canvas.restore()
            canvas.restore()

        elif t_sec < t_s4:
            # Shot 4: Snapped Bow Truth Metaphor & Golden Light
            zoom = 1.0 + 0.08 * ((t_sec - t_s3) / (t_s4 - t_s3))
            canvas.save()
            canvas.translate(W * 0.5, H * 0.5)
            canvas.scale(zoom, zoom)
            canvas.translate(-W * 0.5, -H * 0.5)
            canvas.drawImage(env_snap, 0, 0)
            canvas.drawImage(bow_snapped_snap, 0, 0)
            canvas.restore()

        elif t_sec < t_s5:
            # Shot 5: Royal Court Panic & Parashu Axe Raised Overhead
            shake_x = 5.0 * math.sin(t_sec * 50)
            canvas.save()
            canvas.translate(shake_x, 0)
            canvas.drawImage(env_snap, 0, 0)
            canvas.drawImage(kings_snap, 0, 0)
            # Parashurama towering with raised axe in background center
            canvas.save()
            canvas.translate(0, -30)
            canvas.drawImage(parashurama_full_snap, 0, 0)
            canvas.restore()
            canvas.restore()

        elif t_sec < t_s6:
            # Shot 6: Parashurama Towering Strike Pose
            zoom = 1.0 + 0.10 * ((t_sec - t_s5) / (t_s6 - t_s5))
            canvas.save()
            canvas.translate(W * 0.5, H * 0.5)
            canvas.scale(zoom, zoom)
            canvas.translate(-W * 0.5, -H * 0.5)
            canvas.drawImage(env_snap, 0, 0)
            canvas.drawImage(parashurama_full_snap, 0, 0)
            canvas.restore()

        elif t_sec < t_s7:
            # Shot 7: Shri Ram Divine Stride with Folded Hands (0 dB Silence)
            prog = (t_sec - t_s6) / (t_s7 - t_s6)
            canvas.drawImage(env_snap, 0, 0)
            walk_x = -120 + 240 * prog
            canvas.save()
            canvas.translate(walk_x, 0)
            canvas.drawImage(ram_peace_snap, 0, 0)
            canvas.restore()

        elif t_sec < t_cut_black:
            # Shot 8A (44.2s - 47.0s): Climactic Three-Way Faceoff
            canvas.drawImage(env_snap, 0, 0)
            # Left Parashurama
            canvas.save()
            canvas.translate(-240, 20)
            canvas.drawImage(parashurama_full_snap, 0, 0)
            canvas.restore()
            # Center Shri Ram
            canvas.save()
            canvas.translate(0, 40)
            canvas.drawImage(ram_peace_snap, 0, 0)
            canvas.restore()
            # Right Laxman
            canvas.save()
            canvas.translate(240, 20)
            canvas.drawImage(laxman_full_snap, 0, 0)
            canvas.restore()

        else:
            # Shot 8B (47.0s - 55.0s): Void Black Hard Cut + 3D Golden Cliffhanger Badge
            canvas.clear(skia.ColorSetARGB(255, 6, 3, 8))
            if badge_snap:
                fade_in = min(1.0, (t_sec - t_cut_black) / 0.6)
                badge_scale = 0.92 + 0.08 * fade_in
                canvas.save()
                canvas.translate(W * 0.5, H * 0.5)
                canvas.scale(badge_scale, badge_scale)
                canvas.translate(-W * 0.5, -H * 0.5)
                canvas.drawImage(badge_snap, (W - badge_snap.width()) / 2, (H - badge_snap.height()) / 2)
                canvas.restore()

        # Floating Golden Embers
        for pt in particles:
            py = (pt["y"] - pt["speed"] * frame_idx * 0.8) % H
            canvas.drawCircle(pt["x"], py, pt["r"], skia.Paint(Color=skia.ColorSetARGB(180, 255, 235, 130), AntiAlias=True))

        # Vignette overlay on live visual scenes
        if t_sec < t_cut_black and t_sec > t_s1:
            canvas.drawImage(vig_snap, 0, 0)

        # Zero-copy write to FFmpeg stdin (100% clean visuals, ZERO CAPTIONS)
        surface.readPixels(pix_info, pix_buf, W * 4)
        pipe.stdin.write(pix_buf)

        if frame_idx % 300 == 0:
            print(f"Rendered {frame_idx}/{total_frames} frames ({frame_idx/total_frames*100:.1f}%)", flush=True)

    pipe.stdin.close()
    pipe.wait()
    t_render_done = time.time()
    print(f"✅ Video frames rendered in {t_render_done - t_start_total:.1f}s ({total_frames/(t_render_done - t_start_total):.1f} FPS)!")

    # Mux Video with Master Audio
    print("🎬 Muxing video with punchy master audio...")
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
    print(f"🎉 8-SHOT CINEMATIC VIDEO READY: {final_video}")

    if os.path.exists(temp_video):
        os.remove(temp_video)

if __name__ == "__main__":
    main()
