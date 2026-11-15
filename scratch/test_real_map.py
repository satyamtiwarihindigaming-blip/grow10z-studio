import json
import math
import skia

W, H = 1080, 1920

# Load true India boundary points
with open('studio_ramayana/episodes/ep006/india_map_pts.json', 'r') as f:
    india_pts = json.load(f)

def geo_to_screen(lon, lat):
    # Mapping Lon [67.0, 98.0] and Lat [6.5, 38.0] to canvas
    # Let map fit in W=1080, H=1920
    # X: 70 to 1010 (width 940)
    # Y: 320 to 1580 (height 1260)
    sx = 70 + (lon - 67.0) / (98.0 - 67.0) * 940
    sy = 1580 - (lat - 6.5) / (38.0 - 6.5) * 1260
    return sx, sy

def draw_real_india_map(canvas, W=1080, H=1920):
    # 1. Background Ocean
    ocean_paint = skia.Paint(
        Shader=skia.GradientShader.MakeLinear(
            [skia.Point(0, 0), skia.Point(W, H)],
            [skia.ColorSetARGB(255, 12, 22, 38), skia.ColorSetARGB(255, 8, 14, 24)],
            [0.0, 1.0]
        )
    )
    canvas.drawRect(skia.Rect(0, 0, W, H), ocean_paint)

    # Subtle cartographic latitude/longitude lines
    coord_paint = skia.Paint(Color=skia.ColorSetARGB(35, 100, 150, 200), Style=skia.Paint.kStroke_Style, StrokeWidth=1, AntiAlias=True)
    for gy in range(200, H, 140):
        canvas.drawLine(0, gy, W, gy, coord_paint)
    for gx in range(100, W, 140):
        canvas.drawLine(gx, 0, gx, H, coord_paint)

    # 2. India Landmass Path from True Geographic Points
    india_path = skia.Path()
    start_x, start_y = geo_to_screen(india_pts[0][0], india_pts[0][1])
    india_path.moveTo(start_x, start_y)
    for p in india_pts[1:]:
        px, py = geo_to_screen(p[0], p[1])
        india_path.lineTo(px, py)
    india_path.close()

    # Landmass Drop Shadow & Outer Glow
    land_shadow = skia.Paint(Color=skia.ColorSetARGB(180, 0, 0, 0), AntiAlias=True, ImageFilter=skia.ImageFilters.Blur(15, 15))
    canvas.drawPath(india_path, land_shadow)

    # Landmass Fill (Rich Antique Emerald & Terracotta Gradient)
    land_fill = skia.Paint(
        Shader=skia.GradientShader.MakeLinear(
            [skia.Point(200, 320), skia.Point(700, 1580)],
            [skia.ColorSetARGB(255, 28, 48, 55), skia.ColorSetARGB(255, 22, 38, 44), skia.ColorSetARGB(255, 32, 45, 40)],
            [0.0, 0.5, 1.0]
        ),
        AntiAlias=True
    )
    canvas.drawPath(india_path, land_fill)

    # Landmass Golden Contour Border
    border_paint = skia.Paint(Color=skia.ColorSetARGB(255, 215, 175, 75), Style=skia.Paint.kStroke_Style, StrokeWidth=3.5, AntiAlias=True)
    canvas.drawPath(india_path, border_paint)

    # Coastline Glow
    coast_glow = skia.Paint(Color=skia.ColorSetARGB(90, 120, 210, 255), Style=skia.Paint.kStroke_Style, StrokeWidth=8, AntiAlias=True)
    canvas.drawPath(india_path, coast_glow)

    # 3. Coordinates for Sacred Locations
    # Mithila: Lon 85.9, Lat 26.7
    mx, my = geo_to_screen(85.9, 26.7)
    # Mahendra Parvat: Lon 84.3, Lat 18.9
    px, py = geo_to_screen(84.3, 18.9)
    # Ayodhya: Lon 82.2, Lat 26.8
    ax, ay = geo_to_screen(82.2, 26.8)

    # 4. Red Seismic Shockwave Arc (Mithila to Mahendra)
    arc_path = skia.Path()
    arc_path.moveTo(mx, my)
    # Arc bowing slightly outward to sea
    mid_x, mid_y = (mx + px)/2 + 65, (my + py)/2
    arc_path.quadTo(mid_x, mid_y, px, py)

    # Outer shockwave red beam
    canvas.drawPath(arc_path, skia.Paint(Color=skia.ColorSetARGB(200, 255, 45, 40), Style=skia.Paint.kStroke_Style, StrokeWidth=8, AntiAlias=True))
    canvas.drawPath(arc_path, skia.Paint(Color=skia.ColorSetARGB(255, 255, 240, 150), Style=skia.Paint.kStroke_Style, StrokeWidth=3, AntiAlias=True))

    # Shockwave Rings from Mithila
    for r in [35, 75, 130, 200]:
        canvas.drawCircle(mx, my, r, skia.Paint(Color=skia.ColorSetARGB(max(0, 220 - int(r*0.9)), 255, 80, 50), Style=skia.Paint.kStroke_Style, StrokeWidth=2.5, AntiAlias=True))

    # Target Radar Ping at Mount Mahendra
    for pr in [25, 55, 95]:
        canvas.drawCircle(px, py, pr, skia.Paint(Color=skia.ColorSetARGB(max(0, 240 - int(pr*2.2)), 255, 215, 0), Style=skia.Paint.kStroke_Style, StrokeWidth=3, AntiAlias=True))
    canvas.drawCircle(px, py, 12, skia.Paint(Color=skia.ColorSetARGB(255, 255, 60, 40), AntiAlias=True))
    canvas.drawCircle(px, py, 5, skia.Paint(Color=skia.ColorWHITE, AntiAlias=True))

    # 5. Pop-Up Cards with Text Labels
    # Card 1: Mithila Pop-Up Card
    draw_popup_card(canvas, mx, my, "Mithila (Mithila)", "Shiva Dhanush Bhang Sthal", is_origin=True)

    # Card 2: Mount Mahendra Pop-Up Card
    draw_popup_card(canvas, px, py, "Mt. Mahendra (Mahendra)", "Tapobhumi of Parashurama", is_origin=False)

    # Card 3: Distance Callout Badge along Arc
    draw_distance_badge(canvas, mid_x + 30, mid_y - 20, "3,000 KM Seismic Shockwave")

    # Compass Rose at bottom left
    draw_compass_rose(canvas, 200, 1680)

