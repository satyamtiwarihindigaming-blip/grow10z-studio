"""
GROW10Z — Cinematic Mythological Character & Environment Engine (v2)
High-fidelity Skia 2.5D vector rigs with multi-layer shading,
anatomical curves, royal jewelry, dynamic fabric simulation,
sacred attributes, and cinematic volumetric lighting.
"""

import math
import random
import numpy as np
import skia

def draw_ornate_aura(cv, cx, cy, radius, pulse=1.0, color_scheme="gold"):
    """Multi-ring divine celestial aura with sunburst rays"""
    if color_scheme == "gold":
        c_outer = [skia.ColorSetARGB(190, 255, 220, 110), skia.ColorSetARGB(80, 255, 160, 30), skia.ColorSetARGB(0, 255, 140, 0)]
        c_inner = [skia.ColorSetARGB(245, 255, 250, 210), skia.ColorSetARGB(160, 255, 210, 60), skia.ColorSetARGB(0, 255, 190, 20)]
        ray_c = skia.ColorSetARGB(60, 255, 235, 160)
    elif color_scheme == "crimson_dark": # For Demonic/Tadaka aura
        c_outer = [skia.ColorSetARGB(180, 220, 30, 20), skia.ColorSetARGB(80, 120, 10, 10), skia.ColorSetARGB(0, 40, 5, 5)]
        c_inner = [skia.ColorSetARGB(240, 255, 80, 40), skia.ColorSetARGB(150, 180, 20, 20), skia.ColorSetARGB(0, 100, 10, 10)]
        ray_c = skia.ColorSetARGB(60, 255, 80, 40)
    else: # Sage / Tapasya
        c_outer = [skia.ColorSetARGB(190, 255, 180, 70), skia.ColorSetARGB(80, 240, 120, 20), skia.ColorSetARGB(0, 200, 80, 0)]
        c_inner = [skia.ColorSetARGB(240, 255, 230, 160), skia.ColorSetARGB(150, 255, 160, 40), skia.ColorSetARGB(0, 220, 110, 10)]
        ray_c = skia.ColorSetARGB(60, 255, 200, 100)

    # Outer soft halo
    outer_paint = skia.Paint(
        Shader=skia.GradientShader.MakeRadial(
            skia.Point(cx, cy), radius * 1.4 * pulse,
            c_outer,
            [0.0, 0.6, 1.0]
        ),
        AntiAlias=True
    )
    cv.drawCircle(cx, cy, radius * 1.4 * pulse, outer_paint)
    
    # Sunburst rays
    ray_paint = skia.Paint(Color=ray_c, StrokeWidth=3, AntiAlias=True)
    for angle in range(0, 360, 15):
        rad = math.radians(angle)
        x1 = cx + math.cos(rad) * (radius * 0.75)
        y1 = cy + math.sin(rad) * (radius * 0.75)
        x2 = cx + math.cos(rad) * (radius * 1.25 * pulse)
        y2 = cy + math.sin(rad) * (radius * 1.25 * pulse)
        cv.drawLine(x1, y1, x2, y2, ray_paint)

    # Inner bright corona
    inner_paint = skia.Paint(
        Shader=skia.GradientShader.MakeRadial(
            skia.Point(cx, cy), radius * 0.9,
            c_inner,
            [0.0, 0.7, 1.0]
        ),
        AntiAlias=True
    )
    cv.drawCircle(cx, cy, radius * 0.9, inner_paint)


