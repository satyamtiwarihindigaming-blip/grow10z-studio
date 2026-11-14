import os, sys, math, json, subprocess
import skia
import numpy as np

# Import character rigs
sys.path.append("studio_ramayana/character_engine")
from ramayana_character_rigs import (
    draw_maharaja_dasharatha,
    draw_shri_ram_warrior,
    draw_maharishi_vishwamitra,
    draw_tadaka
)

W, H = 1080, 1920
FPS = 60
DUR = 51.5
TOTAL_FRAMES = int(DUR * FPS)  # 3090 frames

C_GOLD_ROYAL = skia.ColorSetARGB(255, 255, 215, 0)
C_GOLD_DARK = skia.ColorSetARGB(255, 184, 134, 11)
C_PALACE_PILLAR = skia.ColorSetARGB(255, 245, 225, 195)

# Load V2 micro-chunk captions
with open("studio_ramayana/episodes/ep002/caption_events_v2.json", "r", encoding="utf-8") as f:
    caption_events = json.load(f)

caption_sprites = {}
for ev in caption_events:
    p = ev["png"]
    if os.path.exists(p):
        caption_sprites[ev["id"]] = skia.Image.open(p)

# Pre-render 1: 3D Ancient Manuscript Cover
surf_book = skia.Surface(W, H)
cv_b = surf_book.getCanvas()
cv_b.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Color=skia.ColorSetARGB(255, 85, 12, 20)))

p_border = skia.Path()
p_border.addRoundRect(skia.Rect(45, 55, W - 45, H - 55), 24, 24)
cv_b.drawPath(p_border, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=16, Color=C_GOLD_ROYAL, AntiAlias=True))
p_inner = skia.Path()
p_inner.addRoundRect(skia.Rect(75, 85, W - 75, H - 85), 16, 16)
cv_b.drawPath(p_inner, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=4, Color=C_GOLD_DARK, AntiAlias=True))

sun_cx, sun_cy = W / 2, 750
cv_b.drawCircle(sun_cx, sun_cy, 125, skia.Paint(Color=C_GOLD_ROYAL, AntiAlias=True))
cv_b.drawCircle(sun_cx, sun_cy, 108, skia.Paint(Color=skia.ColorSetARGB(255, 110, 16, 24), AntiAlias=True))
for deg in range(0, 360, 20):
    rad = math.radians(deg)
    p_ray = skia.Path()
    p_ray.moveTo(sun_cx + 125 * math.cos(rad), sun_cy + 125 * math.sin(rad))
    p_ray.lineTo(sun_cx + 175 * math.cos(rad), sun_cy + 175 * math.sin(rad))
    cv_b.drawPath(p_ray, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=6, Color=C_GOLD_ROYAL, AntiAlias=True))

plate_book_img = surf_book.makeImageSnapshot()

# Pre-render 2: Royal Ayodhya Darbar Hall
surf_darbar = skia.Surface(W, H)
cv_d = surf_darbar.getCanvas()

sky_grad = skia.GradientShader.MakeLinear(
    [skia.Point(0, 0), skia.Point(0, 1050)],
    [skia.ColorSetARGB(255, 255, 140, 50), skia.ColorSetARGB(255, 255, 210, 110), skia.ColorSetARGB(255, 255, 245, 220)],
    [0.0, 0.6, 1.0]
)
cv_d.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Shader=sky_grad))

# Pillars
for px in [120, W - 120]:
    p_col = skia.Path()
    p_col.addRoundRect(skia.Rect(px - 70, 160, px + 70, H), 12, 12)
    cv_d.drawPath(p_col, skia.Paint(Color=C_PALACE_PILLAR, AntiAlias=True))
    cv_d.drawPath(p_col, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=8, Color=C_GOLD_DARK, AntiAlias=True))

# Grand Arch
p_arch = skia.Path()
p_arch.moveTo(0, 950)
p_arch.lineTo(0, 200)
p_arch.quadTo(W / 2, 60, W, 200)
p_arch.lineTo(W, 950)
p_arch.close()
cv_d.drawPath(p_arch, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=36, Color=C_PALACE_PILLAR, AntiAlias=True))
cv_d.drawPath(p_arch, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=10, Color=C_GOLD_ROYAL, AntiAlias=True))

# Marble Floor
floor_grad = skia.GradientShader.MakeLinear(
    [skia.Point(0, 1100), skia.Point(0, H)],
    [skia.ColorSetARGB(255, 245, 235, 220), skia.ColorSetARGB(255, 195, 180, 165)],
    [0.0, 1.0]
)
cv_d.drawRect(skia.Rect(0, 1100, W, H), skia.Paint(Shader=floor_grad))

plate_darbar_img = surf_darbar.makeImageSnapshot()

# Pre-render 3: Sunset over Sarayu River & Ayodhya Shore
surf_sarayu = skia.Surface(W, H)
cv_s = surf_sarayu.getCanvas()

