import os, sys, math, json, subprocess
import skia
import numpy as np

W, H = 1080, 1920
FPS = 60
DUR = 41.75
TOTAL_FRAMES = int(DUR * FPS)  # 2505 frames

# Sacred Vedic / Royal Ayodhya Palette
C_GOLD_ROYAL = skia.ColorSetARGB(255, 255, 215, 0)
C_GOLD_DARK = skia.ColorSetARGB(255, 184, 134, 11)
C_PITAMBARI = skia.ColorSetARGB(255, 255, 179, 0)
C_NEEL_SHYAM = skia.ColorSetARGB(255, 45, 85, 155)  # Baal Ram's Divine Blue Hue
C_PALACE_PILLAR = skia.ColorSetARGB(255, 245, 225, 195)
C_PARCHMENT = skia.ColorSetARGB(255, 246, 235, 212)
C_INK_RED = skia.ColorSetARGB(255, 168, 32, 42)

with open("studio_ramayana/episodes/ep001/caption_events.json", "r", encoding="utf-8") as f:
    caption_events = json.load(f)

caption_sprites = {}
for ev in caption_events:
    p = ev["png"]
    if os.path.exists(p):
        caption_sprites[ev["id"]] = skia.Image.open(p)

# Pre-render 1: 3D Ancient Ramayana Manuscript Cover & Parchment Plate
surf_book = skia.Surface(W, H)
cv_b = surf_book.getCanvas()

# Velvet Red Leather Book Cover
cv_b.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Color=skia.ColorSetARGB(255, 88, 14, 22)))

# Golden Vedic Ornamental Border (Double border with corner mandalas)
p_border = skia.Path()
p_border.addRoundRect(skia.Rect(45, 55, W - 45, H - 55), 24, 24)
cv_b.drawPath(p_border, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=16, Color=C_GOLD_ROYAL, AntiAlias=True))
p_inner_border = skia.Path()
p_inner_border.addRoundRect(skia.Rect(75, 85, W - 75, H - 85), 16, 16)
cv_b.drawPath(p_inner_border, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=4, Color=C_GOLD_DARK, AntiAlias=True))

# Center Golden Sun (Surya Dynasty Emblem / सूर्यवंश प्रतीक)
sun_cx, sun_cy = W / 2, 750
cv_b.drawCircle(sun_cx, sun_cy, 120, skia.Paint(Color=C_GOLD_ROYAL, AntiAlias=True))
cv_b.drawCircle(sun_cx, sun_cy, 105, skia.Paint(Color=skia.ColorSetARGB(255, 120, 20, 28), AntiAlias=True))
# 16 Sun Rays
for deg in range(0, 360, 22):
    rad = math.radians(deg)
    p_ray = skia.Path()
    p_ray.moveTo(sun_cx + 120 * math.cos(rad), sun_cy + 120 * math.sin(rad))
    p_ray.lineTo(sun_cx + 165 * math.cos(rad), sun_cy + 165 * math.sin(rad))
    cv_b.drawPath(p_ray, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=6, Color=C_GOLD_ROYAL, AntiAlias=True))

plate_book_img = surf_book.makeImageSnapshot()

# Pre-render 2: Grand Ayodhya Royal Palace Hall (Swarna Mandir & Pillars)
surf_palace = skia.Surface(W, H)
cv_p = surf_palace.getCanvas()

# Divine Golden Dawn Sky through palace arches
sky_shader = skia.GradientShader.MakeLinear(
    [(0, 0), (0, 900)],
    [skia.ColorSetARGB(255, 255, 140, 50), skia.ColorSetARGB(255, 255, 220, 120), skia.ColorSetARGB(255, 255, 250, 230)],
    [0.0, 0.6, 1.0]
)
cv_p.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Shader=sky_shader))

# Grand Vedic Arches
p_arch = skia.Path()
p_arch.moveTo(0, 850)
p_arch.lineTo(0, 220)
p_arch.quadTo(W / 2, 80, W, 220)
p_arch.lineTo(W, 850)
p_arch.close()
cv_p.drawPath(p_arch, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=40, Color=C_PALACE_PILLAR, AntiAlias=True))
cv_p.drawPath(p_arch, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=12, Color=C_GOLD_ROYAL, AntiAlias=True))

# Massive Golden Pillars
for px in [120, W - 120]:
    p_col = skia.Path()
    p_col.addRoundRect(skia.Rect(px - 60, 220, px + 60, H), 12, 12)
    cv_p.drawPath(p_col, skia.Paint(Color=C_PALACE_PILLAR, AntiAlias=True))
    cv_p.drawPath(p_col, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=8, Color=C_GOLD_DARK, AntiAlias=True))