def draw_popup_card(canvas, pin_x, pin_y, title, subtitle, is_origin=True):
    # Pin marker
    pin_col = skia.ColorSetARGB(255, 255, 215, 0) if is_origin else skia.ColorSetARGB(255, 255, 75, 55)
    canvas.drawCircle(pin_x, pin_y, 14, skia.Paint(Color=pin_col, AntiAlias=True))
    canvas.drawCircle(pin_x, pin_y, 6, skia.Paint(Color=skia.ColorWHITE, AntiAlias=True))

    # Leader line from pin to card
    card_x = pin_x - 340 if is_origin else pin_x + 60
    card_y = pin_y - 120 if is_origin else pin_y + 40
    card_w, card_h = 380, 95

    leader = skia.Path()
    leader.moveTo(pin_x, pin_y)
    leader.lineTo(card_x + (card_w if is_origin else 0), card_y + card_h/2)
    canvas.drawPath(leader, skia.Paint(Color=pin_col, Style=skia.Paint.kStroke_Style, StrokeWidth=2.5, AntiAlias=True))

    # Card Background with Drop Shadow
    shadow = skia.Paint(Color=skia.ColorSetARGB(180, 0, 0, 0), AntiAlias=True, ImageFilter=skia.ImageFilters.Blur(10, 10))
    canvas.drawRoundRect(skia.Rect(card_x, card_y, card_x + card_w, card_y + card_h), 12, 12, shadow)

    card_bg = skia.Paint(Color=skia.ColorSetARGB(245, 18, 26, 40), AntiAlias=True)
    canvas.drawRoundRect(skia.Rect(card_x, card_y, card_x + card_w, card_y + card_h), 12, 12, card_bg)

    border = skia.Paint(Color=pin_col, Style=skia.Paint.kStroke_Style, StrokeWidth=2.5, AntiAlias=True)
    canvas.drawRoundRect(skia.Rect(card_x, card_y, card_x + card_w, card_y + card_h), 12, 12, border)

    # Accent Header Bar
    canvas.drawRoundRect(skia.Rect(card_x + 8, card_y + 8, card_x + 16, card_y + card_h - 8), 4, 4, skia.Paint(Color=pin_col, AntiAlias=True))

    # Text via Skia Font
    font_title = skia.Font(skia.Typeface('Segoe UI', skia.FontStyle.Bold()), 23)
    canvas.drawString(title, card_x + 28, card_y + 40, font_title, skia.Paint(Color=skia.ColorWHITE, AntiAlias=True))

    font_sub = skia.Font(skia.Typeface('Segoe UI', skia.FontStyle.Normal()), 16)
    canvas.drawString(subtitle, card_x + 28, card_y + 75, font_sub, skia.Paint(Color=skia.ColorSetARGB(220, 200, 220, 240), AntiAlias=True))