def draw_cinematic_shri_ram(cv, cx, cy, scale=1.0, breathing=0.0, bow_draw=0.0):
    """
    Cinema-Grade Ultra-Detailed Shri Ram Warrior Rig:
    - 3D contoured Neel-Shyam celestial complexion with ambient occlusion and golden rim lighting
    - Lotus eyes (कमल नयन) with upper lid fold, pupil depth, dual catchlights, and lashes
    - Urdhva-Pundra Chandan & Kumkum Tilak
    - 5-tier royal Suryavanshi golden Mukut with embossed sunburst, emerald cabochons, and iridescent Peacock Feather
    - Makara-Kundals with pearl drops
    - Sculpted golden armor (Kavach) with lion-crest embossing
    - Layered pearl Kantha, Hansli, and royal Navratna garland
    - Silk Pitambari & crimson Angavastra with dynamic gold-embroidered pleats
    - Celestial Kodanda bow with dragon finials and gleaming arrow with Brahmastra energy
    """
    cv.save()
    cv.translate(cx, cy)
    cv.scale(scale, scale)

    # 1. Divine Aura
    draw_ornate_aura(cv, 0, -110, 260, pulse=1.0 + 0.05 * math.sin(breathing * 2), color_scheme="gold")

    # 2. Celestial Kodanda Bow (Behind body)
    bow_p = skia.Path()
    bow_p.moveTo(110, -280)
    bow_p.cubicTo(210, -70, 200, 160, 95, 340)
    # Bow core gold
    cv.drawPath(bow_p, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=22, Color=skia.ColorSetARGB(255, 212, 160, 23), AntiAlias=True))
    cv.drawPath(bow_p, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=10, Color=skia.ColorSetARGB(255, 255, 238, 140), AntiAlias=True))
    # Dragon horn finials on bow tips
    cv.drawCircle(110, -280, 14, skia.Paint(Color=skia.ColorSetARGB(255, 245, 210, 60), AntiAlias=True))
    cv.drawCircle(95, 340, 14, skia.Paint(Color=skia.ColorSetARGB(255, 245, 210, 60), AntiAlias=True))
    # Bowstring
    string_pull_x = 110 - (bow_draw * 85)
    string_pull_y = 20
    string_p = skia.Path()
    string_p.moveTo(110, -280)
    string_p.lineTo(string_pull_x, string_pull_y)
    string_p.lineTo(95, 340)
    cv.drawPath(string_p, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=3.5, Color=skia.ColorSetARGB(230, 255, 255, 255), AntiAlias=True))

    # 3. Quiver with Feathered Arrows on back
    quiver_p = skia.Path()
    quiver_p.moveTo(-110, -180)
    quiver_p.lineTo(-55, -200)
    quiver_p.lineTo(-20, 120)
    quiver_p.lineTo(-75, 140)
    quiver_p.close()
    cv.drawPath(quiver_p, skia.Paint(Color=skia.ColorSetARGB(255, 120, 25, 35), AntiAlias=True))
    cv.drawPath(quiver_p, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=6, Color=skia.ColorSetARGB(255, 235, 195, 55), AntiAlias=True))
    # Golden arrow shafts & peacock fletchings peeking out
    for i, offset in enumerate([-25, 0, 25]):
        cv.drawLine(-85 + offset, -270, -65 + offset, -190, skia.Paint(StrokeWidth=6, Color=skia.ColorSetARGB(255, 245, 215, 70), AntiAlias=True))
        cv.drawOval(skia.Rect(-92 + offset, -290, -78 + offset, -250), skia.Paint(Color=skia.ColorSetARGB(255, 25, 140, 85), AntiAlias=True))

    # 4. Muscular Heroic Torso & Royal Golden Armor (Kavach)
    C_SKIN_BASE = skia.ColorSetARGB(255, 42, 86, 158)
    C_SKIN_SHADOW = skia.ColorSetARGB(255, 24, 52, 102)
    C_SKIN_HILITE = skia.ColorSetARGB(255, 95, 155, 240)
    C_GOLD_DARK = skia.ColorSetARGB(255, 175, 125, 15)
    C_GOLD_MID = skia.ColorSetARGB(255, 238, 185, 35)
    C_GOLD_BRIGHT = skia.ColorSetARGB(255, 255, 242, 160)

    # Neck
    neck_p = skia.Path()
    neck_p.moveTo(-32, -50)
    neck_p.lineTo(32, -50)
    neck_p.lineTo(38, 20)
    neck_p.lineTo(-38, 20)
    neck_p.close()
    cv.drawPath(neck_p, skia.Paint(Color=C_SKIN_BASE, AntiAlias=True))
    cv.drawRect(skia.Rect(-32, -50, 32, -30), skia.Paint(Color=C_SKIN_SHADOW, AntiAlias=True))

    # Broad Shoulders & Muscular Torso Base
    body_p = skia.Path()
    body_p.moveTo(-115, 30)
    body_p.cubicTo(-135, 65, -95, 160, -80, 270)
    body_p.lineTo(80, 270)
    body_p.cubicTo(95, 160, 135, 65, 115, 30)
    body_p.lineTo(0, 15)
    body_p.close()
    
    torso_shader = skia.GradientShader.MakeLinear(
        [skia.Point(-115, 30), skia.Point(115, 270)],
        [C_SKIN_HILITE, C_SKIN_BASE, C_SKIN_SHADOW],
        [0.0, 0.45, 1.0]
    )
    cv.drawPath(body_p, skia.Paint(Shader=torso_shader, AntiAlias=True))

    # Golden Imperial Kavach (Armor) over chest
    kavach_p = skia.Path()
    kavach_p.moveTo(-85, 35)
    kavach_p.cubicTo(-40, 45, 40, 45, 85, 35)
    kavach_p.lineTo(65, 180)
    kavach_p.cubicTo(30, 210, -30, 210, -65, 180)
    kavach_p.close()

    kavach_shader = skia.GradientShader.MakeLinear(
        [skia.Point(-85, 35), skia.Point(85, 180)],
        [C_GOLD_BRIGHT, C_GOLD_MID, C_GOLD_DARK],
        [0.0, 0.5, 1.0]
    )
    cv.drawPath(kavach_p, skia.Paint(Shader=kavach_shader, AntiAlias=True))
    cv.drawPath(kavach_p, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=5, Color=C_GOLD_DARK, AntiAlias=True))

    # Embossed Sun Emblem (सूर्यवंशी चिन्ह) on breastplate
    cv.drawCircle(0, 105, 24, skia.Paint(Color=skia.ColorSetARGB(255, 255, 220, 80), AntiAlias=True))
    cv.drawCircle(0, 105, 16, skia.Paint(Color=skia.ColorSetARGB(255, 200, 40, 30), AntiAlias=True))
    for deg in range(0, 360, 30):
        rad = math.radians(deg)
        cv.drawLine(math.cos(rad)*24, 105 + math.sin(rad)*24, math.cos(rad)*34, 105 + math.sin(rad)*34, skia.Paint(StrokeWidth=3, Color=C_GOLD_BRIGHT, AntiAlias=True))

    # Royal Pitambari Silk & Pleated Dhoti
    dhoti_p = skia.Path()
    dhoti_p.moveTo(-80, 250)
    dhoti_p.lineTo(80, 250)
    dhoti_p.lineTo(105, 450)
    dhoti_p.lineTo(-105, 450)
    dhoti_p.close()
    dhoti_shader = skia.GradientShader.MakeLinear(
        [skia.Point(0, 250), skia.Point(0, 450)],
        [skia.ColorSetARGB(255, 248, 185, 22), skia.ColorSetARGB(255, 215, 135, 15)],
        [0.0, 1.0]
    )
    cv.drawPath(dhoti_p, skia.Paint(Shader=dhoti_shader, AntiAlias=True))
    cv.drawLine(-105, 440, 105, 440, skia.Paint(StrokeWidth=12, Color=C_GOLD_BRIGHT, AntiAlias=True))

    # Royal Saffron Angavastra (flowing sash draped over shoulder)
    sash_p = skia.Path()
    sash_p.moveTo(-115, 30)
    sash_p.cubicTo(-30, 90, 40, 220, 95, 360)
    sash_p.lineTo(65, 385)
    sash_p.cubicTo(10, 240, -60, 110, -135, 45)
    sash_p.close()
    cv.drawPath(sash_p, skia.Paint(Color=skia.ColorSetARGB(255, 195, 35, 40), AntiAlias=True))
    cv.drawPath(sash_p, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=4, Color=C_GOLD_MID, AntiAlias=True))

    # Heavy Kantha (Choker), Pearl Garlands
    for r in [55, 75, 95]:
        cv.drawOval(skia.Rect(-r, 10, r, 20 + r*0.8), skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=6, Color=skia.ColorSetARGB(245, 255, 252, 235), AntiAlias=True))
    cv.drawCircle(0, 90, 10, skia.Paint(Color=skia.ColorSetARGB(255, 225, 25, 45), AntiAlias=True))
    cv.drawCircle(0, 90, 10, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=3, Color=C_GOLD_BRIGHT, AntiAlias=True))

    # 5. Sculpted Heroic Head & Face
    hair_back_p = skia.Path()
    hair_back_p.addCircle(0, -115, 72)
    cv.drawPath(hair_back_p, skia.Paint(Color=skia.ColorSetARGB(255, 15, 18, 28), AntiAlias=True))

    face_p = skia.Path()
    face_p.moveTo(-48, -145)
    face_p.cubicTo(-62, -90, -48, -35, 0, -22)
    face_p.cubicTo(48, -35, 62, -90, 48, -145)
    face_p.close()

    face_shader = skia.GradientShader.MakeRadial(
        skia.Point(-12, -95), 85,
        [C_SKIN_HILITE, C_SKIN_BASE, C_SKIN_SHADOW],
        [0.0, 0.65, 1.0]
    )
    cv.drawPath(face_p, skia.Paint(Shader=face_shader, AntiAlias=True))

    # Golden Rim Light on cheek
    rim_p = skia.Path()
    rim_p.moveTo(48, -145)
    rim_p.cubicTo(62, -90, 48, -35, 0, -22)
    cv.drawPath(rim_p, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=4, Color=skia.ColorSetARGB(200, 255, 235, 150), AntiAlias=True))

    # Makara Kundals (Golden Royal Earrings)
    for s in [-1, 1]:
        kx = s * 64
        ky = -82
        cv.drawCircle(kx, ky, 14, skia.Paint(Color=C_GOLD_MID, AntiAlias=True))
        cv.drawCircle(kx, ky, 14, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=3, Color=C_GOLD_BRIGHT, AntiAlias=True))
        cv.drawCircle(kx, ky + 22, 7, skia.Paint(Color=skia.ColorWHITE, AntiAlias=True))

    # Lotus Eyes (विशाल कमल नयन)
    for s in [-1, 1]:
        ex = s * 22
        ey = -90
        eye_p = skia.Path()
        eye_p.moveTo(ex - 15, ey)
        eye_p.cubicTo(ex - 7, ey - 10, ex + 7, ey - 10, ex + 15, ey)
        eye_p.cubicTo(ex + 7, ey + 9, ex - 7, ey + 9, ex - 15, ey)
        eye_p.close()
        cv.drawPath(eye_p, skia.Paint(Color=skia.ColorSetARGB(255, 252, 252, 255), AntiAlias=True))
        cv.drawPath(eye_p, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=3.5, Color=skia.ColorSetARGB(255, 18, 22, 32), AntiAlias=True))

        cv.drawCircle(ex, ey, 6.5, skia.Paint(Color=skia.ColorSetARGB(255, 22, 35, 58), AntiAlias=True))
        cv.drawCircle(ex, ey, 4.0, skia.Paint(Color=skia.ColorSetARGB(255, 12, 16, 25), AntiAlias=True))
        cv.drawCircle(ex - 2.5, ey - 2.5, 2.2, skia.Paint(Color=skia.ColorWHITE, AntiAlias=True))
        cv.drawCircle(ex + 2.0, ey + 2.0, 1.2, skia.Paint(Color=skia.ColorWHITE, AntiAlias=True))

        brow_p = skia.Path()
        brow_p.moveTo(ex - 18, ey - 14)
        brow_p.cubicTo(ex - 4, ey - 20, ex + 6, ey - 19, ex + 18, ey - 13)
        cv.drawPath(brow_p, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=3.5, Color=skia.ColorSetARGB(255, 15, 20, 30), AntiAlias=True))

    # Sacred Chandan & Kumkum Tilak (ऊर्ध्वपुण्ड्र तिलक)
    tilak_p = skia.Path()
    tilak_p.moveTo(-10, -135)
    tilak_p.cubicTo(-10, -100, -5, -92, 0, -90)
    tilak_p.cubicTo(5, -92, 10, -100, 10, -135)
    cv.drawPath(tilak_p, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=4.0, Color=skia.ColorSetARGB(255, 255, 250, 230), AntiAlias=True))
    cv.drawLine(0, -133, 0, -92, skia.Paint(StrokeWidth=3.5, Color=skia.ColorSetARGB(255, 225, 25, 35), AntiAlias=True))
    cv.drawCircle(0, -92, 2.5, skia.Paint(Color=skia.ColorSetARGB(255, 225, 25, 35), AntiAlias=True))

    # Nose & Compassionate Divine Smile
    nose_p = skia.Path()
    nose_p.moveTo(0, -90)
    nose_p.lineTo(2, -62)
    nose_p.lineTo(-5, -57)
    nose_p.lineTo(5, -57)
    cv.drawPath(nose_p, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=2.2, Color=C_SKIN_SHADOW, AntiAlias=True))

    lips_p = skia.Path()
    lips_p.moveTo(-14, -43)
    lips_p.cubicTo(-5, -46, 5, -46, 14, -43)
    lips_p.cubicTo(6, -35, -6, -35, -14, -43)
    cv.drawPath(lips_p, skia.Paint(Color=skia.ColorSetARGB(255, 195, 65, 80), AntiAlias=True))
    cv.drawLine(-14, -43, 14, -43, skia.Paint(StrokeWidth=2.0, Color=skia.ColorSetARGB(255, 145, 35, 50), AntiAlias=True))

    # 6. Grand 5-Tier Suryavanshi Mukut (Crown)
    mukut_p = skia.Path()
    mukut_p.moveTo(-52, -140)
    mukut_p.cubicTo(-58, -175, -45, -230, 0, -265)
    mukut_p.cubicTo(45, -230, 58, -175, 52, -140)
    mukut_p.close()

    mukut_shader = skia.GradientShader.MakeLinear(
        [skia.Point(-52, -140), skia.Point(52, -265)],
        [C_GOLD_DARK, C_GOLD_BRIGHT, C_GOLD_MID, C_GOLD_DARK],
        [0.0, 0.4, 0.7, 1.0]
    )
    cv.drawPath(mukut_p, skia.Paint(Shader=mukut_shader, AntiAlias=True))
    cv.drawPath(mukut_p, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=5, Color=C_GOLD_DARK, AntiAlias=True))

    for my in [-160, -195, -230]:
        cv.drawLine(-35 * (1 - (abs(my + 140)/140)), my, 35 * (1 - (abs(my + 140)/140)), my, skia.Paint(StrokeWidth=3, Color=C_GOLD_DARK, AntiAlias=True))
    cv.drawCircle(0, -175, 9, skia.Paint(Color=skia.ColorSetARGB(255, 230, 20, 45), AntiAlias=True))
    cv.drawCircle(0, -175, 9, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=2.5, Color=C_GOLD_BRIGHT, AntiAlias=True))
    for gx in [-24, 24]:
        cv.drawCircle(gx, -165, 6, skia.Paint(Color=skia.ColorSetARGB(255, 20, 165, 80), AntiAlias=True))

    cv.drawCircle(0, -270, 8, skia.Paint(Color=C_GOLD_BRIGHT, AntiAlias=True))

    # Peacock Feather (मयूरपंख / Mayur Pankh)
    pf_p = skia.Path()
    pf_p.moveTo(0, -275)
    pf_p.cubicTo(-28, -320, -15, -365, 0, -375)
    pf_p.cubicTo(15, -365, 28, -320, 0, -275)
    cv.drawPath(pf_p, skia.Paint(Color=skia.ColorSetARGB(255, 18, 145, 90), AntiAlias=True))
    cv.drawCircle(0, -330, 14, skia.Paint(Color=skia.ColorSetARGB(255, 225, 180, 25), AntiAlias=True))
    cv.drawCircle(0, -330, 9, skia.Paint(Color=skia.ColorSetARGB(255, 25, 95, 215), AntiAlias=True))
    cv.drawCircle(0, -330, 4, skia.Paint(Color=skia.ColorSetARGB(255, 12, 18, 45), AntiAlias=True))

    # 7. Arms, Hands & Divine Arrow (Drawing the Bow)
    arm_r = skia.Path()
    arm_r.moveTo(115, 60)
    arm_r.lineTo(165, 45)
    arm_r.lineTo(string_pull_x + 30, string_pull_y)
    arm_r.lineTo(string_pull_x, string_pull_y)
    cv.drawPath(arm_r, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=24, StrokeCap=skia.Paint.kRound_Cap, Color=C_SKIN_BASE, AntiAlias=True))
    cv.drawCircle(145, 52, 15, skia.Paint(Color=C_GOLD_MID, AntiAlias=True))
    cv.drawCircle(string_pull_x, string_pull_y, 14, skia.Paint(Color=C_SKIN_BASE, AntiAlias=True))

    arrow_p = skia.Path()
    arrow_p.moveTo(string_pull_x, string_pull_y)
    arrow_p.lineTo(-240, -40)
    cv.drawPath(arrow_p, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=6, Color=C_GOLD_BRIGHT, AntiAlias=True))
    tip_p = skia.Path()
    tip_p.moveTo(-240, -40)
    tip_p.lineTo(-215, -55)
    tip_p.lineTo(-215, -25)
    tip_p.close()
    cv.drawPath(tip_p, skia.Paint(Color=skia.ColorSetARGB(255, 255, 245, 190), AntiAlias=True))
    flare_paint = skia.Paint(
        Shader=skia.GradientShader.MakeRadial(
            skia.Point(-240, -40), 65,
            [skia.ColorSetARGB(255, 255, 255, 255), skia.ColorSetARGB(180, 255, 200, 40), skia.ColorSetARGB(0, 255, 60, 0)],
            [0.0, 0.4, 1.0]
        ),
        AntiAlias=True
    )
    cv.drawCircle(-240, -40, 65, flare_paint)

    cv.restore()


