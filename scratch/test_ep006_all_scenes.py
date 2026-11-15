import os
import sys
import json
import math
import random
from pathlib import Path
import numpy as np
import skia

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from studio_ramayana.character_engine.cinematic_character_v2 import (
    draw_cinematic_environment,
    draw_sacred_pinaka_bow,
    draw_mighty_kings_struggle,
    draw_maharaja_janak
)

W, H = 1080, 1920

# Load true India boundary points
with open(BASE_DIR / 'studio_ramayana/episodes/ep006/india_map_pts.json', 'r') as f:
    india_pts = json.load(f)

def geo_to_screen(lon, lat):
    sx = 70 + (lon - 67.0) / (98.0 - 67.0) * 940
    sy = 1580 - (lat - 6.5) / (38.0 - 6.5) * 1260
    return sx, sy

# --- SHOT 1: SNAPPED PINAKA BOW ---
def draw_snapped_pinaka_bow(cv, cx=540, cy=1200, scale=1.5, t=1.0):
    cv.save()
    cv.translate(cx, cy)
    cv.scale(scale, scale)

    # Fracture separation increases slightly or pulses
    sep = 28 + 4 * math.sin(t * 8)

    # Blinding Golden & Cyan Shiva Energy Aura at fracture point
    fracture_aura = skia.Paint(
        Shader=skia.GradientShader.MakeRadial(
            skia.Point(0, -320), 280,
            [skia.ColorSetARGB(230, 255, 235, 120), skia.ColorSetARGB(140, 60, 180, 255), skia.ColorTRANSPARENT],
            [0.0, 0.45, 1.0]
        ),
        AntiAlias=True
    )
    cv.drawCircle(0, -320, 280, fracture_aura)

    # Chariot Cart Base
    cart_p = skia.Paint(Color=skia.ColorSetARGB(255, 38, 32, 42), AntiAlias=True)
    cv.drawRect(skia.Rect(-240, 0, 240, 45), cart_p)
    cv.drawRect(skia.Rect(-240, 0, 240, 45), skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=3, Color=skia.ColorSetARGB(255, 215, 165, 45), AntiAlias=True))
    for wx in [-180, -90, 0, 90, 180]:
        cv.drawCircle(wx, 55, 28, skia.Paint(Color=skia.ColorSetARGB(255, 55, 45, 60), AntiAlias=True))
        cv.drawCircle(wx, 55, 28, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=3, Color=skia.ColorSetARGB(255, 215, 165, 45), AntiAlias=True))

    # LEFT HALF of Severed Bow (tilted left)
    cv.save()
    cv.translate(-sep, 0)
    cv.rotate(-6)
    left_half = skia.Path()
    left_half.moveTo(-220, -15)
    left_half.cubicTo(-260, -160, -180, -320, -15, -340)
    # Jagged fracture edge
    left_half.lineTo(-8, -332)
    left_half.lineTo(-20, -320)
    left_half.lineTo(-6, -305)
    left_half.cubicTo(-160, -290, -200, -15, -220, -15)
    left_half.close()
    bow_paint = skia.Paint(
        Shader=skia.GradientShader.MakeLinear(
            [skia.Point(-220, -15), skia.Point(0, -340)],
            [skia.ColorSetARGB(255, 30, 22, 28), skia.ColorSetARGB(255, 80, 52, 40)],
            [0.0, 1.0]
        ),
        AntiAlias=True
    )
    cv.drawPath(left_half, bow_paint)
    cv.drawPath(left_half, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=4, Color=skia.ColorSetARGB(255, 245, 195, 65), AntiAlias=True))
    # Snapped severed bowstring strand
    string_p = skia.Paint(StrokeWidth=3, Color=skia.ColorSetARGB(255, 255, 240, 140), AntiAlias=True)
    cv.drawLine(-220, -15, -45, -45, string_p)
    cv.drawCircle(-45, -45, 4, string_p)
    cv.restore()

    # RIGHT HALF of Severed Bow (tilted right)
    cv.save()
    cv.translate(sep, 0)
    cv.rotate(6)
    right_half = skia.Path()
    right_half.moveTo(220, -15)
    right_half.cubicTo(260, -160, 180, -320, 15, -340)
    # Jagged fracture edge
    right_half.lineTo(8, -332)
    right_half.lineTo(20, -320)
    right_half.lineTo(6, -305)
    right_half.cubicTo(160, -290, 200, -15, 220, -15)
    right_half.close()
    cv.drawPath(right_half, bow_paint)
    cv.drawPath(right_half, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=4, Color=skia.ColorSetARGB(255, 245, 195, 65), AntiAlias=True))
    # Snapped bowstring strand
    cv.drawLine(220, -15, 45, -45, string_p)
    cv.drawCircle(45, -45, 4, string_p)
    cv.restore()

    # Branching Electric Arcs jumping across the gap
    spark_paint = skia.Paint(StrokeWidth=3.5, Color=skia.ColorSetARGB(255, 160, 230, 255), AntiAlias=True)
    spark_glow = skia.Paint(StrokeWidth=8.0, Color=skia.ColorSetARGB(130, 80, 190, 255), AntiAlias=True)
    rnd = random.Random(int(t * 20))
    for _ in range(4):
        arc = skia.Path()
        arc.moveTo(-sep - 10, -320 + rnd.uniform(-30, 30))
        mid1_x = rnd.uniform(-10, 10)
        mid1_y = -320 + rnd.uniform(-40, 40)
        arc.lineTo(mid1_x, mid1_y)
        arc.lineTo(sep + 10, -320 + rnd.uniform(-30, 30))
        cv.drawPath(arc, spark_glow)
        cv.drawPath(arc, spark_paint)

    cv.restore()

