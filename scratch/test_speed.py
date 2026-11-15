import time
import math
import skia
import numpy as np

W, H = 1080, 1920
surf = skia.Surface(W, H)
canvas = surf.getCanvas()

# 1. Just clear
t0 = time.time()
for _ in range(30):
    canvas.clear(skia.ColorBLACK)
print("Clear 30 frames:", time.time() - t0)

# 2. Draw pre-rendered snapshot
img_surf = skia.Surface(W, H)
snap = img_surf.makeImageSnapshot()
t0 = time.time()
for _ in range(30):
    canvas.drawImage(snap, 0, 0)
print("Draw Image 30 frames:", time.time() - t0)

# 3. Vignette
vignette_p = skia.Paint(
    Shader=skia.GradientShader.MakeRadial(
        skia.Point(W * 0.5, H * 0.5), H * 0.65,
        [skia.ColorTRANSPARENT, skia.ColorSetARGB(190, 8, 4, 12)],
        [0.6, 1.0]
    ),
    AntiAlias=True
)
t0 = time.time()
for _ in range(30):
    canvas.drawRect(skia.Rect(0, 0, W, H), vignette_p)
print("Vignette 30 frames:", time.time() - t0)

# 4. ReadPixels
pix_buf = bytearray(W * H * 4)
pix_info = skia.ImageInfo.Make(W, H, skia.kBGRA_8888_ColorType, skia.kPremul_AlphaType)
t0 = time.time()
for _ in range(30):
    surf.readPixels(pix_info, pix_buf, W * 4)
print("ReadPixels 30 frames:", time.time() - t0)