def draw_cinematic_tadaka(cv, cx, cy, scale=1.0, roar_intensity=0.0, phase=0.0):
    """
    Cinema-Grade Demonic Sorceress Tadaka:
    - Towering ash-black monstrous form with volcanic muscle contours
    - Wild flaming tangled crimson/black mane with whipping wind strands
    - Burning yellow/red demonic eyes with sulfurous emission
    - Sharp obsidian fangs and snarling jagged maw
    - Bone and skull necklace with jagged iron cuffs
    - Massive jagged boulder / spiked tree club held high
    - Swirling vortex of black smoke, storm sparks, and red embers
    """
    cv.save()
    cv.translate(cx, cy)
    cv.scale(scale, scale)

    # 1. Swirling Black Smoke & Ember Vortex
    draw_ornate_aura(cv, 0, -100, 240, pulse=1.0 + 0.1 * math.sin(phase * 4), color_scheme="crimson_dark")

    # 2. Spiked Demon Club / Tree Trunk
    club_p = skia.Path()
    club_p.moveTo(110, -320)
    club_p.lineTo(160, -310)
    club_p.lineTo(135, 180)
    club_p.lineTo(85, 180)
    club_p.close()
    cv.drawPath(club_p, skia.Paint(Color=skia.ColorSetARGB(255, 45, 32, 28), AntiAlias=True))
    cv.drawPath(club_p, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=6, Color=skia.ColorSetARGB(255, 25, 18, 15), AntiAlias=True))
    # Jagged Spikes on Club
    for sp_y in [-280, -220, -160, -100]:
        cv.drawLine(145, sp_y, 185, sp_y - 15, skia.Paint(StrokeWidth=8, StrokeCap=skia.Paint.kRound_Cap, Color=skia.ColorSetARGB(255, 180, 40, 30), AntiAlias=True))

    # 3. Monstrous Muscular Demonic Body
    C_DEMON_BASE = skia.ColorSetARGB(255, 32, 35, 42)
    C_DEMON_SHADOW = skia.ColorSetARGB(255, 15, 16, 20)
    C_DEMON_MAGMA = skia.ColorSetARGB(255, 215, 45, 25)

    torso_p = skia.Path()
    torso_p.moveTo(-135, 40)
    torso_p.cubicTo(-160, 110, -120, 240, -95, 380)
    torso_p.lineTo(95, 380)
    torso_p.cubicTo(120, 240, 160, 110, 135, 40)
    torso_p.lineTo(0, 15)
    torso_p.close()

    t_shader = skia.GradientShader.MakeLinear(
        [skia.Point(-135, 40), skia.Point(135, 380)],
        [C_DEMON_MAGMA, C_DEMON_BASE, C_DEMON_SHADOW],
        [0.0, 0.35, 1.0]
    )
    cv.drawPath(torso_p, skia.Paint(Shader=t_shader, AntiAlias=True))

    # Magma Veins glowing across chest
    vein_p = skia.Path()
    vein_p.moveTo(-80, 90)
    vein_p.lineTo(-40, 130)
    vein_p.lineTo(10, 105)
    vein_p.lineTo(60, 150)
    cv.drawPath(vein_p, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=4, Color=C_DEMON_MAGMA, AntiAlias=True))

    # Bone & Skull Necklace
    for bx in range(-90, 100, 25):
        cv.drawOval(skia.Rect(bx - 8, 45 + abs(bx)*0.4, bx + 8, 65 + abs(bx)*0.4), skia.Paint(Color=skia.ColorSetARGB(255, 225, 220, 205), AntiAlias=True))
    # Center Skull
    cv.drawCircle(0, 85, 16, skia.Paint(Color=skia.ColorSetARGB(255, 235, 230, 215), AntiAlias=True))
    cv.drawCircle(-6, 82, 3.5, skia.Paint(Color=skia.ColorSetARGB(255, 15, 15, 20), AntiAlias=True))
    cv.drawCircle(6, 82, 3.5, skia.Paint(Color=skia.ColorSetARGB(255, 15, 15, 20), AntiAlias=True))

    # 4. Wild Flaming Crimson Mane (Hair)
    hair_p = skia.Path()
    for angle in range(-120, 125, 15):
        rad = math.radians(angle - 90)
        h_len = 160 + 35 * math.sin(phase * 6 + angle)
        hx = math.cos(rad) * h_len
        hy = -90 + math.sin(rad) * h_len
        hair_p.moveTo(0, -90)
        hair_p.quadTo(hx * 0.5, hy * 0.5 + 30, hx, hy)
    cv.drawPath(hair_p, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=14, StrokeCap=skia.Paint.kRound_Cap, Color=skia.ColorSetARGB(255, 185, 25, 15), AntiAlias=True))
    cv.drawPath(hair_p, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=6, StrokeCap=skia.Paint.kRound_Cap, Color=skia.ColorSetARGB(255, 245, 120, 30), AntiAlias=True))

    # 5. Demonic Head & Snarl
    cv.drawCircle(0, -90, 68, skia.Paint(Color=C_DEMON_BASE, AntiAlias=True))

    # Burning Sulfurous Demonic Eyes
    for s in [-1, 1]:
        dex = s * 26
        dey = -105
        # Angled demonic eye slant
        cv.drawOval(skia.Rect(dex - 14, dey - 12, dex + 14, dey + 6), skia.Paint(Color=skia.ColorSetARGB(255, 255, 50, 20), AntiAlias=True))
        cv.drawCircle(dex, dey - 3, 5, skia.Paint(Color=skia.ColorSetARGB(255, 255, 240, 80), AntiAlias=True))
        # Eye fire emission
        cv.drawCircle(dex, dey - 3, 12, skia.Paint(
            Shader=skia.GradientShader.MakeRadial(
                skia.Point(dex, dey - 3), 12,
                [skia.ColorSetARGB(180, 255, 200, 50), skia.ColorSetARGB(0, 255, 50, 0)],
                [0.0, 1.0]
            ),
            AntiAlias=True
        ))

    # Snarling Jaw with Sharp Obsidian Fangs
    jaw_p = skia.Path()
    jaw_p.moveTo(-35, -55)
    jaw_p.cubicTo(-20, -15 - roar_intensity * 25, 20, -15 - roar_intensity * 25, 35, -55)
    jaw_p.close()
    cv.drawPath(jaw_p, skia.Paint(Color=skia.ColorSetARGB(255, 12, 10, 14), AntiAlias=True))

    # Sharp Fangs
    for fx in [-22, -8, 8, 22]:
        fang = skia.Path()
        fang.moveTo(fx - 4, -55)
        fang.lineTo(fx, -35 - roar_intensity * 10)
        fang.lineTo(fx + 4, -55)
        fang.close()
        cv.drawPath(fang, skia.Paint(Color=skia.ColorSetARGB(255, 245, 240, 215), AntiAlias=True))

    # 6. Monstrous Claw Arms
    arm_l = skia.Path()
    arm_l.moveTo(-135, 50)
    arm_l.lineTo(-210, 120)
    arm_l.lineTo(-260, 90)
    cv.drawPath(arm_l, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=32, StrokeCap=skia.Paint.kRound_Cap, Color=C_DEMON_BASE, AntiAlias=True))
    # Claws
    for ci in [-15, 0, 15]:
        cv.drawLine(-260, 90 + ci, -295, 90 + ci*1.4, skia.Paint(StrokeWidth=6, StrokeCap=skia.Paint.kRound_Cap, Color=skia.ColorSetARGB(255, 215, 210, 195), AntiAlias=True))

    cv.restore()


