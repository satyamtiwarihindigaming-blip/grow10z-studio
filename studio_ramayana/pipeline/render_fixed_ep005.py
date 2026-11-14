"""
GROW10Z — Flawless, Pure Cinematic Production Renderer for EP005 (The Divine Pinaka Bow)
NO CAPTIONS (Clean, Immersive Visuals):
- Zero on-screen caption clutter per human instruction ("captions lagao he mat video me ok")
- Natural, fast viral pacing (83.56s total runtime, punchy dialogue, natural suspense)
- Visual scenes tightly locked to speech triggers:
    * 0.0s - 2.2s: Fast Ancient Manuscript opening
    * 2.2s - 19.1s: Divine Pinaka Bow Altar Reveal (Lines 00 & 01)
    * 19.1s - 32.9s: Kings Strain & Fail against Pinaka (Lines 02 & 03)
    * 32.9s - 47.5s: Maharaja Janak's Soul-Crushing Lament (Lines 04 & 05)
    * 47.5s - 63.9s: Vishwamitra Smiles & Ram Divine Stride in Silence Vacuum (Lines 06 & 07)
    * 63.9s - 70.8s: Ram Lifts Pinaka Bow Effortlessly with One Hand (Line 08)
    * 70.8s - 81.2s: Ram Pulls Bowstring to Ear, Lightning Sparks (Lines 09 & 10)
    * 81.2s - 81.8s: Cosmic Snap & Blinding White Lightning Flash
    * 81.8s - 83.56s: Pure Black Hard Cut + Gold Suspense Cliffhanger Card
- High-FPS cached snapshots (~25s ultra-fast render)
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
    draw_maharaja_janak
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
    print("🎬 RENDERING CLEAN CINEMATIC EP005 (ZERO CAPTIONS, PUNCHY PACING)")
    print("==================================================")
    t_start_total = time.time()

    with open(TIMELINE_FILE, "r", encoding="utf-8") as f:
        timeline = json.load(f)

    total_duration = timeline[-1]["end"] + 2.4 # 83.56s
    fps = 30
    total_frames = int(total_duration * fps)
    W, H = 1080, 1920

    temp_video = EP_DIR / "temp_video_clean.mp4"
    final_video = EP_DIR / "ep005_final.mp4"

    # 1. Preload Static Badges & Background
    print("📜 Loading manuscript opening & cliffhanger badge...")
    book_snap = skia.Image.MakeFromEncoded(skia.Data.MakeFromFileName(str(EP_DIR / "manuscript_page.png")))
    cliff_snap = skia.Image.MakeFromEncoded(skia.Data.MakeFromFileName(str(EP_DIR / "cliffhanger_badge.png")))

    print("🏛️ Pre-rendering Mithila Darbar environment snapshot...")
    env_snap = make_snapshot(lambda cv: draw_cinematic_environment(cv, "mithila_darbar", 1.0, W, H))

    print("🎭 Pre-rendering Vignette snapshot...")
    vig_paint = skia.Paint(
        Shader=skia.GradientShader.MakeRadial(
            skia.Point(W * 0.5, H * 0.5), H * 0.65,
            [skia.ColorTRANSPARENT, skia.ColorSetARGB(190, 8, 4, 12)],
            [0.6, 1.0]
        ),
        AntiAlias=True
    )
    vig_snap = make_snapshot(lambda cv: cv.drawRect(skia.Rect(0, 0, W, H), vig_paint))

    # 2. Pre-render Character Pose Snapshots
    print("🎨 Pre-rendering Character Rigs into High-FPS Snapshots...")
    bow_altar_snap = make_snapshot(lambda cv: draw_sacred_pinaka_bow(cv, 540, 1420, scale=1.55, glow=1.2))
    bow_close_snap = make_snapshot(lambda cv: draw_sacred_pinaka_bow(cv, 540, 1420, scale=1.70, glow=1.0))
    janak_snap = make_snapshot(lambda cv: draw_maharaja_janak(cv, 540, 1260, scale=1.9, agony=1.0, breathing=0.0))
    vishwamitra_snap = make_snapshot(lambda cv: draw_cinematic_vishwamitra(cv, 240, 1220, scale=1.45, breathing=0.0))
    ram_stride_snap = make_snapshot(lambda cv: draw_cinematic_shri_ram(cv, 540, 1180, scale=1.75, breathing=0.0, bow_draw=0.0))
    ram_lift_snap = make_snapshot(lambda cv: [
        draw_cinematic_shri_ram(cv, 400, 1180, scale=1.80, breathing=0.0, bow_draw=0.0),
        draw_sacred_pinaka_bow(cv, 720, 1140, scale=1.45, glow=2.4)
    ])
    ram_draw_0 = make_snapshot(lambda cv: [
        draw_cinematic_shri_ram(cv, 360, 1180, scale=1.92, breathing=0.0, bow_draw=0.1),
        draw_sacred_pinaka_bow(cv, 730, 1380, scale=1.4, glow=2.0)
    ])
    ram_draw_50 = make_snapshot(lambda cv: [
        draw_cinematic_shri_ram(cv, 360, 1180, scale=1.92, breathing=0.0, bow_draw=0.5),
        draw_sacred_pinaka_bow(cv, 730, 1380, scale=1.4, glow=2.4)
    ])
    ram_draw_100 = make_snapshot(lambda cv: [
        draw_cinematic_shri_ram(cv, 360, 1180, scale=1.92, breathing=0.0, bow_draw=1.0),
        draw_sacred_pinaka_bow(cv, 730, 1380, scale=1.4, glow=2.8)
    ])

    # 3. Floating Golden Embers
    np.random.seed(42)
    particles = [{"x": random.randint(40, W-40), "y": random.randint(50, H-50), "speed": random.uniform(2.5, 6.0), "r": random.uniform(3.0, 7.5)} for _ in range(40)]

    # 4. Setup FFmpeg Pipe
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

    # Timeline bounds (Punchy & Natural)
    t_s1 = timeline[0]["start"]   # 2.20s
    t_s2 = timeline[2]["start"]   # 19.26s
    t_s3 = timeline[4]["start"]   # 33.24s
    t_s4 = timeline[6]["start"]   # 47.83s
    t_s5 = timeline[8]["start"]   # 64.22s
    t_s6a = timeline[9]["start"]  # 71.04s
    t_s6b = timeline[10]["end"]   # 81.16s
    t_flash = t_s6b + 0.6         # 81.76s

    print(f"🚀 Streaming {total_frames} frames ({total_duration:.2f}s) to FFmpeg...")

    for frame_idx in range(total_frames):
        t_sec = frame_idx / fps
        canvas.clear(skia.ColorBLACK)

        # -------------------------------------------------------------
        # 1. VISUAL DIRECTING (Pure Cinematic & Natural Pacing)
        # -------------------------------------------------------------
        if t_sec < t_s1:
            # Shot 1: Manuscript Opening (Fast punchy 2.2s intro)
            prog = min(1.0, t_sec / 2.0)
            zoom = 1.0 + 0.04 * prog
            canvas.save()
            canvas.translate(W * 0.5, H * 0.5)
            canvas.scale(zoom, zoom)
            canvas.translate(-W * 0.5, -H * 0.5)
            canvas.drawImage(book_snap, 0, 0)
            canvas.restore()

        elif t_sec < t_s2:
            # Shot 2: The Divine Pinaka Bow Reveal (Lines 00 & 01)
            pan_x = 18 * math.sin((t_sec - t_s1) * 0.4)
            canvas.drawImage(env_snap, pan_x, 0)
            breath = 1.0 + 0.02 * math.sin(t_sec * 3.5)
            canvas.save()
            canvas.translate(540 + pan_x, 1420)
            canvas.scale(breath, breath)
            canvas.translate(-540, -1420)
            canvas.drawImage(bow_altar_snap, 0, 0)
            canvas.restore()

        elif t_sec < t_s3:
            # Shot 3: Kings Strain & Fail against Pinaka (Lines 02 & 03)
            zoom = 1.0 + 0.05 * ((t_sec - t_s2) / (t_s3 - t_s2))
            canvas.save()
            canvas.translate(W * 0.5, H * 0.5)
            canvas.scale(zoom, zoom)
            canvas.translate(-W * 0.5, -H * 0.5)
            canvas.drawImage(env_snap, 0, 0)
            canvas.drawImage(bow_close_snap, 0, 0)
            canvas.restore()

        elif t_sec < t_s4:
            # Shot 4: Maharaja Janak's Agonizing Lament (Lines 04 & 05)
            zoom = 1.0 + 0.06 * ((t_sec - t_s3) / (t_s4 - t_s3))
            breath = 1.0 + 0.02 * math.sin(t_sec * 3.0)
            canvas.save()
            canvas.translate(W * 0.5, H * 0.5)
            canvas.scale(zoom, zoom)
            canvas.translate(-W * 0.5, -H * 0.5)
            canvas.drawImage(env_snap, 0, 0)
            canvas.save()
            canvas.translate(540, 1260)
            canvas.scale(breath, breath)
            canvas.translate(-540, -1260)
            canvas.drawImage(janak_snap, 0, 0)
            canvas.restore()
            canvas.restore()

        elif t_sec < t_s5:
            # Shot 5: Vishwamitra Smiles & Ram Divine Stride in Silence (Lines 06 & 07)
            canvas.drawImage(env_snap, 0, 0)
            canvas.drawImage(vishwamitra_snap, 0, 0)
            if t_sec < timeline[7]["start"]:
                canvas.drawImage(ram_stride_snap, -120, 0)
            else:
                # Divine stride forward (Silence Vacuum)
                prog = (t_sec - timeline[7]["start"]) / (t_s5 - timeline[7]["start"])
                walk_x = -120 + 240 * prog
                canvas.drawImage(ram_stride_snap, walk_x, 0)
            canvas.drawImage(bow_altar_snap, 340, 20)

        elif t_sec < t_s6a:
            # Shot 6A: Ram Lifting Pinaka Bow with One Hand (Line 08)
            canvas.drawImage(env_snap, 0, 0)
            breath = 1.0 + 0.02 * math.sin(t_sec * 4.0)
            canvas.save()
            canvas.translate(W * 0.5, H * 0.5)
            canvas.scale(breath, breath)
            canvas.translate(-W * 0.5, -H * 0.5)
            canvas.drawImage(ram_lift_snap, 0, 0)
            canvas.restore()

        elif t_sec < t_s6b:
            # Shot 6B: Ram Drawing Bowstring to Ear (Lines 09 & 10)
            cam_zoom = 1.0 + 0.08 * ((t_sec - t_s6a) / (t_s6b - t_s6a))
            canvas.save()
            canvas.translate(W * 0.5, H * 0.5)
            canvas.scale(cam_zoom, cam_zoom)
            canvas.translate(-W * 0.5, -H * 0.5)
            canvas.drawImage(env_snap, 0, 0)
            draw_prog = (t_sec - t_s6a) / (t_s6b - t_s6a)
            if draw_prog < 0.35:
                canvas.drawImage(ram_draw_0, 0, 0)
            elif draw_prog < 0.70:
                canvas.drawImage(ram_draw_50, 0, 0)
            else:
                canvas.drawImage(ram_draw_100, 0, 0)
            canvas.restore()

        elif t_sec < t_flash:
            # Shot 7A: Blinding White Cosmic Flash (Cosmic bow snap)
            canvas.clear(skia.ColorWHITE)

        else:
            # Shot 7B: Pure Black Hard Cut + Gold Suspense Cliffhanger Badge
            canvas.clear(skia.ColorBLACK)
            if cliff_snap:
                canvas.drawImage(cliff_snap, 50, 840)

        # -------------------------------------------------------------
        # 2. FLOATING GOLDEN EMBERS
        # -------------------------------------------------------------
        if t_sec < t_s6b:
            for pt in particles:
                py = (pt["y"] - pt["speed"] * frame_idx * 0.9) % H
                canvas.drawCircle(pt["x"], py, pt["r"], skia.Paint(Color=skia.ColorSetARGB(190, 255, 235, 130), AntiAlias=True))

        # -------------------------------------------------------------
        # 3. CINEMATIC VIGNETTE (Cached Snapshot)
        # -------------------------------------------------------------
        if t_sec < t_s6b:
            canvas.drawImage(vig_snap, 0, 0)

        # Zero-copy write to FFmpeg stdin (NO CAPTIONS AT ALL)
        surface.readPixels(pix_info, pix_buf, W * 4)
        pipe.stdin.write(pix_buf)

        if frame_idx % 300 == 0:
            print(f"Rendered {frame_idx}/{total_frames} frames ({frame_idx/total_frames*100:.1f}%)", flush=True)

    pipe.stdin.close()
    pipe.wait()
    t_render_done = time.time()
    print(f"✅ Video frames rendered in {t_render_done - t_start_total:.1f}s ({total_frames/(t_render_done - t_start_total):.1f} FPS)!")

    # 4. Mux Video with Master Audio
    print("🎬 Muxing final video with master audio...")
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
    print(f"🎉 FINAL VIDEO READY: {final_video}")

    if os.path.exists(temp_video):
        os.remove(temp_video)

if __name__ == "__main__":
    main()