def draw_distance_badge(canvas, bx, by, text):
    bw, bh = 300, 52
    canvas.drawRoundRect(skia.Rect(bx, by, bx + bw, by + bh), 26, 26, skia.Paint(Color=skia.ColorSetARGB(240, 220, 35, 30), AntiAlias=True))
    canvas.drawRoundRect(skia.Rect(bx, by, bx + bw, by + bh), 26, 26, skia.Paint(Color=skia.ColorSetARGB(255, 255, 230, 150), Style=skia.Paint.kStroke_Style, StrokeWidth=2, AntiAlias=True))

    font = skia.Font(skia.Typeface('Segoe UI', skia.FontStyle.Bold()), 18)
    canvas.drawString(text, bx + 22, by + 34, font, skia.Paint(Color=skia.ColorWHITE, AntiAlias=True))

def draw_compass_rose(canvas, cx, cy):
    canvas.drawCircle(cx, cy, 65, skia.Paint(Color=skia.ColorSetARGB(60, 215, 175, 75), Style=skia.Paint.kStroke_Style, StrokeWidth=2, AntiAlias=True))
    canvas.drawCircle(cx, cy, 45, skia.Paint(Color=skia.ColorSetARGB(40, 215, 175, 75), Style=skia.Paint.kStroke_Style, StrokeWidth=1.5, AntiAlias=True))

    gold = skia.Paint(Color=skia.ColorSetARGB(255, 245, 200, 75), AntiAlias=True)
    dark_gold = skia.Paint(Color=skia.ColorSetARGB(255, 160, 120, 35), AntiAlias=True)

    np = skia.Path()
    np.moveTo(cx, cy - 85)
    np.lineTo(cx - 12, cy)
    np.lineTo(cx, cy)
    np.close()
    canvas.drawPath(np, gold)
    np2 = skia.Path()
    np2.moveTo(cx, cy - 85)
    np2.lineTo(cx + 12, cy)
    np2.lineTo(cx, cy)
    np2.close()
    canvas.drawPath(np2, dark_gold)

    sp = skia.Path()
    sp.moveTo(cx, cy + 65)
    sp.lineTo(cx - 10, cy)
    sp.lineTo(cx, cy)
    sp.close()
    canvas.drawPath(sp, dark_gold)
    sp2 = skia.Path()
    sp2.moveTo(cx, cy + 65)
    sp2.lineTo(cx + 10, cy)
    sp2.lineTo(cx, cy)
    sp2.close()
    canvas.drawPath(sp2, gold)

    for sign, l in [(-1, 65), (1, 65)]:
        p = skia.Path()
        p.moveTo(cx + sign*l, cy)
        p.lineTo(cx, cy - 10)
        p.lineTo(cx, cy)
        p.close()
        canvas.drawPath(p, gold if sign > 0 else dark_gold)

    font = skia.Font(skia.Typeface('Segoe UI', skia.FontStyle.Bold()), 22)
    canvas.drawString("N (North)", cx - 35, cy - 95, font, gold)

# Test Render
surf = skia.Surface(W, H)
draw_real_india_map(surf.getCanvas())
surf.makeImageSnapshot().save("scratch/test_real_india_map.png", skia.kPNG)
print("Saved scratch/test_real_india_map.png")