sarayu_sky = skia.GradientShader.MakeLinear(
    [skia.Point(0, 0), skia.Point(0, 1200)],
    [skia.ColorSetARGB(255, 230, 85, 30), skia.ColorSetARGB(255, 255, 165, 60), skia.ColorSetARGB(255, 255, 225, 140)],
    [0.0, 0.5, 1.0]
)
cv_s.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Shader=sarayu_sky))

# Setting Golden Sun
cv_s.drawCircle(W / 2, 700, 110, skia.Paint(Color=skia.ColorSetARGB(255, 255, 240, 180), AntiAlias=True))

# River water
water_grad = skia.GradientShader.MakeLinear(
    [skia.Point(0, 1150), skia.Point(0, H)],
    [skia.ColorSetARGB(255, 180, 95, 45), skia.ColorSetARGB(255, 75, 40, 30)],
    [0.0, 1.0]
)
cv_s.drawRect(skia.Rect(0, 1150, W, H), skia.Paint(Shader=water_grad))

# Ayodhya temple silhouettes in background
temple_p = skia.Paint(Color=skia.ColorSetARGB(200, 70, 30, 25), AntiAlias=True)
for tx in [160, 380, 700, 920]:
    p_t = skia.Path()
    p_t.moveTo(tx - 70, 1150)
    p_t.lineTo(tx, 820)
    p_t.lineTo(tx + 70, 1150)
    p_t.close()
    cv_s.drawPath(p_t, temple_p)

plate_sarayu_img = surf_sarayu.makeImageSnapshot()

print("Plates cached. Launching Cinematic Ep 002 FFmpeg pipeline...")

# Floating sacred particles
np.random.seed(108)
particles = [{"x": np.random.randint(40, W-40), "y": np.random.randint(60, H-60), "r": np.random.uniform(4, 9), "speed": np.random.uniform(1.2, 3.2)} for _ in range(35)]

temp_video = "studio_ramayana/episodes/ep002/temp_video_v2.mp4"
ffmpeg_cmd = [
    "ffmpeg", "-y",
    "-f", "rawvideo",
    "-pix_fmt", "bgra",
    "-s", f"{W}x{H}",
    "-r", str(FPS),
    "-i", "-",
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-profile:v", "baseline",
    "-preset", "ultrafast",
    "-crf", "18",
    temp_video
]

pipe = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)
surf_frame = skia.Surface(W, H)
canvas = surf_frame.getCanvas()

