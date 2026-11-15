import time
import skia
import sys
from pathlib import Path

BASE_DIR = Path(".").resolve()
sys.path.insert(0, str(BASE_DIR))

from studio_ramayana.character_engine.cinematic_character_v2 import (
    draw_sacred_pinaka_bow,
    draw_maharaja_janak,
    draw_cinematic_shri_ram,
    draw_cinematic_vishwamitra
)

W, H = 1080, 1920

# Pre-render snapshots
t0 = time.time()

# 1. Vignette
vig_surf = skia.Surface(W, H)
vcv = vig_surf.getCanvas()
vig_paint = skia.Paint(
    Shader=skia.GradientShader.MakeRadial(
        skia.Point(W * 0.5, H * 0.5), H * 0.65,
        [skia.ColorTRANSPARENT, skia.ColorSetARGB(190, 8, 4, 12)],
        [0.6, 1.0]
    ),
    AntiAlias=True
)
vcv.drawRect(skia.Rect(0, 0, W, H), vig_paint)
vig_snap = vig_surf.makeImageSnapshot()

# 2. Ram Idle Pose
ram_surf = skia.Surface(1080, 1920)
rcv = ram_surf.getCanvas()
draw_cinematic_shri_ram(rcv, 540, 1180, scale=1.75, breathing=0.0, bow_draw=0.0)
ram_idle_snap = ram_surf.makeImageSnapshot()

# 3. Janak Agony Pose
janak_surf = skia.Surface(1080, 1920)
jcv = janak_surf.getCanvas()
draw_maharaja_janak(jcv, 540, 1260, scale=1.9, agony=1.0, breathing=0.0)
janak_snap = janak_surf.makeImageSnapshot()

# 4. Bow Pose
bow_surf = skia.Surface(1080, 1920)
bcv = bow_surf.getCanvas()
draw_sacred_pinaka_bow(bcv, 540, 1420, scale=1.65, glow=1.5)
bow_snap = bow_surf.makeImageSnapshot()

t_prep = time.time() - t0
print(f"Pre-rendered all character snapshots in: {t_prep:.2f}s")

# Now benchmark 300 frames of composing these snapshots
surf = skia.Surface(W, H)
canvas = surf.getCanvas()

t1 = time.time()
for i in range(300):
    canvas.clear(skia.ColorBLACK)
    canvas.drawImage(bow_snap, 0, 0)
    canvas.drawImage(ram_idle_snap, 0, 0)
    canvas.drawImage(vig_snap, 0, 0)
t_render = time.time() - t1
print(f"300 frames rendered in: {t_render:.3f}s -> {300/t_render:.1f} FPS!!")
