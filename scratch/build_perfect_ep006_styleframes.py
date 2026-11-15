import os
import sys
import skia
from PIL import Image

sys.path.insert(0, ".")
from studio_ramayana.character_engine.cinematic_character_v2 import draw_cinematic_environment
from studio_ramayana.character_engine.ep006_visual_rigs import draw_broken_pinaka_bow
from scratch.test_real_map import draw_real_india_map
from scratch.test_full_body_characters import draw_full_body_parashurama, draw_full_body_laxman

W, H = 1080, 1920
out_dir = "studio_ramayana/episodes/ep006/styleframes"
os.makedirs(out_dir, exist_ok=True)

# 1. Frame 1: Broken Pinaka Bow
s1 = skia.Surface(W, H)
cv1 = s1.getCanvas()
draw_cinematic_environment(cv1, "mithila_darbar", 1.5, W, H)
draw_broken_pinaka_bow(cv1, cx=540, cy=1380, scale=1.55, snap_offset=50.0)
p1 = os.path.join(out_dir, "f1_broken_pinaka.png")
s1.makeImageSnapshot().save(p1, skia.kPNG)

# 2. Frame 2: Real India Map with Pop-Up Text Cards & Shockwave Arc
s2 = skia.Surface(W, H)
cv2 = s2.getCanvas()
draw_real_india_map(cv2, W, H)
p2 = os.path.join(out_dir, "f2_real_india_map.png")
s2.makeImageSnapshot().save(p2, skia.kPNG)

# 3. Frame 3: Full-Body Bhagwan Parashurama (Hands, Legs, Feet, Roaring Mouth)
s3 = skia.Surface(W, H)
cv3 = s3.getCanvas()
draw_cinematic_environment(cv3, "mithila_darbar", 22.0, W, H)
draw_full_body_parashurama(cv3, cx=540, ground_y=1680, scale=1.0)
p3 = os.path.join(out_dir, "f3_full_body_parashurama.png")
s3.makeImageSnapshot().save(p3, skia.kPNG)

# 4. Frame 4: Full-Body Kumar Laxman (Crown, Smirk Mouth, Sword Hand, Legs, Feet)
s4 = skia.Surface(W, H)
cv4 = s4.getCanvas()
draw_cinematic_environment(cv4, "mithila_darbar", 32.0, W, H)
draw_full_body_laxman(cv4, cx=540, ground_y=1680, scale=1.0)
p4 = os.path.join(out_dir, "f4_full_body_laxman.png")
s4.makeImageSnapshot().save(p4, skia.kPNG)

print("Rendered all 4 perfect style frames!")

# Build 2x2 Contact Sheet
cw, ch = 540, 960
sheet = Image.new("RGB", (cw * 2, ch * 2), (15, 12, 18))
sheet.paste(Image.open(p1).resize((cw, ch), Image.Resampling.LANCZOS), (0, 0))
sheet.paste(Image.open(p2).resize((cw, ch), Image.Resampling.LANCZOS), (cw, 0))
sheet.paste(Image.open(p3).resize((cw, ch), Image.Resampling.LANCZOS), (0, ch))
sheet.paste(Image.open(p4).resize((cw, ch), Image.Resampling.LANCZOS), (cw, ch))

out_local = "studio_ramayana/episodes/ep006/ep006_perfect_contact_sheet.jpg"
out_art = "C:/Users/LENOVO/.gemini/antigravity/brain/f2ebddc4-8c1b-498e-b760-53e53a5b9bcf/ep006_perfect_contact_sheet.jpg"

sheet.save(out_local, quality=94)
sheet.save(out_art, quality=94)
print("🎉 Perfect EP006 Contact Sheet Built Successfully!")
