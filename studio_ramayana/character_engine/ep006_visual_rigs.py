"""
EP006 VISUAL RIGS & RENDERING ENGINE
Styles:
- Indian Miniature + 24K Gold Leaf (Pinaka & Darbar)
- Antique Blueprint / 3D Cartography (Bharatvarsha Map)
- Mythological Comic Book + Ink Wash (Parashurama Entrance & Roar)
- Luminous Gold Line (Laxman Defiant Smirk)
"""

import math
import numpy as np
import skia

W, H = 1080, 1920

def draw_broken_pinaka_bow(canvas, cx=540, cy=1380, scale=1.5, snap_offset=45.0):
    """
    Renders Shiva's Pinaka Bow snapped cleanly into two halves with jagged golden fracture,
    branching lightning arcs, and blinding cosmic energy burst.
    """
    canvas.save()
    canvas.translate(cx, cy)
    canvas.scale(scale, scale)

    # 1. Radiant Energy Burst at Fracture Point (Center)
    burst_paint = skia.Paint(
        Shader=skia.GradientShader.MakeRadial(
            skia.Point(0, -60), 220,
            [skia.ColorSetARGB(255, 255, 250, 210), skia.ColorSetARGB(180, 255, 180, 40), skia.ColorSetARGB(0, 255, 100, 0)],
            [0.0, 0.45, 1.0]
        ),
        AntiAlias=True
    )
    canvas.drawCircle(0, -60, 220, burst_paint)

    # 2. Golden Altar Cart (Eight-Wheeled Iron Cart with Gold Trim)
    cart_paint = skia.Paint(Color=skia.ColorSetARGB(255, 35, 30, 45), AntiAlias=True)
    canvas.drawRoundRect(skia.Rect(-280, 30, 280, 75), 12, 12, cart_paint)
    
    gold_trim = skia.Paint(Color=skia.ColorSetARGB(255, 245, 200, 75), Style=skia.Paint.kStroke_Style, StrokeWidth=5, AntiAlias=True)
    canvas.drawRoundRect(skia.Rect(-280, 30, 280, 75), 12, 12, gold_trim)

    # 8 Iron Wheels
    for wx in [-240, -170, -100, -30, 40, 110, 180, 250]:
        canvas.drawCircle(wx, 85, 24, cart_paint)
        canvas.drawCircle(wx, 85, 24, gold_trim)
        canvas.drawCircle(wx, 85, 10, skia.Paint(Color=skia.ColorSetARGB(255, 245, 200, 75), AntiAlias=True))

    # 3. Left Half of Broken Bow (Tilted left by snap_offset)
    canvas.save()
    canvas.translate(-snap_offset * 0.7, snap_offset * 0.3)
    canvas.rotate(-14)
    
    # Left bow limb (Arching down to cart)
    left_path = skia.Path()
    left_path.moveTo(-20, -60)
    left_path.cubicTo(-120, -180, -260, -140, -270, 30)
    left_path.lineTo(-245, 30)
    left_path.cubicTo(-235, -120, -110, -150, -15, -45)
    left_path.close()

    gold_body = skia.Paint(
        Shader=skia.GradientShader.MakeLinear(
            [skia.Point(-270, 0), skia.Point(0, -180)],
            [skia.ColorSetARGB(255, 215, 150, 40), skia.ColorSetARGB(255, 255, 235, 130), skia.ColorSetARGB(255, 180, 110, 20)],
            [0.0, 0.5, 1.0]
        ),
        AntiAlias=True
    )
    canvas.drawPath(left_path, gold_body)
    canvas.drawPath(left_path, skia.Paint(Color=skia.ColorSetARGB(255, 255, 240, 180), Style=skia.Paint.kStroke_Style, StrokeWidth=3, AntiAlias=True))
    
    # Jagged fracture edge on left half
    frac_left = skia.Path()
    frac_left.moveTo(-20, -60)
    frac_left.lineTo(-12, -52)
    frac_left.lineTo(-18, -48)
    frac_left.lineTo(-15, -45)
    canvas.drawPath(frac_left, skia.Paint(Color=skia.ColorWHITE, Style=skia.Paint.kStroke_Style, StrokeWidth=4, AntiAlias=True))
    canvas.restore()

    # 4. Right Half of Broken Bow (Tilted right by snap_offset)
    canvas.save()
    canvas.translate(snap_offset * 0.7, snap_offset * 0.3)
    canvas.rotate(14)

    right_path = skia.Path()
    right_path.moveTo(20, -60)
    right_path.cubicTo(120, -180, 260, -140, 270, 30)
    right_path.lineTo(245, 30)
    right_path.cubicTo(235, -120, 110, -150, 15, -45)
    right_path.close()

    canvas.drawPath(right_path, gold_body)
    canvas.drawPath(right_path, skia.Paint(Color=skia.ColorSetARGB(255, 255, 240, 180), Style=skia.Paint.kStroke_Style, StrokeWidth=3, AntiAlias=True))

    # Jagged fracture edge on right half
    frac_right = skia.Path()
    frac_right.moveTo(20, -60)
    frac_right.lineTo(12, -52)
    frac_right.lineTo(18, -48)
    frac_right.lineTo(15, -45)
    canvas.drawPath(frac_right, skia.Paint(Color=skia.ColorWHITE, Style=skia.Paint.kStroke_Style, StrokeWidth=4, AntiAlias=True))
    canvas.restore()

    # 5. Snapped Bowstring (Curling chaotically in two severed strands)
    string_paint = skia.Paint(Color=skia.ColorSetARGB(240, 255, 255, 220), Style=skia.Paint.kStroke_Style, StrokeWidth=3.5, AntiAlias=True)
    str_left = skia.Path()
    str_left.moveTo(-270, 30)
    str_left.cubicTo(-210, -30, -110, 10, -50, -20)
    canvas.drawPath(str_left, string_paint)

    str_right = skia.Path()
    str_right.moveTo(270, 30)
    str_right.cubicTo(210, -30, 110, 10, 50, -20)
    canvas.drawPath(str_right, string_paint)

    # 6. Branching Electric Lightning Arcs from Center Fracture
    np.random.seed(99)
    for _ in range(12):
        l_path = skia.Path()
        l_path.moveTo(np.random.uniform(-10, 10), -55)
        curr_x, curr_y = 0, -55
        for _ in range(5):
            curr_x += np.random.uniform(-45, 45)
            curr_y += np.random.uniform(-40, 40)
            l_path.lineTo(curr_x, curr_y)
        
        # Outer blue-cyan aura
        canvas.drawPath(l_path, skia.Paint(Color=skia.ColorSetARGB(180, 120, 220, 255), Style=skia.Paint.kStroke_Style, StrokeWidth=5, AntiAlias=True))
        # Inner pure white core
        canvas.drawPath(l_path, skia.Paint(Color=skia.ColorWHITE, Style=skia.Paint.kStroke_Style, StrokeWidth=2, AntiAlias=True))

    canvas.restore()


