"""
EP008 Visual Rigs:
- Vaishnava Sharang Bow (Golden celestial recurve with Sudarshana Chakra emblems & Brahmastra arrow)
- Parashurama Devotion & Surrender Pose (Axe on floor, folded hands Anjali Mudra, tears of devotion)
- Shri Ram Cosmic Divine Form (Drawing Vaishnava Bow with cosmic radial sunburst aura)
"""

import math
import skia

def draw_golden_vaishnava_bow(cv, cx, cy, scale=1.0, glow=1.0, bow_draw=0.0):
    """
    Renders the divine Vaishnava Sharang bow of Lord Vishnu.
    Solar gold recurve bow with chakra reliefs, ruby inlays, and blazing Brahmastra arrow.
    """
    cv.save()
    cv.translate(cx, cy)
    cv.scale(scale, scale)

    # 1. Divine Aura Glow
    if glow > 0:
        glow_paint = skia.Paint(
            Shader=skia.GradientShader.MakeRadial(
                skia.Point(0, 0), 220,
                [skia.ColorSetARGB(int(140 * glow), 255, 220, 80),
                 skia.ColorSetARGB(int(60 * glow), 255, 160, 30),
                 skia.ColorTRANSPARENT],
                [0.0, 0.5, 1.0]
            ),
            AntiAlias=True
        )
        cv.drawCircle(0, 0, 220, glow_paint)

    # 2. Celestial Recurve Limbs
    # Upper Limb
    upper_path = skia.Path()
    upper_path.moveTo(0, 0)
    upper_path.cubicTo(-60, -90, -110, -220, -50, -320)
    upper_path.cubicTo(-40, -340, -10, -350, 0, -350)
    upper_path.cubicTo(-20, -330, -70, -200, 0, 0)

    # Lower Limb
    lower_path = skia.Path()
    lower_path.moveTo(0, 0)
    lower_path.cubicTo(-60, 90, -110, 220, -50, 320)
    lower_path.cubicTo(-40, 340, -10, 350, 0, 350)
    lower_path.cubicTo(-20, 330, -70, 200, 0, 0)

    gold_shader = skia.GradientShader.MakeLinear(
        [skia.Point(-100, -350), skia.Point(50, 350)],
        [skia.ColorSetARGB(255, 255, 235, 140),
         skia.ColorSetARGB(255, 230, 175, 45),
         skia.ColorSetARGB(255, 180, 115, 20),
         skia.ColorSetARGB(255, 255, 215, 80)],
        [0.0, 0.35, 0.75, 1.0]
    )
    gold_fill = skia.Paint(Shader=gold_shader, AntiAlias=True)
    cv.drawPath(upper_path, gold_fill)
    cv.drawPath(lower_path, gold_fill)

    # 3. Gold Limb Contours & Highlights
    gold_stroke = skia.Paint(
        Style=skia.Paint.kStroke_Style,
        StrokeWidth=4.0,
        Color=skia.ColorSetARGB(255, 255, 248, 200),
        AntiAlias=True
    )
    cv.drawPath(upper_path, gold_stroke)
    cv.drawPath(lower_path, gold_stroke)

    # 4. Central Grip & Sudarshana Chakra Relief
    grip_paint = skia.Paint(Color=skia.ColorSetARGB(255, 160, 20, 30), AntiAlias=True) # Royal crimson wrap
    cv.drawRoundRect(skia.Rect(-22, -45, 22, 45), 10, 10, grip_paint)
    cv.drawRoundRect(skia.Rect(-22, -45, 22, 45), 10, 10, gold_stroke)

    # Center Chakra Symbol (Vishnu's Mark)
    cv.drawCircle(0, 0, 18, skia.Paint(Color=skia.ColorSetARGB(255, 255, 225, 90), AntiAlias=True))
    cv.drawCircle(0, 0, 10, skia.Paint(Color=skia.ColorSetARGB(255, 200, 40, 30), AntiAlias=True))
    # Chakra Spokes
    spoke_paint = skia.Paint(
        Style=skia.Paint.kStroke_Style,
        StrokeWidth=2.5,
        Color=skia.ColorSetARGB(255, 255, 245, 180),
        AntiAlias=True
    )
    for ang in range(0, 360, 45):
        rad = math.radians(ang)
        cv.drawLine(0, 0, 16 * math.cos(rad), 16 * math.sin(rad), spoke_paint)

    # 5. Celestial Bowstring (Drawn back according to bow_draw)
    string_pull_x = 110 * bow_draw
    string_path = skia.Path()
    string_path.moveTo(0, -345)
    string_path.lineTo(string_pull_x, 0)
    string_path.lineTo(0, 345)

    string_paint = skia.Paint(
        Style=skia.Paint.kStroke_Style,
        StrokeWidth=3.0,
        Color=skia.ColorSetARGB(240, 255, 255, 240),
        AntiAlias=True
    )
    cv.drawPath(string_path, string_paint)

    # 6. Blazing Brahmastra Arrow (when drawn)
    if bow_draw > 0.1:
        arrow_paint = skia.Paint(
            Style=skia.Paint.kStroke_Style,
            StrokeWidth=5.5,
            Color=skia.ColorSetARGB(255, 255, 240, 160),
            AntiAlias=True
        )
        # Arrow shaft
        arrow_len = 340
        start_ax = string_pull_x - arrow_len
        cv.drawLine(string_pull_x, 0, start_ax, 0, arrow_paint)
        
        # Golden Arrowhead
        tip_path = skia.Path()
        tip_path.moveTo(start_ax - 35, 0)
        tip_path.lineTo(start_ax, -16)
        tip_path.lineTo(start_ax - 8, 0)
        tip_path.lineTo(start_ax, 16)
        tip_path.close()
        cv.drawPath(tip_path, skia.Paint(Color=skia.ColorSetARGB(255, 255, 245, 190), AntiAlias=True))

        # Solar Energy Sparkles at Arrowhead
        sparkle_paint = skia.Paint(
            Shader=skia.GradientShader.MakeRadial(
                skia.Point(start_ax - 20, 0), 65,
                [skia.ColorSetARGB(240, 255, 255, 255),
                 skia.ColorSetARGB(180, 255, 200, 50),
                 skia.ColorTRANSPARENT],
                [0.0, 0.4, 1.0]
            ),
            AntiAlias=True
        )
        cv.drawCircle(start_ax - 20, 0, 65, sparkle_paint)

    cv.restore()

