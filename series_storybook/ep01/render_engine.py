import os, sys, math, json, subprocess
import skia
import numpy as np

# Total video parameters
W, H = 1080, 1920
FPS = 60
DUR = 27.17
TOTAL_FRAMES = int(DUR * FPS)  # ~1630 frames

# Indian Folklore Vintage Palette
C_PARCHMENT = skia.ColorSetARGB(255, 238, 226, 204)
C_DARK_INK = skia.ColorSetARGB(255, 17, 22, 38)
C_DEEP_BLUE = skia.ColorSetARGB(255, 26, 38, 64)
C_CRIMSON = skia.ColorSetARGB(255, 158, 48, 55)
C_GOLD_AMBER = skia.ColorSetARGB(255, 205, 160, 95)
C_WELL_WATER = skia.ColorSetARGB(255, 8, 12, 20)

with open("series_storybook/ep01/caption_events.json", "r", encoding="utf-8") as f:
    caption_events = json.load(f)

caption_sprites = {}
for ev in caption_events:
    p = ev["png"]
    if os.path.exists(p):
        caption_sprites[ev["id"]] = skia.Image.open(p)

# Pre-render 1: Ancient Village Illustrated Plate
surf_village = skia.Surface(W, H)
cv_v = surf_village.getCanvas()

# Vintage parchment gradient background
cv_v.drawRect(
    skia.Rect(0, 0, W, H),
    skia.Paint(Shader=skia.GradientShader.MakeLinear(
        [(0, 0), (0, H)],
        [skia.ColorSetARGB(255, 14, 18, 30), skia.ColorSetARGB(255, 8, 10, 18)],
        [0.0, 1.0]
    ))
)

# Aged Paper Texture Border
border_paint = skia.Paint(
    Style=skia.Paint.kStroke_Style,
    StrokeWidth=14,
    Color=skia.ColorSetARGB(255, 165, 138, 101),
    AntiAlias=True
)
cv_v.drawRoundRect(skia.Rect(40, 40, W - 40, H - 40), 28, 28, border_paint)

# Moonlit Village Houses Silhouettes
p_houses = skia.Path()
p_houses.moveTo(0, 1250)
p_houses.lineTo(160, 1150)
p_houses.lineTo(320, 1250)
p_houses.lineTo(440, 1100)
p_houses.lineTo(580, 1250)
p_houses.lineTo(720, 1160)
p_houses.lineTo(880, 1250)
p_houses.lineTo(W, 1120)
p_houses.lineTo(W, H)
p_houses.lineTo(0, H)
p_houses.close()
cv_v.drawPath(p_houses, skia.Paint(Color=skia.ColorSetARGB(255, 18, 24, 38), AntiAlias=True))

# Ancient Banyan Tree branches
p_tree = skia.Path()
p_tree.moveTo(W - 80, 500)
p_tree.cubicTo(W - 240, 600, W - 320, 780, W - 220, 1100)
p_tree.lineTo(W, 1100)
p_tree.close()
cv_v.drawPath(p_tree, skia.Paint(Color=skia.ColorSetARGB(240, 12, 16, 26), AntiAlias=True))

# Stone Well Architecture
well_cx, well_cy = W / 2, 1380
p_well = skia.Path()
p_well.addOval(skia.Rect(well_cx - 260, well_cy - 120, well_cx + 260, well_cy + 120))
cv_v.drawPath(p_well, skia.Paint(Color=skia.ColorSetARGB(255, 32, 40, 58), AntiAlias=True))
# Stone well rim
cv_v.drawPath(p_well, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=22, Color=C_GOLD_AMBER, AntiAlias=True))
# Dark water center
p_water = skia.Path()
p_water.addOval(skia.Rect(well_cx - 220, well_cy - 90, well_cx + 220, well_cy + 90))
cv_v.drawPath(p_water, skia.Paint(Color=C_WELL_WATER, AntiAlias=True))