def draw_ancient_seismic_map(canvas, W=1080, H=1920, progress=0.75):
    """
    Renders Ancient Bharatvarsha 3D Perspective Map in Antique Blueprint / Cartography style:
    Mithila in the north-east, Mount Mahendra in the south-east, glowing shockwave trajectory,
    compass rose, terrain topography contours, and Sanskrit place markers.
    """
    # 1. Antique Parchment & Blueprint Background
    bg_paint = skia.Paint(
        Shader=skia.GradientShader.MakeLinear(
            [skia.Point(0, 0), skia.Point(W, H)],
            [skia.ColorSetARGB(255, 16, 26, 44), skia.ColorSetARGB(255, 10, 16, 28)],
            [0.0, 1.0]
        )
    )
    canvas.drawRect(skia.Rect(0, 0, W, H), bg_paint)

    # 2. Technical Blueprint Coordinate Grid
    grid_paint = skia.Paint(Color=skia.ColorSetARGB(40, 140, 180, 220), Style=skia.Paint.kStroke_Style, StrokeWidth=1, AntiAlias=True)
    for gx in range(0, W, 80):
        canvas.drawLine(gx, 0, gx, H, grid_paint)
    for gy in range(0, H, 80):
        canvas.drawLine(0, gy, W, gy, grid_paint)

    # 3. Topographic Mountain Contours (Himalayas & Eastern Ghats)
    topo_paint = skia.Paint(Color=skia.ColorSetARGB(55, 180, 210, 240), Style=skia.Paint.kStroke_Style, StrokeWidth=2, AntiAlias=True)
    # Himalayan arc in north
    him_path = skia.Path()
    him_path.moveTo(80, 360)
    him_path.cubicTo(320, 280, 720, 310, 980, 420)
    canvas.drawPath(him_path, topo_paint)

    him_path2 = skia.Path()
    him_path2.moveTo(110, 410)
    him_path2.cubicTo(340, 340, 700, 360, 960, 460)
    canvas.drawPath(him_path2, topo_paint)

    # Sacred Rivers (Ganga & Yamuna path)
    river_paint = skia.Paint(Color=skia.ColorSetARGB(130, 80, 180, 235), Style=skia.Paint.kStroke_Style, StrokeWidth=4, AntiAlias=True)
    ganga = skia.Path()
    ganga.moveTo(280, 400)
    ganga.cubicTo(450, 560, 580, 680, 820, 780)
    canvas.drawPath(ganga, river_paint)

    # Ocean Coastline (Bay of Bengal / Purva Samudra)
    coast_paint = skia.Paint(Color=skia.ColorSetARGB(160, 70, 150, 200), Style=skia.Paint.kStroke_Style, StrokeWidth=3, AntiAlias=True)
    coast = skia.Path()
    coast.moveTo(820, 780)
    coast.cubicTo(740, 1020, 680, 1280, 620, 1600)
    canvas.drawPath(coast, coast_paint)

    # 4. Key City Coordinates
    # Mithila: (x=720, y=580)
    # Mahendra Parvat: (x=660, y=1340)
    mx, my = 720, 580
    px, py = 660, 1340

    # 5. Seismic Shockwave Trajectory Vector from Mithila to Mahendra
    traj_path = skia.Path()
    traj_path.moveTo(mx, my)
    # Curved path along geography
    ctrl_x, ctrl_y = 780, 960
    traj_path.quadTo(ctrl_x, ctrl_y, px, py)

    # Neon Red Seismic Pulse Line
    pulse_outer = skia.Paint(Color=skia.ColorSetARGB(180, 255, 60, 50), Style=skia.Paint.kStroke_Style, StrokeWidth=8, AntiAlias=True)
    pulse_core = skia.Paint(Color=skia.ColorSetARGB(255, 255, 230, 140), Style=skia.Paint.kStroke_Style, StrokeWidth=3, AntiAlias=True)
    canvas.drawPath(traj_path, pulse_outer)
    canvas.drawPath(traj_path, pulse_core)

    # Concentric Shockwave Rings expanding from Mithila
    for r in [40, 90, 150, 220, 310]:
        canvas.drawCircle(mx, my, r, skia.Paint(Color=skia.ColorSetARGB(max(0, 190 - int(r*0.6)), 255, 100, 50), Style=skia.Paint.kStroke_Style, StrokeWidth=2.5, AntiAlias=True))

    # Target Radar Ping at Mount Mahendra
    for pr in [30, 65, 110]:
        canvas.drawCircle(px, py, pr, skia.Paint(Color=skia.ColorSetARGB(max(0, 220 - int(pr*1.8)), 255, 220, 40), Style=skia.Paint.kStroke_Style, StrokeWidth=3, AntiAlias=True))
    canvas.drawCircle(px, py, 14, skia.Paint(Color=skia.ColorSetARGB(255, 255, 80, 40), AntiAlias=True))
    canvas.drawCircle(px, py, 6, skia.Paint(Color=skia.ColorWHITE, AntiAlias=True))

    # 6. Ancient Cartography Callout Badges
    # Mithila Pin
    canvas.drawCircle(mx, my, 12, skia.Paint(Color=skia.ColorSetARGB(255, 255, 215, 0), AntiAlias=True))
    canvas.drawCircle(mx, my, 5, skia.Paint(Color=skia.ColorWHITE, AntiAlias=True))
    
    # Distance callout indicator
    canvas.drawLine(mx + 20, my, mx + 160, my - 40, skia.Paint(Color=skia.ColorSetARGB(200, 255, 215, 0), StrokeWidth=2, AntiAlias=True))
    dist_badge = skia.Paint(Color=skia.ColorSetARGB(220, 20, 30, 50), AntiAlias=True)
    canvas.drawRoundRect(skia.Rect(mx + 160, my - 70, mx + 380, my - 15), 8, 8, dist_badge)
    canvas.drawRoundRect(skia.Rect(mx + 160, my - 70, mx + 380, my - 15), 8, 8, skia.Paint(Color=skia.ColorSetARGB(200, 255, 215, 0), Style=skia.Paint.kStroke_Style, StrokeWidth=1.5, AntiAlias=True))

    # Sanskrit Headers & Compass Rose
    # Compass Rose at bottom left
    cx_rose, cy_rose = 200, 1600
    canvas.drawCircle(cx_rose, cy_rose, 70, skia.Paint(Color=skia.ColorSetARGB(60, 255, 215, 0), Style=skia.Paint.kStroke_Style, StrokeWidth=2, AntiAlias=True))
    # 4 points
    for ang in [0, 90, 180, 270]:
        rad = math.radians(ang)
        canvas.drawLine(cx_rose, cy_rose, cx_rose + 90 * math.cos(rad), cy_rose + 90 * math.sin(rad), skia.Paint(Color=skia.ColorSetARGB(200, 255, 215, 0), StrokeWidth=2, AntiAlias=True))


