import os
import sys
import skia
from PIL import Image

sys.path.insert(0, ".")
from studio_ramayana.character_engine.cinematic_character_v2 import draw_cinematic_environment
from studio_ramayana.character_engine.ep006_visual_rigs import (
    draw_broken_pinaka_bow,
    draw_ancient_seismic_map,
    draw_bhagwan_parashurama,
    draw_cinematic_laxman
)

W, H = 1080, 1920
os.makedirs("studio_ramayana/episodes/ep006/styleframes", exist_ok=True)

def render_frame_to_png(draw_func, out_path):
    surface = skia.Surface(W, H)
    canvas = surface.getCanvas()
    draw_func(canvas)
    image = surface.makeImageSnapshot()
    image.save(out_path, skia.kPNG)
    print(f"✅ Rendered: {out_path}")

# Frame 1: Broken Pinaka Bow (Dhanush Bhang)
def f1(cv):
    draw_cinematic_environment(cv, "mithila_darbar", 1.5, W, H)
    draw_broken_pinaka_bow(cv, cx=540, cy=1380, scale=1.55, snap_offset=50.0)

# Frame 2: 3D Seismic Map (Mithila to Mount Mahendra)
def f2(cv):
    draw_ancient_seismic_map(cv, W, H, progress=0.85)

# Frame 3: Bhagwan Parashurama's Tempest Entrance
def f3(cv):
    draw_cinematic_environment(cv, "mithila_darbar", 22.0, W, H)
    draw_bhagwan_parashurama(cv, cx=540, cy=1120, scale=1.75, fury=1.0)

# Frame 4: Laxman's Defiant Smirk
def f4(cv):
    draw_cinematic_environment(cv, "mithila_darbar", 32.0, W, H)
    draw_cinematic_laxman(cv, cx=540, cy=1140, scale=1.75, smirk=1.0)

p1 = "studio_ramayana/episodes/ep006/styleframes/f1_broken_pinaka.png"
p2 = "studio_ramayana/episodes/ep006/styleframes/f2_seismic_map.png"
p3 = "studio_ramayana/episodes/ep006/styleframes/f3_parashurama_fury.png"
p4 = "studio_ramayana/episodes/ep006/styleframes/f4_laxman_defiance.png"

render_frame_to_png(f1, p1)
render_frame_to_png(f2, p2)
render_frame_to_png(f3, p3)
render_frame_to_png(f4, p4)

# Build a 2x2 Contact Sheet
cw, ch = 540, 960
sheet = Image.new("RGB", (cw * 2, ch * 2), (15, 12, 18))
sheet.paste(Image.open(p1).resize((cw, ch)), (0, 0))
sheet.paste(Image.open(p2).resize((cw, ch)), (cw, 0))
sheet.paste(Image.open(p3).resize((cw, ch)), (0, ch))
sheet.paste(Image.open(p4).resize((cw, ch)), (cw, ch))

sheet_out_local = "studio_ramayana/episodes/ep006/ep006_g3_contact_sheet.jpg"
sheet_out_art = "C:/Users/LENOVO/.gemini/antigravity/brain/f2ebddc4-8c1b-498e-b760-53e53a5b9bcf/ep006_g3_contact_sheet.jpg"

sheet.save(sheet_out_local, quality=94)
sheet.save(sheet_out_art, quality=94)
print("🎉 G3 Contact Sheet built successfully!")