def draw_parashurama_surrender(cv, cx, ground_y, scale=1.0):
    """
    Renders Bhagwan Parashurama in profound reverence (Anjali Mudra / Folded Hands).
    Axe resting horizontally at his feet, eyes filled with tears of divine realization.
    """
    cv.save()
    cv.translate(cx, ground_y)
    cv.scale(scale, scale)

    # 1. Battle Axe laid down at feet
    cv.save()
    cv.translate(-140, -25)
    cv.rotate(85)
    # Handle
    handle_p = skia.Paint(Color=skia.ColorSetARGB(255, 80, 45, 25), AntiAlias=True)
    cv.drawRoundRect(skia.Rect(-8, -160, 8, 160), 4, 4, handle_p)
    # Crescent Blade
    axe_p = skia.Path()
    axe_p.moveTo(0, -120)
    axe_p.cubicTo(60, -150, 95, -90, 85, -50)
    axe_p.cubicTo(70, -10, 30, -50, 0, -70)
    cv.drawPath(axe_p, skia.Paint(Color=skia.ColorSetARGB(255, 180, 190, 205), AntiAlias=True))
    cv.restore()

    # 2. Muscular Legs & Tiger Skin Garment
    leg_p = skia.Paint(Color=skia.ColorSetARGB(255, 205, 145, 100), AntiAlias=True)
    cv.drawRoundRect(skia.Rect(-70, -260, -25, -20), 18, 18, leg_p)
    cv.drawRoundRect(skia.Rect(25, -260, 70, -20), 18, 18, leg_p)

    # Tiger Skin Dhoti
    tiger_p = skia.Paint(Color=skia.ColorSetARGB(255, 220, 130, 35), AntiAlias=True)
    cv.drawRoundRect(skia.Rect(-95, -380, 95, -230), 22, 22, tiger_p)
    # Tiger Stripes
    stripe_p = skia.Paint(Color=skia.ColorSetARGB(180, 40, 20, 10), StrokeWidth=4.5, AntiAlias=True)
    for sy in range(-360, -240, 24):
        cv.drawLine(-70, sy, -30, sy + 10, stripe_p)
        cv.drawLine(30, sy + 5, 75, sy - 5, stripe_p)

    # 3. Broad Muscular Torso Bowing Forward (Subtle 8 degree reverence tilt)
    cv.save()
    cv.rotate(-6, 0, -380)

    torso_p = skia.Paint(Color=skia.ColorSetARGB(255, 215, 150, 105), AntiAlias=True)
    cv.drawRoundRect(skia.Rect(-90, -560, 90, -360), 30, 30, torso_p)

    # Sacred Rudraksha Mala & Yajnopavita
    sacred_thread = skia.Paint(
        Style=skia.Paint.kStroke_Style,
        StrokeWidth=3.5,
        Color=skia.ColorSetARGB(255, 245, 245, 240),
        AntiAlias=True
    )
    cv.drawLine(-70, -550, 60, -370, sacred_thread)

    for ry in range(-540, -380, 28):
        cv.drawCircle(-50 + (ry + 540) * 0.7, ry, 6, skia.Paint(Color=skia.ColorSetARGB(255, 120, 50, 20), AntiAlias=True))

    # 4. Folded Hands (Anjali Mudra) Raised to Chest
    # Left & Right Forearms converging to center
    arm_p = skia.Paint(Color=skia.ColorSetARGB(255, 210, 145, 100), AntiAlias=True)
    # Left arm
    l_arm = skia.Path()
    l_arm.moveTo(-85, -530)
    l_arm.lineTo(-20, -450)
    l_arm.lineTo(0, -470)
    l_arm.lineTo(-65, -540)
    cv.drawPath(l_arm, arm_p)

    # Right arm
    r_arm = skia.Path()
    r_arm.moveTo(85, -530)
    r_arm.lineTo(20, -450)
    r_arm.lineTo(0, -470)
    r_arm.lineTo(65, -540)
    cv.drawPath(r_arm, arm_p)

    # Folded Palms pressed together
    palms_p = skia.Paint(Color=skia.ColorSetARGB(255, 225, 160, 115), AntiAlias=True)
    cv.drawRoundRect(skia.Rect(-16, -495, 16, -435), 8, 8, palms_p)
    cv.drawRoundRect(skia.Rect(-16, -495, 16, -435), 8, 8, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=2, Color=skia.ColorSetARGB(180, 90, 45, 25), AntiAlias=True))

    # 5. Reverent Face & Matted Jatas
    # Neck
    cv.drawRect(skia.Rect(-30, -590, 30, -550), torso_p)
    # Head tilted down in devotion
    head_p = skia.Paint(Color=skia.ColorSetARGB(255, 218, 155, 110), AntiAlias=True)
    cv.drawOval(skia.Rect(-55, -700, 55, -580), head_p)

    # Flowing Ascetic Beard & Mustache
    beard_p = skia.Paint(Color=skia.ColorSetARGB(255, 60, 35, 25), AntiAlias=True)
    b_path = skia.Path()
    b_path.moveTo(-45, -620)
    b_path.cubicTo(-40, -530, 40, -530, 45, -620)
    b_path.close()
    cv.drawPath(b_path, beard_p)

    # Softened Devotional Eyes (Tears of Divine Awe)
    eye_p = skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=3.5, Color=skia.ColorSetARGB(255, 45, 20, 15), AntiAlias=True)
    cv.drawArc(skia.Rect(-38, -655, -14, -640), 10, 160, False, eye_p)
    cv.drawArc(skia.Rect(14, -655, 38, -640), 10, 160, False, eye_p)
    # Tear drops
    tear_p = skia.Paint(Color=skia.ColorSetARGB(220, 180, 220, 255), AntiAlias=True)
    cv.drawCircle(-24, -635, 3.5, tear_p)
    cv.drawCircle(24, -635, 3.5, tear_p)

    # Tripundra on Forehead (Sacred White Ash)
    ash_p = skia.Paint(Color=skia.ColorSetARGB(220, 240, 240, 245), StrokeWidth=3.0, AntiAlias=True)
    for ty in [-675, -670, -665]:
        cv.drawLine(-30, ty, 30, ty, ash_p)
    # Red Bindi
    cv.drawCircle(0, -670, 4.0, skia.Paint(Color=skia.ColorSetARGB(255, 200, 25, 20), AntiAlias=True))

    # Ascetic Jatas (Matted Hair tied in tall bun)
    cv.drawRoundRect(skia.Rect(-60, -780, 60, -680), 25, 25, beard_p)
    cv.drawCircle(0, -760, 35, beard_p)

    cv.restore() # Torso rotate
    cv.restore() # Ground transform


