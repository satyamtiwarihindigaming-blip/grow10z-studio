import os, subprocess
from PIL import Image

times = [1.0, 8.6, 17.2, 25.8, 34.4, 40.0]
frame_paths = []

for i, t in enumerate(times):
    out_f = f"out/ep01/frame_{i}.png"
    cmd = [
        "ffmpeg", "-y", "-ss", str(t), "-i", "out/ep01/ep01_final.mp4",
        "-vframes", "1", "-q:v", "2", out_f
    ]
    subprocess.run(cmd, check=True)
    frame_paths.append(out_f)

# Combine into 3 columns x 2 rows contact sheet
thumb_w, thumb_h = 360, 640
grid_w, grid_h = thumb_w * 3 + 40, thumb_h * 2 + 30
sheet = Image.new("RGB", (grid_w, grid_h), (12, 16, 28))

for idx, f_path in enumerate(frame_paths):
    img = Image.open(f_path).resize((thumb_w, thumb_h), Image.LANCZOS)
    col = idx % 3
    row = idx // 3
    x = 10 + col * (thumb_w + 10)
    y = 10 + row * (thumb_h + 10)
    sheet.paste(img, (x, y))

sheet.save("out/ep01/contact_sheet.png")
print("Contact sheet created: out/ep01/contact_sheet.png")
