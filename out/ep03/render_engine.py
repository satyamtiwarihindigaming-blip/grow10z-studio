import os, sys, math, json, subprocess
import skia
import numpy as np

# Total video parameters
W, H = 1080, 1920
FPS = 30
DUR = 59.75
TOTAL_FRAMES = int(DUR * FPS)  # 1792 frames

# Colors (Graphic novel night palette)
C_SKY_TOP = skia.ColorSetARGB(255, 4, 6, 18)
C_SKY_MID = skia.ColorSetARGB(255, 14, 22, 54)
C_SKY_BOT = skia.ColorSetARGB(255, 45, 65, 110)
C_AMBER = skia.ColorSetARGB(255, 255, 196, 70)
C_GLOW = skia.ColorSetARGB(180, 255, 210, 100)
C_CABIN_BG = skia.ColorSetARGB(255, 12, 16, 26)
C_CABIN_FLOOR = skia.ColorSetARGB(255, 8, 10, 16)
C_SPEEDO_BG = skia.ColorSetARGB(255, 18, 24, 38)

# Load caption events
with open("out/ep03/caption_events.json", "r", encoding="utf-8") as f:
    caption_events = json.load(f)

# Load caption sprites into Skia images
caption_sprites = {}
for ev in caption_events:
    p = ev["png"]
    if os.path.exists(p):
        caption_sprites[ev["id"]] = skia.Image.open(p)

# Pre-render 1: High-Speed Night Road Plate (with wet asphalt reflections)
surf_road = skia.Surface(W, H)
cv_road = surf_road.getCanvas()

# Sky
sky_grad = skia.GradientShader.MakeLinear([(0, 0), (0, 850)], [C_SKY_TOP, C_SKY_MID, C_SKY_BOT], [0.0, 0.6, 1.0])
cv_road.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Shader=sky_grad))

# Distant Hills
hill_path = skia.Path()
hill_path.moveTo(0, H)
for x in range(0, W + 10, 10):
    hill_path.lineTo(x, 780 + 35 * math.sin(x * 0.007) + 20 * math.sin(x * 0.015))
hill_path.lineTo(W, H)
hill_path.close()
cv_road.drawPath(hill_path, skia.Paint(AntiAlias=True, Color=skia.ColorSetARGB(255, 10, 15, 32)))

# Mist band
mist_paint = skia.Paint(
    Shader=skia.GradientShader.MakeLinear(
        [(0, 750), (0, 950)],
        [skia.ColorSetARGB(0, 150, 180, 220), skia.ColorSetARGB(70, 150, 180, 220), skia.ColorSetARGB(0, 150, 180, 220)],
        [0.0, 0.5, 1.0]
    )
)
cv_road.drawRect(skia.Rect(0, 750, W, 950), mist_paint)

# Road ground
road_ground = skia.GradientShader.MakeLinear([(0, 880), (0, H)], [skia.ColorSetARGB(255, 10, 12, 18), skia.ColorSetARGB(255, 4, 6, 10)], [0.0, 1.0])
cv_road.drawRect(skia.Rect(0, 880, W, H), skia.Paint(Shader=road_ground))

# Asphalt road perspective
road_p = skia.Path()
road_p.moveTo(W / 2 - 35, 880)
road_p.lineTo(W / 2 + 35, 880)
road_p.lineTo(W + 180, H)
road_p.lineTo(-180, H)
road_p.close()
cv_road.drawPath(road_p, skia.Paint(AntiAlias=True, Color=skia.ColorSetARGB(255, 24, 28, 38)))

plate_road_img = surf_road.makeImageSnapshot()

# Pre-render 2: Bus Driver Cabin Plate (Empty driver seat, windshield, dashboard)
surf_cabin = skia.Surface(W, H)
cv_cabin = surf_cabin.getCanvas()

# Cabin darkness
cv_cabin.drawRect(skia.Rect(0, 0, W, H), skia.Paint(Color=C_CABIN_BG))

# Front Large Windshield
ws_rect = skia.Rect(60, 260, W - 60, 1020)
ws_path = skia.Path()
ws_path.addRoundRect(ws_rect, 30, 30)
# Dark rainy outside seen through glass
cv_cabin.drawPath(ws_path, skia.Paint(AntiAlias=True, Color=skia.ColorSetARGB(255, 8, 12, 22)))

