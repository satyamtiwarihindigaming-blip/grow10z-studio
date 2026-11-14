import os, sys, json, math, subprocess
import numpy as np
import skia

W, H, FPS = 1080, 1920, 30
TOTAL_DUR = 48.15
TOTAL_FRAMES = int(TOTAL_DUR * FPS)  # 1444 frames

# Load caption events & pre-load as Skia Images
caption_events = json.load(open("out/ep02/captions/caption_events.json", encoding="utf-8"))
caption_cache = {}
for ev in caption_events:
    c_path = f"out/ep02/captions/{ev['chunk_id']}.png"
    if os.path.exists(c_path):
        caption_cache[ev["chunk_id"]] = skia.Image.open(c_path)

title_badge = skia.Image.open("out/ep02/captions/title_badge.png")
cliffhanger_badge = skia.Image.open("out/ep02/captions/cliffhanger_badge.png")
phone_badge = skia.Image.open("out/ep02/captions/phone_call_badge.png")

def C(r, g, b, a=255): return skia.ColorSetARGB(a, r, g, b)
def P(**k): return skia.Paint(AntiAlias=True, **k)
def lin(p0, p1, cols, pos=None): return skia.GradientShader.MakeLinear([p0, p1], cols, pos)
def rad(c, r, cols, pos=None): return skia.GradientShader.MakeRadial(c, r, cols, pos)
def blur(s): return skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, s)
def R(l, t, r, b): return skia.Rect.MakeLTRB(l, t, r, b)

# Pre-generate rain particles
np.random.seed(99)
NUM_RAIN = 180
rain_x = np.random.uniform(0, W + 300, NUM_RAIN)
rain_y = np.random.uniform(0, H, NUM_RAIN)
rain_speed = np.random.uniform(1100, 1700, NUM_RAIN)
rain_len = np.random.uniform(35, 65, NUM_RAIN)
rain_alpha = np.random.uniform(70, 160, NUM_RAIN)

def draw_rain(cv, t):
    p = P(Color=C(180, 210, 255, 120), Style=skia.Paint.kStroke_Style, StrokeWidth=2)
    # Slanted rain angle (dx = -12, dy = 45)
    for i in range(NUM_RAIN):
        cur_y = (rain_y[i] + t * rain_speed[i]) % (H + 100)
        cur_x = (rain_x[i] - t * (rain_speed[i] * 0.28)) % (W + 200) - 100
        cv.drawLine(cur_x, cur_y, cur_x - 12, cur_y + rain_len[i], p)

# ================= PRE-RENDER PLATES & SPRITES =================

def make_plate_storm_road():
    surf = skia.Surface(W, H); cv = surf.getCanvas()
    # Storm Sky
    cv.drawRect(R(0, 0, W, H), P(Shader=lin((0, 0), (0, 1100), [C(3, 5, 16), C(12, 18, 42), C(30, 42, 68)], [0, 0.55, 1])))
    # Moon muffled behind storm clouds
    cv.drawCircle(820, 390, 180, P(Shader=rad((820, 390), 180, [C(180, 200, 235, 45), C(180, 200, 235, 0)]), MaskFilter=blur(30)))
    # Road
    cv.drawRect(R(0, 1000, W, H), P(Shader=lin((0, 1000), (0, H), [C(8, 12, 24), C(4, 6, 14)])))
    road = skia.Path()
    road.moveTo(525, 1000); road.lineTo(555, 1000); road.lineTo(1020, H); road.lineTo(60, H); road.close()
    cv.drawPath(road, P(Shader=lin((0, 1000), (0, H), [C(24, 28, 42), C(10, 12, 20)])))
    # Wet road reflection shimmer
    cv.drawRect(R(480, 1020, 600, 1920), P(Shader=lin((0, 1020), (0, 1920), [C(100, 140, 200, 30), C(100, 140, 200, 10)]), MaskFilter=blur(25)))
    return surf.makeImageSnapshot()

