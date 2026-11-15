import math
import skia

W, H = 1080, 1920

def draw_full_body_parashurama(canvas, cx=540, ground_y=1650, scale=1.0):
    """
    Renders Bhagwan Parashurama as a COMPLETE FULL-BODY WARRIOR SAGE:
    - Head & Face: Roaring mouth with teeth, sharp nose, burning eyes, Tripundra, wild flying jatas.
    - Torso & Chest: Muscular warrior physique, tiger-skin sash, Rudraksha malas.
    - Arms & Hands: Left hand pointing fiercely with distinct fingers, Right arm wielding the Parashu battle axe.
    - Legs & Feet: Saffron dhoti, muscular legs, knees, calves, feet planted on cracked ground.
    """
    canvas.save()
    canvas.translate(cx, ground_y)
    canvas.scale(scale, scale)

    # Ground Crack Impact beneath feet
    crack_paint = skia.Paint(Color=skia.ColorSetARGB(180, 255, 60, 40), Style=skia.Paint.kStroke_Style, StrokeWidth=3, AntiAlias=True)
    canvas.drawLine(-140, 0, 140, 0, crack_paint)
    for cx_cr in [-100, -40, 20, 80]:
        canvas.drawLine(cx_cr, 0, cx_cr + 25, 30, crack_paint)
        canvas.drawLine(cx_cr + 25, 30, cx_cr + 10, 50, crack_paint)

    # 1. Aura of Wrath (Crimson & Smoke)
    aura = skia.Paint(
        Shader=skia.GradientShader.MakeRadial(
            skia.Point(0, -650), 650,
            [skia.ColorSetARGB(190, 220, 25, 20), skia.ColorSetARGB(90, 80, 10, 10), skia.ColorSetARGB(0, 0, 0, 0)],
            [0.0, 0.65, 1.0]
        ),
        AntiAlias=True
    )
    canvas.drawCircle(0, -650, 650, aura)

    # 2. FEET & LEGS (पैर और पंजे)
    skin_paint = skia.Paint(
        Shader=skia.GradientShader.MakeLinear(
            [skia.Point(0, -850), skia.Point(0, 0)],
            [skia.ColorSetARGB(255, 205, 140, 95), skia.ColorSetARGB(255, 155, 95, 55)],
            [0.0, 1.0]
        ),
        AntiAlias=True
    )
    skin_outline = skia.Paint(Color=skia.ColorSetARGB(255, 110, 60, 30), Style=skia.Paint.kStroke_Style, StrokeWidth=2.5, AntiAlias=True)

    # Left Foot (Planted forward)
    l_foot = skia.Path()
    l_foot.moveTo(-120, -15)
    l_foot.lineTo(-50, -15)
    l_foot.lineTo(-35, 0)
    l_foot.lineTo(-135, 0)
    l_foot.close()
    canvas.drawPath(l_foot, skin_paint)
    canvas.drawPath(l_foot, skin_outline)
    # 5 Toes on Left Foot
    for tx in range(-130, -50, 16):
        canvas.drawRoundRect(skia.Rect(tx, -8, tx + 13, 0), 4, 4, skin_paint)
        canvas.drawRoundRect(skia.Rect(tx, -8, tx + 13, 0), 4, 4, skin_outline)

    # Right Foot (Braced back)
    r_foot = skia.Path()
    r_foot.moveTo(60, -15)
    r_foot.lineTo(130, -15)
    r_foot.lineTo(145, 0)
    r_foot.lineTo(45, 0)
    r_foot.close()
    canvas.drawPath(r_foot, skin_paint)
    canvas.drawPath(r_foot, skin_outline)
    for tx in range(50, 135, 16):
        canvas.drawRoundRect(skia.Rect(tx, -8, tx + 13, 0), 4, 4, skin_paint)
        canvas.drawRoundRect(skia.Rect(tx, -8, tx + 13, 0), 4, 4, skin_outline)

    # Muscular Calves & Knees
    # Left Leg (Knee at y = -220)
    l_leg = skia.Path()
    l_leg.moveTo(-105, -240)
    l_leg.cubicTo(-125, -140, -115, -60, -95, -15)
    l_leg.lineTo(-65, -15)
    l_leg.cubicTo(-75, -80, -80, -160, -65, -240)
    l_leg.close()
    canvas.drawPath(l_leg, skin_paint)
    canvas.drawPath(l_leg, skin_outline)

    # Right Leg
    r_leg = skia.Path()
    r_leg.moveTo(65, -240)
    r_leg.cubicTo(75, -160, 80, -80, 65, -15)
    r_leg.lineTo(95, -15)
    r_leg.cubicTo(120, -60, 125, -140, 105, -240)
    r_leg.close()
    canvas.drawPath(r_leg, skin_paint)
    canvas.drawPath(r_leg, skin_outline)

    # Rudraksha Anklets on both feet
    rudra = skia.Paint(Color=skia.ColorSetARGB(255, 75, 40, 25), AntiAlias=True)
    for bx in range(-105, -55, 10):
        canvas.drawCircle(bx, -20, 5, rudra)
    for bx in range(65, 115, 10):
        canvas.drawCircle(bx, -20, 5, rudra)

    # 3. LOWER BODY DHOTI (केसरिया धोती व कटि-वस्त्र)
    dhoti_paint = skia.Paint(
        Shader=skia.GradientShader.MakeLinear(
            [skia.Point(0, -450), skia.Point(0, -200)],
            [skia.ColorSetARGB(255, 230, 105, 25), skia.ColorSetARGB(255, 185, 70, 15)],
            [0.0, 1.0]
        ),
        AntiAlias=True
    )
    dhoti_outline = skia.Paint(Color=skia.ColorSetARGB(255, 140, 45, 10), Style=skia.Paint.kStroke_Style, StrokeWidth=3, AntiAlias=True)
    
    dhoti = skia.Path()
    dhoti.moveTo(-110, -460)
    dhoti.lineTo(110, -460)
    dhoti.lineTo(135, -250)
    dhoti.lineTo(15, -220)
    dhoti.lineTo(0, -320)
    dhoti.lineTo(-15, -220)
    dhoti.lineTo(-135, -250)
    dhoti.close()
    canvas.drawPath(dhoti, dhoti_paint)
    canvas.drawPath(dhoti, dhoti_outline)

    # Dhoti Pleats & Folds
    for px in [-80, -40, 0, 40, 80]:
        canvas.drawLine(px, -450, px * 0.7, -250, dhoti_outline)

    # Tiger Skin Kambarbandh (कमरबंद)
    tiger_band = skia.Paint(Color=skia.ColorSetARGB(255, 220, 140, 40), AntiAlias=True)
    canvas.drawRoundRect(skia.Rect(-115, -480, 115, -440), 10, 10, tiger_band)
    canvas.drawRoundRect(skia.Rect(-115, -480, 115, -440), 10, 10, skia.Paint(Color=skia.ColorBLACK, Style=skia.Paint.kStroke_Style, StrokeWidth=2.5, AntiAlias=True))
    for sx in range(-90, 100, 20):
        canvas.drawLine(sx, -475, sx + 10, -445, skia.Paint(Color=skia.ColorBLACK, StrokeWidth=3.5, AntiAlias=True))

    # 4. TORSO & CHEST (विशाल वक्षस्थल और बाहें)
    torso = skia.Path()
    torso.moveTo(-130, -720) # Left shoulder
    torso.lineTo(130, -720)  # Right shoulder
    torso.lineTo(105, -460)  # Right waist
    torso.lineTo(-105, -460) # Left waist
    torso.close()
    canvas.drawPath(torso, skin_paint)
    canvas.drawPath(torso, skin_outline)

    # Muscular Pectorals & Abdominal Definition
    pec_paint = skia.Paint(Color=skia.ColorSetARGB(90, 120, 50, 20), Style=skia.Paint.kStroke_Style, StrokeWidth=3, AntiAlias=True)
    canvas.drawArc(skia.Rect(-100, -680, -10, -600), 20, 140, False, pec_paint) # Left pec
    canvas.drawArc(skia.Rect(10, -680, 100, -600), 20, 140, False, pec_paint)  # Right pec
    # Six-pack abs
    canvas.drawLine(0, -600, 0, -480, pec_paint)
    canvas.drawLine(-45, -550, 45, -550, pec_paint)
    canvas.drawLine(-40, -510, 40, -510, pec_paint)

    # Tiger Skin Sash (बाघम्बर) diagonally across chest
    sash = skia.Path()
    sash.moveTo(-135, -720)
    sash.lineTo(-75, -725)
    sash.lineTo(110, -470)
    sash.lineTo(70, -460)
    sash.close()
    canvas.drawPath(sash, tiger_band)
    canvas.drawPath(sash, skia.Paint(Color=skia.ColorBLACK, Style=skia.Paint.kStroke_Style, StrokeWidth=2.5, AntiAlias=True))
    for sy in range(-680, -480, 30):
        canvas.drawLine(-80 + (sy+680)*0.8, sy, -40 + (sy+680)*0.8, sy + 18, skia.Paint(Color=skia.ColorBLACK, StrokeWidth=4, AntiAlias=True))

    # Double Rudraksha Mala around Neck
    for bx in range(-75, 80, 14):
        by = -700 + int(35 * math.cos(bx / 45.0))
        canvas.drawCircle(bx, by, 7.5, rudra)
        canvas.drawCircle(bx, by, 7.5, skia.Paint(Color=skia.ColorSetARGB(180, 245, 190, 50), Style=skia.Paint.kStroke_Style, StrokeWidth=1.5, AntiAlias=True))

    # 5. ARMS & HANDS (दोनों हाथ और उंगलियां)
    # Left Arm: Pointing Accusatory Finger (👉)
    # Upper arm
    l_arm1 = skia.Path()
    l_arm1.moveTo(-130, -720)
    l_arm1.lineTo(-210, -650)
    l_arm1.lineTo(-180, -620)
    l_arm1.lineTo(-115, -670)
    l_arm1.close()
    canvas.drawPath(l_arm1, skin_paint)
    canvas.drawPath(l_arm1, skin_outline)

    # Forearm extending left
    l_arm2 = skia.Path()
    l_arm2.moveTo(-210, -650)
    l_arm2.lineTo(-290, -650)
    l_arm2.lineTo(-290, -615)
    l_arm2.lineTo(-180, -620)
    l_arm2.close()
    canvas.drawPath(l_arm2, skin_paint)
    canvas.drawPath(l_arm2, skin_outline)

    # Left Hand with Pointing Index Finger
    l_hand = skia.Path()
    l_hand.moveTo(-290, -645)
    l_hand.lineTo(-345, -645) # Index finger pointing left!
    l_hand.lineTo(-345, -635)
    l_hand.lineTo(-305, -635)
    # Knuckles & curled other fingers
    l_hand.lineTo(-305, -615)
    l_hand.lineTo(-290, -615)
    l_hand.close()
    canvas.drawPath(l_hand, skin_paint)
    canvas.drawPath(l_hand, skin_outline)

    # Right Arm: Wielding the Colossal Battle Axe (Parashu)
    # Upper arm angled upward
    r_arm1 = skia.Path()
    r_arm1.moveTo(130, -720)
    r_arm1.lineTo(210, -780)
    r_arm1.lineTo(235, -750)
    r_arm1.lineTo(125, -670)
    r_arm1.close()
    canvas.drawPath(r_arm1, skin_paint)
    canvas.drawPath(r_arm1, skin_outline)

    # Forearm
    r_arm2 = skia.Path()
    r_arm2.moveTo(210, -780)
    r_arm2.lineTo(245, -870)
    r_arm2.lineTo(275, -855)
    r_arm2.lineTo(235, -750)
    r_arm2.close()
    canvas.drawPath(r_arm2, skin_paint)
    canvas.drawPath(r_arm2, skin_outline)

    # Right Hand Clenched around Axe Shaft
    r_fist = skia.Path()
    r_fist.addRoundRect(skia.Rect(235, -890, 275, -850), 8, 8)
    canvas.drawPath(r_fist, skin_paint)
    canvas.drawPath(r_fist, skin_outline)
    for fx in [242, 252, 262]:
        canvas.drawLine(fx, -885, fx, -855, skin_outline)

    # Battle Axe Shaft (Wooden handle with brass bands)
    canvas.drawLine(210, -1080, 280, -380, skia.Paint(Color=skia.ColorSetARGB(255, 90, 50, 25), StrokeWidth=18, AntiAlias=True))
    canvas.drawLine(210, -1080, 280, -380, skia.Paint(Color=skia.ColorSetARGB(255, 235, 190, 60), StrokeWidth=3, Style=skia.Paint.kStroke_Style, AntiAlias=True))

    # Colossal Steel Crescent Axe Blade (Parashu)
    blade = skia.Path()
    blade.moveTo(205, -1020)
    blade.cubicTo(320, -1110, 420, -980, 390, -840)
    blade.cubicTo(360, -740, 260, -820, 215, -870)
    blade.close()

    steel = skia.Paint(
        Shader=skia.GradientShader.MakeLinear(
            [skia.Point(205, -1020), skia.Point(400, -840)],
            [skia.ColorSetARGB(255, 245, 250, 255), skia.ColorSetARGB(255, 150, 170, 195), skia.ColorSetARGB(255, 75, 90, 110)],
            [0.0, 0.5, 1.0]
        ),
        AntiAlias=True
    )
    canvas.drawPath(blade, steel)
    canvas.drawPath(blade, skia.Paint(Color=skia.ColorWHITE, StrokeWidth=4, Style=skia.Paint.kStroke_Style, AntiAlias=True))
    # Electric Sparks on Axe
    for sx_sp, sy_sp in [(380, -960), (390, -880), (350, -800), (300, -1040)]:
        canvas.drawCircle(sx_sp, sy_sp, 5, skia.Paint(Color=skia.ColorSetARGB(255, 255, 230, 40), AntiAlias=True))
        canvas.drawCircle(sx_sp, sy_sp, 2, skia.Paint(Color=skia.ColorWHITE, AntiAlias=True))

    # 6. HEAD & ROARING FACE (मुँह, आँखें, जटाएं)
    # Wild Flying Matted Hair (जटाएं) blowing in fury
    hair_paint = skia.Paint(Color=skia.ColorSetARGB(255, 24, 18, 20), AntiAlias=True)
    for h_ang in [-65, -45, -25, 0, 25, 45, 65, -85, 85]:
        hp = skia.Path()
        hp.moveTo(0, -840)
        curl_x = 220 * math.sin(math.radians(h_ang))
        curl_y = -980 + 100 * math.cos(math.radians(h_ang))
        hp.quadTo(curl_x * 0.7, curl_y - 40, curl_x, curl_y)
        hp.quadTo(curl_x * 0.8, curl_y + 50, 0, -800)
        hp.close()
        canvas.drawPath(hp, hair_paint)

    # Face Shape
    face = skia.Path()
    face.moveTo(-50, -860)
    face.cubicTo(-60, -780, -45, -730, 0, -710)
    face.cubicTo(45, -730, 60, -780, 50, -860)
    face.close()
    canvas.drawPath(face, skin_paint)
    canvas.drawPath(face, skin_outline)

    # Ascetic Beard & Mustache
    beard_paint = skia.Paint(Color=skia.ColorSetARGB(255, 28, 22, 24), AntiAlias=True)
    beard = skia.Path()
    beard.moveTo(-52, -780)
    beard.cubicTo(-70, -700, -30, -620, 0, -600)
    beard.cubicTo(30, -620, 70, -700, 52, -780)
    beard.close()
    canvas.drawPath(beard, beard_paint)

    # Open Roaring Mouth with Teeth (मुँह - रोअरिंग एक्सप्रेशन)
    mouth = skia.Path()
    mouth.moveTo(-22, -748)
    mouth.cubicTo(-10, -756, 10, -756, 22, -748)
    mouth.cubicTo(18, -730, -18, -730, -22, -748)
    mouth.close()
    canvas.drawPath(mouth, skia.Paint(Color=skia.ColorSetARGB(255, 120, 15, 20), AntiAlias=True)) # Dark mouth cavity
    # Upper & Lower White Teeth
    canvas.drawRoundRect(skia.Rect(-16, -752, 16, -746), 2, 2, skia.Paint(Color=skia.ColorWHITE, AntiAlias=True))
    canvas.drawRoundRect(skia.Rect(-14, -736, 14, -732), 2, 2, skia.Paint(Color=skia.ColorWHITE, AntiAlias=True))

    # Sharp Warrior Nose
    canvas.drawLine(0, -810, -6, -770, skin_outline)
    canvas.drawLine(-6, -770, 0, -765, skin_outline)

    # Tripundra on Forehead (3 Sacred Ash lines)
    bhasma = skia.Paint(Color=skia.ColorSetARGB(230, 240, 245, 250), StrokeWidth=3.5, Style=skia.Paint.kStroke_Style, AntiAlias=True)
    for ty in [-835, -827, -819]:
        canvas.drawLine(-25, ty, 25, ty, bhasma)
    # Red Bindi in center
    canvas.drawCircle(0, -827, 4, skia.Paint(Color=skia.ColorSetARGB(255, 210, 20, 20), AntiAlias=True))

    # Burning Red Eyes (धधकते अंगारे)
    eye_bg = skia.Paint(Color=skia.ColorSetARGB(255, 255, 220, 220), AntiAlias=True)
    eye_pupil = skia.Paint(Color=skia.ColorSetARGB(255, 240, 30, 20), AntiAlias=True)
    for ex in [-24, 24]:
        canvas.drawOval(skia.Rect(ex - 12, -802, ex + 12, -788), eye_bg)
        canvas.drawCircle(ex, -795, 6.5, eye_pupil)
        canvas.drawCircle(ex, -795, 3, skia.Paint(Color=skia.ColorSetARGB(255, 255, 230, 100), AntiAlias=True))
        canvas.drawCircle(ex + 1, -796, 1.5, skia.Paint(Color=skia.ColorWHITE, AntiAlias=True))

    # Heavy Angled Brow Lines (Extreme Fury)
    brow = skia.Paint(Color=skia.ColorBLACK, StrokeWidth=5, Style=skia.Paint.kStroke_Style, AntiAlias=True)
    canvas.drawLine(-36, -812, -10, -800, brow)
    canvas.drawLine(36, -812, 10, -800, brow)

    canvas.restore()