def draw_cinematic_vishwamitra(cv, cx, cy, scale=1.0, breathing=0.0):
    """
    Cinema-Grade Vedic Sage Maharishi Vishwamitra:
    - Tapasya Tejas (radiant amber aura)
    - Jata-Mukut (high matted hair crown bound with Rudraksha)
    - Flowing silver-white beard with strand texture
    - Saffron bark valkala and ascetic deerskin drape
    - Abhaya Mudra (blessing hand of righteous command)
    """
    cv.save()
    cv.translate(cx, cy)
    cv.scale(scale, scale)

    # 1. Tapasya Aura
    draw_ornate_aura(cv, 0, -100, 230, pulse=1.0 + 0.04 * math.sin(breathing * 2), color_scheme="sage")

    # 2. Ascetic Saffron Robe & Body
    C_SAGE_SKIN = skia.ColorSetARGB(255, 215, 165, 120)
    C_SAFFRON = skia.ColorSetARGB(255, 225, 95, 25)
    C_SAFFRON_DARK = skia.ColorSetARGB(255, 160, 55, 15)

    robe_p = skia.Path()
    robe_p.moveTo(-90, 40)
    robe_p.cubicTo(-115, 130, -85, 250, -75, 380)
    robe_p.lineTo(75, 380)
    robe_p.cubicTo(85, 250, 115, 130, 90, 40)
    robe_p.close()
    
    r_shader = skia.GradientShader.MakeLinear(
        [skia.Point(-90, 40), skia.Point(90, 380)],
        [C_SAFFRON, C_SAFFRON_DARK],
        [0.0, 1.0]
    )
    cv.drawPath(robe_p, skia.Paint(Shader=r_shader, AntiAlias=True))

    # Sacred Rudraksha Malas & Yajnopavita (Sacred Thread)
    cv.drawLine(-60, 35, 65, 320, skia.Paint(StrokeWidth=4, Color=skia.ColorWHITE, AntiAlias=True))
    for rx in [-45, -20, 5, 30, 55]:
        cv.drawCircle(rx, 65 + abs(rx)*0.4, 7, skia.Paint(Color=skia.ColorSetARGB(255, 115, 55, 30), AntiAlias=True))

    # 3. Head, Jata & Fiery Ascetic Eyes
    cv.drawCircle(0, -90, 54, skia.Paint(Color=C_SAGE_SKIN, AntiAlias=True))

    # Tripundra Tilak on forehead
    for ty in [-118, -112, -106]:
        cv.drawLine(-18, ty, 18, ty, skia.Paint(StrokeWidth=3, Color=skia.ColorSetARGB(230, 240, 240, 245), AntiAlias=True))
    cv.drawCircle(0, -112, 3.5, skia.Paint(Color=skia.ColorSetARGB(255, 220, 30, 30), AntiAlias=True))

    # Eyes
    for s in [-1, 1]:
        ex = s * 20
        ey = -90
        cv.drawOval(skia.Rect(ex - 12, ey - 6, ex + 12, ey + 6), skia.Paint(Color=skia.ColorWHITE, AntiAlias=True))
        cv.drawCircle(ex, ey, 5, skia.Paint(Color=skia.ColorSetARGB(255, 45, 25, 15), AntiAlias=True))
        cv.drawCircle(ex - 2, ey - 2, 1.8, skia.Paint(Color=skia.ColorWHITE, AntiAlias=True))

    # Flowing Silver-White Beard & Mustache
    beard_p = skia.Path()
    beard_p.moveTo(-45, -75)
    beard_p.cubicTo(-60, 10, -20, 110, 0, 140)
    beard_p.cubicTo(20, 110, 60, 10, 45, -75)
    beard_p.close()
    b_shader = skia.GradientShader.MakeLinear(
        [skia.Point(0, -75), skia.Point(0, 140)],
        [skia.ColorSetARGB(255, 245, 245, 250), skia.ColorSetARGB(255, 195, 200, 210)],
        [0.0, 1.0]
    )
    cv.drawPath(beard_p, skia.Paint(Shader=b_shader, AntiAlias=True))
    cv.drawPath(beard_p, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=3, Color=skia.ColorSetARGB(180, 170, 175, 185), AntiAlias=True))

    # Jata-Mukut (Matted Locks)
    jata_p = skia.Path()
    jata_p.moveTo(-40, -125)
    jata_p.cubicTo(-50, -210, -20, -240, 0, -250)
    jata_p.cubicTo(20, -240, 50, -210, 40, -125)
    jata_p.close()
    cv.drawPath(jata_p, skia.Paint(Color=skia.ColorSetARGB(255, 65, 45, 35), AntiAlias=True))
    # Rudraksha circlet around Jata
    for jx in range(-30, 35, 15):
        cv.drawCircle(jx, -170, 6, skia.Paint(Color=skia.ColorSetARGB(255, 130, 60, 25), AntiAlias=True))

    # 4. Blessing Hand (अभय मुद्रा)
    hand_p = skia.Path()
    hand_p.moveTo(85, 90)
    hand_p.lineTo(135, 30)
    hand_p.lineTo(155, 35)
    hand_p.lineTo(150, 75)
    hand_p.lineTo(105, 120)
    hand_p.close()
    cv.drawPath(hand_p, skia.Paint(Color=C_SAGE_SKIN, AntiAlias=True))
    cv.drawPath(hand_p, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=3, Color=skia.ColorSetARGB(255, 170, 120, 80), AntiAlias=True))

    cv.restore()


def draw_ancient_manuscript_page(cv, W, H, episode_title, shloka_text="॥ ॐ श्री गणेशाय नमः ॥", progress=1.0):
    """
    3D Ancient Palm-Leaf / Sanskrit Storybook Manuscript
    - Weathered deckle-edge parchment texture
    - Gold filigree ornamental borders with sacred lotus corners
    - Sanskrit shloka in burnished gold
    - Illuminated Devanagari chapter header
    """
    cv.save()
    
    # Slight perspective scale & angle based on progress
    scale = 0.92 + 0.08 * math.sin(progress * math.pi * 0.5)
    cv.translate(W * 0.5, H * 0.5)
    cv.scale(scale, scale)
    cv.translate(-W * 0.5, -H * 0.5)

    margin_x = 70
    margin_y = 180
    book_w = W - 2 * margin_x
    book_h = H - 2 * margin_y

    # Parchment Drop Shadow
    shadow_rect = skia.Rect(margin_x + 15, margin_y + 25, margin_x + book_w + 15, margin_y + book_h + 25)
    cv.drawRoundRect(shadow_rect, 25, 25, skia.Paint(Color=skia.ColorSetARGB(180, 5, 3, 10), AntiAlias=True))

    # Weathered Ancient Parchment Sheet
    sheet_rect = skia.Rect(margin_x, margin_y, margin_x + book_w, margin_y + book_h)
    parchment_shader = skia.GradientShader.MakeLinear(
        [skia.Point(margin_x, margin_y), skia.Point(margin_x + book_w, margin_y + book_h)],
        [skia.ColorSetARGB(255, 246, 230, 185), skia.ColorSetARGB(255, 228, 202, 145), skia.ColorSetARGB(255, 210, 178, 120)],
        [0.0, 0.55, 1.0]
    )
    cv.drawRoundRect(sheet_rect, 25, 25, skia.Paint(Shader=parchment_shader, AntiAlias=True))

    # Ancient Page Burn / Aging Vignette on edges
    burn_paint = skia.Paint(
        Style=skia.Paint.kStroke_Style,
        StrokeWidth=20,
        Shader=skia.GradientShader.MakeRadial(
            skia.Point(W * 0.5, H * 0.5), book_h * 0.55,
            [skia.ColorSetARGB(0, 120, 70, 30), skia.ColorSetARGB(140, 75, 35, 15), skia.ColorSetARGB(220, 45, 18, 5)],
            [0.6, 0.88, 1.0]
        ),
        AntiAlias=True
    )
    cv.drawRoundRect(sheet_rect, 25, 25, burn_paint)

    # Intricate Golden Embossed Border
    inner_rect = skia.Rect(margin_x + 35, margin_y + 35, margin_x + book_w - 35, margin_y + book_h - 35)
    border_gold = skia.Paint(
        Style=skia.Paint.kStroke_Style,
        StrokeWidth=6,
        Color=skia.ColorSetARGB(255, 195, 140, 25),
        AntiAlias=True
    )
    cv.drawRoundRect(inner_rect, 15, 15, border_gold)
    
    thin_gold = skia.Paint(
        Style=skia.Paint.kStroke_Style,
        StrokeWidth=2,
        Color=skia.ColorSetARGB(255, 145, 95, 15),
        AntiAlias=True
    )
    cv.drawRoundRect(skia.Rect(margin_x + 48, margin_y + 48, margin_x + book_w - 48, margin_y + book_h - 48), 10, 10, thin_gold)

    # Corner Lotus Motifs
    for cx_c in [margin_x + 40, margin_x + book_w - 40]:
        for cy_c in [margin_y + 40, margin_y + book_h - 40]:
            cv.drawCircle(cx_c, cy_c, 16, skia.Paint(Color=skia.ColorSetARGB(255, 215, 160, 35), AntiAlias=True))
            cv.drawCircle(cx_c, cy_c, 8, skia.Paint(Color=skia.ColorSetARGB(255, 180, 35, 30), AntiAlias=True))

    # Sacred Shloka & Title Typography
    font_bold = skia.Font(skia.Typeface.MakeFromName("Arial", skia.FontStyle.Bold()), 42)
    font_title = skia.Font(skia.Typeface.MakeFromName("Arial", skia.FontStyle.Bold()), 56)
    font_sub = skia.Font(skia.Typeface.MakeFromName("Arial", skia.FontStyle.Normal()), 36)

    # Shloka Header
    shloka_paint = skia.Paint(Color=skia.ColorSetARGB(255, 140, 30, 25), AntiAlias=True)
    bounds_shloka = font_bold.measureText(shloka_text)
    cv.drawString(shloka_text, (W - bounds_shloka) * 0.5, margin_y + 140, font_bold, shloka_paint)

    # Divider Line with Golden Kalash
    div_y = margin_y + 185
    cv.drawLine(margin_x + 80, div_y, margin_x + book_w - 80, div_y, skia.Paint(StrokeWidth=3, Color=skia.ColorSetARGB(255, 195, 140, 25), AntiAlias=True))
    cv.drawCircle(W * 0.5, div_y, 10, skia.Paint(Color=skia.ColorSetARGB(255, 195, 140, 25), AntiAlias=True))

    # Chapter Title Plaque
    title_paint = skia.Paint(Color=skia.ColorSetARGB(255, 45, 18, 12), AntiAlias=True)
    # Split title if long
    words = episode_title.split(" ")
    mid = len(words) // 2
    line1 = " ".join(words[:mid])
    line2 = " ".join(words[mid:])

    b1 = font_title.measureText(line1)
    cv.drawString(line1, (W - b1) * 0.5, margin_y + 360, font_title, title_paint)
    if line2:
        b2 = font_title.measureText(line2)
        cv.drawString(line2, (W - b2) * 0.5, margin_y + 450, font_title, title_paint)

    # Sacred Footnote
    footer = "॥ मर्यादा पुरुषोत्तम श्रीराम गाथा ॥"
    bf = font_sub.measureText(footer)
    cv.drawString(footer, (W - bf) * 0.5, margin_y + book_h - 80, font_sub, skia.Paint(Color=skia.ColorSetARGB(255, 120, 60, 25), AntiAlias=True))

    cv.restore()