def make_bus_sprite():
    surf = skia.Surface(1100, 450); cv = surf.getCanvas()
    cone = skia.Path(); cone.moveTo(580, 182); cone.lineTo(1080, 90); cone.lineTo(1080, 410); cone.close()
    cv.drawPath(cone, P(Shader=lin((580, 182), (1080, 182), [C(255, 235, 170, 160), C(255, 235, 170, 0)]), MaskFilter=blur(14)))
    cv.drawRRect(skia.RRect.MakeRectXY(R(0, 4, 596, 230), 28, 28), P(Color=C(0, 0, 0, 110), MaskFilter=blur(14)))
    cv.drawRRect(skia.RRect.MakeRectXY(R(4, 6, 590, 224), 26, 26), P(Shader=lin((0, 6), (0, 224), [C(150, 48, 50), C(92, 26, 34)])))
    cv.drawRect(R(6, 158, 588, 176), P(Color=C(214, 196, 150)))
    for i in range(6):
        wx = 40 + i * 72
        cv.drawRRect(skia.RRect.MakeRectXY(R(wx - 4, 34, wx + 60, 116), 14, 14), P(Color=C(255, 205, 110, 110), MaskFilter=blur(10)))
        cv.drawRRect(skia.RRect.MakeRectXY(R(wx, 40, wx + 56, 110), 10, 10), P(Shader=lin((0, 40), (0, 110), [C(255, 226, 150), C(240, 170, 80)])))
    cv.drawRRect(skia.RRect.MakeRectXY(R(514, 40, 576, 144), 12, 12), P(Shader=lin((0, 40), (0, 144), [C(210, 232, 255), C(120, 150, 190)])))
    cv.drawCircle(586, 186, 16, P(Color=C(255, 246, 200)))
    cv.drawCircle(586, 186, 45, P(Shader=rad((586, 186), 45, [C(255, 240, 180, 170), C(255, 240, 180, 0)])))
    for cx in (130, 440):
        cv.drawCircle(cx, 230, 50, P(Color=C(10, 10, 14)))
        cv.drawCircle(cx, 230, 22, P(Color=C(80, 80, 92)))
        cv.drawCircle(cx, 230, 8, P(Color=C(30, 30, 36)))
    return surf.makeImageSnapshot()

def make_plate_cabin():
    surf = skia.Surface(W, H); cv = surf.getCanvas()
    cv.drawRect(R(0, 0, W, H), P(Shader=lin((0, 0), (0, H), [C(8, 12, 26), C(14, 18, 36)])))
    # Window with dark rainy exterior
    cv.drawRRect(skia.RRect.MakeRectXY(R(120, 240, 960, 950), 36, 36), P(Shader=lin((0, 240), (0, 950), [C(6, 12, 32), C(18, 28, 55)])))
    cv.drawRRect(skia.RRect.MakeRectXY(R(120, 240, 960, 950), 36, 36), P(Color=C(32, 38, 58), Style=skia.Paint.kStroke_Style, StrokeWidth=18))
    # Dim amber lamp
    cv.drawCircle(540, 120, 18, P(Color=C(255, 230, 140)))
    cv.drawPath(skia.Path().moveTo(540, 120).lineTo(150, 1200).lineTo(930, 1200).close(),
                P(Shader=lin((540, 120), (540, 1200), [C(255, 210, 110, 40), C(255, 210, 110, 0)]), MaskFilter=blur(25)))
    return surf.makeImageSnapshot()

