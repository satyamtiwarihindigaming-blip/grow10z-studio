import math
import skia

def draw_baal_ram(cv, cx, cy, scale=1.0, rock_angle=0.0):
    """
    Detailed, sacred 3D-styled Baal Ram character with:
    - Glowing divine halo (तेजपुंज) with ray flare
    - Neel-Shyam soft radiant skin with facial highlights
    - Lotus eyes (विशाल कमल नयन) with bright reflections
    - Tilak (चन्दन व कुमकुम तिलक)
    - Golden Mukut (मुकुट) with Peacock Feather (मोरपंख)
    - Pearl necklace (मुक्ताहार) + Golden Kundal (कुंडल)
    - Silk Pitambari swaddle
    """
    cv.save()
    cv.translate(cx, cy)
    cv.scale(scale, scale)
    cv.rotate(rock_angle)
    
    # 1. Divine Outer Aura (स्वर्ण तेजपुंज)
    halo_paint = skia.Paint(
        Shader=skia.GradientShader.MakeRadial(
            (0, -20), 180,
            [skia.ColorSetARGB(220, 255, 240, 150), skia.ColorSetARGB(120, 255, 190, 40), skia.ColorSetARGB(0, 255, 180, 0)],
            [0.0, 0.5, 1.0]
        ),
        AntiAlias=True
    )
    cv.drawCircle(0, -20, 180, halo_paint)
    
    # 2. Golden Cradle Bedding
    cradle_p = skia.Path()
    cradle_p.addRoundRect(skia.Rect(-160, 40, 160, 180), 30, 30)
    cv.drawPath(cradle_p, skia.Paint(Color=skia.ColorSetARGB(255, 240, 215, 60), AntiAlias=True))
    cv.drawPath(cradle_p, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=8, Color=skia.ColorSetARGB(255, 180, 130, 20), AntiAlias=True))
    
    # Silk Velvet Cushion
    cushion_p = skia.Path()
    cushion_p.addRoundRect(skia.Rect(-140, 55, 140, 160), 20, 20)
    cv.drawPath(cushion_p, skia.Paint(Color=skia.ColorSetARGB(255, 175, 25, 45), AntiAlias=True))
    
    # 3. Baal Ram Head (Neel-Shyam Divine Hue)
    C_SKIN = skia.ColorSetARGB(255, 52, 98, 175)
    C_SKIN_HIGHLIGHT = skia.ColorSetARGB(255, 85, 145, 235)
    
    # Head Base
    cv.drawCircle(0, -20, 68, skia.Paint(Color=C_SKIN, AntiAlias=True))
    # Soft 3D Lighting Highlight on forehead and cheek
    hl_paint = skia.Paint(
        Shader=skia.GradientShader.MakeRadial(
            (-15, -35), 45,
            [skia.ColorSetARGB(140, 120, 185, 255), skia.ColorSetARGB(0, 52, 98, 175)],
            [0.0, 1.0]
        ),
        AntiAlias=True
    )
    cv.drawCircle(-15, -35, 45, hl_paint)
    
    # 4. Lotus Eyes (विशाल कमल नयन)
    for side in [-1, 1]:
        ex = side * 24
        ey = -18
        # Eye white sclera
        eye_p = skia.Path()
        eye_p.moveTo(ex - 16, ey)
        eye_p.quadTo(ex, ey - 10, ex + 16, ey)
        eye_p.quadTo(ex, ey + 10, ex - 16, ey)
        cv.drawPath(eye_p, skia.Paint(Color=skia.ColorWHITE, AntiAlias=True))
        
        # Deep black iris
        cv.drawCircle(ex, ey, 7, skia.Paint(Color=skia.ColorSetARGB(255, 15, 18, 25), AntiAlias=True))
        # Shiny white light reflection
        cv.drawCircle(ex - 2, ey - 2, 2.5, skia.Paint(Color=skia.ColorWHITE, AntiAlias=True))
        # Eyelash line
        cv.drawPath(eye_p, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=2.5, Color=skia.ColorSetARGB(255, 10, 12, 18), AntiAlias=True))
        
        # Golden Kundal (कुंडल / Earring)
        kx = side * 72
        ky = -12
        cv.drawCircle(kx, ky, 10, skia.Paint(Color=skia.ColorSetARGB(255, 255, 215, 0), AntiAlias=True))
        cv.drawCircle(kx, ky + 12, 7, skia.Paint(Color=skia.ColorSetARGB(255, 255, 240, 120), AntiAlias=True))

    # 5. Sacred Chandan-Kumkum Tilak (तिलक)
    t_path = skia.Path()
    # U-shaped Chandan
    t_path.moveTo(-8, -48)
    t_path.lineTo(-8, -32)
    t_path.quadTo(0, -26, 8, -32)
    t_path.lineTo(8, -48)
    cv.drawPath(t_path, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=3.5, Color=skia.ColorSetARGB(255, 255, 250, 220), AntiAlias=True))
    # Red Kumkum line in center
    cv.drawLine(0, -48, 0, -28, skia.Paint(StrokeWidth=3, Color=skia.ColorSetARGB(255, 220, 25, 35), AntiAlias=True))

    # 6. Gentle Divine Smile (मंद मुस्कान)
    smile_p = skia.Path()
    smile_p.moveTo(-12, 6)
    smile_p.quadTo(0, 18, 12, 6)
    cv.drawPath(smile_p, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=3.5, Color=skia.ColorSetARGB(255, 190, 45, 60), AntiAlias=True))

    # 7. Golden Mukut with Peacock Feather (स्वर्ण मुकुट व मोरपंख)
    mukut_p = skia.Path()
    mukut_p.moveTo(-52, -55)
    mukut_p.lineTo(0, -115)
    mukut_p.lineTo(52, -55)
    mukut_p.close()
    cv.drawPath(mukut_p, skia.Paint(Color=skia.ColorSetARGB(255, 255, 205, 30), AntiAlias=True))
    cv.drawPath(mukut_p, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=4, Color=skia.ColorSetARGB(255, 190, 140, 10), AntiAlias=True))
    
    # Red Ruby Jewel in center of Mukut
    cv.drawCircle(0, -75, 7, skia.Paint(Color=skia.ColorSetARGB(255, 220, 15, 30), AntiAlias=True))

    # Peacock Feather Crest (मोरपंख)
    cv.drawOval(skia.Rect(-12, -165, 12, -115), skia.Paint(Color=skia.ColorSetARGB(255, 15, 130, 95), AntiAlias=True))
    cv.drawOval(skia.Rect(-7, -155, 7, -125), skia.Paint(Color=skia.ColorSetARGB(255, 20, 75, 165), AntiAlias=True))
    cv.drawCircle(0, -140, 4, skia.Paint(Color=skia.ColorSetARGB(255, 255, 215, 0), AntiAlias=True))

    # 8. Pearl Necklace (मुक्ताहार)
    for p_ang in range(-50, 60, 15):
        prad = math.radians(p_ang)
        cv.drawCircle(32 * math.sin(prad), 26 + 18 * math.cos(prad), 4.5, skia.Paint(Color=skia.ColorSetARGB(255, 250, 250, 245), AntiAlias=True))

    # 9. Yellow Silk Pitambari Swaddle Cloth (पीताम्बरी)
    swaddle_p = skia.Path()
    swaddle_p.addRoundRect(skia.Rect(-60, 42, 60, 130), 22, 22)
    cv.drawPath(swaddle_p, skia.Paint(Color=skia.ColorSetARGB(255, 255, 185, 15), AntiAlias=True))
    cv.drawPath(swaddle_p, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=5, Color=skia.ColorSetARGB(255, 210, 145, 5), AntiAlias=True))

    cv.restore()