# --- SHOT 2: ROYAL COURT SEISMIC SHOCKWAVE ---
def draw_court_shockwave(cv, t=1.0):
    draw_cinematic_environment(cv, "mithila_darbar", t, W, H)

    # Concentric Shockwave Rings across marble floor
    wave_center_x, wave_center_y = 540, 1420
    for r in [120, 260, 420, 600, 800]:
        r_dyn = (r + int(t * 350)) % 900
        alpha = max(0, int(220 * (1.0 - r_dyn / 900.0)))
        ring_p = skia.Paint(
            Color=skia.ColorSetARGB(alpha, 255, 240, 180),
            Style=skia.Paint.kStroke_Style,
            StrokeWidth=5.0,
            AntiAlias=True
        )
        cv.drawOval(skia.Rect(wave_center_x - r_dyn * 1.4, wave_center_y - r_dyn * 0.45, wave_center_x + r_dyn * 1.4, wave_center_y + r_dyn * 0.45), ring_p)

    # Distressed Kings cowering in panic (left & right)
    draw_mighty_kings_struggle(cv, 260, 1400, scale=1.3, strain=1.0)
    draw_mighty_kings_struggle(cv, 820, 1400, scale=1.3, strain=1.0)

    # Falling marble dust motes
    dust_rnd = random.Random(42)
    dust_paint = skia.Paint(Color=skia.ColorSetARGB(180, 255, 250, 220), AntiAlias=True)
    for _ in range(80):
        dx = dust_rnd.uniform(50, W - 50)
        dy = (dust_rnd.uniform(100, H) + t * 250) % H
        dr = dust_rnd.uniform(2.5, 6.0)
        cv.drawCircle(dx, dy, dr, dust_paint)