def make_tiffin_steaming_sprite():
    surf = skia.Surface(500, 500); cv = surf.getCanvas()
    tx, ty = 250, 250
    # Heat Aura (Red-orange boiling glow)
    cv.drawCircle(tx, ty, 220, P(Shader=rad((tx, ty), 220, [C(255, 140, 40, 200), C(255, 80, 20, 80), C(255, 40, 0, 0)]), MaskFilter=blur(28)))
    for tier in range(3):
        by = ty - 80 + tier * 65
        cv.drawRRect(skia.RRect.MakeRectXY(R(tx - 110, by, tx + 110, by + 58), 16, 16),
                     P(Shader=lin((tx - 110, by), (tx + 110, by + 58), [C(255, 235, 130), C(225, 130, 30)])))
        cv.drawRect(R(tx - 112, by + 26, tx + 112, by + 32), P(Color=C(150, 60, 15)))
    handle = skia.Path(); handle.moveTo(tx - 90, ty - 80); handle.quadTo(tx, ty - 170, tx + 90, ty - 80)
    cv.drawPath(handle, P(Color=C(255, 235, 150), Style=skia.Paint.kStroke_Style, StrokeWidth=10))
    cv.drawPath(handle, P(Color=C(255, 180, 60, 180), Style=skia.Paint.kStroke_Style, StrokeWidth=16, MaskFilter=blur(6)))
    return surf.makeImageSnapshot()

def make_plate_empty_driver_cabin():
    surf = skia.Surface(W, H); cv = surf.getCanvas()
    # Looking down the center aisle towards windshield
    cv.drawRect(R(0, 0, W, H), P(Shader=lin((0, 0), (0, H), [C(6, 10, 22), C(14, 18, 36)])))
    # Front windshield (large panoramic arch)
    cv.drawRRect(skia.RRect.MakeRectXY(R(180, 280, 900, 920), 40, 40), P(Shader=lin((0, 280), (0, 920), [C(4, 8, 20), C(12, 20, 45)])))
    cv.drawRRect(skia.RRect.MakeRectXY(R(180, 280, 900, 920), 40, 40), P(Color=C(28, 34, 52), Style=skia.Paint.kStroke_Style, StrokeWidth=20))
    # Wiper blades parked / moving
    cv.drawLine(360, 880, 490, 520, P(Color=C(15, 20, 30), Style=skia.Paint.kStroke_Style, StrokeWidth=8))
    cv.drawLine(720, 880, 850, 520, P(Color=C(15, 20, 30), Style=skia.Paint.kStroke_Style, StrokeWidth=8))
    # Dashboard console
    cv.drawRect(R(120, 920, 960, 1380), P(Shader=lin((0, 920), (0, 1380), [C(16, 20, 32), C(8, 10, 16)])))
    # Dashboard speedometer green/amber glow
    cv.drawCircle(380, 1040, 48, P(Color=C(20, 40, 60)))
    cv.drawCircle(380, 1040, 45, P(Shader=rad((380, 1040), 45, [C(40, 220, 150, 120), C(40, 220, 150, 0)]), MaskFilter=blur(6)))
    # Center aisle floor running into perspective
    aisle = skia.Path(); aisle.moveTo(420, 1380); aisle.lineTo(660, 1380); aisle.lineTo(820, H); aisle.lineTo(260, H); aisle.close()
    cv.drawPath(aisle, P(Color=C(12, 16, 28)))
    return surf.makeImageSnapshot()

print("Pre-rendering Episode 2 plates and assets...", flush=True)
plate_road = make_plate_storm_road()
sprite_bus = make_bus_sprite()
plate_cabin = make_plate_cabin()
sprite_tiffin = make_tiffin_steaming_sprite()
plate_driver_cabin = make_plate_empty_driver_cabin()
print("All Episode 2 plates cached successfully!", flush=True)

# ================= RENDER SCENES =================