def draw_cinematic_environment(cv, env_type, t_sec, W, H):
    """
    Volumetric 3-Layer Atmospheric Environments:
    - dandaka_forest: Twilight mystic jungle with ancient banyans, volumetric sunbeams, fireflies.
    - ayodhya_palace: Royal golden halls, towering temple spires, flickering brass diyas, starlight.
    - mithila_durbar: Regal assembly hall, carved marble arches, sacred floral garlands.
    """
    if env_type == "dandaka_forest":
        # Celestial Twilight Sky (Deep Indigo to Fiery Amber)
        sky_shader = skia.GradientShader.MakeLinear(
            [skia.Point(0, 0), skia.Point(0, H)],
            [skia.ColorSetARGB(255, 20, 14, 38), skia.ColorSetARGB(255, 95, 35, 40), skia.ColorSetARGB(255, 210, 90, 35), skia.ColorSetARGB(255, 25, 20, 18)],
            [0.0, 0.45, 0.75, 1.0]
        )
        cv.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Shader=sky_shader))

        # Distant Mountain Silhouettes
        mount_p = skia.Path()
        mount_p.moveTo(0, H * 0.65)
        for mx in range(0, W + 100, 180):
            my = H * 0.65 - 120 * math.sin(mx * 0.005 + 1.2)
            mount_p.lineTo(mx, my)
        mount_p.lineTo(W, H)
        mount_p.lineTo(0, H)
        mount_p.close()
        cv.drawPath(mount_p, skia.Paint(Color=skia.ColorSetARGB(180, 35, 20, 32), AntiAlias=True))

        # Volumetric Sunbeams / God-Rays
        ray_p = skia.Paint(
            Shader=skia.GradientShader.MakeLinear(
                [skia.Point(W * 0.8, 0), skia.Point(0, H)],
                [skia.ColorSetARGB(85, 255, 230, 140), skia.ColorSetARGB(0, 255, 180, 50)],
                [0.0, 0.85]
            ),
            AntiAlias=True
        )
        for ro in [100, 280, 480, 720]:
            r_path = skia.Path()
            r_path.moveTo(ro - 60, 0)
            r_path.lineTo(ro + 60, 0)
            r_path.lineTo(ro - 240, H)
            r_path.lineTo(ro - 380, H)
            r_path.close()
            cv.drawPath(r_path, ray_p)

        # Looming Ancient Banyan Tree Silhouettes & Vines
        tree_paint = skia.Paint(Color=skia.ColorSetARGB(235, 16, 12, 18), AntiAlias=True)
        # Left ancient trunk
        cv.drawRect(skia.Rect(-60, 0, 180, H), tree_paint)
        # Right ancient trunk
        cv.drawRect(skia.Rect(W - 140, 0, W + 80, H), tree_paint)
        # Hanging aerial roots / vines
        for vx in [80, 130, W - 100, W - 60]:
            cv.drawLine(vx, 0, vx + 15 * math.sin(vx + t_sec), H * 0.85, skia.Paint(StrokeWidth=6, Color=skia.ColorSetARGB(220, 25, 18, 22), AntiAlias=True))

    elif env_type == "mithila_darbar":
        # Grand Royal Mithila Assembly Hall
        bg_shader = skia.GradientShader.MakeLinear(
            [skia.Point(0, 0), skia.Point(0, H)],
            [skia.ColorSetARGB(255, 20, 8, 16), skia.ColorSetARGB(255, 55, 16, 26), skia.ColorSetARGB(255, 110, 42, 22)],
            [0.0, 0.6, 1.0]
        )
        cv.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Shader=bg_shader))

        # Polished Imperial Marble Floor with Gold Inlays
        floor_y = H * 0.72
        floor_shader = skia.GradientShader.MakeLinear(
            [skia.Point(0, floor_y), skia.Point(0, H)],
            [skia.ColorSetARGB(255, 42, 18, 26), skia.ColorSetARGB(255, 15, 6, 12)],
            [0.0, 1.0]
        )
        cv.drawRect(skia.Rect(0, floor_y, W, H), skia.Paint(Shader=floor_shader))
        cv.drawLine(0, floor_y, W, floor_y, skia.Paint(StrokeWidth=4.5, Color=skia.ColorSetARGB(255, 245, 195, 60), AntiAlias=True))

        # Grand Fluted Mithila Palace Pillars
        pillar_paint = skia.Paint(
            Shader=skia.GradientShader.MakeLinear(
                [skia.Point(0, 0), skia.Point(140, 0)],
                [skia.ColorSetARGB(255, 60, 22, 32), skia.ColorSetARGB(255, 95, 38, 48), skia.ColorSetARGB(255, 45, 15, 22)],
                [0.0, 0.5, 1.0]
            ),
            AntiAlias=True
        )
        for px in [-40, 160, W - 300, W - 100]:
            cv.drawRect(skia.Rect(px, 0, px + 140, floor_y), pillar_paint)
            cv.drawRect(skia.Rect(px - 15, floor_y - 30, px + 155, floor_y), skia.Paint(Color=skia.ColorSetARGB(255, 235, 185, 50), AntiAlias=True))
            cv.drawRect(skia.Rect(px - 15, 0, px + 155, 40), skia.Paint(Color=skia.ColorSetARGB(255, 235, 185, 50), AntiAlias=True))

        # Burning Brass Mashals (Torches)
        for tx in [230, W - 230]:
            cv.drawRect(skia.Rect(tx - 12, floor_y - 480, tx + 12, floor_y - 420), skia.Paint(Color=skia.ColorSetARGB(255, 205, 155, 40), AntiAlias=True))
            cv.drawCircle(tx, floor_y - 480, 28, skia.Paint(Color=skia.ColorSetARGB(255, 185, 130, 35), AntiAlias=True))
            cv.drawCircle(tx, floor_y - 500, 75, skia.Paint(
                Shader=skia.GradientShader.MakeRadial(
                    skia.Point(tx, floor_y - 500), 75,
                    [skia.ColorSetARGB(170, 255, 200, 70), skia.ColorTRANSPARENT],
                    [0.0, 1.0]
                ),
                AntiAlias=True
            ))
            flame_p = skia.Path()
            flame_p.moveTo(tx - 18, floor_y - 480)
            flame_p.cubicTo(tx - 24, floor_y - 520, tx, floor_y - 555, tx, floor_y - 565)
            flame_p.cubicTo(tx + 6, floor_y - 535, tx + 20, floor_y - 515, tx + 18, floor_y - 480)
            flame_p.close()
            cv.drawPath(flame_p, skia.Paint(Color=skia.ColorSetARGB(255, 255, 160, 30), AntiAlias=True))

    else: # Ayodhya Palace Default
        sky_shader = skia.GradientShader.MakeLinear(
            [skia.Point(0, 0), skia.Point(0, H)],
            [skia.ColorSetARGB(255, 18, 12, 36), skia.ColorSetARGB(255, 65, 32, 55), skia.ColorSetARGB(255, 160, 85, 35)],
            [0.0, 0.55, 1.0]
        )
        cv.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Shader=sky_shader))

        # Distant Temple Spires (Shikharas)
        spire_paint = skia.Paint(Color=skia.ColorSetARGB(190, 45, 25, 45), AntiAlias=True)
        for sx in [180, 540, 900]:
            sp = skia.Path()
            sp.moveTo(sx - 140, H - 450)
            sp.lineTo(sx, H - 950)
            sp.lineTo(sx + 140, H - 450)
            sp.close()
            cv.drawPath(sp, spire_paint)
            # Kalash on peak
            cv.drawCircle(sx, H - 960, 14, skia.Paint(Color=skia.ColorSetARGB(255, 235, 190, 50), AntiAlias=True))

        # Royal Palace Marble Pillars
        pillar_paint = skia.Paint(
            Shader=skia.GradientShader.MakeLinear(
                [skia.Point(0, 0), skia.Point(120, 0)],
                [skia.ColorSetARGB(240, 240, 225, 195), skia.ColorSetARGB(240, 180, 160, 135), skia.ColorSetARGB(240, 110, 95, 75)],
                [0.0, 0.5, 1.0]
            ),
            AntiAlias=True
        )
        cv.drawRect(skia.Rect(40, 0, 160, H), pillar_paint)
        cv.drawRect(skia.Rect(W - 160, 0, W - 40, H), pillar_paint)

        # Hanging Brass Diya with Flickering Flame
        for dx in [100, W - 100]:
            # Chain
            cv.drawLine(dx, 0, dx, 450, skia.Paint(StrokeWidth=4, Color=skia.ColorSetARGB(255, 215, 175, 45), AntiAlias=True))
            # Diya Bowl
            cv.drawOval(skia.Rect(dx - 35, 440, dx + 35, 470), skia.Paint(Color=skia.ColorSetARGB(255, 205, 155, 30), AntiAlias=True))
            # Flickering Golden Flame
            flame_h = 35 + 8 * math.sin(t_sec * 12 + dx)
            flame_paint = skia.Paint(
                Shader=skia.GradientShader.MakeRadial(
                    skia.Point(dx, 440 - flame_h * 0.4), flame_h,
                    [skia.ColorSetARGB(255, 255, 250, 200), skia.ColorSetARGB(200, 255, 160, 30), skia.ColorSetARGB(0, 255, 80, 0)],
                    [0.0, 0.5, 1.0]
                ),
                AntiAlias=True
            )
            cv.drawCircle(dx, 440 - flame_h * 0.4, flame_h, flame_paint)


