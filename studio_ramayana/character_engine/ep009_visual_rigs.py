"""
EP009 Visual Rigs:
- Mata Sita (Royal Mithila Bridal attire: crimson-gold chunari, royal maang-tikka, lotus eyes, varmala in hands)
- Sacred Vivah Mandap & Yajna Kunda (Golden pillars, marigold/jasmine torans, sacred Vedic wedding fire)
- Varmala (Fragrant lotus and parijat garland with emerald & pearl accents)
"""

import math
import skia

def draw_sacred_vivah_mandap(cv, w=1080, h=1920):
    """
    Renders the royal Mithila Vivah Mandap with golden pillars,
    sacred Yajna Agni Kund, and hanging marigold-jasmine torans.
    """
    # 1. Base Palace Background
    base_shader = skia.GradientShader.MakeLinear(
        [skia.Point(w * 0.5, 0), skia.Point(w * 0.5, h)],
        [skia.ColorSetARGB(255, 35, 12, 18), skia.ColorSetARGB(255, 18, 6, 12), skia.ColorSetARGB(255, 45, 16, 22)],
        [0.0, 0.5, 1.0]
    )
    cv.drawRect(skia.Rect(0, 0, w, h), skia.Paint(Shader=base_shader))

    # 2. Golden Carved Mandap Pillars
    pillar_shader = skia.GradientShader.MakeLinear(
        [skia.Point(0, 0), skia.Point(120, 0)],
        [skia.ColorSetARGB(255, 230, 180, 50),
         skia.ColorSetARGB(255, 255, 225, 120),
         skia.ColorSetARGB(255, 180, 120, 25)],
        [0.0, 0.5, 1.0]
    )
    p_paint = skia.Paint(Shader=pillar_shader, AntiAlias=True)
    p_stroke = skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=3, Color=skia.ColorSetARGB(255, 255, 245, 180), AntiAlias=True)

    # Left & Right Pillars
    for px in [60, w - 160]:
        cv.drawRect(skia.Rect(px, 120, px + 100, h - 220), p_paint)
        cv.drawRect(skia.Rect(px, 120, px + 100, h - 220), p_stroke)
        # Pillar capitals and bases
        cv.drawRoundRect(skia.Rect(px - 15, 120, px + 115, 180), 8, 8, p_paint)
        cv.drawRoundRect(skia.Rect(px - 20, h - 270, px + 120, h - 210), 8, 8, p_paint)

    # 3. Top Decorative Mandap Arch / Canopy (Chandooa)
    arch_path = skia.Path()
    arch_path.moveTo(40, 180)
    arch_path.cubicTo(w * 0.25, 110, w * 0.75, 110, w - 40, 180)
    arch_path.lineTo(w - 40, 130)
    arch_path.cubicTo(w * 0.75, 60, w * 0.25, 60, 40, 130)
    arch_path.close()
    cv.drawPath(arch_path, skia.Paint(Color=skia.ColorSetARGB(255, 240, 195, 60), AntiAlias=True))

    # Hanging Marigold / Jasmine Floral Torans
    toran_orange = skia.Paint(Color=skia.ColorSetARGB(255, 255, 140, 0), AntiAlias=True)
    toran_white = skia.Paint(Color=skia.ColorSetARGB(255, 255, 250, 235), AntiAlias=True)
    for tx in range(120, w - 120, 60):
        # Swag strings
        for ty in range(160, 280, 24):
            cv.drawCircle(tx, ty, 7, toran_orange if ty % 48 == 0 else toran_white)

    # 4. Sacred Vedic Yajna Agni Kund in Center
    center_x = w * 0.5
    kund_y = 1520
    # Tiered Brick Kund
    cv.drawRect(skia.Rect(center_x - 140, kund_y, center_x + 140, kund_y + 45), skia.Paint(Color=skia.ColorSetARGB(255, 160, 60, 35), AntiAlias=True))
    cv.drawRect(skia.Rect(center_x - 110, kund_y - 30, center_x + 110, kund_y), skia.Paint(Color=skia.ColorSetARGB(255, 200, 75, 40), AntiAlias=True))

    # Sacred Agni Flames
    flame_shader = skia.GradientShader.MakeRadial(
        skia.Point(center_x, kund_y - 50), 90,
        [skia.ColorSetARGB(240, 255, 255, 200),
         skia.ColorSetARGB(200, 255, 160, 20),
         skia.ColorSetARGB(140, 240, 40, 10),
         skia.ColorTRANSPARENT],
        [0.0, 0.4, 0.75, 1.0]
    )
    cv.drawCircle(center_x, kund_y - 50, 90, skia.Paint(Shader=flame_shader, AntiAlias=True))

    # Sacred Flame Tongues
    flame_path = skia.Path()
    flame_path.moveTo(center_x - 60, kund_y - 25)
    flame_path.cubicTo(center_x - 40, kund_y - 120, center_x - 10, kund_y - 150, center_x, kund_y - 170)
    flame_path.cubicTo(center_x + 10, kund_y - 150, center_x + 40, kund_y - 120, center_x + 60, kund_y - 25)
    flame_path.close()
    cv.drawPath(flame_path, skia.Paint(Color=skia.ColorSetARGB(230, 255, 200, 50), AntiAlias=True))

