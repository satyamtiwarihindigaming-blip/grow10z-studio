import os, sys, math, json, subprocess
import skia
import numpy as np

# Import the new high-detail character module
sys.path.append("studio_ramayana/character_engine")
from ramayana_character_rigs import draw_baal_ram, draw_maharaja_dasharatha

W, H = 1080, 1920
FPS = 60
DUR = 41.75
TOTAL_FRAMES = int(DUR * FPS)  # 2505 frames

# Sacred Vedic / Royal Ayodhya Palette
C_GOLD_ROYAL = skia.ColorSetARGB(255, 255, 215, 0)
C_GOLD_DARK = skia.ColorSetARGB(255, 184, 134, 11)
C_PALACE_PILLAR = skia.ColorSetARGB(255, 245, 225, 195)

# Load V2 micro-chunk kinetic captions
with open("studio_ramayana/episodes/ep001/caption_events_v2.json", "r", encoding="utf-8") as f:
    caption_events = json.load(f)

caption_sprites = {}
for ev in caption_events:
    p = ev["png"]
    if os.path.exists(p):
        caption_sprites[ev["id"]] = skia.Image.open(p)

# Pre-render 1: 3D Ancient Ramayana Manuscript Cover
surf_book = skia.Surface(W, H)
cv_b = surf_book.getCanvas()
cv_b.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Color=skia.ColorSetARGB(255, 85, 12, 20)))

# Double Gold Border with intricate patterns
p_border = skia.Path()
p_border.addRoundRect(skia.Rect(45, 55, W - 45, H - 55), 24, 24)
cv_b.drawPath(p_border, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=16, Color=C_GOLD_ROYAL, AntiAlias=True))
p_inner = skia.Path()
p_inner.addRoundRect(skia.Rect(75, 85, W - 75, H - 85), 16, 16)
cv_b.drawPath(p_inner, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=4, Color=C_GOLD_DARK, AntiAlias=True))

# Center Golden Surya Dynasty Sun
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

# Pre-render 2: Grand Ayodhya Royal Palace Hall
surf_palace = skia.Surface(W, H)
cv_p = surf_palace.getCanvas()

# Divine Golden Dawn Sky
sky_shader = skia.GradientShader.MakeLinear(
    [(0, 0), (0, 950)],
    [skia.ColorSetARGB(255, 255, 130, 40), skia.ColorSetARGB(255, 255, 215, 110), skia.ColorSetARGB(255, 255, 250, 235)],
    [0.0, 0.6, 1.0]
)
cv_p.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Shader=sky_shader))

# Grand Vedic Pillars
for px in [140, W - 140]:
    p_col = skia.Path()
    p_col.addRoundRect(skia.Rect(px - 65, 180, px + 65, H), 12, 12)
    cv_p.drawPath(p_col, skia.Paint(Color=C_PALACE_PILLAR, AntiAlias=True))
    cv_p.drawPath(p_col, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=8, Color=C_GOLD_DARK, AntiAlias=True))

# Palace Arch
p_arch = skia.Path()
p_arch.moveTo(0, 900)
p_arch.lineTo(0, 220)
p_arch.quadTo(W / 2, 70, W, 220)
p_arch.lineTo(W, 900)
p_arch.close()
cv_p.drawPath(p_arch, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=40, Color=C_PALACE_PILLAR, AntiAlias=True))
cv_p.drawPath(p_arch, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=12, Color=C_GOLD_ROYAL, AntiAlias=True))

# Marble Floor
floor_shader = skia.GradientShader.MakeLinear(
    [(0, 1150), (0, H)],
    [skia.ColorSetARGB(255, 240, 230, 215), skia.ColorSetARGB(255, 205, 190, 170)],
    [0.0, 1.0]
)
cv_p.drawRect(skia.Rect(0, 1150, W, H), skia.Paint(Shader=floor_shader))

# Golden Chains hanging the cradle
cradle_cx, cradle_cy = W / 2, 1260
cv_p.drawLine(cradle_cx - 160, 480, cradle_cx - 140, cradle_cy, skia.Paint(StrokeWidth=6, Color=C_GOLD_ROYAL, AntiAlias=True))
cv_p.drawLine(cradle_cx + 160, 480, cradle_cx + 140, cradle_cy, skia.Paint(StrokeWidth=6, Color=C_GOLD_ROYAL, AntiAlias=True))

