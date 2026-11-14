import os, sys, json, math, subprocess
import numpy as np
import skia

W, H, FPS = 1080, 1920, 30
TOTAL_DUR = 43.01
TOTAL_FRAMES = int(TOTAL_DUR * FPS)  # 1290 frames

# Load caption events & pre-load as Skia Images
caption_events = json.load(open("out/ep01/captions/caption_events.json", encoding="utf-8"))
caption_cache = {}
for ev in caption_events:
    c_path = f"out/ep01/captions/{ev['chunk_id']}.png"
    if os.path.exists(c_path):
        caption_cache[ev["chunk_id"]] = skia.Image.open(c_path)

title_badge = skia.Image.open("out/ep01/captions/title_badge.png")
cliffhanger_badge = skia.Image.open("out/ep01/captions/cliffhanger_badge.png")

def C(r, g, b, a=255): return skia.ColorSetARGB(a, r, g, b)
def P(**k): return skia.Paint(AntiAlias=True, **k)
def lin(p0, p1, cols, pos=None): return skia.GradientShader.MakeLinear([p0, p1], cols, pos)
def rad(c, r, cols, pos=None): return skia.GradientShader.MakeRadial(c, r, cols, pos)
def blur(s): return skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, s)
def R(l, t, r, b): return skia.Rect.MakeLTRB(l, t, r, b)

# ================= PRE-RENDER PLATES & SPRITES =================

def make_plate_shot1():
    surf = skia.Surface(W, H); cv = surf.getCanvas()
    # Sky
    cv.drawRect(R(0, 0, W, H), P(Shader=lin((0, 0), (0, 1050), [C(5, 8, 26), C(18, 28, 68), C(70, 92, 135)], [0, 0.55, 1])))
    # Stars
    np.random.seed(42)
    sx = np.random.uniform(0, W, 220); sy = np.random.uniform(0, 950, 220)
    for i in range(220): cv.drawCircle(sx[i], sy[i], 1.5, P(Color=C(240, 245, 255, 180)))
    # Moon
    cv.drawCircle(760, 470, 240, P(Shader=rad((760, 470), 240, [C(190, 210, 255, 75), C(190, 210, 255, 0)]), MaskFilter=blur(25)))
    cv.drawCircle(760, 470, 130, P(Shader=lin((680, 390), (840, 550), [C(250, 246, 228), C(205, 210, 220)])))
    for (dx, dy, r, a) in [(-35, -25, 24, 35), (25, 35, 30, 30), (-15, 50, 16, 25), (50, -40, 18, 24)]:
        cv.drawCircle(760 + dx, 470 + dy, r, P(Color=C(140, 145, 160, a)))
    # Hills
    def hill(base, amp, fr, ph, col):
        p = skia.Path(); p.moveTo(0, H)
        for x in range(0, W + 10, 10): p.lineTo(x, base + amp * math.sin(x * fr + ph))
        p.lineTo(W, H); p.close(); cv.drawPath(p, P(Color=col))
    hill(930, 45, 0.005, 0.5, C(16, 26, 56))
    hill(980, 30, 0.008, 2.0, C(10, 16, 36))
    # Mist band
    cv.drawRect(R(0, 900, W, 1180), P(Shader=lin((0, 900), (0, 1180), [C(170, 190, 230, 0), C(170, 190, 230, 50), C(170, 190, 230, 0)], [0, 0.5, 1])))
    # Road
    cv.drawRect(R(0, 1000, W, H), P(Shader=lin((0, 1000), (0, H), [C(10, 16, 30), C(5, 8, 16)])))
    road = skia.Path()
    road.moveTo(525, 1000); road.lineTo(555, 1000); road.lineTo(1010, H); road.lineTo(70, H); road.close()
    cv.drawPath(road, P(Shader=lin((0, 1000), (0, H), [C(30, 34, 50), C(14, 16, 24)])))
    return surf.makeImageSnapshot()

