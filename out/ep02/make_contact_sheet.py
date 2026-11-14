import os
import subprocess
from PIL import Image

video = "out/ep02/ep02_final.mp4"
timestamps = [2.0, 10.0, 18.0, 26.0, 36.0, 44.0]
frames = []

for i, t in enumerate(timestamps):
    out_frame = f"out/ep02/frame_{i+1}.png"
    cmd = [
        "ffmpeg", "-y", "-ss", str(t), "-i", video,
        "-vframes", "1", "-q:v", "2", out_frame
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    frames.append(out_frame)

images = [Image.open(f) for f in frames]
# Grid 3 columns x 2 rows
# Resize each frame for contact sheet (e.g. width 360, height 640)
thumb_w, thumb_h = 360, 640
thumbs = [img.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS) for img in images]

contact_sheet = Image.new("RGB", (thumb_w * 3, thumb_h * 2), (10, 10, 15))

for idx, thumb in enumerate(thumbs):
    col = idx % 3
    row = idx // 3
    contact_sheet.paste(thumb, (col * thumb_w, row * thumb_h))

contact_sheet.save("out/ep02/contact_sheet.png", quality=95)
print("Contact sheet created at out/ep02/contact_sheet.png")

# Cleanup raw extracted individual frames
for f in frames:
    if os.path.exists(f):
        os.remove(f)