def draw_cinematic_mata_sita(cv, cx, cy, scale=1.0, breathing=0.0, varmala_held=True):
    """
    Renders Devi Mata Sita in royal bridal glory:
    - Glowing gold complexion with divine serene radiance
    - Royal crimson bridal chunari with heavy gold zardozi borders
    - Maang tikka, lotus eyes, nath (nose ring), and pearl ornaments
    - Hands gracefully holding the sacred Varmala (lotus & parijat garland)
    """
    cv.save()
    cv.translate(cx, cy)
    cv.scale(scale, scale)

    breath_y = 3.5 * math.sin(breathing * 2.5)
    cv.translate(0, breath_y)

    # 1. Divine Aura (Golden-Cyan Celestial Radiance)
    aura_shader = skia.GradientShader.MakeRadial(
        skia.Point(0, -220), 180,
        [skia.ColorSetARGB(180, 255, 245, 180),
         skia.ColorSetARGB(80, 255, 190, 80),
         skia.ColorTRANSPARENT],
        [0.0, 0.5, 1.0]
    )
    cv.drawCircle(0, -220, 180, skia.Paint(Shader=aura_shader, AntiAlias=True))

    # 2. Flowing Crimson Bridal Chunari (Behind Body)
    veil_shader = skia.GradientShader.MakeLinear(
        [skia.Point(-140, -320), skia.Point(140, 200)],
        [skia.ColorSetARGB(255, 210, 25, 45),
         skia.ColorSetARGB(255, 160, 15, 30),
         skia.ColorSetARGB(255, 230, 40, 60)],
        [0.0, 0.6, 1.0]
    )
    veil_p = skia.Paint(Shader=veil_shader, AntiAlias=True)
    veil_path = skia.Path()
    veil_path.moveTo(0, -310)
    veil_path.cubicTo(-90, -300, -150, -180, -135, 150)
    veil_path.cubicTo(-70, 180, 70, 180, 135, 150)
    veil_path.cubicTo(150, -180, 90, -300, 0, -310)
    veil_path.close()
    cv.drawPath(veil_path, veil_p)

    # Gold Chunari Zardozi Border
    gold_border = skia.Paint(
        Style=skia.Paint.kStroke_Style,
        StrokeWidth=6.0,
        Color=skia.ColorSetARGB(255, 255, 220, 75),
        AntiAlias=True
    )
    cv.drawPath(veil_path, gold_border)

    # 3. Royal Bridal Lehenga (Lower Body)
    lehenga_p = skia.Paint(Color=skia.ColorSetARGB(255, 195, 20, 40), AntiAlias=True)
    l_path = skia.Path()
    l_path.moveTo(-45, -70)
    l_path.lineTo(45, -70)
    l_path.lineTo(95, 160)
    l_path.lineTo(-95, 160)
    l_path.close()
    cv.drawPath(l_path, lehenga_p)

    # Gold Pleats on Lehenga
    gold_thin = skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=3.0, Color=skia.ColorSetARGB(200, 255, 230, 110), AntiAlias=True)
    for lx in range(-75, 80, 25):
        cv.drawLine(lx * 0.5, -60, lx, 155, gold_thin)

    # 4. Graceful Torso & Choli (Golden Yellow with Emerald Inlays)
    choli_shader = skia.GradientShader.MakeLinear(
        [skia.Point(-50, -160), skia.Point(50, -60)],
        [skia.ColorSetARGB(255, 250, 200, 45), skia.ColorSetARGB(255, 215, 155, 25)],
        [0.0, 1.0]
    )
    cv.drawRoundRect(skia.Rect(-50, -165, 50, -65), 18, 18, skia.Paint(Shader=choli_shader, AntiAlias=True))

    # Royal Golden Necklaces (Haar)
    for ny in [-150, -135, -118]:
        rad_w = 26 + (ny + 150) * 0.8
        cv.drawArc(skia.Rect(-rad_w, ny - 10, rad_w, ny + 20), 0, 180, False, gold_thin)

    # Center Emerald Pendant
    cv.drawCircle(0, -95, 7, skia.Paint(Color=skia.ColorSetARGB(255, 20, 160, 60), AntiAlias=True))
    cv.drawCircle(0, -95, 7, gold_thin)

    # 5. Divine Face & Features
    skin_p = skia.Paint(Color=skia.ColorSetARGB(255, 255, 222, 175), AntiAlias=True) # Radiant golden wheatish
    # Neck
    cv.drawRect(skia.Rect(-16, -195, 16, -160), skin_p)
    # Face Oval
    cv.drawOval(skia.Rect(-40, -270, 40, -185), skin_p)

    # Serene Lotus Eyes with Kajal
    eye_p = skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=2.8, Color=skia.ColorSetARGB(255, 30, 15, 20), AntiAlias=True)
    cv.drawArc(skia.Rect(-28, -232, -8, -218), 10, 160, False, eye_p)
    cv.drawArc(skia.Rect(8, -232, 28, -218), 10, 160, False, eye_p)

    # Red Bindi & Chandan Dots
    cv.drawCircle(0, -242, 3.5, skia.Paint(Color=skia.ColorSetARGB(255, 215, 25, 30), AntiAlias=True))
    chandan_p = skia.Paint(Color=skia.ColorSetARGB(255, 255, 250, 240), AntiAlias=True)
    for bx in [-8, -4, 4, 8]:
        cv.drawCircle(bx, -242, 1.5, chandan_p)

    # Sweet Compassionate Lips
    cv.drawOval(skia.Rect(-10, -208, 10, -200), skia.Paint(Color=skia.ColorSetARGB(255, 210, 45, 55), AntiAlias=True))

    # Royal Nath (Nose Ring with Pearl Chain)
    cv.drawCircle(-8, -214, 5.0, gold_thin)
    cv.drawLine(-13, -214, -28, -230, gold_thin)

    # Royal Crown & Maang Tikka
    cv.drawCircle(0, -260, 5.5, skia.Paint(Color=skia.ColorSetARGB(255, 255, 220, 70), AntiAlias=True))
    cv.drawLine(0, -260, 0, -248, gold_thin)

    # Crown Diadem
    crown_p = skia.Paint(Color=skia.ColorSetARGB(255, 255, 215, 60), AntiAlias=True)
    c_path = skia.Path()
    c_path.moveTo(-35, -265)
    c_path.lineTo(0, -305)
    c_path.lineTo(35, -265)
    c_path.close()
    cv.drawPath(c_path, crown_p)
    cv.drawPath(c_path, gold_border)

    # 6. Arms & Sacred Varmala (Held gracefully)
    if varmala_held:
        # Arms in front holding garland
        arm_p = skin_p
        cv.drawRoundRect(skia.Rect(-60, -145, -20, -75), 10, 10, arm_p)
        cv.drawRoundRect(skia.Rect(20, -145, 60, -75), 10, 10, arm_p)
        # Gold Kangans (Bangles)
        cv.drawRect(skia.Rect(-55, -85, -25, -75), gold_border)
        cv.drawRect(skia.Rect(25, -85, 55, -75), gold_border)

        # The Divine Varmala Loop
        var_path = skia.Path()
        var_path.moveTo(-35, -80)
        var_path.cubicTo(-25, -10, 25, -10, 35, -80)
        
        # Rosy Lotus Petals along the garland
        lotus_p = skia.Paint(Color=skia.ColorSetARGB(255, 255, 160, 185), AntiAlias=True)
        white_p = skia.Paint(Color=skia.ColorSetARGB(255, 255, 255, 240), AntiAlias=True)
        for i in range(14):
            t_frac = i / 13.0
            vx = -35 + 70 * t_frac
            vy = -80 + 70 * math.sin(t_frac * math.pi)
            cv.drawCircle(vx, vy, 7.5, lotus_p if i % 2 == 0 else white_p)
            cv.drawCircle(vx, vy, 3.5, skia.Paint(Color=skia.ColorSetARGB(255, 255, 215, 50), AntiAlias=True))

    cv.restore()
