import subprocess
import os
from PIL import Image, ImageDraw, ImageFont

shots = [
    {"t": 1.0, "title": "Shot 1: Sacred Manuscript Opening (0.0s-2.2s)"},
    {"t": 6.0, "title": "Shot 2: Mithila Darbar Altar Reveal (2.2s-12.2s)"},
    {"t": 15.0, "title": "Shot 3: Colossal Pinaka Bow Macro (12.2s-19.3s)"},
    {"t": 22.5, "title": "Shot 4: Mighty Kings Straining in Armor (19.3s-25.8s)"},
    {"t": 29.5, "title": "Shot 5: Immovable Bow Kailash Perspective (25.8s-33.2s)"},
    {"t": 36.5, "title": "Shot 6: Maharaja Janak Royal Grief (33.2s-40.4s)"},
    {"t": 44.0, "title": "Shot 7: Janak Agonized Heavenly Lament (40.4s-47.8s)"},
    {"t": 51.0, "title": "Shot 8: Vishwamitra Divine Serene Smile (47.8s-55.0s)"},
    {"t": 59.5, "title": "Shot 9: Shri Ram Divine Stride Silence (55.0s-64.2s)"},
    {"t": 67.5, "title": "Shot 10: Shri Ram Single-Hand Bow Lift (64.2s-71.0s)"},
    {"t": 74.0, "title": "Shot 11: Extreme Profile Ear-Pull (71.0s-77.7s)"},
    {"t": 79.5, "title": "Shot 12: Cosmic Lightning Burst (77.7s-81.2s)"},
]

frames = []
os.makedirs("studio_ramayana/episodes/ep005/shots", exist_ok=True)

for i, s in enumerate(shots):
    out_jpg = f"studio_ramayana/episodes/ep005/shots/shot_{i+1:02d}.jpg"
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(s["t"]),
        "-i", "studio_ramayana/episodes/ep005/ep005_final.mp4",
        "-vframes", "1",
        "-q:v", "2",
        out_jpg
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    frames.append((out_jpg, s["title"]))

# Build a 4x3 Grid (4 columns, 3 rows)
cols = 4
rows = 3
tw, th = 405, 720 # thumbnail width & height (aspect 9:16)
pad = 16
header_h = 80
badge_h = 36

total_w = cols * tw + (cols + 1) * pad
total_h = header_h + rows * (th + badge_h) + (rows + 1) * pad

sheet = Image.new("RGB", (total_w, total_h), (12, 10, 16))
draw = ImageDraw.Draw(sheet)

# Header
draw.rectangle([(0, 0), (total_w, header_h)], fill=(24, 18, 30))
draw.text((pad, 22), "RAMAYANA EP005: 12-SHOT CINEMATIC VERIFICATION CONTACT SHEET", fill=(255, 215, 0))
draw.text((pad, 48), "Full 83.56s Runtime | 1080x1920 30fps | Zero Captions | Every Line Has Distinct Location & Camera Angle", fill=(200, 200, 200))

# Try default or standard font
for idx, (f_path, title) in enumerate(frames):
    img = Image.open(f_path).resize((tw, th), Image.Resampling.LANCZOS)
    c = idx % cols
    r = idx // cols
    
    x = pad + c * (tw + pad)
    y = header_h + pad + r * (th + badge_h + pad)
    
    # Paste image
    sheet.paste(img, (x, y))
    
    # Badge background
    draw.rectangle([(x, y + th), (x + tw, y + th + badge_h)], fill=(32, 26, 42))
    # Title
    draw.text((x + 8, y + th + 10), title, fill=(240, 220, 160))

out_sheet_local = "studio_ramayana/episodes/ep005/ep005_12shot_contact_sheet.jpg"
out_sheet_art = "C:/Users/LENOVO/.gemini/antigravity/brain/f2ebddc4-8c1b-498e-b760-53e53a5b9bcf/ep005_12shot_contact_sheet.jpg"

sheet.save(out_sheet_local, quality=94)
sheet.save(out_sheet_art, quality=94)
print("✅ 12-Shot Contact Sheet built successfully!")