def make_bus_sprite():
    surf = skia.Surface(1100, 450); cv = surf.getCanvas()
    # Headlight cone
    cone = skia.Path(); cone.moveTo(580, 182); cone.lineTo(1080, 90); cone.lineTo(1080, 410); cone.close()
    cv.drawPath(cone, P(Shader=lin((580, 182), (1080, 182), [C(255, 235, 170, 160), C(255, 235, 170, 0)]), MaskFilter=blur(14)))
    # Body shadow & base
    cv.drawRRect(skia.RRect.MakeRectXY(R(0, 4, 596, 230), 28, 28), P(Color=C(0, 0, 0, 110), MaskFilter=blur(14)))
    cv.drawRRect(skia.RRect.MakeRectXY(R(4, 6, 590, 224), 26, 26), P(Shader=lin((0, 6), (0, 224), [C(150, 48, 50), C(92, 26, 34)])))
    cv.drawRect(R(6, 158, 588, 176), P(Color=C(214, 196, 150)))
    # Windows
    for i in range(6):
        wx = 40 + i * 72
        cv.drawRRect(skia.RRect.MakeRectXY(R(wx - 4, 34, wx + 60, 116), 14, 14), P(Color=C(255, 205, 110, 110), MaskFilter=blur(10)))
        cv.drawRRect(skia.RRect.MakeRectXY(R(wx, 40, wx + 56, 110), 10, 10), P(Shader=lin((0, 40), (0, 110), [C(255, 226, 150), C(240, 170, 80)])))
    # Windshield & headlight
    cv.drawRRect(skia.RRect.MakeRectXY(R(514, 40, 576, 144), 12, 12), P(Shader=lin((0, 40), (0, 144), [C(210, 232, 255), C(120, 150, 190)])))
    cv.drawCircle(586, 186, 16, P(Color=C(255, 246, 200)))
    cv.drawCircle(586, 186, 45, P(Shader=rad((586, 186), 45, [C(255, 240, 180, 170), C(255, 240, 180, 0)])))
    # Wheels
    for cx in (130, 440):
        cv.drawCircle(cx, 230, 50, P(Color=C(10, 10, 14)))
        cv.drawCircle(cx, 230, 22, P(Color=C(80, 80, 92)))
        cv.drawCircle(cx, 230, 8, P(Color=C(30, 30, 36)))
    return surf.makeImageSnapshot()

def make_plate_shot2():
    surf = skia.Surface(W, H); cv = surf.getCanvas()
    cv.drawRect(R(0, 0, W, H), P(Shader=lin((0, 0), (0, H), [C(8, 12, 28), C(14, 18, 38)])))
    # Window
    cv.drawRRect(skia.RRect.MakeRectXY(R(120, 240, 960, 950), 36, 36), P(Shader=lin((0, 240), (0, 950), [C(10, 18, 48), C(25, 38, 80)])))
    cv.drawRRect(skia.RRect.MakeRectXY(R(120, 240, 960, 950), 36, 36), P(Color=C(35, 42, 65), Style=skia.Paint.kStroke_Style, StrokeWidth=18))
    # Lamp
    cv.drawCircle(540, 120, 18, P(Color=C(255, 230, 140)))
    cv.drawPath(skia.Path().moveTo(540, 120).lineTo(150, 1200).lineTo(930, 1200).close(),
                P(Shader=lin((540, 120), (540, 1200), [C(255, 210, 110, 45), C(255, 210, 110, 0)]), MaskFilter=blur(25)))
    return surf.makeImageSnapshot()

def make_plate_shot3():
    surf = skia.Surface(W, H); cv = surf.getCanvas()
    cv.drawRect(R(0, 0, W, H), P(Shader=lin((0, 0), (0, H), [C(6, 8, 16), C(16, 18, 30)])))
    # Amma arm
    cv.drawPath(skia.Path().moveTo(1080, 1100).quadTo(820, 1080, 680, 1050).lineTo(690, 1180).quadTo(840, 1200, 1080, 1220).close(), P(Color=C(10, 12, 20)))
    cv.drawPath(skia.Path().moveTo(1080, 1096).quadTo(820, 1076, 680, 1046), P(Color=C(255, 196, 120, 160), Style=skia.Paint.kStroke_Style, StrokeWidth=5, MaskFilter=blur(3)))
    # Rohan hand
    cv.drawPath(skia.Path().moveTo(0, 1180).quadTo(280, 1160, 420, 1140).lineTo(410, 1260).quadTo(270, 1280, 0, 1300).close(), P(Color=C(12, 14, 24)))
    cv.drawPath(skia.Path().moveTo(0, 1176).quadTo(280, 1156, 420, 1136), P(Color=C(255, 196, 120, 160), Style=skia.Paint.kStroke_Style, StrokeWidth=5, MaskFilter=blur(3)))
    return surf.makeImageSnapshot()