for f in range(TOTAL_FRAMES):
    t = f / FPS
    canvas.clear(skia.ColorBLACK)

    # SCENE 1: 3D Manuscript Opening (0.0s - 3.2s)
    if t < 3.2:
        canvas.drawImage(plate_darbar_img, 0, 0)
        draw_maharaja_dasharatha(canvas, 540, 1080, scale=1.45)
        
        # 3D Book page turn fold
        turn_t = min(1.0, max(0.0, (t - 0.4) / 2.6))
        curve = turn_t * turn_t * (3.0 - 2.0 * turn_t)
        angle = -curve * 90.0
        
        canvas.save()
        canvas.translate(0, H / 2)
        m = skia.Matrix()
        scale_x = math.cos(math.radians(angle))
        skew_y = math.sin(math.radians(angle)) * 0.22
        m.setScaleX(scale_x)
        m.setSkewY(skew_y)
        canvas.concat(m)
        canvas.translate(0, -H / 2)
        
        if angle > -85.0:
            canvas.drawImage(plate_book_img, 0, 0)
            sh_paint = skia.Paint(Color=skia.ColorSetARGB(int(turn_t * 220), 0, 0, 0))
            canvas.drawRect(skia.Rect(0, 0, W, H), sh_paint)
        canvas.restore()

    # SCENE 2: Ayodhya Darbar & Royal Court (3.2s - 10.4s)
    elif t < 10.4:
        # Subtle slow cinematic zoom
        zoom = 1.0 + (t - 3.2) * 0.015
        canvas.save()
        canvas.translate(W / 2, H / 2)
        canvas.scale(zoom, zoom)
        canvas.translate(-W / 2, -H / 2)
        canvas.drawImage(plate_darbar_img, 0, 0)
        
        # Maharaja Dasharatha on golden throne
        draw_maharaja_dasharatha(canvas, 540, 1100, scale=1.55)
        canvas.restore()

    # SCENE 3: Entrance of Maharishi Vishwamitra (10.4s - 22.4s)
    elif t < 22.4:
        canvas.drawImage(plate_darbar_img, 0, 0)
        
        # Flaring Tapasya Energy
        flare_alpha = int(120 + 35 * math.sin(t * 6.0))
        cv_flare = skia.Paint(
            Shader=skia.GradientShader.MakeRadial(
                skia.Point(620, 1020), 320,
                [skia.ColorSetARGB(flare_alpha, 255, 180, 50), skia.ColorSetARGB(0, 255, 100, 0)],
                [0.0, 1.0]
            ),
            AntiAlias=True
        )
        canvas.drawCircle(620, 1020, 320, cv_flare)
        
        # Dasharatha in awe on left, Vishwamitra dominating right
        draw_maharaja_dasharatha(canvas, 240, 1200, scale=1.35)
        breath = 1.0 + 0.015 * math.sin(t * 3.0)
        draw_maharishi_vishwamitra(canvas, 680, 1040, scale=1.85 * breath)

    # SCENE 4: Dasharatha's Grief & Reluctance (22.4s - 30.5s)
    elif t < 30.5:
        # Dimmer, emotional lighting
        canvas.drawImage(plate_darbar_img, 0, 0)
        dim_paint = skia.Paint(Color=skia.ColorSetARGB(75, 10, 5, 20))
        canvas.drawRect(skia.Rect(0, 0, W, H), dim_paint)
        
        # Close-up of Dasharatha with folded hands in distress
        draw_maharaja_dasharatha(canvas, 480, 1050, scale=1.85)

    # SCENE 5: Shri Ram & Lakshman Step Forward (30.5s - 37.5s)
    elif t < 37.5:
        canvas.drawImage(plate_darbar_img, 0, 0)
        # Divine celestial glow of Shri Ram
        breath = 1.0 + 0.018 * math.sin(t * 3.2)
        # Shri Ram Center Stage
        draw_shri_ram_warrior(canvas, 540, 1050, scale=1.85 * breath)
        # Vishwamitra bestowing blessing on right
        draw_maharishi_vishwamitra(canvas, 880, 1150, scale=1.35)

    # SCENE 6: Heroic Departure to Sarayu Shore (37.5s - 45.0s)
    elif t < 45.0:
        canvas.drawImage(plate_sarayu_img, 0, 0)
        # Dynamic walking / marching motion
        march_bob = 8.0 * math.sin(t * 7.5)
        # Shri Ram warrior leading
        draw_shri_ram_warrior(canvas, 500, 1080 + march_bob, scale=1.75)
        # Lakshman walking alongside
        draw_shri_ram_warrior(canvas, 780, 1120 - march_bob, scale=1.45)

    # SCENE 7: Cliffhanger - The Dreaded Tadaka Teaser (45.0s - 51.5s)
    else:
        # Darkening twilight into demon-haunted forest
        dark_p = skia.Paint(
            Shader=skia.GradientShader.MakeLinear(
                [skia.Point(0, 0), skia.Point(0, H)],
                [skia.ColorSetARGB(255, 30, 8, 12), skia.ColorSetARGB(255, 15, 5, 10)],
                [0.0, 1.0]
            )
        )
        canvas.drawRect(skia.Rect(0, 0, W, H), dark_p)
        
        # Tadaka towering silhouette with fiery red eyes
        draw_tadaka(canvas, 540, 980, scale=1.85)
        # Fiery embers
        for pt in particles:
            canvas.drawCircle(pt["x"], pt["y"], pt["r"] * 1.5, skia.Paint(Color=skia.ColorSetARGB(220, 255, 60, 20), AntiAlias=True))

    # Floating sacred dust & flower petals (Scenes 1-6)
    if t < 45.0:
        for pt in particles:
            py = (pt["y"] - pt["speed"] * f * 0.8) % H
            canvas.drawCircle(pt["x"], py, pt["r"], skia.Paint(Color=skia.ColorSetARGB(180, 255, 230, 110), AntiAlias=True))

    # KINETIC SUBTITLE OVERLAY
    for ev in caption_events:
        if ev["start"] <= t < ev["end"]:
            sp = caption_sprites.get(ev["id"])
            if sp:
                # Pop bounce animation
                elapsed = t - ev["start"]
                pop_scale = min(1.0, elapsed * 6.0) if elapsed < 0.18 else 1.0
                canvas.save()
                canvas.translate(W / 2, H - 360)
                canvas.scale(pop_scale, pop_scale)
                canvas.drawImage(sp, -sp.width() / 2, -sp.height() / 2)
                canvas.restore()
            break

    # Top Brand Header
    h_font = skia.Font(skia.Typeface.MakeFromName("Arial", skia.FontStyle.Bold()), 38)
    canvas.drawString("GROW10Z • सम्पूर्ण रामायण", 80, 115, h_font, skia.Paint(Color=skia.ColorSetARGB(230, 255, 215, 0), AntiAlias=True))
    canvas.drawString("भाग 002: विश्वामित्र आगमन", W - 460, 115, h_font, skia.Paint(Color=skia.ColorSetARGB(200, 255, 245, 220), AntiAlias=True))

    # Write frame to FFmpeg pipe
    img = surf_frame.makeImageSnapshot()
    pipe.stdin.write(img.tobytes())

    if f % 400 == 0:
        print(f"Render progress: {f}/{TOTAL_FRAMES} frames ({f/TOTAL_FRAMES*100:.1f}%)")

pipe.stdin.close()
pipe.wait()

print("Video stream complete! Muxing master audio...")

final_video = "studio_ramayana/episodes/ep002/ep002_final.mp4"
audio_file = "studio_ramayana/episodes/ep002/voice/ep002_final_audio.wav"

subprocess.run([
    "ffmpeg", "-y",
    "-i", temp_video,
    "-i", audio_file,
    "-c:v", "copy",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    final_video
], check=True)

print(f"🎉 Remastered Cinematic Ep 002 COMPLETE! File: {final_video}")