def render_shot1(cv, t):
    cv.drawImage(plate_road, 0, 0)
    st = t
    # Moving dashed line
    for i in range(10):
        t0 = ((i / 10.0 + (st * 0.5) % 0.1)) ** 1.8
        t1 = (((i + 0.4) / 10.0 + (st * 0.5) % 0.1)) ** 1.8
        y0 = 1000 + t0 * 920; y1 = 1000 + t1 * 920
        w0 = 2 + t0 * 14; w1 = 2 + t1 * 14
        d = skia.Path()
        d.moveTo(540 - w0 / 2, y0); d.lineTo(540 + w0 / 2, y0); d.lineTo(540 + w1 / 2, y1); d.lineTo(540 - w1 / 2, y1); d.close()
        cv.drawPath(d, P(Color=C(200, 190, 150, 150)))
    # Moving bus in storm
    bus_x = 40 + math.sin(st * 0.6) * 15
    cv.drawImage(sprite_bus, bus_x, 1250)
    # Title badge (0 to 4.5s)
    if st < 4.5:
        alpha = int(255 * min(1.0, st / 0.8) * max(0.0, (4.5 - st) / 0.8))
        if alpha > 10:
            paint = P(); paint.setAlpha(alpha)
            cv.drawImage(title_badge, 90, 220, skia.SamplingOptions(), paint)
    draw_rain(cv, t)

def render_shot2(cv, t):
    # Inside cabin: Rohan holding steaming tiffin
    cv.drawImage(plate_cabin, 0, 0)
    st = t - 7.0
    # Scenery sliding past window
    for k in range(5):
        tx = (st * 500 + k * 260) % 1100 - 150
        cv.drawRect(R(960 - tx, 500, 980 - tx, 950), P(Color=C(4, 6, 14, 180)))
        cv.drawCircle(970 - tx, 500, 75, P(Color=C(4, 6, 14, 180)))
        
    # Rohan Silhouette (Left)
    r_pts = [(160, 1500), (170, 1150), (220, 1020), (280, 920), (380, 920), (440, 1020), (480, 1150), (500, 1500)]
    rp_rim = skia.Path(); rp_rim.moveTo(r_pts[0][0]-6, r_pts[0][1])
    for pt in r_pts[1:]: rp_rim.lineTo(pt[0]-6, pt[1])
    rp_rim.close()
    cv.drawPath(rp_rim, P(Color=C(255, 196, 120, 140), MaskFilter=blur(4)))
    rp = skia.Path(); rp.moveTo(r_pts[0][0], r_pts[0][1])
    for pt in r_pts[1:]: rp.lineTo(pt[0], pt[1])
    rp.close(); cv.drawPath(rp, P(Color=C(10, 14, 24)))
    cv.drawCircle(330, 820, 95, P(Color=C(10, 14, 24)))
    cv.drawCircle(326, 820, 97, P(Color=C(255, 196, 120, 160), Style=skia.Paint.kStroke_Style, StrokeWidth=5, MaskFilter=blur(2)))
    
    # Steaming boiling tiffin on Rohan's lap (Center-Right: 620, 1120)
    pulse = 1.0 + 0.05 * math.sin(st * 4.5)
    cv.save(); cv.translate(620, 1140); cv.scale(pulse, pulse); cv.drawImage(sprite_tiffin, -250, -250); cv.restore()
    
    # Steam rising from boiling tiffin
    for s_idx in range(16):
        sy = 1040 - (st * 45 + s_idx * 28) % 320
        sx = 620 + math.sin(st * 2.5 + s_idx * 1.5) * (30 + s_idx * 4)
        s_alpha = int(120 * (1.0 - (1040 - sy) / 340))
        cv.drawCircle(sx, sy, 14 + s_idx * 2, P(Color=C(240, 245, 255, max(0, s_alpha)), MaskFilter=blur(8)))
    draw_rain(cv, t)