def make_tiffin_sprite():
    surf = skia.Surface(500, 500); cv = surf.getCanvas()
    tx, ty = 250, 250
    # Glow
    cv.drawCircle(tx, ty, 210, P(Shader=rad((tx, ty), 210, [C(255, 205, 80, 180), C(255, 160, 40, 70), C(255, 140, 20, 0)]), MaskFilter=blur(25)))
    for tier in range(3):
        by = ty - 80 + tier * 65
        cv.drawRRect(skia.RRect.MakeRectXY(R(tx - 110, by, tx + 110, by + 58), 16, 16),
                     P(Shader=lin((tx - 110, by), (tx + 110, by + 58), [C(255, 230, 140), C(220, 150, 45)])))
        cv.drawRect(R(tx - 112, by + 26, tx + 112, by + 32), P(Color=C(130, 75, 20)))
    handle = skia.Path(); handle.moveTo(tx - 90, ty - 80); handle.quadTo(tx, ty - 170, tx + 90, ty - 80)
    cv.drawPath(handle, P(Color=C(255, 235, 150), Style=skia.Paint.kStroke_Style, StrokeWidth=10))
    cv.drawPath(handle, P(Color=C(255, 200, 80, 180), Style=skia.Paint.kStroke_Style, StrokeWidth=16, MaskFilter=blur(6)))
    return surf.makeImageSnapshot()

def make_plate_shot5():
    surf = skia.Surface(W, H); cv = surf.getCanvas()
    cv.drawRect(R(0, 0, W, H), P(Shader=lin((0, 0), (0, 1100), [C(3, 5, 16), C(10, 18, 42), C(35, 48, 75)], [0, 0.6, 1])))
    # Moon
    cv.drawCircle(800, 380, 160, P(Shader=rad((800, 380), 160, [C(190, 210, 255, 60), C(190, 210, 255, 0)]), MaskFilter=blur(20)))
    cv.drawCircle(800, 380, 90, P(Shader=lin((740, 320), (860, 440), [C(245, 242, 225), C(195, 200, 210)])))
    cv.drawRect(R(0, 1050, W, H), P(Shader=lin((0, 1050), (0, H), [C(10, 14, 26), C(4, 6, 12)])))
    # Dead trees
    def dead_tree(tx, ty, sc):
        p = skia.Path(); p.moveTo(tx - 18 * sc, ty); p.lineTo(tx - 6 * sc, ty - 320 * sc)
        p.lineTo(tx - 80 * sc, ty - 460 * sc); p.lineTo(tx - 60 * sc, ty - 470 * sc)
        p.lineTo(tx - 2 * sc, ty - 350 * sc); p.lineTo(tx + 60 * sc, ty - 490 * sc)
        p.lineTo(tx + 75 * sc, ty - 480 * sc); p.lineTo(tx + 12 * sc, ty - 320 * sc)
        p.lineTo(tx + 22 * sc, ty); p.close()
        cv.drawPath(p, P(Color=C(4, 6, 12)))
    dead_tree(240, 1280, 1.1); dead_tree(680, 1340, 0.9); dead_tree(880, 1220, 1.2)
    # Mist
    for j in range(3):
        my = 1000 + j * 140
        cv.drawRect(R(0, my, W, my + 180),
                    P(Shader=lin((0, my), (0, my + 180), [C(160, 185, 220, 0), C(160, 185, 220, 75), C(160, 185, 220, 0)], [0, 0.5, 1]), MaskFilter=blur(18)))
    return surf.makeImageSnapshot()

print("Pre-rendering static background plates and asset sprites...", flush=True)
plate1 = make_plate_shot1()
sprite_bus = make_bus_sprite()
plate2 = make_plate_shot2()
plate3 = make_plate_shot3()
sprite_tiffin = make_tiffin_sprite()
plate5 = make_plate_shot5()
print("All plates pre-rendered into memory successfully!", flush=True)

# ================= RENDER SHOTS USING PRE-RENDERED PLATES =================