def draw_bhagwan_parashurama(canvas, cx=540, cy=1120, scale=1.75, fury=1.0):
    """
    Renders Bhagwan Parashurama (Avatar of Vishnu, disciple of Shiva):
    Blazing red eyes, fierce furrowed brow, sacred Tripundra on forehead,
    wild flying jatas (matted hair), tiger-skin angavastra, Rudraksha malas,
    and his divine Battle Axe (Parashu) crackling with celestial fire!
    """
    canvas.save()
    canvas.translate(cx, cy)
    canvas.scale(scale, scale)

    # 1. Tempest Fury Aura (Dark Crimson & Ink Wash Smoke)
    fury_aura = skia.Paint(
        Shader=skia.GradientShader.MakeRadial(
            skia.Point(0, -120), 320,
            [skia.ColorSetARGB(220, 180, 20, 15), skia.ColorSetARGB(120, 80, 8, 10), skia.ColorSetARGB(0, 0, 0, 0)],
            [0.0, 0.6, 1.0]
        ),
        AntiAlias=True
    )
    canvas.drawCircle(0, -120, 320, fury_aura)

    # 2. Wild Flying Jatas (Matted Hair blowing in storm wind)
    hair_paint = skia.Paint(Color=skia.ColorSetARGB(255, 25, 20, 22), AntiAlias=True)
    for h_angle in [-50, -35, -20, 0, 20, 35, 50, -65, 65]:
        hp = skia.Path()
        hp.moveTo(0, -220)
        curl_x = 180 * math.sin(math.radians(h_angle))
        curl_y = -320 + 80 * math.cos(math.radians(h_angle))
        hp.quadTo(curl_x * 0.7, curl_y - 30, curl_x, curl_y)
        hp.quadTo(curl_x * 0.8, curl_y + 40, 0, -180)
        hp.close()
        canvas.drawPath(hp, hair_paint)

    # 3. Broad Muscular Torso (Tanned Warrior Sage Skin)
    skin_paint = skia.Paint(
        Shader=skia.GradientShader.MakeLinear(
            [skia.Point(0, -120), skia.Point(0, 140)],
            [skia.ColorSetARGB(255, 205, 140, 95), skia.ColorSetARGB(255, 160, 95, 55)],
            [0.0, 1.0]
        ),
        AntiAlias=True
    )
    torso = skia.Path()
    torso.moveTo(-110, -80)
    torso.lineTo(110, -80)
    torso.lineTo(85, 160)
    torso.lineTo(-85, 160)
    torso.close()
    canvas.drawPath(torso, skin_paint)

    # Tiger Skin Angavastra across chest (diagonal sash)
    tiger_paint = skia.Paint(Color=skia.ColorSetARGB(255, 215, 130, 35), AntiAlias=True)
    tiger_stripes = skia.Paint(Color=skia.ColorSetARGB(255, 30, 20, 15), StrokeWidth=5, Style=skia.Paint.kStroke_Style, AntiAlias=True)
    sash = skia.Path()
    sash.moveTo(-115, -75)
    sash.lineTo(-65, -80)
    sash.lineTo(95, 150)
    sash.lineTo(55, 160)
    sash.close()
    canvas.drawPath(sash, tiger_paint)
    # Stripes on tiger skin
    for sy in range(-40, 140, 25):
        canvas.drawLine(-80 + sy*0.8, sy - 15, -30 + sy*0.8, sy + 10, tiger_stripes)

    # Rudraksha Malas (Dark brown beads around neck)
    rudra_paint = skia.Paint(Color=skia.ColorSetARGB(255, 75, 40, 25), AntiAlias=True)
    for bx in range(-70, 75, 15):
        by = -70 + int(25 * math.cos(bx / 50.0))
        canvas.drawCircle(bx, by, 7, rudra_paint)
        canvas.drawCircle(bx, by, 7, skia.Paint(Color=skia.ColorSetARGB(180, 245, 180, 50), Style=skia.Paint.kStroke_Style, StrokeWidth=1.5, AntiAlias=True))

    # 4. Fierce Face & Burning Red Eyes
    face = skia.Path()
    face.moveTo(-45, -200)
    face.cubicTo(-55, -150, -45, -95, 0, -85)
    face.cubicTo(45, -95, 55, -150, 45, -200)
    face.close()
    canvas.drawPath(face, skin_paint)

    # Dense ascetic beard (Rishi shmashru)
    beard_paint = skia.Paint(Color=skia.ColorSetARGB(255, 35, 28, 30), AntiAlias=True)
    beard = skia.Path()
    beard.moveTo(-48, -135)
    beard.cubicTo(-60, -70, -20, 10, 0, 30)
    beard.cubicTo(20, 10, 60, -70, 48, -135)
    beard.close()
    canvas.drawPath(beard, beard_paint)

    # Sacred Tripundra on forehead (3 white ash lines)
    bhasma_paint = skia.Paint(Color=skia.ColorSetARGB(220, 240, 240, 245), StrokeWidth=3, Style=skia.Paint.kStroke_Style, AntiAlias=True)
    for ty in [-180, -174, -168]:
        canvas.drawLine(-22, ty, 22, ty, bhasma_paint)
    # Red Kumkum center dot
    canvas.drawCircle(0, -174, 3.5, skia.Paint(Color=skia.ColorSetARGB(255, 200, 20, 20), AntiAlias=True))

    # Burning Red Eyes (Glowing like live coals)
    eye_glow = skia.Paint(Color=skia.ColorSetARGB(200, 255, 40, 20), AntiAlias=True)
    for ex in [-22, 22]:
        canvas.drawCircle(ex, -145, 10, eye_glow)
        canvas.drawCircle(ex, -145, 5, skia.Paint(Color=skia.ColorSetARGB(255, 255, 230, 120), AntiAlias=True))
        canvas.drawCircle(ex, -145, 2, skia.Paint(Color=skia.ColorWHITE, AntiAlias=True))

    # Furrowed Angry Eyebrows
    brow_paint = skia.Paint(Color=skia.ColorSetARGB(255, 20, 15, 15), StrokeWidth=4, Style=skia.Paint.kStroke_Style, AntiAlias=True)
    canvas.drawLine(-34, -155, -10, -148, brow_paint)
    canvas.drawLine(34, -155, 10, -148, brow_paint)

    # 5. Divine Battle Axe (Parashu) in Right Hand
    # Shaft (Long wooden handle wrapped in leather)
    shaft_paint = skia.Paint(Color=skia.ColorSetARGB(255, 95, 55, 30), StrokeWidth=14, Style=skia.Paint.kStroke_Style, AntiAlias=True)
    canvas.drawLine(140, -280, 80, 220, shaft_paint)
    canvas.drawLine(140, -280, 80, 220, skia.Paint(Color=skia.ColorSetARGB(255, 220, 180, 60), StrokeWidth=2, Style=skia.Paint.kStroke_Style, AntiAlias=True))

    # Colossal Crescent Steel Blade of Parashu
    blade = skia.Path()
    blade.moveTo(135, -240)
    blade.cubicTo(210, -290, 260, -220, 250, -140)
    blade.cubicTo(230, -70, 170, -120, 125, -160)
    blade.close()

    steel_grad = skia.Paint(
        Shader=skia.GradientShader.MakeLinear(
            [skia.Point(130, -240), skia.Point(250, -140)],
            [skia.ColorSetARGB(255, 240, 245, 255), skia.ColorSetARGB(255, 140, 160, 185), skia.ColorSetARGB(255, 80, 95, 115)],
            [0.0, 0.5, 1.0]
        ),
        AntiAlias=True
    )
    canvas.drawPath(blade, steel_grad)
    # Razor Sharp Edge Glow
    canvas.drawPath(blade, skia.Paint(Color=skia.ColorWHITE, StrokeWidth=3, Style=skia.Paint.kStroke_Style, AntiAlias=True))

    # Crackling Sparks on Axe Blade
    for spx, spy in [(240, -210), (245, -160), (220, -110), (190, -260)]:
        canvas.drawCircle(spx, spy, 4, skia.Paint(Color=skia.ColorSetARGB(255, 255, 220, 40), AntiAlias=True))

    canvas.restore()