def render_shot3(cv, t):
    # Close-up: Phone begins vibrating in pocket / phone screen illuminates Rohan
    cv.drawImage(plate_cabin, 0, 0)
    st = t - 15.0
    
    # Rohan startled silhouette
    cv.drawCircle(340, 780, 110, P(Color=C(10, 14, 24)))
    cv.drawCircle(336, 780, 112, P(Color=C(100, 160, 255, 180), Style=skia.Paint.kStroke_Style, StrokeWidth=5, MaskFilter=blur(3)))
    
    # Phone Vibration (Tremor oscillation)
    vib_x = math.sin(st * 70) * 6.0 if (0.5 < st < 2.5 or 3.2 < st < 5.2) else 0.0
    vib_y = math.cos(st * 65) * 5.0 if (0.5 < st < 2.5 or 3.2 < st < 5.2) else 0.0
    
    cv.save()
    cv.translate(620 + vib_x, 980 + vib_y)
    # Phone screen glow aura
    cv.drawCircle(180, 310, 260, P(Shader=rad((180, 310), 260, [C(80, 160, 255, 120), C(80, 160, 255, 0)]), MaskFilter=blur(25)))
    cv.drawImage(phone_badge, 0, 0)
    cv.restore()
    draw_rain(cv, t)

def render_shot4(cv, t):
    # Phone call / Sudden Lightning Flash at 23.0s
    st = t - 21.0
    cv.drawImage(plate_cabin, 0, 0)
    
    # Lightning flash effect (between t = 22.8s and 23.2s => st: 1.8 to 2.2s)
    is_lightning = (1.8 <= st <= 2.05) or (2.12 <= st <= 2.22)
    if is_lightning:
        # Flash the entire cabin in silver-white
        cv.drawRect(R(0, 0, W, H), P(Color=C(240, 245, 255, 220)))
        # Stark black silhouettes cast across cabin
        cv.drawRect(R(180, 300, 920, 920), P(Color=C(255, 255, 255, 255)))
        
    # Rohan with phone pressed to ear
    cv.drawCircle(440, 800, 105, P(Color=C(10, 14, 24)))
    # Blue screen bounce light
    cv.drawCircle(430, 800, 107, P(Color=C(100, 160, 255, 160), Style=skia.Paint.kStroke_Style, StrokeWidth=5, MaskFilter=blur(2)))
    # Shocked eye highlight
    cv.drawCircle(485, 785, 6, P(Color=C(255, 255, 255, 240)))
    cv.drawCircle(485, 785, 2, P(Color=C(10, 15, 30)))
    draw_rain(cv, t)

def render_shot5(cv, t):
    # Empty Driver Cabin: Steering wheel turning on its own
    st = t - 31.0
    scale = 1.0 + 0.08 * (st / 6.0)
    cv.save(); cv.translate(540, 960); cv.scale(scale, scale); cv.translate(-540, -960)
    cv.drawImage(plate_driver_cabin, 0, 0)
    
    # Steering wheel turning autonomously (at 420, 1000)
    steer_x, steer_y = 420, 1020
    wheel_rot = math.sin(st * 3.0) * 45.0  # rotates ±45 degrees
    
    cv.save()
    cv.translate(steer_x, steer_y)
    cv.rotate(wheel_rot)
    # Big bus steering wheel rim
    cv.drawCircle(0, 0, 110, P(Color=C(22, 28, 42), Style=skia.Paint.kStroke_Style, StrokeWidth=18))
    cv.drawCircle(0, 0, 112, P(Color=C(100, 140, 200, 120), Style=skia.Paint.kStroke_Style, StrokeWidth=3, MaskFilter=blur(2)))
    # Center hub & spokes
    cv.drawCircle(0, 0, 32, P(Color=C(15, 20, 30)))
    cv.drawLine(-100, 0, 100, 0, P(Color=C(20, 26, 38), Style=skia.Paint.kStroke_Style, StrokeWidth=12))
    cv.drawLine(0, 0, 0, 100, P(Color=C(20, 26, 38), Style=skia.Paint.kStroke_Style, StrokeWidth=12))
    cv.restore()
    
    # Empty Driver Seat (Nobody sitting in it!)
    cv.drawRRect(skia.RRect.MakeRectXY(R(640, 720, 840, 1280), 30, 30), P(Color=C(10, 14, 24)))
    cv.drawRRect(skia.RRect.MakeRectXY(R(640, 720, 840, 1280), 30, 30), P(Color=C(60, 80, 120, 100), Style=skia.Paint.kStroke_Style, StrokeWidth=3, MaskFilter=blur(2)))
    
    cv.restore()
    draw_rain(cv, t)