def draw_sacred_shila(cv, cx, cy, scale=1.0, glow=0.0):
    """
    Sacred Ahilya Stone (मौन पाषाण शिला)
    - Weathered ancient stone with cracked mossy texture
    - Emerging divine golden-white celestial radiance as Shri Ram approaches
    """
    cv.save()
    cv.translate(cx, cy)
    cv.scale(scale, scale)

    # 1. Emerging Divine Aura if touched
    if glow > 0.05:
        aura_paint = skia.Paint(
            Shader=skia.GradientShader.MakeRadial(
                skia.Point(0, -30), 160 * glow,
                [skia.ColorSetARGB(int(240 * glow), 255, 250, 220), skia.ColorSetARGB(int(140 * glow), 255, 200, 70), skia.ColorSetARGB(0, 255, 160, 20)],
                [0.0, 0.6, 1.0]
            ),
            AntiAlias=True
        )
        cv.drawCircle(0, -30, 160 * glow, aura_paint)

    # 2. Rock Base (शिला)
    shila_p = skia.Path()
    shila_p.moveTo(-110, 40)
    shila_p.cubicTo(-130, -20, -70, -85, 0, -95)
    shila_p.cubicTo(70, -85, 130, -20, 110, 40)
    shila_p.close()

    rock_shader = skia.GradientShader.MakeLinear(
        [skia.Point(-110, -95), skia.Point(110, 40)],
        [skia.ColorSetARGB(255, 120, 115, 110), skia.ColorSetARGB(255, 65, 60, 62), skia.ColorSetARGB(255, 38, 35, 40)],
        [0.0, 0.6, 1.0]
    )
    cv.drawPath(shila_p, skia.Paint(Shader=rock_shader, AntiAlias=True))
    cv.drawPath(shila_p, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=4, Color=skia.ColorSetARGB(255, 45, 40, 45), AntiAlias=True))

    # Cracks & Ancient Moss Veins
    cv.drawLine(-50, -40, -10, 10, skia.Paint(StrokeWidth=3, Color=skia.ColorSetARGB(180, 25, 22, 28), AntiAlias=True))
    cv.drawLine(-10, 10, 35, -20, skia.Paint(StrokeWidth=2.5, Color=skia.ColorSetARGB(180, 25, 22, 28), AntiAlias=True))
    cv.drawLine(20, -60, 45, -30, skia.Paint(StrokeWidth=2, Color=skia.ColorSetARGB(180, 40, 85, 45), AntiAlias=True))

    cv.restore()


def draw_cinematic_ahilya(cv, cx, cy, scale=1.0, emergence=1.0):
    """
    Mata Ahilya Emerging from Shila (शिला से दिव्य उद्धार)
    - Sacred golden-white aura of liberation (मुक्ति तेज)
    - Hands folded in reverent prayer (करबद्ध प्रार्थना)
    - Lotus eyes filled with divine tears of devotion and gratitude
    - Pure ascetic ivory and saffron attire
    """
    cv.save()
    cv.translate(cx, cy)
    cv.scale(scale * emergence, scale * emergence)

    # 1. Ethereal Divine Aura
    draw_ornate_aura(cv, 0, -90, 220, pulse=1.0 + 0.05 * math.sin(emergence * 4), color_scheme="gold")

    # 2. Sacred Robe (Ivory & Saffron Ascetic Saree)
    C_SKIN = skia.ColorSetARGB(255, 245, 205, 165)
    C_SAREE_BASE = skia.ColorSetARGB(255, 252, 248, 238)
    C_SAREE_SHADOW = skia.ColorSetARGB(255, 215, 195, 175)
    C_GOLD = skia.ColorSetARGB(255, 235, 185, 45)

    robe_p = skia.Path()
    robe_p.moveTo(-70, 35)
    robe_p.cubicTo(-95, 120, -75, 230, -65, 360)
    robe_p.lineTo(65, 360)
    robe_p.cubicTo(75, 230, 95, 120, 70, 35)
    robe_p.close()

    r_shader = skia.GradientShader.MakeLinear(
        [skia.Point(-70, 35), skia.Point(70, 360)],
        [C_SAREE_BASE, C_SAREE_SHADOW],
        [0.0, 1.0]
    )
    cv.drawPath(robe_p, skia.Paint(Shader=r_shader, AntiAlias=True))
    cv.drawPath(robe_p, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=3.5, Color=C_GOLD, AntiAlias=True))

    # Flowing Pallu draped over head and shoulder
    pallu_p = skia.Path()
    pallu_p.moveTo(-50, -120)
    pallu_p.cubicTo(-75, -50, -85, 80, -95, 260)
    pallu_p.lineTo(-65, 275)
    pallu_p.cubicTo(-55, 90, -45, -40, -35, -115)
    pallu_p.close()
    cv.drawPath(pallu_p, skia.Paint(Color=C_SAREE_BASE, AntiAlias=True))
    cv.drawPath(pallu_p, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=2.5, Color=C_GOLD, AntiAlias=True))

    # 3. Head & Divine Facial Features
    cv.drawCircle(0, -90, 50, skia.Paint(Color=C_SKIN, AntiAlias=True))

    # Sacred Vermilion Bindi on forehead
    cv.drawCircle(0, -105, 4, skia.Paint(Color=skia.ColorSetARGB(255, 215, 30, 35), AntiAlias=True))

    # Eyes filled with devotion and gratitude (कमल नयन)
    for s in [-1, 1]:
        ex = s * 18
        ey = -90
        eye_p = skia.Path()
        eye_p.moveTo(ex - 12, ey)
        eye_p.cubicTo(ex - 5, ey - 7, ex + 5, ey - 7, ex + 12, ey)
        eye_p.cubicTo(ex + 5, ey + 7, ex - 5, ey + 7, ex - 12, ey)
        eye_p.close()
        cv.drawPath(eye_p, skia.Paint(Color=skia.ColorWHITE, AntiAlias=True))
        cv.drawCircle(ex, ey, 5, skia.Paint(Color=skia.ColorSetARGB(255, 45, 30, 25), AntiAlias=True))
        cv.drawCircle(ex - 1.8, ey - 1.8, 1.8, skia.Paint(Color=skia.ColorWHITE, AntiAlias=True))
        # Tear of gratitude
        cv.drawCircle(ex, ey + 10, 2.0, skia.Paint(Color=skia.ColorSetARGB(200, 220, 240, 255), AntiAlias=True))

    # Gentle Smile of Liberation
    smile_p = skia.Path()
    smile_p.moveTo(-10, -68)
    smile_p.cubicTo(-3, -63, 3, -63, 10, -68)
    cv.drawPath(smile_p, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=2.2, Color=skia.ColorSetARGB(255, 175, 45, 55), AntiAlias=True))

    # 4. Folded Hands in Prayer (करबद्ध हाथ / Anjali Mudra)
    hands_p = skia.Path()
    hands_p.moveTo(-16, 50)
    hands_p.lineTo(0, 10)
    hands_p.lineTo(16, 50)
    hands_p.close()
    cv.drawPath(hands_p, skia.Paint(Color=C_SKIN, AntiAlias=True))
    cv.drawPath(hands_p, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=2.5, Color=skia.ColorSetARGB(255, 185, 130, 85), AntiAlias=True))

    cv.restore()


