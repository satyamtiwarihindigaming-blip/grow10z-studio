import skia
import numpy as np

# 1024x1024 High-res Profile Picture / Logo
W, H = 1024, 1024
surf = skia.Surface(W, H)
canvas = surf.getCanvas()

# 1. Dark Cinematic Gradient Background
grad_shader = skia.GradientShader.MakeRadial(
    (W / 2, H / 2), 650,
    [skia.Color(18, 22, 38), skia.Color(8, 9, 16), skia.Color(3, 4, 8)],
    [0.0, 0.65, 1.0]
)
bg_paint = skia.Paint(Shader=grad_shader)
canvas.drawRect(skia.Rect(0, 0, W, H), bg_paint)

# 2. Glowing Outer Rings (Neon Cyan & Electric Blue)
ring_paint = skia.Paint(
    Style=skia.Paint.kStroke_Style,
    StrokeWidth=12,
    AntiAlias=True,
    Color=skia.Color(0, 225, 255, 220),
    MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 6)
)
canvas.drawCircle(W / 2, H / 2, 460, ring_paint)

ring_core = skia.Paint(
    Style=skia.Paint.kStroke_Style,
    StrokeWidth=5,
    AntiAlias=True,
    Color=skia.Color(255, 255, 255, 255)
)
canvas.drawCircle(W / 2, H / 2, 460, ring_core)

# Inner Neon Amber / Gold Glow Ring
ring_inner = skia.Paint(
    Style=skia.Paint.kStroke_Style,
    StrokeWidth=8,
    AntiAlias=True,
    Color=skia.Color(255, 170, 0, 180),
    MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 10)
)
canvas.drawCircle(W / 2, H / 2, 435, ring_inner)

# 3. Dramatic Mystery Bus Silhouette / Road in the Center
# Road perspective
road_path = skia.Path()
road_path.moveTo(W / 2 - 40, 520)
road_path.lineTo(W / 2 + 40, 520)
road_path.lineTo(W / 2 + 320, 840)
road_path.lineTo(W / 2 - 320, 840)
road_path.close()

road_paint = skia.Paint(
    AntiAlias=True,
    Color=skia.Color(15, 18, 28, 230)
)
canvas.drawPath(road_path, road_paint)

# Neon Road markings
road_line = skia.Paint(
    Style=skia.Paint.kStroke_Style,
    StrokeWidth=6,
    Color=skia.Color(0, 230, 255, 190),
    AntiAlias=True
)
canvas.drawLine(W / 2, 530, W / 2, 830, road_line)

# Bus Silhouette
bus_path = skia.Path()
bx, by, bw, bh = W / 2 - 130, 410, 260, 180
bus_path.addRoundRect(skia.Rect(bx, by, bx + bw, by + bh), 24, 24)
bus_paint = skia.Paint(AntiAlias=True, Color=skia.Color(12, 14, 22))
canvas.drawPath(bus_path, bus_paint)

# Bus Windshield (cyan tinted night reflection)
ws_path = skia.Path()
ws_path.addRoundRect(skia.Rect(bx + 20, by + 25, bx + bw - 20, by + 95), 12, 12)
ws_paint = skia.Paint(
    AntiAlias=True,
    Color=skia.Color(0, 210, 255, 80),
    StrokeWidth=3,
    Style=skia.Paint.kStrokeAndFill_Style
)
canvas.drawPath(ws_path, ws_paint)

# Bus Headlights beam (volumetric cinematic cone)
beam_paint = skia.Paint(
    AntiAlias=True,
    Shader=skia.GradientShader.MakeLinear(
        [(W / 2, by + bh), (W / 2, by + bh + 260)],
        [skia.Color(255, 230, 130, 140), skia.Color(255, 200, 50, 0)],
        [0.0, 1.0]
    )
)
beam_path = skia.Path()
beam_path.moveTo(bx + 35, by + bh - 30)
beam_path.lineTo(bx - 120, by + bh + 260)
beam_path.lineTo(bx + bw + 120, by + bh + 260)
beam_path.lineTo(bx + bw - 35, by + bh - 30)
beam_path.close()
canvas.drawPath(beam_path, beam_paint)

# Dual Headlight Orbs
hl_paint = skia.Paint(
    AntiAlias=True,
    Color=skia.Color(255, 255, 220, 255),
    MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 8)
)
canvas.drawCircle(bx + 45, by + 130, 16, hl_paint)
canvas.drawCircle(bx + bw - 45, by + 130, 16, hl_paint)

# 4. Big Bold 3D Stylized Modern Text "GROW10Z"
font_mgr = skia.FontMgr()
tf_bold = font_mgr.matchFamilyStyle("Arial", skia.FontStyle.Bold())
if not tf_bold:
    tf_bold = skia.Typeface.MakeFromFile("fonts/FreeSansBold.ttf")

font_title = skia.Font(tf_bold, 102)

title_text = "GROW10Z"
title_w = font_title.measureText(title_text)
tx = (W - title_w) / 2
ty = 310

# Glow shadow behind text
glow_text = skia.Paint(
    AntiAlias=True,
    Color=skia.Color(0, 220, 255, 220),
    MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 18)
)
canvas.drawString(title_text, tx, ty, font_title, glow_text)

# Crisp white front text
white_text = skia.Paint(
    AntiAlias=True,
    Color=skia.Color(255, 255, 255, 255)
)
canvas.drawString(title_text, tx, ty, font_title, white_text)

# Subtitle Pill: "3D STORIES & SUSPENSE"
font_sub = skia.Font(tf_bold, 34)
sub_text = "3D STORIES & SUSPENSE"
sub_w = font_sub.measureText(sub_text)
sx = (W - sub_w) / 2
sy = 370

pill_bg = skia.Paint(AntiAlias=True, Color=skia.Color(255, 50, 80, 220))
canvas.drawRoundRect(skia.Rect(sx - 24, sy - 34, sx + sub_w + 24, sy + 14), 16, 16, pill_bg)

font_sub_paint = skia.Paint(AntiAlias=True, Color=skia.Color(255, 255, 255))
canvas.drawString(sub_text, sx, sy, font_sub, font_sub_paint)

# Save Logo
img = surf.makeImageSnapshot()
img.save("branding/grow10z_logo.png", skia.kPNG)
print("Logo successfully generated at branding/grow10z_logo.png")