def render_shot6(cv, t):
    # Cliffhanger Card & CTA
    st = t - 37.0
    render_shot5(cv, 37.0)
    cv.drawRect(R(0, 0, W, H), P(Color=C(4, 6, 14, 180)))
    
    pulse = 1.0 + 0.02 * math.sin(st * 3.5)
    cv.save(); cv.translate(540, 780); cv.scale(pulse, pulse)
    cv.drawImage(cliffhanger_badge, -480, -170)
    cv.restore()

# ================= MAIN RENDER PIPELINE =================

def get_active_caption(t):
    for ev in caption_events:
        if ev["start"] <= t <= ev["end"]:
            return caption_cache.get(ev["chunk_id"])
    return None

def main():
    print(f"Starting real-time Skia render of Episode 2: {TOTAL_FRAMES} frames ({TOTAL_DUR}s) at 30fps...", flush=True)
    
    temp_mp4 = "out/ep02/temp_video.mp4"
    audio_wav = "out/ep02/voice/ep02_final_audio.wav"
    out_mp4 = "out/ep02/ep02_final.mp4"
    
    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{W}x{H}",
        "-pix_fmt", "rgba",
        "-r", str(FPS),
        "-i", "-",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "19",
        "-pix_fmt", "yuv420p",
        temp_mp4
    ]
    
    log_file = open("out/ep02/ffmpeg_encode.log", "w")
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=log_file)
    
    surf = skia.Surface(W, H)
    canvas = surf.getCanvas()
    vignette_paint = P(Shader=rad((540, 960), 1250, [C(0, 0, 0, 0), C(0, 0, 0, 60), C(0, 0, 0, 195)], [0, 0.55, 1]))
    
    for frame_idx in range(TOTAL_FRAMES):
        t = frame_idx / float(FPS)
        canvas.clear(skia.ColorBLACK)
        
        if t < 7.0:
            render_shot1(canvas, t)
        elif t < 15.0:
            render_shot2(canvas, t)
        elif t < 21.0:
            render_shot3(canvas, t)
        elif t < 31.0:
            render_shot4(canvas, t)
        elif t < 37.0:
            render_shot5(canvas, t)
        else:
            render_shot6(canvas, t)
            
        canvas.drawRect(R(0, 0, W, H), vignette_paint)
        
        cap_img = get_active_caption(t)
        if cap_img is not None:
            cx = (W - cap_img.width()) // 2
            cy = 1530
            canvas.drawImage(cap_img, cx, cy)
            
        raw_bytes = surf.makeImageSnapshot().tobytes()
        proc.stdin.write(raw_bytes)
        
        if frame_idx % 150 == 0 or frame_idx == TOTAL_FRAMES - 1:
            print(f"Rendered frame {frame_idx}/{TOTAL_FRAMES} ({frame_idx/TOTAL_FRAMES*100:.1f}%) [t={t:.2f}s]", flush=True)
            
    proc.stdin.close()
    proc.wait()
    log_file.close()
    print("Video stream finished. Muxing master audio track...", flush=True)
    
    mux_cmd = [
        "ffmpeg", "-y",
        "-i", temp_mp4,
        "-i", audio_wav,
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        "-movflags", "+faststart",
        out_mp4
    ]
    subprocess.run(mux_cmd, check=True)
    if os.path.exists(temp_mp4):
        try: os.remove(temp_mp4)
        except: pass
    print(f"Episode 2 master short video complete! Saved: {out_mp4}", flush=True)

if __name__ == "__main__":
    main()