# --- SHOT 3: REAL INDIA MAP ---
def draw_real_india_map(cv, t=1.0):
    # Ocean Background
    ocean_paint = skia.Paint(
        Shader=skia.GradientShader.MakeLinear(
            [skia.Point(0, 0), skia.Point(W, H)],
            [skia.ColorSetARGB(255, 12, 22, 38), skia.ColorSetARGB(255, 8, 14, 24)],
            [0.0, 1.0]
        )
    )
    cv.drawRect(skia.Rect(0, 0, W, H), ocean_paint)

    # Cartographic Grid
    coord_paint = skia.Paint(Color=skia.ColorSetARGB(35, 100, 150, 200), Style=skia.Paint.kStroke_Style, StrokeWidth=1, AntiAlias=True)
    for gy in range(200, H, 140):
        cv.drawLine(0, gy, W, gy, coord_paint)
    for gx in range(100, W, 140):
        cv.drawLine(gx, 0, gx, H, coord_paint)

    # India Landmass
    india_path = skia.Path()
    start_x, start_y = geo_to_screen(india_pts[0][0], india_pts[0][1])
    india_path.moveTo(start_x, start_y)
    for p in india_pts[1:]:
        px, py = geo_to_screen(p[0], p[1])
        india_path.lineTo(px, py)
    india_path.close()

    # Drop shadow & fill
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

    # Coordinates
    mx, my = geo_to_screen(85.9, 26.7) # Mithila
    px, py = geo_to_screen(84.3, 18.9) # Mahendra

    # Red Seismic Shockwave Arc (Mithila to Mahendra)
    arc_path = skia.Path()
    arc_path.moveTo(mx, my)
    mid_x, mid_y = (mx + px)/2 + 65, (my + py)/2
    arc_path.quadTo(mid_x, mid_y, px, py)

    cv.drawPath(arc_path, skia.Paint(Color=skia.ColorSetARGB(200, 255, 45, 40), Style=skia.Paint.kStroke_Style, StrokeWidth=8, AntiAlias=True))
    cv.drawPath(arc_path, skia.Paint(Color=skia.ColorSetARGB(255, 255, 240, 150), Style=skia.Paint.kStroke_Style, StrokeWidth=3, AntiAlias=True))

    # Shockwave Rings from Mithila
    for r in [35, 75, 130]:
        cv.drawCircle(mx, my, r, skia.Paint(Color=skia.ColorSetARGB(max(0, 220 - int(r*1.1)), 255, 80, 50), Style=skia.Paint.kStroke_Style, StrokeWidth=2.5, AntiAlias=True))

    # Radar Pings at Mount Mahendra
    pulse_r = 30 + int(t * 80) % 90
    cv.drawCircle(px, py, pulse_r, skia.Paint(Color=skia.ColorSetARGB(max(0, 240 - pulse_r * 2), 255, 215, 0), Style=skia.Paint.kStroke_Style, StrokeWidth=3, AntiAlias=True))
    cv.drawCircle(px, py, 12, skia.Paint(Color=skia.ColorSetARGB(255, 255, 60, 40), AntiAlias=True))
    cv.drawCircle(px, py, 5, skia.Paint(Color=skia.ColorWHITE, AntiAlias=True))

    # Pop-Up Card 1: Mithila
    c1 = skia.Rect(mx - 150, my - 120, mx + 150, my - 40)
    cv.drawRoundRect(c1, 14, 14, skia.Paint(Color=skia.ColorSetARGB(235, 25, 15, 20), AntiAlias=True))
    cv.drawRoundRect(c1, 14, 14, skia.Paint(Color=skia.ColorSetARGB(255, 235, 185, 60), Style=skia.Paint.kStroke_Style, StrokeWidth=2.5, AntiAlias=True))
    # Pin needle
    pin1 = skia.Path()
    pin1.moveTo(mx - 10, my - 40)
    pin1.lineTo(mx + 10, my - 40)
    pin1.lineTo(mx, my - 5)
    pin1.close()
    cv.drawPath(pin1, skia.Paint(Color=skia.ColorSetARGB(255, 235, 185, 60), AntiAlias=True))

    # Pop-Up Card 2: Mount Mahendra (3,000 KM)
    c2 = skia.Rect(px - 180, py + 40, px + 180, py + 120)
    cv.drawRoundRect(c2, 14, 14, skia.Paint(Color=skia.ColorSetARGB(235, 15, 20, 32), AntiAlias=True))
    cv.drawRoundRect(c2, 14, 14, skia.Paint(Color=skia.ColorSetARGB(255, 255, 80, 60), Style=skia.Paint.kStroke_Style, StrokeWidth=2.5, AntiAlias=True))
    pin2 = skia.Path()
    pin2.moveTo(px - 10, py + 40)
    pin2.lineTo(px + 10, py + 40)
    pin2.lineTo(px, py + 12)
    pin2.close()
    cv.drawPath(pin2, skia.Paint(Color=skia.ColorSetARGB(255, 255, 80, 60), AntiAlias=True))