plate_palace_img = surf_palace.makeImageSnapshot()

print("Plates cached. Launching High-Detail Ramayana FFmpeg pipeline...")

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
    "studio_ramayana/episodes/ep001/temp_video_v2.mp4"
]

ffmpeg_proc = subprocess.Popen(
    ffmpeg_cmd,
    stdin=subprocess.PIPE,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

render_surf = skia.Surface(W, H)
cv = render_surf.getCanvas()

# Procedural Flower Petals
rng = np.random.default_rng(108)
petal_x = rng.uniform(0, W, 140)
petal_y = rng.uniform(0, H, 140)
petal_s = rng.uniform(3, 7, 140)

for frame_idx in range(TOTAL_FRAMES):
    t = frame_idx / FPS
    
    # 1. 0.0s - 4.5s: 3D Ancient Book Open & Dolly-In
    if t < 4.5:
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
        cv.drawImage(plate_palace_img, 0, 0)
        
        # Camera Pan & Zoom dynamics
        cradle_cx, cradle_cy = W / 2, 1260
        rock_angle = 3.5 * math.sin(t * 3.0)
        
        # 18.0s - 23.0s: Dramatic Close-up on Baal Ram's Lotus Eyes & Smile
        if 18.0 <= t <= 23.0:
            ram_scale = 1.35
            ram_y = cradle_cy - 120
        else:
            ram_scale = 1.0
            ram_y = cradle_cy
            
        # Draw High-Detail Baal Ram
        draw_baal_ram(cv, cradle_cx, ram_y, scale=ram_scale, rock_angle=rock_angle)
        
        # Draw High-Detail Maharaja Dasharatha (t >= 12.0s)
        if t >= 12.0:
            draw_maharaja_dasharatha(cv, 240, 960, scale=1.0)
            
        # Pushpa Varsha (पुष्प वर्षा - Falling sacred petals at t >= 23.0s)
        if t >= 23.0:
            petal_y = (petal_y + petal_s) % H
            for px_pt, py_pt in zip(petal_x, petal_y):
                cv.drawOval(skia.Rect(px_pt - 9, py_pt - 5, px_pt + 9, py_pt + 5), skia.Paint(Color=skia.ColorSetARGB(235, 255, 75, 85), AntiAlias=True))

    # Top Header Series Pill: "GROW10Z • रामायण: भाग 1"
    pill_w, pill_h = 650, 72
    px_hd = (W - pill_w) / 2
    cv.drawRoundRect(skia.Rect(px_hd, 45, px_hd + pill_w, 45 + pill_h), 20, 20, skia.Paint(Color=skia.ColorSetARGB(245, 18, 22, 38), AntiAlias=True))
    cv.drawRoundRect(skia.Rect(px_hd, 45, px_hd + pill_w, 45 + pill_h), 20, 20, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=4, Color=C_GOLD_ROYAL, AntiAlias=True))

    # Burned-In V2 Kinetic Micro-Chunk Subtitles
    for ev in caption_events:
        if ev["start"] <= t <= ev["end"]:
            sp = caption_sprites.get(ev["id"])
            if sp:
                cx = (W - sp.width()) / 2
                cy = 1450  # Inside Instagram/Shorts ideal safe-zone
                cv.drawImage(sp, cx, cy)
            break

    img = render_surf.makeImageSnapshot()
    raw_bytes = img.tobytes()
    ffmpeg_proc.stdin.write(raw_bytes)

ffmpeg_proc.stdin.close()
ffmpeg_proc.wait()

print("Video stream finished. Muxing master 60fps audio...")

mux_cmd = [
    "ffmpeg", "-y",
    "-i", "studio_ramayana/episodes/ep001/temp_video_v2.mp4",
    "-i", "studio_ramayana/episodes/ep001/voice/ep001_final_audio.wav",
    "-c:v", "copy",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    "-movflags", "+faststart",
    "studio_ramayana/episodes/ep001/ep001_final.mp4"
]
subprocess.run(mux_cmd, check=True)
print("Updated Remastered Ramayana Ep 001 Complete! File: studio_ramayana/episodes/ep001/ep001_final.mp4")