def draw_full_body_laxman(canvas, cx=540, ground_y=1650, scale=1.0):
    """
    Renders Kumar Laxman as a COMPLETE FULL-BODY YOUTHFUL WARRIOR PRINCE:
    - Head & Face: Golden crown (Mukut), arched right eyebrow, defiant smirk/mouth, piercing eyes.
    - Torso & Armor: Golden cuirass, royal silk pitambara, pearl necklace.
    - Arms & Hands: Left hand resting defiantly on sword pommel, Right hand poised gracefully.
    - Legs & Feet: Yellow silk dhoti, golden anklets, feet planted in fearless posture.
    """
    canvas.save()
    canvas.translate(cx, ground_y)
    canvas.scale(scale, scale)

    # 1. Divine Radiant Serpent-Gold Halo
    halo = skia.Paint(
        Shader=skia.GradientShader.MakeRadial(
            skia.Point(0, -780), 260,
            [skia.ColorSetARGB(240, 255, 235, 140), skia.ColorSetARGB(140, 255, 195, 50), skia.ColorSetARGB(0, 255, 160, 0)],
            [0.0, 0.5, 1.0]
        ),
        AntiAlias=True
    )
    canvas.drawCircle(0, -780, 260, halo)

    # 2. FEET & LEGS (पैर और पंजे)
    skin_paint = skia.Paint(
        Shader=skia.GradientShader.MakeLinear(
            [skia.Point(0, -850), skia.Point(0, 0)],
            [skia.ColorSetARGB(255, 250, 218, 180), skia.ColorSetARGB(255, 235, 195, 150)],
            [0.0, 1.0]
        ),
        AntiAlias=True
    )
    skin_outline = skia.Paint(Color=skia.ColorSetARGB(255, 160, 110, 60), Style=skia.Paint.kStroke_Style, StrokeWidth=2.5, AntiAlias=True)

    # Golden Royal Sandals (Paduka / चरण-पादुका)
    paduka_paint = skia.Paint(Color=skia.ColorSetARGB(255, 245, 205, 60), AntiAlias=True)
    canvas.drawRoundRect(skia.Rect(-120, -12, -40, 0), 6, 6, paduka_paint)
    canvas.drawRoundRect(skia.Rect(40, -12, 120, 0), 6, 6, paduka_paint)

    # Left & Right Feet with 5 distinct toes
    for tx in range(-110, -45, 13):
        canvas.drawRoundRect(skia.Rect(tx, -20, tx + 10, -10), 3, 3, skin_paint)
        canvas.drawRoundRect(skia.Rect(tx, -20, tx + 10, -10), 3, 3, skin_outline)
    for tx in range(50, 115, 13):
        canvas.drawRoundRect(skia.Rect(tx, -20, tx + 10, -10), 3, 3, skin_paint)
        canvas.drawRoundRect(skia.Rect(tx, -20, tx + 10, -10), 3, 3, skin_outline)

    # Golden Anklets (नूपुर)
    gold_nupur = skia.Paint(Color=skia.ColorSetARGB(255, 255, 225, 75), AntiAlias=True)
    for bx in range(-100, -50, 10):
        canvas.drawCircle(bx, -28, 5, gold_nupur)
    for bx in range(55, 105, 10):
        canvas.drawCircle(bx, -28, 5, gold_nupur)

    # Muscular Fair Legs
    l_leg = skia.Path()
    l_leg.moveTo(-95, -240)
    l_leg.lineTo(-90, -35)
    l_leg.lineTo(-60, -35)
    l_leg.lineTo(-65, -240)
    l_leg.close()
    canvas.drawPath(l_leg, skin_paint)
    canvas.drawPath(l_leg, skin_outline)

    r_leg = skia.Path()
    r_leg.moveTo(65, -240)
    r_leg.lineTo(60, -35)
    r_leg.lineTo(90, -35)
    r_leg.lineTo(95, -240)
    r_leg.close()
    canvas.drawPath(r_leg, skin_paint)
    canvas.drawPath(r_leg, skin_outline)

    # 3. ROYAL SILK PITAMBARA DHOTI (पीताम्बरी धोती)
    dhoti_silk = skia.Paint(
        Shader=skia.GradientShader.MakeLinear(
            [skia.Point(0, -480), skia.Point(0, -200)],
            [skia.ColorSetARGB(255, 255, 215, 45), skia.ColorSetARGB(255, 230, 175, 20)],
            [0.0, 1.0]
        ),
        AntiAlias=True
    )
    dhoti_border = skia.Paint(Color=skia.ColorSetARGB(255, 190, 30, 35), Style=skia.Paint.kStroke_Style, StrokeWidth=4, AntiAlias=True)

    dhoti = skia.Path()
    dhoti.moveTo(-100, -480)
    dhoti.lineTo(100, -480)
    dhoti.lineTo(125, -240)
    dhoti.lineTo(15, -210)
    dhoti.lineTo(0, -300)
    dhoti.lineTo(-15, -210)
    dhoti.lineTo(-125, -240)
    dhoti.close()
    canvas.drawPath(dhoti, dhoti_silk)
    canvas.drawPath(dhoti, dhoti_border)

    # Central Pleats (काच्छा)
    canvas.drawLine(0, -480, 0, -220, dhoti_border)
    for px in [-60, -30, 30, 60]:
        canvas.drawLine(px, -475, px * 0.8, -235, skia.Paint(Color=skia.ColorSetARGB(180, 190, 140, 20), StrokeWidth=2.5, AntiAlias=True))

    # Royal Golden Waistband (स्वर्ण मेखला)
    gold_belt = skia.Paint(Color=skia.ColorSetARGB(255, 255, 225, 75), AntiAlias=True)
    canvas.drawRoundRect(skia.Rect(-105, -500, 105, -465), 8, 8, gold_belt)
    canvas.drawCircle(0, -482, 14, skia.Paint(Color=skia.ColorSetARGB(255, 220, 25, 35), AntiAlias=True)) # Ruby jewel

    # 4. TORSO & GOLDEN CUIRASS (स्वर्ण कवच वक्ष)
    torso = skia.Path()
    torso.moveTo(-115, -720)
    torso.lineTo(115, -720)
    torso.lineTo(95, -480)
    torso.lineTo(-95, -480)
    torso.close()
    canvas.drawPath(torso, skin_paint)
    canvas.drawPath(torso, skin_outline)

    # Golden Chest Armor (कवच)
    cuirass_paint = skia.Paint(
        Shader=skia.GradientShader.MakeLinear(
            [skia.Point(-100, -720), skia.Point(100, -500)],
            [skia.ColorSetARGB(255, 255, 235, 120), skia.ColorSetARGB(255, 215, 170, 50)],
            [0.0, 1.0]
        ),
        AntiAlias=True
    )
    cuirass = skia.Path()
    cuirass.moveTo(-105, -715)
    cuirass.lineTo(105, -715)
    cuirass.lineTo(85, -510)
    cuirass.lineTo(-85, -510)
    cuirass.close()
    canvas.drawPath(cuirass, cuirass_paint)
    canvas.drawPath(cuirass, skia.Paint(Color=skia.ColorSetARGB(255, 255, 245, 180), StrokeWidth=3, Style=skia.Paint.kStroke_Style, AntiAlias=True))

    # Royal Pearl Necklace (मुक्ताहार)
    pearl = skia.Paint(Color=skia.ColorSetARGB(255, 255, 255, 250), AntiAlias=True)
    for bx in range(-65, 70, 12):
        by = -700 + int(25 * math.cos(bx / 40.0))
        canvas.drawCircle(bx, by, 6, pearl)

    # 5. ARMS & HANDS (दोनों हाथ और तलवार)
    # Left Arm: Resting defiantly on sword pommel
    l_arm1 = skia.Path()
    l_arm1.moveTo(-115, -720)
    l_arm1.lineTo(-175, -630)
    l_arm1.lineTo(-145, -605)
    l_arm1.lineTo(-95, -670)
    l_arm1.close()
    canvas.drawPath(l_arm1, skin_paint)
    canvas.drawPath(l_arm1, skin_outline)

    l_arm2 = skia.Path()
    l_arm2.moveTo(-175, -630)
    l_arm2.lineTo(-125, -510)
    l_arm2.lineTo(-95, -510)
    l_arm2.lineTo(-145, -605)
    l_arm2.close()
    canvas.drawPath(l_arm2, skin_paint)
    canvas.drawPath(l_arm2, skin_outline)

    # Left Hand on Sword Pommel (हथेली और पांच उंगलियां)
    canvas.drawCircle(-110, -500, 14, skin_paint)
    for fx in range(-120, -95, 6):
        canvas.drawRoundRect(skia.Rect(fx, -505, fx + 5, -485), 2.5, 2.5, skin_paint)
        canvas.drawRoundRect(skia.Rect(fx, -505, fx + 5, -485), 2.5, 2.5, skin_outline)

    # Sheathed Royal Sword on Left Hip (खड्ग)
    # Golden pommel
    canvas.drawCircle(-110, -480, 15, gold_belt)
    canvas.drawCircle(-110, -480, 7, skia.Paint(Color=skia.ColorSetARGB(255, 25, 175, 225), AntiAlias=True)) # Cyan gem
    # Crossguard
    canvas.drawRect(skia.Rect(-135, -465, -85, -455), gold_belt)
    # Scabbard (मयान)
    scabbard = skia.Path()
    scabbard.moveTo(-118, -455)
    scabbard.lineTo(-102, -455)
    scabbard.lineTo(-70, -180)
    scabbard.lineTo(-84, -180)
    scabbard.close()
    canvas.drawPath(scabbard, skia.Paint(Color=skia.ColorSetARGB(255, 110, 25, 30), AntiAlias=True))
    canvas.drawPath(scabbard, skia.Paint(Color=skia.ColorSetARGB(255, 255, 215, 60), StrokeWidth=2.5, Style=skia.Paint.kStroke_Style, AntiAlias=True))

    # Right Arm: Poised gracefully on hip
    r_arm1 = skia.Path()
    r_arm1.moveTo(115, -720)
    r_arm1.lineTo(170, -630)
    r_arm1.lineTo(140, -605)
    r_arm1.lineTo(95, -670)
    r_arm1.close()
    canvas.drawPath(r_arm1, skin_paint)
    canvas.drawPath(r_arm1, skin_outline)

    r_arm2 = skia.Path()
    r_arm2.moveTo(170, -630)
    r_arm2.lineTo(105, -520)
    r_arm2.lineTo(80, -520)
    r_arm2.lineTo(140, -605)
    r_arm2.close()
    canvas.drawPath(r_arm2, skin_paint)
    canvas.drawPath(r_arm2, skin_outline)

    # Right Hand resting on right hip
    canvas.drawCircle(95, -510, 13, skin_paint)

    # Golden Armlets on both arms (अंगद व कंकण)
    canvas.drawRoundRect(skia.Rect(-170, -645, -140, -625), 4, 4, gold_belt)
    canvas.drawRoundRect(skia.Rect(135, -645, 165, -625), 4, 4, gold_belt)

    # 6. HEAD & EXPRESSIVE FACE WITH DEFIANT SMIRK (मुँह, आँखें, मुकुट)
    face = skia.Path()
    face.moveTo(-45, -830)
    face.cubicTo(-55, -760, -42, -700, 0, -685)
    face.cubicTo(42, -700, 55, -760, 45, -830)
    face.close()
    canvas.drawPath(face, skin_paint)
    canvas.drawPath(face, skin_outline)

    # Royal Golden Crown (मुकुट)
    crown = skia.Path()
    crown.moveTo(-52, -825)
    crown.lineTo(-32, -895)
    crown.lineTo(0, -925)
    crown.lineTo(32, -895)
    crown.lineTo(52, -825)
    crown.close()
    canvas.drawPath(crown, gold_belt)
    canvas.drawPath(crown, skia.Paint(Color=skia.ColorSetARGB(255, 255, 245, 180), StrokeWidth=3, Style=skia.Paint.kStroke_Style, AntiAlias=True))
    canvas.drawCircle(0, -875, 8, skia.Paint(Color=skia.ColorSetARGB(255, 220, 20, 30), AntiAlias=True))

    # Royal Tilak (उर्ध्वपुण्ड्र)
    canvas.drawLine(0, -810, 0, -780, skia.Paint(Color=skia.ColorSetARGB(255, 220, 25, 25), StrokeWidth=3.5, AntiAlias=True))

    # Piercing Intelligent Eyes
    eye_bg = skia.Paint(Color=skia.ColorWHITE, AntiAlias=True)
    for ex in [-20, 20]:
        canvas.drawOval(skia.Rect(ex - 10, -775, ex + 10, -762), eye_bg)
        canvas.drawCircle(ex, -768, 5, skia.Paint(Color=skia.ColorSetARGB(255, 25, 20, 25), AntiAlias=True))
        canvas.drawCircle(ex + 1.5, -770, 1.8, skia.Paint(Color=skia.ColorWHITE, AntiAlias=True))

    # Arched Defiant Eyebrows (Right eyebrow raised in confident smirk!)
    brow = skia.Paint(Color=skia.ColorSetARGB(255, 30, 25, 25), StrokeWidth=3.5, Style=skia.Paint.kStroke_Style, AntiAlias=True)
    canvas.drawLine(-30, -782, -10, -780, brow)
    canvas.drawLine(10, -780, 32, -792, brow) # Raised right eyebrow!

    # Sharp Prince Nose
    canvas.drawLine(0, -775, -5, -745, skin_outline)
    canvas.drawLine(-5, -745, 0, -740, skin_outline)

    # Defiant Amused Smirk / Mouth (मुस्कुराता हुआ मुँह)
    smirk = skia.Path()
    smirk.moveTo(-15, -720)
    smirk.quadTo(0, -716, 18, -726) # Tilted up on right cheek!
    canvas.drawPath(smirk, skia.Paint(Color=skia.ColorSetARGB(255, 195, 50, 55), StrokeWidth=3.5, Style=skia.Paint.kStroke_Style, AntiAlias=True))

    canvas.restore()

# Render test frames
p_parashu = "scratch/test_full_body_parashurama.png"
p_laxman = "scratch/test_full_body_laxman.png"

surf1 = skia.Surface(W, H)
draw_full_body_parashurama(surf1.getCanvas(), cx=540, ground_y=1650, scale=1.0)
surf1.makeImageSnapshot().save(p_parashu, skia.kPNG)

surf2 = skia.Surface(W, H)
draw_full_body_laxman(surf2.getCanvas(), cx=540, ground_y=1650, scale=1.0)
surf2.makeImageSnapshot().save(p_laxman, skia.kPNG)

print("Saved full-body character test renders!")