def draw_cosmic_sunburst_aura(cv, cx, cy, radius=450, rays=24, phase=0.0):
    """
    Draws a blinding divine solar sunburst aura that radiates behind Lord Shri Ram.
    """
    cv.save()
    cv.translate(cx, cy)
    cv.rotate(phase * 15)

    # Central Core Glow
    core_shader = skia.GradientShader.MakeRadial(
        skia.Point(0, 0), radius * 0.7,
        [skia.ColorSetARGB(230, 255, 255, 240),
         skia.ColorSetARGB(180, 255, 220, 90),
         skia.ColorSetARGB(80, 255, 140, 20),
         skia.ColorTRANSPARENT],
        [0.0, 0.35, 0.7, 1.0]
    )
    cv.drawCircle(0, 0, radius * 0.7, skia.Paint(Shader=core_shader, AntiAlias=True))

    # Sunburst Rays
    ray_shader = skia.GradientShader.MakeLinear(
        [skia.Point(0, 0), skia.Point(0, radius)],
        [skia.ColorSetARGB(220, 255, 235, 120), skia.ColorTRANSPARENT],
        [0.0, 1.0]
    )
    ray_paint = skia.Paint(Shader=ray_shader, AntiAlias=True)

    angle_step = 360 / rays
    for i in range(rays):
        cv.save()
        cv.rotate(i * angle_step)
        ray_p = skia.Path()
        ray_p.moveTo(0, 0)
        ray_p.lineTo(-14, radius)
        ray_p.lineTo(14, radius)
        ray_p.close()
        cv.drawPath(ray_p, ray_paint)
        cv.restore()

    cv.restore()