def render_shot1(cv, t):
    cv.drawImage(plate1, 0, 0)
    st = t
    # Moving dashed line
    for i in range(10):
        t0 = ((i / 10.0 + (st * 0.4) % 0.1)) ** 1.8
        t1 = (((i + 0.4) / 10.0 + (st * 0.4) % 0.1)) ** 1.8
        y0 = 1000 + t0 * 920; y1 = 1000 + t1 * 920
        w0 = 2 + t0 * 14; w1 = 2 + t1 * 14
        d = skia.Path()
        d.moveTo(540 - w0 / 2, y0); d.lineTo(540 + w0 / 2, y0); d.lineTo(540 + w1 / 2, y1); d.lineTo(540 - w1 / 2, y1); d.close()
        cv.drawPath(d, P(Color=C(200, 190, 150, 150)))
    # Moving bus
    bus_x = 40 + math.sin(st * 0.5) * 20
    cv.drawImage(sprite_bus, bus_x, 1250)
    # Title badge
    if st < 4.2:
        alpha = int(255 * min(1.0, st / 0.8) * max(0.0, (4.2 - st) / 0.8))
        if alpha > 10:
            paint = P(); paint.setAlpha(alpha)
            cv.drawImage(title_badge, 90, 220, skia.SamplingOptions(), paint)

def render_shot2(cv, t):
    cv.drawImage(plate2, 0, 0)
    st = t - 8.5
    # Scenery passing window
    for k in range(5):
        tx = (st * 450 + k * 280) % 1100 - 150
        cv.drawRect(R(960 - tx, 500, 980 - tx, 950), P(Color=C(5, 8, 18, 180)))
        cv.drawCircle(970 - tx, 500, 80, P(Color=C(5, 8, 18, 180)))
    
    shake_x = 0; shake_y = 0
    if 3.3 < st < 5.8:
        shake_x = math.sin(st * 45) * 4.0; shake_y = math.cos(st * 40) * 3.0
    cv.save(); cv.translate(shake_x, shake_y)
    
    # Rohan silhouette
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
    if st > 3.5: cv.drawCircle(375, 805, 5, P(Color=C(255, 255, 255, 240)))
    cv.drawRRect(skia.RRect.MakeRectXY(R(120, 1060, 240, 1360), 24, 24), P(Color=C(14, 18, 30)))
    
    # Amma silhouette
    a_pts = [(620, 1500), (660, 1180), (710, 1020), (770, 900), (870, 900), (940, 1020), (980, 1180), (1020, 1500)]
    ap_rim = skia.Path(); ap_rim.moveTo(a_pts[0][0]+6, a_pts[0][1])
    for pt in a_pts[1:]: ap_rim.lineTo(pt[0]+6, pt[1])
    ap_rim.close()
    cv.drawPath(ap_rim, P(Color=C(255, 196, 120, 140), MaskFilter=blur(4)))
    ap = skia.Path(); ap.moveTo(a_pts[0][0], a_pts[0][1])
    for pt in a_pts[1:]: ap.lineTo(pt[0], pt[1])
    ap.close(); cv.drawPath(ap, P(Color=C(8, 10, 18)))
    cv.drawCircle(820, 830, 105, P(Color=C(8, 10, 18)))
    cv.drawCircle(824, 830, 107, P(Color=C(255, 196, 120, 160), Style=skia.Paint.kStroke_Style, StrokeWidth=5, MaskFilter=blur(2)))
    cv.drawCircle(775, 825, 3, P(Color=C(255, 235, 180, 180)))
    cv.restore()

def render_shot3(cv, t):
    st = t - 18.5
    scale = 1.0 + 0.08 * (st / 8.3)
    cv.save(); cv.translate(540, 960); cv.scale(scale, scale); cv.translate(-540, -960)
    cv.drawImage(plate3, 0, 0)
    pulse = 1.0 + 0.05 * math.sin(st * 4.0)
    cv.save(); cv.translate(540, 1060); cv.scale(pulse, pulse); cv.drawImage(sprite_tiffin, -250, -250); cv.restore()
    # Embers
    for k in range(12):
        px = 540 + math.sin(st * 1.5 + k * 1.2) * (80 + k * 8)
        py = 1060 - 40 - (st * 35 + k * 25) % 240
        pa = int(180 * (1.0 - (1060 - py) / 280))
        cv.drawCircle(px, py, 2.5, P(Color=C(255, 230, 130, max(0, pa)), MaskFilter=blur(1.5)))
    cv.restore()

