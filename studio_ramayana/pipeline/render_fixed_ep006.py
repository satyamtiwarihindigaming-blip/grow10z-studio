"""
GROW10Z — Ultra-Fast Cinema-Grade 8-Shot Production Director for EP006 (Pinaka Bhang & Divine Wrath)
100% Visual Directing Locked to Every Line:
- Shot 1 (0.0s - 5.2s): Snapped Pinaka Bow with Branching Electric Arcs & Camera Push-in (Line 00)
- Shot 2 (5.2s - 9.5s): Royal Court Seismic Shockwave, Trembling Pillars, Ducking Kings (Line 01)
- Shot 3 (9.5s - 16.5s): Real India Map, 3,000 KM Red Shockwave Vector Arc, Pop-Up Cards (Line 02)
- Shot 4 (16.5s - 22.8s): 3D Parashu Axe Slam with 21 Conquest Victory Markers (Line 03)
- Shot 5 (22.8s - 27.0s): Full-Body Bhagwan Parashurama Storming In with Glowing Axe & Sparks (Line 04)
- Shot 6 (27.0s - 32.0s): Parashurama Divine Roar Macro Close-up on Blazing Eyes & Teeth (Line 05)
- Shot 7 (32.0s - 40.5s): Full-Body Kumar Laxman Fearless Defiant Stance in 0 dB Silence (Line 06)
- Shot 8 (40.5s - 49.5s): Standoff Tension -> Void Black Cut -> 3D Golden Cliffhanger Badge (Line 07)
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
    draw_mighty_kings_struggle
)
from scratch.test_full_body_characters import (
    draw_full_body_parashurama,
    draw_full_body_laxman
)

EP_DIR = BASE_DIR / "studio_ramayana" / "episodes" / "ep006"
TIMELINE_FILE = EP_DIR / "timeline.json"
AUDIO_MASTER_FILE = EP_DIR / "audio_master.wav"
INDIA_PTS_FILE = EP_DIR / "india_map_pts.json"

W, H = 1080, 1920
FPS = 30

with open(INDIA_PTS_FILE, "r", encoding="utf-8") as f:
    india_pts = json.load(f)

def geo_to_screen(lon, lat):
    sx = 70 + (lon - 67.0) / (98.0 - 67.0) * 940
    sy = 1580 - (lat - 6.5) / (38.0 - 6.5) * 1260
    return sx, sy

def make_snapshot(draw_fn, width=W, height=H):
    surf = skia.Surface(width, height)
    cv = surf.getCanvas()
    draw_fn(cv)
    return surf.makeImageSnapshot()

# --- SHOT 1: SNAPPED PINAKA BOW COMPONENT ---
def draw_snapped_bow_halves(cv, cx=540, cy=1200, scale=1.5, sep=32):
    cv.save()
    cv.translate(cx, cy)
    cv.scale(scale, scale)

    # Fracture Shiva Aura
    fracture_aura = skia.Paint(
        Shader=skia.GradientShader.MakeRadial(
            skia.Point(0, -320), 300,
            [skia.ColorSetARGB(240, 255, 240, 140), skia.ColorSetARGB(150, 70, 190, 255), skia.ColorTRANSPARENT],
            [0.0, 0.45, 1.0]
        ),
        AntiAlias=True
    )
    cv.drawCircle(0, -320, 300, fracture_aura)

    # Chariot Cart Base
    cart_p = skia.Paint(Color=skia.ColorSetARGB(255, 38, 32, 42), AntiAlias=True)
    cv.drawRect(skia.Rect(-240, 0, 240, 45), cart_p)
    cv.drawRect(skia.Rect(-240, 0, 240, 45), skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=3, Color=skia.ColorSetARGB(255, 215, 165, 45), AntiAlias=True))
    for wx in [-180, -90, 0, 90, 180]:
        cv.drawCircle(wx, 55, 28, skia.Paint(Color=skia.ColorSetARGB(255, 55, 45, 60), AntiAlias=True))
        cv.drawCircle(wx, 55, 28, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=3, Color=skia.ColorSetARGB(255, 215, 165, 45), AntiAlias=True))

    bow_paint = skia.Paint(
        Shader=skia.GradientShader.MakeLinear(
            [skia.Point(-220, -15), skia.Point(0, -340)],
            [skia.ColorSetARGB(255, 30, 22, 28), skia.ColorSetARGB(255, 80, 52, 40)],
            [0.0, 1.0]
        ),
        AntiAlias=True
    )
    gold_border = skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=4, Color=skia.ColorSetARGB(255, 245, 195, 65), AntiAlias=True)
    string_p = skia.Paint(StrokeWidth=3, Color=skia.ColorSetARGB(255, 255, 240, 140), AntiAlias=True)

    # LEFT HALF of Severed Bow
    cv.save()
    cv.translate(-sep, 0)
    cv.rotate(-7)
    left_half = skia.Path()
    left_half.moveTo(-220, -15)
    left_half.cubicTo(-260, -160, -180, -320, -15, -340)
    left_half.lineTo(-8, -332)
    left_half.lineTo(-20, -320)
    left_half.lineTo(-6, -305)
    left_half.cubicTo(-160, -290, -200, -15, -220, -15)
    left_half.close()
    cv.drawPath(left_half, bow_paint)
    cv.drawPath(left_half, gold_border)
    cv.drawLine(-220, -15, -45, -45, string_p)
    cv.drawCircle(-45, -45, 4, string_p)
    cv.restore()

    # RIGHT HALF of Severed Bow
    cv.save()
    cv.translate(sep, 0)
    cv.rotate(7)
    right_half = skia.Path()
    right_half.moveTo(220, -15)
    right_half.cubicTo(260, -160, 180, -320, 15, -340)
    right_half.lineTo(8, -332)
    right_half.lineTo(20, -320)
    right_half.lineTo(6, -305)
    right_half.cubicTo(160, -290, 200, -15, 220, -15)
    right_half.close()
    cv.drawPath(right_half, bow_paint)
    cv.drawPath(right_half, gold_border)
    cv.drawLine(220, -15, 45, -45, string_p)
    cv.drawCircle(45, -45, 4, string_p)
    cv.restore()

    cv.restore()

# --- SHOT 3: BASE INDIA MAP ---
def draw_popup_card(cv, pin_x, pin_y, title, subtitle, is_origin=True):
    pin_col = skia.ColorSetARGB(255, 255, 215, 0) if is_origin else skia.ColorSetARGB(255, 255, 75, 55)
    cv.drawCircle(pin_x, pin_y, 14, skia.Paint(Color=pin_col, AntiAlias=True))
    cv.drawCircle(pin_x, pin_y, 6, skia.Paint(Color=skia.ColorWHITE, AntiAlias=True))

    card_x = pin_x - 340 if is_origin else pin_x + 60
    card_y = pin_y - 120 if is_origin else pin_y + 40
    card_w, card_h = 380, 95

    leader = skia.Path()
    leader.moveTo(pin_x, pin_y)
    leader.lineTo(card_x + (card_w if is_origin else 0), card_y + card_h/2)
    cv.drawPath(leader, skia.Paint(Color=pin_col, Style=skia.Paint.kStroke_Style, StrokeWidth=2.5, AntiAlias=True))

    shadow = skia.Paint(Color=skia.ColorSetARGB(180, 0, 0, 0), AntiAlias=True, ImageFilter=skia.ImageFilters.Blur(10, 10))
    cv.drawRoundRect(skia.Rect(card_x, card_y, card_x + card_w, card_y + card_h), 12, 12, shadow)

    card_bg = skia.Paint(Color=skia.ColorSetARGB(245, 18, 26, 40), AntiAlias=True)
    cv.drawRoundRect(skia.Rect(card_x, card_y, card_x + card_w, card_y + card_h), 12, 12, card_bg)

    border = skia.Paint(Color=pin_col, Style=skia.Paint.kStroke_Style, StrokeWidth=2.5, AntiAlias=True)
    cv.drawRoundRect(skia.Rect(card_x, card_y, card_x + card_w, card_y + card_h), 12, 12, border)

    cv.drawRoundRect(skia.Rect(card_x + 8, card_y + 8, card_x + 16, card_y + card_h - 8), 4, 4, skia.Paint(Color=pin_col, AntiAlias=True))

    font_title = skia.Font(skia.Typeface('Segoe UI', skia.FontStyle.Bold()), 23)
    cv.drawString(title, card_x + 28, card_y + 40, font_title, skia.Paint(Color=skia.ColorWHITE, AntiAlias=True))

    font_sub = skia.Font(skia.Typeface('Segoe UI', skia.FontStyle.Normal()), 16)
    cv.drawString(subtitle, card_x + 28, card_y + 75, font_sub, skia.Paint(Color=skia.ColorSetARGB(220, 200, 220, 240), AntiAlias=True))

def draw_distance_badge(cv, bx, by, text):
    bw, bh = 320, 54
    cv.drawRoundRect(skia.Rect(bx, by, bx + bw, by + bh), 27, 27, skia.Paint(Color=skia.ColorSetARGB(240, 220, 35, 30), AntiAlias=True))
    cv.drawRoundRect(skia.Rect(bx, by, bx + bw, by + bh), 27, 27, skia.Paint(Color=skia.ColorSetARGB(255, 255, 230, 150), Style=skia.Paint.kStroke_Style, StrokeWidth=2.5, AntiAlias=True))
    font = skia.Font(skia.Typeface('Segoe UI', skia.FontStyle.Bold()), 19)
    cv.drawString(text, bx + 22, by + 35, font, skia.Paint(Color=skia.ColorWHITE, AntiAlias=True))

def draw_compass_rose(cv, cx, cy):
    cv.drawCircle(cx, cy, 65, skia.Paint(Color=skia.ColorSetARGB(60, 215, 175, 75), Style=skia.Paint.kStroke_Style, StrokeWidth=2, AntiAlias=True))
    cv.drawCircle(cx, cy, 45, skia.Paint(Color=skia.ColorSetARGB(40, 215, 175, 75), Style=skia.Paint.kStroke_Style, StrokeWidth=1.5, AntiAlias=True))
    gold = skia.Paint(Color=skia.ColorSetARGB(255, 245, 200, 75), AntiAlias=True)
    north_p = skia.Path()
    north_p.moveTo(cx, cy - 65)
    north_p.lineTo(cx + 12, cy - 10)
    north_p.lineTo(cx, cy)
    north_p.close()
    cv.drawPath(north_p, gold)

def render_base_india_map(cv):
    ocean_paint = skia.Paint(
        Shader=skia.GradientShader.MakeLinear(
            [skia.Point(0, 0), skia.Point(W, H)],
            [skia.ColorSetARGB(255, 12, 22, 38), skia.ColorSetARGB(255, 8, 14, 24)],
            [0.0, 1.0]
        )
    )
    cv.drawRect(skia.Rect(0, 0, W, H), ocean_paint)

    coord_paint = skia.Paint(Color=skia.ColorSetARGB(35, 100, 150, 200), Style=skia.Paint.kStroke_Style, StrokeWidth=1, AntiAlias=True)
    for gy in range(200, H, 140):
        cv.drawLine(0, gy, W, gy, coord_paint)
    for gx in range(100, W, 140):
        cv.drawLine(gx, 0, gx, H, coord_paint)

    india_path = skia.Path()
    start_x, start_y = geo_to_screen(india_pts[0][0], india_pts[0][1])
    india_path.moveTo(start_x, start_y)
    for p in india_pts[1:]:
        px, py = geo_to_screen(p[0], p[1])
        india_path.lineTo(px, py)
    india_path.close()

    cv.drawPath(india_path, skia.Paint(Color=skia.ColorSetARGB(180, 0, 0, 0), AntiAlias=True, ImageFilter=skia.ImageFilters.Blur(15, 15)))
    land_fill = skia.Paint(
        Shader=skia.GradientShader.MakeLinear(
            [skia.Point(200, 320), skia.Point(700, 1580)],
            [skia.ColorSetARGB(255, 28, 48, 55), skia.ColorSetARGB(255, 22, 38, 44), skia.ColorSetARGB(255, 32, 45, 40)],
            [0.0, 0.5, 1.0]
        ),
        AntiAlias=True
    )
    cv.drawPath(india_path, land_fill)
    cv.drawPath(india_path, skia.Paint(Color=skia.ColorSetARGB(255, 215, 175, 75), Style=skia.Paint.kStroke_Style, StrokeWidth=3.5, AntiAlias=True))
    cv.drawPath(india_path, skia.Paint(Color=skia.ColorSetARGB(90, 120, 210, 255), Style=skia.Paint.kStroke_Style, StrokeWidth=8, AntiAlias=True))

    mx, my = geo_to_screen(85.9, 26.7) # Mithila
    px, py = geo_to_screen(84.3, 18.9) # Mahendra
    mid_x, mid_y = (mx + px)/2 + 65, (my + py)/2

    draw_popup_card(cv, mx, my, "Mithila (Mithila)", "Shiva Dhanush Bhang Sthal", is_origin=True)
    draw_popup_card(cv, px, py, "Mt. Mahendra (3,000 KM)", "Tapobhumi of Parashurama", is_origin=False)
    draw_distance_badge(cv, mid_x + 30, mid_y - 20, "3,000 KM Shockwave")
    draw_compass_rose(cv, 200, 1680)

# --- SHOT 4: 3D PARASHU AXE BASE ---
def render_parashu_legend_base(cv):
    bg_p = skia.Paint(
        Shader=skia.GradientShader.MakeRadial(
            skia.Point(540, 960), 900,
            [skia.ColorSetARGB(255, 48, 12, 18), skia.ColorSetARGB(255, 15, 5, 8)],
            [0.0, 1.0]
        )
    )
    cv.drawRect(skia.Rect(0, 0, W, H), bg_p)

    cx, cy = 540, 960
    radius = 380
    for i in range(21):
        angle = (i / 21.0) * 2 * math.pi
        bx = cx + radius * math.cos(angle)
        by = cy + radius * math.sin(angle)
        cv.drawCircle(bx, by, 22, skia.Paint(Color=skia.ColorSetARGB(220, 180, 25, 20), AntiAlias=True))
        cv.drawCircle(bx, by, 22, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=2.5, Color=skia.ColorSetARGB(255, 245, 195, 60), AntiAlias=True))
        cv.drawCircle(bx, by, 7, skia.Paint(Color=skia.ColorSetARGB(255, 255, 230, 140), AntiAlias=True))

def draw_animated_axe(cv, cx=540, cy=960, angle_deg=-18):
    cv.save()
    cv.translate(cx, cy)
    cv.rotate(angle_deg)

    shaft = skia.Rect(-18, -480, 18, 480)
    cv.drawRect(shaft, skia.Paint(Color=skia.ColorSetARGB(255, 75, 45, 30), AntiAlias=True))
    cv.drawRect(shaft, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=3, Color=skia.ColorSetARGB(255, 215, 165, 45), AntiAlias=True))
    for sy in range(-420, 440, 90):
        cv.drawRect(skia.Rect(-22, sy, 22, sy + 18), skia.Paint(Color=skia.ColorSetARGB(255, 245, 195, 55), AntiAlias=True))

    blade = skia.Path()
    blade.moveTo(18, -320)
    blade.cubicTo(140, -380, 280, -260, 320, -180)
    blade.cubicTo(260, -80, 140, -40, 18, -80)
    blade.close()

    blade_glow = skia.Paint(
        Shader=skia.GradientShader.MakeRadial(
            skia.Point(220, -180), 220,
            [skia.ColorSetARGB(230, 255, 80, 30), skia.ColorSetARGB(130, 255, 210, 50), skia.ColorTRANSPARENT],
            [0.0, 0.5, 1.0]
        ),
        AntiAlias=True
    )
    cv.drawCircle(220, -180, 220, blade_glow)

    blade_paint = skia.Paint(
        Shader=skia.GradientShader.MakeLinear(
            [skia.Point(18, -320), skia.Point(320, -180)],
            [skia.ColorSetARGB(255, 220, 225, 235), skia.ColorSetARGB(255, 140, 150, 165), skia.ColorSetARGB(255, 45, 50, 60)],
            [0.0, 0.4, 1.0]
        ),
        AntiAlias=True
    )
    cv.drawPath(blade, blade_paint)
    cv.drawPath(blade, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=4.5, Color=skia.ColorSetARGB(255, 255, 235, 120), AntiAlias=True))

    cv.restore()

def main():
    print("==================================================")
    print("🎬 RENDERING 8-SHOT CINEMATIC MASTERPIECE (EP006)")
    print("==================================================")
    t_start_total = time.time()

    total_duration = 49.50 # Exact audio master duration
    total_frames = int(total_duration * FPS) # 1485 frames

    temp_video = EP_DIR / "temp_video_8shot.mp4"
    final_video = EP_DIR / "ep006_final.mp4"

    # 1. Preload Static Badges & Background
    print("📜 Preloading background, manuscript & badges...")
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

    # Pre-render Base Real India Map Snapshot
    print("🗺️ Pre-rendering Real India Map base snapshot...")
    india_base_snap = make_snapshot(render_base_india_map)

    # Pre-render Parashu Legend Base Snapshot
    print("🪓 Pre-rendering Parashu Legend base snapshot...")
    parashu_base_snap = make_snapshot(render_parashu_legend_base)

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
    t_s1 = 5.20   # Shot 1: Snapped Bow (0.0s - 5.2s)
    t_s2 = 9.50   # Shot 2: Seismic Shockwave Court (5.2s - 9.5s)
    t_s3 = 16.50  # Shot 3: Real India Map (9.5s - 16.5s)
    t_s4 = 22.80  # Shot 4: Parashu Legend 21 Battles (16.5s - 22.8s)
    t_s5 = 27.00  # Shot 5: Parashurama Full Body Stride (22.8s - 27.0s)
    t_s6 = 32.00  # Shot 6: Parashurama Roar Macro (27.0s - 32.0s)
    t_s7 = 40.50  # Shot 7: Full Body Laxman Defiant Smirk (32.0s - 40.5s)
    t_cut_black = 42.00 # Standoff tension -> Hard cut to black (40.5s - 42.0s -> 42.0s+)

    print(f"🚀 Streaming {total_frames} frames into FFmpeg pipeline...")

    # Floating golden dust particles
    np.random.seed(42)
    particles = [{"x": random.randint(40, W-40), "y": random.randint(50, H-50), "speed": random.uniform(2.5, 6.0), "r": random.uniform(3.0, 7.5)} for _ in range(45)]

    # Map Arc Points
    mx, my = geo_to_screen(85.9, 26.7)
    px, py = geo_to_screen(84.3, 18.9)
    mid_x, mid_y = (mx + px)/2 + 65, (my + py)/2
    arc_path = skia.Path()
    arc_path.moveTo(mx, my)
    arc_path.quadTo(mid_x, mid_y, px, py)

    for frame_idx in range(total_frames):
        t_sec = frame_idx / FPS
        canvas.clear(skia.ColorSetARGB(255, 10, 6, 12))

        # --- SCENE SELECTION ---
        if t_sec < t_s1:
            # Shot 1: Snapped Pinaka Bow Macro Push-in & Dual-axis Shake
            shake_x = 7.0 * math.sin(t_sec * 50) * max(0.0, 1.0 - t_sec / 2.0)
            shake_y = 5.0 * math.cos(t_sec * 45) * max(0.0, 1.0 - t_sec / 2.0)
            zoom = 1.0 + 0.12 * (t_sec / t_s1)
            canvas.save()
            canvas.translate(W * 0.5 + shake_x, H * 0.5 + shake_y)
            canvas.scale(zoom, zoom)
            canvas.translate(-W * 0.5, -H * 0.5)
            canvas.drawImage(env_snap, 0, 0)
            sep = 32 + 6 * math.sin(t_sec * 8)
            draw_snapped_bow_halves(canvas, 540, 1380, scale=1.55, sep=sep)
            # Branching Electric Arcs jumping across the gap
            spark_paint = skia.Paint(StrokeWidth=3.5, Color=skia.ColorSetARGB(255, 160, 230, 255), AntiAlias=True)
            spark_glow = skia.Paint(StrokeWidth=8.0, Color=skia.ColorSetARGB(140, 80, 190, 255), AntiAlias=True)
            rnd = random.Random(int(t_sec * 30))
            for _ in range(5):
                arc = skia.Path()
                arc.moveTo(540 - sep - 18, 1380 - 480 + rnd.uniform(-40, 40))
                arc.lineTo(540 + rnd.uniform(-20, 20), 1380 - 480 + rnd.uniform(-50, 50))
                arc.lineTo(540 + sep + 18, 1380 - 480 + rnd.uniform(-40, 40))
                canvas.drawPath(arc, spark_glow)
                canvas.drawPath(arc, spark_paint)
            canvas.restore()

        elif t_sec < t_s2:
            # Shot 2: Seismic Court Shockwave
            zoom = 1.0 + 0.05 * ((t_sec - t_s1) / (t_s2 - t_s1))
            canvas.save()
            canvas.translate(W * 0.5, H * 0.5)
            canvas.scale(zoom, zoom)
            canvas.translate(-W * 0.5, -H * 0.5)
            canvas.drawImage(env_snap, 0, 0)
            canvas.drawImage(kings_snap, 0, 0)
            # Dynamic Shockwave Rings
            wave_center_x, wave_center_y = 540, 1420
            t_rel = t_sec - t_s1
            for r in [100, 260, 440, 640, 850]:
                r_dyn = (r + int(t_rel * 400)) % 1050
                alpha = max(0, int(230 * (1.0 - r_dyn / 1050.0)))
                ring_p = skia.Paint(
                    Color=skia.ColorSetARGB(alpha, 255, 240, 170),
                    Style=skia.Paint.kStroke_Style,
                    StrokeWidth=5.5,
                    AntiAlias=True
                )
                canvas.drawOval(skia.Rect(wave_center_x - r_dyn * 1.4, wave_center_y - r_dyn * 0.45, wave_center_x + r_dyn * 1.4, wave_center_y + r_dyn * 0.45), ring_p)
            canvas.restore()

        elif t_sec < t_s3:
            # Shot 3: Real India Map with Kashmir, Gujarat, Bay of Bengal
            zoom = 1.0 + 0.06 * ((t_sec - t_s2) / (t_s3 - t_s2))
            canvas.save()
            canvas.translate(W * 0.5, H * 0.5)
            canvas.scale(zoom, zoom)
            canvas.translate(-W * 0.5, -H * 0.5)
            canvas.drawImage(india_base_snap, 0, 0)
            # Dynamic Red Shockwave Arc & Pulsing Rings
            canvas.drawPath(arc_path, skia.Paint(Color=skia.ColorSetARGB(200, 255, 45, 40), Style=skia.Paint.kStroke_Style, StrokeWidth=8, AntiAlias=True))
            canvas.drawPath(arc_path, skia.Paint(Color=skia.ColorSetARGB(255, 255, 240, 150), Style=skia.Paint.kStroke_Style, StrokeWidth=3, AntiAlias=True))
            t_m = t_sec - t_s2
            for r in [35, 75, 130]:
                canvas.drawCircle(mx, my, r, skia.Paint(Color=skia.ColorSetARGB(max(0, 220 - int(r*1.1)), 255, 80, 50), Style=skia.Paint.kStroke_Style, StrokeWidth=2.5, AntiAlias=True))
            pulse_r = 30 + int(t_m * 80) % 90
            canvas.drawCircle(px, py, pulse_r, skia.Paint(Color=skia.ColorSetARGB(max(0, 240 - pulse_r * 2), 255, 215, 0), Style=skia.Paint.kStroke_Style, StrokeWidth=3, AntiAlias=True))
            canvas.restore()

        elif t_sec < t_s4:
            # Shot 4: Chronological Legend of Parashurama & 21 Conquests
            canvas.drawImage(parashu_base_snap, 0, 0)
            axe_rot = -18 + math.sin((t_sec - t_s3) * 3.5) * 6
            draw_animated_axe(canvas, cx=540, cy=960, angle_deg=axe_rot)

        elif t_sec < t_s5:
            # Shot 5: Full-Body Bhagwan Parashurama Entrance
            prog = (t_sec - t_s4) / (t_s5 - t_s4)
            canvas.drawImage(env_snap, 0, 0)
            stride_x = 35 * math.sin(prog * math.pi * 3)
            ground_y = 15 * abs(math.sin(prog * math.pi * 3))
            canvas.save()
            canvas.translate(stride_x, ground_y)
            canvas.drawImage(parashurama_full_snap, 0, 0)
            canvas.restore()

        elif t_sec < t_s6:
            # Shot 6: Parashurama Roar Macro Close-up on Blazing Eyes & Roaring Mouth
            roar_shake = 5.0 * math.sin(t_sec * 40)
            canvas.save()
            canvas.translate(roar_shake, 0)
            canvas.drawImage(env_snap, 0, 0)
            # Center right on head (y=-780 relative to ground_y=1660 -> y=880)
            canvas.save()
            canvas.translate(540, 960)
            macro_scale = 2.1 + 0.12 * math.sin((t_sec - t_s5) * 6)
            canvas.scale(macro_scale, macro_scale)
            canvas.translate(-540, -880)
            canvas.drawImage(parashurama_full_snap, 0, 0)
            canvas.restore()
            canvas.restore()

        elif t_sec < t_s7:
            # Shot 7: Full-Body Kumar Laxman Defiant Smirk in 0 dB Silence
            canvas.drawImage(env_snap, 0, 0)
            draw_mighty_kings_struggle(canvas, 240, 1420, scale=1.1, strain=1.0)
            lax_breath = 1.0 + 0.015 * math.sin((t_sec - t_s6) * 3.0)
            canvas.save()
            canvas.translate(580, 1660)
            canvas.scale(lax_breath, lax_breath)
            canvas.translate(-580, -1660)
            canvas.drawImage(laxman_full_snap, 0, 0)
            canvas.restore()

        elif t_sec < t_cut_black:
            # Shot 8A (40.5s - 42.0s): Standoff Face-off Tension
            canvas.drawImage(env_snap, 0, 0)
            # Left side Parashurama
            canvas.save()
            canvas.translate(-220, 20)
            canvas.drawImage(parashurama_full_snap, 0, 0)
            canvas.restore()
            # Right side Laxman
            canvas.save()
            canvas.translate(180, 20)
            canvas.drawImage(laxman_full_snap, 0, 0)
            canvas.restore()

        else:
            # Shot 8B (42.0s - 49.5s): Void Black Hard Cut + 3D Golden Cliffhanger Badge
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
        if t_sec < t_cut_black and t_sec > t_s3:
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