plate_village_img = surf_village.makeImageSnapshot()

print("Plates cached. Launching FFmpeg 60fps render pipeline...")

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
    "-crf", "20",
    "-pix_fmt", "yuv420p",
    "series_storybook/ep01/temp_video.mp4"
]

ffmpeg_proc = subprocess.Popen(
    ffmpeg_cmd,
    stdin=subprocess.PIPE,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

render_surf = skia.Surface(W, H)
cv = render_surf.getCanvas()

for frame_idx in range(TOTAL_FRAMES):
    t = frame_idx / FPS
    
    cv.drawImage(plate_village_img, 0, 0)
    
    # Scene Logic based on Blueprint:
    # 0.0 - 3.5s: Scene 1: Extreme Close-up of Dark Well Water + Eyes Opening
    # 3.5 - 9.0s: Scene 2: Ancient Book Opening / Camera dolly into village
    # 9.0 - 15.0s: Scene 3: Raghav bending over well reflection
    # 15.0 - 22.0s: Scene 4: Woman standing behind reflection
    # 22.0 - 26.0s: Scene 5 & 6: Ghost warning & Smiling Reflection
    # 26.0 - 27.2s: Scene 7: Page loop "तुम्हारा था"
    
    well_water_cx, well_water_cy = W / 2, 1380
    
    # Ripples in well water
    ripple_r = (frame_idx * 2) % 180
    cv.drawOval(
        skia.Rect(well_water_cx - ripple_r, well_water_cy - ripple_r * 0.45, well_water_cx + ripple_r, well_water_cy + ripple_r * 0.45),
        skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=2, Color=skia.ColorSetARGB(80, 140, 180, 220), AntiAlias=True)
    )
    
    if t < 3.5:
        # Scene 1: Impossible Hook - Push-in into Water reflection
        scale_cam = 1.0 + (t / 3.5) * 0.45
        cv.save()
        cv.translate(well_water_cx, well_water_cy - 450)
        cv.scale(scale_cam, scale_cam)
        
        # Face 1: Raghav
        cv.drawCircle(-70, 0, 65, skia.Paint(Color=skia.ColorSetARGB(200, 22, 30, 48), AntiAlias=True))
        # Face 2: Woman Reflection
        cv.drawCircle(70, -20, 60, skia.Paint(Color=skia.ColorSetARGB(220, 240, 240, 250), AntiAlias=True))
        # Woman Glowing Red Eyes
        cv.drawCircle(55, -24, 5, skia.Paint(Color=skia.ColorSetARGB(255, 255, 40, 40), AntiAlias=True))
        cv.drawCircle(85, -24, 5, skia.Paint(Color=skia.ColorSetARGB(255, 255, 40, 40), AntiAlias=True))
        
        # Face 3: The Viewer's Shadow (Silhouette)
        cv.drawCircle(0, 110, 80, skia.Paint(Color=skia.ColorSetARGB(180, 8, 10, 16), AntiAlias=True))
        cv.restore()
        
    elif t < 15.0:
        # Scene 2 & 3: Raghav bending over well (Over the shoulder)
        rx, ry = W / 2 - 140, 1100 + 4 * math.sin(t * 4.0)
        # Raghav Kurta & Bag Silhouette
        p_raghav = skia.Path()
        p_raghav.addRoundRect(skia.Rect(rx - 70, ry, rx + 70, ry + 240), 30, 30)
        cv.drawPath(p_raghav, skia.Paint(Color=skia.ColorSetARGB(255, 20, 26, 42), AntiAlias=True))
        # Golden Rim Light on Raghav's profile
        cv.drawPath(p_raghav, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=6, Color=C_GOLD_AMBER, AntiAlias=True))
        # Head
        cv.drawCircle(rx, ry - 55, 48, skia.Paint(Color=skia.ColorSetARGB(255, 24, 30, 48), AntiAlias=True))
        
    elif t < 22.0:
        # Scene 4: The Woman Standing Behind Him!
        rx, ry = W / 2 - 140, 1100
        # Raghav
        cv.drawCircle(rx, ry - 55, 48, skia.Paint(Color=skia.ColorSetARGB(255, 20, 26, 42), AntiAlias=True))
        
        # Pale Saree Ghost Woman behind him (Faded White)
        gx, gy = W / 2 + 120, 940
        p_ghost = skia.Path()
        p_ghost.moveTo(gx - 40, gy + 320)
        p_ghost.lineTo(gx - 20, gy)
        p_ghost.lineTo(gx + 20, gy)
        p_ghost.lineTo(gx + 40, gy + 320)
        p_ghost.close()
        cv.drawPath(p_ghost, skia.Paint(Color=skia.ColorSetARGB(230, 235, 238, 245), AntiAlias=True))
        cv.drawCircle(gx, gy - 35, 36, skia.Paint(Color=skia.ColorSetARGB(240, 245, 245, 255), AntiAlias=True))
        # Long hair
        cv.drawRect(skia.Rect(gx - 40, gy - 35, gx - 30, gy + 160), skia.Paint(Color=skia.ColorSetARGB(255, 10, 12, 18), AntiAlias=True))
        
    else:
        # Scene 5, 6, 7: Smiling Reflection Twist & Ancient Storybook Close
        # Extreme Close up of smiling water reflection
        cv.drawCircle(W / 2, 900, 180, skia.Paint(Color=skia.ColorSetARGB(240, 18, 24, 40), AntiAlias=True))
        # Sinister Red Smiling Curve
        smile_path = skia.Path()
        smile_path.moveTo(W / 2 - 70, 930)
        smile_path.quadTo(W / 2, 1020, W / 2 + 70, 930)
        cv.drawPath(smile_path, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=10, Color=C_CRIMSON, AntiAlias=True))
        # Glowing Eyes
        cv.drawCircle(W / 2 - 50, 860, 12, skia.Paint(Color=C_GOLD_AMBER, AntiAlias=True))
        cv.drawCircle(W / 2 + 50, 860, 12, skia.Paint(Color=C_GOLD_AMBER, AntiAlias=True))
        
        if t >= 25.5:
            # Page-turn border vignette closing in (Book Loop)
            book_prog = (t - 25.5) / 1.6
            vign_r = 1400 * (1.0 - book_prog)
            cv.drawRect(
                skia.Rect(0, 0, W, H),
                skia.Paint(
                    Shader=skia.GradientShader.MakeRadial(
                        (W / 2, H / 2), max(50, vign_r),
                        [skia.ColorSetARGB(0, 0, 0, 0), skia.ColorSetARGB(255, 6, 8, 14)],
                        [0.6, 1.0]
                    )
                )
            )

    # Ancient Storybook Header Pill
    header_w, header_h = 620, 72
    hx = (W - header_w) / 2
    cv.drawRoundRect(skia.Rect(hx, 50, hx + header_w, 50 + header_h), 18, 18, skia.Paint(Color=skia.ColorSetARGB(235, 12, 16, 28), AntiAlias=True))
    cv.drawRoundRect(skia.Rect(hx, 50, hx + header_w, 50 + header_h), 18, 18, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=3, Color=C_GOLD_AMBER, AntiAlias=True))

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

print("Video stream finished. Muxing master 60fps audio...")

mux_cmd = [
    "ffmpeg", "-y",
    "-i", "series_storybook/ep01/temp_video.mp4",
    "-i", "series_storybook/ep01/voice/ep01_final_audio.wav",
    "-c:v", "copy",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    "-movflags", "+faststart",
    "series_storybook/ep01/ep01_final.mp4"
]
subprocess.run(mux_cmd, check=True)
print("GROW10Z Storybook Episode 001 Complete! File: series_storybook/ep01/ep01_final.mp4")