def draw_maharaja_dasharatha(cv, cx, cy, scale=1.0):
    """
    Detailed, dignified Maharaja Dasharatha:
    - Regal facial profile with sharp royal features and graying beard
    - Grand imperial Sun-dynasty golden crown (रत्नजड़ित राजमुकुट)
    - Royal silk angavastram & crimson robes
    - Multi-strand pearl & emerald royal necklace (हार)
    - Hands folded in divine prayer (करबद्ध प्रणाम)
    """
    cv.save()
    cv.translate(cx, cy)
    cv.scale(scale, scale)
    
    # 1. Royal Crown (विशाल राजमुकुट)
    cr_p = skia.Path()
    cr_p.moveTo(-45, -100)
    cr_p.lineTo(-15, -170)
    cr_p.lineTo(0, -185)
    cr_p.lineTo(15, -170)
    cr_p.lineTo(45, -100)
    cr_p.close()
    cv.drawPath(cr_p, skia.Paint(Color=skia.ColorSetARGB(255, 255, 215, 20), AntiAlias=True))
    cv.drawPath(cr_p, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=5, Color=skia.ColorSetARGB(255, 180, 130, 10), AntiAlias=True))
    # Emeralds on Crown
    for gem_x in [-25, 0, 25]:
        cv.drawCircle(gem_x, -125, 6, skia.Paint(Color=skia.ColorSetARGB(255, 25, 150, 75), AntiAlias=True))
        
    # 2. King's Head
    cv.drawCircle(0, -55, 50, skia.Paint(Color=skia.ColorSetARGB(255, 215, 168, 125), AntiAlias=True))
    
    # Eyes filled with devotion and joy
    cv.drawOval(skia.Rect(10, -65, 32, -50), skia.Paint(Color=skia.ColorWHITE, AntiAlias=True))
    cv.drawCircle(22, -58, 5, skia.Paint(Color=skia.ColorSetARGB(255, 20, 24, 30), AntiAlias=True))
    cv.drawCircle(20, -60, 2, skia.Paint(Color=skia.ColorWHITE, AntiAlias=True))
    
    # Royal Moustache & Beard (राजसी दाढ़ी-मूँछ)
    beard_p = skia.Path()
    beard_p.moveTo(-35, -45)
    beard_p.lineTo(25, -45)
    beard_p.lineTo(35, -20)
    beard_p.lineTo(-10, -5)
    beard_p.close()
    cv.drawPath(beard_p, skia.Paint(Color=skia.ColorSetARGB(255, 60, 50, 55), AntiAlias=True))

    # Royal Golden Kundal
    cv.drawCircle(-40, -45, 10, skia.Paint(Color=skia.ColorSetARGB(255, 255, 215, 0), AntiAlias=True))

    # 3. Imperial Royal Robe (राजसी उत्तरीय)
    robe_p = skia.Path()
    robe_p.addRoundRect(skia.Rect(-80, 0, 80, 360), 30, 30)
    cv.drawPath(robe_p, skia.Paint(Color=skia.ColorSetARGB(255, 155, 22, 38), AntiAlias=True))
    cv.drawPath(robe_p, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=8, Color=skia.ColorSetARGB(255, 255, 215, 0), AntiAlias=True))

    # Folded Hands in Prayer (करबद्ध हाथ)
    hands_p = skia.Path()
    hands_p.moveTo(15, 60)
    hands_p.lineTo(55, 40)
    hands_p.lineTo(75, 75)
    hands_p.lineTo(35, 95)
    hands_p.close()
    cv.drawPath(hands_p, skia.Paint(Color=skia.ColorSetARGB(255, 215, 168, 125), AntiAlias=True))
    cv.drawPath(hands_p, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=3, Color=skia.ColorSetARGB(255, 170, 120, 80), AntiAlias=True))

    # Royal Multi-Strand Garland
    cv.drawOval(skia.Rect(-50, 10, 50, 120), skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=10, Color=skia.ColorSetARGB(255, 255, 230, 80), AntiAlias=True))

    cv.restore()