def render_shot4(cv, t):
    st = t - 26.8
    cv.drawRect(R(0, 0, W, H), P(Shader=lin((0, 0), (0, H), [C(5, 8, 20), C(12, 16, 32)])))
    door_open = min(1.0, max(0.0, (st - 0.4) / 1.2))
    cv.drawRect(R(260, 360, 820, 1580), P(Shader=lin((260, 360), (820, 1580), [C(2, 4, 10), C(8, 12, 24)])))
    fog_alpha = int(140 * door_open)
    if fog_alpha > 0:
        cv.drawRect(R(180, 1200, 900, 1650),
                    P(Shader=lin((0, 1200), (0, 1650), [C(180, 205, 240, 0), C(180, 205, 240, fog_alpha), C(180, 205, 240, 0)]), MaskFilter=blur(30)))
    door_w = 280 * (1.0 - door_open * 0.75)
    cv.drawRect(R(260, 360, 260 + door_w, 1580), P(Color=C(18, 24, 40)))
    cv.drawRect(R(820 - door_w, 360, 820, 1580), P(Color=C(18, 24, 40)))
    if st > 1.2:
        walk = min(1.0, (st - 1.2) / 4.0); ax = 540 + walk * 80; ay = 1100 + walk * 180; scale = 1.0 - walk * 0.28
        cv.save(); cv.translate(ax, ay); cv.scale(scale, scale)
        cv.drawCircle(0, -130, 85, P(Color=C(6, 8, 14)))
        cv.drawPath(skia.Path().moveTo(-120, 180).cubicTo(-100, -60, 100, -60, 120, 180).close(), P(Color=C(6, 8, 14)))
        cv.drawCircle(-3, -130, 87, P(Color=C(255, 196, 120, 140), Style=skia.Paint.kStroke_Style, StrokeWidth=4, MaskFilter=blur(2)))
        cv.restore()
    cv.drawPath(skia.Path().moveTo(60, 1920).lineTo(120, 1400).lineTo(240, 1250).lineTo(280, 1920).close(), P(Color=C(8, 10, 18)))
    cv.drawCircle(190, 1160, 80, P(Color=C(8, 10, 18)))
    cv.drawCircle(188, 1160, 82, P(Color=C(255, 196, 120, 150), Style=skia.Paint.kStroke_Style, StrokeWidth=4, MaskFilter=blur(2)))

def render_shot5(cv, t):
    st = t - 34.5
    scale = 1.0 + 0.12 * (st / 2.7)
    cv.save(); cv.translate(540, 960); cv.scale(scale, scale); cv.translate(-540, -960)
    cv.drawImage(plate5, 0, 0)
    cv.drawRect(R(0, 0, W, H), P(Shader=rad((540, 960), 900, [C(0, 0, 0, 0), C(0, 0, 0, 80), C(0, 0, 0, 240)], [0, 0.6, 1])))
    cv.restore()

def render_shot6(cv, t):
    st = t - 37.2
    render_shot5(cv, 37.0)
    cv.drawRect(R(0, 0, W, H), P(Color=C(4, 6, 14, 175)))
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
    print(f"Starting real-time Skia render of {TOTAL_FRAMES} frames ({TOTAL_DUR}s) at 30fps...", flush=True)
    
    temp_mp4 = "out/ep01/temp_video.mp4"
    audio_wav = "out/ep01/voice/ep01_final_audio.wav"
    out_mp4 = "out/ep01/ep01_final.mp4"
    
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
    
    log_file = open("out/ep01/ffmpeg_encode.log", "w")
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=log_file)
    
    surf = skia.Surface(W, H)
    canvas = surf.getCanvas()
    vignette_paint = P(Shader=rad((540, 960), 1250, [C(0, 0, 0, 0), C(0, 0, 0, 60), C(0, 0, 0, 195)], [0, 0.55, 1]))
    
    for frame_idx in range(TOTAL_FRAMES):
        t = frame_idx / float(FPS)
        canvas.clear(skia.ColorBLACK)
        
        if t < 8.5:
            render_shot1(canvas, t)
        elif t < 18.5:
            render_shot2(canvas, t)
        elif t < 26.8:
            render_shot3(canvas, t)
        elif t < 34.5:
            render_shot4(canvas, t)
        elif t < 37.2:
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
    print(f"Master short video complete! Saved: {out_mp4}", flush=True)

if __name__ == "__main__":
    main()