# Marble Palace Floor with Reflection
floor_shader = skia.GradientShader.MakeLinear(
    [(0, 1150), (0, H)],
    [skia.ColorSetARGB(255, 240, 230, 215), skia.ColorSetARGB(255, 210, 195, 175)],
    [0.0, 1.0]
)
cv_p.drawRect(skia.Rect(0, 1150, W, H), skia.Paint(Shader=floor_shader))

# Royal Golden Cradle (स्वर्ण पालना) in Center
cradle_cx, cradle_cy = W / 2, 1280
# Cradle Stand & Chains
cv_p.drawLine(cradle_cx - 160, 500, cradle_cx - 140, cradle_cy, skia.Paint(StrokeWidth=6, Color=C_GOLD_ROYAL, AntiAlias=True))
cv_p.drawLine(cradle_cx + 160, 500, cradle_cx + 140, cradle_cy, skia.Paint(StrokeWidth=6, Color=C_GOLD_ROYAL, AntiAlias=True))

# Golden Cradle Body
p_cradle = skia.Path()
p_cradle.addRoundRect(skia.Rect(cradle_cx - 180, cradle_cy - 60, cradle_cx + 180, cradle_cy + 80), 30, 30)
cv_p.drawPath(p_cradle, skia.Paint(Color=skia.ColorSetARGB(255, 255, 205, 45), AntiAlias=True))
cv_p.drawPath(p_cradle, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=8, Color=C_GOLD_DARK, AntiAlias=True))

# Red Velvet Bedding
p_bed = skia.Path()
p_bed.addRoundRect(skia.Rect(cradle_cx - 150, cradle_cy - 40, cradle_cx + 150, cradle_cy + 60), 20, 20)
cv_p.drawPath(p_bed, skia.Paint(Color=skia.ColorSetARGB(255, 180, 22, 35), AntiAlias=True))

plate_palace_img = surf_palace.makeImageSnapshot()

print("Ramayana Studio Plates cached. Starting FFmpeg 60fps render engine...")

ffmpeg_cmd = [
    "ffmpeg", "-y",
    "-f", "rawvideo",
    "-vcodec", "rawvideo",
    "-s", f"{W}x{H}",
    "-pix_fmt", "bgra",
    "-r", str(FPS),
    "-i", "-",
    "-c:v", "libx264",
    "-preset", "ultrafast",
    "-crf", "19",
    "-pix_fmt", "yuv420p",
    "studio_ramayana/episodes/ep001/temp_video.mp4"
]