def draw_sacred_pinaka_bow(cv, cx, cy, scale=1.0, glow=1.0, crack=0.0):
    """
    Renders Lord Shiva's Divine Pinaka Bow resting on the 8-Wheeled Heavy Iron Chariot Cart.
    Includes dark bronze-obsidian finish, serpent motifs, glowing runes, and electric aura.
    """
    cv.save()
    cv.translate(cx, cy)
    cv.scale(scale, scale)

    # 1. Divine Shiva Aura (Cyan-Gold Resonant Pulse)
    if glow > 0:
        aura_p = skia.Paint(
            Shader=skia.GradientShader.MakeRadial(
                skia.Point(0, -180), 320,
                [skia.ColorSetARGB(int(140 * glow), 65, 185, 255), skia.ColorSetARGB(int(60 * glow), 245, 195, 60), skia.ColorTRANSPARENT],
                [0.0, 0.55, 1.0]
            ),
            AntiAlias=True
        )
        cv.drawCircle(0, -180, 320, aura_p)

    # 2. Eight-Wheeled Heavy Iron Cart Base (अष्ट-चक्र लौह-रथ)
    cart_paint = skia.Paint(
        Shader=skia.GradientShader.MakeLinear(
            [skia.Point(0, 0), skia.Point(0, 80)],
            [skia.ColorSetARGB(255, 38, 32, 42), skia.ColorSetARGB(255, 18, 15, 22)],
            [0.0, 1.0]
        ),
        AntiAlias=True
    )
    # Heavy Iron Bed
    cv.drawRoundRect(skia.Rect(-280, 0, 280, 55), 12, 12, cart_paint)
    cv.drawRoundRect(skia.Rect(-280, 0, 280, 55), 12, 12, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=3, Color=skia.ColorSetARGB(255, 95, 85, 105), AntiAlias=True))

    # Iron Wheels with Brass Hubs
    wheel_xs = [-240, -160, -80, 80, 160, 240]
    for wx in wheel_xs:
        cv.drawCircle(wx, 55, 32, cart_paint)
        cv.drawCircle(wx, 55, 32, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=3.5, Color=skia.ColorSetARGB(255, 120, 110, 130), AntiAlias=True))
        cv.drawCircle(wx, 55, 10, skia.Paint(Color=skia.ColorSetARGB(255, 220, 175, 55), AntiAlias=True))

    # Heavy Iron Chains Binding the Bow to the Cart
    chain_p = skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=5, Color=skia.ColorSetARGB(255, 140, 130, 150), AntiAlias=True)
    for ch_x in [-180, -60, 60, 180]:
        cv.drawLine(ch_x, 5, ch_x - 15, -45, chain_p)
        cv.drawLine(ch_x - 15, -45, ch_x + 10, -55, chain_p)

    # 3. Massive Divine Bow Body (Pinaka)
    bow_body = skia.Path()
    bow_body.moveTo(-220, -15)
    bow_body.cubicTo(-260, -160, -180, -320, 0, -340)
    bow_body.cubicTo(180, -320, 260, -160, 220, -15)
    bow_body.cubicTo(235, -15, 205, -305, 0, -325)
    bow_body.cubicTo(-205, -305, -235, -15, -220, -15)
    bow_body.close()

    bow_paint = skia.Paint(
        Shader=skia.GradientShader.MakeLinear(
            [skia.Point(-220, -15), skia.Point(220, -340)],
            [skia.ColorSetARGB(255, 30, 22, 28), skia.ColorSetARGB(255, 75, 48, 38), skia.ColorSetARGB(255, 25, 18, 24)],
            [0.0, 0.5, 1.0]
        ),
        AntiAlias=True
    )
    cv.drawPath(bow_body, bow_paint)
    cv.drawPath(bow_body, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=4.5, Color=skia.ColorSetARGB(255, 225, 175, 55), AntiAlias=True))

    # Glowing Blue Shiva Runes along the Bow Limbs
    rune_paint = skia.Paint(Color=skia.ColorSetARGB(235, 100, 215, 255), AntiAlias=True)
    for rx in [-150, -100, -50, 50, 100, 150]:
        ry = -315 + abs(rx) * 0.95
        cv.drawCircle(rx, ry, 4.5, rune_paint)
        cv.drawCircle(rx, ry, 8.0, skia.Paint(Color=skia.ColorSetARGB(90, 80, 200, 255), AntiAlias=True))

    # Serpent Carvings (Sheshanaga Motif) on the Tips
    for s_side, sx in [(-1, -220), (1, 220)]:
        cv.drawCircle(sx, -15, 14, skia.Paint(Color=skia.ColorSetARGB(255, 235, 185, 50), AntiAlias=True))
        cv.drawCircle(sx + s_side * 5, -18, 4, skia.Paint(Color=skia.ColorSetARGB(255, 220, 30, 30), AntiAlias=True))

    # 4. Taut Golden Bowstring (प्रत्यंचा)
    string_p = skia.Paint(
        StrokeWidth=3.5,
        Color=skia.ColorSetARGB(255, 255, 240, 140),
        AntiAlias=True
    )
    cv.drawLine(-220, -15, 220, -15, string_p)
    cv.drawCircle(0, -15, 6, skia.Paint(Color=skia.ColorSetARGB(240, 255, 255, 220), AntiAlias=True))

    cv.restore()


def draw_maharaja_janak(cv, cx, cy, scale=1.0, agony=1.0, breathing=0.0):
    """
    Renders Maharaja Janak of Mithila with Royal Crown, White Beard, Royal Robes,
    and expressive features portraying grief/despair in the Swayamwar hall.
    """
    cv.save()
    cv.translate(cx, cy)
    cv.scale(scale, scale)

    # 1. Royal Purple & Gold Angavastra
    robe_paint = skia.Paint(
        Shader=skia.GradientShader.MakeLinear(
            [skia.Point(-120, -60), skia.Point(120, 240)],
            [skia.ColorSetARGB(255, 65, 20, 65), skia.ColorSetARGB(255, 95, 30, 85), skia.ColorSetARGB(255, 45, 12, 45)],
            [0.0, 0.5, 1.0]
        ),
        AntiAlias=True
    )
    torso_p = skia.Path()
    torso_p.moveTo(-75, -50)
    torso_p.lineTo(75, -50)
    torso_p.lineTo(95, 200)
    torso_p.lineTo(-95, 200)
    torso_p.close()
    cv.drawPath(torso_p, robe_paint)
    cv.drawPath(torso_p, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=4, Color=skia.ColorSetARGB(255, 245, 195, 55), AntiAlias=True))

    # Golden Royal Sash / Uttariya draped across chest
    sash_p = skia.Path()
    sash_p.moveTo(-75, -50)
    sash_p.lineTo(-20, -50)
    sash_p.lineTo(95, 170)
    sash_p.lineTo(65, 195)
    sash_p.close()
    cv.drawPath(sash_p, skia.Paint(Color=skia.ColorSetARGB(255, 225, 175, 45), AntiAlias=True))

    # 2. Venerable Head & Majestic White Beard
    cv.drawCircle(0, -95, 50, skia.Paint(Color=skia.ColorSetARGB(255, 235, 190, 150), AntiAlias=True))

    # Flowing White Beard of the Sage-King
    beard_p = skia.Path()
    beard_p.moveTo(-42, -85)
    beard_p.cubicTo(-48, -20, -35, 60, 0, 95)
    beard_p.cubicTo(35, 60, 48, -20, 42, -85)
    beard_p.close()
    cv.drawPath(beard_p, skia.Paint(Color=skia.ColorSetARGB(255, 242, 242, 246), AntiAlias=True))
    cv.drawPath(beard_p, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=2, Color=skia.ColorSetARGB(180, 200, 200, 210), AntiAlias=True))

    # White Moustache
    m_p = skia.Path()
    m_p.moveTo(-32, -75)
    m_p.cubicTo(-15, -60, 0, -68, 0, -72)
    m_p.cubicTo(0, -68, 15, -60, 32, -75)
    m_p.cubicTo(20, -82, -20, -82, -32, -75)
    m_p.close()
    cv.drawPath(m_p, skia.Paint(Color=skia.ColorSetARGB(255, 245, 245, 250), AntiAlias=True))

    # Eyes of Agony / Sorrow (Tears Glistening)
    for s in [-1, 1]:
        ex = s * 18
        ey = -100
        cv.drawLine(ex - 12 * s, ey - 16 - agony * 4, ex + 12 * s, ey - 10, skia.Paint(StrokeWidth=3, Color=skia.ColorSetARGB(255, 180, 180, 190), AntiAlias=True))
        cv.drawCircle(ex, ey, 6.5, skia.Paint(Color=skia.ColorSetARGB(255, 55, 40, 35), AntiAlias=True))
        cv.drawCircle(ex - 1.5, ey - 1.5, 2, skia.Paint(Color=skia.ColorWHITE, AntiAlias=True))
        if agony > 0.3:
            cv.drawCircle(ex, ey + 12, 2.5, skia.Paint(Color=skia.ColorSetARGB(220, 230, 245, 255), AntiAlias=True))

    # 3. Royal Mithila Crown (त्रि-शिखर स्वर्ण मुकुट)
    crown_p = skia.Path()
    crown_p.moveTo(-52, -135)
    crown_p.lineTo(-42, -190)
    crown_p.lineTo(-18, -155)
    crown_p.lineTo(0, -215)
    crown_p.lineTo(18, -155)
    crown_p.lineTo(42, -190)
    crown_p.lineTo(52, -135)
    crown_p.close()
    cv.drawPath(crown_p, skia.Paint(
        Shader=skia.GradientShader.MakeLinear(
            [skia.Point(-52, -215), skia.Point(52, -135)],
            [skia.ColorSetARGB(255, 255, 225, 75), skia.ColorSetARGB(255, 215, 160, 35)],
            [0.0, 1.0]
        ),
        AntiAlias=True
    ))
    cv.drawPath(crown_p, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=3, Color=skia.ColorSetARGB(255, 160, 110, 20), AntiAlias=True))
    cv.drawCircle(0, -165, 8, skia.Paint(Color=skia.ColorSetARGB(255, 215, 25, 35), AntiAlias=True))
    cv.drawLine(0, -125, 0, -108, skia.Paint(StrokeWidth=3, Color=skia.ColorSetARGB(255, 215, 30, 35), AntiAlias=True))

    cv.restore()