def draw_shri_ram_warrior(cv, cx, cy, scale=1.0, pose_t=0.0):
    """
    Shri Ram as Young Warrior:
    - Glowing celestial radiance (तेजपुंज)
    - Neel-Shyam complexioned youth with lotus eyes and chandan tilak
    - Royal Golden Mukut with peacock motif
    - Royal Golden Bow (कोदण्ड धनुष) with quiver and arrows
    - Pitambari dhoti and angavastra with golden embroidery
    """
    cv.save()
    cv.translate(cx, cy)
    cv.scale(scale, scale)

    # 1. Divine Aura
    aura_paint = skia.Paint(
        Shader=skia.GradientShader.MakeRadial(
            skia.Point(0, -60), 220,
            [skia.ColorSetARGB(200, 255, 235, 140), skia.ColorSetARGB(80, 255, 180, 40), skia.ColorSetARGB(0, 255, 180, 0)],
            [0.0, 0.6, 1.0]
        ),
        AntiAlias=True
    )
    cv.drawCircle(0, -60, 220, aura_paint)

    # 2. Golden Bow (Kodanda Dhanush) behind back
    bow_p = skia.Path()
    bow_p.moveTo(90, -180)
    bow_p.quadTo(150, 40, 80, 260)
    cv.drawPath(bow_p, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=14, Color=skia.ColorSetARGB(255, 230, 180, 30), AntiAlias=True))
    cv.drawPath(bow_p, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=6, Color=skia.ColorSetARGB(255, 255, 245, 180), AntiAlias=True))
    # Bow string
    cv.drawLine(90, -180, 80, 260, skia.Paint(StrokeWidth=2, Color=skia.ColorWHITE, AntiAlias=True))

    # 3. Body & Pitambari
    torso_p = skia.Path()
    torso_p.moveTo(-70, 20)
    torso_p.lineTo(70, 20)
    torso_p.lineTo(55, 200)
    torso_p.lineTo(-55, 200)
    torso_p.close()
    cv.drawPath(torso_p, skia.Paint(Color=skia.ColorSetARGB(255, 245, 175, 25), AntiAlias=True))
    cv.drawPath(torso_p, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=6, Color=skia.ColorSetARGB(255, 200, 130, 15), AntiAlias=True))

    # Golden Armor / Kavach & Pearl Garland
    cv.drawOval(skia.Rect(-45, 30, 45, 140), skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=8, Color=skia.ColorSetARGB(255, 255, 220, 60), AntiAlias=True))

    # 4. Neel-Shyam Neck & Face
    cv.drawRect(skia.Rect(-20, -10, 20, 25), skia.Paint(Color=skia.ColorSetARGB(255, 52, 98, 175), AntiAlias=True))
    cv.drawCircle(0, -60, 52, skia.Paint(Color=skia.ColorSetARGB(255, 52, 98, 175), AntiAlias=True))
    
    # Lotus Eyes & Gentle Divine Smile
    for s in [-1, 1]:
        cv.drawOval(skia.Rect(s*14 - 10, -70, s*14 + 10, -56), skia.Paint(Color=skia.ColorWHITE, AntiAlias=True))
        cv.drawCircle(s*14, -63, 5, skia.Paint(Color=skia.ColorSetARGB(255, 20, 25, 35), AntiAlias=True))
        cv.drawCircle(s*14 - 2, -65, 2, skia.Paint(Color=skia.ColorWHITE, AntiAlias=True))
    
    # Chandan & Kumkum Tilak
    tilak_p = skia.Path()
    tilak_p.moveTo(-8, -95)
    tilak_p.quadTo(0, -65, 8, -95)
    cv.drawPath(tilak_p, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=4, Color=skia.ColorSetARGB(255, 255, 245, 210), AntiAlias=True))
    cv.drawCircle(0, -82, 3, skia.Paint(Color=skia.ColorSetARGB(255, 215, 30, 30), AntiAlias=True))

    # 5. Golden Mukut with Peacock Feather
    mukut_p = skia.Path()
    mukut_p.moveTo(-45, -95)
    mukut_p.lineTo(0, -175)
    mukut_p.lineTo(45, -95)
    mukut_p.close()
    cv.drawPath(mukut_p, skia.Paint(Color=skia.ColorSetARGB(255, 255, 215, 0), AntiAlias=True))
    cv.drawPath(mukut_p, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=4, Color=skia.ColorSetARGB(255, 180, 130, 10), AntiAlias=True))
    # Peacock Feather on Top
    cv.drawOval(skia.Rect(-12, -210, 12, -170), skia.Paint(Color=skia.ColorSetARGB(255, 20, 140, 80), AntiAlias=True))
    cv.drawCircle(0, -190, 6, skia.Paint(Color=skia.ColorSetARGB(255, 30, 80, 200), AntiAlias=True))

    cv.restore()