ffmpeg_proc = subprocess.Popen(
    ffmpeg_cmd,
    stdin=subprocess.PIPE,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

render_surf = skia.Surface(W, H)
cv = render_surf.getCanvas()

# Procedural Flower Petal Shower (पुष्प वर्षा) Coordinates
rng = np.random.default_rng(108)
petal_x = rng.uniform(0, W, 120)
petal_y = rng.uniform(0, H, 120)
petal_s = rng.uniform(3, 7, 120)

for frame_idx in range(TOTAL_FRAMES):
    t = frame_idx / FPS
    
    # 1. 0.0s - 4.5s: 3D Ancient Manuscript Book Opens & Camera Dolly-in Through Page
    if t < 4.5:
        # 3D Book Dolly Push-in
        prog = t / 4.5
        scale_cam = 1.0 + (prog ** 2.0) * 2.5
        alpha_book = max(0.0, 1.0 - (prog ** 3.0))
        
        cv.drawImage(plate_palace_img, 0, 0)
        
        cv.save()
        cv.translate(W / 2, H / 2)
        cv.scale(scale_cam, scale_cam)
        cv.translate(-W / 2, -H / 2)
        
        paint_b = skia.Paint(AntiAlias=True)
        paint_b.setAlphaf(alpha_book)
        cv.drawImage(plate_book_img, 0, 0, skia.SamplingOptions(), paint_b)
        cv.restore()
        
    else:
        # Full Ayodhya Royal Palace Environment
        cv.drawImage(plate_palace_img, 0, 0)
        
        cradle_cx, cradle_cy = W / 2, 1280
        # Gentle divine rocking of the cradle
        rock_angle = 3.5 * math.sin(t * 3.0)
        
        cv.save()
        cv.translate(cradle_cx, cradle_cy - 120)
        cv.rotate(rock_angle)
        cv.translate(-cradle_cx, -(cradle_cy - 120))
        
        # Divine Baal Ram (नन्हें बाल श्रीराम)
        # Divine Blue Skin with glowing aura (नील कमल सी कांति)
        cv.drawCircle(cradle_cx, cradle_cy - 10, 48, skia.Paint(Color=C_NEEL_SHYAM, AntiAlias=True))
        # Golden Halo Aura (तेजपुंज) around Baal Ram's head
        halo_paint = skia.Paint(
            Shader=skia.GradientShader.MakeRadial(
                (cradle_cx, cradle_cy - 10), 110,
                [skia.ColorSetARGB(180, 255, 230, 100), skia.ColorSetARGB(0, 255, 215, 0)],
                [0.0, 1.0]
            ),
            AntiAlias=True
        )
        cv.drawCircle(cradle_cx, cradle_cy - 10, 110, halo_paint)
        
        # Golden Mukut (बाल मुकुट) with Peacock Feather Crest
        p_mukut = skia.Path()
        p_mukut.moveTo(cradle_cx - 35, cradle_cy - 45)
        p_mukut.lineTo(cradle_cx, cradle_cy - 85)
        p_mukut.lineTo(cradle_cx + 35, cradle_cy - 45)
        p_mukut.close()
        cv.drawPath(p_mukut, skia.Paint(Color=C_GOLD_ROYAL, AntiAlias=True))
        
        # Yellow Silk Pitambari Swaddle Cloth
        p_cloth = skia.Path()
        p_cloth.addRoundRect(skia.Rect(cradle_cx - 50, cradle_cy + 15, cradle_cx + 50, cradle_cy + 75), 18, 18)
        cv.drawPath(p_cloth, skia.Paint(Color=C_PITAMBARI, AntiAlias=True))
        cv.restore()
        
        # Maharaja Dasharatha (Standing proudly on screen-left, t >= 12.0s)
        if t >= 12.0:
            dx, dy = 260, 1020
            # Royal Kurta & Crown
            cv.drawCircle(dx, dy - 60, 46, skia.Paint(Color=skia.ColorSetARGB(255, 210, 160, 110), AntiAlias=True)) # Skin
            # Crown
            p_cr = skia.Path()
            p_cr.moveTo(dx - 35, dy - 95); p_cr.lineTo(dx, dy - 145); p_cr.lineTo(dx + 35, dy - 95); p_cr.close()
            cv.drawPath(p_cr, skia.Paint(Color=C_GOLD_ROYAL, AntiAlias=True))
            # Royal Robe
            p_robe = skia.Path()
            p_robe.addRoundRect(skia.Rect(dx - 70, dy - 10, dx + 70, dy + 320), 25, 25)
            cv.drawPath(p_robe, skia.Paint(Color=skia.ColorSetARGB(255, 140, 20, 30), AntiAlias=True))
            # Golden Royal Garland (माला)
            cv.drawOval(skia.Rect(dx - 45, dy, dx + 45, dy + 110), skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=8, Color=C_GOLD_ROYAL, AntiAlias=True))
            
        # Pushpa Varsha (फूलों की वर्षा - Gentle Falling Rose & Marigold Petals)
        if t >= 26.0:
            petal_y = (petal_y + petal_s) % H
            for px_pt, py_pt in zip(petal_x, petal_y):
                # Golden & Red Petals
                cv.drawOval(skia.Rect(px_pt - 8, py_pt - 5, px_pt + 8, py_pt + 5), skia.Paint(Color=skia.ColorSetARGB(230, 255, 80, 90), AntiAlias=True))

    # Top Header Series Pill: "GROW10Z • रामायण: भाग 1"
    pill_w, pill_h = 650, 72
    px_hd = (W - pill_w) / 2
    cv.drawRoundRect(skia.Rect(px_hd, 45, px_hd + pill_w, 45 + pill_h), 20, 20, skia.Paint(Color=skia.ColorSetARGB(240, 18, 22, 38), AntiAlias=True))
    cv.drawRoundRect(skia.Rect(px_hd, 45, px_hd + pill_w, 45 + pill_h), 20, 20, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=4, Color=C_GOLD_ROYAL, AntiAlias=True))

    # Burned-in micro-timed Devanagari captions
    for ev in caption_events:
        if ev["start"] <= t <= ev["end"]:
            sp = caption_sprites.get(ev["id"])
            if sp:
                cx = (W - sp.width()) / 2
                cy = 1420
                cv.drawImage(sp, cx, cy)
            break

    img = render_surf.makeImageSnapshot()
    raw_bytes = img.tobytes()
    ffmpeg_proc.stdin.write(raw_bytes)

ffmpeg_proc.stdin.close()
ffmpeg_proc.wait()

print("Ramayana Ep 001 Video stream finished. Muxing master 60fps audio...")

mux_cmd = [
    "ffmpeg", "-y",
    "-i", "studio_ramayana/episodes/ep001/temp_video.mp4",
    "-i", "studio_ramayana/episodes/ep001/voice/ep001_final_audio.wav",
    "-c:v", "copy",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    "-movflags", "+faststart",
    "studio_ramayana/episodes/ep001/ep001_final.mp4"
]
subprocess.run(mux_cmd, check=True)
print("GROW10Z Ramayana Episode 001 Complete! Saved: studio_ramayana/episodes/ep001/ep001_final.mp4")