# Headlights projected on road through windshield
hl_path = skia.Path()
hl_path.moveTo(W / 2 - 40, 680)
hl_path.lineTo(W / 2 + 40, 680)
hl_path.lineTo(W - 40, 1020)
hl_path.lineTo(40, 1020)
hl_path.close()
hl_paint = skia.Paint(
    AntiAlias=True,
    Shader=skia.GradientShader.MakeLinear(
        [(W / 2, 680), (W / 2, 1020)],
        [skia.ColorSetARGB(180, 255, 240, 160), skia.ColorSetARGB(0, 255, 230, 100)],
        [0.0, 1.0]
    )
)
cv_cabin.drawPath(hl_path, hl_paint)

# Windshield frame pillars
pillar_paint = skia.Paint(AntiAlias=True, Color=skia.ColorSetARGB(255, 18, 22, 34))
cv_cabin.drawRect(skia.Rect(0, 0, 80, H), pillar_paint)
cv_cabin.drawRect(skia.Rect(W - 80, 0, W, H), pillar_paint)
cv_cabin.drawRect(skia.Rect(0, 0, W, 270), pillar_paint)
# Center dividing wiper post
cv_cabin.drawRect(skia.Rect(W / 2 - 12, 260, W / 2 + 12, 1020), pillar_paint)

# Driver dashboard console
dash_paint = skia.Paint(AntiAlias=True, Color=skia.ColorSetARGB(255, 15, 18, 28))
dash_path = skia.Path()
dash_path.moveTo(0, 1000)
dash_path.lineTo(W, 1000)
dash_path.lineTo(W, H)
dash_path.lineTo(0, H)
dash_path.close()
cv_cabin.drawPath(dash_path, dash_paint)

# Empty Driver Seat (Prominent high back silhouette on the right side)
seat_paint = skia.Paint(AntiAlias=True, Color=skia.ColorSetARGB(255, 22, 26, 38))
seat_path = skia.Path()
# Headrest
seat_path.addRoundRect(skia.Rect(W / 2 + 90, 640, W / 2 + 250, 750), 20, 20)
# Backrest
seat_path.addRoundRect(skia.Rect(W / 2 + 70, 760, W / 2 + 270, 1080), 25, 25)
cv_cabin.drawPath(seat_path, seat_paint)

# Yellow/Amber Rim light on empty seat (Highlights that nobody is sitting here!)
rim_paint = skia.Paint(
    AntiAlias=True,
    Style=skia.Paint.kStroke_Style,
    StrokeWidth=6,
    Color=skia.ColorSetARGB(200, 255, 196, 80),
    MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 3)
)
cv_cabin.drawPath(seat_path, rim_paint)

plate_cabin_img = surf_cabin.makeImageSnapshot()

print("Ep 03 Plates rendered. Starting FFmpeg pipeline...")

# Fast FFmpeg H.264 pipe
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
    "-crf", "22",
    "-pix_fmt", "yuv420p",
    "out/ep03/temp_video.mp4"
]