def draw_maharishi_vishwamitra(cv, cx, cy, scale=1.0):
    """
    Maharishi Vishwamitra:
    - Tapasya tejas (radiance of penance)
    - Flowing white sage beard and jata (matted locks)
    - Saffron utpata robe and Rudraksha malas
    - Raised hand with blessing (अभय मुद्रा)
    """
    cv.save()
    cv.translate(cx, cy)
    cv.scale(scale, scale)

    # 1. Tapasya Aura
    cv.drawCircle(0, -70, 190, skia.Paint(
        Shader=skia.GradientShader.MakeRadial(
            skia.Point(0, -70), 190,
            [skia.ColorSetARGB(180, 255, 200, 100), skia.ColorSetARGB(60, 255, 140, 30), skia.ColorSetARGB(0, 255, 100, 0)],
            [0.0, 0.5, 1.0]
        ),
        AntiAlias=True
    ))

    # 2. Saffron Ascetic Robe
    robe = skia.Path()
    robe.moveTo(-75, 10)
    robe.lineTo(75, 10)
    robe.lineTo(60, 220)
    robe.lineTo(-60, 220)
    robe.close()
    cv.drawPath(robe, skia.Paint(Color=skia.ColorSetARGB(255, 225, 105, 25), AntiAlias=True))

    # 3. Rudraksha Mala
    cv.drawOval(skia.Rect(-40, 20, 40, 110), skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=8, Color=skia.ColorSetARGB(255, 90, 45, 20), AntiAlias=True))

    # 4. Sage Head & Jata (Ascetic Locks)
    cv.drawCircle(0, -65, 48, skia.Paint(Color=skia.ColorSetARGB(255, 210, 160, 120), AntiAlias=True))
    # Jatamukut
    cv.drawOval(skia.Rect(-35, -135, 35, -90), skia.Paint(Color=skia.ColorSetARGB(255, 70, 45, 30), AntiAlias=True))

    # Eyes & Tripund Tilak
    for s in [-1, 1]:
        cv.drawOval(skia.Rect(s*14 - 8, -75, s*14 + 8, -63), skia.Paint(Color=skia.ColorWHITE, AntiAlias=True))
        cv.drawCircle(s*14, -69, 4, skia.Paint(Color=skia.ColorSetARGB(255, 25, 20, 20), AntiAlias=True))
    # Tripund
    cv.drawLine(-18, -88, 18, -88, skia.Paint(StrokeWidth=3, Color=skia.ColorWHITE, AntiAlias=True))
    cv.drawLine(-18, -92, 18, -92, skia.Paint(StrokeWidth=3, Color=skia.ColorWHITE, AntiAlias=True))
    cv.drawCircle(0, -90, 3, skia.Paint(Color=skia.ColorSetARGB(255, 200, 30, 30), AntiAlias=True))

    # 5. Grand White Beard (तपस्वी श्वेत दाढ़ी)
    beard = skia.Path()
    beard.moveTo(-35, -50)
    beard.lineTo(35, -50)
    beard.lineTo(20, 45)
    beard.lineTo(0, 75)
    beard.lineTo(-20, 45)
    beard.close()
    cv.drawPath(beard, skia.Paint(Color=skia.ColorSetARGB(255, 245, 245, 245), AntiAlias=True))
    cv.drawPath(beard, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=3, Color=skia.ColorSetARGB(255, 200, 200, 200), AntiAlias=True))

    cv.restore()