def draw_cinematic_laxman(canvas, cx=540, cy=1140, scale=1.75, smirk=1.0):
    """
    Renders Kumar Laxman (Avatar of Sheshanaga):
    Fearless youthful prince with fair golden complexion, arched eyebrow,
    confident amused smirk, hand resting on gem-studded sword pommel,
    royal silk pitambara, and glowing serpent-gold divine halo!
    """
    canvas.save()
    canvas.translate(cx, cy)
    canvas.scale(scale, scale)

    # 1. Radiant Serpent-Gold Halo (Sheshanaga Radiance)
    halo_paint = skia.Paint(
        Shader=skia.GradientShader.MakeRadial(
            skia.Point(0, -160), 180,
            [skia.ColorSetARGB(240, 255, 235, 140), skia.ColorSetARGB(130, 255, 195, 50), skia.ColorSetARGB(0, 255, 160, 0)],
            [0.0, 0.5, 1.0]
        ),
        AntiAlias=True
    )
    canvas.drawCircle(0, -160, 180, halo_paint)

    # 2. Regal Royal Attire (Silk Pitambara & Golden Armor Breastplate)
    skin_paint = skia.Paint(
        Shader=skia.GradientShader.MakeLinear(
            [skia.Point(0, -180), skia.Point(0, 100)],
            [skia.ColorSetARGB(255, 250, 215, 175), skia.ColorSetARGB(255, 230, 185, 140)],
            [0.0, 1.0]
        ),
        AntiAlias=True
    )
    
    # Torso with Royal Gold Chest Armor
    torso = skia.Path()
    torso.moveTo(-90, -90)
    torso.lineTo(90, -90)
    torso.lineTo(70, 150)
    torso.lineTo(-70, 150)
    torso.close()
    canvas.drawPath(torso, skin_paint)

    # Gold Armor Cuirass
    armor_paint = skia.Paint(
        Shader=skia.GradientShader.MakeLinear(
            [skia.Point(-80, -90), skia.Point(80, 140)],
            [skia.ColorSetARGB(255, 255, 225, 110), skia.ColorSetARGB(255, 210, 160, 45)],
            [0.0, 1.0]
        ),
        AntiAlias=True
    )
    armor_path = skia.Path()
    armor_path.moveTo(-80, -85)
    armor_path.lineTo(80, -85)
    armor_path.lineTo(60, 110)
    armor_path.lineTo(-60, 110)
    armor_path.close()
    canvas.drawPath(armor_path, armor_paint)
    canvas.drawPath(armor_path, skia.Paint(Color=skia.ColorSetARGB(255, 255, 245, 180), StrokeWidth=3, Style=skia.Paint.kStroke_Style, AntiAlias=True))

    # Royal Pearl Necklace (Kanthahara)
    pearl_paint = skia.Paint(Color=skia.ColorSetARGB(255, 255, 255, 250), AntiAlias=True)
    for px in range(-55, 60, 12):
        py = -75 + int(20 * math.cos(px / 40.0))
        canvas.drawCircle(px, py, 5.5, pearl_paint)

    # 3. Youthful Handsome Prince Face
    face = skia.Path()
    face.moveTo(-42, -195)
    face.cubicTo(-50, -145, -40, -100, 0, -90)
    face.cubicTo(40, -100, 50, -145, 42, -195)
    face.close()
    canvas.drawPath(face, skin_paint)

    # Royal Golden Mukut (Crown) with Ruby Gem
    crown = skia.Path()
    crown.moveTo(-48, -190)
    crown.lineTo(-30, -250)
    crown.lineTo(0, -275)
    crown.lineTo(30, -250)
    crown.lineTo(48, -190)
    crown.close()
    canvas.drawPath(crown, armor_paint)
    canvas.drawPath(crown, skia.Paint(Color=skia.ColorSetARGB(255, 255, 245, 180), StrokeWidth=2.5, Style=skia.Paint.kStroke_Style, AntiAlias=True))
    canvas.drawCircle(0, -230, 7, skia.Paint(Color=skia.ColorSetARGB(255, 225, 25, 35), AntiAlias=True))

    # Tilak (Urdhva Pundra with Chandan & Vermilion)
    canvas.drawLine(0, -175, 0, -155, skia.Paint(Color=skia.ColorSetARGB(255, 225, 30, 30), StrokeWidth=3, AntiAlias=True))

    # Fearless Sparkling Eyes
    for ex in [-18, 18]:
        canvas.drawOval(skia.Rect(ex - 8, -150, ex + 8, -140), skia.Paint(Color=skia.ColorWHITE, AntiAlias=True))
        canvas.drawCircle(ex, -145, 4, skia.Paint(Color=skia.ColorSetARGB(255, 20, 20, 25), AntiAlias=True))
        canvas.drawCircle(ex + 1, -146, 1.5, skia.Paint(Color=skia.ColorWHITE, AntiAlias=True))

    # Arched Arrogant/Confident Eyebrows (Right eyebrow raised in amused challenge)
    brow_paint = skia.Paint(Color=skia.ColorSetARGB(255, 30, 25, 25), StrokeWidth=3.5, Style=skia.Paint.kStroke_Style, AntiAlias=True)
    canvas.drawLine(-27, -158, -9, -156, brow_paint)
    canvas.drawLine(9, -157, 28, -164, brow_paint) # Raised right eyebrow!

    # Confident Defiant Smirk (Half-Smile)
    smirk_path = skia.Path()
    smirk_path.moveTo(-12, -118)
    smirk_path.quadTo(0, -114, 15, -122) # Turned up on right side!
    canvas.drawPath(smirk_path, skia.Paint(Color=skia.ColorSetARGB(255, 185, 55, 60), StrokeWidth=3, Style=skia.Paint.kStroke_Style, AntiAlias=True))

    # 4. Hand Resting Defiantly on Gem-Studded Sword Pommel
    sword_hilt = skia.Paint(Color=skia.ColorSetARGB(255, 245, 205, 70), AntiAlias=True)
    canvas.drawCircle(-85, 65, 16, sword_hilt) # Golden Pommel
    canvas.drawCircle(-85, 65, 7, skia.Paint(Color=skia.ColorSetARGB(255, 20, 160, 220), AntiAlias=True)) # Cyan Gem
    canvas.drawLine(-85, 75, -85, 120, skia.Paint(Color=skia.ColorSetARGB(255, 60, 40, 30), StrokeWidth=10, AntiAlias=True)) # Grip
    canvas.drawRect(skia.Rect(-115, 118, -55, 128), sword_hilt) # Crossguard

    # Prince's Hand over Pommel
    canvas.drawCircle(-85, 55, 15, skin_paint)
    for fx in range(-95, -70, 7):
        canvas.drawRoundRect(skia.Rect(fx, 45, fx + 6, 68), 3, 3, skin_paint)

    canvas.restore()
