import time
import math
import skia
import sys
from pathlib import Path

BASE_DIR = Path(".").resolve()
sys.path.insert(0, str(BASE_DIR))

from studio_ramayana.character_engine.cinematic_character_v2 import (
    draw_sacred_pinaka_bow,
    draw_maharaja_janak,
    draw_cinematic_shri_ram
)

W, H = 1080, 1920
surf = skia.Surface(W, H)
canvas = surf.getCanvas()

# Benchmark character rigs
t0 = time.time()
for i in range(30):
    draw_sacred_pinaka_bow(canvas, 540, 1420, scale=1.55, glow=1.0)
print("Bow 30 frames:", time.time() - t0)

t0 = time.time()
for i in range(30):
    draw_maharaja_janak(canvas, 540, 1260, scale=1.9, agony=1.0, breathing=i/30.0)
print("Janak 30 frames:", time.time() - t0)

t0 = time.time()
for i in range(30):
    draw_cinematic_shri_ram(canvas, 420, 1180, scale=1.75, breathing=i/30.0)
print("Ram 30 frames:", time.time() - t0)