ffmpeg_proc = subprocess.Popen(
    ffmpeg_cmd,
    stdin=subprocess.PIPE,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

render_surf = skia.Surface(W, H)
cv = render_surf.getCanvas()

# Rain drop coordinates
rng = np.random.default_rng(101)
rain_x = rng.uniform(0, W, 180)
rain_y = rng.uniform(0, H, 180)
rain_s = rng.uniform(25, 55, 180)

# Speedo Center
SP_CX, SP_CY, SP_R = W / 2 - 180, 1220, 140

for frame_idx in range(TOTAL_FRAMES):
    t = frame_idx / FPS
    
    # Scene Switch Logic
    # 0.0 - 15.0s: Exterior High-Speed Road & Bus Pursuit (Camera push-in)
    # 15.0 - 36.0s: Raghav running through dark cabin aisle
    # 36.0 - 60.0s: The Driver Cabin Reveal (Empty seat, spinning wheel, 120 km/h)
    
    if t < 15.0:
        # Scene 1: Exterior Speeding Bus
        cv.drawImage(plate_road_img, 0, 0)
        
        # Fast moving lane stripes
        lane_speed = (frame_idx * 26) % 360
        for i in range(8):
            d_pos = ((i * 120 + lane_speed) % 960) / 960.0
            y_pos = 880 + (d_pos ** 2.2) * 1040
            w_pos = 4 + d_pos * 24
            h_pos = 10 + d_pos * 60
            cv.drawRect(
                skia.Rect(W / 2 - w_pos / 2, y_pos, W / 2 + w_pos / 2, y_pos + h_pos),
                skia.Paint(Color=skia.ColorSetARGB(180, 240, 230, 180))
            )
            
        # Bus Silhouette rushing forward
        bus_w, bus_h = 420, 240
        bx = W / 2 - bus_w / 2 + 15 * math.sin(t * 8.0)  # road sway
        by = 1040 + 8 * math.cos(t * 12.0)
        
        # Red Tail-lights trails
        trail_paint = skia.Paint(Color=skia.ColorSetARGB(220, 255, 20, 30), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 8))
        cv.drawCircle(bx + 40, by + bus_h - 40, 22, trail_paint)
        cv.drawCircle(bx + bus_w - 40, by + bus_h - 40, 22, trail_paint)
        
        # Bus Body
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect(bx, by, bx + bus_w, by + bus_h), 25, 25), skia.Paint(AntiAlias=True, Color=skia.ColorSetARGB(255, 14, 18, 30)))
        # Bus Roof Warning Light
        cv.drawCircle(W / 2, by + 10, 12, skia.Paint(Color=skia.ColorSetARGB(240, 255, 160, 20), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 6)))
        
    else:
        # Scene 2 & 3: Inside Front Cabin
        cv.drawImage(plate_cabin_img, 0, 0)
        
        # Camera Handheld Panic Shake (t > 15)
        shake_x = 4.0 * math.sin(t * 22.0)
        shake_y = 3.0 * math.cos(t * 26.0)
        
        # 1. Self-Spinning Ghost Steering Wheel (Left side of cabin)
        wheel_cx = W / 2 - 180 + shake_x
        wheel_cy = 980 + shake_y
        wheel_rot = (frame_idx * 14.0) % 360  # Rapidly turning on its own!
        
        cv.save()
        cv.translate(wheel_cx, wheel_cy)
        cv.rotate(wheel_rot)
        
        # Outer Wheel Ring
        cv.drawCircle(0, 0, 110, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=18, Color=skia.ColorSetARGB(255, 28, 32, 45), AntiAlias=True))
        # Center Hub
        cv.drawCircle(0, 0, 38, skia.Paint(Color=skia.ColorSetARGB(255, 20, 24, 34), AntiAlias=True))
        # 3 Spokes
        for ang in [0, 120, 240]:
            rad = math.radians(ang)
            cv.drawLine(0, 0, 100 * math.cos(rad), 100 * math.sin(rad), skia.Paint(StrokeWidth=14, Color=skia.ColorSetARGB(255, 26, 30, 42), AntiAlias=True))
            
        # Ghostly Cyan Glow around the spinning steering wheel
        cv.drawCircle(0, 0, 115, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=8, Color=skia.ColorSetARGB(140, 0, 220, 255), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 10)))
        cv.restore()
        
        # 2. Pulsing Speedometer (Dial showing 100 -> 120 km/h)
        # Dial Background
        cv.drawCircle(SP_CX, SP_CY, SP_R, skia.Paint(Color=C_SPEEDO_BG, AntiAlias=True))
        cv.drawCircle(SP_CX, SP_CY, SP_R, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=6, Color=skia.ColorSetARGB(255, 255, 50, 50), AntiAlias=True))
        
        # Dial numbers & tick marks
        for deg in range(135, 405, 30):
            r_ang = math.radians(deg)
            x1 = SP_CX + (SP_R - 24) * math.cos(r_ang)
            y1 = SP_CY + (SP_R - 24) * math.sin(r_ang)
            x2 = SP_CX + (SP_R - 8) * math.cos(r_ang)
            y2 = SP_CY + (SP_R - 8) * math.sin(r_ang)
            cv.drawLine(x1, y1, x2, y2, skia.Paint(StrokeWidth=4, Color=skia.ColorWHITE, AntiAlias=True))
            
        # Shaking Speedo Needle (jittering at 120 km/h danger zone)
        needle_jitter = 3.5 * math.sin(t * 35.0)
        needle_deg = 350 + needle_jitter  # points near 120 km/h redline
        n_rad = math.radians(needle_deg)
        nx = SP_CX + (SP_R - 20) * math.cos(n_rad)
        ny = SP_CY + (SP_R - 20) * math.sin(n_rad)
        cv.drawLine(SP_CX, SP_CY, nx, ny, skia.Paint(StrokeWidth=6, Color=skia.ColorSetARGB(255, 255, 30, 30), AntiAlias=True))
        cv.drawCircle(SP_CX, SP_CY, 14, skia.Paint(Color=skia.ColorSetARGB(255, 255, 200, 200), AntiAlias=True))
        
        # 3. Rear-view Mirror at top (Reveals White Shawl Old Woman staring at t > 46s)
        mirror_rect = skia.Rect(W / 2 - 190, 80, W / 2 + 190, 220)
        cv.drawRRect(skia.RRect.MakeRectXY(mirror_rect, 20, 20), skia.Paint(Color=skia.ColorSetARGB(255, 22, 28, 40), AntiAlias=True))
        cv.drawRRect(skia.RRect.MakeRectXY(mirror_rect, 20, 20), skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=4, Color=skia.ColorSetARGB(255, 80, 95, 125)))
        
        if t >= 46.0:
            # Ghostly Woman Silhouette in Mirror
            cv.drawCircle(W / 2, 140, 32, skia.Paint(Color=skia.ColorSetARGB(240, 240, 245, 255), AntiAlias=True))  # Pale Head
            # Red glowing eyes
            cv.drawCircle(W / 2 - 10, 138, 4, skia.Paint(Color=skia.ColorSetARGB(255, 255, 30, 30), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 2)))
            cv.drawCircle(W / 2 + 10, 138, 4, skia.Paint(Color=skia.ColorSetARGB(255, 255, 30, 30), MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 2)))
            # White Shawl
            cv.drawCircle(W / 2, 210, 65, skia.Paint(Color=skia.ColorSetARGB(220, 230, 235, 245), AntiAlias=True))

    # Dynamic Rain Droplets Layer across screen
    rain_y = (rain_y + rain_s) % H
    rain_paint = skia.Paint(StrokeWidth=2.5, Color=skia.ColorSetARGB(110, 200, 225, 255), AntiAlias=True)
    for rx, ry, rs in zip(rain_x, rain_y, rain_s):
        cv.drawLine(rx, ry, rx - 3, ry + rs * 0.7, rain_paint)
        
    # Top Header Series Pill Badge
    pill_w, pill_h = 560, 68
    px = (W - pill_w) / 2
    cv.drawRoundRect(skia.Rect(px, 30, px + pill_w, 30 + pill_h), 20, 20, skia.Paint(Color=skia.ColorSetARGB(230, 8, 12, 22), AntiAlias=True))
    cv.drawRoundRect(skia.Rect(px, 30, px + pill_w, 30 + pill_h), 20, 20, skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=3, Color=skia.ColorSetARGB(255, 255, 60, 60), AntiAlias=True))

    # Burned-In Devanagari Caption Sprites
    for ev in caption_events:
        if ev["start"] <= t <= ev["end"]:
            sp = caption_sprites.get(ev["id"])
            if sp:
                cx = (W - sp.width()) / 2
                cy = 1380
                cv.drawImage(sp, cx, cy)
            break

    # Send raw bytes to FFmpeg (BGRA)
    img = render_surf.makeImageSnapshot()
    raw_bytes = img.tobytes()
    ffmpeg_proc.stdin.write(raw_bytes)

ffmpeg_proc.stdin.close()
ffmpeg_proc.wait()
print("Episode 3 raw video rendered. Muxing master audio...")

# Final audio mux
mux_cmd = [
    "ffmpeg", "-y",
    "-i", "out/ep03/temp_video.mp4",
    "-i", "out/ep03/voice/ep03_final_audio.wav",
    "-c:v", "copy",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    "-movflags", "+faststart",
    "out/ep03/ep03_final.mp4"
]
subprocess.run(mux_cmd, check=True)
print("Episode 3 complete: out/ep03/ep03_final.mp4")