def draw_mighty_kings_struggle(cv, cx, cy, scale=1.0, strain=1.0):
    """
    Renders two mighty warrior kings straining with full arrogance and power
    against the immovable sacred Pinaka bow.
    """
    cv.save()
    cv.translate(cx, cy)
    cv.scale(scale, scale)

    # King 1 (Left side, straining rightwards)
    for side, kx in [(-1, -120), (1, 120)]:
        cv.save()
        cv.translate(kx, 0)
        cv.scale(side, 1)

        # Muscular armored torso
        body_p = skia.Path()
        body_p.moveTo(-45, 120)
        body_p.lineTo(-65, -20)
        body_p.lineTo(-30, -80)
        body_p.lineTo(25, -80)
        body_p.lineTo(45, -20)
        body_p.lineTo(30, 120)
        body_p.close()
        # Heavy bronze armor
        cv.drawPath(body_p, skia.Paint(
            Shader=skia.GradientShader.MakeLinear(
                [skia.Point(-65, -80), skia.Point(45, 120)],
                [skia.ColorSetARGB(255, 140, 85, 35), skia.ColorSetARGB(255, 75, 45, 20)],
                [0.0, 1.0]
            ),
            AntiAlias=True
        ))
        cv.drawPath(body_p, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=3, Color=skia.ColorSetARGB(255, 210, 150, 60), AntiAlias=True))

        # Strained arm reaching toward bow center
        arm_p = skia.Path()
        arm_p.moveTo(-10, -60)
        arm_p.lineTo(60, -20 + strain * 5)
        arm_p.lineTo(110, -10 + strain * 8)
        cv.drawPath(arm_p, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=28, StrokeCap=skia.Paint.kRound_Cap, Color=skia.ColorSetARGB(255, 160, 95, 45), AntiAlias=True))
        # Spiked bronze bracer
        cv.drawCircle(80, -15, 16, skia.Paint(Color=skia.ColorSetARGB(255, 215, 165, 45), AntiAlias=True))

        # Fierce helmet with horns
        head_p = skia.Path()
        head_p.moveTo(-25, -80)
        head_p.lineTo(-20, -135)
        head_p.lineTo(15, -135)
        head_p.lineTo(20, -80)
        head_p.close()
        cv.drawPath(head_p, skia.Paint(Color=skia.ColorSetARGB(255, 95, 60, 25), AntiAlias=True))

        # Helmet Horns
        horn_p = skia.Path()
        horn_p.moveTo(-20, -125)
        horn_p.cubicTo(-55, -165, -35, -205, -15, -215)
        horn_p.cubicTo(-25, -185, -20, -155, -15, -125)
        cv.drawPath(horn_p, skia.Paint(Color=skia.ColorSetARGB(255, 230, 190, 70), AntiAlias=True))

        # Straining sweat drops
        if strain > 0.5:
            cv.drawCircle(25, -95, 3, skia.Paint(Color=skia.ColorSetARGB(200, 210, 240, 255), AntiAlias=True))
            cv.drawCircle(32, -80, 2.5, skia.Paint(Color=skia.ColorSetARGB(200, 210, 240, 255), AntiAlias=True))

        cv.restore()

    # Red anger / frustration aura around kings
    cv.drawCircle(0, 0, 280, skia.Paint(
        Shader=skia.GradientShader.MakeRadial(
            skia.Point(0, 0), 280,
            [skia.ColorSetARGB(70, 220, 40, 20), skia.ColorTRANSPARENT],
            [0.2, 1.0]
        ),
        AntiAlias=True
    ))

    cv.restore()


def draw_ram_extreme_profile_pull(cv, cx, cy, scale=1.0, pull=1.0, spark=True):
    """
    Cinema-Grade Heroic Profile Close-up:
    Shri Ram's focused divine lotus eyes, golden Suryavanshi mukut,
    and hands pulling the Pinaka bowstring right back to his ear.
    Electric sparks and celestial energy crackling.
    """
    cv.save()
    cv.translate(cx, cy)
    cv.scale(scale, scale)

    # 1. Divine Aura Flare
    cv.drawCircle(0, -60, 320, skia.Paint(
        Shader=skia.GradientShader.MakeRadial(
            skia.Point(0, -60), 320,
            [skia.ColorSetARGB(180, 255, 225, 110), skia.ColorSetARGB(60, 255, 150, 30), skia.ColorTRANSPARENT],
            [0.1, 0.6, 1.0]
        ),
        AntiAlias=True
    ))

    # 2. Celestial Blue Contoured Face (Heroic Profile)
    face_p = skia.Path()
    face_p.moveTo(-110, 80)
    face_p.cubicTo(-130, -30, -110, -140, -40, -190)
    face_p.cubicTo(20, -190, 80, -140, 95, -50)
    face_p.cubicTo(105, 30, 80, 110, 20, 140)
    face_p.cubicTo(-40, 150, -85, 130, -110, 80)
    face_p.close()

    cv.drawPath(face_p, skia.Paint(
        Shader=skia.GradientShader.MakeLinear(
            [skia.Point(-110, -190), skia.Point(95, 140)],
            [skia.ColorSetARGB(255, 45, 120, 195), skia.ColorSetARGB(255, 20, 75, 145), skia.ColorSetARGB(255, 12, 45, 95)],
            [0.0, 0.6, 1.0]
        ),
        AntiAlias=True
    ))

    # Golden Rim Light on Jaw and Brow
    cv.drawPath(face_p, skia.Paint(
        Style=skia.Paint.kStroke_Style, StrokeWidth=5,
        Color=skia.ColorSetARGB(180, 255, 230, 130), AntiAlias=True
    ))

    # 3. Divine Lotus Eye (कमल नयन - Focused Heroic Glint)
    eye_x, eye_y = -10, -55
    eye_p = skia.Path()
    eye_p.moveTo(eye_x - 38, eye_y)
    eye_p.cubicTo(eye_x - 15, eye_y - 20, eye_x + 18, eye_y - 20, eye_x + 42, eye_y)
    eye_p.cubicTo(eye_x + 18, eye_y + 18, eye_x - 15, eye_y + 18, eye_x - 38, eye_y)
    eye_p.close()
    cv.drawPath(eye_p, skia.Paint(Color=skia.ColorSetARGB(255, 248, 248, 252), AntiAlias=True))
    # Iris
    cv.drawCircle(eye_x + 2, eye_y, 14, skia.Paint(Color=skia.ColorSetARGB(255, 25, 30, 45), AntiAlias=True))
    # Catchlight
    cv.drawCircle(eye_x + 6, eye_y - 4, 4.5, skia.Paint(Color=skia.ColorWHITE, AntiAlias=True))
    # Upper Lash & Eyebrow
    cv.drawPath(eye_p, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=3.5, Color=skia.ColorSetARGB(255, 15, 20, 30), AntiAlias=True))
    brow_p = skia.Path()
    brow_p.moveTo(eye_x - 44, eye_y - 26)
    brow_p.cubicTo(eye_x - 10, eye_y - 42, eye_x + 25, eye_y - 38, eye_x + 50, eye_y - 22)
    cv.drawPath(brow_p, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=6, StrokeCap=skia.Paint.kRound_Cap, Color=skia.ColorSetARGB(255, 12, 18, 28), AntiAlias=True))

    # Tilak
    tilak_p = skia.Path()
    tilak_p.moveTo(eye_x - 70, eye_y - 85)
    tilak_p.lineTo(eye_x - 70, eye_y - 145)
    cv.drawPath(tilak_p, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=7, Color=skia.ColorSetARGB(255, 245, 240, 215), AntiAlias=True))
    cv.drawCircle(eye_x - 70, eye_y - 100, 5, skia.Paint(Color=skia.ColorSetARGB(255, 210, 25, 35), AntiAlias=True))

    # 4. Makara-Kundal (Golden Earring touching bowstring)
    cv.drawCircle(78, -35, 18, skia.Paint(Color=skia.ColorSetARGB(255, 245, 205, 55), AntiAlias=True))
    cv.drawCircle(78, -12, 8, skia.Paint(Color=skia.ColorSetARGB(255, 255, 240, 180), AntiAlias=True))

    # 5. Bowstring Pulled to Ear!
    pull_x = 75 - (1.0 - pull) * 80
    pull_y = -30
    cv.drawLine(-160, -320, pull_x, pull_y, skia.Paint(StrokeWidth=5, Color=skia.ColorSetARGB(255, 255, 245, 210), AntiAlias=True))
    cv.drawLine(pull_x, pull_y, -140, 280, skia.Paint(StrokeWidth=5, Color=skia.ColorSetARGB(255, 255, 245, 210), AntiAlias=True))

    # Arm & Golden Gauntlet
    cv.drawCircle(pull_x + 12, pull_y, 22, skia.Paint(Color=skia.ColorSetARGB(255, 225, 175, 45), AntiAlias=True))
    cv.drawCircle(pull_x + 12, pull_y, 14, skia.Paint(Color=skia.ColorSetARGB(255, 255, 230, 110), AntiAlias=True))

    # 6. Arcane Electric Sparks (Lightning crackling on wood)
    if spark:
        for _ in range(8):
            sx = pull_x + random.uniform(-60, 40)
            sy = pull_y + random.uniform(-80, 80)
            cv.drawLine(pull_x, pull_y, sx, sy, skia.Paint(StrokeWidth=2.5, Color=skia.ColorSetARGB(230, 200, 240, 255), AntiAlias=True))
            cv.drawCircle(sx, sy, 3.5, skia.Paint(Color=skia.ColorWHITE, AntiAlias=True))

    cv.restore()


def draw_cosmic_lightning_burst(cv, cx, cy, intensity=1.0, seed=42):
    """
    Renders violent branching divine lightning bolts and cosmic shockwaves.
    """
    np.random.seed(seed)
    cv.save()
    cv.translate(cx, cy)

    # Radial blinding shockwave
    cv.drawCircle(0, 0, 450 * intensity, skia.Paint(
        Shader=skia.GradientShader.MakeRadial(
            skia.Point(0, 0), 450 * intensity,
            [skia.ColorSetARGB(230, 255, 255, 255), skia.ColorSetARGB(140, 120, 210, 255), skia.ColorTRANSPARENT],
            [0.1, 0.45, 1.0]
        ),
        AntiAlias=True
    ))

    # Branching bolts
    for b in range(12):
        angle = (b / 12.0) * 2 * math.pi + np.random.uniform(-0.15, 0.15)
        cur_x, cur_y = 0, 0
        dist = np.random.uniform(220, 550) * intensity
        steps = 6
        p = skia.Path()
        p.moveTo(0, 0)
        for s in range(1, steps + 1):
            r = (s / steps) * dist
            jitter = np.random.uniform(-25, 25)
            nx = r * math.cos(angle) + jitter * math.sin(angle)
            ny = r * math.sin(angle) + jitter * math.cos(angle)
            p.lineTo(nx, ny)
        cv.drawPath(p, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=4, Color=skia.ColorWHITE, AntiAlias=True))
        cv.drawPath(p, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=10, Color=skia.ColorSetARGB(120, 100, 190, 255), AntiAlias=True))

    cv.restore()