# --- SHOT 4: 3D PARASHU BATTLE AXE & 21 CONQUEST MARKERS ---
def draw_parashu_legend(cv, t=1.0):
    # Dark Crimson & Ash Background
    bg_p = skia.Paint(
        Shader=skia.GradientShader.MakeRadial(
            skia.Point(540, 960), 900,
            [skia.ColorSetARGB(255, 45, 12, 18), skia.ColorSetARGB(255, 15, 5, 8)],
            [0.0, 1.0]
        )
    )
    cv.drawRect(skia.Rect(0, 0, W, H), bg_p)

    # 21 Conquest Victory Markers (२१ विजय चक्र) arranged in dynamic radiating circle
    cx, cy = 540, 960
    radius = 380
    for i in range(21):
        angle = (i / 21.0) * 2 * math.pi + t * 0.2
        bx = cx + radius * math.cos(angle)
        by = cy + radius * math.sin(angle)
        # Victory Marker Ring & Star
        cv.drawCircle(bx, by, 22, skia.Paint(Color=skia.ColorSetARGB(220, 180, 25, 20), AntiAlias=True))
        cv.drawCircle(bx, by, 22, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=2.5, Color=skia.ColorSetARGB(255, 245, 195, 60), AntiAlias=True))
        cv.drawCircle(bx, by, 7, skia.Paint(Color=skia.ColorSetARGB(255, 255, 230, 140), AntiAlias=True))

    # Center Colossal 3D Battle Axe (Parashu)
    cv.save()
    cv.translate(cx, cy)
    cv.rotate(-18 + math.sin(t * 3) * 4)

    # Axe Shaft (Solid Bronze & Iron)
    shaft = skia.Rect(-18, -480, 18, 480)
    cv.drawRect(shaft, skia.Paint(Color=skia.ColorSetARGB(255, 75, 45, 30), AntiAlias=True))
    cv.drawRect(shaft, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=3, Color=skia.ColorSetARGB(255, 215, 165, 45), AntiAlias=True))
    # Gold bindings along shaft
    for sy in range(-420, 440, 90):
        cv.drawRect(skia.Rect(-22, sy, 22, sy + 18), skia.Paint(Color=skia.ColorSetARGB(255, 245, 195, 55), AntiAlias=True))

    # Crescent Blazing Blade of Parashu
    blade = skia.Path()
    blade.moveTo(18, -320)
    blade.cubicTo(140, -380, 280, -260, 320, -180)
    blade.cubicTo(260, -80, 140, -40, 18, -80)
    blade.close()

    blade_glow = skia.Paint(
        Shader=skia.GradientShader.MakeRadial(
            skia.Point(220, -180), 220,
            [skia.ColorSetARGB(220, 255, 80, 30), skia.ColorSetARGB(120, 255, 210, 50), skia.ColorTRANSPARENT],
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

# Import full-body drawing functions from scratch
from scratch.test_full_body_characters import (
    draw_full_body_parashurama,
    draw_full_body_laxman
)

# Test rendering snapshots of all 8 scenes
def run_test():
    print("Testing 8 Scene Renderers for EP006...")
    shots = []

    # Shot 1: Snapped Pinaka Bow
    s1 = skia.Surface(W, H)
    cv1 = s1.getCanvas()
    draw_cinematic_environment(cv1, "mithila_darbar", 1.0, W, H)
    draw_snapped_pinaka_bow(cv1, 540, 1380, scale=1.55, t=1.0)
    shots.append(s1.makeImageSnapshot())

    # Shot 2: Seismic Court Shockwave
    s2 = skia.Surface(W, H)
    cv2 = s2.getCanvas()
    draw_court_shockwave(cv2, t=1.5)
    shots.append(s2.makeImageSnapshot())

    # Shot 3: Real India Map
    s3 = skia.Surface(W, H)
    cv3 = s3.getCanvas()
    draw_real_india_map(cv3, t=1.2)
    shots.append(s3.makeImageSnapshot())

    # Shot 4: Parashu Legend & 21 Conquest Markers
    s4 = skia.Surface(W, H)
    cv4 = s4.getCanvas()
    draw_parashu_legend(cv4, t=1.0)
    shots.append(s4.makeImageSnapshot())

    # Shot 5: Full-Body Parashurama Entrance
    s5 = skia.Surface(W, H)
    cv5 = s5.getCanvas()
    draw_cinematic_environment(cv5, "mithila_darbar", 1.0, W, H)
    draw_full_body_parashurama(cv5, cx=540, ground_y=1660, scale=1.0)
    shots.append(s5.makeImageSnapshot())

    # Shot 6: Parashurama Roar Macro Close-up
    s6 = skia.Surface(W, H)
    cv6 = s6.getCanvas()
    draw_cinematic_environment(cv6, "mithila_darbar", 1.0, W, H)
    draw_full_body_parashurama(cv6, cx=540, ground_y=2300, scale=2.1) # Dramatic low macro close-up
    shots.append(s6.makeImageSnapshot())

    # Shot 7: Full-Body Kumar Laxman Fearless Smirk
    s7 = skia.Surface(W, H)
    cv7 = s7.getCanvas()
    draw_cinematic_environment(cv7, "mithila_darbar", 1.0, W, H)
    # Cowering king in background
    draw_mighty_kings_struggle(cv7, 240, 1420, scale=1.1, strain=1.0)
    draw_full_body_laxman(cv7, cx=580, ground_y=1660, scale=0.98)
    shots.append(s7.makeImageSnapshot())

    # Shot 8: Cliffhanger Badge on Black with Embers
    s8 = skia.Surface(W, H)
    cv8 = s8.getCanvas()
    cv8.clear(skia.ColorSetARGB(255, 8, 4, 10))
    # Load cliffhanger badge
    badge_path = BASE_DIR / "studio_ramayana" / "episodes" / "ep006" / "cliffhanger_badge.png"
    badge_img = skia.Image.MakeFromEncoded(skia.Data.MakeFromFileName(str(badge_path)))
    if badge_img:
        cv8.drawImage(badge_img, (W - badge_img.width()) / 2, (H - badge_img.height()) / 2)
    shots.append(s8.makeImageSnapshot())

    # Build 8-frame contact sheet (4 columns x 2 rows)
    cs_w, cs_h = 1920, 1080
    cs_surf = skia.Surface(cs_w, cs_h)
    cs_cv = cs_surf.getCanvas()
    cs_cv.clear(skia.ColorSetARGB(255, 12, 8, 16))

    thumb_w, thumb_h = 440, 480
    pad_x, pad_y = 32, 40
    for idx, snap in enumerate(shots):
        col = idx % 4
        row = idx // 4
        x = pad_x + col * (thumb_w + 24)
        y = pad_y + row * (thumb_h + 30)
        dest_rect = skia.Rect(x, y, x + thumb_w, y + thumb_h)
        cs_cv.drawImageRect(snap, dest_rect)
        cs_cv.drawRect(dest_rect, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=2.5, Color=skia.ColorSetARGB(255, 235, 185, 55), AntiAlias=True))

    out_cs = BASE_DIR / "studio_ramayana" / "episodes" / "ep006" / "ep006_8shot_verification.jpg"
    cs_img = cs_surf.makeImageSnapshot()
    cs_img.save(str(out_cs), skia.kJPEG)
    print(f"✅ Generated 8-shot verification contact sheet: {out_cs}")

if __name__ == "__main__":
    run_test()