def draw_tadaka(cv, cx, cy, scale=1.0):
    """
    Demoness Tadaka:
    - Dark volcanic demonic storm aura
    - Clawed silhouette with fiery glowing red eyes and fangs
    - Thorny bone jewelry and terrifying presence
    """
    cv.save()
    cv.translate(cx, cy)
    cv.scale(scale, scale)

    # 1. Dark Fiery Aura
    cv.drawCircle(0, -60, 240, skia.Paint(
        Shader=skia.GradientShader.MakeRadial(
            skia.Point(0, -60), 240,
            [skia.ColorSetARGB(180, 180, 20, 20), skia.ColorSetARGB(100, 30, 5, 5), skia.ColorSetARGB(0, 0, 0, 0)],
            [0.0, 0.6, 1.0]
        ),
        AntiAlias=True
    ))

    # 2. Dark Monstrous Body
    body = skia.Path()
    body.moveTo(-90, 20)
    body.lineTo(90, 20)
    body.lineTo(110, 240)
    body.lineTo(-110, 240)
    body.close()
    cv.drawPath(body, skia.Paint(Color=skia.ColorSetARGB(255, 35, 30, 40), AntiAlias=True))

    # 3. Terrifying Head
    cv.drawCircle(0, -60, 65, skia.Paint(Color=skia.ColorSetARGB(255, 45, 38, 52), AntiAlias=True))

    # Fiery Glowing Eyes
    for s in [-1, 1]:
        cv.drawOval(skia.Rect(s*18 - 14, -75, s*18 + 14, -55), skia.Paint(Color=skia.ColorSetARGB(255, 255, 40, 20), AntiAlias=True))
        cv.drawCircle(s*18, -65, 5, skia.Paint(Color=skia.ColorSetARGB(255, 255, 240, 50), AntiAlias=True))

    # Sharp Fangs
    cv.drawPath(skia.Path().moveTo(-15, -35).lineTo(-10, -20).lineTo(-5, -35), skia.Paint(Color=skia.ColorWHITE, AntiAlias=True))
    cv.drawPath(skia.Path().moveTo(5, -35).lineTo(10, -20).lineTo(15, -35), skia.Paint(Color=skia.ColorWHITE, AntiAlias=True))

    # Disheveled Wild Hair
    hair = skia.Path()
    hair.moveTo(-70, -60)
    hair.lineTo(-120, -110)
    hair.lineTo(-40, -120)
    hair.lineTo(0, -150)
    hair.lineTo(40, -120)
    hair.lineTo(120, -110)
    hair.lineTo(70, -60)
    hair.close()
    cv.drawPath(hair, skia.Paint(Color=skia.ColorSetARGB(255, 20, 15, 25), AntiAlias=True))

    cv.restore()
