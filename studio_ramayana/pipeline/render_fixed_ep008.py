"""
GROW10Z — Ultra-Fast Cinema-Grade 7-Shot Production Director for EP008 (Shri Ram - Parashurama Milan)
Exact Visual Directing Locked to Every Line:
- Shot 1 (0.0s - 7.0s): Parashurama Wrath & Axe Raised Overhead in Mithila Darbar (Line 00)
- Shot 2 (7.0s - 15.0s): Lakshman Defiant Smirk -> Shri Ram Divine Stride Between Them (Line 01)
- Shot 3 (15.0s - 27.0s): Shri Ram Gentle Folded Hands Plea, Diffusing Cosmic Wrath (Line 02)
- Shot 4 (27.0s - 36.5s): Parashurama Lowers Axe & Presents Golden Vaishnava Sharang Bow (Line 03)
- Shot 5 (36.5s - 44.5s): 0 dB Silence Vacuum -> Shri Ram Strings Vaishnava Bow -> Blinding Sunburst Aura (Line 04)
- Shot 6 (44.5s - 53.0s): Parashurama's Divine Realization, Tears of Awe & Complete Surrender (Line 05)
- Shot 7 (53.0s - 66.0s): Divine Wide Tableaux -> Hard Cut to Void Black -> 3D Gold Cliffhanger Badge (Line 06)
ZERO CAPTIONS on video frame (100% clean visual animation).
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
from studio_ramayana.character_engine.ep008_visual_rigs import (
    draw_golden_vaishnava_bow,
    draw_parashurama_surrender,
    draw_cosmic_sunburst_aura
)

EP_DIR = BASE_DIR / "studio_ramayana" / "episodes" / "ep008"
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
    print("🎬 RENDERING 7-SHOT CINEMATIC MASTERPIECE (EP008)")
    print("==================================================")
    t_start_total = time.time()

    total_duration = 66.00 # Exact audio master duration
    total_frames = int(total_duration * FPS) # 1980 frames

    temp_video = EP_DIR / "temp_video_ep008.mp4"
    final_video = EP_DIR / "ep008_final.mp4"

    # 1. Preload Badges & Assets
    print("📜 Preloading background, badges & snapshots...")
    badge_path = EP_DIR / "cliffhanger_badge.png"
    badge_snap = skia.Image.MakeFromEncoded(skia.Data.MakeFromFileName(str(badge_path)))

    manuscript_path = EP_DIR / "manuscript_page.png"
    manuscript_snap = skia.Image.MakeFromEncoded(skia.Data.MakeFromFileName(str(manuscript_path)))

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
    print("👑 Pre-rendering Cowering Kings...")
    kings_snap = make_snapshot(lambda cv: [
        draw_mighty_kings_struggle(cv, 180, 1420, scale=1.2, strain=1.0),
        draw_mighty_kings_struggle(cv, 380, 1440, scale=1.1, strain=0.8),
        draw_mighty_kings_struggle(cv, 700, 1440, scale=1.1, strain=0.8),
        draw_mighty_kings_struggle(cv, 900, 1420, scale=1.2, strain=1.0)
    ])

    # Pre-render Characters
    print("⚔️ Pre-rendering Character Rigs...")
    parashurama_wrath_snap = make_snapshot(lambda cv: draw_full_body_parashurama(cv, cx=540, ground_y=1660, scale=1.0))
    laxman_full_snap = make_snapshot(lambda cv: draw_full_body_laxman(cv, cx=580, ground_y=1660, scale=0.98))
    ram_peace_snap = make_snapshot(lambda cv: draw_cinematic_shri_ram(cv, 540, 1220, scale=1.75, breathing=0.0, bow_draw=0.0))
    parashurama_surrender_snap = make_snapshot(lambda cv: draw_parashurama_surrender(cv, cx=540, ground_y=1660, scale=1.0))

    # Pre-render Vaishnava Bow Snapshots (resting vs drawn)
    vaishnava_bow_snap = make_snapshot(lambda cv: draw_golden_vaishnava_bow(cv, cx=540, cy=960, scale=1.3, glow=1.2, bow_draw=0.0))
    vaishnava_drawn_snap = make_snapshot(lambda cv: draw_golden_vaishnava_bow(cv, cx=540, cy=960, scale=1.4, glow=1.8, bow_draw=1.0))

    # Snapped Pinaka on floor
    broken_bow_snap = make_snapshot(lambda cv: draw_snapped_bow_halves(cv, cx=540, cy=1480, scale=1.25))

    # Golden Embers & Floating Petals
    np.random.seed(108)
    particles = [{"x": random.randint(40, W-40), "y": random.randint(50, H-50), "speed": random.uniform(2.5, 6.0), "r": random.uniform(3.0, 7.5)} for _ in range(45)]
    petals = [{"x": random.randint(30, W-30), "y": random.randint(20, H-20), "vx": random.uniform(-1.5, 1.5), "vy": random.uniform(3.0, 6.5), "size": random.uniform(12, 22), "angle": random.uniform(0, 360)} for _ in range(35)]

    # 2. Setup FFmpeg Pipe
    print("⚙️ Initializing FFmpeg sub-process...")
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-pix_fmt", "bgra",
        "-s", f"{W}x{H}",
        "-r", str(FPS),
        "-i", "-",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "ultrafast",
        "-crf", "18",
        str(temp_video)
    ]
    pipe = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)
    pix_buf = bytearray(W * H * 4)
    pix_info = skia.ImageInfo.Make(W, H, skia.kBGRA_8888_ColorType, skia.kPremul_AlphaType)

    surface = skia.Surface(W, H)
    canvas = surface.getCanvas()

    print(f"🚀 Rendering {total_frames} frames at 30 FPS...")
    render_start = time.time()

    for f_idx in range(total_frames):
        t_sec = f_idx / FPS
        canvas.clear(skia.ColorBLACK)

        # =========================================================================
        # SHOT 1: 0.0s - 7.0s | Parashurama Wrath & Axe Raised Overhead (Line 00)
        # =========================================================================
        if t_sec < 7.0:
            if t_sec < 3.2:
                # Ancient Manuscript Page Push-in
                progress = min(1.0, t_sec / 3.0)
                zoom = 1.0 + 0.04 * progress
                canvas.save()
                canvas.translate(W * 0.5, H * 0.5)
                canvas.scale(zoom, zoom)
                canvas.translate(-W * 0.5, -H * 0.5)
                canvas.drawImage(manuscript_snap, 0, 0)
                canvas.restore()
            else:
                # Court Terror & Axe Raised
                shake_x = 7.0 * math.sin(t_sec * 35) if t_sec > 5.0 else 0
                shake_y = 5.0 * math.cos(t_sec * 40) if t_sec > 5.0 else 0
                canvas.save()
                canvas.translate(shake_x, shake_y)
                canvas.drawImage(env_snap, 0, 0)
                canvas.drawImage(kings_snap, 0, 0)
                canvas.drawImage(broken_bow_snap, 0, 0)
                # Towering Parashurama
                canvas.drawImage(parashurama_wrath_snap, 0, 0)
                canvas.restore()

        # =========================================================================
        # SHOT 2: 7.0s - 15.0s | Laxman Defiant Smirk -> Shri Ram Divine Stride (Line 01)
        # =========================================================================
        elif t_sec < 15.0:
            canvas.drawImage(env_snap, 0, 0)
            canvas.drawImage(broken_bow_snap, 0, 0)

            # Left side: Parashurama glaring
            canvas.save()
            canvas.translate(-260, 0)
            canvas.drawImage(parashurama_wrath_snap, 0, 0)
            canvas.restore()

            # Right side: Kumar Laxman smiling fearless
            canvas.save()
            canvas.translate(220, 0)
            canvas.drawImage(laxman_full_snap, 0, 0)
            canvas.restore()

            # Center: Shri Ram strides forward smoothly
            stride_p = min(1.0, max(0.0, (t_sec - 10.0) / 4.5))
            if stride_p > 0:
                ram_y_offset = (1.0 - stride_p) * 200
                ram_alpha = min(255, int(stride_p * 255))
                canvas.save()
                canvas.translate(0, ram_y_offset)
                # Divine Cyan-Gold Aura blooming
                aura_p = skia.Paint(
                    Shader=skia.GradientShader.MakeRadial(
                        skia.Point(540, 1100), 280 * stride_p,
                        [skia.ColorSetARGB(int(140 * stride_p), 180, 240, 255),
                         skia.ColorSetARGB(int(60 * stride_p), 255, 220, 80),
                         skia.ColorTRANSPARENT],
                        [0.0, 0.5, 1.0]
                    ),
                    AntiAlias=True
                )
                canvas.drawCircle(540, 1100, 280 * stride_p, aura_p)
                canvas.drawImage(ram_peace_snap, 0, 0)
                canvas.restore()

        # =========================================================================
        # SHOT 3: 15.0s - 27.0s | Shri Ram Folded Hands Peaceful Plea (Line 02)
        # =========================================================================
        elif t_sec < 27.0:
            cam_zoom = 1.0 + 0.06 * ((t_sec - 15.0) / 12.0)
            canvas.save()
            canvas.translate(W * 0.5, H * 0.5)
            canvas.scale(cam_zoom, cam_zoom)
            canvas.translate(-W * 0.5, -H * 0.5)
            canvas.drawImage(env_snap, 0, 0)

            # Left: Parashurama listening in astonishment
            canvas.save()
            canvas.translate(-300, 0)
            canvas.scale(0.95, 0.95)
            canvas.drawImage(parashurama_wrath_snap, 0, 0)
            canvas.restore()

            # Center-Right: Shri Ram with folded hands in divine radiance
            canvas.save()
            canvas.translate(40, -40)
            # Soft pulsating halo
            halo_r = 260 + 15 * math.sin(t_sec * 3.5)
            halo_p = skia.Paint(
                Shader=skia.GradientShader.MakeRadial(
                    skia.Point(540, 1100), halo_r,
                    [skia.ColorSetARGB(160, 255, 240, 180),
                     skia.ColorSetARGB(70, 140, 220, 255),
                     skia.ColorTRANSPARENT],
                    [0.0, 0.5, 1.0]
                ),
                AntiAlias=True
            )
            canvas.drawCircle(540, 1100, halo_r, halo_p)
            canvas.drawImage(ram_peace_snap, 0, 0)
            canvas.restore()
            canvas.restore()

        # =========================================================================
        # SHOT 4: 27.0s - 36.5s | Parashurama Presents Golden Vaishnava Bow (Line 03)
        # =========================================================================
        elif t_sec < 36.5:
            canvas.drawImage(env_snap, 0, 0)
            canvas.drawImage(broken_bow_snap, 0, 0)

            # Left: Parashurama offering the bow
            canvas.save()
            canvas.translate(-220, 0)
            canvas.drawImage(parashurama_wrath_snap, 0, 0)
            canvas.restore()

            # Center: Blazing Golden Vaishnava Bow floating and gleaming
            bow_pulse = 1.0 + 0.04 * math.sin(t_sec * 4.0)
            canvas.save()
            canvas.translate(20, -100)
            canvas.scale(bow_pulse, bow_pulse)
            canvas.drawImage(vaishnava_bow_snap, 0, 0)
            canvas.restore()

            # Right: Shri Ram calmly gazing at the bow
            canvas.save()
            canvas.translate(280, 0)
            canvas.drawImage(ram_peace_snap, 0, 0)
            canvas.restore()

        # =========================================================================
        # SHOT 5: 36.5s - 44.5s | 0 dB Silence -> Shri Ram Strings Bow -> Cosmic Sunburst (Line 04)
        # =========================================================================
        elif t_sec < 44.5:
            # Silence Vacuum -> Cosmic Flash!
            cam_zoom = 1.0 + 0.08 * ((t_sec - 36.5) / 8.0)
            canvas.save()
            canvas.translate(W * 0.5, H * 0.5)
            canvas.scale(cam_zoom, cam_zoom)
            canvas.translate(-W * 0.5, -H * 0.5)
            canvas.drawImage(env_snap, 0, 0)

            draw_progress = min(1.0, (t_sec - 38.0) / 3.0)

            # Blinding Cosmic Sunburst Aura behind Shri Ram
            if t_sec >= 39.5:
                aura_intensity = min(1.0, (t_sec - 39.5) / 1.5)
                draw_cosmic_sunburst_aura(canvas, 540, 1100, radius=520, rays=28, phase=t_sec * aura_intensity)

            # Shri Ram holding the bow
            canvas.drawImage(ram_peace_snap, 0, 0)

            # Drawn Vaishnava Bow
            canvas.save()
            canvas.translate(140, -100)
            if draw_progress >= 0.8:
                canvas.drawImage(vaishnava_drawn_snap, 0, 0)
            else:
                canvas.drawImage(vaishnava_bow_snap, 0, 0)
            canvas.restore()

            # White Flash at climax stringing point
            if 41.2 <= t_sec <= 41.6:
                flash_alpha = int((1.0 - (t_sec - 41.2) / 0.4) * 220)
                canvas.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Color=skia.ColorSetARGB(flash_alpha, 255, 255, 255)))

            canvas.restore()

        # =========================================================================
        # SHOT 6: 44.5s - 53.0s | Parashurama's Divine Realization & Surrender (Line 05)
        # =========================================================================
        elif t_sec < 53.0:
            canvas.drawImage(env_snap, 0, 0)

            # Left: Bhagwan Parashurama in profound Anjali Mudra surrender
            canvas.save()
            canvas.translate(-160, 0)
            canvas.drawImage(parashurama_surrender_snap, 0, 0)
            canvas.restore()

            # Right: Lord Shri Ram smiling with divine compassion
            canvas.save()
            canvas.translate(220, 0)
            # Radiant golden halo
            halo_p = skia.Paint(
                Shader=skia.GradientShader.MakeRadial(
                    skia.Point(540, 1100), 290,
                    [skia.ColorSetARGB(180, 255, 235, 120),
                     skia.ColorSetARGB(60, 255, 180, 40),
                     skia.ColorTRANSPARENT],
                    [0.0, 0.5, 1.0]
                ),
                AntiAlias=True
            )
            canvas.drawCircle(540, 1100, 290, halo_p)
            canvas.drawImage(ram_peace_snap, 0, 0)
            canvas.restore()

            # Celestial Flower Shower (Petals falling)
            for pet in petals:
                pet_y = (pet["y"] + pet["vy"] * f_idx * 0.9) % H
                pet_x = pet["x"] + 15 * math.sin((f_idx * 0.05) + pet["angle"])
                canvas.save()
                canvas.translate(pet_x, pet_y)
                canvas.rotate(pet["angle"] + f_idx * 2)
                p_paint = skia.Paint(Color=skia.ColorSetARGB(220, 255, 182, 193), AntiAlias=True) # Soft rose petal
                canvas.drawOval(skia.Rect(-pet["size"] * 0.5, -pet["size"], pet["size"] * 0.5, pet["size"]), p_paint)
                canvas.restore()

        # =========================================================================
        # SHOT 7: 53.0s - 66.0s | Wide Standoff -> Void Black -> 3D Gold Cliffhanger Badge (Line 06)
        # =========================================================================
        else:
            if t_sec < 59.5:
                # Grand Tableaux wide shot
                canvas.drawImage(env_snap, 0, 0)
                canvas.drawImage(broken_bow_snap, 0, 0)

                # Parashurama surrendered
                canvas.save()
                canvas.translate(-260, 0)
                canvas.drawImage(parashurama_surrender_snap, 0, 0)
                canvas.restore()

                # Shri Ram center
                canvas.drawImage(ram_peace_snap, 0, 0)

                # Laxman right
                canvas.save()
                canvas.translate(280, 0)
                canvas.drawImage(laxman_full_snap, 0, 0)
                canvas.restore()

                # Flower petals
                for pet in petals:
                    pet_y = (pet["y"] + pet["vy"] * f_idx * 0.9) % H
                    pet_x = pet["x"] + 15 * math.sin((f_idx * 0.05) + pet["angle"])
                    canvas.save()
                    canvas.translate(pet_x, pet_y)
                    p_paint = skia.Paint(Color=skia.ColorSetARGB(200, 255, 215, 0), AntiAlias=True) # Golden marigold
                    canvas.drawOval(skia.Rect(-pet["size"] * 0.5, -pet["size"], pet["size"] * 0.5, pet["size"]), p_paint)
                    canvas.restore()

            else:
                # HARD CUT TO VOID BLACK
                canvas.clear(skia.ColorBLACK)

                # Fade in 3D Golden Cliffhanger Badge
                if badge_snap:
                    badge_fade = min(1.0, (t_sec - 59.5) * 3.0)
                    canvas.save()
                    # Subtle floating hover
                    hover_y = 6.0 * math.sin((t_sec - 59.5) * 2.5)
                    canvas.translate(0, hover_y)
                    canvas.drawImage(badge_snap, 80, 780)
                    canvas.restore()

        # Embers
        if t_sec < 59.5:
            for pt in particles:
                py = (pt["y"] - pt["speed"] * f_idx * 0.8) % H
                canvas.drawCircle(pt["x"], py, pt["r"], skia.Paint(Color=skia.ColorSetARGB(170, 255, 235, 140), AntiAlias=True))

        # Vignette Guard
        if t_sec < 59.5:
            canvas.drawImage(vig_snap, 0, 0)

        # Pipe pixels
        surface.readPixels(pix_info, pix_buf, W * 4)
        pipe.stdin.write(pix_buf)

        if f_idx % 150 == 0:
            pct = (f_idx / total_frames) * 100
            elapsed = time.time() - render_start
            fps_curr = (f_idx + 1) / elapsed if elapsed > 0 else 0
            print(f"Rendered {f_idx}/{total_frames} frames ({pct:.1f}%) @ {fps_curr:.1f} FPS", flush=True)

    pipe.stdin.close()
    pipe.wait()
    render_dur = time.time() - render_start
    print(f"✅ Video frames rendered in {render_dur:.1f}s ({total_frames/render_dur:.1f} FPS)!")

    # Mux with Audio Master
    print("🎬 Muxing with 44.1kHz stereo audio master...")
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
    if temp_video.exists():
        temp_video.unlink()

    print(f"🎉 MASTER VIDEO DELIVERABLE CREATED: {final_video}")
    return str(final_video)

if __name__ == "__main__":
    main()
